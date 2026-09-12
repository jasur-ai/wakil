# P3 — HANDS (owner: ai3)

**Mission.** Own everything that touches **real Telegram**: user session with 2FA enforcement, flood queue, bot face, local data, search/watchers, dossier export. You make the **security story flawless** — it is the trust foundation.

## ⚠ FIRST TASK — deadline **D1 10:30** (D0-8)
**`spike/resend_callback.md`**: can a user (MTProto) session press a bot's inline button? Test `ResendBotCallbackQuery`/`SendBotCallbackQuery` from Telethon against any bot with inline buttons (e.g. `@UzumSupport`). Document: works → `press_button()` real; fails → fallback (user taps final confirm OR text command). **Never discover this on demo day.**

## Already built by lead (extend, don't rewrite)
- `session.py` — login + **forced 2FA** (`edit_2fa`), session chmod 600
- `flood.py` — per-chat flood queue, visible "waiting Xs" (by design)
- `app.py` — FastAPI, **all 7 endpoints** + events + wipe + serves the mini app at `/`
- `db.py` + `schema.sql` — 9 tables · `dossier.py` — 8-section .docx, R10-gated · `search.py` (+demo fixtures)

## Your tasks (docs/team-battle-plan.md §P3)
- **D1 EOD** — stranger login E2E on a real test account (phone → code → 2FA forced → session file secured) at a **public tunnel URL**; WIPE verified; `make demo` cold start OK.
- **D2 EOD** — aiogram bot face (DM intake: text + voice passthrough to P1; escalation buttons → `POST /decision`; guardian tokens); live search vs 4 seeded channels + watcher (2-min) → bot-DM ping; **dossier E2E** (one tap → real .docx); Case Bus integration (events render in the live timeline).
- **D3** — `@consumergovuz_bot` read-only probe → `spike/` notes; `make demo` **6/6** cold starts; record the full-system backup run; freeze 14:00; on-call for rehearsals.

## Non-negotiables
- Secrets: env only (`API_ID`, `API_HASH`, `BOT_TOKEN`). `sessions/` + `*.session` never committed (gitignored — keep it that way), chmod 600.
- Every outbound goes through P1's guard — hands never sends raw LLM text.
- `resendBotCallbackQuery` result is a DECISIONS.md entry, written by 10:30.

## Env (local, from organizer)
`API_ID`, `API_HASH` (my.telegram.org) · `BOT_TOKEN` (aiogram face) · `WAKIL_DB` (default: hands/wakil.db) · `WAKIL_SESSIONS` (default: hands/sessions/)
