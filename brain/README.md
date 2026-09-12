# P1 — BRAIN (owner: ai1)

**Mission.** The agent that negotiates in-bounds, cites real law, verifies money, and learns. The 3 hero beats must be flawless: (1) guard refuses an out-of-bounds offer, (2) a real law citation leaves with a source chip, (3) close only on verified money.

**"Training" note (pitch line).** We don't train a model — the LLM is rented. What we ship: guard + corpus + strategy + memory + eval. *The model is a commodity; the mandate, the guard, and the memory are the product.*

## Already built by lead (green — extend, don't break)
- `guard.py` — BoundaryGuard, **11 rules**, stdlib-only · `test_guard.py` — **16 passing tests** (`python test_guard.py`)
- `corpus.py` — LegalCorpus (sqlite), seeded: `18-modda`, `uzum-14`, `1159` (`python corpus.py` self-test)
- `graph.py` — Agent skeleton: loop, rewrite budget, escalation, user decisions
- `prompts/strategy_uz.md` — tone + move ladder (UZ)

## Run everything (ai1 additions)
```
python3 test_guard.py            # D0 gate suite — 17 tests, lead's, keep green
python3 -m unittest test_brain    # ai1 suite — 40 tests (corpus, R12, slots, verify, learn, loop)
python3 eval.py                   # 10 scripted transcripts → "guard violations: 0 (must be 0)"
python3 corpus.py && python3 slots.py && python3 verify.py && python3 learn.py   # self-tests
```
`make test` in the repo root still runs only `test_guard.py` — lead owns the Makefile; proposed
addition: `cd brain && $(PY) -m unittest test_brain && $(PY) eval.py`.

**Read first: `legal_findings.md`** — the audit of every legal claim in the repo (2 corrections
that would have failed the demo are already fixed in code there).

## Your tasks (docs/team-battle-plan.md §P1)
- [x] **D1 EOD** — guard suite still green (17/17 untouched) + **3 real guard bugs fixed**; corpus seeding E2E (add entries from docs sources w/ source_url + fetched_at); **Whisper (uz, self-hosted) on 3 fixture clips → slot JSON** (voice note → mandate prefill)
      → **slot parser done + tested on 3 transcripts** (`slots.py`); *STT leg still unverified —
      needs the voice fixture (board row 9) and `faster-whisper` installed.*
- [~] **D2 EOD** — loop finished and driven by `eval.py` against scripted transcripts; **still to
      run against the live counterparty bot**. Vision + learning are done (`verify.py`, `learn.py`).
- **D2 EOD** — full loop vs the counterparty bot (`voice/counterpart_bot.py`, branches deny/grant): denial → below-min → **guard.escalation** → hold → **outbound with law citation** → resolution; verification vision (JSON schema; 5 fixtures: 2 match / 2 mismatch / 1 garbage); learning loop (👎 + tag → typed pref with provenance → 2nd mandate pre-filled, assertion test).
- [~] **D3** — eval harness **shipped**: 10 scripted transcripts, **0 guard violations**, closed-rate
      reported, independent re-audit of every send. Prompt tuning on real LLM output still pending
      (vendor undecided).

## Still mine (next block)
- integration loop against P4's counterparty bot (needs it running) — `eval.py` is the same shape,
  so it should be a 20-min swap of `FakeHands` for the real `hands` object;
- prompt tuning on real LLM output (vendor still undecided — **D0 blocker, log it in chat.md**);
- dossier citation block: emit `{ref, title, source_url, fetched_at}` per cite so P3's .docx
  carries sources, and drop any ref where `corpus.quotable(ref)` is False.

## Non-negotiables
- `llm` stays injected (vendor-agnostic). Guard is the last line — never bypass for "the demo".
- Every citation you emit must resolve in the corpus (R09). Corpus entry = ref + title + body + source_url + fetched_at.
- Add tests for anything new; keep `python test_guard.py` green (it's the booth demo).
