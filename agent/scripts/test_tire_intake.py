"""tire_intake.py: For TIRE parsing, dedup, lockfile verification, ledger apply, skip_model."""
import base64
import json

import prestep_common as pc
import pytest
import tire_intake as ti

BODY = """# Repo health: stash

## For TIRE

quick | stash | bump urllib3 2.7.0->2.8.0 (PYSEC-1) | peer-dep risk: unknown
quick | stash | bump urllib3 2.7.0->2.8.0 (PYSEC-2) | peer-dep risk: unknown
human | stash | rotate the deploy key | peer-dep risk: n/a

## Other
quick | nope | ignored | x
"""

LEDGER = """---
kind: findings-ledger
---

# Findings ledger

Last intake: 2026-10-01 (TIRE)

| ID | First seen | Last seen | Seen | Source | Repo | Finding | Class | Status | Link |
|----|-----------|-----------|------|--------|------|---------|-------|--------|------|
| F-20261001-01 | 2026-10-01 | 2026-10-01 | 1 | x | stash | Bump urllib3 2.7.0 -> 2.8.0 (PYSEC-1) | quick | open | |
| F-20261001-02 | 2026-10-01 | 2026-10-01 | 1 | x | vigil | Bump next 16.4.0 -> 16.4.1 (GHSA-a) | quick | done | pr |

## Closed
"""

REPOS = [{"repo": "stash", "full_name": "nitsuah/stash", "path": "/x"},
         {"repo": "vigil", "full_name": "nitsuah/vigil", "path": "/y"}]


def test_parse_and_group_merges_advisories():
    items = ti.group_items(ti.parse_for_tire(BODY))
    assert len(items) == 2
    bump = next(i for i in items if "pkg" in i)
    assert bump["advisories"] == ["PYSEC-1", "PYSEC-2"]
    assert bump["finding"] == "Bump urllib3 2.7.0 -> 2.8.0 (PYSEC-1, PYSEC-2)"
    assert ti.parse_for_tire("## Other\nquick | a | b | c") == []


def test_dedup_changed_and_new():
    rows = pc.parse_ledger(LEDGER)
    items = ti.group_items(ti.parse_for_tire(BODY))
    res = ti.intake(rows, items, REPOS, "2026-10-30", None)
    by_status = {i["status"]: i for i in res["items"]}
    assert by_status["changed"]["reason"] == "new advisory PYSEC-2"
    assert by_status["changed"]["ledger_id"] == "F-20261001-01"
    assert by_status["new"]["class"] == "human"
    assert by_status["new"]["ledger_id"] == "F-20261030-01"


def test_closed_row_is_not_reopened_without_verify():
    body = "## For TIRE\nquick | vigil | bump next 16.4.0->16.4.1 (GHSA-a) | peer-dep risk: low\n"
    rows = pc.parse_ledger(LEDGER)
    items = ti.group_items(ti.parse_for_tire(body))
    res = ti.intake(rows, items, REPOS, "2026-10-30", None)
    assert res["items"] == [] and res["recurred_unverified"] == ["F-20261001-02"]
    # verified still vulnerable: a regression, reported as new
    res = ti.intake(rows, items, REPOS, "2026-10-30", lambda *_: ("vulnerable", "pinned 16.4.0"))
    assert res["items"][0]["status"] == "new"


def test_verified_fixed_marks_done_and_nothing_left_for_model():
    rows = pc.parse_ledger(LEDGER)
    items = ti.group_items(ti.parse_for_tire(BODY))
    res = ti.intake(rows, items, REPOS, "2026-10-30", lambda *_: ("fixed", "pins 2.8.1"))
    assert [f["id"] for f in res["fixed"]] == ["F-20261001-01"]
    assert all(i["class"] != "quick" for i in res["items"])
    out = ti.apply_ledger(LEDGER, rows, res, "2026-10-30", True)
    assert "| done | Verified 2026-10-30: pins 2.8.1 |" in out


def test_lockfile_parsers_and_verdict():
    lock = json.dumps({"packages": {
        "": {},
        "node_modules/a/node_modules/urllib3": {"version": "2.7.0"},
        "node_modules/urllib3": {"version": "2.8.1"}}})
    assert sorted(ti.lockfile_versions("package-lock.json", lock, "urllib3")) == ["2.7.0", "2.8.1"]
    assert ti.lockfile_versions("requirements.txt", "Foo_Bar==1.2.3\nx==1\n", "foo-bar") == ["1.2.3"]
    uv = 'name = "msgpack"\nversion = "1.2.1"\n'
    assert ti.lockfile_versions("uv.lock", uv, "msgpack") == ["1.2.1"]
    assert ti.verdict_for(["2.7.0", "2.8.1"], "2.8.0")[0] == "vulnerable"
    assert ti.verdict_for(["2.8.0"], "2.8.0")[0] == "fixed"
    assert ti.verdict_for([], "2.8.0")[0] == "unknown"
    assert ti.vkey("^0.35.4") > ti.vkey("0.33.5")


def test_default_checker_reads_lockfile_via_gh(fake_cmd):
    lock = base64.b64encode(json.dumps(
        {"packages": {"node_modules/sharp": {"version": "0.35.4"}}}).encode()).decode()
    fake_cmd.on("repo", "view", data={"defaultBranchRef": {"name": "main"}})
    fake_cmd.on("repos/nitsuah/vigil/git/trees/main?recursive=1",
                data={"tree": [{"path": "package-lock.json", "type": "blob"},
                               {"path": "node_modules/x/package-lock.json", "type": "blob"}]})
    fake_cmd.on("repos/nitsuah/vigil/contents/package-lock.json?ref=main", data={"content": lock})
    chk = ti.LockfileChecker()
    assert chk(REPOS[1], "sharp", "0.33.5", "0.35.4")[0] == "fixed"
    assert chk(REPOS[1], "sharp", "0.33.5", "0.36.0")[0] == "vulnerable"
    assert sum("contents" in " ".join(c) for c in fake_cmd.calls) == 1  # cached per repo


