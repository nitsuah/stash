"""git log --pretty=%s v1.0..HEAD | python changelog.py "v1.1.0" > CHANGELOG-entry.md
Groups conventional-commit subjects (feat, fix, docs, perf, refactor, chore...) into a Markdown changelog entry. Stdlib only."""
import re, sys, datetime

TITLES = {"feat": "Added", "fix": "Fixed", "perf": "Performance", "docs": "Documentation", "refactor": "Changed", "test": "Tests", "chore": "Maintenance", "build": "Maintenance", "ci": "Maintenance"}
version = sys.argv[1] if len(sys.argv) > 1 else "Unreleased"
groups = {}
for line in sys.stdin.read().splitlines():
    m = re.match(r"^(\w+)(\(([^)]*)\))?(!)?: (.+)$", line.strip())
    if not m:
        if line.strip():
            groups.setdefault("Other", []).append(line.strip())
        continue
    kind, scope, breaking, msg = m.group(1), m.group(3), m.group(4), m.group(5)
    key = "Breaking changes" if breaking else TITLES.get(kind, "Other")
    groups.setdefault(key, []).append((f"**{scope}:** " if scope else "") + msg)
order = ["Breaking changes", "Added", "Fixed", "Changed", "Performance", "Documentation", "Tests", "Maintenance", "Other"]
print(f"## {version} - {datetime.date.today().isoformat()}\n")
for k in order:
    if k in groups:
        print(f"### {k}")
        for i in groups[k]:
            print(f"- {i}")
        print()
