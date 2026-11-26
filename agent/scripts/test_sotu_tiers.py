"""sotu.py helpers: apply_tiers, kickoff_prompt, _keywords. No network."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sotu", os.path.join(HERE, "sotu.py"))
sotu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sotu)


def test_apply_tiers_without_live_copies_scope_tier():
    repos = [{"repo": "a", "scope_tier": "1"}, {"repo": "b", "scope_tier": "3"}]
    assert sotu.apply_tiers(repos, None) == []
    assert [r["tier"] for r in repos] == ["1", "3"]


def test_apply_tiers_reports_drift_against_live_tiers():
    repos = [
        {"repo": "a", "scope_tier": "1"},
        {"repo": "b", "scope_tier": "3"},
        {"repo": "c", "scope_tier": "2"},
    ]
    drift = sotu.apply_tiers(repos, {"a": "1", "b": "2"})
    assert [r["tier"] for r in repos] == ["1", "2", "-"]
    assert drift == [
        {"repo": "b", "vigil": "2", "scope_md": "3"},
        {"repo": "c", "vigil": "-", "scope_md": "2"},
    ]


def test_kickoff_prompt_basic():
    repos = {"app": {"path": "C:/code/app"}}
    t = {"repo": "app", "title": "Ship it", "ref": "TASKS.md:4", "priority": "P1"}
    out = sotu.kickoff_prompt(t, repos)
    assert "Kick off app (C:/code/app)" in out
    assert '"Ship it"' in out and "TASKS.md:4" in out and "P1" in out
    assert "Acceptance criteria" not in out


def test_kickoff_prompt_appends_criteria():
    t = {"repo": "app", "title": "T", "ref": "r", "priority": "P2", "criteria": "tests pass"}
    out = sotu.kickoff_prompt(t, {"app": {"path": "p"}})
    assert out.endswith("Acceptance criteria: tests pass")


def test_kickoff_prompt_unprioritized_and_unknown_repo_path():
    t = {"repo": "ghost", "title": "T", "ref": "r", "priority": None}
    out = sotu.kickoff_prompt(t, {})
    assert "unprioritized" in out
    assert "Kick off ghost (ghost)" in out


def test_keywords_filters_short_words_and_stopwords():
    assert sotu._keywords("Rotate the Cloudflare token; check build") == {
        "rotate",
        "cloudflare",
        "token",
    }


def test_keywords_keeps_hyphenated_words():
    assert "pre-commit" in sotu._keywords("Add a pre-commit hook")
