"""python dedupe.py in.csv column [--threshold 0.88] > report.csv
Finds likely duplicate values in one column (exact after normalizing case/spacing/punctuation, plus fuzzy matches) and prints groups.
Never deletes anything: it only reports. Stdlib only."""
import csv, difflib, re, sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
th = float(sys.argv[sys.argv.index("--threshold") + 1]) if "--threshold" in sys.argv else 0.88
if "--threshold" in sys.argv:
    args = [a for a in args if a != sys.argv[sys.argv.index("--threshold") + 1]]
src, col = args[0], args[1]
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", re.sub(r"\s+", " ", s.lower()).strip())
rows = list(csv.DictReader(open(src, newline="", encoding="utf-8-sig")))
vals = [(i, r[col], norm(r[col])) for i, r in enumerate(rows)]
group = list(range(len(vals)))
def find(x):
    while group[x] != x:
        group[x] = group[group[x]]
        x = group[x]
    return x
for a in range(len(vals)):
    for b in range(a + 1, len(vals)):
        if vals[a][2] and (vals[a][2] == vals[b][2] or difflib.SequenceMatcher(None, vals[a][2], vals[b][2]).ratio() >= th):
            group[find(b)] = find(a)
groups = {}
for i in range(len(vals)):
    groups.setdefault(find(i), []).append(i)
wr = csv.writer(sys.stdout, lineterminator="\n")
wr.writerow(["group", "row_number", col])
g = 0
for members in groups.values():
    if len(members) > 1:
        g += 1
        for m in members:
            wr.writerow([g, m + 2, vals[m][1]])
print(f"{g} duplicate group(s) in {len(rows)} rows", file=sys.stderr)
