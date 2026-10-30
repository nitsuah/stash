"""sotu.py pre-step: auto routine health, delta, verify hints. No network: gh is stubbed."""
import datetime as dt
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sotu", os.path.join(HERE, "sotu.py"))
sotu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sotu)

TODAY = dt.date(2026, 10, 30)


def fake_gh(monkeypatch, responses):
    """responses: function(args) -> (rc, stdout, stderr). Records calls."""
    calls = []

    def run(args):
        calls.append(args)
        return responses(args)

    monkeypatch.setattr(sotu, "run_gh", run)
    return calls


def test_local_task_rows_from_frontmatter(tmp_path):
    (tmp_path / "week-x").mkdir()
    (tmp_path / "week-x" / "SKILL.md").write_text("---\nname: week-x\ndescription: d\n---\nbody\n", encoding="utf-8")
    (tmp_path / "_backup").mkdir()
    (tmp_path / "_backup" / "SKILL.md").write_text("---\nname: nope\n---\n", encoding="utf-8")
    (tmp_path / "nofm").mkdir()
    (tmp_path / "nofm" / "SKILL.md").write_text("no frontmatter", encoding="utf-8")
    rows = sotu.local_task_rows(tmp_path)
    assert [r["name"] for r in rows] == ["nofm", "week-x"]
    assert all(r["status"] == "unknown" and r["last_run"] == "unknown" for r in rows)


def test_local_task_rows_missing_dir(tmp_path):
    assert sotu.local_task_rows(tmp_path / "absent") == []


def test_auto_routines_happy_path(monkeypatch, tmp_path):
    def resp(args):
        if args[0] == "run":
            return 0, json.dumps([{"conclusion": "success", "status": "completed", "createdAt": "2026-10-29T10:00:00Z"}]), ""
        owner = args[args.index("--owner") + 1]
        repos = [{"repository": {"name": "fire"}}, {"repository": {"name": "fire"}}] if owner == "nitsuah" else []
        return 0, json.dumps(repos), ""

    fake_gh(monkeypatch, resp)
    out = sotu.auto_routines(["fire", "vigil"], tmp_path)
    by = {r["name"]: r for r in out["routines"]}
    assert by["obn-health"]["status"] == "succeeded" and by["obn-health"]["last_run"] == "2026-10-29"
    assert by["repo-health issues"]["status"] == "issues" and "fire 2" in by["repo-health issues"]["note"]
    assert out["repo_health_issues"] == {"fire": 2, "vigil": 0}
    assert out["quota"] is None


def test_auto_routines_unknown_when_gh_fails(monkeypatch, tmp_path):
    fake_gh(monkeypatch, lambda a: (1, "", "boom"))
    out = sotu.auto_routines(["fire"], tmp_path)
    assert {r["status"] for r in out["routines"]} == {"unknown"}
    assert out["repo_health_issues"] is None


def test_clean_when_no_issues(monkeypatch, tmp_path):
    fake_gh(monkeypatch, lambda a: (0, "[]", ""))
    rows = {r["name"]: r for r in sotu.auto_routines(["fire"], tmp_path)["routines"]}
    assert rows["repo-health issues"]["status"] == "clean"
    assert rows["obn-health"]["status"] == "unknown"  # empty run list is not a guess


def t(repo, title, prio="P1", status="todo"):
    return {"repo": repo, "title": title, "priority": prio, "status": status, "ref": "TASKS.md:1"}


def test_delta_new_closed_moved():
    prev = {"generated_at": "w1", "tasks": [t("a", "old"), t("a", "stay"), t("a", "mover", "P2")],
            "needs_you": [t("a", "ny-old")], "kickoff": [t("b", "k1")]}
    cur = {"tasks": [t("a", "stay"), t("a", "new"), t("a", "mover", "P1")],
           "needs_you": [], "kickoff": [t("b", "k1")]}
    d = sotu.compute_delta(prev, cur)
    assert [i["title"] for i in d["tasks"]["new"]] == ["new"]
    assert [i["title"] for i in d["tasks"]["closed"]] == ["old"]
    assert d["tasks"]["moved"][0]["from"]["priority"] == "P2" and d["tasks"]["moved"][0]["to"]["priority"] == "P1"
    assert [i["title"] for i in d["needs_you"]["closed"]] == ["ny-old"]
    assert d["kickoff"]["new"] == [] and d["empty"] is False
    md = "\n".join(sotu.delta_markdown(d))
    assert "## Changes since last run" in md and "new" in md


def test_delta_empty_and_no_baseline():
    same = {"generated_at": "w1", "tasks": [t("a", "x")], "needs_you": [], "kickoff": []}
    d = sotu.compute_delta(same, dict(same))
    assert d["empty"] is True
    assert "nothing changed" in "\n".join(sotu.delta_markdown(d))
    nb = sotu.compute_delta(None, same)
    assert nb["empty"] is False and "no previous" in "\n".join(sotu.delta_markdown(nb))


