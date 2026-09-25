"""Gate for auto-merging routine PRs in stash: is every change routine-owned?

Passes a file when it is
  - a dated note (agent/notes/YYYY-MM-DD.md or YYYY-Www.md) or under agent/repos/, or
  - any other .md whose only differences are build-vault-indexes.py output: `<!-- nav -->`
    lines and `<!-- vault-links:start/end -->` blocks (including a new folder-hub stub).
Anything else (a hand edit riding along, a deletion, a non-.md file) fails the gate.

Usage (from the stash repo root):
  python agent/scripts/check-generated-diff.py <base-ref> <head-ref>
  e.g. git fetch origin pull/<N>/head && python agent/scripts/check-generated-diff.py origin/main FETCH_HEAD
Exit 0 = every file is routine-owned; exit 1 prints the files that are not.
"""
import re
import subprocess
import sys

ROUTINE_PATHS = re.compile(r"^agent/notes/\d{4}-(\d{2}-\d{2}|W\d{2})\.md$|^agent/repos/")
BLOCK = re.compile(r"\n*<!-- vault-links:start -->.*?<!-- vault-links:end -->\n*", re.S)
STUB = re.compile(r"^# [^\n]+\nFolder hub for `projects/[^`]+/`\. Add context above the generated block\.$")


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8").stdout


def show(ref, path):
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True, encoding="utf-8")
    return r.stdout if r.returncode == 0 else None


def strip(text):
    """Content minus generated text; blank lines are ignored (the generator pads around what it inserts)."""
    text = BLOCK.sub("\n", text.replace("\r\n", "\n"))
    return "\n".join(l.rstrip() for l in text.split("\n") if l.strip() and "<!-- nav -->" not in l)


base, head = sys.argv[1], sys.argv[2]
bad = []
for line in git("diff", "--name-status", f"{base}...{head}").splitlines():
    status, path = line.split("\t")[0], line.split("\t")[-1]
    if ROUTINE_PATHS.match(path):
        continue
    if status.startswith("D") or not path.endswith(".md"):
        bad.append(f"{status} {path}")
        continue
    old, new = show(base, path), strip(show(head, path) or "")
    if old is None:
        if not STUB.match(new):
            bad.append(f"{status} {path} (new file, not a folder-hub stub)")
    elif strip(old) != new:
        bad.append(f"{status} {path} (hand edits outside generated nav/blocks)")

if bad:
    print("not routine-owned:")
    for b in bad:
        print("  " + b)
    sys.exit(1)
print("ok: every change is routine-owned")
