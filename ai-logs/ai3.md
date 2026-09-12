# AI3 — running notes (P3 HANDS)

Role: **bot backend / session**. Repo: **https://github.com/jasur-ai/wakil** · spelling **`wakil`** (never `vakil`).

Before starting: read `chat.md` §4 board → claim a row → branch `ai3/<slug>` → commit prefix `ai3:` → PR → append START + DONE to `chat.md` §5.

## My tasks (from board)
| Date | Task | Branch/PR | Status |
|------|------|-----------|--------|
| 2026-09-12 | **SPIKE FIRST — deadline D1 10:30**: `spike/resend_callback.md` (user session pressing a bot inline button) | `ai3/spike` | ⬜ |
| 2026-09-12 | Stranger login → code → **2FA enforced** → session secured → WIPE, E2E on a test account at a public URL | `ai3/login-e2e` | ⬜ |
| 2026-09-12 | Bot face (aiogram: DM intake, escalation buttons, guardian tokens) + live search vs 4 channels + watcher (2-min) + dossier E2E | `ai3/bot-face` | ⬜ |
| 2026-09-12 | D3: `@consumergovuz_bot` read-only probe; `make demo` 6/6 cold starts; record full-system backup | `ai3/probe` | ⬜ |

## Notes / context
- **Do not rebuild** — `session.py` (login + forced 2FA via `edit_2fa`), `flood.py`, `app.py` (FastAPI, 7 endpoints + wipe, serves mini app at `/`), `db.py`+`schema.sql`, `dossier.py`, `search.py` already exist. Extend them.
- **Spike deadline is hard (10:30).** Result → `spike/resend_callback.md` + a `DECISIONS.md` line. Never discover it on demo day.
- Secrets: env only (`API_ID`, `API_HASH`, `BOT_TOKEN`). `sessions/` + `*.session` never committed (gitignored), chmod 600.
- Every outbound goes through AI1's guard — hands never sends raw LLM text.
- Env names: `WAKIL_DB`, `WAKIL_SESSIONS`.
- Task sheet: `hands/README.md`.
