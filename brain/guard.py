"""wakil BoundaryGuard — the only door between the agent's brain and the world.

The LLM may *want* to say anything. The Guard decides what may leave the device.

Verdicts:
    PASS      — send as is
    REWRITE   — do not send; `detail` tells the LLM what to fix (budget: 2 rewrites)
    ESCALATE  — do not send; the user must choose: accept_exception | hold | stop
    BLOCK     — never send; logged as an incident

Rules (checked in order, first hit wins):
    R01 value bounds        — offers below the user's floor; counters below floor (BLOCK) / above max (REWRITE)
    R02 outcome whitelist   — only `acceptable_outcomes` may be proposed
    R03 data allowlist      — only `evidence` data may leave (PII patterns blocked)
    R04 tone                — no aggression / no all-caps
    R05 irreversible tap    — cancel/refund/complaint-class actions need the user's tap
    R06 timebox             — after max_wait_hours the agent must stop and ask
    R07 disclosure          — first message must disclose representation
    R08 language            — outbound must be Uzbek or Russian
    R09 citation must resolve — "N-modda" must exist in the LegalCorpus (no invented law)
    R10 dossier completeness — all 8 sections present (enforced via check_dossier)
    R11 state threat        — 1159 / agency / court only if allow_state_threat=true

Advisory (opt-in, NOT in the default chain — ai1, see legal_findings.md):
    R12 article fit         — citing Art. 18 (good-quality exchange) in a DEFECT case, or
                              16/17 in a no-defect case, is legally wrong even though the
                              article exists. Also: never quote text from a corpus entry the
                              corpus itself marks non-quotable. Exposed as
                              `check_article_fit()` and called by the Agent before send, so
                              the D0 gate suite stays exactly as rehearsed.

Stdlib only. Run the tests:  python test_guard.py
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional


class Verdict(str, Enum):
    PASS = "pass"
    REWRITE = "rewrite"
    ESCALATE = "escalate"
    BLOCK = "block"


@dataclass
class Outbound:
    """What the agent is trying to send. `turn` is 1-indexed per case."""
    text: str
    turn: int = 1
    intent: str = "message"            # message | counter | offer | react_to_offer | close | final | <action>
    action_class: str = "none"         # none | reversible | irreversible
    proposed_value: Optional[float] = None    # money the agent proposes (UZS)
    incoming_value: Optional[float] = None    # money the counterparty offered (UZS)
    proposed_outcome: Optional[str] = None    # e.g. "full_refund"
    media: list = field(default_factory=list)
    citations: list = field(default_factory=list)   # e.g. ["18-modda"]


@dataclass
class GuardResult:
    verdict: Verdict
    rule: str
    detail: str
    options: list = field(default_factory=list)

    @property
    def allowed(self) -> bool:
        return self.verdict is Verdict.PASS


# ---------------------------------------------------------------- helpers

# R07 matches what the LLM and the counterparty actually WRITE. The brand is `wakil`
# (AGENTS.md rule 1) and every piece of outbound copy uses it — but the Uzbek dictionary
# word for "representative" is spelled with a v, so the model sometimes writes that form.
# Accepting ONLY the brand spelling would make the guard REWRITE a natural, correct
# disclosure sentence, i.e. "fix" valid Uzbek into worse Uzbek. Both forms pass here;
# this list is a matcher, never brand copy.
DISCLOSURE_MARKERS = ("wakil", "wakilman", "vakil", "vakilman", "vakolat", "vaakil", "wakolat",
                      "delegate", "mening wakilim", "bizning vakilimiz", "authorized delegate")
STATE_MARKERS = ("1159", "consumergovuz", "agentlig", "davlat", "state agency", "sudga", "sudda", "court")
AGGRESSIVE = ("qaysar", "ahmoq", "oskor", "qo'pol", "fuck", "shit", "idiot", "тварь", "сука", "дурак", "идиот")
PII_RES = (
    re.compile(r"\+?\d[\d\s\-()]{7,}\d"),      # phone-ish: 9+ digits
    re.compile(r"\b\d{16}\b"),                  # card number
    re.compile(r"\b\d{3} ?\d{3} ?\d{3} ?\d\b"),  # id-ish
)
# UZ/RU are the working languages of the arena; anything else is a rewrite, not a suggestion.
FOREIGN_WORDS = ("would", "like", "request", "refund", "under", "our", "policy", "please",
                 "we", "your", "the", "and", "have", "been", "money", "back", "according",
                 "article", "law", "hereby", "require", "consider", "dear")
UZ_RU_WORDS = ("so'm", "sum", "buyurtma", "qaytar", "modda", "tasdiq", "rad", "beramiz",
               "qilamiz", "so'raymiz", "vakil", "rizino", "vakolat", "возврат", "просим",
               "товар", "ден", "шу", "holat", "taklif", "asos")
MONEY_RE = re.compile(r"(\d[\d\s.,]*)\s*(k\b|so'?m\b|UZS\b)", re.IGNORECASE)


def parse_money(text: str) -> Optional[float]:
    """Largest monetary figure in the text ('450 000 so'm', '300k')."""
    best: Optional[float] = None
    for m in MONEY_RE.finditer(text):
        raw = m.group(1).replace(" ", "").replace(",", ".")
        try:
            val = float(raw)
        except ValueError:
            continue
        if m.group(2).lower() == "k":
            val *= 1000.0
        if best is None or val > best:
            best = val
    return best


def find_article_refs(text: str) -> list[str]:
    """Article references in a message: '18-modda', '18-moddasining', '18-modda', 'Article 18'."""
    refs: set[str] = set()
    for m in re.finditer(r"(\d{1,3})\s*[-–]\s*(?:modda|moddasi)", text, re.IGNORECASE):
        refs.add(f"{m.group(1)}-modda")
    for m in re.finditer(r"modda(?:sining|si)?\s*(\d{1,3})", text, re.IGNORECASE):
        refs.add(f"{m.group(1)}-modda")
    for m in re.finditer(r"\barticle\s+(\d{1,3})\b", text, re.IGNORECASE):
        refs.add(f"{m.group(1)}-modda")
    return sorted(refs)


# ---------------------------------------------------------------- the guard

class BoundaryGuard:
    def __init__(self, mandate: dict, corpus=None, now: Optional[Callable[[], float]] = None):
        self.m = mandate
        self.corpus = corpus            # LegalCorpus; in production ALWAYS provided (R09 needs it)
        self.now = now or time.time
        b = mandate["bounds"]
        self.min_v = float(b["min_value"])
        self.max_v = float(b.get("max_value", b["min_value"]))
        self.outcomes = {str(o).lower() for o in b["acceptable_outcomes"]}
        self.allow_state = bool(b.get("allow_state_threat", False))
        self.max_wait_h = float(b["max_wait_hours"])
        self.evidence = mandate.get("evidence") or []
        self.case_started = float(mandate.get("created_at_ts", self.now()))
        self.incidents: list[str] = []

    # -- entry point ------------------------------------------------------
    def check_outbound(self, o: Outbound) -> GuardResult:
        for rule in (self.r01_value_bounds, self.r02_outcome_whitelist, self.r03_data_allowlist,
                     self.r04_tone, self.r05_irreversible, self.r06_timebox, self.r07_disclosure,
                     self.r08_language, self.r09_citation, self.r11_state_threat):
            res = rule(o)
            if res is not None:
                return res
        return GuardResult(Verdict.PASS, "none", "ok")

    def check_dossier(self, report: dict) -> GuardResult:
        """R10 — a dossier may only be exported when all 8 sections are non-empty."""
        missing = [s for s, v in report.items() if not str(v or "").strip()]
        if missing:
            return GuardResult(Verdict.BLOCK, "R10-dossier-completeness", f"dossier incomplete: {missing}")
        return GuardResult(Verdict.PASS, "R10-dossier-completeness", "all sections present")

    # -- rules ------------------------------------------------------------
    def r01_value_bounds(self, o: Outbound) -> Optional[GuardResult]:
        if o.intent == "react_to_offer" and o.incoming_value is not None:
            if o.incoming_value < self.min_v:
                return GuardResult(Verdict.ESCALATE, "R01-value-bounds",
                    f"counterparty offered {o.incoming_value:.0f} — below your floor {self.min_v:.0f}",
                    options=["accept_exception", "hold", "stop"])
            return None
        if o.proposed_value is not None:
            if o.proposed_value < self.min_v:
                self.incidents.append(f"R01 proposed {o.proposed_value:.0f} < floor {self.min_v:.0f}")
                return GuardResult(Verdict.BLOCK, "R01-value-bounds",
                    "agent proposed below the user's floor — dropped")
            if o.proposed_value > self.max_v:
                return GuardResult(Verdict.REWRITE, "R01-value-bounds",
                    f"do not propose above the user's max {self.max_v:.0f}")
        if o.intent in ("counter", "offer"):
            parsed = parse_money(o.text)
            if parsed is not None and parsed < self.min_v:
                self.incidents.append(f"R01 text proposes {parsed:.0f} < floor {self.min_v:.0f}")
                return GuardResult(Verdict.BLOCK, "R01-value-bounds",
                    "message proposes a value below the user's floor")
        return None

    def r02_outcome_whitelist(self, o: Outbound) -> Optional[GuardResult]:
        if o.proposed_outcome and o.proposed_outcome.lower() not in self.outcomes:
            return GuardResult(Verdict.ESCALATE, "R02-outcome-whitelist",
                f"'{o.proposed_outcome}' is not in your acceptable outcomes {sorted(self.outcomes)}",
                options=["accept_exception", "hold", "stop"])
        return None

    def _evidence_blob(self) -> str:
        parts = []
        for e in self.evidence:
            parts.append(str(e.get("ref", "")))
            for v in (e.get("data") or {}).values():
                parts.append(str(v))
        return " ".join(parts)

    def r03_data_allowlist(self, o: Outbound) -> Optional[GuardResult]:
        blob = self._evidence_blob()
        for rx in PII_RES:
            for m in rx.finditer(o.text):
                hit = m.group(0).strip()
                if len(re.sub(r"\D", "", hit)) >= 9 and hit not in blob:
                    self.incidents.append(f"R03 data outside evidence allowlist: {hit[:4]}…")
                    return GuardResult(Verdict.BLOCK, "R03-data-allowlist",
                        "message contains data that is not in the evidence allowlist — dropped")
        for ref in o.media:
            if not any(e.get("ref") == ref for e in self.evidence):
                self.incidents.append(f"R03 media {ref} not in evidence allowlist")
                return GuardResult(Verdict.BLOCK, "R03-data-allowlist",
                    f"media '{ref}' is not in the evidence allowlist")
        return None

    def r04_tone(self, o: Outbound) -> Optional[GuardResult]:
        t = o.text.lower()
        for w in AGGRESSIVE:
            if w in t:
                self.incidents.append(f"R04 aggressive word: {w}")
                return GuardResult(Verdict.BLOCK, "R04-tone", f"aggressive word '{w}' — dropped")
        letters = [c for c in o.text if c.isalpha()]
        caps = [c for c in letters if c.isupper()]
        if letters and len(caps) / len(letters) > 0.6 and len(o.text) > 20:
            return GuardResult(Verdict.REWRITE, "R04-tone", "all-caps shouting — rewrite calmly, same content")
        return None

    def r05_irreversible(self, o: Outbound) -> Optional[GuardResult]:
        if o.action_class == "irreversible":
            return GuardResult(Verdict.ESCALATE, "R05-irreversible-tap",
                f"irreversible action '{o.intent}' requires the user's tap",
                options=["accept_exception", "hold", "stop"])
        return None

    def r06_timebox(self, o: Outbound) -> Optional[GuardResult]:
        elapsed_h = (self.now() - self.case_started) / 3600.0
        if elapsed_h > self.max_wait_h and o.intent not in ("close", "final"):
            return GuardResult(Verdict.REWRITE, "R06-timebox",
                f"mandate timebox reached ({elapsed_h:.0f}h > {self.max_wait_h:.0f}h) — stop negotiating and ask the user")
        return None

    def r07_disclosure(self, o: Outbound) -> Optional[GuardResult]:
        if o.turn == 1 and not any(m in o.text.lower() for m in DISCLOSURE_MARKERS):
            return GuardResult(Verdict.REWRITE, "R07-disclosure",
                "first message must disclose representation — say you are the user's authorized delegate (wakil)")
        return None

    def r08_language(self, o: Outbound) -> Optional[GuardResult]:
        latin = len(re.findall(r"[a-zʻ]", o.text, re.IGNORECASE))
        cyr = len(re.findall(r"[а-яё]", o.text, re.IGNORECASE))
        if max(latin, cyr) < 3:
            return GuardResult(Verdict.REWRITE, "R08-language", "outbound must be Uzbek or Russian — rewrite in uz or ru")
        # Script alone is not language: an English sentence passes the check above, and
        # an English demand at a Tashkent marketplace support desk is a lost case, not a
        # style choice. Detect the foreign-function-word signature and send it back.
        t = " " + re.sub(r"[^a-z'ʻ]+", " ", o.text.lower()) + " "
        foreign = sum(1 for w in FOREIGN_WORDS if f" {w} " in t)
        local = sum(1 for w in UZ_RU_WORDS if f" {w} " in t)
        if foreign >= 2 and local == 0:
            return GuardResult(Verdict.REWRITE, "R08-language",
                "this reads as a foreign language — rewrite in Uzbek (or Russian if the "
                "counterparty wrote in Russian); the counterpart is a UZ support desk")
        return None

    def r09_citation(self, o: Outbound) -> Optional[GuardResult]:
        if self.corpus is None:
            return None  # production always passes a corpus; None = unit-test mode
        refs = find_article_refs(o.text)
        for c in o.citations or []:
            if c not in refs:
                refs.append(c)
        for ref in refs:
            if self.corpus.get(ref) is None:
                self.incidents.append(f"R09 unresolved citation: {ref}")
                return GuardResult(Verdict.BLOCK, "R09-citation-must-resolve",
                    f"'{ref}' does not exist in the legal corpus — never invent law; remove it or re-derive from the corpus")
        return None

    def r11_state_threat(self, o: Outbound) -> Optional[GuardResult]:
        t = o.text.lower()
        for w in STATE_MARKERS:
            if w in t and not self.allow_state:
                self.incidents.append(f"R11 state escalation without pre-authorization: {w}")
                return GuardResult(Verdict.BLOCK, "R11-state-threat",
                    f"'{w}' — state escalation (agency/1159/court) requires allow_state_threat=true in the mandate")
        return None

    # -- R12 advisory (ai1): a real article used in the wrong kind of case --
    def check_article_fit(self, o: Outbound, case_kind: str) -> GuardResult:
        """An article can EXIST in the corpus and still be the wrong one to wave at a
        seller. Art. 18 = exchange of a *good-quality* item; Art. 16/17 = *defective*
        goods. Our demo case (nosoz iPhone, ekran defekti) is a defect case: citing 18
        there is the fastest way for a human manager — or a lawyer in the jury — to
        dismiss the whole claim. Advisory by design: called from the Agent, not from
        check_outbound, so the rehearsed D0 gate suite is untouched."""
        if self.corpus is None:
            return GuardResult(Verdict.PASS, "R12-article-fit", "no corpus — fit not checked")
        refs = o.citations or self.corpus.find_refs(o.text)
        for ref in refs:
            entry = self.corpus.get(ref)
            if entry and not self.corpus.quotable(ref):
                return GuardResult(Verdict.REWRITE, "R12-article-fit",
                    f"'{ref}' is in the corpus but its text is unverified — argue the facts, do not quote it")
            applies = self.corpus.article_applies_to(ref)
            if applies in ("defect", "quality") and case_kind in ("defect", "quality") \
                    and applies != case_kind:
                want = "16-modda / 17-modda" if case_kind == "defect" else "18-modda"
                return GuardResult(Verdict.REWRITE, "R12-article-fit",
                    f"'{ref}' governs {applies}-goods cases, this is a {case_kind} case — "
                    f"cite {want} instead (never the other way round, never invent)")
        return GuardResult(Verdict.PASS, "R12-article-fit", "ok")


# ---------------------------------------------------------------- mandate validation

MANDATE_REQUIRED = ("case_ref", "objective", "counterpart", "bounds", "strategy", "evidence")
BOUNDS_REQUIRED = ("min_value", "acceptable_outcomes", "max_wait_hours", "non_negotiables")


def validate_mandate(m: dict) -> list[str]:
    """Used by onboarding (UI + POST /case). Returns a list of problems (empty = valid)."""
    errs: list[str] = []
    for f in MANDATE_REQUIRED:
        if not m.get(f):
            errs.append(f"missing: {f}")
    b = m.get("bounds") or {}
    for f in BOUNDS_REQUIRED:
        if f not in b:
            errs.append(f"bounds missing: {f}")
    try:
        if float(b.get("min_value", -1)) < 0:
            errs.append("min_value must be >= 0")
    except (TypeError, ValueError):
        errs.append("min_value must be a number")
    if not isinstance(b.get("acceptable_outcomes"), list) or not b.get("acceptable_outcomes"):
        errs.append("acceptable_outcomes must be a non-empty list")
    if not re.match(r"^M-\d{4}$", str(m.get("case_ref", ""))):
        errs.append("case_ref must match M-0000")
    return errs
