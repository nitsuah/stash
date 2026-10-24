import json, pathlib, re

seen = {}
for f in sorted(pathlib.Path("raw").glob("*.json")):
    for i in json.loads(f.read_text(encoding="utf-8") or "[]"):
        seen[i["url"]] = i
rows = []
for i in seen.values():
    m = re.search(r"\$\s?([0-9][0-9,]*)", i["title"])
    usd = int(m.group(1).replace(",", "")) if m else 0
    if usd < 25 or usd > 10000:
        continue
    c = i["commentsCount"]
    rows.append((usd // (c + 1), usd, c, i["repository"]["nameWithOwner"], i["title"][:80], i["url"]))
print("score\tusd\tcomments\trepo\ttitle\turl")
for r in sorted(rows, reverse=True):
    print("\t".join(map(str, r)))
