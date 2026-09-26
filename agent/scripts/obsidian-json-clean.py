"""Git clean filter for tracked Obsidian settings (agent/.obsidian/*.json).

Obsidian rewrites these files whenever the app is used: it drops the trailing
newline, and graph.json stores the graph view's current zoom and float jitter
from its force sliders. None of that is a real settings change, but it left
stash dirty on `main` day after day, so the daily repo sync skipped stash.

This filter normalizes what git sees (never the file on disk):
- JSON re-serialized with 2-space indent and a trailing newline;
- graph.json: view state (`scale`, `close`) pinned, force floats rounded.

Real edits (a new color group, a filter, a plugin toggle) still show up.

Setup, once per clone (the filter is attached in .gitattributes, but git only
runs filters defined in the local config; without it nothing breaks, the files
just show as modified again):

    git config filter.obsidian-json.clean "python agent/scripts/obsidian-json-clean.py %f"
    git config filter.obsidian-json.required false
"""

import json
import sys

GRAPH_PINNED = {"scale": 1, "close": True}


def normalize(text, path):
    try:
        data = json.loads(text)
    except ValueError:
        return text  # not JSON (or mid-write): pass through untouched
    if path.replace("\\", "/").endswith("/graph.json") and isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, float):
                data[key] = round(value, 3)
        for key, value in GRAPH_PINNED.items():
            if key in data:
                data[key] = value
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else ""
    text = sys.stdin.buffer.read().decode("utf-8-sig")
    sys.stdout.buffer.write(normalize(text, path).encode("utf-8"))


if __name__ == "__main__":
    main()
