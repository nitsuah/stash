"""Back up the local scheduled-task routines into agent/routines/ (public-safe copies).

Copies ~/.claude/scheduled-tasks/<name>/SKILL.md for each routine in ROUTINES to
agent/routines/routine-<name>.md, with vault frontmatter and REDACTIONS applied.
stash is PUBLIC, so the export refuses to write anything that still matches the
pii-scan.sh patterns (emails, phone numbers, credential formats) after redaction.

The canonical behaviour of most routines lives in agent/prompts/*.md; these
SKILL.md files are the thin wrappers that schedule them, which exist nowhere
else (they live outside every repo). Cloud routine prompts can't be read from
disk: snapshot those by hand from RemoteTrigger `get` (see routines-backup.md).

Usage: python agent/scripts/export-routines.py [--check]
  --check  exit 1 if any backup is missing or differs from a fresh export
"""
import json
import os
import re
import sys

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(os.path.expanduser("~"), ".claude", "scheduled-tasks")
OUT = os.path.join(VAULT, "routines")

# Recurring routines only: one-shot catch-ups (catchup-*) and the retired hub-checkin are skipped.
ROUTINES = ["daily-repo-sync", "week-sotu", "week-fin-sum", "ops-catchup", "monthly-tire-kick",
            "monthly-pmo-audit", "monthly-usage-report", "monthly-self-improvement"]

# Personal context that steers tone in the live prompt but doesn't belong in a public copy.
REDACTIONS = [
    (re.compile(r"\s*Austin is (?:in a wealth-preservation phase|a technical professional)[^.]*\."), ""),
    (re.compile(r"recovering from burnout", re.I), "[personal context redacted]"),
    (re.compile(r"\bAustin Hardy's\b"), "the owner's"),
    (re.compile(r"\b(?:he|she) could be earning\b"), "the owner could be earning"),
    (re.compile(r"\bwhat get_cds shows (?:he|she)'s earning\b"), "what get_cds shows is being earned"),
]

# Same patterns as pii-scan.sh, kept in step with it.
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
EMAIL_OK = re.compile(r"^(noreply@|no-reply@|.*@users\.noreply\.github\.com$|.*@example\.(com|org|net)$)", re.I)
PHONE = re.compile(r"(^|[^0-9])(\+?1[ .-]?)?\(?[2-9][0-9]{2}\)?[ .-][0-9]{3}[ .-][0-9]{4}([^0-9]|$)")
SECRET = re.compile(r"(ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|gh[osu]_[A-Za-z0-9]{30,}|sk-ant-[A-Za-z0-9_-]{20,}"
                    r"|sk-proj-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,}|AKIA[0-9A-Z]{16}|xox[abpr]-[A-Za-z0-9-]{10,}"
                    r"|AIza[0-9A-Za-z_-]{35}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")


def unquote(value):
    """A YAML-quoted source value back to plain text, so it isn't quoted twice on output."""
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except ValueError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def export(name):
    raw = open(os.path.join(SRC, name, "SKILL.md"), encoding="utf-8").read().replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.DOTALL)
    d = re.search(r"^description:\s*(.*?)\s*$", m.group(1), re.M) if m else None
    desc = unquote(d.group(1)) if d else ""
    body = raw[m.end():] if m else raw
    for pat, repl in REDACTIONS:
        body = pat.sub(repl, body)
        desc = pat.sub(repl, desc)
    head = (f'---\nup: "[[routines-backup]]"\nkind: routine-backup\nroutine: {name}\nruns: local\n'
            f"description: {json.dumps(desc, ensure_ascii=False)}\n---\n\n# routine · {name}\n\n"
            f"> Backup of `~/.claude/scheduled-tasks/{name}/SKILL.md`, exported by `scripts/export-routines.py`."
            f" Edit the live task (or the prompt it points at), then re-export. Don't edit this copy.\n\n")
    return head + body.strip() + "\n"


def leaks(text):
    hits = [e for e in EMAIL.findall(text) if not EMAIL_OK.match(e)]
    return hits + PHONE.findall(text) + SECRET.findall(text)


def main():
    check = "--check" in sys.argv
    os.makedirs(OUT, exist_ok=True)
    bad = 0
    for name in ROUTINES:
        path = os.path.join(OUT, f"routine-{name}.md")
        if not os.path.exists(os.path.join(SRC, name, "SKILL.md")):
            print(f"  [missing] {name}: no SKILL.md under {SRC}")
            bad += 1
            continue
        text = export(name)
        if leaks(text):
            print(f"  [refused] {name}: matches a PII/credential pattern after redaction; add a REDACTIONS rule")
            bad += 1
            continue
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old == text:
            continue
        if check:
            print(f"  [stale] routines/routine-{name}.md")
            bad += 1
        else:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print(f"  [wrote] routines/routine-{name}.md")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
