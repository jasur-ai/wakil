"""wakil state machine — P1 BRAIN (finished by ai1, D1 block).

States:
    intake → open → negotiate ⇄ (guard → send | escalate_user → user_decision)
                     ├→ verify (screenshot → vision) → close
                     └→ timeboxed / stopped

Design rules (do not violate):
- Every outbound passes BoundaryGuard BEFORE hands.send. No exceptions.
- LLM is INJECTED: `llm(prompt: str) -> str` — vendor-agnostic (OpenAI/Anthropic/local).
- Rewrite budget: 2 per message; then the user is asked (never send a 3rd draft).
- guard.escalation always stops the loop until a user.decision event.
- The agent may only close on verification.result == "confirmed".

ai1 build notes (D1):
- `_prompt()` now assembles from prompts/strategy_uz.md + the live corpus text, and
  picks the RIGHT article for the case kind (Art. 16/17 for defects, Art. 18 for a
  good-quality return) — see brain/legal_findings.md §1.
- `_classify()` is a small deterministic classifier (no model), with an optional
  `offer_parser` so P4's below-min branch is detected reliably in the demo.
- `verify()` implements the money-verification gate (local vision injected, or a
  dict when P2/P4 hand us OCR). Nothing closes without `confirmed`.
- Learning: an `accept_exception` decision is written back as a typed pref with
  provenance (case_ref), so the next mandate card is pre-filled (beat 6).
"""
from __future__ import annotations

import os
import re
from enum import Enum
from typing import Callable, Optional

from corpus import LegalCorpus
from guard import BoundaryGuard, Outbound, Verdict

STRATEGY_PATH = os.path.join(os.path.dirname(__file__), "prompts", "strategy_uz.md")

# UZ/RU surface forms that mean "here is a number, take it or leave it"
OFFER_HINTS = ("taklif", "qisman", "mo'amlа", "предлага", "частичн", "o'rniga", "kompensatsiya")
ACCEPT_HINTS = ("tasdiql", "qabul qil", "to'liq qaytar", "возврат оформ", "approved")
REFUSE_HINTS = ("rad", "o'zgartirilmaydi", "imkoni yo'q", "отказ", "yopildi")


class State(str, Enum):
    INTAKE = "intake"
    OPEN = "open"
    NEGOTIATE = "negotiate"
    ESCALATE_USER = "escalate_user"
    VERIFY = "verify"
    CLOSE = "close"
    STOPPED = "stopped"


