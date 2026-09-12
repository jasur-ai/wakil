"""BoundaryGuard test suite — 16 tests, stdlib only.

Run:  python test_guard.py     (or:  pytest -q test_guard.py)
The green suite IS the trust story: no out-of-bounds message ever leaves the device.
"""
import time

import corpus as C
import guard as G
from guard import BoundaryGuard, Outbound, Verdict, validate_mandate


def make_mandate(**over) -> dict:
    m = {
        "case_ref": "M-0001",
        "objective": "to'liq qaytarish: nosoz iPhone 15 (ekran defekti)",
        "counterpart": {"name": "Uzum Marketplace", "channel": "@UzumSupport"},
        "bounds": {
            "min_value": 450000,
            "max_value": 450000,
            "acceptable_outcomes": ["full_refund"],
            "max_wait_hours": 48,
            "non_negotiables": ["450k dan past bo'lmagan qisman to'lov"],
            "allow_state_threat": False,
        },
        "evidence": [
            {"kind": "order_ref", "ref": "order", "data": {"order": "UZ-778-112"}},
            {"kind": "screenshot", "ref": "photo1", "data": {}},
        ],
        "strategy": "meherban doimiylik, faktlar, 2 rad etishda eskalyatsiya",
        "created_at_ts": time.time(),
    }
    m.update(over)
    return m


def mk(text: str, **kw) -> Outbound:
    d = {"turn": 2, "intent": "message"}
    d.update(kw)
    return Outbound(text=text, **d)


# -- PASS ----------------------------------------------------------------
def test_pass_basic():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("Assalomu alaykum! Buyurtma UZ-778-112 bo'yicha to'liq qaytarish so'rayman. Men foydalanuvchi wakiliman."))
    assert res.verdict is Verdict.PASS, res


# -- R01 value bounds ----------------------------------------------------
def test_r01_offer_below_floor_escalates():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("rad etamiz", intent="react_to_offer", incoming_value=300000))
    assert res.verdict is Verdict.ESCALATE and res.rule == "R01-value-bounds"
    assert res.options == ["accept_exception", "hold", "stop"]


def test_r01_propose_below_floor_blocks():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("400 000 so'm qilib beramiz", intent="counter", proposed_value=400000))
    assert res.verdict is Verdict.BLOCK and res.rule == "R01-value-bounds"
    assert g.incidents


def test_r01_propose_above_max_rewrites():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("500 000 so'm taklif qilamiz", intent="counter", proposed_value=500000))
    assert res.verdict is Verdict.REWRITE and res.rule == "R01-value-bounds"


# -- R02 outcome whitelist ------------------------------------------------
def test_r02_outcome_not_whitelisted_escalates():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("almashtirish taklif qilamiz", proposed_outcome="exchange"))
    assert res.verdict is Verdict.ESCALATE and res.rule == "R02-outcome-whitelist"


# -- R03 data allowlist ----------------------------------------------------
def test_r03_pii_not_in_evidence_blocks():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("Telefonim +998 90 123 45 67, qo'ng'iroq qiling"))
    assert res.verdict is Verdict.BLOCK and res.rule == "R03-data-allowlist"


def test_r03_evidence_data_allowed():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("Assalomu alaykum, men wakilman. Buyurtma raqami UZ-778-112 bo'yicha qaytarish kerak.", turn=1))
    assert res.verdict is Verdict.PASS, res


# -- R04 tone --------------------------------------------------------------
def test_r04_aggressive_blocks():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("Bu juda qaysar qaror, darhol to'lang!"))
    assert res.verdict is Verdict.BLOCK and res.rule == "R04-tone"


# -- R05 irreversible ------------------------------------------------------
def test_r05_irreversible_escalates():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("buyurtmani bekor qilamiz", intent="cancel_order", action_class="irreversible"))
    assert res.verdict is Verdict.ESCALATE and res.rule == "R05-irreversible-tap"


# -- R06 timebox -----------------------------------------------------------
def test_r06_timebox_rewrites():
    m = make_mandate()
    m["created_at_ts"] = 0.0
    g = BoundaryGuard(m, now=lambda: 50 * 3600)
    res = g.check_outbound(mk("keyinroq javob berasizmi"))
    assert res.verdict is Verdict.REWRITE and res.rule == "R06-timebox"


# -- R07 disclosure ---------------------------------------------------------
def test_r07_missing_disclosure_rewrites():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("Assalomu alaykum, qaytarish kerak", turn=1))
    assert res.verdict is Verdict.REWRITE and res.rule == "R07-disclosure"


# -- R08 language -----------------------------------------------------------
def test_r08_no_language_rewrites():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("42"))
    assert res.verdict is Verdict.REWRITE and res.rule == "R08-language"


# -- R09 citations -----------------------------------------------------------
def test_r09_hallucinated_citation_blocks():
    c = C.LegalCorpus(); c.seed_default()
    g = BoundaryGuard(make_mandate(), corpus=c)
    res = g.check_outbound(mk("Qonunning 99-moddasiga ko'ra siz majbursiz"))
    assert res.verdict is Verdict.BLOCK and res.rule == "R09-citation-must-resolve"


def test_r09_real_citation_passes():
    c = C.LegalCorpus(); c.seed_default()
    g = BoundaryGuard(make_mandate(), corpus=c)
    res = g.check_outbound(mk("18-moddaga ko'ra 10 kunlik qaytarish huquqim bor"))
    assert res.verdict is Verdict.PASS, res


# -- R11 state threat ---------------------------------------------------------
def test_r11_state_blocked_when_not_allowed():
    g = BoundaryGuard(make_mandate())
    res = g.check_outbound(mk("Davlat agentligiga shikoyat beraman"))
    old = res.verdict
    assert old is Verdict.BLOCK and res.rule == "R11-state-threat"


def test_r11_state_allowed_when_preauthorized():
    m = make_mandate()
    m["bounds"]["allow_state_threat"] = True
    g = BoundaryGuard(m)
    res = g.check_outbound(mk("Davlat agentligiga (1159) murojaat qilaman"))
    assert res.verdict is Verdict.PASS, res


# -- mandate validation ---------------------------------------------------------
def test_validate_mandate():
    assert validate_mandate(make_mandate()) == []
    broken = make_mandate()
    del broken["objective"]
    broken["case_ref"] = "X-1"
    broken["bounds"].pop("min_value")
    errs = validate_mandate(broken)
    assert any("objective" in e for e in errs)
    assert any("min_value" in e for e in errs)
    assert any("case_ref" in e for e in errs)


ALL = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]

if __name__ == "__main__":
    failed = 0
    for fn in ALL:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {fn.__name__}: {e}")
    print(f"\n{len(ALL) - failed}/{len(ALL)} tests passed")
    raise SystemExit(1 if failed else 0)
