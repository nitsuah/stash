"""Credential-leak checks for enrich-mirror.py: a token in a repo's origin URL must never
reach the mirrored docs (stash is public). Runs the script end to end on a throwaway repo."""
import pathlib
import subprocess
import sys

import pytest

SCRIPT = pathlib.Path(__file__).with_name("enrich-mirror.py")
FAKE_TOKEN = "not-a-real-token"


def run(tmp_path, origin):
    src, dest = tmp_path / "src", tmp_path / "dest"
    dest.mkdir()
    subprocess.run(["git", "init", "-q", str(src)], check=True)
    subprocess.run(["git", "-C", str(src), "remote", "add", "origin", origin], check=True)
    (dest / "README.md").write_text("# Demo\n\nSee [license](LICENSE).\n", encoding="utf-8")
    proc = subprocess.run([sys.executable, str(SCRIPT), str(src), str(dest), "demo"],
                          capture_output=True, text=True)
    return proc, (dest / "README.md").read_text(encoding="utf-8")


@pytest.mark.parametrize("origin", [
    f"https://{FAKE_TOKEN}@github.com/nitsuah/demo.git",
    f"https://x-access-token:{FAKE_TOKEN}@github.com/nitsuah/demo",
    "git@github.com:nitsuah/demo.git",
    "ssh://git@github.com/nitsuah/demo.git",
    "https://github.com/nitsuah/demo.git",
])
def test_source_url_has_no_userinfo(tmp_path, origin):
    proc, out = run(tmp_path, origin)
    assert proc.returncode == 0, proc.stderr
    assert "source: https://github.com/nitsuah/demo" in out
    assert FAKE_TOKEN not in out and "@github.com" not in out


@pytest.mark.parametrize("origin", [
    f"https://{FAKE_TOKEN}@evil@example.com/demo.git",
    f"https://github.com?contact={FAKE_TOKEN}@example.com",  # '@' past the authority isn't userinfo
])
def test_refuses_unnormalizable_userinfo(tmp_path, origin):
    proc, out = run(tmp_path, origin)
    assert proc.returncode != 0
    assert FAKE_TOKEN not in proc.stdout + proc.stderr
    assert out == "# Demo\n\nSee [license](LICENSE).\n"
