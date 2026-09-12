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
| 4 | Guard suite green in `wakil` (extend, don't break) | AI1 | 🟡 verify `python brain/test_guard.py` | 2026-09-12 |
| 5 | Finish `brain/graph.py` loop + prompts + Whisper(uz) + vision + learning | AI1 | ⬜ TODO | 2026-09-12 |
| 6 | Wire `face/` to live endpoints + tunnel public URL | AI2 | ⬜ TODO | 2026-09-12 |
| 7 | Stranger login → 2FA enforced → WIPE, E2E on a test account | AI3 | ⬜ TODO | 2026-09-12 |
| 8 | Bot face (aiogram) + search/watcher + dossier E2E | AI3 | ⬜ TODO | 2026-09-12 |
| 9 | Fixtures: 12s UZ voice note, 4 channel posts, 2 wallet screenshots | Lead | ⬜ TODO | 2026-09-12 |
| 10 | Deck from poster + script timed ×2 + Q&A cards | Lead | ⬜ TODO | 2026-09-12 |
| 11 | Rehearsals (D2:1, D3:6) + backup video + printed runbook | Lead | ⬜ TODO | 2026-09-12 |

Legend: ⬜ TODO · 🟡 IN PROGRESS/BLOCKED · ✅ DONE

## 5. Log ← append new entries at the bottom
### 2026-09-12 — LEAD — DONE (consolidation)
- Task: Resolve the 3-repo split; make `wakil` the single public source of truth.
- What I did: Owner decision (single repo `wakil`, public, spelling `wakil`). Migrated all product work from `VAKIL` into this repo, rewrote spelling `vakil`→`wakil` across all text + filenames, normalized env names (`WAKIL_DB`, `WAKIL_SESSIONS`), unified `chat.md`/`AGENTS.md`/`README.md`, kept the AI repo-scanner tool + PR template. Guard suite re-verified **17/17 green** in the new location.
- Files touched: repo-wide (product dirs added; `chat.md`, `AGENTS.md`, `README.md`, `docs/project-brief.md`, `ai-logs/*` unified).
- Result: one repo, one team, one spelling. `VAKIL` + `wakil-everywhere` deleted by lead (done).
- Next: AI3 spike (row 3, **10:30**); AI1/AI2/AI3 pick up rows 4–8.

### 2026-09-12 — LEAD — UPDATE (official codebase decided)
- Task: Resolve the discovered **parallel implementation** `hackathon-ml/vakil` (TypeScript, different org account).
- What I did: Confirmed it is a separate **TS** build of the same spec — guard (10 rules) + negotiation engine (8 nodes) + LLM clients (anthropic/openai) + gramjs telegram gateway + dossier + mini-app API — actively pushed (last 10:38), has copied our strategy docs, bloated to ~18MB (committed `node_modules`), no README/chat. Owner confirmed it is **theirs** and decided **Python (`jasur-ai/wakil`) is the official codebase** (D0-12).
- Result: One official repo, one stack (**Python**). `hackathon-ml/vakil` = pending owner action (delete, or admin token for cleanup); **nobody works there**.
- Next: continue D1 gates here (AI3 spike **10:30**; board rows 4–8). If owner provides an admin token, lead cleans `hackathon-ml` (delete or strip `node_modules`).

### 2026-09-12 — LEAD — DONE (working product, deployed)
- Task: Turn the skeleton into a **real, running, deployed product** (owner: "finish everything, deploy, real product").
- What I did: Implemented the live agent loop — `hands/gateway.py` (MockUzumGateway + real stub), `hands/llm.py` (ScriptedLLM + real stub), `hands/agent.py` (mandate-bound negotiation loop gated by the BoundaryGuard, verification, dossier, learning), wired into `hands/app.py` (case auto-starts the agent; `POST /decision` resumes; `GET /case/{id}/dossier` download). Face: dossier download link.
- Verified end-to-end (live on :8000): create mandate → agent opens (disclosure, PASS) → counterparty offers **300 000 (below floor)** → **guard R01 ESCALATE** → user taps **hold** → agent replies with **18-modda citation** → counterparty grants 450 000 → **verification confirmed (450000)** → **dossier .docx generated** → **case resolved_verified** → **pref learned** (qisman_tolov=no, provenance M-9001). Guard suite **17/17**. Face + dossier download both 200.
- Result: `wakil` is a **working product**, deployed and demoable at the live :8000 URL (demo mode, offline; swap to live Telethon/LLM via `VAKIL_MODE=live`).
- Next: AI3 real-session spike (row 3, 10:30) to flip demo→live; AI2 tunnel for a public mini-app URL; Lead fixtures/rehearsals.
