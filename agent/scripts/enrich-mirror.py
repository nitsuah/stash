"""Enrich a freshly synced repo mirror (agent/repos/<repo>/) for the Obsidian graph.

Called by sync-repos.ps1 right after it exports a repo's committed .md files. It
runs on every sync, over bytes just exported from git, so its output is
deterministic and never drifts. Upstream files are never touched.

For every mirrored .md:
  1. Frontmatter `up: "[[repos/<repo>]]"`, `source: <GitHub URL>`, `kind: repo-doc`, `repo:`, merged into
     any upstream frontmatter (upstream keys win). Every mirrored doc then links
     to its repo hub. That makes each repo one cluster around a node named after
     the repo instead of a generic README, and a mirrored doc can't be orphaned.
  2. Relative links, and vault-style [[wikilinks]], to things the sync doesn't copy
     (LICENSE, images, .github/, folders) become GitHub URLs, so they still work and stop showing up as
     ghost nodes. Links between mirrored docs stay relative. Links that match
     nothing upstream are left as they are; fix-doc-links.py fixes those
     upstream.
  3. `#word` in prose (hex colours, web hashtags) is escaped with a backslash, so repo docs
     don't create tag nodes in the graph; the vault has no tags of its own.

Usage: python enrich-mirror.py <repo-clone> <mirror-dir> <repo-name>
"""
import os
import posixpath
import re
import subprocess
import sys
from urllib.parse import unquote

src, dest, repo = sys.argv[1:4]
MDLINK = re.compile(r"(!?\[(?:\\.|[^\]\\])*\]\()([^)\s]+)((?:\s+\"[^\"]*\")?\))")  # link text may hold \[ \]
WIKI = re.compile(r"(!?\[\[)([^\]|#]+)((?:#[^\]|]*)?(?:\|[^\]]*)?\]\])")
FENCE = re.compile(r"^\s*(```|~~~)")


def git(*args):
    return subprocess.run(["git", "-C", src, *args], capture_output=True, text=True,
                          encoding="utf-8").stdout.strip()


branch = git("rev-parse", "--abbrev-ref", "origin/HEAD").split("/", 1)[-1] or "main"
remote = re.sub(r"\.git$", "", git("remote", "get-url", "origin"))
remote = re.sub(r"^git@github\.com:", "https://github.com/", remote)
upstream = set(git("ls-tree", "-r", "--name-only", "origin/HEAD").splitlines())
updirs = {posixpath.dirname(f) for f in upstream}
for d in list(updirs):
    while d:
        updirs.add(d)
        d = posixpath.dirname(d)

mirrored = set()
for dp, _, fn in os.walk(dest):
    for f in fn:
        if f.endswith(".md"):
            mirrored.add(os.path.relpath(os.path.join(dp, f), dest).replace(os.sep, "/"))


TAG = re.compile(r"(^|[\s(])#([A-Za-z][\w/-]*)")


def untag(line):
    """Repo docs never mean Obsidian tags: `#ff4444` or `#DronePhotography` in prose would
    become tag nodes in the graph. Backslash-escape them outside headings, code and links."""
    if re.match(r"^\s*#{1,6}\s", line) or "](" in line and re.search(r"\]\([^)]*#", line):
        return line
    return TAG.sub(lambda m: m.group(1) + "\\#" + m.group(2), line)


def url(path, anchor=""):
    kind = "tree" if path in updirs else "blob"
    return f"{remote}/{kind}/{branch}/{path}" + (f"#{anchor}" if anchor else "")


def enrich(doc, text):
    here = posixpath.dirname(doc)

    def fix(m):
        target = m.group(2)
        if re.match(r"^([a-z][a-z0-9+.-]*:|#|<)", target, re.I):
            return m.group(0)
        path, _, anchor = target.partition("#")
        p = posixpath.normpath(unquote(path.lstrip("/")) if path.startswith("/")
                               else posixpath.join(here, unquote(path))).rstrip("/")
        if p in mirrored or p.startswith(".."):
            return m.group(0)
        if p in upstream or p in updirs:
            return m.group(1) + url(p, anchor) + m.group(3)
        return m.group(0)

    def fix_wiki(m):
        # vault-style [[farm.png]] / [[repos/<repo>/docs/x.html|x]] pointing at a file the mirror
        # doesn't carry (sync copies .md only): turn it into a Markdown link to GitHub
        t = m.group(2).strip().rstrip("\\")
        rel_t = t[len(f"repos/{repo}/"):] if t.lower().startswith(f"repos/{repo.lower()}/") else t
        if rel_t in upstream and not rel_t.endswith(".md"):
            p = rel_t
        else:
            hits = [f for f in upstream if posixpath.basename(f) == posixpath.basename(t) and not f.endswith(".md")]
            if len(hits) != 1:  # one upstream file with that name, even under a stale path (a renamed repo)
                return m.group(0)
            p = hits[0]
        label = m.group(3).split("|", 1)[1][:-2] if "|" in m.group(3) else posixpath.basename(p)
        bang = "!" if m.group(1).startswith("!") else ""
        return f"{bang}[{label}]({url(p)})"

    out, fenced = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            fenced = not fenced
            out.append(line)
            continue
        if fenced:
            out.append(line)
            continue
        parts = re.split(r"((?<!\[)`[^`]*`(?!\]))", line)  # a `code` span, but not [`link text`](...)
        out.append("".join(p if i % 2 else untag(WIKI.sub(fix_wiki, MDLINK.sub(fix, p))) for i, p in enumerate(parts)))
    body = "\n".join(out)

    ours = {"up": f'"[[repos/{repo}]]"', "source": url(doc), "kind": "repo-doc", "repo": repo}
    m = re.match(r"^---\n(.*?)\n---\n", body, re.S)
    if m:
        keys = {l.split(":", 1)[0].strip() for l in m.group(1).split("\n") if ":" in l}
        extra = [f"{k}: {v}" for k, v in ours.items() if k not in keys]
        return f"---\n{m.group(1)}\n" + "".join(e + "\n" for e in extra) + "---\n" + body[m.end():]
    return "---\n" + "".join(f"{k}: {v}\n" for k, v in ours.items()) + "---\n\n" + body


changed = 0
for doc in sorted(mirrored):
    path = os.path.join(dest, *doc.split("/"))
    raw = open(path, encoding="utf-8", errors="replace").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n")
    new = enrich(doc, text)  # idempotent: existing keys are kept, GitHub URLs aren't rewritten again
    if new != text:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(new.replace("\n", nl))
        changed += 1
print(f"  [enrich] {changed} of {len(mirrored)} mirrored doc(s) given hub frontmatter / GitHub links")
