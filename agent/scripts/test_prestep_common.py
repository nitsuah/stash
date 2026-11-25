"""pytest coverage for agent/scripts/prestep_common.py."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prestep_common as pc


class TestSplitRow:
    def test_escaped_pipe_does_not_split(self):
        assert pc.split_row("| a | b \\| c | d |") == ["a", "b \\| c", "d"]

    def test_not_a_row_returns_none(self):
        assert pc.split_row("not a row") is None

    def test_trailing_newline_tolerated(self):
        assert pc.split_row("| a | b |\n") == ["a", "b"]

    def test_empty_row(self):
        assert pc.split_row("||") == [""]


class TestWriteJson:
    def test_creates_parent_dir_keeps_key_order_newline_and_roundtrip(self, tmp_path):
        target = tmp_path / "sub" / "x.json"
        data = {"b": 1, "a": [1]}
        pc.write_json(target, data)
        text = target.read_text(encoding="utf-8")
        assert text.endswith("\n")
        assert json.loads(text) == data
        # key order preserved: b before a
        assert text.index('"b"') < text.index('"a"')


class TestRunCmd:
    def test_file_not_found_returns_124(self, monkeypatch):
        def raise_fnf(*args, **kwargs):
            raise FileNotFoundError("no such file")

        monkeypatch.setattr(pc.subprocess, "run", raise_fnf)
        result = pc.run_cmd(["does-not-exist"])
        assert result.returncode == 124
        assert "FileNotFoundError" in result.stderr

    def test_timeout_expired_returns_124(self, monkeypatch):
        def raise_timeout(*args, **kwargs):
            raise subprocess.TimeoutExpired(cmd="sleep", timeout=1)

        monkeypatch.setattr(pc.subprocess, "run", raise_timeout)
        result = pc.run_cmd(["sleep", "10"])
        assert result.returncode == 124
        assert "TimeoutExpired" in result.stderr


class TestGh:
    def test_success_returns_stdout(self, fake_cmd):
        fake_cmd.on("repo", stdout="OUT")
        assert pc.gh(["repo", "view", "x"]) == "OUT"

    def test_failure_raises_gh_error_with_message(self, fake_cmd):
        fake_cmd.on("repo", rc=1, stderr="boom")
        with pytest.raises(pc.GhError) as exc:
            pc.gh(["repo", "view", "x"])
        assert "gh repo view x failed: boom" in str(exc.value)


class TestGhJson:
    def test_data_returns_dict(self, fake_cmd):
        fake_cmd.on("repo", data={"a": 1})
        assert pc.gh_json(["repo", "view", "x"]) == {"a": 1}

    def test_empty_stdout_returns_empty_list(self, fake_cmd):
        fake_cmd.on("repo", stdout="")
        assert pc.gh_json(["repo", "view", "x"]) == []

    def test_invalid_json_raises_gh_error(self, fake_cmd):
        fake_cmd.on("repo", stdout="{not json")
        with pytest.raises(pc.GhError) as exc:
            pc.gh_json(["repo", "view", "x"])
        assert "invalid JSON" in str(exc.value)


class TestGit:
    def test_success_returns_stdout_and_records_argv(self, fake_cmd):
        fake_cmd.on("status", stdout="clean")
        out = pc.git("/p", "status")
        assert out == "clean"
        assert fake_cmd.calls[0][:4] == ["git", "-C", "/p", "status"]

    def test_failure_raises_gh_error(self, fake_cmd):
        fake_cmd.on("status", rc=128, stderr="not a repo")
        with pytest.raises(pc.GhError) as exc:
            pc.git("/p", "status")
        assert "git status failed" in str(exc.value)


class TestDefaultBranch:
    def test_trunk_when_name_present(self, fake_cmd):
        fake_cmd.on("repo", data={"defaultBranchRef": {"name": "trunk"}})
        assert pc.default_branch("o/r") == "trunk"

    def test_main_when_default_branch_ref_none(self, fake_cmd):
        fake_cmd.on("repo", data={"defaultBranchRef": None})
        assert pc.default_branch("o/r") == "main"

    def test_main_when_empty_object(self, fake_cmd):
        fake_cmd.on("repo", data={})
        assert pc.default_branch("o/r") == "main"
