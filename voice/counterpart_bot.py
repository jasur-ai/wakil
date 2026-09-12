"""Simulated @UzumSupport — the counterparty for rehearsals (owner: lead/voice).

Runs on the counterparty phone. Branches (start: /case M-0001 <branch>):
  instant → T1 receipt → T2 approved 450 000 (happy close)
  deny    → T1 receipt → T2 policy denial + UNDER-MIN offer 300 000 → (agent pushes) T3 grant: 450 000 approved
  grant   → like deny, but T3 always approves at the agent's floor
  refuse  → T1 receipt → T2 denial → T3 hard refusal (for the dossier/state-ladder beat)

Demo label rule (D0-10): the booth screen marks it as SIMULATED.

Run: BOT_TOKEN=xxx python counterpart_bot.py
"""
from __future__ import annotations

import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

STATE: dict[int, dict] = {}

T1 = "Assalomu alaykum! Buyurtma UZ-778-112 bo'yicha murojaatingizni oldik. Tekshirib beramiz."
T2_DENY = ("Afsuski, tovar qaytarilgan holatda qabul qilinmaydi (qoida 7.2). "
           "Sizga 300 000 so'm qisman qaytarish taklif qilamiz.")
T3_GRANT = ("Menejer bilan bog'landik. Arizangiz asosli deb tanoldik — "
            "450 000 so'm to'liq qaytarish tasdiqlandi. 3 ish kuni ichida kartaingizga tushadi.")
T3_REFUSE = ("Qaror o'zgartirilmaydi: 300 000 so'mdan boshqa variant yo'q. "
             "Murojaatingiz yopildi deb hisoblanadi.")
T2_INSTANT = "Murojaatingiz asosli. 450 000 so'm to'liq qaytarish tasdiqlandi. 3 ish kuni ichida kartaingizga tushadi."


async def start(m: Message):
    parts = (m.text or "").split()
    ref = parts[1] if len(parts) > 1 else "M-0001"
    branch = parts[2] if len(parts) > 2 else "deny"
    STATE[m.chat.id] = {"ref": ref, "branch": branch, "stage": 0}
    await m.answer(T1)


async def next_turn(m: Message):
    s = STATE.get(m.chat.id)
    if not s or s["stage"] == 2:
        return
    s["stage"] += 1
    b = s["branch"]
    if b == "instant":
        await m.answer(T2_INSTANT)
        return
    if s["stage"] == 1:
        await m.answer(T2_DENY)
        return
    # stage 2 (agent pushed back)
    await m.answer(T3_GRANT if b in ("deny", "grant") else T3_REFUSE)


async def main():
    token = os.environ["BOT_TOKEN"]
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.message.register(start, F.text.startswith("/case"))
    dp.message.register(next_turn)
    me = await bot.get_me()
    print(f"counterparty bot ready as @{me.username} — send: /case M-0001 deny")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
