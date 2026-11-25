"""pytest coverage for check-tasks-format.py"""
import importlib.util
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cft", os.path.join(HERE, "check-tasks-format.py"))
cft = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cft)


def test_skipped_pattern_matches():
    skipped_lines = [
        "  - [ ] nested",
        "    - [x] deeper",
        "* [ ] star",
        "+ [/] plus",
    ]
    for line in skipped_lines:
        assert cft.SKIPPED.match(line), f"should match: {line}"

    not_skipped = [
        "- [ ] top",
        " - [ ] one space",
    ]
    for line in not_skipped:
        assert not cft.SKIPPED.match(line), f"should not match: {line}"


def test_check_happy_path(monkeypatch):
    TEXT = (
        "# Tasks\n\n"
        "## Todo\n"
        "- [ ] first item\n\n"
        "## Done\n"
        "- [x] shipped\n"
    )

    monkeypatch.setattr(cft, "default_ref", lambda path: "origin/main")
    monkeypatch.setattr(cft, "read_file", lambda path, ref, rel: TEXT if rel == "TASKS.md" else None)

    repo = {"repo": "demo", "path": "/x"}
    result = cft.check(repo)

    assert result["missing"] is False
    assert result["rel"] == "TASKS.md"
    assert result["missing_sections"] == ["in progress"]
    assert result["skipped"] == []


def test_check_skipped_nested_item(monkeypatch):
    TEXT = (
        "# Tasks\n\n"
        "## Todo\n"
        "- [ ] first item\n\n"
        "## Done\n"
        "- [x] shipped\n"
        "  - [ ] nested\n"
    )

    monkeypatch.setattr(cft, "default_ref", lambda path: "origin/main")
    monkeypatch.setattr(cft, "read_file", lambda path, ref, rel: TEXT if rel == "TASKS.md" else None)

    repo = {"repo": "demo", "path": "/x"}
    result = cft.check(repo)

    assert result["skipped"] == ["TASKS.md:8"]


def test_check_no_tasks_file(monkeypatch):
    monkeypatch.setattr(cft, "default_ref", lambda path: "origin/main")
    monkeypatch.setattr(cft, "read_file", lambda path, ref, rel: None)

    repo = {"repo": "demo", "path": "/x"}
    result = cft.check(repo)

    assert result["missing"] is True
    assert result["why"] == "no TASKS.md on origin/main"


def test_check_no_default_ref(monkeypatch):
    monkeypatch.setattr(cft, "default_ref", lambda path: None)

    repo = {"repo": "demo", "path": "/x"}
    result = cft.check(repo)

    assert result["missing"] is True
    assert "never fetched" in result["why"]


def test_check_read_error(monkeypatch):
    monkeypatch.setattr(cft, "default_ref", lambda path: "origin/main")
    monkeypatch.setattr(cft, "read_file", lambda path, ref, rel: (_ for _ in ()).throw(cft.ReadError("boom")))

    repo = {"repo": "demo", "path": "/x"}
    result = cft.check(repo)

    assert result["missing"] is True
    assert result["why"].startswith("read failed:")
