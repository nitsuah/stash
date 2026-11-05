import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("check-generated-diff.py")


def git(repo, *args):
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def repo_with_base(tmp_path, files=None):
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Test")
    git(repo, "config", "user.email", "test@example.com")
    for name, content in (files or {"README.md": "base\n"}).items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "base")
    return repo, git(repo, "rev-parse", "HEAD")


def commit(repo):
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "change")
    return git(repo, "rev-parse", "HEAD")


def run_gate(repo, base, head):
    return subprocess.run(
        [sys.executable, str(SCRIPT), base, head], cwd=repo, capture_output=True,
        text=True,
    )


def test_accepts_dated_routine_note(tmp_path):
    repo, base = repo_with_base(tmp_path)
    path = repo / "agent/notes/2026-11-05.md"
    path.parent.mkdir(parents=True)
    path.write_text("# Daily note\n", encoding="utf-8")
    assert run_gate(repo, base, commit(repo)).returncode == 0


def test_accepts_generated_nav_and_vault_links_only(tmp_path):
    repo, base = repo_with_base(
        tmp_path, {"projects/demo.md": "---\ntitle: Demo\n---\nContext.\n"}
    )
    path = repo / "projects/demo.md"
    path.write_text(
        "---\ntitle: Demo\nkind: project\nrepo: demo\ndate: 2026-11-05\n---\n"
        "Context.\n> 🧭 [[prev]] · [[next]] <!-- nav -->\n"
        "<!-- vault-links:start -->\n- [[README]]\n<!-- vault-links:end -->\n",
        encoding="utf-8",
    )
    result = run_gate(repo, base, commit(repo))
    assert result.returncode == 0
    assert "ok: every change is routine-owned" in result.stdout


def test_rejects_hand_edit_outside_generated_blocks(tmp_path):
    repo, base = repo_with_base(tmp_path, {"docs/guide.md": "Keep this.\n"})
    (repo / "docs/guide.md").write_text(
        "Keep this.\nManual edit.\n", encoding="utf-8"
    )
    result = run_gate(repo, base, commit(repo))
    assert result.returncode == 1
    assert "hand edits outside generated" in result.stdout


def test_rejects_deleted_file(tmp_path):
    repo, base = repo_with_base(tmp_path, {"docs/guide.md": "Keep this.\n"})
    (repo / "docs/guide.md").unlink()
    result = run_gate(repo, base, commit(repo))
    assert result.returncode == 1 and "D docs/guide.md" in result.stdout
