# P1 — BRAIN (owner: ai1)

**Mission.** The agent that negotiates in-bounds, cites real law, verifies money, and learns. The 3 hero beats must be flawless: (1) guard refuses an out-of-bounds offer, (2) a real law citation leaves with a source chip, (3) close only on verified money.

**"Training" note (pitch line).** We don't train a model — the LLM is rented. What we ship: guard + corpus + strategy + memory + eval. *The model is a commodity; the mandate, the guard, and the memory are the product.*

## Already built by lead (green — extend, don't break)
- `guard.py` — BoundaryGuard, **11 rules**, stdlib-only · `test_guard.py` — **16 passing tests** (`python test_guard.py`)
- `corpus.py` — LegalCorpus (sqlite), seeded: `18-modda`, `uzum-14`, `1159` (`python corpus.py` self-test)
- `graph.py` — Agent skeleton: loop, rewrite budget, escalation, user decisions
- `prompts/strategy_uz.md` — tone + move ladder (UZ)

## Your tasks (docs/team-battle-plan.md §P1)
- **D1 EOD** — guard suite still green; corpus seeding E2E (add entries from docs sources w/ source_url + fetched_at); **Whisper (uz, self-hosted) on 3 fixture clips → slot JSON** (voice note → mandate prefill).
- **D2 EOD** — full loop vs the counterparty bot (`voice/counterpart_bot.py`, branches deny/grant): denial → below-min → **guard.escalation** → hold → **outbound with law citation** → resolution; verification vision (JSON schema; 5 fixtures: 2 match / 2 mismatch / 1 garbage); learning loop (👎 + tag → typed pref with provenance → 2nd mandate pre-filled, assertion test).
- **D3** — eval harness: 10 scripted transcripts → **0 guard violations** + win rate; prompt tuning; freeze 14:00; rehearsal support.

## Non-negotiables
- `llm` stays injected (vendor-agnostic). Guard is the last line — never bypass for "the demo".
- Every citation you emit must resolve in the corpus (R09). Corpus entry = ref + title + body + source_url + fetched_at.
- Add tests for anything new; keep `python test_guard.py` green (it's the booth demo).
