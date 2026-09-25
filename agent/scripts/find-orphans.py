"""Find orphaned notes in the Obsidian vault (stash/agent).

An orphan is a note with no resolved links in either direction, which is what
Obsidian's graph view shows as an unconnected dot. Notes with outbound links but
no inbound links are reported separately as "unreferenced".

Links are resolved roughly the way Obsidian does:
  [[target]] / [[target|alias]] / [[target#heading]] / ![[embed]]
  [text](path.md) (relative to the note, then vault-relative)
  falling back to a unique basename match.

Usage (from anywhere):
  python stash/agent/scripts/find-orphans.py                 # summary by folder
  python stash/agent/scripts/find-orphans.py --list          # every orphan path
  python stash/agent/scripts/find-orphans.py --json out.json # machine-readable
  python stash/agent/scripts/find-orphans.py --under repos   # limit the report to a subtree

Written 2026-09-24 as prep for the obn orphan-detection routine; see
reports/pmo-ff-2026-09-24.md.
"""
import argparse
import json
import os
import re
from collections import Counter, defaultdict
from urllib.parse import unquote

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKIP_DIRS = {".obsidian", ".git", "node_modules", ".trash", "__pycache__"}

WIKI = re.compile(r"!?\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
INLINE = re.compile(r"(`+)[^`\n].*?\1")


def strip_code(text):
    """Drop fenced blocks (``` or ~~~, closed by the same char at >= the opening length) and inline code."""
    out, fence = [], None
    for line in text.splitlines():
        m = FENCE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)
                continue
            out.append(INLINE.sub("", line))
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence):
            fence = None
    return "\n".join(out)


def collect():
    notes = []
    for dp, dn, fn in os.walk(VAULT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f.lower().endswith(".md"):
                notes.append(os.path.relpath(os.path.join(dp, f), VAULT).replace(os.sep, "/"))
    return sorted(notes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--json")
    ap.add_argument("--under", default="")
    a = ap.parse_args()

    notes = collect()
    lower = {n.lower(): n for n in notes}
    noext = {n[:-3].lower(): n for n in notes}
    by_base = defaultdict(list)
    for n in notes:
        by_base[os.path.basename(n)[:-3].lower()].append(n)

    def resolve(src, target):
        t = unquote(target.split("#")[0].split("?")[0]).strip().rstrip("\\")
        if not t or re.match(r"^[a-z]+:", t, re.I):
            return None
        cands = []
        here = os.path.dirname(src)
        for base in (here, ""):
            p = os.path.normpath(os.path.join(base, t)).replace(os.sep, "/")
            if p == ".." or p.startswith("../"):
                continue  # resolves outside the vault
            cands += [p.lower(), (p + ".md").lower()]
        if not cands:
            return None
        for c in cands:
            if c in lower:
                return lower[c]
            if c in noext:
                return noext[c]
        hits = by_base.get(os.path.basename(t)[:-3].lower() if t.lower().endswith(".md")
                           else os.path.basename(t).lower(), [])
        return hits[0] if len(hits) == 1 else None

    out_links = defaultdict(set)
    in_links = defaultdict(set)
    for n in notes:
        try:
            text = open(os.path.join(VAULT, n), encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        text = strip_code(text)
        targets = WIKI.findall(text) + [m for m in MDLINK.findall(text) if m.lower().split("#")[0].endswith(".md") or "." not in os.path.basename(m.split("#")[0])]
        for t in targets:
            r = resolve(n, t)
            if r and r != n:
                out_links[n].add(r)
                in_links[r].add(n)

    under = a.under.replace("\\", "/").strip("/")
    scope = [n for n in notes if n == under or n.startswith(under + "/")] if under else notes
    orphans = [n for n in scope if not out_links[n] and not in_links[n]]
    unref = [n for n in scope if out_links[n] and not in_links[n]]

    def top(n):
        parts = n.split("/")
        return "/".join(parts[:2]) if parts[0] == "repos" and len(parts) > 2 else parts[0] if len(parts) > 1 else "(root)"

    print(f"vault: {VAULT}")
    print(f"notes: {len(scope)}  orphans (no links in or out): {len(orphans)}  "
          f"unreferenced (links out, none in): {len(unref)}")
    print("\norphans by folder:")
    for k, v in Counter(top(n) for n in orphans).most_common():
        print(f"  {v:4d}  {k}")
    if a.list:
        print("\norphans:")
        for n in orphans:
            print("  " + n)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"notes": len(scope), "orphans": orphans, "unreferenced": unref}, f, indent=2)


if __name__ == "__main__":
    main()
