"""python extract.py notes.txt > found.csv   Pulls emails, US phone numbers, URLs, dates and dollar amounts out of text. Stdlib only."""
import csv, re, sys

text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
PATTERNS = {
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "phone": r"(?:\+?1[ .-]?)?\(?\d{3}\)?[ .-]?\d{3}[ .-]?\d{4}",
    "url": r"https?://[^\s<>\"')]+",
    "date": r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})\b",
    "amount": r"\$\s?\d[\d,]*(?:\.\d{2})?",
}
wr = csv.writer(sys.stdout, lineterminator="\n")
wr.writerow(["type", "value", "line"])
counts = {}
for kind, pat in PATTERNS.items():
    for m in re.finditer(pat, text):
        line = text.count("\n", 0, m.start()) + 1
        wr.writerow([kind, m.group(0).strip(), line])
        counts[kind] = counts.get(kind, 0) + 1
print(counts, file=sys.stderr)
