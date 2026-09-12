"""wakil voice → mandate slots (ai1, D1 gate item 3).

Pipeline: voice note (uz) → ASR transcript → slot JSON → mandate card prefill.

ASR is INJECTED (`asr: Callable[[path], str]`) exactly like the LLM — the booth runs
`faster-whisper` locally (D0-5: nothing leaves the device), tests inject a fake.
This module owns the part that is actually ours: turning a messy Uzbek/Russian
transcript into a schema-valid `contracts/00` mandate, and reporting what is still
missing so the Mini App asks for it instead of guessing.

Why deterministic parsing and not an LLM here: the floor number is a legal bound.
If we let the model round "to'rt yuz ellik ming" we lose the case. Numbers, order
refs and consent are parsed by rules; the LLM only ever polishes prose.

Run: python slots.py   → fixture self-test
"""
from __future__ import annotations

import re
from typing import Callable, Optional

UNITS = {"bir": 1, "ikki": 2, "uch": 3, "to'rt": 4, "dort": 4, "besh": 5, "olti": 6,
         "yetti": 7, "sakkiz": 8, "to'qqiz": 9, "toqiz": 9,
         "o'n": 10, "on": 10, "o'n bir": 11, "o'n ikki": 12, "o'n uch": 13, "o'n to'rt": 14,
         "o'n besh": 15, "o'n olti": 16, "o'n yetti": 17, "o'n sakkiz": 18, "o'n to'qqiz": 19,
         "yigirma": 20, "yigirmа": 20, "o'ttiz": 30, "ottiz": 30, "qirq": 40, "ellik": 50,
         "oltmish": 60, "yettmish": 70, "sakson": 80, "to'qson": 90, "toqson": 90}
SCALE = {"yuz": 100, "ming": 1_000, "million": 1_000_000, "mln": 1_000_000,
         "milliard": 1_000_000_000, "mlrd": 1_000_000_000, "mld": 1_000_000_000}

OUTCOME_WORDS = [
    (("to'liq qaytar", "pulni qaytar", "полный возврат", "qaytarib ber", "вернуть", "возврат"), "full_refund"),
    (("qisman", "yarmi", "частичн"), "partial_refund"),
    (("almashtir", "boshqasiga"), "exchange"),
    (("ta'mir", "qayta tikla", "гаранти"), "warranty_repair"),
    (("chegirma", "skidk"), "discount"),
    (("o'rniga qo'y", "yangisiga"), "replacement"),
]
DENY_CONSENT = ("faqat suhbat", "hech qayerga shikoyat", "ne podavat", "sud emas",
                "qilmang", "qilish shart emas", "kerak emas", "hojati yo'q",
                "не буду", "не надо", "не стоит")

COUNTERPARTS = {
    "uzum": ("Uzum Marketplace", "@Uzum_Support_Bot"),
    "beeline": ("Beeline Uzbekistan", "@Beeline_UZbot"),
    "ucell": ("Ucell", "@UcellInformation"),
    "artel": ("Artel", "@artel_uzbot"),
    "click": ("Click", "@click_support"),
    "payme": ("Payme", "@payme_support"),
}


def parse_uz_number(text: str) -> Optional[float]:
    """Digits, '450k', '450 000', and Uzbek words ('to'rt yuz ellik ming')."""
    return _num(_normize(text))


def _normize(text: str) -> str:
    return (text or "").lower().replace("\u2018", "'").replace("\u2019", "'").strip()


def _num(t: str) -> Optional[float]:
    m = re.search(r"(\d[\d\s._]*(?:[.,]\d+)?)\s*(kuber|k|mln|million|mlrd|milliard)?", t)
    if m and re.search(r"\d", m.group(1)):
        digits = re.sub(r"[^\d]", "", m.group(1))
        val = float(m.group(1).replace(" ", "").replace("_", "").replace(",", "."))
        mult = {"k": 1e3, "kuber": 1e3, "mln": 1e6, "million": 1e6,
                "mlrd": 1e9, "milliard": 1e9}.get((m.group(2) or "").lower(), 1)
        # '450 000 so'm' — a bare 6+ digit figure is already the full amount
        if mult == 1 and len(digits) >= 4:
            val = float(digits)
        return val * mult
    total, cur = 0.0, 0.0
    for tok in re.findall(r"[a-z'ʻ]+", t):
        if tok in UNITS:
            cur += UNITS[tok]
        elif tok in SCALE:
            if SCALE[tok] == 100:
                cur = (cur or 1) * 100
            else:
                total += (cur or 1) * SCALE[tok]
                cur = 0.0
    total += cur
    return total or None


