"""Check every tracked repo's TASKS.md against the parser-safe format vigil reads.

Uses sotu.py's parser (same rules as vigil), so what this flags is what vigil misses:
  - no TASKS.md (root or docs/) on the default branch
  - missing the Done / In Progress / Todo sections
  - open items with no priority (no `- Priority: Pn` sub-bullet, inline [Pn] tag or Pn heading)
  - checkboxes vigil skips: indented more than one space, or `*`/`+` bullets instead of `-`

Reads only origin's default branch, never local HEAD (run `git fetch` first, or pass --fetch). Prints a markdown
report for the PMO audit; --check exits 1 when anything is flagged.
"""
import argparse
import re
import sys
from collections import defaultdict

import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("sotu", Path(__file__).with_name("sotu.py"))
sotu = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sotu)

SECTIONS = ("done", "in progress", "todo")
SKIPPED = re.compile(r"^(?:\s{2,}- |\s*[*+] )\[( |/|x)\]\s+", re.I)


def default_ref(path: str) -> str | None:
    """The remote default branch only; never local HEAD, so the audit can't report an unpushed file."""
    for ref in ("origin/HEAD", "origin/main", "origin/master"):
        try:
            sotu.git(path, "rev-parse", "--verify", "-q", ref)
            return ref
        except (sotu.subprocess.CalledProcessError, FileNotFoundError, sotu.subprocess.TimeoutExpired):
            continue
    return None


def check(repo: dict) -> dict:
    ref = default_ref(repo["path"])
    if not ref:
        return {"repo": repo["repo"], "missing": True, "why": "no remote default branch (clone missing or never fetched?)"}
    text = rel = None
    for candidate in ("TASKS.md", "docs/TASKS.md"):
        try:
            text = sotu.git(repo["path"], "show", f"{ref}:{candidate}")
        except sotu.subprocess.CalledProcessError:
            continue  # not on the default branch
        except sotu.subprocess.TimeoutExpired:
            return {"repo": repo["repo"], "missing": True, "why": f"git show timed out on {ref}"}
        rel = candidate
        break
    if not text:
        return {"repo": repo["repo"], "missing": True, "why": f"no TASKS.md on {ref}"}
    headings = {m.group(1).strip().lower() for m in re.finditer(r"^##\s+(.*)", text, re.M)}
    missing_sections = [s for s in SECTIONS if not any(h.startswith(s) for h in headings)]
    tasks = sotu.parse_tasks(text, repo["repo"], rel)
    no_prio = [t for t in tasks if not t["priority"]]
    skipped = [f"{rel}:{n}" for n, line in enumerate(text.splitlines(), 1) if SKIPPED.match(line)]
    return {"repo": repo["repo"], "missing": False, "rel": rel, "items": len(tasks),
            "missing_sections": missing_sections, "no_prio": no_prio, "skipped": skipped}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fetch", action="store_true", help="git fetch each tracked repo first")
    ap.add_argument("--check", action="store_true", help="exit 1 if any repo is flagged")
    ap.add_argument("--details", action="store_true", help="list every flagged item, not just counts")
    a = ap.parse_args()

    repos = sotu.tracked_repos()
    if a.fetch:
        sotu.fetch_all(repos)
    results = [check(r) for r in repos]

    flagged = 0
    print("| Repo | File | Open items | No priority | Skipped by parser | Missing sections |")
    print("|------|------|-----------:|------------:|------------------:|------------------|")
    for r in results:
        if r["missing"]:
            flagged += 1
            print(f"| {r['repo']} | none | - | - | - | {r['why']} |")
            continue
        bad = r["no_prio"] or r["skipped"] or r["missing_sections"]
        flagged += bool(bad)
        print(f"| {r['repo']} | {r['rel']} | {r['items']} | {len(r['no_prio'])} | {len(r['skipped'])} | "
              f"{', '.join(r['missing_sections']) or '-'} |")
    if a.details:
        for r in results:
            if r["missing"] or not (r["no_prio"] or r["skipped"]):
                continue
            print(f"\n**{r['repo']}**")
            for t in r["no_prio"]:
                print(f"- no priority: {t['ref']} {t['title'][:90]}")
            for ref in r["skipped"]:
                print(f"- skipped checkbox: {ref}")
    print(f"\n{flagged} of {len(results)} repos flagged.")
    return 1 if a.check and flagged else 0


if __name__ == "__main__":
    sys.exit(main())
