#!/usr/bin/env python3
"""Saturday week review pre-step: reads Mon-Fri daily notes and extracts Repo Activity.

Writes JSON for the DAILY step 4 (Coverage and Wins):
  present      ISO dates of notes that exist (Mon-Fri)
  missing      ISO dates of notes that don't exist
  repo_activity {date: [lines from ## Repo Activity section]}

Usage:
  python agent/scripts/week_review.py [--notes-dir DIR] [--saturday YYYY-MM-DD]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


def week_days(saturday: dt.date) -> list[dt.date]:
    """The five dates Monday to Friday of the week that ends on `saturday`."""
    # Saturday is the end of the week; Monday is 5 days before
    monday = saturday - dt.timedelta(days=5)
    return [monday + dt.timedelta(days=i) for i in range(5)]


def repo_activity(text: str) -> list[str]:
    """Bullet lines between `## Repo Activity` heading and the next `## ` heading."""
    lines = text.splitlines()
    in_section = False
    result: list[str] = []
    for line in lines:
        if line.startswith("## Repo Activity"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("- "):
            result.append(line[2:])
    return result


def collect(notes_dir: Path, saturday: dt.date) -> dict:
    """Collect present/missing notes and their Repo Activity for the Mon-Fri week."""
    days = week_days(saturday)
    present: list[str] = []
    missing: list[str] = []
    repo_activity_map: dict[str, list[str]] = {}
    for d in days:
        iso = d.isoformat()
        note_path = notes_dir / f"{iso}.md"
        if note_path.is_file():
            present.append(iso)
            text = note_path.read_text(encoding="utf-8")
            repo_activity_map[iso] = repo_activity(text)
        else:
            missing.append(iso)
    return {
        "saturday": saturday.isoformat(),
        "present": present,
        "missing": missing,
        "repo_activity": repo_activity_map,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    repo_root = Path(__file__).resolve().parents[2]
    default_notes = repo_root / "agent" / "notes"
    ap.add_argument("--notes-dir", default=str(default_notes))
    # most recent Saturday on or before today
    today = dt.date.today()
    last_sat = today - dt.timedelta(days=(today.weekday() + 2) % 7)
    ap.add_argument("--saturday", default=last_sat.isoformat())
    a = ap.parse_args(argv)

    saturday = dt.date.fromisoformat(a.saturday)
    result = collect(Path(a.notes_dir), saturday)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