def test_backtick_paths():
    assert sotu._backtick_paths("fix `agent/scripts/x.py` and `foo.md`, not `a b` or `../etc/x.y`") == [
        "agent/scripts/x.py", "foo.md"]


REPOS = {"pub": {"full_name": "nitsuah/pub", "private": False},
         "priv": {"full_name": "nitsuah/priv", "private": True}}


def verify_data(delta):
    return {"generated_at": "now", "delta": delta, "needs_you": [],
            "kickoff": [{**t("pub", "Add retry logic to `src/retry.py` client"), "criteria": None}],
            "tasks": [t("pub", "Add retry logic to `src/retry.py` client"), t("priv", "Rotate webhook secrets"),
                      t("pub", "Low item", "P2")]}


def test_verify_hints_and_skip(monkeypatch):
    def resp(args):
        if args[0] == "pr":
            repo = args[args.index("-R") + 1]
            if repo == "nitsuah/pub":
                return 0, json.dumps([{"number": 7, "title": "feat: retry logic client", "body": "",
                                       "mergedAt": "2026-10-28T00:00:00Z"}]), ""
            return 0, "[]", ""
        return 1, "", "gh: Not Found (HTTP 404)"

    calls = fake_gh(monkeypatch, resp)
    delta = {"previous": "w1", "empty": True, "tasks": {"new": [], "moved": []}}
    v = sotu.build_verify(verify_data(delta), REPOS, TODAY)
    # one pr list per repo, however many items
    assert sorted(c[c.index("-R") + 1] for c in calls if c[0] == "pr") == ["nitsuah/priv", "nitsuah/pub"]
    by = {i["title"]: i for i in v["items"]}
    pub = by["Add retry logic to `src/retry.py` client"]
    assert pub["pr_hints"][0]["number"] == 7 and pub["skip_model"] is False
    assert pub["path_checks"] == [{"path": "src/retry.py", "exists": False}]
    priv = by["Rotate webhook secrets"]
    assert priv["skip_model"] is True and priv["pr_hints"] == []
    assert "Low item" not in by  # P2 not verified
    assert v["all_skip"] is False


def test_private_repo_hints_hide_titles(monkeypatch):
    def resp(args):
        return 0, json.dumps([{"number": 3, "title": "Rotate webhook secrets", "body": "",
                               "mergedAt": "2026-10-29T00:00:00Z"}]), ""

    fake_gh(monkeypatch, resp)
    data = {"generated_at": "n", "delta": {"previous": "w", "empty": True}, "needs_you": [], "kickoff": [],
            "tasks": [t("priv", "Rotate webhook secrets")]}
    v = sotu.build_verify(data, REPOS, TODAY)
    hint = v["items"][0]["pr_hints"][0]
    assert hint["number"] == 3 and "title" not in hint


def test_changed_or_no_baseline_never_skips(monkeypatch):
    fake_gh(monkeypatch, lambda a: (0, "[]", ""))
    d = {"previous": "w", "empty": False, "tasks": {"new": [{"repo": "priv", "title": "Rotate webhook secrets"}],
                                                      "moved": []}}
    v = sotu.build_verify(verify_data(d), REPOS, TODAY)
    assert {i["title"]: i["skip_model"] for i in v["items"]}["Rotate webhook secrets"] is False
    v2 = sotu.build_verify(verify_data({"previous": None, "empty": False}), REPOS, TODAY)
    assert not any(i["skip_model"] for i in v2["items"])


def test_pr_lookup_failure_never_skips(monkeypatch):
    fake_gh(monkeypatch, lambda a: (1, "", "boom"))
    v = sotu.build_verify(verify_data({"previous": "w", "empty": True}), REPOS, TODAY)
    assert all(i["lookup_failed"] and not i["skip_model"] for i in v["items"])


def test_routines_none_and_file_backcompat(tmp_path, monkeypatch):
    monkeypatch.setattr(sotu, "auto_routines", lambda *a, **k: (_ for _ in ()).throw(AssertionError("no auto")))
    f = tmp_path / "r.json"
    f.write_text(json.dumps({"routines": [{"name": "x"}], "quota": {"weekly": 5}}), encoding="utf-8")
    monkeypatch.setattr(sotu, "tracked_repos", lambda: [
        {"repo": "pub", "path": str(tmp_path), "full_name": "nitsuah/pub", "private": False, "scope_tier": "1"}])
    monkeypatch.setattr(sotu, "local_tasks", lambda repos: ([], []))
    monkeypatch.setattr(sotu, "ledger_items", lambda: [])
    d = sotu.build(str(f), False, fetch=False)
    assert d["routines"] == [{"name": "x"}] and d["quota"] == {"weekly": 5}
    assert sotu.build("none", False, fetch=False)["routines"] == []
