"""Deterministic vault and routine-output health check (replaces the cloud week-obn-import routine).

Prints a markdown report to stdout and exits 1 when any RED check fails, so CI can fail the job
and open an issue. Read-only. stash is PUBLIC: the report holds counts, file names and dates only.

Checks (same six as the old routine):
  1. STALE NOTES      non-dated agent/notes/*.md untouched for 30+ days (info); newest daily note
                      older than 3 days (RED)
  2. MISSING REPORTS  report types overdue against their cadence (RED)
  3. PLACEHOLDERS     agent/prompts/*.md under 10 lines (RED)
  4. UNTRACKED REPOS  Tracked repos in scope.md with no report in 60+ days (RED)
  5. FOLLOW-UPS       'Pending' items older than 14 days in agent/jobs/ (RED, skipped if absent)
  6. VAULT GRAPH      find-orphans.py --check, output copied verbatim (RED on FAIL lines or exit != 0)

Usage:
  python agent/scripts/obn_health.py [--today YYYY-MM-DD] [--no-graph]
Run from anywhere; the vault is resolved relative to this file. Needs full git history for the
stale-note dates (checkout with fetch-depth: 0).
"""
import argparse
import datetime as dt
import os
import re
import subprocess
import sys

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORTS = os.path.join(VAULT, "reports")
NOTES = os.path.join(VAULT, "notes")
PROMPTS = os.path.join(VAULT, "prompts")
JOBS = os.path.join(VAULT, "jobs")
SCOPE = os.path.join(VAULT, "projects", "scope.md")

STALE_NOTE_DAYS = 30
DAILY_NOTE_MAX_AGE = 3
PLACEHOLDER_LINES = 10
UNTRACKED_DAYS = 60
FOLLOWUP_DAYS = 14

# label -> (directory under reports/, filename glob prefix or None for every .md, max age days)
CADENCE = {
    "cloud/daily-brief": ("cloud/daily-brief", None, 4),
    "cloud/week-vuln": ("cloud/week-vuln", None, 9),
    "eng-loc": ("", "eng-loc-", 9),
    "eng-mini": ("", "eng-mini-", 9),
    "sotu-data": ("sotu", "sotu-", 11),
    "tire-kick": ("", "tire-kick-", 35),
    "pmo-audit": ("", "pmo-audit-", 35),
    "usage-report": ("", "usage-report-", 35),
    "rsi-report": ("", "rsi-report-", 35),
}

DATE_RE = re.compile(r"(\d{4})-(\d{2})(?:-(\d{2}))?")
WEEK_RE = re.compile(r"(\d{4})-W(\d{2})")
DAILY_NOTE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")
WEEKLY_NOTE_RE = re.compile(r"^\d{4}-W\d{2}\.md$")


def file_date(name):
    """Date a report by its filename: YYYY-MM-DD, YYYY-MM (month start) or YYYY-Www (Monday)."""
    m = WEEK_RE.search(name)
    if m:
        try:
            return dt.date.fromisocalendar(int(m.group(1)), int(m.group(2)), 1)
        except ValueError:
            return None
    m = DATE_RE.search(name)
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3) or 1))
    except ValueError:
        return None


def git_last_commit_date(path):
    out = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", path],
        cwd=VAULT, capture_output=True, text=True, check=False,
    ).stdout.strip()
    try:
        return dt.date.fromisoformat(out)
    except ValueError:
        return None


def stale_notes(today, notes_dir=NOTES, last_commit=git_last_commit_date):
    """Return (stale [(name, age)], newest daily note date or None)."""
    stale, newest = [], None
    if not os.path.isdir(notes_dir):
        return stale, newest
    for name in sorted(os.listdir(notes_dir)):
        if not name.endswith(".md"):
            continue
        if DAILY_NOTE_RE.match(name):
            d = file_date(name)
            if d and (newest is None or d > newest):
                newest = d
            continue
        if WEEKLY_NOTE_RE.match(name):
            continue
        d = last_commit(os.path.join(notes_dir, name))
        if d and (today - d).days >= STALE_NOTE_DAYS:
            stale.append((name, (today - d).days))
    return stale, newest


def newest_report_date(directory, prefix):
    if not os.path.isdir(directory):
        return None
    newest = None
    for name in os.listdir(directory):
        if not name.endswith(".md") or (prefix and not name.startswith(prefix)):
            continue
        d = file_date(name)
        if d and (newest is None or d > newest):
            newest = d
    return newest


def missing_reports(today, reports_dir=REPORTS, cadence=CADENCE):
    """Return [(label, newest date or None, age or None, limit)] for overdue types."""
    overdue = []
    for label, (sub, prefix, limit) in cadence.items():
        newest = newest_report_date(os.path.join(reports_dir, sub), prefix)
        age = (today - newest).days if newest else None
        if newest is None or age > limit:
            overdue.append((label, newest, age, limit))
    return overdue


def placeholder_prompts(prompts_dir=PROMPTS):
    out = []
    if not os.path.isdir(prompts_dir):
        return out
    for name in sorted(os.listdir(prompts_dir)):
        if not name.endswith(".md"):
            continue
        with open(os.path.join(prompts_dir, name), encoding="utf-8") as f:
            n = sum(1 for _ in f)
        if n < PLACEHOLDER_LINES:
            out.append((name, n))
    return out


