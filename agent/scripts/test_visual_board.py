"""pytest coverage for visual_board.py: the COLUMNS table and fix_hint. No git or gh calls."""
import pytest
import visual_board as vb

REPO = {"path": "C:/code/app", "full_name": "o/app"}


def test_columns_are_unique_nonempty_pairs():
    assert len(vb.COLUMNS) == 11
    keys = [k for k, _ in vb.COLUMNS]
    assert len(set(keys)) == len(keys)
    for key, label in vb.COLUMNS:
        assert isinstance(key, str) and key
        assert isinstance(label, str) and label


@pytest.mark.parametrize("key", [k for k, _ in vb.COLUMNS])
def test_every_column_has_a_fix_hint(key):
    hint = vb.fix_hint(key, REPO)
    assert isinstance(hint, str) and hint


def test_actions_pr_hint_uses_token_permission():
    hint = vb.fix_hint("actions_pr", REPO)
    assert "repos/o/app/actions/permissions/workflow" in hint
    assert "default_workflow_permissions=read" in hint
    assert "default_workflow_permissions=write" in vb.fix_hint("actions_pr", REPO, token_perm="write")


def test_spots_and_journeys_hints():
    assert "C:/code/app" in vb.fix_hint("spots", REPO)
    assert vb.fix_hint("journeys", REPO).startswith("Run /journeys")


def test_unknown_column_raises_key_error():
    with pytest.raises(KeyError):
        vb.fix_hint("nope", REPO)
