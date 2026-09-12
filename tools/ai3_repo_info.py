#!/usr/bin/env python3
"""
ai3_repo_info.py — AI3's repo-intelligence scanner.

Pulls everything worth knowing about a GitHub repo and renders it as
`reports/repo-info.md` (human) + `reports/repo-info.json` (machine).

Stdlib only — no pip install required.

Usage
-----
    export GITHUB_TOKEN="$(cat ~/.wakil_token)"     # or any PAT
    python3 tools/ai3_repo_info.py                  # default repo: jasur-ai/wakil
    python3 tools/ai3_repo_info.py --repo owner/name
    python3 tools/ai3_repo_info.py --json-only
    python3 tools/ai3_repo_info.py --out-dir reports

Exit codes: 0 ok, 1 fatal (bad token / repo not found / network).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

API = "https://api.github.com"
DEFAULT_REPO = "jasur-ai/wakil"
UA = "wakil-ai3-repo-scanner/1.0"


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
def _request(url: str, token: str | None, timeout: int = 30):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": UA,
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8")), dict(resp.headers)


def get(path_or_url: str, token: str | None, params: dict | None = None):
    """GET a GitHub API path. Returns (data, ok). Never raises."""
    url = path_or_url if path_or_url.startswith("http") else API + path_or_url
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    try:
        data, _ = _request(url, token)
        return data, True
    except urllib.error.HTTPError as e:  # 404/403/etc — degrade gracefully
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            body = {"message": str(e)}
        return {"_error": e.code, "_message": body.get("message", str(e))}, False
    except Exception as e:  # network, dns, timeout
        return {"_error": -1, "_message": str(e)}, False


def paged(path: str, token: str | None, per_page: int = 100, max_pages: int = 5):
    """Follow Link rel=next up to max_pages."""
    out, page = [], 1
    while page <= max_pages:
        data, ok = get(path, token, {"per_page": per_page, "page": page})
        if not ok or not isinstance(data, list) or not data:
            break
        out.extend(data)
        if len(data) < per_page:
            break
        page += 1
    return out


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def iso(ts: str | None) -> str:
    return (ts or "").replace("T", " ").replace("Z", " UTC") or "—"


def ago(ts: str | None) -> str:
    if not ts:
        return "—"
    try:
        then = _dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=_dt.timezone.utc)
    except ValueError:
        return "—"
    delta = _dt.datetime.now(_dt.timezone.utc) - then
    days = delta.days
    if days <= 0:
        return "today"
    if days == 1:
        return "yesterday"
    if days < 30:
        return f"{days} days ago"
    if days < 365:
        return f"{days // 30} months ago"
    return f"{days // 365} years ago"


def human(n: int | None) -> str:
    if n is None:
        return "—"
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} TB"


def who(u) -> str:
    if not isinstance(u, dict):
        return "—"
    return u.get("login") or u.get("name") or "—"


def guess_stack(tree: list[dict]) -> list[str]:
    exts = Counter(
        (Path(f["path"]).suffix or Path(f["path"]).name).lower()
        for f in tree if f.get("type") == "blob"
    )
    names = {f["path"].rsplit("/", 1)[-1].lower() for f in tree if f.get("type") == "blob"}
    signals: list[str] = []
    table = [
        ("Python", lambda: exts[".py"] > 0),
        ("JavaScript/TypeScript", lambda: (exts[".js"] + exts[".ts"] + exts[".jsx"] + exts[".tsx"]) > 0),
        ("Node/npm", lambda: "package.json" in names),
        ("React/Next.js", lambda: any(n in names for n in ("next.config.js", "next.config.mjs", "next.config.ts")) or exts[".jsx"] + exts[".tsx"] > 0),
        ("FastAPI/Flask/Django", lambda: any(n in names for n in ("requirements.txt", "pyproject.toml", "manage.py", "main.py", "app.py"))),
        ("Docker", lambda: "dockerfile" in names or "docker-compose.yml" in names),
        ("CI (GitHub Actions)", lambda: any(".github/workflows/" in f["path"] for f in tree)),
        ("Docs (Markdown)", lambda: exts[".md"] > 0),
    ]
    for label, test in table:
        try:
            if test():
                signals.append(label)
        except Exception:
            pass
    return signals


# --------------------------------------------------------------------------- #
# collect
# --------------------------------------------------------------------------- #
def collect(repo: str, token: str | None) -> dict:
    info: dict = {"repo": repo, "generated_at_utc": _dt.datetime.now(_dt.timezone.utc)
                  .strftime("%Y-%m-%d %H:%M:%S UTC")}

    meta, ok = get(f"/repos/{repo}", token)
    if not ok:
        msg = meta.get("_message", "unknown error")
        code = meta.get("_error")
        if code == 404:
            raise SystemExit(f"[ai3] fatal: repo '{repo}' not found (404) or token lacks access.\n  → {msg}")
        raise SystemExit(f"[ai3] fatal: cannot read '{repo}' — {msg}")
    info["meta"] = meta

    branch = meta.get("default_branch") or "main"
    info["default_branch"] = branch

    topics, _ = get(f"/repos/{repo}/topics", token)
    info["topics"] = (topics or {}).get("names", []) if isinstance(topics, dict) else []

    langs, _ = get(f"/repos/{repo}/languages", token)
    info["languages"] = langs if isinstance(langs, dict) else {}

    branches = paged(f"/repos/{repo}/branches", token)
    info["branches"] = [{"name": b.get("name"), "sha": (b.get("commit") or {}).get("sha", "")[:7]}
                        for b in branches]

    tags = paged(f"/repos/{repo}/tags", token)
    info["tags"] = [{"name": t.get("name"), "sha": (t.get("commit") or {}).get("sha", "")[:7]} for t in tags]

    releases = paged(f"/repos/{repo}/releases", token, per_page=10)
    info["releases"] = [{"tag": r.get("tag_name"), "name": r.get("name"), "published": r.get("published_at")}
                        for r in releases]

    commits = paged(f"/repos/{repo}/commits", token, per_page=30, max_pages=2)
    info["commits"] = [{
        "sha": c.get("sha", "")[:7],
        "message": (c.get("commit") or {}).get("message", "").split("\n")[0],
        "author": who((c.get("commit") or {}).get("author")) or who(c.get("author")),
        "date": (c.get("commit") or {}).get("author", {}).get("date"),
    } for c in commits]

    contribs = paged(f"/repos/{repo}/contributors", token)
    info["contributors"] = [{"login": who(c), "commits": c.get("contributions", 0)} for c in contribs]

    tree_data, _ = get(f"/repos/{repo}/git/trees/{branch}", token, {"recursive": "1"})
    blobs = [f for f in (tree_data.get("tree") or []) if f.get("type") == "blob"]
    info["tree"] = [{"path": f["path"], "size": f.get("size", 0)} for f in blobs]
    info["tree_truncated"] = bool(tree_data.get("truncated"))

    issues = paged(f"/repos/{repo}/issues", token, {"state": "open"})
    info["issues"] = [{
        "number": i.get("number"),
        "title": i.get("title"),
        "author": who(i.get("user")),
        "created": i.get("created_at"),
        "labels": [l.get("name") for l in (i.get("labels") or [])],
        "is_pr": "pull_request" in i,
    } for i in issues]

    pulls = paged(f"/repos/{repo}/pulls", token, {"state": "open"})
    info["pulls"] = [{
        "number": p.get("number"),
        "title": p.get("title"),
        "author": who(p.get("user")),
        "created": p.get("created_at"),
        "base": (p.get("base") or {}).get("ref"),
        "head": (p.get("head") or {}).get("ref"),
    } for p in pulls]

    views, okv = get(f"/repos/{repo}/traffic/views", token)
    info["traffic_views"] = views if okv else None
    clones, okc = get(f"/repos/{repo}/traffic/clones", token)
    info["traffic_clones"] = clones if okc else None

    info["stack_signals"] = guess_stack(tree_data.get("tree") or [])
    return info


# --------------------------------------------------------------------------- #
# render
# --------------------------------------------------------------------------- #
def render_md(info: dict) -> str:
    m = info["meta"]
    L: list[str] = []
    a = L.append

    a(f"# Repo report — `{info['repo']}`")
    a("")
    a(f"> Generated by AI3 (`tools/ai3_repo_info.py`) on **{info['generated_at_utc']}**.  ")
    a("> This file is **generated** — do not hand-edit. Re-run the tool to refresh.")
    a("")
    a(f"**Spelling:** `wakil` (never `wakil`).")
    a("")

    a("## 1. Snapshot")
    a("")
    a("| Field | Value |")
    a("|-------|-------|")
    a(f"| Full name | `{m.get('full_name')}` |")
    a(f"| URL | {m.get('html_url')} |")
    a(f"| Clone | `{m.get('clone_url')}` |")
    a(f"| Visibility | {'private' if m.get('private') else 'public'} |")
    a(f"| Default branch | `{m.get('default_branch')}` |")
    a(f"| Description | {m.get('description') or '—'} |")
    a(f"| Homepage | {m.get('homepage') or '—'} |")
    a(f"| Primary language | {m.get('language') or '—'} |")
    a(f"| Topics | {', '.join(info['topics']) or '—'} |")
    a(f"| Created | {iso(m.get('created_at'))} ({ago(m.get('created_at'))}) |")
    a(f"| Last push | {iso(m.get('pushed_at'))} ({ago(m.get('pushed_at'))}) |")
    a(f"| Size | {human(m.get('size', 0) * 1024)} |")
    a(f"| Stars / Forks / Watchers | {m.get('stargazers_count', 0)} / {m.get('forks_count', 0)} / {m.get('subscribers_count', 0)} |")
    a(f"| Open issues (incl. PRs) | {m.get('open_issues_count', 0)} |")
    lic = m.get("license") or {}
    a(f"| License | {lic.get('spdx_id') or '—'} |")
    a(f"| Features | issues={'yes' if m.get('has_issues') else 'no'}, wiki={'yes' if m.get('has_wiki') else 'no'}, projects={'yes' if m.get('has_projects') else 'no'}, discussions={'yes' if m.get('has_discussions') else 'no'} |")
    a("")

    if info["stack_signals"]:
        a("**Detected stack signals:** " + ", ".join(f"`{s}`" for s in info["stack_signals"]))
        a("")

    if info["languages"]:
        total = sum(info["languages"].values()) or 1
        a("## 2. Languages")
        a("")
        a("| Language | Bytes | Share |")
        a("|----------|-------|-------|")
        for lang, b in sorted(info["languages"].items(), key=lambda kv: -kv[1]):
            a(f"| {lang} | {human(b)} | {b / total * 100:.1f}% |")
        a("")

    a("## 3. Branches, tags, releases")
    a("")
    a(f"**Branches ({len(info['branches'])}):** "
      + (", ".join(f"`{b['name']}`" for b in info["branches"]) or "—"))
    a("")
    a(f"**Tags ({len(info['tags'])}):** "
      + (", ".join(f"`{t['name']}`" for t in info["tags"]) or "—"))
    a("")
    if info["releases"]:
        a("| Release | Published |")
        a("|---------|-----------|")
        for r in info["releases"][:10]:
            a(f"| {r['tag']} — {r['name'] or ''} | {iso(r['published'])} |")
    else:
        a("**Releases:** none yet.")
    a("")

    a("## 4. Recent commits")
    a("")
    if info["commits"]:
        a("| SHA | Date | Author | Message |")
        a("|-----|------|--------|---------|")
        for c in info["commits"]:
            msg = c["message"].replace("|", "\\|")
            a(f"| `{c['sha']}` | {iso(c['date'])[:16]} | {c['author']} | {msg[:90]} |")
    else:
        a("_No commits yet._")
    a("")

    if info["contributors"]:
        a("## 5. Contributors")
        a("")
        a("| User | Commits |")
        a("|------|---------|")
        for c in info["contributors"]:
            a(f"| {c['login']} | {c['commits']} |")
        a("")

    a("## 6. Open issues & pull requests")
    a("")
    prs_only = [i for i in info["issues"] if i["is_pr"]]
    iss_only = [i for i in info["issues"] if not i["is_pr"]]
    if iss_only:
        a("| # | Title | Author | Created | Labels |")
        a("|---|-------|--------|---------|--------|")
        for i in iss_only:
            a(f"| {i['number']} | {i['title']} | {i['author']} | {iso(i['created'])[:10]} | "
              f"{', '.join(i['labels']) or '—'} |")
    else:
        a("**Issues:** none open.")
    a("")
    if info["pulls"]:
        a("| PR | Title | Author | head → base | Created |")
        a("|----|-------|--------|-------------|---------|")
        for p in info["pulls"]:
            a(f"| #{p['number']} | {p['title']} | {p['author']} | `{p['head']}` → `{p['base']}` | {iso(p['created'])[:10]} |")
    else:
        a("**Pull requests:** none open.")
    a("")

    a("## 7. File map")
    a("")
    files = info["tree"]
    if not files:
        a("_Empty tree._")
    else:
        by_dir: dict[str, list[dict]] = {}
        for f in files:
            parts = f["path"].split("/")
            key = "/".join(parts[:-1]) or "(root)"
            by_dir.setdefault(key, []).append(f)
        a(f"**{len(files)} files** across **{len(by_dir)} directories**"
          + (" — *(tree listing truncated by API)*" if info["tree_truncated"] else "") + ".")
        a("")
        a("```")
        for d in sorted(by_dir, key=lambda k: (k != "(root)", k)):
            a(f"{d}/")
            for f in sorted(by_dir[d], key=lambda x: x["path"]):
                a(f"    {f['path'].rsplit('/', 1)[-1]}  ({human(f['size'])})")
        a("```")
    a("")

    tv, tc = info.get("traffic_views"), info.get("traffic_clones")
    if tv or tc:
        a("## 8. Traffic (last 14 days)")
        a("")
        if tv:
            a(f"- Views: **{tv.get('count', 0)}** total, **{tv.get('uniques', 0)}** unique")
        if tc:
            a(f"- Clones: **{tc.get('count', 0)}** total, **{tc.get('uniques', 0)}** unique")
        a("")

    a("---")
    a("")
    a("_Regenerate:_ `export GITHUB_TOKEN=... && python3 tools/ai3_repo_info.py`")
    a("")
    return "\n".join(L)


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="AI3 repo-intelligence scanner")
    ap.add_argument("--repo", default=os.environ.get("WAKIL_REPO", DEFAULT_REPO),
                    help=f"owner/name (default: {DEFAULT_REPO})")
    ap.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"), help="GitHub PAT (or $GITHUB_TOKEN)")
    ap.add_argument("--out-dir", default="reports", help="output directory (default: reports)")
    ap.add_argument("--json-only", action="store_true", help="skip the markdown report")
    args = ap.parse_args(argv)

    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo):
        print(f"[ai3] bad --repo value: {args.repo!r} (expected owner/name)", file=sys.stderr)
        return 1

    print(f"[ai3] scanning {args.repo} ...")
    info = collect(args.repo, args.token)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    jpath = out / "repo-info.json"
    jpath.write_text(json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[ai3] wrote {jpath}")

    if not args.json_only:
        mpath = out / "repo-info.md"
        mpath.write_text(render_md(info), encoding="utf-8")
        print(f"[ai3] wrote {mpath}")

    print(f"[ai3] done — {len(info['tree'])} files, {len(info['commits'])} commits, "
          f"{len(info['branches'])} branches, {len([i for i in info['issues'] if not i['is_pr']])} open issues.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
