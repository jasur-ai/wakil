# AI2 — running notes (P2 FACE)

Role: **Mini App UI/UX**. Repo: **https://github.com/jasur-ai/wakil** · spelling **`wakil`** (never `vakil`).

Before starting: read `chat.md` §4 board → claim a row → branch `ai2/<slug>` → commit prefix `ai2:` → PR → append START + DONE to `chat.md` §5.

## My tasks (from board)
| Date | Task | Branch/PR | Status |
|------|------|-----------|--------|
| 2026-09-12 | Wire `face/index.html` to live endpoints (`hands/app.py` serves it at `/`) + Cloudflare quick tunnel public URL | `ai2/wire-face` | ⬜ |
| 2026-09-12 | Live timeline vs real Case Bus events + 2-phone (owner + guardian) + Lead approves UZ copy at D2 standup | `ai2/live-timeline` | ⬜ |
| 2026-09-12 | Polish pass on demo screens; tablet-operator tap choreography into `voice/runbook.md`; freeze D3 14:00 | `ai2/polish` | ⬜ |

## Notes / context
- **Do not rebuild** — `face/index.html` already has: 8-step onboarding (2FA-enforce), live timeline (2s poll), escalation modal, prefs+provenance, search+price table, guardian, WIPE, UZ/EN. Extend it.
- One HTML file, no build step. UI validation mirrors `contracts/00` (incomplete mandate can't be submitted).
- Polling (2s) is the design (D0-9). Every guard decision visible — no silent rewrites.
- Demo-critical screens only (runbook beats 1,2,3,4,6).
- Task sheet: `face/README.md`.
