"""Search over the user's channels (Contract 01: search_global / iter_new).

Telethon class names to verify in the D1 spike:
  telethon.tl.functions.messages.SearchGlobalRequest / SearchRequest
Fallback if either is unavailable: iterate the scoped dialogs + local regex
over `iter_new` results (document the choice in spike/resend_callback.md).
"""
from __future__ import annotations

from datetime import datetime, timedelta


def jump_url(dialog: str, msg_id: int | None) -> str:
    if not dialog:
        return ""
    if msg_id:
        return f"https://t.me/{dialog}/{msg_id}"
    return f"https://t.me/{dialog}"


async def search_global(client, q: str, since_days: int = 30, limit: int = 20):
    """Global search across the user's Telegram."""
    from telethon.tl.functions.messages import SearchGlobalRequest
    res = await client(SearchGlobalRequest(q, limit=limit))
    cutoff = datetime.utcnow() - timedelta(days=since_days)
    out = []
    for m in res.messages:
        try:
            if m.date and m.date < cutoff:
                continue
        except Exception:
            pass
        out.append({"text": (m.text or m.message or "")[:400],
                    "dialog": getattr(m, "peer_id", None),
                    "ts": m.date.isoformat() if m.date else None,
                    "url": jump_url(str(getattr(m, "peer_id", "")), m.id)})
    return rank_by_recency(out)


async def search_scoped(client, dialog: str, q: str, limit: int = 30):
    """Scoped search in dialogs the user picked (privacy default)."""
    from telethon.tl.functions.messages import SearchRequest
    res = await client(SearchRequest(q, peer=dialog, limit=limit))
    out = [{"text": (m.text or m.message or "")[:400], "dialog": dialog,
            "ts": m.date.isoformat() if m.date else None,
            "url": jump_url(dialog, m.id)} for m in res.messages]
    return rank_by_recency(out)


def rank_by_recency(hits: list[dict]) -> list[dict]:
    return sorted(hits, key=lambda h: h.get("ts") or "", reverse=True)


# -- demo mode (no live session at the booth yet) ------------------------------
_DEMO = [
    {"item": "iPhone 15 128GB", "source": "@telefon_uz", "price": "6 999 000", "url": "https://t.me/telefon_uz"},
    {"item": "iPhone 15 128GB", "source": "@olarmarket", "price": "6 850 000", "url": "https://t.me/olarmarket"},
    {"item": "iPhone 15 256GB", "source": "@olarmarket", "price": "7 900 000", "url": "https://t.me/olarmarket"},
]


def demo_search(k: str) -> dict:
    hits = [dict(h) for h in _DEMO if (not k or k.lower() in h["item"].lower())]
    return {"results": hits,
            "price_table": [{"item": h["item"], "source": h["source"], "price": h["price"], "url": h["url"]}
                            for h in hits],
            "note": "demo fixtures — live search needs the user session (Contract 01)"}
