"""Shared helpers for the monthly routine pre-step scripts (tire_intake, pmo_prep, usage_gather).

The scripts replace data gathering that TIRE, PMO and USAGE used to do with a model. Everything
here is stdlib only. Subprocess calls go through `run_cmd` so tests can stub `gh` and `git`.
stash is PUBLIC: outputs hold repo names, counts, dates and public advisory IDs only.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
VAULT = SCRIPTS.parent
REPORTS = VAULT / "reports"
LEDGER = REPORTS / "findings-ledger.md"
CMD_TIMEOUT = 90


class GhError(Exception):
    """A gh or git call failed; the message is short and safe to print."""


def run_cmd(args: list[str], cwd: str | None = None, timeout: int = CMD_TIMEOUT):
    """Run a command and return the CompletedProcess. Never raises on a non-zero exit."""
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                              check=False, timeout=timeout)
    except (subprocess.TimeoutExpired, FileNotFoundError, NotADirectoryError) as exc:
        return subprocess.CompletedProcess(args, 124, "", type(exc).__name__)


def gh(args: list[str]) -> str:
    """Run `gh <args>` and return stdout, raising GhError on failure."""
    proc = run_cmd(["gh", *args])
    if proc.returncode != 0:
        raise GhError(f"gh {' '.join(args[:3])} failed: {(proc.stderr or '').strip()[:160]}")
    return proc.stdout


def gh_json(args: list[str]):
    out = gh(args)
    try:
        return json.loads(out) if out.strip() else []
    except json.JSONDecodeError as exc:
        raise GhError(f"gh {' '.join(args[:3])} returned invalid JSON") from exc


def git(path: str, *args: str) -> str:
    proc = run_cmd(["git", "-C", path, *args])
    if proc.returncode != 0:
        raise GhError(f"git {args[0]} failed: {(proc.stderr or '').strip()[:160]}")
    return proc.stdout


def load_script(filename: str):
    """Import a sibling script by file name (works for hyphenated names such as sotu.py's peers)."""
    spec = importlib.util.spec_from_file_location(
        re.sub(r"\W", "_", Path(filename).stem), SCRIPTS / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tracked_repos() -> list[dict]:
    """The Tracked table in scope.md (name, local path, owner/repo), parsed by sotu.py."""
    return load_script("sotu.py").tracked_repos()


def split_row(line: str) -> list[str] | None:
    """Split a markdown table row on unescaped pipes. None if the line is not a row."""
    line = line.rstrip("\n")
    if not line.startswith("|"):
        return None
    cells = re.split(r"(?<!\\)\|", line.strip())[1:-1]
    return [c.strip() for c in cells]


LEDGER_COLS = ["ID", "First seen", "Last seen", "Seen", "Source", "Repo", "Finding", "Class",
               "Status", "Link"]


def parse_ledger(text: str) -> list[dict]:
    """Rows of the findings ledger tables, each with its line index in `text.splitlines()`."""
    rows = []
    for idx, line in enumerate(text.splitlines()):
        cells = split_row(line)
        if not cells or len(cells) != len(LEDGER_COLS) or not cells[0].startswith("F-"):
            continue
        row = dict(zip(LEDGER_COLS, cells, strict=True))
        row["_line"] = idx
        rows.append(row)
    return rows


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def default_branch(full_name: str) -> str:
    data = gh_json(["repo", "view", full_name, "--json", "defaultBranchRef"])
    return (data.get("defaultBranchRef") or {}).get("name") or "main"
