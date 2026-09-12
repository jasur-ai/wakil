"""wakil learning loop — typed preferences with provenance (ai1, D2 "beat 6").

The pitch line is "wakil remembers how you like to be represented". Mechanically that
means: a 👎 + a short tag after a case becomes ONE typed pref row (`prefs` table,
`hands/schema.sql`), carrying `provenance` = which case taught it. The next mandate card
is pre-filled from prefs — but only for fields the user has NOT set, and every pref
stays individually deletable in the Mini App (product rule 5: visible + WIPE-able).

Kept pure (dicts in / dicts out) so it can be unit-tested without sqlite and wired by
P3 to `db.get_prefs / upsert_pref / delete_pref`.

Run: python learn.py   → self-test
"""
from __future__ import annotations

from typing import Any, Callable, Optional

# what we are allowed to remember, and how to coerce/validate it
PREF_SCHEMA: dict[str, tuple[str, Callable[[Any], Any], str]] = {
    "max_wait_hours":   ("number", lambda v: float(v), "how long you let wakil push before asking you"),
    "min_value_policy": ("text",   str, "e.g. 'never accept below floor without me'"),
    "allow_state_threat": ("bool", lambda v: str(v).lower() in ("1", "true", "yes", "ha"), "pre-authorize naming the agency/1159"),
    "tone":             ("text",   str, "polite-persistent | formal | brief"),
    "preferred_outcome": ("text",  str, "full_refund | exchange | warranty_repair ..."),
    "counterpart_channel": ("text", str, "support handle we already know works"),
}
MAX_PREFS = 40          # a delegate with 400 remembered opinions is a liability


class PrefError(ValueError):
    pass


def coerce(key: str, value: Any):
    if key not in PREF_SCHEMA:
        raise PrefError(f"unknown pref key '{key}' — memory is typed on purpose (R03 spirit)")
    return PREF_SCHEMA[key][1](value)


def record(prefs: list[dict], key: str, value: Any, provenance: str) -> list[dict]:
    """Upsert, newest-wins, keeps the list bounded. Provenance is mandatory."""
    if not provenance:
        raise PrefError("every pref must say which case taught it (provenance)")
    v = coerce(key, value)
    out = [p for p in prefs if p.get("key") != key]
    out.append({"key": key, "value": v, "provenance": provenance})
    return out[-MAX_PREFS:]


def feedback(rating: int, tag: str, case_ref: str) -> list[tuple[str, Any, str]]:
    """👎 + a tag from the Mini App → concrete pref mutations (never silent rewrites)."""
    t = (tag or "").lower()
    out: list[tuple[str, Any, str]] = []
    prov = f"from {case_ref}"
    if "erta" in t or "too late" in t or "kech" in t:
        out.append(("max_wait_hours", 72.0, prov))
    if "tez" in t or "fast" in t or "joy" in t:
        out.append(("max_wait_hours", 24.0, prov))
    if "qo'pol" in t or "rude" in t or "aggress" in t:
        out.append(("tone", "formal", prov))
    if "qisqa" in t or "long" in t or "uzun" in t:
        out.append(("tone", "brief", prov))
    if "davlat" in t or "agency" in t or "1159" in t:
        out.append(("allow_state_threat", True, prov))
    if "aloqa" in t or "channel" in t:
        out.append(("preferred_outcome", "full_refund", prov))
    if rating >= 0 and not out:
        out.append(("min_value_policy", "floor is the floor", prov))
    return out


def prefill(mandate: dict, prefs: list[dict]) -> tuple[dict, list[str]]:
    """Apply remembered prefs to a NEW mandate. Only fills what is empty/absent.
    Returns (mandate, applied[]) so the UI can badge each pre-filled field."""
    m = {k: (dict(v) if isinstance(v, dict) else list(v) if isinstance(v, list) else v)
         for k, v in mandate.items()}
    m.setdefault("bounds", {})
    applied: list[str] = []
    seeds: list[dict] = []
    by_key = {p["key"]: p for p in prefs if p.get("key") in PREF_SCHEMA}

    def apply(path: str, val: Any, prov: str):
        if path.startswith("bounds."):
            field = path.split(".", 1)[1]
            cur = m["bounds"].get(field)
            empty = cur in (None, "", [], 0, {}) or (field == "min_value" and not cur)
            if empty:
                m["bounds"][field] = val
        else:
            if not m.get(path):
                m[path] = val
        applied.append(path)
        seeds.append({"key": path, "value": val, "provenance": prov})

    if "max_wait_hours" in by_key:
        p = by_key["max_wait_hours"]
        cur = m["bounds"].get("max_wait_hours")
        if not cur:
            apply("bounds.max_wait_hours", p["value"], p["provenance"])
    if "allow_state_threat" in by_key:
        p = by_key["allow_state_threat"]
        if "allow_state_threat" not in m["bounds"]:
            apply("bounds.allow_state_threat", p["value"], p["provenance"])
    if "tone" in by_key and not m.get("strategy"):
        p = by_key["tone"]
        apply("strategy", f"{p['value']} (eslangan uslub)", p["provenance"])
    if "preferred_outcome" in by_key:
        p = by_key["preferred_outcome"]
        if not m["bounds"].get("acceptable_outcomes"):
            apply("bounds.acceptable_outcomes", [p["value"]], p["provenance"])
    if "counterpart_channel" in by_key:
        p = by_key["counterpart_channel"]
        if not m.get("counterpart", {}).get("channel"):
            m.setdefault("counterpart", {})["channel"] = p["value"]
            applied.append("counterpart.channel")
            seeds.append({"key": "counterpart.channel", "value": p["value"], "provenance": p["provenance"]})
    if seeds:
        m["learned_seeds"] = m.get("learned_seeds", []) + seeds
    return m, applied


if __name__ == "__main__":
    prefs: list[dict] = []
    for k, v, prov in feedback(-1, "erta topshirdi, keyinroq qo'rqitdi", "M-0007"):
        prefs = record(prefs, k, v, prov)
    print("prefs:", prefs)
    assert any(p["key"] == "max_wait_hours" and p["value"] == 72.0 for p in prefs)
    card = {"case_ref": "M-0008", "objective": "xato yetkazib berilgan telefon",
            "counterpart": {"name": "Uzum Marketplace"}, "bounds": {"min_value": 450000,
            "acceptable_outcomes": ["full_refund"], "non_negotiables": []}, "evidence": [],
            "strategy": "", }
    m2, applied = prefill(card, prefs)
    print("applied:", applied, "→ wait", m2["bounds"]["max_wait_hours"], "h")
    assert m2["bounds"]["max_wait_hours"] == 72.0
    assert m2["learned_seeds"][0]["provenance"] == "from M-0007"
    assert m2["bounds"]["min_value"] == 450000, "a pref must never overwrite a stated floor"
    try:
        record(prefs, "bank_card", "4000 0000 0000 0000", "from M-0007")
        raise AssertionError("typed prefs must reject unknown keys")
    except PrefError:
        pass
    print("learn self-test OK")
