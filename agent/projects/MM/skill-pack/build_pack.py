


def main():
    """Builds the 'Claude Code Skills Starter Bundle' from the user's own skills. Scrubs personal paths; reports leftovers for human review."""
    import pathlib
    import re
    import shutil
    import zipfile

    SRC = pathlib.Path.home() / ".claude" / "skills"
    SKILLS = ["content-gen", "repo-audit", "site-gen", "journeys", "opencut", "brag-slim", "promo"]
    root = pathlib.Path(__file__).parent
    dist = root / "dist" / "claude-code-skills-bundle"
    missing = [s for s in SKILLS if not (SRC / s / "SKILL.md").is_file()]
    if missing:
        raise SystemExit("Missing source skills before build: " + ", ".join(missing))
    shutil.rmtree(root / "dist", ignore_errors=True)
    dist.mkdir(parents=True)
    BS = chr(92)
    home_path = pathlib.Path.home()
    home = str(home_path)
    home_forms = {home, home.replace("/", BS), home.replace(BS, "/"), home_path.as_posix()}
    if home_path.drive:
        home_tail = home_path.as_posix().split(":", 1)[1].lstrip("/")
        home_forms.add("/" + home_path.drive[0].lower() + "/" + home_tail)
    SUBS = [(p, "~") for p in sorted(home_forms, key=len, reverse=True) if p]
    SUBS.extend([
        (f"C:{BS}Users{BS}ajhar{BS}code{BS}", "~/code/"),
        (f"C:{BS}Users{BS}ajhar", "~"),
        ("/c/Users/ajhar", "~"),
        ("ajhar", "<user>"),
    ])
    LEFT = re.compile(
        r"(?P<project>nitsuah)|(?P<email>gmail|@[\w.-]+\.\w+)|(?P<credential>api[_-]?key|token|secret)", re.I
    )
    PERSONAL_HOME = re.compile(r'''(?i)(?:[A-Z]:[/\\]Users[/\\][^/\\\s"']+|/Users/[^/\s"']+|/home/[^/\s"']+|/[a-z]/Users/[^/\s"']+)''')
    report = []
    for s in SKILLS:
        t = (SRC / s / "SKILL.md").read_text(encoding="utf-8")
        for a, b in SUBS:
            t = re.sub(re.escape(a), lambda _match, replacement=b: replacement, t, flags=re.IGNORECASE)
        t = t.replace(BS, "/")
        (dist / s).mkdir()
        (dist / s / "SKILL.md").write_text(t, encoding="utf-8")
        for i, line in enumerate(t.splitlines(), 1):
            match = LEFT.search(line)
            home_match = PERSONAL_HOME.search(line)
            if match or home_match:
                kind = "personal_home_path" if home_match else match.lastgroup
                report.append(f"{s}:{i}: {kind}")
    (dist / "README.txt").write_text(
        "Claude Code Skills Starter Bundle\n"
        "Copy any folder into ~/.claude/skills/ . Each skill is a SKILL.md workflow for Claude Code. "
        "Some reference external tools (Docker, Netlify, Playwright) and example repo names; "
        "adapt paths and names to your setup. Personal and commercial use; do not resell.\n"
    )
    review_path = root / "REVIEW-LEFTOVERS.txt"
    review_path.write_text("\n".join(report), encoding="utf-8")
    if report:
        raise SystemExit(f"Refusing to create a distributable ZIP: {len(report)} lines need human review. See {review_path}")

    zp = root / "claude-code-skills-bundle.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(dist.rglob("*")):
            if p.is_file():
                z.write(p, f"claude-code-skills-bundle/{p.relative_to(dist).as_posix()}")
    print(len(SKILLS), "skills", zp.stat().st_size, "bytes; no flagged lines")


if __name__ == "__main__":
    main()
