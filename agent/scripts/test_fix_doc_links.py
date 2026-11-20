"""fix-doc-links.py and enrich-mirror.py must not write through symlinks."""
import os
import pathlib
import subprocess
import sys

import pytest

HERE = pathlib.Path(__file__).parent
pytestmark = pytest.mark.skipif(not hasattr(os, "symlink") or os.name == "nt", reason="needs POSIX symlinks")


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.com", *args],
                   check=True, capture_output=True)


def test_fix_doc_links_skips_symlinked_doc(tmp_path):
    repo, outside = tmp_path / "repo", tmp_path / "outside.md"
    (repo / "docs").mkdir(parents=True)
    outside.write_text("[x](sub/guide.md)\n", encoding="utf-8")
    (repo / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
    (repo / "docs" / "a.md").write_text("[g](guide.md)\n", encoding="utf-8")
    (repo / "README.md").write_text("[g](docs/guide.md)\n[b](guide.md)\n", encoding="utf-8")
    os.symlink(outside, repo / "docs" / "link.md")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "x")
    proc = subprocess.run([sys.executable, str(HERE / "fix-doc-links.py"), str(repo), "--write"],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert outside.read_text(encoding="utf-8") == "[x](sub/guide.md)\n"
    assert (repo / "README.md").read_text(encoding="utf-8") == "[g](docs/guide.md)\n[b](./docs/guide.md)\n"
    assert (repo / "docs" / "link.md").is_symlink()


def test_enrich_mirror_skips_symlinked_doc(tmp_path):
    src, dest, outside = tmp_path / "src", tmp_path / "dest", tmp_path / "outside.md"
    dest.mkdir()
    subprocess.run(["git", "init", "-q", str(src)], check=True)
    subprocess.run(["git", "-C", str(src), "remote", "add", "origin", "https://github.com/nitsuah/demo.git"], check=True)
    outside.write_text("# Outside\n", encoding="utf-8")
    (dest / "README.md").write_text("# Demo\n", encoding="utf-8")
    os.symlink(outside, dest / "LINK.md")
    proc = subprocess.run([sys.executable, str(HERE / "enrich-mirror.py"), str(src), str(dest), "demo"],
                          capture_output=True, text=True)
    assert proc.returncode == 0, proc.stderr
    assert outside.read_text(encoding="utf-8") == "# Outside\n"
    assert (dest / "LINK.md").is_symlink()
    assert (dest / "README.md").read_text(encoding="utf-8").startswith("---\n")
