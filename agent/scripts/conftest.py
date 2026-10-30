"""Make the sibling pre-step modules importable and give their tests a stubbed gh/git."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import prestep_common as pc  # noqa: E402


@pytest.fixture
def fake_cmd(monkeypatch):
    """Stub `pc.run_cmd`. Register handlers with fake_cmd.on(*tokens, data=... or stdout=...).

    A handler matches when every token is in the command's argv; the newest handler wins.
    """
    class Fake:
        def __init__(self):
            self.handlers, self.calls = [], []

        def on(self, *tokens, stdout="", rc=0, stderr="", data=None):
            out = json.dumps(data) if data is not None else stdout
            self.handlers.append((tokens, out, rc, stderr))

        def __call__(self, args, cwd=None, timeout=0):
            self.calls.append(list(args))
            for tokens, out, rc, err in reversed(self.handlers):
                if all(t in args for t in tokens):
                    return subprocess.CompletedProcess(args, rc, out, err)
            return subprocess.CompletedProcess(args, 1, "", "no stub for " + " ".join(args[:3]))

    fake = Fake()
    monkeypatch.setattr(pc, "run_cmd", fake)
    return fake
