"""Add idempotent breadcrumb nav lines + a README docs index to a repo.

Usage (from the repo root, on a fresh branch):
    python C:/Users/<user>/code/stash/agent/scripts/repo-breadcrumbs.py . <repo-name>

Re-run it whenever a repo gains, moves or removes docs (the monthly PMO audit does,
per prompts/PMO.md); it only changes files when something is actually new.

Links are relative markdown links with explicit ./ or ../ so they resolve on
GitHub and in the Obsidian mirror (stash/agent/repos/<repo>/, which keeps the
root + docs/ layout). Bare `TASKS.md` would be ambiguous across 17 repos in
the vault, so every link carries a path prefix.
"""
import os, re, subprocess, sys

CORE = ["FEATURES", "ROADMAP", "TASKS", "CHANGELOG", "METRICS"]
LABEL = {"FEATURES": "Features", "ROADMAP": "Roadmap", "TASKS": "Tasks",
         "CHANGELOG": "Changelog", "METRICS": "Metrics", "INDEX": "Index"}
NAV_TAG = "<!-- nav -->"
IDX_START, IDX_END = "<!-- docs-index:start -->", "<!-- docs-index:end -->"


def rel(frm_dir, target):
    r = os.path.relpath(target, frm_dir).replace(os.sep, "/")
    return r if r.startswith("../") else "./" + r


def read(p):
    with open(p, "rb") as f:
        raw = f.read().decode("utf-8").lstrip("﻿")
    nl = "\r\n" if "\r\n" in raw else "\n"
    return raw.replace("\r\n", "\n"), nl


def write(p, text, nl):
    with open(p, "wb") as f:
        f.write(text.replace("\n", nl).encode("utf-8"))


def title_of(p):
    text, _ = read(p)
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else os.path.splitext(os.path.basename(p))[0]


def insert_nav(text, nav):
    # also drop kryptos-style plain-text "Breadcrumb: Home > Docs > X" lines near the top
    raw = text.split("\n")
    lines = []
    for i, l in enumerate(raw):
        if NAV_TAG in l or (i < 12 and l.startswith("Breadcrumb:")):
            continue
        # a bare ">" spacer we added to join the nav with a following blockquote (MD028)
        if l.strip() == ">" and i > 0 and NAV_TAG in raw[i - 1]:
            continue
        lines.append(l)
    # collapse a blank line we may have left behind directly under the H1
    start = 0
    if lines and lines[0].strip() == "---":  # frontmatter
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 1
                break
    h1 = None
    in_code = False
    for i in range(start, min(len(lines), start + 40)):
        if lines[i].lstrip().startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"^#\s+\S", lines[i]):
            h1 = i
            break
    if h1 is None:
        rest = lines[start:]
        while rest and rest[0].strip() == "":
            rest = rest[1:]
        new = lines[:start] + [nav, ""] + rest
    else:
        after = lines[h1 + 1:]
        while after and after[0].strip() == "" and len(after) > 1 and after[1].strip() == "":
            after = after[1:]
        if after and after[0].strip() != "":
            after = [""] + after
        # nav directly above another blockquote: join them with ">" instead of a
        # blank line, which markdownlint flags as MD028
        if len(after) > 1 and after[0] == "" and after[1].startswith(">"):
            after = [">"] + after[1:]
        new = lines[:h1 + 1] + ["", nav] + after
    return "\n".join(new)


