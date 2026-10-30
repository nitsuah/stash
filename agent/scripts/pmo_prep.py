#!/usr/bin/env python3
"""PMO pre-step: per tracked repo, the facts the audit needs, so the model reads one JSON file.

Writes `agent/reports/pmo-prep.json` with, per repo: the `check-tasks-format.py` row, PRs merged
since the last audit, last-commit dates of the planning docs (root and docs/), duplicate doc
locations, missing standards files, the open `bot:repo-health` issue count, and
`changed: true/false`. A repo is `changed` when a TASKS/ROADMAP/README commit or a merged PR is
newer than the last audit, when the findings ledger has an open `pmo` row for it, or when a full
sweep applies (`--full`, or the quarterly months Jan/Apr/Jul/Oct). PMO audits only `changed`
repos. stash (the vault) is reported but never marked changed by itself.

The merged-PR list is trimmed to 20 entries; `count` is the full number.
Calls: one `gh pr list`, one `gh api` tree listing and one `gh issue list` per repo; doc dates
come from the local clone's origin default branch (use --fetch to refresh the clones first).
stash is PUBLIC: output holds counts, repo names, file names and dates only.

Usage:
  python agent/scripts/pmo_prep.py [--full] [--fetch] [--since YYYY-MM-DD] [--today YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import prestep_common as pc

OUT = pc.REPORTS / "pmo-prep.json"
QUARTER_MONTHS = {1, 4, 7, 10}
DOC_NAMES = ("README", "TASKS", "ROADMAP", "CHANGELOG", "FEATURES", "METRICS", "CONTRIBUTING",
             "API", "ARCHITECTURE")
CHANGE_DOCS = ("README", "TASKS", "ROADMAP")  # PMO.md's audit-scope rule
DUP_DOCS = tuple(d for d in DOC_NAMES if d != "README")
VAULT_REPO = "stash"


def last_audit_date(reports: Path = pc.REPORTS) -> dt.date | None:
    dates = []
    for p in reports.glob("pmo-audit-*.md"):
        m = re.fullmatch(r"pmo-audit-(\d{4}-\d{2}-\d{2})\.md", p.name)
        if m:
            dates.append(dt.date.fromisoformat(m.group(1)))
    return max(dates, default=None)


def tree_paths(full_name: str) -> tuple[list[str], bool]:
    tree = pc.gh_json(["api", f"repos/{full_name}/git/trees/HEAD?recursive=1"])
    paths = [t["path"] for t in tree.get("tree", [])]
    return paths, bool(tree.get("truncated"))


def missing_standards(paths: list[str]) -> list[str]:
    """Standards files absent from the tree. Repo-local only (org defaults don't count)."""
    low = {p.lower() for p in paths}

    def has(*names: str) -> bool:
        return any(n.lower() in low for n in names)

    missing = []
    if not any(re.fullmatch(r"license(\.\w+)?", p) for p in low):
        missing.append("LICENSE")
    for name in ("SECURITY.md", "CODE_OF_CONDUCT.md"):
        if not has(name, f"docs/{name}", f".github/{name}"):
            missing.append(name)
    if not has("CHANGELOG.md", "docs/CHANGELOG.md"):
        missing.append("CHANGELOG.md")
    if not any(p.startswith(".github/issue_template/") or p == ".github/issue_template.md"
               for p in low):
        missing.append(".github/ISSUE_TEMPLATE/")
    if not has(".github/pull_request_template.md", "pull_request_template.md",
               "docs/pull_request_template.md"):
        missing.append(".github/pull_request_template.md")
    return missing


def doc_locations(paths: list[str]) -> dict[str, list[str]]:
    """doc name -> the paths it exists at (root and/or docs/), exact `<NAME>.md` match."""
    wanted = {f"{n}.md": n for n in DOC_NAMES} | {f"docs/{n}.md": n for n in DOC_NAMES}
    out: dict[str, list[str]] = {}
    for p in paths:
        if p in wanted:
            out.setdefault(wanted[p], []).append(p)
    return out


def doc_dates(path: str, ref: str, locations: dict[str, list[str]]) -> dict[str, str | None]:
    """Last-commit date per existing doc path, from the local clone (None if unreadable)."""
    out: dict[str, str | None] = {}
    for paths in locations.values():
        for rel in paths:
            try:
                out[rel] = pc.git(path, "log", "-1", "--format=%cs", ref, "--", rel).strip() or None
            except pc.GhError:
                out[rel] = None
    return out


def duplicates(locations: dict[str, list[str]], dates: dict[str, str | None]) -> list[dict]:
    return [{"doc": f"{name}.md", "root": dates.get(f"{name}.md"),
             "docs": dates.get(f"docs/{name}.md")}
            for name in DUP_DOCS if len(locations.get(name, [])) == 2]


def pmo_rows(ledger_text: str) -> dict[str, int]:
    """Open `pmo`-class ledger rows per repo."""
    counts: dict[str, int] = {}
    for row in pc.parse_ledger(ledger_text):
        if row["Class"] == "pmo" and row["Status"] == "open":
            for repo in row["Repo"].split(","):
                counts[repo.strip()] = counts.get(repo.strip(), 0) + 1
    return counts


def format_row(fmt, repo: dict) -> dict:
    """The check-tasks-format.py result for one repo, trimmed to counts and short lists."""
    r = fmt.check(repo)
    if r.get("missing"):
        return {"tasks_file": None, "why": r["why"]}
    return {"tasks_file": r["rel"], "open_items": r["items"],
            "missing_sections": r["missing_sections"], "no_priority": len(r["no_prio"]),
            "skipped_checkboxes": len(r["skipped"])}


def prep_repo(repo: dict, fmt, since: dt.date | None, pmo_open: dict[str, int],
              full: bool) -> dict:
    name, errors = repo["repo"], []
    row: dict = {"repo": name, "tasks_format": {}, "errors": errors}
    try:
        row["tasks_format"] = format_row(fmt, repo)
    except Exception as exc:  # one broken clone must not sink the whole run
        errors.append(f"tasks-format: {type(exc).__name__}")
    paths: list[str] = []
    try:
        paths, truncated = tree_paths(repo["full_name"])
        row["missing_standards"] = missing_standards(paths)
        if truncated:
            errors.append("tree truncated: standards and doc lists may be incomplete")
    except pc.GhError as exc:
        row["missing_standards"] = None
        errors.append(str(exc))
    locations = doc_locations(paths)
    dates: dict[str, str | None] = {}
    try:
        ref = fmt.default_ref(repo["path"])
        if ref:
            dates = doc_dates(repo["path"], ref, locations)
        else:
            errors.append("no remote default branch in the local clone")
    except fmt.ReadError as exc:
        errors.append(str(exc))
    row["doc_dates"] = dates
    row["duplicate_doc_locations"] = duplicates(locations, dates)
    merged = None
    try:
        args = ["pr", "list", "-R", repo["full_name"], "--state", "merged", "--json",
                "number,title,mergedAt", "--limit", "100"]
        if since:
            args += ["--search", f"merged:>={since.isoformat()}"]
        prs = pc.gh_json(args)
        merged = [{"number": p["number"], "title": p["title"][:80],
                   "merged": p["mergedAt"][:10]} for p in prs]
    except pc.GhError as exc:
        errors.append(str(exc))
    row["merged_prs_since_audit"] = {"count": len(merged) if merged is not None else None,
                                     "capped": len(merged or []) >= 100,
                                     "prs": (merged or [])[:20]}
    try:
        row["open_repo_health_issues"] = len(pc.gh_json(
            ["issue", "list", "-R", repo["full_name"], "--label", "bot:repo-health", "--state",
             "open", "--json", "number", "--limit", "20"]))
    except pc.GhError as exc:
        row["open_repo_health_issues"] = None
        errors.append(str(exc))

    reasons = []
    if since:
        for doc in CHANGE_DOCS:
            newest = max((d for p, d in dates.items()
                          if d and p in (f"{doc}.md", f"docs/{doc}.md")), default=None)
            if newest and newest >= since.isoformat():
                reasons.append(f"{doc} changed {newest}")
    else:
        reasons.append("no prior audit found")
    if row["merged_prs_since_audit"]["count"]:
        reasons.append(f"{row['merged_prs_since_audit']['count']} merged PRs")
    if pmo_open.get(name):
        reasons.append(f"{pmo_open[name]} open pmo ledger rows")
    if full:
        reasons.append("full sweep")
    if name == VAULT_REPO:
        row["note"] = "vault: skipped by name in the PMO loop; vault upkeep (step 7) covers it"
        reasons = ["full sweep"] if full else []
    row["changed"] = bool(reasons)
    row["reasons"] = reasons
    return row


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--full", action="store_true", help="mark every repo changed (full sweep)")
    ap.add_argument("--fetch", action="store_true", help="git fetch each tracked clone first")
    ap.add_argument("--since", help="override the last audit date (YYYY-MM-DD)")
    ap.add_argument("--today", default=dt.date.today().isoformat())
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args(argv)

    today = dt.date.fromisoformat(a.today)
    since = dt.date.fromisoformat(a.since) if a.since else last_audit_date()
    full = a.full or today.month in QUARTER_MONTHS
    fmt = pc.load_script("check-tasks-format.py")
    repos = pc.tracked_repos()
    stale_fetch: list[str] = []
    if a.fetch:
        stale_fetch = fmt.sotu.fetch_all(repos)
    ledger = pc.LEDGER.read_text("utf-8") if pc.LEDGER.exists() else ""
    pmo_open = pmo_rows(ledger)
    rows = [prep_repo(r, fmt, since, pmo_open, full) for r in repos]
    data = {"generated": a.today, "last_audit": since.isoformat() if since else None,
            "full_sweep": full, "fetch_failed": stale_fetch,
            "changed_repos": [r["repo"] for r in rows if r["changed"]],
            "unchanged_repos": [r["repo"] for r in rows if not r["changed"]],
            "repos": rows}
    pc.write_json(Path(a.out), data)
    n_err = sum(bool(r["errors"]) for r in rows)
    print(f"pmo_prep: repos={len(rows)} changed={len(data['changed_repos'])} "
          f"full_sweep={str(full).lower()} last_audit={data['last_audit']} repos_with_errors={n_err}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