CUR_RE = r"so'?m[a-zа-яё]*|UZS|сўм[a-zа-яё]*|сум[a-zа-яё]*|sum[a-z]*"


def extract_amount_near_currency(text: str) -> Optional[float]:
    """Numbers are only money when they sit *immediately* before the currency word.
    Parsing the whole sentence is how "450 ming so'm ... ikki kun" becomes 450002 and
    how an order ref ("UZ-778-112") becomes the floor. A wrong floor is a wrong legal
    bound, so the window is anchored at the currency token and reads backwards.
    """
    t = _normize(text)
    best = None
    for m in re.finditer(CUR_RE, t, re.IGNORECASE):
        window = t[max(0, m.start() - 48):m.start()].strip().rstrip("-–—,;:")
        val = _amount_at_end(window)
        if val is not None and (best is None or val > best):
            best = val
    return best


def _amount_at_end(window: str) -> Optional[float]:
    """'... 450 000 ' → 450000 ; '... to'rt yuz ellik ming ' → 450000 ; 'UZ-778-112. ' → None
    (digits not adjacent to the currency, or cut by a sentence end, are not money)."""
    if not window or window.endswith((".", "!", "?")):
        return None
    # the number may not swallow a sentence end: "UZ-778-112. 450 000 so'm" must read 450000,
    # not 112450000 — so only spaces (thousands) and a tight decimal are allowed here.
    m = re.search(r"(\d[\d ]*(?:[.,]\d{1,3})?)\s*(kuber|k|mln|million|mlrd|milliard)?\s*$", window)
    if m:
        digits = re.sub(r"[^\d]", "", m.group(1))
        if not digits:
            return None
        # a hyphen/slash-joined ref (UZ-778-112) or a date is not an amount
        pre = window[:m.start(1)]
        if re.search(r"[-/]\s*$", pre) and len(digits) < 6 and not m.group(2):
            return None
        if len(digits) <= 3 and not m.group(2):
            return None                      # bare "450" with no scale word is not a floor
        val = float(digits)
        mult = {"k": 1e3, "kuber": 1e3, "mln": 1e6, "million": 1e6,
                "mlrd": 1e9, "milliard": 1e9}.get((m.group(2) or "").lower(), 1)
        return val * mult
    toks = re.findall(r"[a-z'ʻ]+", window)[-6:]
    numtoks: list[str] = []
    for tok in reversed(toks):
        if tok in UNITS or tok in SCALE:
            numtoks.insert(0, tok)
        elif numtoks:
            break
    return _num(" ".join(numtoks)) if numtoks else None


def extract(transcript: str, *, asr: Optional[Callable[[str], str]] = None,
            audio_path: str | None = None) -> dict:
    """Voice path (audio_path + asr) OR text path (transcript). Returns a prefill dict
    plus `missing` — never a half-invented mandate."""
    text = asr(audio_path) if (asr and audio_path) else transcript
    t = (text or "").strip()
    low = t.lower()
    out: dict = {"objective": None, "counterpart": {}, "bounds": {}, "evidence": [],
                 "strategy": "meherban doimiylik, faktlar, 2 rad etishda eskalyatsiya",
                 "transcript": t, "missing": [], "notes": []}

    name = next((k for k in COUNTERPARTS if k in low), None)
    if name:
        out["counterpart"] = {"name": COUNTERPARTS[name][0], "channel": COUNTERPARTS[name][1]}
        out["notes"].append(f"counterpart matched from transcript: {name}")

    order = re.search(r"\b([A-Z]{2,3}-\d{3}-\d{3,6}|\d{8,12})\b", t)
    if order:
        out["evidence"].append({"kind": "order_ref", "ref": "order", "data": {"order": order.group(1)}})

    money = extract_amount_near_currency(t)
    if money:
        out["bounds"]["min_value"] = money
        out["bounds"]["max_value"] = money
    else:
        out["missing"].append("bounds.min_value")

    hours = None
    if re.search(r"сутк|sutk", low):
        hours = 24.0
    m = re.search(r"(\d+|o'n|ikki|uch|to'rt|besh|bir)\s*(soat|соат|hour|chas|ч[ао]с)", low)
    if m:
        v = parse_uz_number(m.group(1))
        hours = v
    else:
        m = re.search(r"(\d+|o'n|ikki|uch|to'rt|besh|bir)\s*(kun|кун|day|kunlik)", low)
        if m:
            hours = (parse_uz_number(m.group(1)) or 1) * 24
    if hours:
        out["bounds"]["max_wait_hours"] = hours
    else:
        out["missing"].append("bounds.max_wait_hours")

    if any(w in low for w in ("qisman", "yarmi", "частичн")):
        outcomes = ["partial_refund"]
    else:
        outcomes = [o for words, o in OUTCOME_WORDS if any(w in low for w in words)]
        if not outcomes and re.search(r"qaytar|возврат|вернут", low):
            outcomes = ["full_refund"]          # "450 ming so'm qaytarilsa bo'ldi" = refund
    if outcomes:
        out["bounds"]["acceptable_outcomes"] = sorted(set(outcomes))
    else:
        out["missing"].append("bounds.acceptable_outcomes")

    out["bounds"]["non_negotiables"] = []
    if re.search(r"past\s*(bo'?lmasin|kirmasin)", low):
        out["bounds"]["non_negotiables"].append(f"{money:.0f} dan past taklif qabul qilinmasin"
                                                if money else "past taklif qabul qilinmasin")
    out["bounds"]["allow_state_threat"] = not any(d in low for d in DENY_CONSENT) and bool(
        re.search(r"(davlat|qo'mita|1159|agentlik|shikoyat|суд)", low))

    obj = re.split(r"[.!?]", t)[0].strip()
    out["objective"] = obj[:400] if obj else None
    if not out["objective"]:
        out["missing"].append("objective")
    if audio_path:
        out["evidence"].append({"kind": "voice_note", "ref": "voice1", "data": {}})
    return out


