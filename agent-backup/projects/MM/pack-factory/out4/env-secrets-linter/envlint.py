"""python envlint.py [folder]   Scans text files for likely committed secrets and .env problems. Offline, stdlib only.
Exit code 1 if anything is found, so it can run in CI or a git pre-commit hook. Heuristic: expect false positives and misses."""
import os, re, sys

RULES = [
    ("AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----")),
    ("Slack token", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}")),
    ("Generic secret assignment", re.compile(r"(?i)(?:secret|password|passwd|api[_-]?key|token)\s*[:=]\s*['\"]?[A-Za-z0-9/+_=-]{16,}['\"]?")),
]
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}
SKIP_EXT = {".png", ".jpg", ".gif", ".zip", ".pdf", ".woff", ".woff2", ".ico"}
root = sys.argv[1] if len(sys.argv) > 1 else "."
found = 0
for d, dirs, files in os.walk(root):
    dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
    for f in files:
        p = os.path.join(d, f)
        if os.path.splitext(f)[1].lower() in SKIP_EXT:
            continue
        if f == ".env" or (f.startswith(".env.") and f != ".env.example"):
            print(f"{p}: env file present (make sure it is git-ignored)")
            found += 1
        try:
            for n, line in enumerate(open(p, encoding="utf-8"), 1):
                for name, rx in RULES:
                    if rx.search(line):
                        print(f"{p}:{n}: {name}")
                        found += 1
        except (UnicodeDecodeError, OSError):
            pass
print(f"{found} finding(s)", file=sys.stderr)
sys.exit(1 if found else 0)
