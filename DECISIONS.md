# DECISIONS (frozen contracts — changes require a lead entry in chat.md)

- **D0-1 · Branding.** Repo, docs, code comments, UI: **wakil** (capital) everywhere.
- **D0-2 · Repo visibility.** Private now (real session-flow code); flip to public before submission if the team agrees (lead decides, logged here).
- **D0-3 · Shared artifacts are canonical.** `contracts/00` (mandate), `01` (hands API), `02` (case bus), `03` (mini app REST). Nobody edits these except via a logged decision.
- **D0-4 · Tech.** brain: Python (guard/corpus stdlib-only; LLM injected, vendor-agnostic). hands: Python — Telethon + aiogram + FastAPI + SQLite (local). face: **single HTML file, no build step**, vanilla JS. voice: aiogram.
- **D0-5 · Secrets.** Env vars only. `.env`, `*.session`, `sessions/`, `*.db` gitignored. Session files chmod 600.
- **D0-6 · Branching.** `p1-brain` (ai1) · `p2-face` (ai2) · `p3-hands` (ai3) · lead on `main`. Merge at 12:00 / 18:00 or on green gate.
- **D0-7 · Scope.** Freeze D2 12:00 (no new features). Code freeze D3 18:00. Demo-critical = the 6 beats in `voice/runbook.md`.
- **D0-8 · Button spike.** `resendBotCallbackQuery` from a user session — **ai3, hard deadline D1 10:30**, result in `spike/resend_callback.md`. If fail → fallback = user taps final confirm (or text command), decided at the 10:30 check-in, never on demo day.
- **D0-9 · UI polling.** Mini App polls `GET /case/{id}/events?since=` every 2s (SSE later if stable). Polling is the design, not a fallback.
- **D0-10 · Demo honesty.** The simulated `@UzumSupport` is labeled as simulated on the booth screen. Real-bot flows (Uzum/Beeline/Ucell/agency) are shown from documented menu walks + the live probe of `@consumergovuz_bot`.
- **D0-11 · ONE repo rule (2026-09-12).** The ONLY project repository is **`jasur-ai/wakil`** (private). Two stray empty repos were created by another teammate at 10:05–10:07 UTC: `wakil` (PUBLIC — do NOT push anything there) and `wakil-everywhere` (private). **Neither is the project repo. Nobody creates new repos; nobody pushes anywhere but `jasur-ai/wakil`.** If you started in one of them, move your work to `wakil` (branch per role) and log it here.