def tracked_repos(scope_path=SCOPE):
    """Return {repo: [aliases]} from the 'Tracked' table in scope.md."""
    repos = {}
    if not os.path.isfile(scope_path):
        return repos
    in_tracked = False
    with open(scope_path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("## "):
                in_tracked = line.startswith("## Tracked")
                continue
            if not in_tracked or not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            name = cells[0].strip("` ")
            if not name or name.lower() == "repo" or set(name) <= set("-: "):
                continue
            aliases = re.findall(r"formerly `([\w.-]+)`", line)
            repos[name] = aliases
    return repos


def all_report_files(reports_dir=REPORTS):
    for _root, _dirs, files in os.walk(reports_dir):
        for name in files:
            if name.endswith(".md"):
                yield name


def untracked_repos(today, repos, reports_dir=REPORTS):
    """Tracked repos with no dated report naming them (or an alias) in UNTRACKED_DAYS."""
    names = list(all_report_files(reports_dir))
    stale = []
    for repo, aliases in sorted(repos.items()):
        keys = [repo, *aliases]
        dates = [file_date(n) for n in names if any(k in n for k in keys)]
        dates = [d for d in dates if d]
        newest = max(dates) if dates else None
        if newest is None or (today - newest).days >= UNTRACKED_DAYS:
            stale.append((repo, newest))
    return stale


def pending_followups(today, jobs_dir=JOBS):
    """'Pending' lines older than FOLLOWUP_DAYS in agent/jobs/*.md, dated by a YYYY-MM-DD on the line."""
    if not os.path.isdir(jobs_dir):
        return None
    out = []
    for name in sorted(os.listdir(jobs_dir)):
        if not name.endswith(".md"):
            continue
        with open(os.path.join(jobs_dir, name), encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                if "pending" not in line.lower():
                    continue
                d = file_date(line) if DATE_RE.search(line) else None
                if d and (today - d).days > FOLLOWUP_DAYS:
                    out.append((f"{name}:{i}", (today - d).days))
    return out


def vault_graph():
    proc = subprocess.run(
        [sys.executable, os.path.join(VAULT, "scripts", "find-orphans.py"), "--check"],
        cwd=VAULT, capture_output=True, text=True, check=False,
    )
    text = (proc.stdout + proc.stderr).strip()
    red = proc.returncode != 0 or "FAIL" in text
    return text, red


def build_report(today, graph=True):
    lines, red = [], []

    stale, newest = stale_notes(today)
    daily_age = (today - newest).days if newest else None
    daily_red = newest is None or daily_age > DAILY_NOTE_MAX_AGE

    overdue = missing_reports(today)
    placeholders = placeholder_prompts()
    untracked = untracked_repos(today, tracked_repos())
    followups = pending_followups(today)

    lines.append(f"# obn-health: {today.isoformat()}")
    lines.append("")

    lines.append("## 1. Stale notes")
    if newest:
        lines.append(f"Newest daily note: {newest.isoformat()} ({daily_age}d old)"
                     f"{' (RED: over ' + str(DAILY_NOTE_MAX_AGE) + 'd)' if daily_red else ''}.")
    else:
        lines.append("No daily note found (RED).")
    if daily_red:
        red.append("daily note")
    lines.extend([f"- {n}: {a}d since last commit" for n, a in stale] or ["No non-dated notes over 30d."])

    lines.append("")
    lines.append("## 2. Missing reports")
    for label, newest_d, age, limit in overdue:
        when = f"{newest_d.isoformat()} ({age}d)" if newest_d else "never"
        lines.append(f"- RED {label}: last {when}, limit {limit}d")
    if overdue:
        red.append("missing reports")
    else:
        lines.append("All report types within cadence.")

    lines.append("")
    lines.append("## 3. Placeholder prompts")
    lines.extend([f"- RED {n}: {c} lines" for n, c in placeholders] or ["None."])
    if placeholders:
        red.append("placeholder prompts")

    lines.append("")
    lines.append("## 4. Untracked repos")
    for repo, newest_d in untracked:
        lines.append(f"- RED {repo}: last report {newest_d.isoformat() if newest_d else 'never'}")
    if untracked:
        red.append("untracked repos")
    else:
        lines.append("None flagged.")

    lines.append("")
    lines.append("## 5. Follow-ups")
    if followups is None:
        lines.append("`agent/jobs/` does not exist: skipped.")
    else:
        lines.extend([f"- RED {w}: pending {a}d" for w, a in followups] or ["None over 14d."])
        if followups:
            red.append("follow-ups")

    lines.append("")
    lines.append("## 6. Vault graph (`find-orphans.py --check`)")
    if graph:
        text, graph_red = vault_graph()
        lines.append("```")
        lines.append(text)
        lines.append("```")
        if graph_red:
            red.append("vault graph")
    else:
        lines.append("Skipped (--no-graph).")

    lines.insert(2, f"**{'RED: ' + ', '.join(red) if red else 'All clear.'}**")
    lines.insert(3, "")
    return "\n".join(lines) + "\n", bool(red)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD), for tests")
    ap.add_argument("--no-graph", action="store_true", help="skip find-orphans.py --check")
    args = ap.parse_args()
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    report, red = build_report(today, graph=not args.no_graph)
    sys.stdout.write(report)
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
