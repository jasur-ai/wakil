"""Telegram gateway — the agent's 'hands' to the counterparty.

Two implementations behind one protocol:
- MockUzumGateway: deterministic scripted @UzumSupport (demo/deploy, no credentials).
- RealTelegramGateway: Telethon-based user session (production, needs credentials).

The agent only depends on the Gateway protocol, so demo <-> live is a config swap.
"""
from __future__ import annotations
import asyncio
from typing import Optional, Protocol


class Gateway(Protocol):
    dialog: str
    async def send(self, text: str, media: Optional[str] = None) -> int: ...
    async def next_inbound(self, timeout: float = 60.0) -> Optional[str]: ...
    async def close(self) -> None: ...


class MockUzumGateway:
    """Deterministic scripted counterparty simulating @UzumSupport (deny -> grant).

    Beat 1 reply: policy denial + BELOW-FLOOR offer (300 000) -> forces the guard.
    Beat 2 reply (after the agent holds the floor / cites law): full grant (450 000).
    """
    dialog = "@UzumSupport"

    def __init__(self, branch: str = "deny", think_s: float = 1.6):
        self.branch = branch
        self.think_s = think_s
        self._q: asyncio.Queue = asyncio.Queue()
        self._sent = 0
        self._closed = False

    async def send(self, text: str, media: Optional[str] = None) -> int:
        self._sent += 1
        asyncio.create_task(self._reply(text, self._sent))
        return self._sent

    async def _reply(self, agent_text: str, n: int):
        await asyncio.sleep(self.think_s)
        if self._closed:
            return
        t = agent_text.lower()
        if n == 1:
            reply = ("Afsuski, tovar qaytarilgan holatda qabul qilinmaydi (qoida 7.2). "
                     "Sizga 300 000 so'm qisman qaytarish taklif qilamiz.")
        elif "modda" in t or "qonun" in t or "450" in t:
            reply = ("Menejer bilan bog'landik. Arizangiz asosli deb tanoldik — "
                     "450 000 so'm to'liq qaytarish tasdiqlandi. 3 ish kuni ichida kartangizga tushadi.")
        else:
            reply = "Tushundik, ko'rib chiqamiz. Biroz vaqt bering."
        await self._q.put(reply)

    async def next_inbound(self, timeout: float = 60.0) -> Optional[str]:
        try:
            return await asyncio.wait_for(self._q.get(), timeout)
        except asyncio.TimeoutError:
            return None

    async def close(self):
        self._closed = True


class RealTelegramGateway:
    """Live gateway via a Telethon user session (production). Needs API_ID/API_HASH + a logged-in session.

    Intentionally thin here; AI3 (P3) wires the full session + flood queue per hands/session.py + flood.py.
    """
    def __init__(self, dialog: str, client=None):
        if client is None:
            raise RuntimeError("RealTelegramGateway needs a logged-in Telethon client (credentials not configured in demo mode).")
        self.dialog = dialog
        self.client = client
        self._since: dict = {}

    async def send(self, text: str, media: Optional[str] = None) -> int:
        msg = await self.client.send_message(self.dialog, text, file=media)
        return getattr(msg, "id", 0)

    async def next_inbound(self, timeout: float = 60.0) -> Optional[str]:
        # TODO(P3): stream new messages for self.dialog since last id (iter_new), with jump links.
        return None

    async def close(self):
        try:
            await self.client.disconnect()
        except Exception:
            pass
