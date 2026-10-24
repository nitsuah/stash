import datetime
import json
import pathlib
import re

BAD_REPOS = ("bounty-plaza",)
seen = {}
for f in sorted(pathlib.Path("raw").glob("*.json")):
    for i in json.loads(f.read_text(encoding="utf-8") or "[]"):
        seen[i["url"]] = i
now = datetime.datetime.now(datetime.timezone.utc)
rows = []
for i in seen.values():
    repo = i["repository"]["nameWithOwner"]
    if any(b in repo for b in BAD_REPOS):
        continue
    m = re.search(r"\$\s?([0-9][0-9,]*)", i["title"])
    usd = int(m.group(1).replace(",", "")) if m else 0
    age = (now - datetime.datetime.fromisoformat(i["createdAt"].replace("Z", "+00:00"))).days
    c = i["commentsCount"]
    if not (40 <= usd <= 1500) or c > 12 or age > 60:
        continue
    rows.append((usd // (c + 1), usd, c, age, repo, i["title"][:70], i["url"]))
print("score\tusd\tcomments\tage_days\trepo\ttitle\turl")
for r in sorted(rows, reverse=True):
    print("\t".join(map(str, r)))
