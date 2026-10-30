"""pmo_prep.py: standards, duplicate docs, changed rule, per-repo JSON."""
import datetime as dt
import json

import pmo_prep as pp
import prestep_common as pc

REPO = {"repo": "demo", "full_name": "nitsuah/demo", "path": "/demo"}
SINCE = dt.date(2026, 10, 1)


class FakeFmt:
    class ReadError(Exception):
        pass

    def check(self, repo):
        return {"repo": repo["repo"], "missing": False, "rel": "TASKS.md", "items": 4,
                "missing_sections": [], "no_prio": [1, 2], "skipped": []}

    def default_ref(self, path):
        return "origin/main"


def test_missing_standards_accepts_alternate_locations():
    paths = ["LICENSE.md", ".github/SECURITY.md", "docs/CODE_OF_CONDUCT.md", "docs/CHANGELOG.md",
             ".github/ISSUE_TEMPLATE/bug.yml", ".github/PULL_REQUEST_TEMPLATE.md"]
    assert pp.missing_standards(paths) == []
    assert pp.missing_standards(["README.md"]) == [
        "LICENSE", "SECURITY.md", "CODE_OF_CONDUCT.md", "CHANGELOG.md",
        ".github/ISSUE_TEMPLATE/", ".github/pull_request_template.md"]


def test_duplicates_and_locations():
    paths = ["README.md", "TASKS.md", "docs/TASKS.md", "docs/ROADMAP.md", "src/TASKS.md"]
    loc = pp.doc_locations(paths)
    assert loc["TASKS"] == ["TASKS.md", "docs/TASKS.md"]
    assert "src/TASKS.md" not in sum(loc.values(), [])
    dates = {"TASKS.md": "2026-10-01", "docs/TASKS.md": "2026-09-01"}
    assert pp.duplicates(loc, dates) == [
        {"doc": "TASKS.md", "root": "2026-10-01", "docs": "2026-09-01"}]


def test_last_audit_date_newest(tmp_path):
    for n in ("pmo-audit-2026-03-27.md", "pmo-audit-2026-10-01.md", "pmo-audit-x.md"):
        (tmp_path / n).write_text("x")
    assert pp.last_audit_date(tmp_path) == dt.date(2026, 10, 1)
    assert pp.last_audit_date(tmp_path / "none") is None


def stub(fake_cmd, prs=None, doc_date="2026-09-01"):
    fake_cmd.on("api", data={"tree": [{"path": "TASKS.md"}, {"path": "docs/TASKS.md"},
                                      {"path": "README.md"}], "truncated": False})
    fake_cmd.on("pr", "list", data=prs or [])
    fake_cmd.on("issue", "list", data=[{"number": 7}])
    fake_cmd.on("-C", "log", stdout=doc_date + "\n")


def test_prep_repo_unchanged(fake_cmd):
    stub(fake_cmd)
    row = pp.prep_repo(REPO, FakeFmt(), SINCE, {}, False)
    assert row["changed"] is False and row["reasons"] == []
    assert row["open_repo_health_issues"] == 1
    assert row["tasks_format"]["no_priority"] == 2
    assert row["duplicate_doc_locations"][0]["doc"] == "TASKS.md"
    assert "LICENSE" in row["missing_standards"]
    # exactly one PR list, one tree listing and one issue list per repo
    assert sum(c[:3] == ["gh", "pr", "list"] for c in fake_cmd.calls) == 1
    assert sum(c[:2] == ["gh", "api"] for c in fake_cmd.calls) == 1
    assert sum(c[:3] == ["gh", "issue", "list"] for c in fake_cmd.calls) == 1


def test_prep_repo_changed_by_each_reason(fake_cmd):
    stub(fake_cmd, doc_date="2026-10-10")
    row = pp.prep_repo(REPO, FakeFmt(), SINCE, {}, False)
    assert row["changed"] and any("changed 2026-10-10" in r for r in row["reasons"])
    fake_cmd.handlers.clear()
    stub(fake_cmd, prs=[{"number": 3, "title": "t", "mergedAt": "2026-10-05T00:00:00Z"}])
    assert pp.prep_repo(REPO, FakeFmt(), SINCE, {}, False)["reasons"] == ["1 merged PRs"]
    fake_cmd.handlers.clear()
    stub(fake_cmd)
    assert pp.prep_repo(REPO, FakeFmt(), SINCE, {"demo": 2}, False)["changed"]
    assert pp.prep_repo(REPO, FakeFmt(), SINCE, {}, True)["reasons"] == ["full sweep"]


def test_vault_repo_is_not_changed_by_itself(fake_cmd):
    stub(fake_cmd, doc_date="2026-10-10")
    vault = {"repo": "stash", "full_name": "nitsuah/stash", "path": "/s"}
    row = pp.prep_repo(vault, FakeFmt(), SINCE, {}, False)
    assert row["changed"] is False and "vault" in row["note"]


def test_gh_failure_is_recorded_not_fatal(fake_cmd):
    fake_cmd.on("gh", rc=1, stderr="boom")
    fake_cmd.on("-C", "log", stdout="2026-10-10\n")
    row = pp.prep_repo(REPO, FakeFmt(), SINCE, {}, False)
    assert row["missing_standards"] is None and row["merged_prs_since_audit"]["count"] is None
    assert len(row["errors"]) >= 3


def test_main_writes_json(tmp_path, monkeypatch, fake_cmd):
    stub(fake_cmd)
    monkeypatch.setattr(pc, "tracked_repos", lambda: [REPO])
    monkeypatch.setattr(pc, "load_script", lambda name: FakeFmt())
    monkeypatch.setattr(pc, "LEDGER", tmp_path / "none.md")
    monkeypatch.setattr(pp, "last_audit_date", lambda *a: SINCE)
    out = tmp_path / "p.json"
    assert pp.main(["--today", "2026-11-01", "--out", str(out)]) == 0
    data = json.loads(out.read_text())
    assert data["unchanged_repos"] == ["demo"] and data["full_sweep"] is False
    pp.main(["--today", "2027-01-05", "--out", str(out)])  # quarterly month
    assert json.loads(out.read_text())["changed_repos"] == ["demo"]


def test_pmo_rows_counts_open_pmo_only():
    text = ("| ID | First seen | Last seen | Seen | Source | Repo | Finding | Class | Status | Link |\n"
            "|--|--|--|--|--|--|--|--|--|--|\n"
            "| F-1 | a | b | 1 | s | demo, vigil | f | pmo | open | |\n"
            "| F-2 | a | b | 1 | s | demo | f | pmo | done | |\n"
            "| F-3 | a | b | 1 | s | demo | f | quick | open | |\n")
    assert pp.pmo_rows(text) == {"demo": 1, "vigil": 1}
