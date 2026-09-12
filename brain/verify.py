"""wakil money verification — the gate between "they said yes" and "case closed" (ai1, D2).

Product rule 4: wakil reports success only after the money is verified. This module is
that check. Vision/OCR is INJECTED (local model on the booth laptop — D0-5), so the
decision logic here is pure, testable, and vendor-free.

verdict:
    confirmed   — amount AND currency match the mandate floor  → only this may close
    mismatch    — readable, but the number is wrong (partial pay, wrong currency)
    unreadable  — no amount could be parsed → never close, never claim failure either

Run: python verify.py   → fixture self-test (5 screenshots: 2 match / 2 mismatch / 1 garbage)
"""
from __future__ import annotations

import re
from typing import Callable, Optional

AMOUNT_RE = re.compile(r"(\d[\d\s.,_]{2,})\s*(so'?m[a-zа-яё]*|UZS|сўм[a-zа-яё]*|сум[a-zа-яё]*|USDT|USD|EUR|RUB)", re.IGNORECASE)
# a UZ wallet says "so'm", the law says "UZS", OCR says "сум" — same currency. Normalizing
# here (not in the mandate) keeps the mandate honest and the matcher from calling a match a
# mismatch, which would refuse to close a case we actually won.
CUR_CANON = {"SOM": "UZS", "SO M": "UZS", "SUM": "UZS", "UZS": "UZS", "СУМ": "UZS",
             "СЎМ": "UZS", "USDT": "USDT", "USD": "USD", "EUR": "EUR", "RUB": "RUB"}


def canon_currency(raw) -> str:
    if not raw:
        return "UZS"
    key = re.sub(r"[^A-ZА-ЯЁЎ]", "", str(raw).upper())
    return CUR_CANON.get(key, key or "UZS")


def parse_ocr(text: str) -> dict:
    """Raw OCR string → {amount, currency}. Best-effort on purpose: a screenshot is noisy.
    Returns amount=None when nothing money-shaped is present (→ `unreadable`)."""
    if not text:
        return {"amount": None, "currency": None}
    best = None
    cur = None
    for m in AMOUNT_RE.finditer(text):
        raw = re.sub(r"[^\d.]", "", m.group(1).replace(" ", ""))
        if raw.count(".") > 1:
            raw = raw.replace(".", "")[:-1] if len(raw.split(".")[-1]) in (2, 3) else raw.replace(".", "")
        try:
            v = float(raw)
        except ValueError:
            continue
        if best is None or v > best:
            best, cur = v, canon_currency(m.group(2))
    return {"amount": best, "currency": cur}


def expected_from_mandate(mandate: dict) -> dict:
    b = mandate["bounds"]
    return {"amount": float(b["min_value"]), "currency": "UZS",
            "counterpart": mandate.get("counterpart", {}).get("name", ""),
            "accept_max": bool(b.get("max_value", b["min_value"]))}


def verdict(expected: dict, observed: Optional[dict], *, tolerance: float = 0.5) -> dict:
    """Compare what the mandate demands with what the screenshot shows."""
    if not observed or observed.get("amount") is None:
        return {"verdict": "unreadable", "reason": "amount not legible on the screenshot",
                "expected": expected, "observed": observed or {}}
    got = float(observed["amount"])
    want = float(expected["amount"])
    exp_cur = canon_currency(expected.get("currency") or "UZS")
    got_cur = canon_currency(observed.get("currency") or "UZS")
    if got_cur != exp_cur:
        return {"verdict": "mismatch", "reason": f"currency {got_cur} != {exp_cur}",
                "expected": expected, "observed": observed}
    if abs(got - want) <= tolerance:
        return {"verdict": "confirmed", "reason": "amount matches the mandate floor",
                "expected": expected, "observed": observed}
    if got < want:
        return {"verdict": "mismatch", "reason": f"paid {got:.0f} < floor {want:.0f} (partial?)",
                "expected": expected, "observed": observed}
    return {"verdict": "mismatch", "reason": f"paid {got:.0f} > floor {want:.0f} — confirm with user",
            "expected": expected, "observed": observed}


def event_payload(expected: dict, observed: Optional[dict], v: dict) -> dict:
    """contracts/02 → verification.result {expected, observed, verdict}."""
    return {"expected": expected, "observed": observed or {}, "verdict": v["verdict"],
            "reason": v["reason"]}


FIXTURES = [
    ("wallet_ok_card", {"amount": 450000, "currency": "UZS", "payer": "Uzum Market"}, "confirmed"),
    ("wallet_ok_str", parse_ocr("Postuplenie +450 000 so'm  Uzum Market  12.09 14:03"), "confirmed"),
    ("wallet_partial", {"amount": 300000, "currency": "UZS", "payer": "Uzum Market"}, "mismatch"),
    ("wallet_wrong_currency", {"amount": 450000, "currency": "USD"}, "mismatch"),
    ("wallet_garbage", None, "unreadable"),
]


def run(vision: Callable[[str], dict] | None = None):
    exp = {"amount": 450000.0, "currency": "UZS", "counterpart": "Uzum Marketplace", "accept_max": True}
    rows = []
    for name, obs, want in FIXTURES:
        got = verdict(exp, obs)
        rows.append((name, got["verdict"], want, got["reason"]))
        assert got["verdict"] == want, (name, got)
    return rows


if __name__ == "__main__":
    for name, got, want, why in run():
        print(f"  {name:22s} {got:10s} (expect {want:10s}) — {why}")
    print("verify self-test OK — 5/5 fixtures, only 'confirmed' may close a case")
