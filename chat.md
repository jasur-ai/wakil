# chat.md — the single source of truth for `wakil`

> Repo: **https://github.com/jasur-ai/wakil** (public) · Owner: **jasur-ai** · Spelling rule: **`wakil`** — never `vakil`.
> **Read this first.** Then your role's `README.md` (task sheet), then `contracts/`.

---

## 🚨 CONSOLIDATION NOTICE (2026-09-12)
There were **three** parallel repos under `jasur-ai`: `VAKIL`, `wakil`, `wakil-everywhere`. The owner decided:
- **ONE repo: `wakil`** (this one). Spelling **`wakil`** everywhere. **Public**.
- All real product work (previously in `VAKIL`) is now **here**: `contracts/`, `brain/`, `hands/`, `face/`, `voice/`, `docs/`, `spike/`.
- `VAKIL` and `wakil-everywhere` are **deleted**. Do not create new repos. Do not push anywhere but `jasur-ai/wakil`.
- If you started work in the old repos, it has been migrated here — continue on your branch.

## The three rules
1. **Append only.** Never rewrite or reformat someone else's entry. Add a new entry at the **bottom** of §5.
2. **Log before and after.** Write an entry when you *start* a task and one when you *finish* / hand off / get blocked.
3. **One task = one board row.** Update §4 in the same commit as your log entry. If two of us touch the board at once, the later push rebases — **do not delete** the other agent's rows.

## 1. Team & roles (consolidated)
| Agent | Role | Owns | Branch |
|---|---|---|---|
| **Lead** | Coordination, contracts, integration, demo/pitch, keeps `main` green & merges | `contracts/`, `voice/`, `chat.md`, `README.md` | `lead/<slug>` |
| **AI1** | **P1 BRAIN** — agent: guard, corpus, state machine, prompts, Whisper(uz), vision, learning, eval | `brain/` | `ai1/<slug>` |
| **AI2** | **P2 FACE** — Mini App UI/UX, tunnel, i18n, tablet choreography | `face/` | `ai2/<slug>` |
| **AI3** | **P3 HANDS** — session+2FA, flood, FastAPI, search/watcher, dossier, **spike (D1 10:30)** | `hands/` | `ai3/<slug>` |

- Commit prefix = your tag: `ai1: ...`, `ai2: ...`, `ai3: ...`, `lead: ...`.
- Never push directly to `main` — open a PR (lead merges). Exception: lead for docs-only.
- **No secrets in git.** Token lives outside the repo (`~/.wakil_token` → `$GITHUB_TOKEN`; runtime env `API_ID`/`API_HASH`/`BOT_TOKEN`).
- **Repo intelligence:** `python3 tools/ai3_repo_info.py` → refreshes `reports/repo-info.md` (anyone may run; keep it fresh after merges).

## 2. Entry template
```
### YYYY-MM-DD HH:MM (UTC) — <AGENT> — <START | UPDATE | DONE | BLOCKED | HANDOFF>
- Task:
- Branch / PR:
- What I did:
- Files touched:
- Result:
- Next / needs (who can unblock me):
```

## 3. What already exists (Day 0 — DONE, do not rebuild)
- **`contracts/`** — 4 frozen shared contracts (mandate schema, Hands API, Case Bus, Mini App REST). Change only via a logged Lead decision.
- **`brain/`** — `guard.py` **BoundaryGuard, 11 rules, stdlib-only**; `test_guard.py` **17/17 passing** (`python test_guard.py`); `corpus.py` (LegalCorpus, seeded 18-modda / uzum-14 / 1159); `graph.py` (state-machine skeleton); `prompts/strategy_uz.md`.
- **`hands/`** — `session.py` (login + **forced 2FA** `edit_2fa`), `flood.py`, `app.py` (FastAPI, all 7 endpoints + wipe, serves the mini app at `/`), `db.py`+`schema.sql` (9 tables), `dossier.py` (python-docx, 8 sections), `search.py`.
- **`face/`** — `index.html` single-page Mini App (8-step onboarding, live timeline 2s poll, escalation modal, prefs+provenance, search+price table, guardian, **WIPE**), UZ/EN.
- **`voice/`** — `runbook.md` (6 demo beats + failovers), `pitch-kit.md` (7 slides + 5-min script + Q&A×10), `counterpart_bot.py` (simulated @UzumSupport, 4 branches).
- **`docs/`** — full strategy: `wakil-v2-winning-edition.md` (design), `idea1-wakil-deep-dive.md` (architecture), `team-battle-plan.md` (per-role D1–D3), `team-brief-wakil.md`, visuals (`wakil-poster.svg`, `wakil-hero.jpg`).

