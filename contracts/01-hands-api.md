# Contract 01 — Hands API (P3 implements · P1 consumes)

Python, async. **P1 never touches Telethon directly.** Every action on the user's real account goes through this API. Implemented in `hands/` (session.py, flood.py, search.py).

| Method | Signature | Notes |
|---|---|---|
| `send` | `async send(dialog: str, text: str, media: str \| None = None) -> int` | Flood-aware (flood.py: 1 msg/s per chat, auto-sleep on `FloodWaitError`, visible "waiting Xs" state). `dialog` = username \| chat_id. Returns tg msg_id. **Only guard-PASS text reaches here.** Logged to `message_log` with guard verdict. |
| `observe` | `async observe(dialog: str, limit: int = 10) -> list[dict]` | Last messages: `{id, from_id, text, ts}`. |
| `press_button` | `async press_button(dialog: str, button_ref: str) -> bool` | **Spike-dependent (D1 10:30).** If spike fails → P1 switches to text commands; P2 shows "tap to confirm" fallback (D0-8). |
| `search_global` | `async search_global(q: str, since_days: int = 30, dialogs: list[str] \| None = None) -> list[dict]` | `dialogs=None` → Telegram `searchGlobal`; else scoped `messages.search`. Returns `{text, dialog, ts, url}` (url = t.me jump link). |
| `iter_new` | `async iter_new(dialogs: list[str], since_id: int) -> list[dict]` | Watcher feed (2-min cadence), new messages with jump links. |

**Rules.**
- 1 msg/s per chat. Flood waits are **by design**: the Mini App shows the wait state (it reads as engineering, not luck).
- Rate limits: Telethon auto-sleep respected; no parallel sends to the same chat (per-chat lock in flood.py).
- Gray-zone honesty: the session is the user's own account, user-initiated, rate-limited, talking only to dialogs the user explicitly picked (scope step in onboarding). See docs/idea1-wakil-deep-dive.md §3.
