# AI1 — running notes (P1 BRAIN)

Role: **agent / brain**. Repo: **https://github.com/jasur-ai/wakil** · spelling **`wakil`** (never `vakil`).

Before starting: read `chat.md` §4 board → claim a row → branch `ai1/<slug>` → commit prefix `ai1:` → PR → append START + DONE to `chat.md` §5.

## My tasks (from board)
| Date | Task | Branch/PR | Status |
|------|------|-----------|--------|
| 2026-09-12 | Verify guard suite green in `wakil` (`python brain/test_guard.py`) | — | ⬜ |
| 2026-09-12 | Finish `brain/graph.py` loop + prompts (from `prompts/strategy_uz.md`) + Whisper(uz) slot extraction + verification vision + learning loop + eval harness | `ai1/brain-loop` | ⬜ |

## Notes / context
- **Do not rebuild** — `guard.py` (11 rules), `corpus.py`, `graph.py` skeleton, `prompts/strategy_uz.md` already exist. Extend them.
- Guard is stdlib-only and **17/17 green** — keep it green; it's the booth demo.
- LLM stays injected (vendor-agnostic). Guard is the last line — never bypass "for the demo".
- Every citation you emit must resolve in the corpus (R09).
- Task sheet: `brain/README.md`.
