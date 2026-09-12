# AGENTS.md — how to work in this repo

Repo: **https://github.com/jasur-ai/wakil** (public) · Owner: **jasur-ai**
Spelling: **`wakil`**, always. Never `vakil` (in code, docs, commits, branch names).

## What this project is (30-second brief)
**wakil** is a personal **Telegram delegate** for Uzbekistan: you give it a signed **mandate** (objective, floor, walk-away); it negotiates in-bounds with company support bots + human managers, escalates up the **state ladder** (→ `@consumergovuz_bot` / hotline 1159), builds a complaint **dossier**, and reports success **only after the money is verified**. Hard rules: **data local-only**, **2FA enforced**, **11-rule BoundaryGuard**, **no hallucinated law**, **one-tap WIPE**. Full design: `docs/wakil-v2-winning-edition.md`.

## Who you are
- **Lead** — coordinates, keeps `main` green, reviews/merges PRs, owns `contracts/` + `voice/`.
- **AI1 / AI2 / AI3** — implementation. Pick a task from the status board in `chat.md` §4, claim the row, then work.

## Ground rules
1. **Spelling**: `wakil`. Never `vakil`.
2. **Append-only log**: never rewrite another agent's `chat.md` entry (§5).
3. **Branches**: `ai1/<slug>`, `ai2/<slug>`, `ai3/<slug>`, `lead/<slug>`. PR into `main`; lead merges.
4. **Commit prefix**: `ai1: ...`, `ai2: ...`, `ai3: ...`, `lead: ...`.
5. **Check the board before starting** — if a task is claimed, don't duplicate it.
6. **No secrets in git.** Token from `~/.wakil_token` → `$GITHUB_TOKEN`; runtime `API_ID`/`API_HASH`/`BOT_TOKEN`. `.gitignore` covers `.env*`, `*.session`, `sessions/`, `*.db`.
7. **If you add code, add the smallest thing that proves it runs**, and say how you verified it in your log entry.

## Repo layout
```
wakil/
├── chat.md              # single source of truth (append-only, §5)
├── AGENTS.md            # this file
├── README.md            # project overview + quickstart
├── DECISIONS.md         # frozen decisions (change only via lead)
├── Makefile             # make install / test / demo
├── contracts/           # 4 frozen shared contracts (P1 canonical mandate)
├── brain/               # P1 (AI1): guard (11 rules, 17 tests), corpus, graph, prompts
├── hands/               # P3 (AI3): session+2FA, flood, FastAPI, schema, dossier, search
├── face/                # P2 (AI2): single-page Mini App (no build step)
├── voice/               # P4 (Lead): runbook, pitch kit, counterparty bot
├── spike/               # timeboxed investigations (e.g. resend_callback)
├── docs/                # strategy + visuals
├── ai-logs/             # per-agent running notes
├── reports/             # generated (do not hand-edit) — repo-info.md/.json
└── tools/ai3_repo_info.py  # repo scanner (stdlib only)
```

## Commands
```bash
make install              # python deps (hands + voice)
make test                 # brain guard suite (17 tests, stdlib-only)
make demo                 # hands FastAPI on :8000 (mini app served at /)

# repo snapshot (keep reports/ fresh after merges)
export GITHUB_TOKEN="$(cat ~/.wakil_token)"
python3 tools/ai3_repo_info.py            # writes reports/repo-info.md + .json
```

## Definition of done (per task)
- [ ] Board row in `chat.md` §4 updated.
- [ ] Start **and** finish entries appended to `chat.md` §5.
- [ ] Code committed on your branch with the right prefix and a PR opened.
- [ ] You state how you verified it (tests run / command / screenshot).
- [ ] If you touched repo structure, `reports/repo-info.md` regenerated.
