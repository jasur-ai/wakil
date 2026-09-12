# AGENTS.md — how to work in this repo

Repo: **https://github.com/jasur-ai/wakil** · Owner: **jasur-ai**
Spelling: **`wakil`**, always. Not `vakil`.

## Who you are

There are **three agents** working here at a time: **AI1**, **AI2**, **AI3**.
The **team lead** coordinates, keeps `main` green and reviews/merges PRs.

- **AI1 / AI2** — implementation. Pick a task from the status board in `chat.md`.
- **AI3** — repo intelligence. Finds information *in* / *about* this repo and keeps `reports/repo-info.md` current.

Everyone: **read `chat.md` first, then append your entry at the bottom of section 4.**

## Ground rules

1. **Spelling**: the project is `wakil`. Never write `vakil` in code, docs, commits or branch names.
2. **Append-only log**: never rewrite another agent's `chat.md` entry.
3. **Branches**: `ai1/<slug>`, `ai2/<slug>`, `ai3/<slug>`, `lead/<slug>`. PR into `main`; the lead merges.
4. **Commit prefix**: `ai1: ...`, `ai2: ...`, `ai3: ...`, `lead: ...`.
5. **Check the board before starting** — if a task is claimed, don't duplicate it.
6. **No secrets in git.** The GitHub token is read from `$GITHUB_TOKEN` (stored outside the repo in `~/.wakil_token`). `.gitignore` covers `.env*`.
7. **Tests / verification**: if you add code, add the smallest thing that proves it runs, and say how you verified it in your log entry.

## Repo layout

```
wakil/
├── chat.md              # shared work log  (append-only, section 4)
├── AGENTS.md            # this file
├── README.md            # project overview
├── docs/                # specs, briefs, decisions
├── ai-logs/             # per-agent running notes (ai1.md, ai2.md, ai3.md)
├── reports/             # generated reports (do not hand-edit)
│   ├── repo-info.md     # <- AI3 generates
│   └── repo-info.json   # <- AI3 generates
└── tools/               # scripts
    └── ai3_repo_info.py # repo scanner (stdlib only, no pip install needed)
```

## Commands

```bash
# clone
git clone https://github.com/jasur-ai/wakil.git && cd wakil

# refresh the repo snapshot (AI3's tool)
export GITHUB_TOKEN="$(cat ~/.wakil_token)"
python3 tools/ai3_repo_info.py                 # writes reports/repo-info.md + .json
python3 tools/ai3_repo_info.py --json-only     # machine-readable only
python3 tools/ai3_repo_info.py --repo owner/name
```

## Definition of done (per task)

- [ ] Task row in `chat.md` status board updated.
- [ ] Start *and* finish entries appended to `chat.md`.
- [ ] Code committed on your branch with the right prefix and a PR opened.
- [ ] If you touched repo structure, `reports/repo-info.md` regenerated (ask AI3 or run the tool).
