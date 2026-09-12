"""wakil state machine — SKELETON (ai1 finishes, D2, per docs/team-battle-plan.md P1).

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

TODO(ai1): _classify(), prompt building from prompts/strategy_uz.md,
Whisper(uz) slot extraction → mandate prefill, verify() with local vision,
learning loop (typed prefs + provenance), eval harness (10 transcripts).
"""
from __future__ import annotations

from enum import Enum
from typing import Callable

from corpus import LegalCorpus
from guard import BoundaryGuard, Outbound, Verdict


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

    def __init__(self, mandate: dict, hands, llm: Callable[[str], str], corpus: LegalCorpus, emit):
        self.m = mandate
        self.hands = hands
        self.llm = llm
        self.emit = emit
        self.guard = BoundaryGuard(mandate, corpus)
        self.corpus = corpus
        self.state = State.OPEN
        self.turn = 0
        self.dialog = mandate["counterpart"]["channel"]

    # -- one negotiation turn (inbound counterparty message) ---------------
    def run_inbound(self, text: str):
        self.turn += 1
        self.emit("turn.inbound", {"text": text, "from": self.dialog})
        last_instruction: str | None = None
        for _attempt in range(3):  # 1 draft + 2 rewrites
            draft = self.llm(self._prompt(text, last_instruction))
            o = Outbound(text=draft, turn=self.turn, intent=self._classify(draft, text))
            res = self.guard.check_outbound(o)
            if res.verdict is Verdict.PASS:
                msg_id = self.hands.send(self.dialog, draft)
                self.emit("turn.outbound", {"text": draft, "guard_verdict": "PASS", "msg_id": msg_id})
                return
            if res.verdict is Verdict.ESCALATE or res.verdict is Verdict.BLOCK:
                self.emit("guard.escalation", {"rule": res.rule, "violation": res.detail,
                                               "options": res.options or ["hold", "stop"]})
                self.state = State.ESCALATE_USER
                return
            last_instruction = res.detail  # REWRITE
        self.emit("guard.escalation", {"rule": "rewrite-budget-exhausted",
                                       "violation": "2 rewrites failed the guard — user decides",
                                       "options": ["hold", "stop"]})
        self.state = State.ESCALATE_USER

    # -- user answered the escalation modal --------------------------------
    def on_user_decision(self, option: str):
        self.emit("user.decision", {"option": option})
        if option == "stop":
            self.state = State.STOPPED
            self.emit("case.resolved", {"outcome": "stopped_by_user"})
        elif option == "hold":
            self.state = State.NEGOTIATE
            self.turn += 1
            draft = self.llm(self._prompt("(user said HOLD: stay at the mandate floor, cite the corpus if useful)", None))
            o = Outbound(text=draft, turn=self.turn)
            res = self.guard.check_outbound(o)
            if res.verdict is Verdict.PASS:
                self.hands.send(self.dialog, draft)
                self.emit("turn.outbound", {"text": draft, "guard_verdict": "PASS"})
        elif option == "accept_exception":
            # TODO(ai1): record the exception in prefs with provenance + continue within the EXCEPTION bounds
            self.state = State.NEGOTIATE

    # -- internals -----------------------------------------------------------
    def _classify(self, draft: str, inbound: str) -> str:
        """TODO(ai1): light classifier (heuristic now)."""
        if inbound and ("qaytarish" in inbound.lower() or "taklif" in inbound.lower()):
            return "react_to_offer"
        return "message"

    def _prompt(self, inbound: str, instruction: str | None) -> str:
        """TODO(ai1): assemble from prompts/strategy_uz.md + mandate + last N messages (hands.observe)."""
        b = self.m["bounds"]
        parts = [
            "wakil agent. You act ONLY inside this mandate:",
            f"objective: {self.m['objective']}",
            f"floor: {b['min_value']} UZS, max: {b.get('max_value', b['min_value'])} UZS",
            f"acceptable outcomes: {b['acceptable_outcomes']}",
            f"strategy: {self.m['strategy']}",
            f"state escalation allowed: {b.get('allow_state_threat', False)}",
            f"inbound from counterpart: {inbound}",
        ]
        if instruction:
            parts.append(f"GATE INSTRUCTION (fix this): {instruction}")
        parts.append("Reply in Uzbek, 1-2 sentences, no markdown.")
        return "\n".join(parts)
