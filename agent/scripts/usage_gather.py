#!/usr/bin/env python3
"""USAGE pre-step: computes what USAGE.md sources 1-2 need without a model.

Writes `agent/reports/usage-data.json` for the reporting window (the previous completed calendar
month by default, `--month YYYY-MM` to pick another):

  scheduled_tasks  run stats per task from run records under ~/.claude/scheduled-tasks, or
                   `unavailable: <reason>` when no readable run records exist (never guessed)
  workflows        `gh run list` stats for stash's `obn-health` and each tracked repo's
                   `repo-health` workflow (per-repo errors become `unavailable: <reason>`)
  shipped          merged PR count (gh) and commit count (local clone, origin default branch) per
                   tracked repo

Claude session and quota numbers are not here: they only exist behind MCP tools, so the model
still reads those (USAGE.md source 1). stash is PUBLIC: counts and workflow names only.

Usage:
  python agent/scripts/usage_gather.py [--month YYYY-MM] [--tasks-dir DIR] [--today YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import sys
from collections import Counter
from pathlib import Path

import prestep_common as pc

OUT = pc.REPORTS / "usage-data.json"
STASH_FULL = "nitsuah/stash"
DEFAULT_TASKS_DIR = Path.home() / ".claude" / "scheduled-tasks"
DISPLAY_TASKS_DIR = "~/.claude/scheduled-tasks"
FAIL_STATES = {"failure", "failed", "error", "timed_out", "cancelled"}
OK_STATES = {"success", "succeeded", "completed", "ok"}


def window(month: str | None, today: dt.date) -> tuple[dt.date, dt.date]:
    """(first day, last day) of `month`, or of the last completed calendar month before today."""
    if month:
        year, mon = (int(x) for x in month.split("-"))
    else:
        first_this = today.replace(day=1)
        prev = first_this - dt.timedelta(days=1)
        year, mon = prev.year, prev.month
    return dt.date(year, mon, 1), dt.date(year, mon, calendar.monthrange(year, mon)[1])


def run_stats(conclusions: list[str]) -> dict:
    c = Counter((x or "unknown").lower() for x in conclusions)
    return {"runs": len(conclusions), "success": c.get("success", 0),
            "failure": c.get("failure", 0) + c.get("timed_out", 0),
            "cancelled": c.get("cancelled", 0),
            "other": len(conclusions) - c.get("success", 0) - c.get("failure", 0)
            - c.get("timed_out", 0) - c.get("cancelled", 0)}


def workflow_stats(full_name: str, workflow: str, start: dt.date, end: dt.date) -> dict:
    try:
        runs = pc.gh_json(["run", "list", "-R", full_name, "--workflow", workflow, "--created",
                           f"{start.isoformat()}..{end.isoformat()}", "--json",
                           "conclusion,status", "--limit", "200"])
    except pc.GhError as exc:
        return {"unavailable": str(exc)}
    # A run still in progress has no conclusion yet; report it as its status.
    return run_stats([r.get("conclusion") or r.get("status") or "unknown" for r in runs])


def shipped(repo: dict, start: dt.date, end: dt.date) -> dict:
    out: dict = {}
    try:
        prs = pc.gh_json(["pr", "list", "-R", repo["full_name"], "--state", "merged", "--search",
                          f"merged:{start.isoformat()}..{end.isoformat()}", "--json", "number",
                          "--limit", "500"])
        out["merged_prs"] = len(prs)
    except pc.GhError as exc:
        out["merged_prs"] = f"unavailable: {exc}"
    try:
        ref = next(r for r in ("origin/HEAD", "origin/main", "origin/master")
                   if pc.run_cmd(["git", "-C", repo["path"], "rev-parse", "--verify", "-q",
                                  r]).returncode == 0)
        out["commits"] = int(pc.git(repo["path"], "rev-list", "--count", f"--since={start}",
                                    f"--until={end} 23:59:59", ref).strip())
    except (StopIteration, pc.GhError, ValueError):
        out["commits"] = "unavailable: no readable origin branch in the local clone"
    return out


def read_records(path: Path) -> list[dict]:
    """Dict records from a .json (list or {runs: [...]}) or .jsonl file; [] if unreadable."""
    try:
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".jsonl":
            data = [json.loads(ln) for ln in text.splitlines() if ln.strip()]
        else:
            data = json.loads(text)
            data = data.get("runs", []) if isinstance(data, dict) else data
    except (OSError, ValueError):
        return []
    return [d for d in data if isinstance(d, dict)]


def record_day(rec: dict) -> dt.date | None:
    for key in ("started_at", "startedAt", "created_at", "createdAt"):
        val = rec.get(key)
        if isinstance(val, str):
            try:
                return dt.date.fromisoformat(val[:10])
            except ValueError:
                return None
    return None


def scheduled_task_stats(tasks_dir: Path, start: dt.date, end: dt.date) -> dict:
    """Per-task run stats from run records on disk, else `unavailable` with the reason."""
    if not tasks_dir.is_dir():
        return {"unavailable": f"{DISPLAY_TASKS_DIR} does not exist"}
    tasks: dict[str, dict] = {}
    seen_files = 0
    for task in sorted(p for p in tasks_dir.iterdir() if p.is_dir() and not p.name.startswith("_")):
        recs: list[dict] = []
        for f in sorted(task.rglob("*")):
            if f.is_file() and f.suffix in (".json", ".jsonl"):
                seen_files += 1
                recs += read_records(f)
        dated = [(record_day(r), r) for r in recs]
        window_recs = [r for d, r in dated if d and start <= d <= end]
        if not recs:
            continue
        states = [str(r.get("status") or r.get("state") or "unknown").lower() for r in window_recs]
        stats = run_stats(["success" if s in OK_STATES else "failure" if s in FAIL_STATES
                           else s for s in states])
        reasons = Counter(str(r.get("error"))[:80] for r in window_recs if r.get("error"))
        stats["top_failure_reason"] = reasons.most_common(1)[0][0] if reasons else None
        tasks[task.name] = stats
    if not tasks:
        return {"unavailable": f"no run records (.json/.jsonl) under {DISPLAY_TASKS_DIR}; "
                f"only task definitions are on disk, run history lives behind the "
                f"scheduled-tasks MCP list_task_runs (limit 50)"}
    return {"tasks": tasks, "record_files": seen_files}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--month", help="YYYY-MM (default: previous completed month)")
    ap.add_argument("--tasks-dir", default=str(DEFAULT_TASKS_DIR))
    ap.add_argument("--today", default=dt.date.today().isoformat())
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)

    start, end = window(a.month, dt.date.fromisoformat(a.today))
    repos = pc.tracked_repos()
    data = {
        "generated": a.today, "month": start.strftime("%Y-%m"),
        "window": {"from": start.isoformat(), "to": end.isoformat()},
        "partial_month": end >= dt.date.fromisoformat(a.today),
        "scheduled_tasks": scheduled_task_stats(Path(a.tasks_dir), start, end),
        "workflows": {"stash/obn-health": workflow_stats(STASH_FULL, "obn-health.yml", start, end),
                      **{f"{r['repo']}/repo-health": workflow_stats(
                          r["full_name"], "repo-health.yml", start, end) for r in repos}},
        "shipped": {r["repo"]: shipped(r, start, end) for r in repos},
    }
    pc.write_json(Path(a.out), data)
    wf_bad = sum("unavailable" in v for v in data["workflows"].values())
    prs = sum(v["merged_prs"] for v in data["shipped"].values() if isinstance(v["merged_prs"], int))
    commits = sum(v["commits"] for v in data["shipped"].values() if isinstance(v["commits"], int))
    st = data["scheduled_tasks"]
    print(f"usage_gather: month={data['month']} repos={len(repos)} merged_prs={prs} "
          f"commits={commits} workflows={len(data['workflows'])} workflows_unavailable={wf_bad} "
          f"scheduled_tasks={'unavailable' if 'unavailable' in st else len(st['tasks'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