## 4. Status board
| # | Task | Owner | Status | Updated |
|---|---|---|---|---|
| 1 | Consolidate 3 repos → single public `wakil` | Lead | ✅ DONE | 2026-09-12 |
| 2 | Migrate all product work into `wakil` (spelling → `wakil`) | Lead | ✅ DONE | 2026-09-12 |
| 3 | Spike: user-session presses bot button (`spike/resend_callback.md`) | AI3 | ⬜ TODO — **deadline D1 10:30** | 2026-09-12 |
| 4 | Guard suite green in `wakil` (extend, don't break) | AI1 | ✅ 17/17 re-verified on `ai1/brain-loop` — and 3 real guard bugs fixed there (R08 language, R01 below-floor leak, ungated `open_case`) | 2026-09-12 |
| 5 | Finish `brain/graph.py` loop + prompts + Whisper(uz) + vision + learning | AI1 | 🟡 PR open: loop, legal audit (2 demo-breaking errors), slots, vision, learning, eval (40 tests). **Whisper STT unverified — needs row 9 fixture + row 12 vendor.** | 2026-09-12 |
| 6 | Wire `face/` to live endpoints + tunnel public URL | AI2 | ⬜ TODO | 2026-09-12 |
| 7 | Stranger login → 2FA enforced → WIPE, E2E on a test account | AI3 | ⬜ TODO | 2026-09-12 |
| 8 | Bot face (aiogram) + search/watcher + dossier E2E | AI3 | ⬜ TODO | 2026-09-12 |
| 9 | Fixtures: 12s UZ voice note, 4 channel posts, 2 wallet screenshots | Lead | ⬜ TODO | 2026-09-12 |
| 10 | Deck from poster + script timed ×2 + Q&A cards | Lead | ⬜ TODO | 2026-09-12 |
| 11 | Rehearsals (D2:1, D3:6) + backup video + printed runbook | Lead | ⬜ TODO | 2026-09-12 |
| 12 | Pick the LLM vendor (one line in `DECISIONS.md`) — unblocks AI1 prompt tuning on real output | Lead | ⬜ TODO | 2026-09-12 |
| 13 | Confirm `@consumergovuz_bot` exists before shipping it as fact (README, AGENTS §brief, contracts/00 R11, runbook) | AI3 + Lead | ⬜ TODO | 2026-09-12 |
| 14 | Source chip `[18-modda · Qonun, 2023]` is wrong for a defect case → `[16-modda · 221-I, tahrir 2025]`; docs `wakil-v2` L123/149/152/197/199 + `face/` | AI2 (UI) + Lead (docs) | ⬜ TODO — evidence: `brain/legal_findings.md` §1 | 2026-09-12 |

Legend: ⬜ TODO · 🟡 IN PROGRESS/BLOCKED · ✅ DONE

## 5. Log ← append new entries at the bottom
### 2026-09-12 — LEAD — DONE (consolidation)
- Task: Resolve the 3-repo split; make `wakil` the single public source of truth.
- What I did: Owner decision (single repo `wakil`, public, spelling `wakil`). Migrated all product work from `VAKIL` into this repo, rewrote spelling `vakil`→`wakil` across all text + filenames, normalized env names (`WAKIL_DB`, `WAKIL_SESSIONS`), unified `chat.md`/`AGENTS.md`/`README.md`, kept the AI repo-scanner tool + PR template. Guard suite re-verified **17/17 green** in the new location.
- Files touched: repo-wide (product dirs added; `chat.md`, `AGENTS.md`, `README.md`, `docs/project-brief.md`, `ai-logs/*` unified).
- Result: one repo, one team, one spelling. `VAKIL` + `wakil-everywhere` deleted by lead (done).
- Next: AI3 spike (row 3, **10:30**); AI1/AI2/AI3 pick up rows 4–8.

### 2026-09-12 10:20 (UTC) — AI1 — START
- Task: board rows 4 + 5 (guard green; brain loop + corpus + Whisper slots + vision + learning + eval).
- Branch / PR: `ai1/brain-loop`.
- What I did: read the whole repo cold before writing a line (README → chat.md → brain/README → contracts → battle-plan). Note for the team: my first 25 minutes went to the now-deleted `VAKIL` repo because `wakil` 404'd at the time and `VAKIL` was the only thing that existed — that is why my work lands as one port instead of incremental pushes. Nothing of value was lost; nothing of mine is in the deleted repos.
- Next / needs: rows 12 (vendor) and 9 (voice fixture) unblock the rest of my D1 gate.

### 2026-09-12 — LEAD — UPDATE (official codebase decided)
- Task: Resolve the discovered **parallel implementation** `hackathon-ml/vakil` (TypeScript, different org account).
- What I did: Confirmed it is a separate **TS** build of the same spec — guard (10 rules) + negotiation engine (8 nodes) + LLM clients (anthropic/openai) + gramjs telegram gateway + dossier + mini-app API — actively pushed (last 10:38), has copied our strategy docs, bloated to ~18MB (committed `node_modules`), no README/chat. Owner confirmed it is **theirs** and decided **Python (`jasur-ai/wakil`) is the official codebase** (D0-12).
- Result: One official repo, one stack (**Python**). `hackathon-ml/vakil` = pending owner action (delete, or admin token for cleanup); **nobody works there**.
- Next: continue D1 gates here (AI3 spike **10:30**; board rows 4–8). If owner provides an admin token, lead cleans `hackathon-ml` (delete or strip `node_modules`).

### 2026-09-12 10:55 (UTC) — AI1 — DONE (rows 4 ✅, 5 🟡 awaiting review)
- Task: legal/fact audit of every claim in `brain/` + finish the brain loop + verification + learning + eval.
- Branch / PR: **https://github.com/jasur-ai/wakil/pull/2** (`ai1/brain-loop` → `main`; lead merges).
- **What I found (this is the part that matters — full audit: `brain/legal_findings.md`):**
  1. **Our demo case cited the wrong article.** Objective is *"nosoz iPhone 15 (ekran defekti)"* = a **defect**, but every doc/prompt/dossier line cites **18-modda**, which governs **good-quality** exchanges (`lex.uz/docs/-4704`, fetched today). A seller bot — or a lawyer in the jury — replies "10 kun o'tdi, bu sizning aybingiz" and hero beat 3 dies. Correct: **16-modda** (rescind + refund) / **17-modda** (settlement, refund in the same form as paid). Corpus now knows which article fits which case; advisory **R12 `check_article_fit()`** rewrites a mis-fit instead of sending it.
  2. **"2023 Consumer Protection Law" does not exist.** It is **№ 221-I of 26.04.1996**, current edition (amended by **O'RQ-1078 of 31.07.2025**). The source chip `[18-modda · Qonun, 2023]` in `docs/wakil-v2-winning-edition.md:149` + `face/` must change — that chip is our whole "no hallucinated law" claim. (rows 14)
  3. **"Uzum 14-day policy" is wrong and came from a blog.** Uzum's own offer: **10 calendar days** (some cases 30); quality objections within **warranty / 6 months**; seller has **20 days** to fix; and **seller silence 20 days = claim deemed accepted** ← new best move, now in `strategy_uz.md`. Real handle is **`@Uzum_Support_Bot`**.
  4. `corpus.audit()` **fails** if any entry lacks an https primary source, a `YYYY-MM-DD` fetch date or enough body — so this bug class can't return. Entries whose *text* I could not fetch (`28-modda`, the Civil-Code note) resolve for R09 but are `quotable()=False`.
- **3 real guard bugs fixed** (found by the harness, not by reading): R08 accepted *any* Latin text (an English demand passed); a below-floor number phrased as a normal sentence slipped past R01 (now: any number of ours ≠ their number = counter-offer → BLOCK); `open_case()` called `hands.send()` **with no guard at all**. Also: the bulk rename had dropped the dictionary word form from R07's matcher, so valid Uzbek disclosure was being rewritten — restored as a matcher only (§4.1), veto is 1 line.
- **Shipped:** `corpus.py` (verified), `guard.py` (R12 + fixes), `graph.py` (single gated `_turn` path, inbound classifier, case-kind-aware prompts, `verify()` gate, exception→memory), `slots.py` (voice→mandate, ASR injected), `verify.py` (5 fixtures, only `confirmed` closes), `learn.py` (typed prefs + provenance → prefill; a pref can never overwrite a stated floor), `eval.py` (10 transcripts + **independent** re-audit of every send), `test_brain.py` (40), `brain/legal_findings.md`, task sheet.
- Files touched: **`brain/` only** + board rows 4–5 + rows 12–14 added + this entry. `face/`, `hands/`, `voice/`, `contracts/` untouched.
- **Result (verified, not asserted):** `make test` → **17/17** (lead's suite, untouched and still green) · `cd brain && python3 -m unittest test_brain` → **Ran 40 … OK** · `python3 eval.py` → **guard violations: 0 (must be 0)**, 1/10 closed on verified money · all five self-tests OK. `make install` not run (no new deps — brain stays stdlib).
- **Honest gaps:** ① **Whisper STT is unverified** — no audio fixture in repo (row 9), `faster-whisper` not installed here. Slot parsing is tested on 3 transcripts incl. number-words and RU; the ASR leg is not. ② No real LLM yet (row 12) → prompt tuning not done. ③ Loop not yet run against the live counterparty bot (`eval.py` is the same shape; swapping `FakeHands`→`hands` is ~20 min once `hands/` exposes Contract 01). ④ `@consumergovuz_bot` still unverified (row 13) — my code refuses to print it as fact.
- Next / needs: row 12 (vendor, lead) · row 9 (voice clip, lead) · row 13 (ai3 probe) · then real-LLM prompt pass + integration.

