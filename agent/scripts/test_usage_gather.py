"""usage_gather.py: window, run stats, unavailable handling, JSON shape."""
import datetime as dt
import json

import prestep_common as pc
import usage_gather as ug

REPO = {"repo": "demo", "full_name": "nitsuah/demo", "path": "/demo"}
OCT = (dt.date(2026, 10, 1), dt.date(2026, 10, 31))


def test_window_defaults_to_previous_month():
    assert ug.window(None, dt.date(2026, 11, 1)) == OCT
    assert ug.window(None, dt.date(2027, 1, 3)) == (dt.date(2026, 12, 1), dt.date(2026, 12, 31))
    assert ug.window("2026-02", dt.date(2026, 11, 1))[1] == dt.date(2026, 2, 28)


def test_run_stats_counts():
    s = ug.run_stats(["success", "success", "failure", "cancelled", "in_progress", None])
    assert s == {"runs": 6, "success": 2, "failure": 1, "cancelled": 1, "other": 2}


def test_scheduled_tasks_unavailable_without_records(tmp_path):
    (tmp_path / "t1").mkdir()
    (tmp_path / "t1" / "SKILL.md").write_text("x")
    out = ug.scheduled_task_stats(tmp_path, *OCT)
    assert "unavailable" in out and "list_task_runs" in out["unavailable"]
    assert "does not exist" in ug.scheduled_task_stats(tmp_path / "nope", *OCT)["unavailable"]


def test_scheduled_tasks_reads_records_in_window(tmp_path):
    t = tmp_path / "daily"
    t.mkdir()
    (t / "runs.json").write_text(json.dumps({"runs": [
        {"started_at": "2026-10-02T10:00:00Z", "status": "succeeded"},
        {"started_at": "2026-10-03T10:00:00Z", "status": "failed", "error": "weekly limit"},
        {"started_at": "2026-09-30T10:00:00Z", "status": "failed"}]}))
    (tmp_path / "_backup").mkdir()
    out = ug.scheduled_task_stats(tmp_path, *OCT)
    assert out["tasks"]["daily"]["runs"] == 2 and out["tasks"]["daily"]["failure"] == 1
    assert out["tasks"]["daily"]["top_failure_reason"] == "weekly limit"


def test_workflow_stats_and_gh_failure(fake_cmd):
    fake_cmd.on("run", "list", "nitsuah/demo",
                data=[{"conclusion": "success", "status": "completed"},
                      {"conclusion": "", "status": "in_progress"}])
    s = ug.workflow_stats("nitsuah/demo", "repo-health.yml", *OCT)
    assert s["runs"] == 2 and s["success"] == 1 and s["other"] == 1
    assert "2026-10-01..2026-10-31" in fake_cmd.calls[0]
    fake_cmd.on("run", "list", "nitsuah/bad", rc=1, stderr="workflow not found")
    assert "unavailable" in ug.workflow_stats("nitsuah/bad", "x.yml", *OCT)


def test_shipped_counts_and_unavailable_commits(fake_cmd):
    fake_cmd.on("pr", "list", data=[{"number": 1}, {"number": 2}])
    fake_cmd.on("rev-parse", stdout="abc\n")
    fake_cmd.on("rev-list", stdout="14\n")
    assert ug.shipped(REPO, *OCT) == {"merged_prs": 2, "commits": 14}
    fake_cmd.handlers.clear()
    fake_cmd.on("pr", "list", rc=1, stderr="no auth")
    out = ug.shipped(REPO, *OCT)
    assert out["merged_prs"].startswith("unavailable") and out["commits"].startswith("unavailable")


def test_main_writes_json(tmp_path, monkeypatch, fake_cmd):
    monkeypatch.setattr(pc, "tracked_repos", lambda: [REPO])
    fake_cmd.on("run", "list", data=[{"conclusion": "success", "status": "completed"}])
    fake_cmd.on("pr", "list", data=[{"number": 1}])
    fake_cmd.on("rev-parse", stdout="abc\n")
    fake_cmd.on("rev-list", stdout="3\n")
    out = tmp_path / "u.json"
    args = ["--today", "2026-11-01", "--tasks-dir", str(tmp_path / "no"), "--out", str(out)]
    assert ug.main(args) == 0
    data = json.loads(out.read_text())
    assert data["month"] == "2026-10" and data["partial_month"] is False
    assert set(data["workflows"]) == {"stash/obn-health", "demo/repo-health"}
    assert data["shipped"]["demo"] == {"merged_prs": 1, "commits": 3}
    assert "unavailable" in data["scheduled_tasks"]
