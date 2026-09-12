# DECISIONS (frozen contracts — changes require a lead entry in chat.md)

- **D0-1 · Branding / spelling.** Repo, docs, code comments, UI, commits, branch names: **`wakil`** everywhere — never `vakil`.
- **D0-2 · Repo visibility.** `jasur-ai/wakil` is **public** (owner decision 2026-09-12).
- **D0-3 · Shared artifacts are canonical.** `contracts/00` (mandate), `01` (hands API), `02` (case bus), `03` (mini app REST). Nobody edits these except via a logged decision.
- **D0-4 · Tech.** brain: Python (guard/corpus stdlib-only; LLM injected, vendor-agnostic). hands: Python — Telethon + aiogram + FastAPI + SQLite (local). face: **single HTML file, no build step**, vanilla JS. voice: aiogram.
- **D0-5 · Secrets.** Env vars only. `.env*`, `*.session`, `sessions/`, `*.db`, `outputs/` gitignored. Session files chmod 600. Token lives outside the repo (`~/.wakil_token` → `$GITHUB_TOKEN`).
- **D0-6 · Branching.** `ai1/<slug>` · `ai2/<slug>` · `ai3/<slug>` · `lead/<slug>`. Commit prefix = tag (`ai1:`, `ai2:`, `ai3:`, `lead:`). PR into `main`; lead merges. Merge at 12:00 / 18:00 or on green gate.
- **D0-7 · Scope.** Freeze D2 12:00 (no new features). Code freeze D3 18:00. Demo-critical = the 6 beats in `voice/runbook.md`.
- **D0-8 · Button spike.** `resendBotCallbackQuery` from a user session — **ai3, hard deadline D1 10:30**, result in `spike/resend_callback.md`. If fail → fallback = user taps final confirm (or text command), decided at the 10:30 check-in, never on demo day.
- **D0-9 · UI polling.** Mini App polls `GET /case/{id}/events?since=` every 2s (SSE later if stable). Polling is the design, not a fallback.
- **D0-10 · Demo honesty.** The simulated `@UzumSupport` is labeled as simulated on the booth screen. Real-bot flows (Uzum/Beeline/Ucell/agency) are shown from documented menu walks + the live probe of `@consumergovuz_bot`.
- **D0-11 · ONE repo rule (2026-09-12).** The ONLY project repository is **`jasur-ai/wakil`** (public). The earlier duplicates — `VAKIL` (uppercase) and `wakil-everywhere` — were consolidated here and **deleted**. **Nobody creates new repos; nobody pushes anywhere but `jasur-ai/wakil`.**
- **D0-12 · Official codebase (2026-09-12).** Owner decision: the official hackathon codebase is **Python — `jasur-ai/wakil`** (this repo). A separate parallel **TypeScript** implementation exists at **`hackathon-ml/vakil`** (a different org account; owner confirmed it is theirs). It is **NOT** the official repo and **no work happens there**. It is bloated to ~18MB (committed `node_modules`). Pending owner action: delete it, or provide an admin token to clean it (that org blocks fine-grained tokens with lifetime >366 days). Until then it is left untouched.
