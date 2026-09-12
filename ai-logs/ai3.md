# AI3 — running notes  *(repo intelligence)*

**My job:** be the agent that *knows* this repo. Find things, publish facts, keep `reports/repo-info.md` fresh.
Repo: https://github.com/jasur-ai/wakil — spelling is **`wakil`**, never `vakil`.

## What I own

- `tools/ai3_repo_info.py` — the scanner (stdlib only, no dependencies).
- `reports/repo-info.md` — human-readable repo snapshot (**generated**, never hand-edit).
- `reports/repo-info.json` — the same data as JSON, for other agents to consume.

## How to run me

```bash
export GITHUB_TOKEN="$(cat ~/.wakil_token)"     # token lives outside the repo on purpose
python3 tools/ai3_repo_info.py                  # reports/repo-info.md + .json
python3 tools/ai3_repo_info.py --json-only
python3 tools/ai3_repo_info.py --repo owner/name --out-dir reports
```

No `GITHUB_TOKEN` still works for public repos, but rate-limits hard (60 req/hour unauthenticated).

## What the report answers

- What is this repo? (visibility, description, license, topics, size, stars)
- What's in it? (full file map + detected stack signals)
- What changed lately? (last ~30 commits, who authored them)
- Who works on it? (contributors, branch/tag/release list)
- What's open? (issues + PRs with authors and labels)
- How hot is it? (14-day views/clones, if the token has push rights)

## Refresh policy

Re-run after: any merge to `main`, any new branch worth tracking, or whenever AI1/AI2 ask a
"where is X / what changed / who did what" question that the current report can't answer.
Log every refresh in `chat.md`.

## Run history

| Date (UTC) | Trigger | Result |
|------------|---------|--------|
| 2026-09-12 | Repo bootstrap — first scan | `reports/repo-info.md` created |

## Backlog for me

- [ ] Add `--grep` so agents can search file contents via the code-search API.
- [ ] Add a `--diff-since <sha>` mode: "what changed since commit X".
- [ ] Emit a per-directory LOC table.
- [ ] Optional: watch open PRs and post a summary into `chat.md`.
