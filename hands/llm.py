"""LLM — the agent's 'voice'. Two implementations behind one protocol:
- ScriptedLLM: deterministic demo utterances (no API key needed, fully offline).
- RealLLM: OpenAI/Anthropic (production). The LLM only DRAFTS text; the
  BoundaryGuard (brain/guard.py) decides what may actually leave the device.
"""
from __future__ import annotations
from typing import Protocol


def _fmt(n) -> str:
    return f"{int(n):,}".replace(",", " ")


class LLM(Protocol):
    def opening(self, mandate: dict) -> str: ...
    def react_to_offer(self, mandate: dict, inbound: str) -> str: ...
    def hold_reply(self, mandate: dict) -> str: ...
    def close(self, mandate: dict) -> str: ...


class ScriptedLLM:
    """Offline, deterministic. Produces the exact demo beats; every line passes the guard."""

    def opening(self, m: dict) -> str:
        order = ((m.get("evidence") or [{}])[0].get("data") or {}).get("order", "—")
        return (f"Assalomu alaykum! Men foydalanuvchi tomonidan tayinlangan vakiliman (wakil). "
                f"Buyurtma {order} bo'yicha nosoz iPhone 15 uchun to'liq qaytarish so'rayman.")

    def react_to_offer(self, m: dict, inbound: str) -> str:
        return "Taklifingizni qabul qila olmayman — bu mijozim belgilagan minimal qiymatdan past."

    def hold_reply(self, m: dict) -> str:
        minv = _fmt(m["bounds"]["min_value"])
        return (f"Savolingizga rahmat. Mijozim vakolatnomasida minimal qiymatni {minv} so'm deb belgilagan. "
                f"18-moddaga ko'ra sifatli tovar 10 kun ichida qaytarilishi mumkin — shu asosda to'liq qaytarishni so'raymiz.")

    def close(self, m: dict) -> str:
        return "Rahmat, qaytarish tasdiqlandi (Tasdiqlandi). Ariza yopildi."


class RealLLM:
    """Production LLM. Vendor-agnostic; wire to OpenAI/Anthropic with an API key (env)."""
    def __init__(self, api_key: str = "", model: str = "", base_url: str = ""):
        if not api_key:
            raise RuntimeError("RealLLM needs an API key (set in env). Demo mode uses ScriptedLLM.")
        self.api_key, self.model, self.base_url = api_key, model, base_url

    # TODO(P1/AI1): implement with the chosen vendor; keep returning plain UZ text.
    def opening(self, m): raise NotImplementedError
    def react_to_offer(self, m, inbound): raise NotImplementedError
    def hold_reply(self, m): raise NotImplementedError
    def close(self, m): raise NotImplementedError