def test_checker_failure_is_unknown(fake_cmd):
    fake_cmd.on("repo", "view", rc=1, stderr="not found")
    verdict, why = ti.LockfileChecker()(REPOS[0], "x", "1", "2")
    assert verdict == "unknown" and "lockfile read failed" in why


def setup_main(tmp_path, monkeypatch, fake_cmd, ledger_text, issues):
    ledger = tmp_path / "ledger.md"
    ledger.write_text(ledger_text, encoding="utf-8")
    monkeypatch.setattr(pc, "tracked_repos", lambda: REPOS)
    monkeypatch.setattr(pc, "REPORTS", tmp_path / "empty")
    monkeypatch.setattr(pc, "VAULT", tmp_path)
    for r in REPOS:
        fake_cmd.on("issue", "list", r["full_name"], data=issues.get(r["repo"], []))
    return ledger, tmp_path / "in.json"


def run_main(ledger, out, *args):
    rc = ti.main(["--today", "2026-10-30", "--ledger", str(ledger), "--out", str(out), *args])
    return rc, json.loads(out.read_text())


def test_dry_run_does_not_touch_ledger_and_flags_model(tmp_path, monkeypatch, fake_cmd):
    ledger, out = setup_main(tmp_path, monkeypatch, fake_cmd, LEDGER,
                             {"stash": [{"number": 1, "body": BODY}]})
    rc, data = run_main(ledger, out, "--no-verify")
    assert rc == 0 and ledger.read_text() == LEDGER
    assert data["skip_model"] is False and data["counts"]["quick"] == 1
    assert data["applied"] is False and data["verified"] is False


def test_skip_model_when_only_dedup_and_apply_bumps_seen(tmp_path, monkeypatch, fake_cmd):
    body = "## For TIRE\nquick | stash | bump urllib3 2.7.0->2.8.0 (PYSEC-1) | peer-dep risk: x\n"
    issues = {"stash": [{"number": 1, "body": body}]}
    ledger, out = setup_main(tmp_path, monkeypatch, fake_cmd, LEDGER, issues)
    _, data = run_main(ledger, out, "--no-verify", "--apply")
    assert data["skip_model"] is True and data["items"] == [] and data["counts"]["deduped"] == 1
    text = ledger.read_text()
    assert "| F-20261001-01 | 2026-10-01 | 2026-10-30 | 2 |" in text
    assert "Last intake: 2026-10-30 (TIRE)" in text
    # idempotent within a day: a second apply does not bump Seen again
    run_main(ledger, out, "--no-verify", "--apply")
    assert "| 2026-10-30 | 2 |" in ledger.read_text()


def test_load_error_blocks_skip(tmp_path, monkeypatch, fake_cmd):
    ledger, out = setup_main(tmp_path, monkeypatch, fake_cmd, LEDGER, {})
    fake_cmd.on("issue", "list", rc=1, stderr="rate limited")
    _, data = run_main(ledger, out, "--no-verify")
    assert data["skip_model"] is False and data["counts"]["load_errors"] == 2


def test_new_rows_appended_inside_table_and_pipes_escaped():
    rows = pc.parse_ledger(LEDGER)
    res = {"touch": [], "fixed": [], "deduped": 0, "items": [],
           "new_rows": [{"id": "F-20261030-01", "status": "open", "link": "",
                         "item": {"repo": "stash", "finding": "a | b", "class": "pmo"}}]}
    out = ti.apply_ledger(LEDGER, rows, res, "2026-10-30", False)
    lines = out.splitlines()
    new = next(i for i, ln in enumerate(lines) if ln.startswith("| F-20261030-01"))
    assert lines[new - 1].startswith("| F-20261001-02") and "a \\| b" in lines[new]
    assert lines[-1] == "## Closed" and "Last intake: 2026-10-01" in out
    assert len(pc.parse_ledger(out)) == 3


def test_prose_sources_hold_last_intake(tmp_path, monkeypatch):
    rep = tmp_path / "reports"
    rep.mkdir()
    (rep / "pmo-audit-2026-10-20.md").write_text("x")
    (rep / "pmo-audit-2026-09-01.md").write_text("x")
    monkeypatch.setattr(pc, "REPORTS", rep)
    monkeypatch.setattr(pc, "VAULT", tmp_path)
    assert ti.prose_sources("2026-10-01", "2026-10-30") == ["reports/pmo-audit-2026-10-20.md"]


def test_apply_with_prose_keeps_last_intake(tmp_path, monkeypatch, fake_cmd):
    ledger, out = setup_main(tmp_path, monkeypatch, fake_cmd, LEDGER, {})
    rep = tmp_path / "empty"
    rep.mkdir()
    (rep / "metrics-2026-10-20.md").write_text("x")
    _, data = run_main(ledger, out, "--no-verify", "--apply")
    assert data["prose_sources"] == ["empty/metrics-2026-10-20.md"] and data["skip_model"] is True
    assert "Last intake: 2026-10-01 (TIRE)" in ledger.read_text()


@pytest.mark.parametrize("text,want",
                         [("Last intake: 2026-10-28 (TIRE)", "2026-10-28"), ("", None)])
def test_parse_last_intake(text, want):
    assert ti.parse_last_intake(text) == want
