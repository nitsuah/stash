"""Builds the 'Claude Code Skills Starter Bundle' from the user's own skills. Scrubs personal paths; reports leftovers for human review."""
import pathlib
import re
import shutil
import zipfile

SRC = pathlib.Path.home() / ".claude" / "skills"
SKILLS = ["content-gen", "repo-audit", "site-gen", "journeys", "opencut", "brag-slim", "promo"]
root = pathlib.Path(__file__).parent
dist = root / "dist" / "claude-code-skills-bundle"
shutil.rmtree(root / "dist", ignore_errors=True)
dist.mkdir(parents=True)
BS = chr(92)
SUBS = [
    (f"C:{BS}Users{BS}ajhar{BS}code", "~/code"),
    (f"C:{BS}Users{BS}ajhar", "~"),
    ("/c/Users/ajhar", "~"),
    ("ajhar", "<user>"),
]
LEFT = re.compile(r"nitsuah|Nitsuah|gmail|@[\w.-]+\.\w+|api[_-]?key|token|secret", re.I)
report = []
for s in SKILLS:
    t = (SRC / s / "SKILL.md").read_text(encoding="utf-8")
    for a, b in SUBS:
        t = t.replace(a, b)
    (dist / s).mkdir()
    (dist / s / "SKILL.md").write_text(t, encoding="utf-8")
    for i, line in enumerate(t.splitlines(), 1):
        if LEFT.search(line):
            report.append(f"{s}:{i}: {line.strip()[:140]}")
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
