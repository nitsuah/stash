"""Find and repair broken relative links between docs, in a repo or in this vault.

Repo mode (default), from any repo:
    python <stash>/agent/scripts/fix-doc-links.py <repo-dir>            # report only
    python <stash>/agent/scripts/fix-doc-links.py <repo-dir> --write    # repair in place
  Checks every committed .md's relative Markdown links `[text](path)` and `![alt](path)`
  against the committed tree. A broken link is repaired only when exactly one target is
  plausible:
    1. the same path read from the repo root (the usual bug: a doc moved into docs/ or
       docs/archive/ but kept root-relative links), else
    2. the same path minus leading ../ (the doc moved a folder deeper), else
    3. the one committed file in the repo with that file name.
  Anything else is reported and left alone; never guessed. Code spans and fences are skipped.
  --unlink-dead-archive also turns unrepairable links in */archive/* docs into plain
  text. Archived docs are history, so their references to deleted files are expected.
  --unlink-dead goes further: any link (or Obsidian [[wikilink]]) whose target exists nowhere
  in the repo becomes plain text (a missing image becomes its alt text). Use it once a human
  has looked at the report and agreed the targets are really gone.

Vault mode, for notes written in this vault (skips the repos/<repo>/ mirrors, which are
fixed upstream and re-synced):
    python agent/scripts/fix-doc-links.py --vault [--write]
  Repairs `[[path]]` wikilinks whose target moved: the one note with the same name under
  the deepest folder of the old path that still exists (repos/avatar/ROADMAP ->
  repos/avatar/docs/ROADMAP).
  --unlink-dead-mirrors also turns links into repos/... that match nothing (a deleted
  repo or an archived doc) into plain text: `[[repos/x/doc|Doc]]` -> `Doc`. Only mirror
  paths qualify, because nobody hand-creates a note there later.
  --under=repos/ limits vault mode to notes under a prefix (the daily routine fixes only
  its own repo hubs).

Idempotent: a second run finds nothing. Run by the PMO audit next to repo-breadcrumbs.py.
"""
import os
import posixpath
import re
import subprocess
import sys
from collections import defaultdict
from urllib.parse import unquote

WRITE = "--write" in sys.argv
UNLINK = "--unlink-dead-mirrors" in sys.argv or "--unlink-dead-archive" in sys.argv
UNLINK_ALL = "--unlink-dead" in sys.argv
UNDER = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--under=")), "")  # vault mode: only notes under this prefix
MDLINK = re.compile(r"(!?\[(?:\\.|[^\]\\])*\]\()([^)\s]+)((?:\s+\"[^\"]*\")?\))")  # link text may hold \[ \]
WIKI = re.compile(r"(!?\[\[)([^\]|#]+)((?:#[^\]|]*)?(?:\|[^\]]*)?\]\])")
FENCE = re.compile(r"^\s*(```|~~~)")


def rel(frm_dir, target):
    r = posixpath.relpath(target, frm_dir or ".")
    return r if r.startswith("../") else "./" + r


def rewrite(text, fix_line):
    """Apply fix_line to prose only: skip fenced blocks and `code spans`."""
    out, fenced = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            fenced = not fenced
        if fenced or FENCE.match(line):
            out.append(line)
            continue
        parts = re.split(r"((?<!\[)`[^`]*`(?!\]))", line)  # a `code` span, but not [`link text`](...)
        out.append("".join(p if i % 2 else fix_line(p) for i, p in enumerate(parts)))
    return "\n".join(out)


def save(path, text, new, nl):
    if new != text and WRITE:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new.replace("\n", nl))


