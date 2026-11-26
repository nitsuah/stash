"""sotu.py pure helpers: norm_tier, classify, public_view. No network."""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sotu", os.path.join(HERE, "sotu.py"))
sotu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sotu)


def item(**kw):
    base = {"repo": "app", "title": "Fix the login bug", "section": "Todo", "priority": "P1"}
    base.update(kw)
    return base


def test_norm_tier_accepts_t_tier_and_bare_digits():
    assert [sotu.norm_tier(x) for x in ("T1", "Tier 2", "3")] == ["1", "2", "3"]


def test_norm_tier_falls_back_to_dash():
    assert [sotu.norm_tier(x) for x in (None, "", "-", "5")] == ["-", "-", "-", "-"]


def test_classify_plain_item_scores_its_priority():
    t = sotu.classify(item())
    assert t["initiative"] is False
    assert t["score"] == 60.0
    assert t["routine_candidate"] is False


def test_classify_tier_one_bump():
    assert sotu.classify(item(tier="1"))["score"] == 65.0


def test_classify_stash_initiative_gets_multiplier():
    t = sotu.classify(item(repo="stash", title="Add PMO report for all repos", priority="P2"))
    assert t["initiative"] is True
    assert t["score"] == 45.0


def test_classify_every_repo_title_is_initiative_outside_stash():
    t = sotu.classify(item(title="Update every repo badge"))
    assert t["initiative"] is True


def test_classify_stash_pmo_audit_is_routine_candidate():
    t = sotu.classify(item(repo="stash", title="Add PMO audit report"))
    assert t["initiative"] is True
    assert t["routine_candidate"] is True


def test_classify_without_priority_scores_five():
    assert sotu.classify(item(priority=None))["score"] == 5.0


def test_public_view_leaves_public_repos_unchanged():
    t = item(ref="docs/internal/plan.md:3", criteria="c", owner="o")
    assert sotu.public_view(t, {"secret"}) is t


def test_public_view_keeps_task_refs_for_private_repos():
    for ref in ("docs/TASKS.md:12", "TASKS.md"):
        assert sotu.public_view(item(repo="secret", ref=ref), {"secret"})["ref"] == ref


def test_public_view_redacts_private_repo_details():
    t = item(repo="secret", ref="docs/internal/plan.md:3", criteria="c", owner="o")
    out = sotu.public_view(t, {"secret"})
    assert out["ref"] == "TASKS.md"
    assert out["criteria"] is None and out["owner"] is None and out["section"] is None
    assert out["title"] == "Fix the login bug" and out["priority"] == "P1"