def main(repo_dir, repo_name):
    docs = os.path.join(repo_dir, "docs")
    core = {}
    for c in CORE + ["INDEX"]:
        for cand in (os.path.join(repo_dir, c + ".md"), os.path.join(docs, c + ".md")):
            if os.path.isfile(cand):
                core[c] = cand
                break
    readme = os.path.join(repo_dir, "README.md")

    def nav_for(path):
        d = os.path.dirname(path)
        parts = [f"[{repo_name}]({rel(d, readme)})" if path != readme else f"**{repo_name}**"]
        for c in ["INDEX"] + CORE:
            if c not in core:
                continue
            if os.path.normcase(core[c]) == os.path.normcase(path):
                parts.append(f"**{LABEL[c]}**")
            else:
                parts.append(f"[{LABEL[c]}]({rel(d, core[c])})")
        return "> 🧭 " + " · ".join(parts) + " " + NAV_TAG

    targets = []
    if os.path.isdir(docs):
        targets += [os.path.join(docs, f) for f in sorted(os.listdir(docs)) if f.lower().endswith(".md")]
        nested = []
        for dp, dn, fn in os.walk(docs):
            dn[:] = sorted(x for x in dn if x not in ("node_modules", ".git"))
            if dp == docs:
                continue
            nested += [os.path.join(dp, f) for f in sorted(fn) if f.lower().endswith(".md")]
        targets += nested
    targets += [p for p in core.values() if os.path.dirname(p) == repo_dir]
    # other root-level markdown (CLAUDE.md, AGENTS.md, CONTRIBUTING.md, ...)
    extra_root = [os.path.join(repo_dir, f) for f in sorted(os.listdir(repo_dir))
                  if f.lower().endswith(".md") and f != "README.md"
                  and os.path.join(repo_dir, f) not in targets]
    targets += extra_root

    # only docs committed in HEAD: never touch or index a user's untracked/staged-new file
    tracked = set(subprocess.run(["git", "-C", repo_dir, "ls-tree", "-r", "--name-only", "HEAD"],
                                 capture_output=True, text=True).stdout.splitlines())
    targets = [p for p in targets
               if os.path.relpath(p, repo_dir).replace(os.sep, "/") in tracked]

    # committed docs outside the repo root and docs/ (subfolder READMEs etc.): indexed
    # in the README so they aren't orphans, but no nav line is inserted into them.
    # Same exclusions as stash's sync-repos.ps1 (.github/, root templates/; for stash itself,
    # agent/ is the vault and links itself through VAULT-MAP).
    extras = [os.path.join(repo_dir, *t.split("/")) for t in sorted(tracked)
              if t.lower().endswith(".md") and "/" in t and not t.startswith("docs/")
              and not re.search(r"(^|/)\.github/|^templates/|(^|/)node_modules/", t)
              and not (repo_name == "stash" and t.startswith("agent/"))]

    changed = 0
    for p in dict.fromkeys(targets):
        text, nl = read(p)
        new = insert_nav(text, nav_for(p))
        if new != text:
            write(p, new, nl)
            changed += 1

    # README: nav line + docs index block
    if os.path.isfile(readme):
        text, nl = read(readme)
        text = insert_nav(text, nav_for(readme))
        rows = []
        # top-level docs/ files lead without a heading, unless other folders get headings too
        group = None if extras else "docs/"
        for p in list(dict.fromkeys(targets)) + extras:
            r = rel(repo_dir, p)
            if p in extras:
                g = os.path.relpath(os.path.dirname(p), repo_dir).replace(os.sep, "/") + "/"
            elif not p.startswith(docs + os.sep):
                g = "repo root"
            else:
                sub = os.path.relpath(os.path.dirname(p), docs).replace(os.sep, "/")
                g = "docs/" if sub == "." else f"docs/{sub}/"
            if g != group:
                rows += ([""] if rows else []) + [f"**`{g}`**", ""]
                group = g
            title = re.sub(r"([\[\]])", lambda m: "\\" + m.group(1), title_of(p))  # a [ or ] in a title would break the link
            rows.append(f"- [{title}]({r}) — `{r[2:]}`")
        # blank lines inside the markers keep the block Prettier-stable
        scope = ("Every doc at the repo root (other than this README) and under `docs/` (the files mirrored into the "
                 "Obsidian vault), so none of them is orphaned.") if not extras else (
                 "Every committed Markdown doc in this repo (other than this README, `.github/` and `templates/`), "
                 "the same set mirrored into the Obsidian vault, so none of them is orphaned.")
        block = "\n".join([IDX_START, "", "## Docs Index", "", scope, ""] + rows + ["", IDX_END])
        if IDX_START in text:
            text = re.sub(re.escape(IDX_START) + r".*?" + re.escape(IDX_END), lambda m: block, text, flags=re.S)
        else:
            m = re.search(r"^##\s+.*licen[cs]e.*$", text, re.M | re.I)
            if m:
                text = text[:m.start()] + block + "\n\n" + text[m.start():]
            else:
                text = text.rstrip("\n") + "\n\n" + block + "\n"
        old, _ = read(readme)
        if text != old:
            write(readme, text, nl)
            changed += 1
    print(f"{repo_name}: {changed} file(s) updated")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
