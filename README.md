# wakil — Your Personal Telegram Delegate

> A chatbot answers. **wakil closes the case.**

**wakil** is an agentic consumer advocate for **Uzbekistan** that works **inside Telegram** — the messenger where the dispute already happens. You give it a signed **mandate** (objective, your floor, your walk-away). It negotiates with company support bots, human managers, and escalates up the **state ladder** to the Consumer Protection Agency (`@consumergovuz_bot`, hotline 1159), builds the complaint **dossier**, and reports "solved" **only when the money is verified**.

**Hard product rules (these ARE the product):**
1. Data **never leaves the device** — local FastAPI + SQLite; one machine is the only server.
2. **2FA enforced** at login — wakil refuses to run without it (`edit_2fa` wizard).
3. Acts **strictly inside the user's mandate** — 11-rule BoundaryGuard; an out-of-bounds offer never leaves without a user tap.
4. **No hallucinated law** — every citation must resolve in the local legal corpus with a real source.
5. Every guard decision is visible in the Mini App; **WIPE** deletes everything in one tap.

**Why now.** The arena is already in Telegram: company support bots + the state agency's own bot, 1B+ MAU platform (~85% of Uzbekistan), Uzum 20M MAU, e-com growing 40%/yr, the 2023 Consumer Protection Law (Art. 18 = 10-day return) — and 33% of state complaints are exactly our case. Gartner says >40% of agentic projects die by 2027 from unclear value + weak risk controls. **wakil is the counter-position: the mandate is the value, the guard is the risk control.**

---

## Start here (for agents)
1. **`chat.md`** — the single source of truth: team, roles, status board, append-only log.
2. **`AGENTS.md`** — the rules (spelling `wakil`, branch/commit prefixes, definition of done).
3. Your role's **`README.md`** (`brain/`, `face/`, or `hands/`) — your task sheet.
4. **`contracts/`** — the 4 frozen shared contracts.
5. **`reports/repo-info.md`** — a generated snapshot (file map, commits, languages). Regenerate: `python3 tools/ai3_repo_info.py`.

## Layout
| Path | What lives there |
|------|------------------|
| `chat.md` | Single source of truth (board + append-only log) |
| `AGENTS.md` / `DECISIONS.md` | Working rules / frozen decisions |
| `contracts/` | 4 frozen shared contracts (mandate, hands API, case bus, mini-app REST) |
| `brain/` | **P1 (AI1)** — BoundaryGuard (11 rules, 17 tests), LegalCorpus, state machine, UZ strategy |
| `hands/` | **P3 (AI3)** — session+2FA, flood queue, FastAPI (7 endpoints), schema, dossier, search |
| `face/` | **P2 (AI2)** — single-page Mini App (no build step) |
| `voice/` | **P4 (Lead)** — demo runbook, pitch kit, simulated @UzumSupport counterparty bot |
| `spike/` | Timeboxed investigations (e.g. `resend_callback.md`) |
| `docs/` | Full strategy (v1 deep-dive, v2 winning edition, battle plan, brief) + visuals |
| `ai-logs/` · `reports/` · `tools/` | Per-agent notes · generated repo reports · repo scanner |

## Agent roles
| Agent | Role | Owns |
|---|---|---|
| **Lead** | Coordination, contracts, integration, demo/pitch, keeps `main` green | `contracts/`, `voice/` |
| **AI1** | P1 BRAIN — agent (guard, corpus, loop, prompts, Whisper(uz), vision, learning, eval) | `brain/` |
| **AI2** | P2 FACE — Mini App UI/UX, tunnel, i18n, tablet choreography | `face/` |
| **AI3** | P3 HANDS — session+2FA, flood, FastAPI, search/watcher, dossier, spike | `hands/` |

## Quick start
```bash
make install              # python deps (hands + voice)
make test                 # brain guard suite (17 tests, stdlib-only)
make demo                 # hands FastAPI on :8000 (mini app served at /)

# repo snapshot (after merges)
export GITHUB_TOKEN="$(cat ~/.wakil_token)"
python3 tools/ai3_repo_info.py
```

## Status
Consolidated **2026-09-12** into this single public repo (was: `VAKIL` + `wakil` + `wakil-everywhere`). Day-0 trust core is green: guard **17/17 tests**, corpus seeded, session/2FA + FastAPI skeleton in place. Per-role D1–D3 plan: `docs/team-battle-plan.md`.

*Spelling: **`wakil`** — never `vakil`.*
