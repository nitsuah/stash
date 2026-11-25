"""week_review.py: week_days, repo_activity, collect JSON shape."""
import datetime as dt
import json

import week_review as wr


def test_week_days_mon_fri():
    sat = dt.date(2026, 10, 17)
    days = wr.week_days(sat)
    assert days == [
        dt.date(2026, 10, 12),
        dt.date(2026, 10, 13),
        dt.date(2026, 10, 14),
        dt.date(2026, 10, 15),
        dt.date(2026, 10, 16),
    ]


def test_repo_activity_extracts_bullets_between_headings():
    text = """# Note

## Repo Activity
- first activity line
- second activity line

## Tasks
- some task
"""
    assert wr.repo_activity(text) == ["first activity line", "second activity line"]


def test_repo_activity_returns_empty_when_heading_absent():
    text = """# Note

## Tasks
- some task
"""
    assert wr.repo_activity(text) == []


def test_collect_present_missing_and_repo_activity(tmp_path):
    notes_dir = tmp_path / "notes"
    notes_dir.mkdir()

    # Monday exists with Repo Activity
    mon = notes_dir / "2026-10-12.md"
    mon.write_text("""# 2026-10-12

## Repo Activity
- fixed bug in login
- refactored auth module

## Tasks
- review PR
""", encoding="utf-8")

    # Tuesday exists without Repo Activity
    tue = notes_dir / "2026-10-13.md"
    tue.write_text("""# 2026-10-13

## Tasks
- write tests
""", encoding="utf-8")

    # Wed, Thu, Fri missing (no files)

    result = wr.collect(notes_dir, dt.date(2026, 10, 17))

    assert result["saturday"] == "2026-10-17"
    assert result["present"] == ["2026-10-12", "2026-10-13"]
    assert result["missing"] == ["2026-10-14", "2026-10-15", "2026-10-16"]
    assert result["repo_activity"] == {
        "2026-10-12": ["fixed bug in login", "refactored auth module"],
        "2026-10-13": [],
    }