def load(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    return raw.replace("\r\n", "\n"), "\r\n" if "\r\n" in raw else "\n"


def repo_mode(repo):
    files = subprocess.run(["git", "-C", repo, "ls-files"], capture_output=True, text=True,
                           encoding="utf-8").stdout.splitlines()
    exists = set(files)
    dirs = {posixpath.dirname(f) for f in files}
    while "" in dirs:
        dirs.discard("")
    for d in list(dirs):
        while d:
            dirs.add(d)
            d = posixpath.dirname(d)
    by_name = defaultdict(list)
    for f in files:
        by_name[posixpath.basename(f).lower()].append(f)
    fixed, unfixable = 0, []
    # repo docs may carry vault-style [[repos/<repo>]] links; those resolve in the vault mirror
    vault = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    vault_notes = set()
    for dp, dn, fn in os.walk(vault):
        dn[:] = [d for d in dn if not d.startswith(".")]
        vault_notes |= {os.path.relpath(os.path.join(dp, f), vault).replace(os.sep, "/")[:-3].lower()
                        for f in fn if f.endswith(".md")}

    # same set sync-repos.ps1 mirrors: .github/ and a root templates/ are repo config, not docs
    for doc in (f for f in files if f.lower().endswith(".md")
                and not re.search(r"(^|/)\.github/|^templates/|(^|/)node_modules/", f)
                and not (os.path.basename(repo) == "stash" and f.startswith("agent/"))):  # the vault: use --vault
        here = posixpath.dirname(doc)
        found = []

        def fix(m):
            nonlocal fixed
            target = m.group(2)
            if re.match(r"^([a-z][a-z0-9+.-]*:|#|<|/)", target, re.I):
                return m.group(0)
            path, _, anchor = target.partition("#")
            p = posixpath.normpath(posixpath.join(here, unquote(path))).rstrip("/")
            if p in exists or p in dirs or not path:
                return m.group(0)
            root = posixpath.normpath(unquote(path)).rstrip("/")
            # ../README.md written before the doc moved a folder deeper: try it from the repo root
            unup = re.sub(r"^(\.\./)+", "", root)
            if (root in exists or root in dirs) and not root.startswith(".."):
                cands = [root]
            elif unup != root and (unup in exists or unup in dirs):
                cands = [unup]
            else:
                cands = by_name.get(posixpath.basename(root).lower(), [])
            if len(cands) != 1:
                if (UNLINK and "/archive/" in "/" + doc) or (UNLINK_ALL and not cands):
                    # keep the words, drop a link to something that doesn't exist anywhere in the repo
                    fixed += 1
                    text = m.group(1)[m.group(1).index("[") + 1:-2]
                    return text if not m.group(1).startswith("!") else (text or f"`{path}`") + " (image not in repo)"
                found.append(target)
                return m.group(0)
            fixed += 1
            new = rel(here, cands[0]) + (("#" + anchor) if anchor else "")
            return m.group(1) + new + m.group(3)

        def fix_wiki(m):
            # Obsidian-style [[links]] in repo docs: GitHub never renders them, so only dead ones matter
            nonlocal fixed
            t = m.group(2).strip().rstrip("\\")
            stem = t[:-3] if t.lower().endswith(".md") else t
            if stem.lower() in vault_notes or (stem + ".md") in exists or t in exists \
                    or posixpath.basename(stem).lower() + ".md" in by_name \
                    or posixpath.basename(t).lower() in by_name:
                return m.group(0)
            if not UNLINK_ALL:
                found.append(t)
                return m.group(0)
            fixed += 1
            alias = m.group(3).split("|", 1)[1][:-2] if "|" in m.group(3) else None
            return alias or f"`{t}`"

        text, nl = load(os.path.join(repo, doc))
        new = rewrite(text, lambda s: WIKI.sub(fix_wiki, MDLINK.sub(fix, s)))
        save(os.path.join(repo, doc), text, new, nl)
        unfixable += [f"{doc}: {t}" for t in found]
    return fixed, unfixable


def vault_mode(vault):
    notes = []
    for dp, dn, fn in os.walk(vault):
        dn[:] = [d for d in dn if not d.startswith(".")]
        notes += [os.path.relpath(os.path.join(dp, f), vault).replace(os.sep, "/")[:-3]
                  for f in fn if f.endswith(".md")]
    lower = {n.lower() for n in notes}
    by_name = defaultdict(list)
    for n in notes:
        by_name[posixpath.basename(n).lower()].append(n)
    fixed, unfixable = 0, []
    for note in notes:
        if re.match(r"^repos/[^/]+/", note):
            continue  # mirrors: fix upstream
        if UNDER and not note.startswith(UNDER):
            continue
        found = []

        def fix(m):
            nonlocal fixed
            t = m.group(2).strip().rstrip("\\")
            t = t[:-3] if t.lower().endswith(".md") else t
            name = posixpath.basename(t).lower()
            if t.lower() in lower or ("/" not in t and name in by_name) or "." in posixpath.basename(t):
                return m.group(0)  # resolves, or an attachment (not a note)
            base = posixpath.dirname(t)
            while base and not any(n.lower().startswith(base.lower() + "/") for n in notes):
                base = posixpath.dirname(base)
            cands = [n for n in by_name.get(name, []) if not base or n.lower().startswith(base.lower() + "/")]
            repo = t.lower().split("/")[1] if t.lower().startswith("repos/") and "/" in t else None
            if repo and f"repos/{repo}" not in lower and not any(n.lower().startswith(f"repos/{repo}/") for n in notes):
                cands = []  # the whole repo is gone (e.g. motor-pool): a same-named doc elsewhere isn't it
            if not cands and UNLINK and t.lower().startswith("repos/"):
                # a mirror doc (or repo) that no longer exists: keep the words, drop the ghost node
                fixed += 1
                alias = m.group(3).split("|", 1)[1][:-2] if "|" in m.group(3) else None
                return alias or f"`{t}`"
            if not base or len(cands) != 1:
                found.append(m.group(2))
                return m.group(0)
            fixed += 1
            escaped = "\\" if m.group(2).endswith("\\") else ""  # [[x\|alias]] inside a table
            return m.group(1) + cands[0] + escaped + m.group(3)

        path = os.path.join(vault, note + ".md")
        text, nl = load(path)
        new = rewrite(text, lambda s: WIKI.sub(fix, s))
        save(path, text, new, nl)
        unfixable += [f"{note}.md: {t}" for t in found]
    return fixed, unfixable


if "--vault" in sys.argv:
    fixed, unfixable = vault_mode(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
else:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    fixed, unfixable = repo_mode(os.path.abspath(args[0] if args else "."))
print(f"{'fixed' if WRITE else 'fixable'}: {fixed}  unfixable (left alone): {len(unfixable)}")
for u in unfixable:
    print("  " + u)
