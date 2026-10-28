"""python csv_clean.py in.csv out.csv [--dedupe] [--lower-emails] [--phones] [--dates date_col,...]
Trims whitespace, collapses repeated spaces, optionally dedupes rows, lowercases email columns, normalizes US phones to
(XXX) XXX-XXXX and dates to YYYY-MM-DD. Prints a report. Stdlib only."""
import csv, re, sys
from datetime import datetime

args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = [a for a in sys.argv[1:] if a.startswith("--")]
src, dst = args[0], args[1]
date_cols = []
for i, a in enumerate(sys.argv):
    if a == "--dates" and i + 1 < len(sys.argv):
        date_cols = sys.argv[i + 1].split(",")
        args = [x for x in args if x != sys.argv[i + 1]]
FORMATS = ["%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d %b %Y", "%b %d, %Y", "%Y/%m/%d"]


def to_iso(v):
    for f in FORMATS:
        try:
            return datetime.strptime(v, f).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return v


def phone(v):
    d = re.sub(r"\D", "", v)
    if len(d) == 11 and d[0] == "1":
        d = d[1:]
    return f"({d[:3]}) {d[3:6]}-{d[6:]}" if len(d) == 10 else v


rows = list(csv.DictReader(open(src, newline="", encoding="utf-8-sig")))
fields = list(rows[0].keys()) if rows else []
changed = 0
for r in rows:
    for k in fields:
        v = r[k] or ""
        n = re.sub(r"\s+", " ", v).strip()
        if "--lower-emails" in flags and "email" in k.lower():
            n = n.lower()
        if "--phones" in flags and "phone" in k.lower():
            n = phone(n)
        if k in date_cols and n:
            n = to_iso(n)
        if n != v:
            changed += 1
        r[k] = n
before = len(rows)
if "--dedupe" in flags:
    seen, out = set(), []
    for r in rows:
        key = tuple(r.values())
        if key not in seen:
            seen.add(key)
            out.append(r)
    rows = out
with open(dst, "w", newline="", encoding="utf-8") as f:
    wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
    wr.writeheader()
    wr.writerows(rows)
print(f"rows in: {before}, rows out: {len(rows)}, cells changed: {changed}", file=sys.stderr)
