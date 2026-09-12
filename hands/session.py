"""wakil session layer — the user's own Telegram account, 2FA enforced.

Flow (onboarding, mini app steps 3–5):
  1. login(phone) → interactive phone code
  2. two-step check (GetPasswordRequest)
     - 2FA OFF  → wizard FORCES it on (wakil refuses to run without it)
     - 2FA ON   → continue
  3. session file chmod 600, path recorded in users table (never in git)

Gray-zone honesty (docs/v1 §3): user's own account, user-initiated,
rate-limited (flood.py), only dialogs the user explicitly scoped.
"""
from __future__ import annotations

import os

from telethon import TelegramClient
from telethon.tl.functions.account import GetPasswordRequest

SESSION_DIR = os.environ.get("WAKIL_SESSIONS", os.path.join(os.path.dirname(__file__), "sessions"))


class TwoFaNotSetError(RuntimeError):
    """Safety stop: wakil never runs without two-step verification."""


class SessionManager:
    def __init__(self, api_id: int, api_hash: str, session_dir: str = SESSION_DIR):
        self.api_id = int(api_id)
        self.api_hash = api_hash
        self.session_dir = session_dir
        os.makedirs(self.session_dir, exist_ok=True)

    def _session_path(self, phone: str) -> str:
        safe = "".join(c for c in phone if c.isalnum())
        return os.path.join(self.session_dir, f"wakil-{safe}")

    def client(self, phone: str) -> TelegramClient:
        return TelegramClient(self._session_path(phone), self.api_id, self.api_hash)

    async def login(self, phone: str, input_fn=input, print_fn=print) -> str:
        """Interactive login. Returns the secured session file path."""
        client = self.client(phone)
        await client.start(
            phone=phone,
            code=lambda: input_fn("Telefon kodi: "),
            password=lambda: input_fn("2FA parol (agar bor bo'lsa): "),
        )
        await self.enforce_2fa(client, input_fn=input_fn, print_fn=print_fn)
        path = self._session_path(phone) + ".session"
        self.secure_session_file(path)
        await client.disconnect()
        return path

    async def enforce_2fa(self, client: TelegramClient, input_fn=input, print_fn=print) -> None:
        """Force two-step verification on. wakil's first security promise."""
        info = await client(GetPasswordRequest())
        if not info.has_password:
            print_fn("2FA o'chiq emas. wakil 2FAsiz ishlay olmaydi — endi yoqamiz.")
            new_password = input_fn("Yangi 2FA parol: ")
            if len(new_password) < 8:
                raise TwoFaNotSetError("2FA parol juda qisqa (>=8 belgi)")
            await client.edit_2fa(new_password)  # Telethon shortcut for UpdatePasswordSettings
            check = await client(GetPasswordRequest())
            if not check.has_password:
                raise TwoFaNotSetError("2FA qo'yilmadi — xavfsizlik qoidasi bo'yicha to'xtatildi")
            print_fn("2FA yoqildi va tasdiqlandi. Davom etamiz.")

    def secure_session_file(self, path: str) -> None:
        if os.path.exists(path):
            os.chmod(path, 0o600)
