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
import sys
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
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if a note outside the repos/<repo>/ mirrors is orphaned or unreachable, or "
                         "two notes outside the mirrors share a name (an ambiguous [[wikilink]])")
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
    unresolved = defaultdict(set)  # note -> link targets that match no note (ghost nodes in the graph)
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
            elif r is None and t.split("#")[0].strip() and not re.match(r"^[a-z]+:", t, re.I):
                unresolved[n].add(t.split("#")[0].strip())

    under = a.under.replace("\\", "/").strip("/")
    scope = [n for n in notes if n == under or n.startswith(under + "/")] if under else notes
    orphans = [n for n in scope if not out_links[n] and not in_links[n]]
    unref = [n for n in scope if out_links[n] and not in_links[n]]

    # agents navigate top-down: how many notes can they reach from the vault home (VAULT-MAP) by following links?
    root = "VAULT-MAP.md" if "VAULT-MAP.md" in out_links else "AGENT-MAIN.md"
    depth = {root: 0} if root in out_links else {}
    frontier = list(depth)
    while frontier:
        nxt = []
        for n in frontier:
            for t in out_links[n]:
                if t not in depth:
                    depth[t] = depth[n] + 1
                    nxt.append(t)
        frontier = nxt
    unreachable = [n for n in scope if n not in depth]
    stars = sorted(((len(out_links[n]), n) for n in scope if len(out_links[n]) >= 40), reverse=True)

    def top(n):
        parts = n.split("/")
        return "/".join(parts[:2]) if parts[0] == "repos" and len(parts) > 2 else parts[0] if len(parts) > 1 else "(root)"

    print(f"vault: {VAULT}")
    print(f"notes: {len(scope)}  orphans (no links in or out): {len(orphans)}  "
          f"unreferenced (links out, none in): {len(unref)}")
    hops = Counter(min(d, 4) for n, d in depth.items() if n in scope)
    print(f"reachable from {root[:-3]}: {len(scope) - len(unreachable)}  unreachable: {len(unreachable)}  "
          "by hops: " + ", ".join(f"{'4+' if k == 4 else k}:{v}" for k, v in sorted(hops.items())))
    if stars:
        print("star hubs (40+ out-links): " + ", ".join(f"{n} ({c})" for c, n in stars))
    broken = {n: sorted(unresolved[n]) for n in scope if unresolved[n]}
    print(f"unresolved links (ghost nodes): {sum(len(v) for v in broken.values())} in {len(broken)} notes")
    print("\norphans by folder:")
    for k, v in Counter(top(n) for n in orphans).most_common():
        print(f"  {v:4d}  {k}")
    if broken:
        print("\nunresolved links by folder:")
        for k, v in Counter(top(n) for n, ts in broken.items() for _ in ts).most_common():
            print(f"  {v:4d}  {k}")
    if a.list:
        print("\nunresolved links:")
        for n, ts in broken.items():
            print(f"  {n}: " + ", ".join(ts))
        print("\norphans:")
        for n in orphans:
            print("  " + n)
        print("\nunreferenced:")
        for n in unref:
            print("  " + n)
        print("\nunreachable from the vault home (outside repo mirrors):")
        for n in unreachable:
            if not re.match(r"^repos/[^/]+/", n):
                print("  " + n)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"notes": len(scope), "orphans": orphans, "unreferenced": unref,
                       "unreachable": unreachable, "unresolved": broken}, f, indent=2)
    if a.check:
        native = [n for n in notes if not re.match(r"^repos/[^/]+/", n)]
        bad = sorted({n for n in orphans + unreachable if n in native})
        names = defaultdict(list)
        for n in native:
            names[os.path.basename(n).lower()].append(n)
        dupes = {k: v for k, v in names.items() if len(v) > 1}
        if bad:
            print(f"\nFAIL: {len(bad)} note(s) outside the repo mirrors have no path from the vault home:")
            for n in bad:
                print("  " + n)
        if dupes:
            print(f"\nFAIL: {len(dupes)} name(s) shared by notes outside the repo mirrors "
                  "(a bare [[name]] is ambiguous and the graph shows look-alike nodes); rename one:")
            for v in dupes.values():
                print("  " + " · ".join(v))
        if bad or dupes:
            sys.exit(1)


if __name__ == "__main__":
    main()
