#!/usr/bin/env python3
"""State of the Union data builder for the week-sotu routine (see agent/prompts/SOTU.md).

Deterministic: gathers open work and routine health into one JSON file plus a
Markdown summary, so the routine only has to add a short "focus" note instead of
hand-writing a report. Standard library only.

Sources, in order:
  1. vigil MCP `get_open_tasks` when VIGIL_MCP_KEY is set (one HTTP call).
  2. Otherwise each tracked repo's TASKS.md (root or docs/), read from the
     local clone's origin default branch, parsed with vigil's rules.
  3. Open rows in agent/reports/findings-ledger.md.
  4. Optional --routines JSON written by the routine (routine health + quota).

Usage:
  python agent/scripts/sotu.py [--routines path.json] [--no-vigil]
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
VIGIL_URL = os.environ.get("VIGIL_MCP_URL", "https://ghoverseer.netlify.app/api/mcp")

# Display grouping only. Repos not listed land in tier III.
TIERS = {
    "I": ["vigil", "fire", "skyview", "ats-fill", "agent-board"],
    "II": ["darkmoon", "bb-mcp", "nitsuah-io", "avatar", "deployer", "kryptos"],
}
PRIO_RANK = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, None: 4}
HUMAN_OWNER = re.compile(r"\b(you|austin|human|manual|owner)\b", re.I)
PARKED = re.compile(r"(20\d\d)[- ]Q[1-4]|\bdeferred\b", re.I)
GIT_TIMEOUT = 60
# Portfolio initiatives: work that applies across repos (often filed in stash, e.g. "diagrams and
# screenshots for app repos"). They are weighted against single-app items in the kickoff queue.
INITIATIVE = re.compile(r"\b(every|each|all|app|tracked) repos?\b|cross-repo|portfolio|best practice|"
                        r"README|agent PR|TASKS\.md everywhere|routines?\b|PMO|DAILY|TIRE|CI-generated", re.I)
# Initiatives that act on other routines' output (reports, ledger, notes, runs) are candidates for a routine.
ROUTINE_CANDIDATE = re.compile(r"\b(routines?|DAILY|PMO|TIRE|audit|report|ledger|generator|runs?|checks?|lists?|reads?)\b", re.I)
PRIO_SCORE = {"P0": 100, "P1": 60, "P2": 30, "P3": 10, None: 5}


def tier_of(repo: str) -> str:
    for tier, names in TIERS.items():
        if repo in names:
            return tier
    return "III"


def tracked_repos() -> list[dict]:
    """Rows of scope.md's '## Tracked' table: name, local path, owner/repo."""
    repos, in_table = [], False
    for line in SCOPE.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_table = line.strip() == "## Tracked (active audit/automation scope)"
            continue
        if not in_table or not line.startswith("| ") or line.startswith("| Repo") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        path = re.search(r"`([^`]+)`", cells[1])
        url = re.search(r"https://github\.com/([\w.-]+/[\w.-]+)", cells[2])
        if path and url:
            private = len(cells) > 4 and "private" in cells[4].lower()
            repos.append({"repo": cells[0], "path": path.group(1), "full_name": url.group(1), "private": private})
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
        sub = re.match(r"^\s+- (Priority|Owner|Assignee|Acceptance Criteria):\s*(.*)", line)
        if current and sub:
            key, val = sub.group(1), sub.group(2).strip()
            if key == "Priority":
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
        out.append({"repo": repo, "title": t["title"], "ref": t.get("section") or "TASKS.md",
                    "priority": t.get("priority"), "status": t.get("status"),
                    "owner": t.get("owner"), "section": t.get("section"), "criteria": None})
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
        items.append({"id": c[0], "first_seen": c[1], "seen": int(c[3] or 1), "repo": c[5],
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
        re.search(r"\b(every|all|each) repos?\b", t["title"], re.I))
    t["initiative"] = initiative
    t["routine_candidate"] = initiative and bool(ROUTINE_CANDIDATE.search(t["title"]))
    # Initiatives reach every tracked repo, so they get 1.5x; single-app items keep their own priority
    # weight, plus a small bump for tier I apps. A P1 app item still outranks a P2 initiative.
    score = PRIO_SCORE.get(t["priority"], 5) * (1.5 if initiative else 1.0)
    if not initiative and tier_of(t["repo"]) == "I":
        score += 5
    t["score"] = round(score, 1)
    return t


def public_view(t: dict, private: set[str]) -> dict:
    """stash is public: private repos keep title, ref and priority only."""
    if t["repo"] not in private:
        return t
    return {**t, "criteria": None, "owner": None, "section": None}


def build(routines_path: str | None, use_vigil: bool, fetch: bool = True) -> dict:
    repos = tracked_repos()
    by_name = {r["repo"]: r for r in repos}
    private = {r["repo"] for r in repos if r["private"]}
    stale = fetch_all(repos) if fetch else []
    tasks = vigil_tasks(repos) if use_vigil else None
    source, missing = ("vigil", [])
    if tasks is None:
        tasks, missing = local_tasks(repos)
        source = "local TASKS.md"
    tasks = [classify(public_view(t, private)) for t in tasks]
    tasks.sort(key=lambda t: (PRIO_RANK.get(t["priority"], 4), t["status"] != "in-progress", t["repo"]))
    ledger = ledger_items()

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
    routines = json.loads(Path(routines_path).read_text(encoding="utf-8")) if routines_path else {}
    return {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
        "source": source, "missing_tasks_file": missing, "stale_refs": stale,
        "counts": {p or "none": sum(1 for t in tasks if t["priority"] == p) for p in ("P0", "P1", "P2", "P3", None)},
        "needs_you": needs_you, "kickoff": kickoff, "aging": aging, "initiatives": initiatives,
        "tasks": [dict(tier=tier_of(t["repo"]), **t) for t in tasks],
        "ledger_open": ledger,
        "routines": routines.get("routines", []), "quota": routines.get("quota"),
    }


def to_markdown(d: dict, week: str) -> str:
    L = [f"---\nkind: sotu\nweek: {week}\n---\n", f"# State of the Union — {week}\n",
         f"Generated {d['generated_at']} from {d['source']}. "
         f"Open tasks: " + ", ".join(f"{k} {v}" for k, v in d["counts"].items()) + ".\n",
         "<!-- focus -->\n"]
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
    if d.get("stale_refs"):
        L.append(f"\nFetch failed, tasks may be stale: {', '.join(d['stale_refs'])}.")
    if d["missing_tasks_file"]:
        L.append(f"\nNo TASKS.md found: {', '.join(d['missing_tasks_file'])}.")
    return "\n".join(L) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--routines", help="JSON with {routines: [...], quota: {...}} written by the routine")
    ap.add_argument("--no-vigil", action="store_true", help="skip vigil even if VIGIL_MCP_KEY is set")
    ap.add_argument("--no-fetch", action="store_true", help="don't git fetch the tracked repos first")
    args = ap.parse_args()
    data = build(args.routines, not args.no_vigil, not args.no_fetch)
    data["tasks"].sort(key=lambda t: (t["tier"], t["repo"], PRIO_RANK.get(t["priority"], 4)))
    y, w, _ = dt.date.today().isocalendar()
    week = f"{y}-W{w:02d}"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "sotu-data.json").write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    (OUT_DIR / f"sotu-{week}.md").write_text(to_markdown(data, week), encoding="utf-8")
    print(f"sotu: {len(data['tasks'])} tasks ({data['source']}), {len(data['needs_you'])} need you, "
          f"{len(data['kickoff'])} kickoff, {len(data['aging'])} aging -> agent/reports/sotu/sotu-{week}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