class Agent:
    """One case = one Agent. `emit(type, payload)` is wired to P3's db.add_event."""

    def __init__(self, mandate: dict, hands, llm: Callable[[str], str], corpus: LegalCorpus, emit,
                 learn: Optional[Callable[[str, object, str], None]] = None,
                 now: Optional[Callable[[], float]] = None):
        self.m = mandate
        self.hands = hands
        self.llm = llm
        self.emit = emit
        self.learn = learn                     # (key, value, provenance) → prefs
        self.corpus = corpus
        self.case_kind = corpus.case_kind(mandate) if corpus else "unknown"
        self.guard = BoundaryGuard(mandate, corpus, now=now)
        self.state = State.OPEN
        self.turn = 0
        self.denials = 0
        self.dialog = mandate["counterpart"]["channel"]
        self.strategy = self._load_strategy()
        self.history: list[tuple[str, str]] = []   # (dir, text)

    # -- opening (turn 1 must carry the disclosure — R07) ------------------
    def open_case(self) -> str | None:
        self.turn += 1
        self.emit("case.created", {"mandate": self.m})
        return self._turn("<opening: disclose that you are the user's authorized delegate (wakil), "
                          "state the order ref, state the defect fact, state the requested remedy>", None)

    # -- one negotiation turn (inbound counterparty message) ---------------
    def run_inbound(self, text: str) -> str | None:
        self.turn += 1
        self.history.append(("in", text))
        self.emit("turn.inbound", {"text": text, "from": self.dialog})
        cls = self.classify_inbound(text)
        if cls["is_refusal"]:
            self.denials += 1
        if cls["is_acceptance"]:
            self.state = State.VERIFY
            self.emit("case.resolved", {"outcome": "counterparty_accepted", "amount": cls["amount"],
                                        "note": "awaiting verified payment before close"})
            return None
        return self._turn(text, cls)

    def _turn(self, inbound: str, cls: dict | None) -> str | None:
        """Draft → guard → (send | rewrite x2 | escalate). The ONLY path to hands.send."""
        last_instruction: str | None = None
        for _attempt in range(3):                        # 1 draft + 2 rewrites
            draft = self.llm(self._prompt(inbound, last_instruction))
            o = self._outbound(draft, inbound, cls)
            res = self.guard.check_outbound(o)
            if res.verdict is Verdict.PASS:
                res = self.guard.check_article_fit(o, self.case_kind)   # ai1, advisory R12
            if res.verdict is Verdict.PASS:
                msg_id = self.hands.send(self.dialog, draft)
                self.history.append(("out", draft))
                self.emit("turn.outbound", {"text": draft, "guard_verdict": "PASS",
                                            "msg_id": msg_id, "citations": o.citations})
                return msg_id
            if res.verdict in (Verdict.ESCALATE, Verdict.BLOCK):
                self.emit("guard.escalation", {"rule": res.rule, "violation": res.detail,
                                               "offer": (cls or {}).get("amount"),
                                               "options": res.options or ["hold", "stop"]})
                self.state = State.ESCALATE_USER
                return None
            last_instruction = res.detail                # REWRITE
        self.emit("guard.escalation", {"rule": "rewrite-budget-exhausted",
                                       "violation": "2 rewrites failed the guard — user decides",
                                       "options": ["hold", "stop"]})
        self.state = State.ESCALATE_USER
        return None

    def _outbound(self, draft: str, inbound: str, cls: dict | None) -> Outbound:
        """Intent + numbers are what R01/R02 read. We only mark a number as OURS when
        the draft actually proposes it — quoting their 300k back is not a counter-offer."""
        intent = self._classify(draft, inbound)
        amount = parse_amount(draft)
        incoming = cls.get("amount") if (cls and intent == "react_to_offer") else None
        return Outbound(text=draft, turn=self.turn, intent=intent,
                        proposed_value=amount if intent == "offer" else None,
                        incoming_value=incoming,
                        proposed_outcome=self.detect_outcome(draft),
                        citations=self.corpus.find_refs(draft) if self.corpus else [])

    # -- user answered the escalation modal --------------------------------
    def on_user_decision(self, option: str, exception: dict | None = None) -> str | None:
        self.emit("user.decision", {"option": option})
        if option == "stop":
            self.state = State.STOPPED
            self.emit("case.resolved", {"outcome": "stopped_by_user"})
            return None
        if option == "accept_exception":
            # the written exception becomes memory (beat 6): typed pref + provenance
            if self.learn and exception:
                for k, v in exception.items():
                    self.learn(k, v, f"from {self.m['case_ref']}")
            self.state = State.NEGOTIATE
            self.m.setdefault("bounds", {}).update(exception or {})
            self.guard = BoundaryGuard(self.m, self.corpus)      # re-bind to the new bounds
            return self._say("(user accepted an exception — confirm it back to the counterpart, "
                             "restate the new agreed number once, then ask for the timeline)")
        if option == "hold":
            self.state = State.NEGOTIATE
            return self._say("(user said HOLD: stay at the mandate floor, cite the corpus for THIS "
                             f"case kind — {self.case_kind})")
        return None

    # -- money verification: the only thing that may close a case ----------
    def verify(self, screenshot: object, vision: Callable[[object], dict] | None = None) -> dict:
        """`screenshot` = path or payload handed by P3; `vision` = local OCR/vision fn.
        Returns the verification.result event payload (also emitted on the case bus)."""
        expected = {"amount": float(self.m["bounds"]["min_value"]),
                    "currency": "UZS",
                    "counterpart": self.m["counterpart"].get("name", "")}
        observed = vision(screenshot) if vision else (screenshot if isinstance(screenshot, dict) else None)
        if not observed or observed.get("amount") is None:
            verdict = "unreadable"
        elif abs(float(observed["amount"]) - expected["amount"]) < 0.5:
            verdict = "confirmed"
        else:
            verdict = "mismatch"
        payload = {"expected": expected, "observed": observed, "verdict": verdict}
        self.emit("verification.result", payload)
        if verdict == "confirmed":
            self.state = State.CLOSE
            self.emit("case.resolved", {"outcome": "verified_refund",
                                        "amount": expected["amount"],
                                        "article": self._best_article()})
        return payload

    # -- internals ----------------------------------------------------------
    def _say(self, instruction: str) -> str | None:
        """One more gated message (used by the hold / accept_exception paths)."""
        self.turn += 1
        return self._turn(instruction, None)

    @staticmethod
    def classify_inbound(text: str) -> dict:
        """Analyse the COUNTERPARTY's message: offer / acceptance / refusal + the number."""
        t = (text or "").lower()
        return {"is_offer": any(h in t for h in OFFER_HINTS),
                "is_acceptance": any(h in t for h in ACCEPT_HINTS),
                "is_refusal": any(h in t for h in REFUSE_HINTS),
                "amount": parse_amount(t)}

    def _classify(self, draft: str, inbound: str = "") -> str:
        """Classify the AGENT's own draft to a guard intent (R01/R02 key off this).

        Rule: any number we put on the table that is NOT the number they just said is a
        counter-offer — verb-phrasing is too easy to miss ("...qilib tursak-chi?" is a
        proposal in UZ but matches no verb list). Quoting their number back is not.
        Verbs are still honoured so an unambiguous proposal is caught even without an
        inbound offer to compare against."""
        t = (draft or "").lower()
        amount = parse_amount(t)
        theirs = parse_amount((inbound or "").lower())
        if amount is not None and any(
                v in t for v in ("qilib beramiz", "qilib tursak", "taklif qilamiz", "rozimiz",
                                 "kelishamiz", "hisoblab beramiz", "qo'shib", "qoʻshib")):
            return "offer"
        if amount is not None and theirs is not None and amount != theirs:
            return "counter"
        if amount is not None and theirs is not None and any(h in (inbound or "").lower() for h in OFFER_HINTS):
            return "react_to_offer"
        return "message"

    @staticmethod
    def detect_outcome(draft: str) -> str | None:
        """Which remedy the draft actually asks for → R02 whitelist check."""
        t = (draft or "").lower()
        for word, outcome in (("to'liq qaytar", "full_refund"), ("qisman qaytar", "partial_refund"),
                              ("almasht", "exchange"), ("ta'mir", "warranty_repair"),
                              ("chegirma", "discount"), ("o'rniga qo'y", "replacement")):
            if word in t:
                return outcome
        return None

    def _best_article(self) -> str | None:
        e = self.corpus.cite("nuqsonli tovar pulni qaytarish" if self.case_kind == "defect"
                             else "maqbul sifatli tovarni almashtirish", 1, self.case_kind)
        return e[0]["ref"] if e else None

    def _allowed_articles(self) -> list[str]:
        """Corpus refs the prompt is allowed to mention for THIS case kind."""
        if not self.corpus:
            return []
        return [e["ref"] for e in self.corpus.all()
                if e["kind"] == "law" and self.corpus.quotable(e["ref"])
                and self.corpus.article_applies_to(e["ref"]) in (self.case_kind, "both")]

    def _load_strategy(self) -> str:
        try:
            with open(STRATEGY_PATH, encoding="utf-8") as f:
                return f.read()
        except OSError:
            return ""

    def _prompt(self, inbound: str, instruction: str | None) -> str:
        b = self.m["bounds"]
        allowed = self._allowed_articles()
        cites = "\n".join(
            f"  - {r}: {self.corpus.get(r)['body'][:220]}" for r in allowed) or "  (corpus empty — do NOT cite any article)"
        parts = [
            "wakil agent. You act ONLY inside this mandate:",
            f"objective: {self.m['objective']}",
            f"case kind: {self.case_kind}",
            f"floor: {b['min_value']} UZS, max: {b.get('max_value', b['min_value'])} UZS",
            f"acceptable outcomes: {b['acceptable_outcomes']}",
            f"strategy: {self.m['strategy']}",
            f"state escalation allowed: {b.get('allow_state_threat', False)}",
            f"evidence you may reference (nothing else): {self._evidence_refs()}",
            "",
            "LEGAL MOVES — you may cite ONLY these corpus refs, verbatim sense, no others:",
            cites,
            "",
            "Dialogue so far (last 6):",
            *[f"  {d}: {t[:160]}" for d, t in self.history[-6:]],
            f"counterpart just said: {inbound}",
        ]
        if instruction:
            parts.append(f"GATE INSTRUCTION (fix exactly this): {instruction}")
        parts.append("Reply in Uzbek, 1-2 sentences, no markdown, no invented article numbers.")
        return "\n".join(parts)

    def _evidence_refs(self) -> str:
        vals = []
        for e in self.m.get("evidence") or []:
            vals.extend((e.get("data") or {}).values())
        return ", ".join(str(v) for v in vals) or "(none)"


def parse_amount(text: str) -> float | None:
    """Largest UZS figure: '300 000 so'm', '450k', '1,6 mlrd'."""
    best = None
    for m in re.finditer(r"(\d[\d\s.,]*)\s*(kuber|k\b|mln|mlrd|so'?m|UZS)", text, re.IGNORECASE):
        raw = m.group(1).replace(" ", "").replace(",", ".")
        try:
            v = float(raw)
        except ValueError:
            continue
        mult = {"k": 1e3, "kuber": 1e3, "mln": 1e6, "mlrd": 1e9}.get(m.group(2).lower(), 1)
        v *= mult
        if best is None or v > best:
            best = v
    return best
