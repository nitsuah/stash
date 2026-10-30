"""obn_health.py: date parsing, cadence checks, scope.md parsing."""
import datetime as dt
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("obn_health", os.path.join(HERE, "obn_health.py"))
oh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oh)

TODAY = dt.date(2026, 10, 29)


def touch(path, text="x\n"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def test_file_date_formats():
    assert oh.file_date("obn-2026-10-28.md") == dt.date(2026, 10, 28)
    assert oh.file_date("usage-report-2026-09.md") == dt.date(2026, 9, 1)
    assert oh.file_date("sotu-2026-W43.md") == dt.date(2026, 10, 19)
    assert oh.file_date("scope.md") is None


def test_missing_reports_flags_old_and_absent(tmp_path):
    r = str(tmp_path)
    touch(os.path.join(r, "eng-loc-fire-2026-10-28.md"))
    touch(os.path.join(r, "eng-mini-fire-2026-10-01.md"))
    cadence = {"eng-loc": ("", "eng-loc-", 9), "eng-mini": ("", "eng-mini-", 9),
               "tire-kick": ("", "tire-kick-", 35)}
    over = {label: age for label, _d, age, _l in oh.missing_reports(TODAY, r, cadence)}
    assert "eng-loc" not in over
    assert over["eng-mini"] == 28
    assert over["tire-kick"] is None


def test_stale_notes_skips_dated_and_reports_newest(tmp_path):
    n = str(tmp_path)
    for name in ("2026-10-25.md", "2026-10-27.md", "2026-W43.md", "old.md", "fresh.md"):
        touch(os.path.join(n, name))
    ages = {"old.md": dt.date(2026, 8, 1), "fresh.md": dt.date(2026, 10, 20)}
    stale, newest = oh.stale_notes(TODAY, n, lambda p: ages[os.path.basename(p)])
    assert newest == dt.date(2026, 10, 27)
    assert [name for name, _ in stale] == ["old.md"]


def test_placeholder_prompts(tmp_path):
    p = str(tmp_path)
    touch(os.path.join(p, "SHORT.md"), "a\nb\n")
    touch(os.path.join(p, "LONG.md"), "x\n" * 12)
    assert oh.placeholder_prompts(p) == [("SHORT.md", 2)]


def test_tracked_repos_and_untracked(tmp_path):
    scope = tmp_path / "scope.md"
    scope.write_text(
        "## Tracked\n\n| Repo | Tier |\n|---|---|\n"
        "| fire | T1 |\n| motor-pool | T1 (formerly `agent-board`) |\n\n## Other\n| nope | x |\n",
        encoding="utf-8",
    )
    repos = oh.tracked_repos(str(scope))
    assert repos == {"fire": [], "motor-pool": ["agent-board"]}

    r = str(tmp_path / "reports")
    touch(os.path.join(r, "eng-loc-fire-2026-10-28.md"))
    touch(os.path.join(r, "eng-loc-agent-board-2026-10-20.md"))
    assert oh.untracked_repos(TODAY, repos, r) == []
    touch(os.path.join(r, "eng-loc-fire-2026-01-01.md"))
    os.remove(os.path.join(r, "eng-loc-fire-2026-10-28.md"))
    assert [name for name, _ in oh.untracked_repos(TODAY, repos, r)] == ["fire"]


def test_pending_followups_absent_dir_is_none(tmp_path):
    assert oh.pending_followups(TODAY, str(tmp_path / "jobs")) is None
    j = str(tmp_path / "jobs")
    touch(os.path.join(j, "a.md"), "- Pending 2026-10-01 call\n- Pending 2026-10-28 call\n- done 2026-09-01\n")
    assert oh.pending_followups(TODAY, j) == [("a.md:1", 28)]
