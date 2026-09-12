"""Flood-aware per-chat sender (user session side).

Rules (gray-zone hygiene, docs/v1 §3):
- 1 message / second / chat minimum gap
- serial per chat (asyncio.Lock)
- FloodWaitError → sleep e.seconds (+1) and retry; visible "waiting Xs" state
  is BY DESIGN — the mini app shows it; it reads as engineering, not luck.
"""
from __future__ import annotations

import asyncio
import time

from telethon.errors import FloodWaitError

MIN_GAP_S = 1.05
MAX_RETRIES = 6


class FloodQueue:
    def __init__(self):
        self._locks: dict[str, asyncio.Lock] = {}
        self._last: dict[str, float] = {}
        self.wait_notice = ""  # last wait message, surfaced to the UI

    def _key(self, entity) -> str:
        return str(getattr(entity, "id", entity))

    async def send(self, client, entity, text: str, media=None):
        key = self._key(entity)
        lock = self._locks.setdefault(key, asyncio.Lock())
        async with lock:
            last = self._last.get(key)
            if last is not None:
                gap = MIN_GAP_S - (time.monotonic() - last)
                if gap > 0:
                    self.wait_notice = f"rate limit: {gap:.0f}s kutmoqda"
                    await asyncio.sleep(gap)
            for _ in range(MAX_RETRIES):
                try:
                    msg = await client.send_message(entity, text, file=media)
                    self._last[key] = time.monotonic()
                    self.wait_notice = ""
                    return msg
                except FloodWaitError as e:
                    self.wait_notice = f"rate limit: {e.seconds + 1}s kutmoqda"
                    await asyncio.sleep(e.seconds + 1)
            raise RuntimeError("flood-wait loop exceeded — back off and ask the user")
