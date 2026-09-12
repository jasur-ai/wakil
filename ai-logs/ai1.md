# AI1 — running notes (P1 BRAIN)

Role: **agent / brain**. Repo: **https://github.com/jasur-ai/wakil** · spelling **`wakil`** (never `vakil`).

Before starting: read `chat.md` §4 board → claim a row → branch `ai1/<slug>` → commit prefix `ai1:` → PR → append START + DONE to `chat.md` §5.

## My tasks (from board)
| Date | Task | Branch/PR | Status |
|------|------|-----------|--------|
| 2026-09-12 | Verify guard suite green in `wakil` (`python brain/test_guard.py`) | `ai1/brain-loop` | ✅ 17/17, +3 guard bugs fixed |
| 2026-09-12 | Finish `brain/graph.py` loop + prompts (from `prompts/strategy_uz.md`) + Whisper(uz) slot extraction + verification vision + learning loop + eval harness | `ai1/brain-loop` | 🟡 loop/prompts/verify/learn/eval + **legal audit** done; Whisper STT + live-bot integration pending |

## Notes / context
- **Do not rebuild** — `guard.py` (11 rules), `corpus.py`, `graph.py` skeleton, `prompts/strategy_uz.md` already exist. Extend them.
- Guard is stdlib-only and **17/17 green** — keep it green; it's the booth demo.
- LLM stays injected (vendor-agnostic). Guard is the last line — never bypass "for the demo".
- Every citation you emit must resolve in the corpus (R09).
- Task sheet: `brain/README.md`.

## Blockers / asks
- **LLM vendor** not chosen → real-output prompt tuning blocked (board row 12).
- **Voice fixture** (12s UZ) not in repo → Whisper leg unverified (row 9). `faster-whisper` also not installed here.
- `@consumergovuz_bot` unverified → keep it out of shipped UI copy until ai3's probe (row 13).

## Decisions I made (flag if wrong)
- `face/`, `hands/`, `voice/`, `contracts/` are other owners' — I only *reported* the wrong-law chip
  (row 14) rather than editing their files.
- R12 (article fit) is **advisory**, called from the Agent, not inserted into `check_outbound()` —
  so the rehearsed 17-test D0 gate is bit-identical. Fold it into the main chain if the lead wants.
- The dict word form stays in R07's matcher (input matching ≠ brand copy). Everything we *send* says `wakil`.

## Findings worth re-reading before the pitch
`brain/legal_findings.md` — esp. §1 (the two errors), §3 (pitch-grade numbers, incl. the
**1.6+ млрд so'm** order against Uzum, which is our best "the ladder bites" line), §4 (open items).
