# chat.md — shared work log for `wakil`

> This file is the **single source of truth** for coordination between the agents working on this repo.
> Repo: **https://github.com/jasur-ai/wakil**  ·  Owner: **jasur-ai**  ·  Spelling rule: **`wakil`** — never `vakil`.

---

## 0. The three rules

1. **Append only.** Never rewrite or reformat someone else's entry. Add a new `###` entry at the **bottom** of the log (section 4).
2. **Log before and after.** Write an entry when you *start* a task and another when you *finish* it (or when you hand it off / get blocked).
3. **One task = one line in the board.** Update section 3 (Status board) in the same commit as your log entry. If two of us touch the board at once, the later push rebases and re-applies — do **not** delete the other agent's rows.

---

## 1. Team & roles

| Agent | Role | Owns | Notes |
|-------|------|------|-------|
| **Team lead** | Coordination, repo & branch hygiene, merges, final review | `README.md`, `docs/`, releases | Keeps `chat.md` structure stable, resolves conflicts between agents |
| **AI1** | *(to be assigned — build / feature implementation)* | `src/` | Claim a task in section 3 first |
| **AI2** | *(to be assigned — build / feature implementation)* | `src/` | Claim a task in section 3 first |
| **AI3** | **Repo intelligence** — find & publish information *in* / *about* repo `wakil` | `tools/ai3_repo_info.py`, `reports/` | Scans the repo (files, commits, issues, languages, size, activity) and keeps `reports/repo-info.md` fresh. Answers "where is X / what changed / who did what" questions for the others. |

**Conventions**

- Branch naming: `ai1/<slug>`, `ai2/<slug>`, `ai3/<slug>`, `lead/<slug>`.
- Commit prefix with your tag: `ai3: refresh repo-info report`.
- Never push directly to `main` — open a PR (except the lead for docs-only or release commits).
- Never commit secrets. GitHub token lives **outside** the repo (`~/.wakil_token`), loaded as `$GITHUB_TOKEN`.

---

## 2. Entry template (copy this)

```
### YYYY-MM-DD HH:MM (UTC) — AI? — <status: START | UPDATE | DONE | BLOCKED | HANDOFF>
- Task:
- Branch / PR:
- What I did:
- Files touched:
- Result:
- Next / needs (who can unblock me):
```

---

## 3. Status board

| # | Task | Owner | Status | Updated |
|---|------|-------|--------|---------|
| 1 | Create GitHub repo `jasur-ai/wakil` | Team lead (AI3 acting) | ✅ DONE | 2026-09-12 |
| 2 | Create `chat.md` shared log + team/role conventions | Team lead (AI3 acting) | ✅ DONE | 2026-09-12 |
| 3 | Repo skeleton: README, AGENTS.md, docs/, .gitignore | Team lead (AI3 acting) | ✅ DONE | 2026-09-12 |
| 4 | AI3 repo-intelligence tool + first `reports/repo-info.md` | AI3 | ✅ DONE | 2026-09-12 |
| 5 | *(open)* Project brief — what `wakil` actually is / stack / scope | Team lead | 🟡 OPEN — needs user input | |
| 6 | *(open)* AI1 first task | AI1 | ⬜ TODO | |
| 7 | *(open)* AI2 first task | AI2 | ⬜ TODO | |

Legend: ⬜ TODO · 🟡 IN PROGRESS / BLOCKED · ✅ DONE

---

## 4. Log  ← append new entries at the bottom

### 2026-09-12 — TEAM LEAD / AI3 — DONE
- Task: Bootstrap the repo and the shared log.
- Branch / PR: `main` (initial commit, direct push by lead).
- What I did:
  - Created the public GitHub repo **jasur-ai/wakil** (https://github.com/jasur-ai/wakil) with issues + wiki + projects enabled, default branch `main`.
  - Wrote `chat.md` (this file): rules, roles, entry template, status board.
  - Wrote `README.md`, `AGENTS.md` (rules for agents), `docs/project-brief.md`, `.gitignore`.
- Files touched: `chat.md`, `README.md`, `AGENTS.md`, `docs/project-brief.md`, `.gitignore`.
- Result: repo exists and is cloneable; coordination rules are in place.
- Next: AI3 scans the repo and publishes `reports/repo-info.md`; lead asks the user to confirm scope/stack so AI1 and AI2 can pick up real tasks.

### 2026-09-12 — AI3 — DONE
- Task: Repo intelligence — make repo `wakil` machine- and human-readable for the other agents.
- Branch / PR: `main`.
- What I did:
  - Added `tools/ai3_repo_info.py`: a dependency-free (stdlib-only) GitHub API scanner. It pulls repo metadata, branches, tags, recent commits, contributors, the full file tree, open issues/PRs, language breakdown and traffic, then emits `reports/repo-info.md` + `reports/repo-info.json`.
  - Ran it → produced the first `reports/repo-info.md` (repo snapshot + file map + activity).
  - Documented how to run it (`GITHUB_TOKEN=... python3 tools/ai3_repo_info.py`) in `AGENTS.md` and in my own `ai-logs/ai3.md`.
- Files touched: `tools/ai3_repo_info.py`, `reports/repo-info.md`, `reports/repo-info.json`, `ai-logs/ai3.md`.
- Result: anyone (AI1/AI2/lead) can now answer "what's in this repo / what changed recently" in one look, or re-run the scanner for a fresh snapshot.
- Next: keep `reports/repo-info.md` refreshed after every notable change; answer lookup questions from AI1/AI2 on request.
