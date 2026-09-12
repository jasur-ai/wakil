# wakil

> Shared workspace for the **wakil** project, built collaboratively by three agents (**AI1**, **AI2**, **AI3**) coordinated by a **team lead**.
> Repo: https://github.com/jasur-ai/wakil

**Spelling matters:** the project is **`wakil`** — never `vakil`.

---

## Start here

1. **`chat.md`** — the shared work log. Read the status board, then append your own entry at the bottom.
2. **`AGENTS.md`** — the rules (branch naming, commit prefixes, definition of done).
3. **`reports/repo-info.md`** — a generated snapshot of this repo: file map, recent commits, open issues, languages. Regenerate with `python3 tools/ai3_repo_info.py`.

## Layout

| Path | What lives there |
|------|------------------|
| `chat.md` | Shared append-only log + status board |
| `AGENTS.md` | Working rules for agents |
| `docs/` | Briefs, specs, decisions |
| `ai-logs/` | Per-agent running notes (`ai1.md`, `ai2.md`, `ai3.md`) |
| `reports/` | Generated repo reports — do not hand-edit |
| `tools/` | Scripts (`ai3_repo_info.py` — repo scanner) |

## Agent roles

| Agent | Role |
|-------|------|
| **AI1** | Implementation (task-driven, see status board) |
| **AI2** | Implementation (task-driven, see status board) |
| **AI3** | Repo intelligence — scans this repo and publishes `reports/repo-info.md`; answers "where is X / what changed / who did what" |

## Quick start

```bash
git clone https://github.com/jasur-ai/wakil.git
cd wakil
export GITHUB_TOKEN="$(cat ~/.wakil_token)"   # token lives outside the repo on purpose
python3 tools/ai3_repo_info.py                # refresh reports/repo-info.md
```

## Status

Bootstrapped 2026-09-12: repo created, `chat.md` conventions in place, AI3's repo scanner live.
Scope/stack of the product itself is still to be confirmed — see `docs/project-brief.md`.
