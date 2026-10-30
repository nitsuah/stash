#!/usr/bin/env python3
"""State of the Union data builder for the week-sotu routine (see agent/prompts/SOTU.md).

Deterministic: gathers open work and routine health into one JSON file plus a
Markdown summary, so the routine only has to add a short "focus" note instead of
hand-writing a report. Standard library only.

Scope: tier 1 and 2 repos only. Tiers come from vigil's live `repos[].tier`
(GET /api/context) when VIGIL_MCP_KEY is set, else from scope.md's Tier column;
disagreements are reported as drift so scope.md can be corrected.

Sources, in order:
  1. Each in-scope repo's TASKS.md (root or docs/), read from the local clone's
     origin default branch right after a fetch, parsed with vigil's rules. This is
     the default because vigil's task cache lags same-day merges by hours.
  2. vigil MCP `get_open_tasks` instead, only with --vigil-tasks.
  3. Open rows in agent/reports/findings-ledger.md.
  4. Routine health: by default (`--routines auto`) built here from the local scheduled-task
     SKILL.md files, `gh run list` for the obn-health and repo-health workflows, and the open
     `bot:repo-health` issue count per repo. Anything it can't determine is "unknown", never
     guessed. `--routines path.json` still takes a routine-written JSON (e.g. to add quota);
     `--routines none` skips routine health.

Also: a `delta` block against the previous sotu-data.json (new / closed / moved items), and
with --verify-hints a sidecar sotu-verify.json of merged-PR and path evidence per item.

Usage:
  python agent/scripts/sotu.py [--routines auto|none|path.json] [--verify-hints] [--no-vigil]
                               [--vigil-tasks] [--all-tiers]
Writes agent/reports/sotu/sotu-data.json and agent/reports/sotu/sotu-<YYYY>-W<ww>.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

STASH = Path(__file__).resolve().parents[2]
SCOPE = STASH / "agent" / "projects" / "scope.md"
LEDGER = STASH / "agent" / "reports" / "findings-ledger.md"
OUT_DIR = STASH / "agent" / "reports" / "sotu"
VIGIL_URL = os.environ.get("VIGIL_MCP_URL", "https://gh-vigil.netlify.app/api/mcp")
VIGIL_CONTEXT_URL = os.environ.get("VIGIL_CONTEXT_URL", "https://gh-vigil.netlify.app/api/context")

# SOTU covers vigil tiers 1 and 2 only (T1 Critical, T2 Important). "-" = not registered in vigil.
SCOPE_TIERS = {"1", "2"}
PRIO_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, None: 4}
HUMAN_OWNER = re.compile(r"\b(you|austin|human|manual|owner)\b", re.IGNORECASE)
PARKED = re.compile(r"(20\d\d)[- ]Q[1-4]|\bdeferred\b|\bon hold\b|\bblocked\b", re.IGNORECASE)
GIT_TIMEOUT = 60
# Portfolio initiatives: work that applies across repos (often filed in stash, e.g. "diagrams and
# screenshots for app repos"). They are weighted against single-app items in the kickoff queue.
INITIATIVE = re.compile(r"\b(every|each|all|app|tracked) repos?\b|cross-repo|portfolio|best practice|"
                        r"README|agent PR|TASKS\.md everywhere|routines?\b|PMO|DAILY|TIRE|CI-generated", re.IGNORECASE)
# Initiatives that act on other routines' output (reports, ledger, notes, runs) are candidates for a routine.
ROUTINE_CANDIDATE = re.compile(r"\b(routines?|DAILY|PMO|TIRE|audit|report|ledger|generator|runs?|checks?|lists?|reads?)\b", re.IGNORECASE)
PRIO_SCORE = {"P0": 100, "P1": 60, "P2": 30, "P3": 10, None: 5}


def norm_tier(raw: str | None) -> str:
    """'T1' / 'Tier 1' / '1' -> '1'; anything else (unregistered, '—') -> '-'."""
    m = re.search(r"([1-4])", raw or "")
    return m.group(1) if m else "-"


def vigil_tiers() -> dict[str, str] | None:
    """Live tiers from vigil's /api/context, keyed by repo name. None when vigil can't be read."""
    key = os.environ.get("VIGIL_MCP_KEY")
    if not key or not VIGIL_CONTEXT_URL.startswith("https://"):
        return None
    req = urllib.request.Request(VIGIL_CONTEXT_URL, headers={"Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            ctx = json.load(resp)
    except Exception as exc:  # fall back to scope.md, but say why
        print(f"vigil tiers unavailable ({exc}); using scope.md's Tier column", file=sys.stderr)
        return None
    return {r["name"]: norm_tier(r.get("tier")) for r in ctx.get("repos", []) if r.get("name")}


def apply_tiers(repos: list[dict], live: dict[str, str] | None) -> list[dict]:
    """Set each repo's tier (vigil wins over scope.md) and return the rows where scope.md disagrees."""
    drift = []
    for r in repos:
        if live is None:
            r["tier"] = r["scope_tier"]
            continue
        r["tier"] = live.get(r["repo"], "-")
        if r["tier"] != r["scope_tier"]:
            drift.append({"repo": r["repo"], "vigil": r["tier"], "scope_md": r["scope_tier"]})
    return drift