def merge_into_mandate(prefill: dict, case_ref: str, created_at_ts: float) -> dict:
    """Build a draft mandate the UI can show; guard validation decides if it is submittable."""
    b = prefill.get("bounds") or {}
    m = {
        "case_ref": case_ref,
        "objective": prefill.get("objective") or "",
        "counterpart": prefill.get("counterpart") or {},
        "bounds": {
            "min_value": b.get("min_value", 0),
            "max_value": b.get("max_value", b.get("min_value", 0)),
            "acceptable_outcomes": b.get("acceptable_outcomes", []),
            "max_wait_hours": b.get("max_wait_hours", 48),
            "non_negotiables": b.get("non_negotiables", []),
            "allow_state_threat": b.get("allow_state_threat", False),
        },
        "evidence": prefill.get("evidence") or [],
        "strategy": prefill.get("strategy", "meherban doimiylik"),
        "created_at_ts": created_at_ts,
    }
    if prefill.get("learned_seeds"):
        m["learned_seeds"] = prefill["learned_seeds"]
    return m


FIXTURES = {
    # Whisper output as digits (the common case)
    "f1": ("Assalomu alaykum. Uzumdan olgan iPhone 15 ekranida nuqson chiqdi. "
           "Buyurtma UZ-778-112. 450 000 so'mni to'liq qaytarishni so'rayman, 48 soat vaqt bering. "
           "Hal bo'lmasa davlat qo'mitasiga shikoyat qilamiz. 450 mingdan past bo'lmasin."),
    # Whisper output as words (uz speech often comes back spelled out)
    "f2": ("Uzum bozoridan telefon oldim, ishlamayapti, to'rt yuz ellik ming so'm qaytarilsa "
           "bo'ldi, ikki kun kutaman, boshqa yurga shikoyat qilmang."),
    # Russian speaker (common in Tashkent) — no state consent, no order ref
    "f3": ("Товар бракованный, прошу вернуть 450 000 сумов, ждать буду сутки, никуда жаловаться не буду."),
}

if __name__ == "__main__":
    import json
    for k, txt in FIXTURES.items():
        r = extract(txt)
        print(f"--- {k}: floor={r['bounds'].get('min_value')} wait={r['bounds'].get('max_wait_hours')}h "
              f"outcomes={r['bounds'].get('acceptable_outcomes')} state={r['bounds'].get('allow_state_threat')} "
              f"missing={r['missing']}")
        assert r["bounds"]["min_value"] == 450000, (k, r["bounds"])
        assert r["bounds"]["max_wait_hours"] in (48, 24)
    assert parse_uz_number("to'rt yuz ellik ming") == 450000
    assert parse_uz_number("o'n uch ming") == 13000
    assert parse_uz_number("1,6 mlrd") == 1_600_000_000
    print("slots self-test OK  (ASR itself is not exercised here — see legal_findings.md §ASR)")
    print(json.dumps(extract(FIXTURES["f1"])["counterpart"], ensure_ascii=False))
