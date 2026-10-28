"""app.json userIgnoreFilters and find-orphans.py IGNORED_RE must agree, and must never hide notes."""
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("find_orphans", os.path.join(HERE, "find-orphans.py"))
fo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fo)

with open(os.path.join(HERE, "..", ".obsidian", "app.json"), encoding="utf-8") as fh:
    FILTERS = [re.compile(f[1:-1]) for f in json.load(fh)["userIgnoreFilters"] if f.startswith("/") and f.endswith("/")]

HIDDEN = ["projects/MM/x/scan.mjs", "projects/MM/x/sub/a.json", "projects/MM/x/Dockerfile", "projects/MM/x/.gitignore",
          "projects/MM/tools-site/redirect-site/_redirects", "projects/MM/x/icon.png", "reports/sotu/sotu-data.json",
          "scripts/sotu-page.html", "scripts/vault-graph-gif.js"]
SHOWN = ["projects/MM", "projects/MM/x", "projects/MM/x/sub", "projects/MM/x/README.md", "projects/MM/x/sub/notes.md",
         "scripts/build-vault-indexes.py", "reports/eng-mini-fire-2026-10-28.md", "reports/sotu"]


def test_hidden_files_match_both_lists():
    for p in HIDDEN:
        assert fo.IGNORED_RE.search(p), p
        assert any(f.search(p) for f in FILTERS), p


def test_directories_and_notes_never_match():
    for p in SHOWN:
        assert not fo.IGNORED_RE.search(p), p
        assert not any(f.search(p) for f in FILTERS), p