def tracked_repos() -> list[dict]:
    """Rows of scope.md's '## Tracked' table: name, local path, owner/repo."""
    # Columns are found by header name, so adding or reordering a column (the Tier
    # column, 2026-10-15) can't silently empty the list.
    repos, in_table, col = [], False, {}
    for line in SCOPE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_table = line.strip() == "## Tracked (active audit/automation scope)"
            continue
        if not in_table or not line.startswith("| ") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[0] == "Repo":
            col = {name.lower(): i for i, name in enumerate(cells)}
            continue
        if not col:
            continue
        def cell(name: str, cells: list[str] = cells) -> str:
            i = col.get(name)
            return cells[i] if i is not None and i < len(cells) else ""

        path = re.search(r"`([^`]+)`", cell("local path"))
        url = re.search(r"https://github\.com/([\w.-]+/[\w.-]+)", cell("github url"))
        if path and url:
            private = "private" in cell("visibility").lower()
            repos.append({"repo": cells[0], "path": path.group(1), "full_name": url.group(1), "private": private,
                          "scope_tier": norm_tier(cell("tier"))})
    if not repos:
        raise SystemExit(f"tracked_repos: no rows parsed from {SCOPE} (heading or column names changed?)")
    return repos


def git(path: str, *args: str) -> str:
    """Run git with a timeout. Paths come from scope.md (a trusted, version-controlled file)."""
    return subprocess.run(["git", "-C", path, *args], capture_output=True, text=True,
                          encoding="utf-8", check=True, timeout=GIT_TIMEOUT).stdout


def fetch_all(repos: list[dict]) -> list[str]:
    """Refresh origin refs so the report isn't built from stale clones. Returns repos whose fetch failed."""
    stale = []
    for r in repos:
        try:
            git(r["path"], "fetch", "-q", "origin")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as exc:
            print(f"fetch failed for {r['repo']} ({type(exc).__name__}); its tasks may be stale", file=sys.stderr)
            stale.append(r["repo"])
    return stale


