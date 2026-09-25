"""Suggest links for weakly connected vault notes from Smart Connections embeddings.

Suggest-only: it never edits a note. Smart Connections (the Obsidian plugin) keeps a
local embedding per note in .smart-env/multi/*.ajson; this ranks, for each note
outside the repo mirrors with at most one link in or out, the most similar notes it
isn't linked to yet. A human or the PMO audit reads the list and adds the links that
make sense, in the body where the dependency is, not as a "see also" dump.

Paths are listed as plain `code`, not [[wikilinks]]: a suggestion list must not
itself add edges to the graph.

Usage:  python agent/scripts/suggest-links.py            # print suggestions
        python agent/scripts/suggest-links.py --write    # also save reports/link-suggestions-<date>.md
Needs Obsidian to have embedded the vault at least once (Smart Connections runs in the app).
"""
import datetime as dt
import glob
import json
import math
import os
import re
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")  # the Windows console defaults to cp1252

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOP, MIN_SCORE, MAX_LINKS = 3, 0.80, 1


def embeddings():
    """{note path: vector} from the Smart Connections store (later lines win; null = deleted)."""
    vecs = {}
    line_re = re.compile(r'^"smart_sources:([^"]+)":\s*(null|\{.*\}),?\s*$')
    for f in glob.glob(os.path.join(VAULT, ".smart-env", "multi", "*.ajson")):
        for line in open(f, encoding="utf-8", errors="replace"):
            m = line_re.match(line.strip())
            if not m:
                continue
            path, raw = m.groups()
            if raw == "null":
                vecs.pop(path, None)
                continue
            try:
                models = json.loads(raw).get("embeddings") or {}
            except json.JSONDecodeError:
                continue
            vec = next((e.get("vec") for e in models.values() if e.get("vec")), None)
            if vec:
                norm = math.sqrt(sum(x * x for x in vec)) or 1.0
                vecs[path] = [x / norm for x in vec]
    return vecs


def link_map():
    out = os.path.join(tempfile.gettempdir(), "vault-links.json")
    subprocess.run([sys.executable, os.path.join(VAULT, "scripts", "find-orphans.py"), "--json", out],
                   capture_output=True)
    return json.load(open(out, encoding="utf-8"))["links"]


vecs, links = embeddings(), link_map()
native = [n for n in links if not re.match(r"^repos/[^/]+/", n)
          and not re.match(r"^(notes/\d{4}-|reports/)", n) and n in vecs]
weak = [n for n in native if len(links[n]) <= MAX_LINKS]
rows = []
for n in sorted(weak):
    near = sorted(((sum(a * b for a, b in zip(vecs[n], v)), m) for m, v in vecs.items()
                   if m != n and m not in links[n] and m in links), reverse=True)[:TOP]
    near = [(s, m) for s, m in near if s >= MIN_SCORE]
    if near:
        rows.append(f"- `{n}` → " + ", ".join(f"`{m}` ({s:.2f})" for s, m in near))

today = dt.date.today().isoformat()
body = [f"# link-suggestions — {today}", "",
        f"Weakly connected notes (≤{MAX_LINKS} link) outside the repo mirrors, with the most similar "
        f"notes they don't link to yet (Smart Connections embeddings, cosine ≥ {MIN_SCORE}). "
        "Suggestions only: add a link where the note actually depends on the other one, and ignore the rest.",
        "", f"{len(weak)} weakly connected note(s) checked, {len(rows)} with suggestions.", ""] + (rows or ["None this week."])
print("\n".join(body))
if "--write" in sys.argv:
    path = os.path.join(VAULT, "reports", f"link-suggestions-{today}.md")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(body) + "\n")
    print(f"\nwrote {os.path.relpath(path, VAULT)}")