def git_show(path: str, rel: str) -> str | None:
    for ref in ("origin/HEAD", "origin/main", "origin/master", "HEAD"):
        try:
            return git(path, "show", f"{ref}:{rel}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
        except subprocess.TimeoutExpired:
            print(f"git show timed out in {path}", file=sys.stderr)
            return None
    return None


def parse_tasks(text: str, repo: str, rel: str) -> list[dict]:
    """vigil's rules: sub-bullet Priority > inline tag > heading; [/] or 'In Progress' = in-progress."""
    tasks, heading_prio, section, current = [], None, None, None
    for n, line in enumerate(text.splitlines(), 1):
        h = re.match(r"^(#{2,4})\s+(.*)", line)
        if h:
            section = h.group(2).strip()
            m = re.search(r"\bP([0-3])\b", section)
            heading_prio = f"P{m.group(1)}" if m else (None if h.group(1) == "##" else heading_prio)
            current = None
            continue
        item = re.match(r"^(\s*)- \[( |/)\]\s+(.*)", line)
        if item and len(item.group(1)) <= 1:
            full = item.group(3).replace("**", "").strip()
            title = full if len(full) <= 160 else full[:157] + "..."
            inline = re.search(r"[\[(]P([0-3])\b", title)
            current = {
                "repo": repo, "title": title, "ref": f"{rel}:{n}",
                "priority": f"P{inline.group(1)}" if inline else heading_prio,
                "status": "in-progress" if item.group(2) == "/" or (section or "").lower().startswith("in progress") else "todo",
                "owner": None, "section": section, "criteria": None,
                "parked": bool(PARKED.search(full)),
            }
            tasks.append(current)
            continue
        sub = re.match(r"^\s+- (Priority|Owner|Assignee|Acceptance Criteria|Status|Blocker|Blocked on):\s*(.*)", line)
        if current and sub:
            key, val = sub.group(1), sub.group(2).strip()
            if key in ("Status", "Blocker", "Blocked on"):
                # "Status: on hold ..." / "Blocked on: ..." parks the item (kept out of the kickoff queue)
                current["parked"] = current["parked"] or key != "Status" or bool(PARKED.search(val))
            elif key == "Priority":
                m = re.search(r"P([0-3])", val)
                current["priority"] = f"P{m.group(1)}" if m else current["priority"]
            elif key in ("Owner", "Assignee"):
                current["owner"] = val
            else:
                current["criteria"] = val[:300]
        elif line.strip() and not line.startswith(" "):
            current = None
    return tasks


def local_tasks(repos: list[dict]) -> tuple[list[dict], list[str]]:
    tasks, missing = [], []
    for r in repos:
        text = rel = None
        for candidate in ("TASKS.md", "docs/TASKS.md"):
            text = git_show(r["path"], candidate)
            if text:
                rel = candidate
                break
        if not text:
            missing.append(r["repo"])
            continue
        tasks += parse_tasks(text, r["repo"], rel)
    return tasks, missing


def vigil_tasks(repos: list[dict]) -> list[dict] | None:
    key = os.environ.get("VIGIL_MCP_KEY")
    if not key:
        return None
    if not VIGIL_URL.startswith("https://"):
        print("VIGIL_MCP_URL must be https; not sending the key. Using local TASKS.md", file=sys.stderr)
        return None
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": "get_open_tasks", "arguments": {"limit": 500}}}).encode()
    req = urllib.request.Request(VIGIL_URL, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
        rollup = json.loads(payload["result"]["content"][0]["text"])
    except Exception as exc:  # fall back to local parsing, but say why
        print(f"vigil unavailable ({exc}); using local TASKS.md", file=sys.stderr)
        return None
    names = {r["full_name"].lower(): r["repo"] for r in repos}
    out = []
    for t in rollup.get("tasks", []):
        repo = names.get((t.get("full_name") or "").lower(), t.get("repo"))
        out.append({"repo": repo, "title": t["title"].replace("**", ""), "ref": "TASKS.md",
                    "priority": t.get("priority"), "status": t.get("status"),
                    "owner": t.get("owner"), "section": t.get("section"), "criteria": None,
                    # vigil's rollup has no sub-bullets, so honor its own flag and the title/status text
                    "parked": bool(t.get("parked")) or bool(PARKED.search(f"{t['title']} {t.get('status') or ''}"))})
    return out


def ledger_items() -> list[dict]:
    items = []
    if not LEDGER.exists():
        return items
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| F-"):
            continue
        c = [x.strip() for x in line.strip("|").split("|")]
        if len(c) < 10 or c[8] not in ("open", "pr-open", "blocked"):
            continue
        items.append({"id": c[0], "first_seen": c[1], "seen": int(c[3]) if c[3].isdigit() else 1, "repo": c[5],
                      "finding": c[6], "class": c[7], "status": c[8], "link": c[9]})
    return items


def kickoff_prompt(t: dict, repos: dict) -> str:
    path = repos.get(t["repo"], {}).get("path", t["repo"])
    crit = f" Acceptance criteria: {t['criteria']}" if t.get("criteria") else ""
    return (f"Kick off {t['repo']} ({path}): \"{t['title']}\" ({t['ref']}, {t['priority'] or 'unprioritized'}). "
            f"Read the item and its sub-bullets in TASKS.md, confirm scope with me in 3 bullets, then work on a "
            f"feature branch with a PR; run tests in Docker.{crit}")


def classify(t: dict) -> dict:
    text = f"{t['title']} {t.get('section') or ''}"
    initiative = (t["repo"] == "stash" and bool(INITIATIVE.search(text))) or bool(
        re.search(r"\b(every|all|each) repos?\b", t["title"], re.IGNORECASE))
    t["initiative"] = initiative
    t["routine_candidate"] = initiative and bool(ROUTINE_CANDIDATE.search(t["title"]))
    # Initiatives reach every tracked repo, so they get 1.5x; single-app items keep their own priority
    # weight, plus a small bump for tier 1 apps. A P1 app item still outranks a P2 initiative.
    score = PRIO_SCORE.get(t["priority"], 5) * (1.5 if initiative else 1.0)
    if not initiative and t.get("tier") == "1":
        score += 5
    t["score"] = round(score, 1)
    return t


def public_view(t: dict, private: set[str]) -> dict:
    """stash is public: private repos keep title, ref and priority only."""
    if t["repo"] not in private:
        return t
    # ref keeps only a file:line locator; anything else (e.g. a section name) is dropped.
    ref = t.get("ref") or ""
    safe_ref = ref if re.fullmatch(r"(docs/)?TASKS\.md(:\d+)?", ref) else "TASKS.md"
    return {**t, "ref": safe_ref, "criteria": None, "owner": None, "section": None}


# ---- routine health (auto), delta and verify hints --------------------------------------------
LOCAL_TASKS_DIR = Path(os.environ.get("SOTU_TASKS_DIR", Path.home() / ".claude" / "scheduled-tasks"))
HEALTH_OWNERS = ("nitsuah", "Nitsuah-Labs")
HEALTH_WORKFLOWS = (("obn-health", "obn-health.yml"), ("repo-health", "repo-health.yml"))
GH_REPO = "nitsuah/stash"
GH_TIMEOUT = 60
STOPWORDS = {"about", "after", "again", "also", "build", "check", "every", "first", "from", "into", "item",
             "make", "move", "needs", "other", "should", "some", "than", "that", "their", "them", "then",
             "there", "these", "this", "update", "using", "when", "which", "with", "work", "write"}


def run_gh(args: list[str]) -> tuple[int, str, str]:
    """Run `gh`; returns (returncode, stdout, stderr). returncode -1 when gh is missing or times out."""
    try:
        p = subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", timeout=GH_TIMEOUT)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return -1, "", "gh unavailable"
    return p.returncode, p.stdout, p.stderr


def gh_json(args: list[str]):
    """Parsed JSON from `gh`, or None when the call fails (callers then report 'unknown')."""
    rc, out, _ = run_gh(args)
    if rc != 0:
        return None
    try:
        return json.loads(out)
    except ValueError:
        return None


def local_task_rows(tasks_dir: Path | None = None) -> list[dict]:
    """One row per local scheduled task from SKILL.md frontmatter. Run state isn't on disk: it stays unknown."""
    d = tasks_dir or LOCAL_TASKS_DIR
    rows = []
    if not d.is_dir():
        return rows
    for skill in sorted(d.glob("*/SKILL.md")):
        if skill.parent.name.startswith("_"):
            continue
        m = re.match(r"---\s*\n(.*?)\n---", skill.read_text(encoding="utf-8", errors="replace"), re.DOTALL)
        name = None
        if m:
            nm = re.search(r"^name:\s*(.+?)\s*$", m.group(1), re.MULTILINE)
            name = nm.group(1).strip("'\"") if nm else None
        rows.append({"name": name or skill.parent.name, "last_run": "unknown", "status": "unknown",
                     "next_run": "unknown", "note": "local task; enabled and last run not readable from disk"})
    return rows


def actions_row(name: str, workflow: str, repo: str = GH_REPO) -> dict:
    runs = gh_json(["run", "list", "-R", repo, "--workflow", workflow, "--limit", "1",
                    "--json", "conclusion,status,createdAt"])
    if not runs:
        return {"name": name, "last_run": "unknown", "status": "unknown", "next_run": "unknown",
                "note": f"GitHub Actions {workflow}: no run data"}
    r = runs[0]
    conclusion = r.get("conclusion") or r.get("status") or "unknown"
    status = {"success": "succeeded", "failure": "failed", "in_progress": "running",
              "queued": "running"}.get(conclusion, conclusion)
    return {"name": name, "last_run": (r.get("createdAt") or "unknown")[:10], "status": status,
            "next_run": "unknown", "note": f"GitHub Actions {workflow}"}


def repo_health_counts(repos: list[str] | None = None) -> dict[str, int] | None:
    """Open bot:repo-health issues per repo name across the owners; None if any search failed."""
    counts: dict[str, int] = {}
    for owner in HEALTH_OWNERS:
        found = gh_json(["search", "issues", "--owner", owner, "--label", "bot:repo-health", "--state", "open",
                         "--json", "repository", "--limit", "200"])
        if found is None:
            return None
        for it in found:
            name = (it.get("repository") or {}).get("name") or "unknown"
            counts[name] = counts.get(name, 0) + 1
    for r in repos or []:
        counts.setdefault(r, 0)
    return counts


def auto_routines(repos: list[str] | None = None, tasks_dir: Path | None = None) -> dict:
    rows = local_task_rows(tasks_dir)
    rows += [actions_row(n, w) for n, w in HEALTH_WORKFLOWS]
    counts = repo_health_counts(repos)
    if counts is None:
        rows.append({"name": "repo-health issues", "last_run": "unknown", "status": "unknown", "next_run": "unknown",
                     "note": "gh search failed; open issue count unknown"})
    else:
        total = sum(counts.values())
        detail = ", ".join(f"{r} {n}" for r, n in sorted(counts.items()) if n) or "none open"
        rows.append({"name": "repo-health issues", "last_run": "unknown", "status": "issues" if total else "clean",
                     "next_run": "unknown", "note": f"{total} open: {detail}"})
    return {"routines": rows, "quota": None, "repo_health_issues": counts}


def _item_key(t: dict) -> str:
    return f"{t.get('repo')}|{t.get('title') or t.get('finding') or t.get('id')}"


def _brief(t: dict) -> dict:
    return {"repo": t.get("repo"), "title": t.get("title") or t.get("finding"), "priority": t.get("priority")}


def _diff(prev: list[dict], cur: list[dict], moved_fields: tuple[str, ...] = ()) -> dict:
    p = {_item_key(t): t for t in prev}
    c = {_item_key(t): t for t in cur}
    out = {"new": [_brief(c[k]) for k in c if k not in p], "closed": [_brief(p[k]) for k in p if k not in c]}
    if moved_fields:
        out["moved"] = [{**_brief(c[k]), "from": {f: p[k].get(f) for f in moved_fields},
                         "to": {f: c[k].get(f) for f in moved_fields}}
                        for k in c if k in p and any(p[k].get(f) != c[k].get(f) for f in moved_fields)]
    return out


def compute_delta(prev: dict | None, cur: dict) -> dict:
    """Changes against the previous run's JSON. `empty` is False when there is no baseline."""
    if not prev:
        return {"previous": None, "empty": False, "note": "no previous sotu-data.json"}
    d = {"previous": prev.get("generated_at"),
         "tasks": _diff(prev.get("tasks", []), cur.get("tasks", []), ("priority", "status")),
         "needs_you": _diff(prev.get("needs_you", []), cur.get("needs_you", [])),
         "kickoff": _diff(prev.get("kickoff", []), cur.get("kickoff", []))}
    d["empty"] = not any(d[s][k] for s in ("tasks", "needs_you", "kickoff") for k in d[s])
    return d


def delta_markdown(d: dict, cap: int = 8) -> list[str]:
    L = ["## Changes since last run\n"]
    if d.get("previous") is None:
        return L + ["- no previous run to compare\n"]
    if d["empty"]:
        return L + ["- nothing changed\n"]
    for section, label in (("needs_you", "Needs you"), ("kickoff", "Kickoff"), ("tasks", "Tasks")):
        for kind, items in d[section].items():
            if not items:
                continue
            shown = [f"{i['repo']}: {i['title']}" + (f" ({i['from']} -> {i['to']})" if kind == "moved" else "")
                     for i in items[:cap]]
            more = f" (+{len(items) - cap} more)" if len(items) > cap else ""
            L.append(f"- {label} {kind} ({len(items)}): " + "; ".join(shown) + more)
    return L + [""]


def _keywords(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z][a-z0-9-]{4,}", text.lower()) if w not in STOPWORDS}


def _backtick_paths(text: str) -> list[str]:
    out = []
    for tok in re.findall(r"`([^`\s]+)`", text or ""):
        if tok.startswith("./"):
            tok = tok[2:]
        if re.fullmatch(r"[\w.@-]+(/[\w.@-]+)+/?|[\w-]+\.[A-Za-z0-9]{1,5}", tok) and ".." not in tok and tok not in out:
            out.append(tok)
    return out


def _since(t: dict, today: dt.date) -> tuple[str, str]:
    m = re.search(r"20\d\d-\d\d-\d\d", f"{t.get('first_seen') or ''} {t.get('title') or ''}")
    if m:
        return m.group(0), "item"
    return (today - dt.timedelta(days=28)).isoformat(), "default-28d"


def verify_items(data: dict) -> list[dict]:
    """Needs-you, kickoff and open P0/P1 items, deduped by repo+title."""
    seen, items = set(), []
    pools = [("needs_you", data.get("needs_you", [])), ("kickoff", data.get("kickoff", [])),
             ("p0p1", [t for t in data.get("tasks", []) if t.get("priority") in ("P0", "P1")])]
    for kind, pool in pools:
        for t in pool:
            k = _item_key(t)
            if k not in seen:
                seen.add(k)
                items.append({**t, "_kind": kind})
    return items


def build_verify(data: dict, repos: dict[str, dict], today: dt.date | None = None, max_path_checks: int = 15) -> dict:
    """Evidence per item. One `gh pr list` per repo. Private repos expose PR numbers/dates only."""
    today = today or dt.date.today()
    items = verify_items(data)
    delta = data.get("delta") or {}
    changed = set()
    for sec in ("needs_you", "kickoff", "tasks"):
        for kind in ("new", "moved"):
            changed |= {f"{i['repo']}|{i['title']}" for i in (delta.get(sec) or {}).get(kind, [])}
    no_baseline = delta.get("previous") is None
    since = {_item_key(t): _since(t, today) for t in items}
    by_repo: dict[str, list[dict]] = {}
    for t in items:
        by_repo.setdefault(t["repo"], []).append(t)
    prs: dict[str, list[dict] | None] = {}
    for repo, its in by_repo.items():
        meta = repos.get(repo)
        if not meta:
            prs[repo] = None
            continue
        earliest = min(since[_item_key(t)][0] for t in its)
        prs[repo] = gh_json(["pr", "list", "-R", meta["full_name"], "--state", "merged", "--search",
                             f"merged:>={earliest}", "--json", "number,title,body,mergedAt", "--limit", "100"])
    checks_left = max_path_checks
    out = []
    for t in items:
        repo, meta = t["repo"], repos.get(t["repo"], {})
        key = _item_key(t)
        since_date, src = since[key]
        kws = _keywords(t.get("title") or t.get("finding") or "")
        need = 1 if len(kws) <= 2 else 2
        hints, lookup_failed = [], prs.get(repo) is None
        for pr in prs.get(repo) or []:
            if (pr.get("mergedAt") or "")[:10] < since_date:
                continue
            hit = _keywords(f"{pr.get('title') or ''} {pr.get('body') or ''}") & kws
            if len(hit) >= need:
                h = {"number": pr["number"], "mergedAt": pr.get("mergedAt"), "matched": sorted(hit)}
                if not meta.get("private"):
                    h["title"] = pr.get("title")
                hints.append(h)
        path_checks = []
        if not meta.get("private") and meta.get("full_name"):
            for path in _backtick_paths(f"{t.get('title') or ''} {t.get('criteria') or ''}")[:3]:
                if checks_left <= 0:
                    path_checks.append({"path": path, "exists": None})
                    continue
                checks_left -= 1
                rc, _, err = run_gh(["api", f"repos/{meta['full_name']}/contents/{path}", "--silent"])
                path_checks.append({"path": path, "exists": True if rc == 0 else (False if "404" in err else None)})
        is_changed = no_baseline or key in changed
        no_evidence = not hints and all(c["exists"] is None for c in path_checks)
        out.append({"key": key, "kind": t["_kind"], "repo": repo, "title": t.get("title") or t.get("finding"),
                    "priority": t.get("priority"), "since": since_date, "since_source": src,
                    "pr_hints": hints, "path_checks": path_checks, "lookup_failed": lookup_failed,
                    "changed": is_changed, "skip_model": bool(no_evidence and not is_changed and not lookup_failed)})
    return {"generated_at": data.get("generated_at"), "items": out,
            "all_skip": all(i["skip_model"] for i in out), "delta_empty": bool(delta.get("empty"))}


def build(routines_path: str | None, use_vigil: bool, fetch: bool = True, all_tiers: bool = False,
          vigil_task_source: bool = False) -> dict:
    all_repos = tracked_repos()
    live = vigil_tiers() if use_vigil else None
    drift = apply_tiers(all_repos, live)
    repos = all_repos if all_tiers else [r for r in all_repos if r["tier"] in SCOPE_TIERS]
    if not repos:
        raise SystemExit("build: no tier 1/2 repos in scope (vigil tiers unreadable and scope.md Tier column empty?)")
    in_scope = {r["repo"] for r in repos}
    out_of_scope = {r["repo"] for r in all_repos} - in_scope
    tier_by = {r["repo"]: r["tier"] for r in all_repos}
    by_name = {r["repo"]: r for r in repos}
    private = {r["repo"] for r in repos if r["private"]}
    stale = fetch_all(repos) if fetch else []
    tasks = vigil_tasks(repos) if use_vigil and vigil_task_source else None
    source, missing = ("vigil", [])
    if tasks is None:
        tasks, missing = local_tasks(repos)
        source = "local TASKS.md"
    else:
        # vigil doesn't index every tracked repo; fill the gaps from TASKS.md so none silently drop out.
        covered = {t["repo"] for t in tasks}
        gaps = [r for r in repos if r["repo"] not in covered]
        if gaps:
            extra, missing = local_tasks(gaps)
            tasks += extra
            filled = sorted({t["repo"] for t in extra})
            if filled:
                source = f"vigil + local TASKS.md ({', '.join(filled)})"
    tasks = [classify({**public_view(t, private), "tier": tier_by.get(t["repo"], "-")})
             for t in tasks if t["repo"] in in_scope]
    tasks.sort(key=lambda t: (PRIO_RANK.get(t["priority"], 4), t["status"] != "in-progress", t["repo"]))
    # Ledger rows for out-of-scope repos drop out; cross-cutting rows (e.g. "cloud routines") stay.
    ledger = [i for i in ledger_items() if i["repo"] not in out_of_scope]

    needs_you = [dict(kind="task", **t) for t in tasks
                 if (t.get("owner") and HUMAN_OWNER.search(t["owner"])) or t["title"].lower().startswith("manual step")]
    needs_you += [dict(kind="ledger", **i) for i in ledger if i["class"] == "human"]

    human_refs = {(i["repo"], i.get("ref")) for i in needs_you}
    kickoff, seen, n_init = [], set(), 0
    for t in sorted(tasks, key=lambda t: -t["score"]):
        if t["score"] < 30 or (t["repo"], t["ref"]) in human_refs or t.get("parked") or PARKED.search(t["title"]):
            continue
        # One app item per repo; up to 2 initiatives so cross-repo work competes without crowding out apps.
        if t["initiative"]:
            if n_init >= 2:
                continue
            n_init += 1
        elif t["repo"] in seen:
            continue
        seen.add(t["repo"])
        kickoff.append({**t, "prompt": kickoff_prompt(t, by_name)})
        if len(kickoff) == 5:
            break
    initiatives = [t for t in tasks if t["initiative"] and not t.get("parked")]

    today = dt.date.today()
    aging = [i for i in ledger if i["seen"] >= 3 or (today - dt.date.fromisoformat(i["first_seen"])).days > 21]
    if routines_path == "auto":
        routines = auto_routines([r["repo"] for r in all_repos])
    elif routines_path and routines_path != "none":
        routines = json.loads(Path(routines_path).read_text(encoding="utf-8"))
    else:
        routines = {}
    prio_path = OUT_DIR / "priorities.json"  # curated top initiatives + WSJF top 5 (SOTU.md step 5)
    priorities = json.loads(prio_path.read_text(encoding="utf-8")) if prio_path.exists() else {}
    # Same rule as ledger rows: repo-specific entries for out-of-scope repos drop out of the
    # output (the source file is left for SOTU.md step 7); cross-cutting entries stay.
    for key in ("initiatives", "top5"):
        if isinstance(priorities.get(key), list):
            priorities[key] = [p for p in priorities[key] if p.get("repo") not in out_of_scope]
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
        "source": source, "missing_tasks_file": missing, "stale_refs": stale,
        "counts": {p or "none": sum(1 for t in tasks if t["priority"] == p) for p in ("P0", "P1", "P2", "P3", None)},
        "needs_you": needs_you, "kickoff": kickoff, "aging": aging, "initiatives": initiatives,
        "tasks": tasks,
        "scope": {"tiers": "all" if all_tiers else sorted(SCOPE_TIERS), "repos": sorted(in_scope),
                  "excluded": sorted(out_of_scope), "tier_source": "vigil" if live is not None else "scope.md"},
        "tier_drift": drift,
        "ledger_open": ledger,
        "routines": routines.get("routines", []), "quota": routines.get("quota"),
        "repo_health_issues": routines.get("repo_health_issues"),
        "priorities": priorities,
    }


def to_markdown(d: dict, week: str) -> str:
    L = [f"---\nkind: sotu\nweek: {week}\n---\n", f"# State of the Union — {week}\n",
         f"Generated {d['generated_at']} from {d['source']}. "
         f"Open tasks: " + ", ".join(f"{k} {v}" for k, v in d["counts"].items()) + ".\n",
         f"Scope: tier {', '.join(d['scope']['tiers']) if d['scope']['tiers'] != 'all' else 'all'} repos "
         f"per {d['scope']['tier_source']} ({', '.join(d['scope']['repos'])}). "
         f"Left out: {', '.join(d['scope']['excluded']) or 'none'}.\n",
         "<!-- focus -->\n"]
    if d.get("delta"):
        L += delta_markdown(d["delta"])
    if d.get("quota"):
        q = d["quota"]
        L.append(f"Quota: weekly {q.get('weekly')}%, 5-hour {q.get('five_hour')}% (resets {q.get('weekly_resets')}).\n")
    L.append("## Needs you\n")
    L += [f"- **{i['repo']}**: {i.get('title') or i.get('finding')} ({i.get('ref') or i.get('id')})" for i in d["needs_you"]] or ["- nothing"]
    L.append("\n## Kickoff queue\n")
    L += [f"{n}. **{t['repo']}** {t['priority']}{' (initiative)' if t['initiative'] else ''}: {t['title']} ({t['ref']})\n   > {t['prompt']}"
          for n, t in enumerate(d["kickoff"], 1)] or ["- nothing ready"]
    L.append("\n## Portfolio initiatives\n\nCross-repo work. A routine candidate acts on other routines' output.\n")
    L += [f"- {t['priority'] or '-'} {'[routine candidate] ' if t['routine_candidate'] else ''}{t['title']} ({t['repo']} {t['ref']})"
          for t in d["initiatives"]] or ["- none"]
    if d["routines"]:
        L.append("\n## Routine health\n\n| Routine | Last run | Status | Next |\n|---|---|---|---|")
        L += [f"| {r.get('name')} | {r.get('last_run', '')} | {r.get('status', '')} | {r.get('next_run', '')} |" for r in d["routines"]]
    L.append("\n## Findings aging (seen 3+ times or older than 21 days)\n")
    L += [f"- {i['id']} {i['repo']}: {i['finding']} ({i['class']}, {i['status']})" for i in d["aging"]] or ["- none"]
    L.append("\n## Open work by repo\n")
    repo = None
    low: dict[str, int] = {}
    for t in d["tasks"]:
        if t["priority"] in ("P3", None):
            low[t["repo"]] = low.get(t["repo"], 0) + 1
            continue
        if t["repo"] != repo:
            repo = t["repo"]
            L.append(f"\n### {repo} (tier {t['tier']})")
        L.append(f"- {t['priority']} {t['title']} ({t['ref']})")
    if low:
        L.append("\nP3 / unprioritized, counts only (full list in sotu-data.json): "
                 + ", ".join(f"{r} {n}" for r, n in sorted(low.items())) + ".")
    if d.get("tier_drift"):
        L.append("\nscope.md Tier column differs from vigil (update scope.md): "
                 + ", ".join(f"{x['repo']} vigil {x['vigil']} vs scope.md {x['scope_md']}" for x in d["tier_drift"]) + ".")
    if d.get("stale_refs"):
        L.append(f"\nFetch failed, tasks may be stale: {', '.join(d['stale_refs'])}.")
    if d["missing_tasks_file"]:
        L.append(f"\nNo TASKS.md found: {', '.join(d['missing_tasks_file'])}.")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--routines", default="auto",
                    help="'auto' (default): build routine health here; 'none': skip; or a JSON path with "
                         "{routines: [...], quota: {...}} written by the routine")
    ap.add_argument("--verify-hints", action="store_true",
                    help="also write sotu-verify.json: merged-PR and path evidence for Needs-you, kickoff, P0/P1 items")
    ap.add_argument("--no-vigil", action="store_true", help="skip vigil (tiers fall back to scope.md)")
    ap.add_argument("--vigil-tasks", action="store_true", help="read tasks from vigil's cache instead of TASKS.md")
    ap.add_argument("--no-fetch", action="store_true", help="don't git fetch the tracked repos first")
    ap.add_argument("--all-tiers", action="store_true", help="include tier 3/4 and unregistered repos")
    args = ap.parse_args()
    data = build(args.routines, not args.no_vigil, not args.no_fetch, args.all_tiers, args.vigil_tasks)
    prev_path = OUT_DIR / "sotu-data.json"
    try:
        prev = json.loads(prev_path.read_text(encoding="utf-8")) if prev_path.exists() else None
    except ValueError:
        prev = None
    data["delta"] = compute_delta(prev, data)
    data["tasks"].sort(key=lambda t: (t["tier"], t["repo"], PRIO_RANK.get(t["priority"], 4)))
    y, w, _ = dt.date.today().isocalendar()
    week = f"{y}-W{w:02d}"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "sotu-data.json").write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    (OUT_DIR / f"sotu-{week}.md").write_text(to_markdown(data, week), encoding="utf-8")
    if args.verify_hints:
        repos = {r["repo"]: r for r in tracked_repos()}
        verify = build_verify(data, repos)
        (OUT_DIR / "sotu-verify.json").write_text(json.dumps(verify, indent=1), encoding="utf-8")
        print(f"sotu: verify hints for {len(verify['items'])} items, "
              f"{sum(1 for i in verify['items'] if i['skip_model'])} skip_model, all_skip={verify['all_skip']}")
    print(f"sotu: {len(data['tasks'])} tasks ({data['source']}), {len(data['needs_you'])} need you, "
          f"{len(data['kickoff'])} kickoff, {len(data['aging'])} aging -> agent/reports/sotu/sotu-{week}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
