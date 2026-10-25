"""Batch 3 pack builder: self-hosting compose pack, CSV cleaner, test data generator, dedupe tool, text extractor,
backup script, model/dataset card templates. Stdlib only. Run in python:3-slim, then validate compose with docker."""
import csv
import pathlib
import shutil
import subprocess
import sys
import textwrap
import time
import zipfile

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out3"
shutil.rmtree(OUT, ignore_errors=True)
LIC = "Personal and commercial use. Do not resell or redistribute the files themselves.\n"


def w(base, rel, text):
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")


def zip_pack(slug):
    z = OUT / f"{slug}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted((OUT / slug).rglob("*")):
            if p.is_file():
                zf.write(p, f"{slug}/{p.relative_to(OUT / slug).as_posix()}")
    return z.stat().st_size


# ---------- self-hosting compose pack ----------
b = OUT / "self-hosting-compose-pack"
STACKS = {
    "umami": ("Privacy-friendly web analytics", """
        services:
          umami:
            image: ghcr.io/umami-software/umami:postgresql-latest
            ports: ["3000:3000"]
            environment:
              DATABASE_URL: postgresql://umami:${DB_PASSWORD}@db:5432/umami
              APP_SECRET: ${APP_SECRET}
            depends_on: [db]
            restart: unless-stopped
          db:
            image: postgres:16
            environment:
              POSTGRES_DB: umami
              POSTGRES_USER: umami
              POSTGRES_PASSWORD: ${DB_PASSWORD}
            volumes: [umami-db:/var/lib/postgresql/data]
            restart: unless-stopped
        volumes:
          umami-db:
        """, "DB_PASSWORD=change-me\nAPP_SECRET=change-me-too\n", "Open http://localhost:3000. Default login is documented by Umami; change it immediately."),
    "uptime-kuma": ("Self-hosted uptime monitoring", """
        services:
          kuma:
            image: louislam/uptime-kuma:1
            ports: ["3001:3001"]
            volumes: [kuma-data:/app/data]
            restart: unless-stopped
        volumes:
          kuma-data:
        """, "", "Open http://localhost:3001 and create the admin account."),
    "listmonk": ("Newsletter and mailing lists", """
        services:
          app:
            image: listmonk/listmonk:latest
            ports: ["9000:9000"]
            environment:
              LISTMONK_app__address: 0.0.0.0:9000
              LISTMONK_db__user: listmonk
              LISTMONK_db__password: ${DB_PASSWORD}
              LISTMONK_db__database: listmonk
              LISTMONK_db__host: db
              LISTMONK_db__port: 5432
              LISTMONK_ADMIN_USER: ${ADMIN_USER}
              LISTMONK_ADMIN_PASSWORD: ${ADMIN_PASSWORD}
            depends_on: [db]
            restart: unless-stopped
          db:
            image: postgres:16
            environment:
              POSTGRES_USER: listmonk
              POSTGRES_PASSWORD: ${DB_PASSWORD}
              POSTGRES_DB: listmonk
            volumes: [listmonk-db:/var/lib/postgresql/data]
            restart: unless-stopped
        volumes:
          listmonk-db:
        """, "DB_PASSWORD=change-me\nADMIN_USER=admin\nADMIN_PASSWORD=change-me-too\n", "First run may need `docker compose run --rm app ./listmonk --install` (see listmonk docs). You need an SMTP provider to send mail; follow anti-spam laws."),
    "nextcloud": ("Private file sync and sharing", """
        services:
          app:
            image: nextcloud:stable
            ports: ["8080:80"]
            environment:
              MYSQL_HOST: db
              MYSQL_DATABASE: nextcloud
              MYSQL_USER: nextcloud
              MYSQL_PASSWORD: ${DB_PASSWORD}
            volumes: [nextcloud-data:/var/www/html]
            depends_on: [db]
            restart: unless-stopped
          db:
            image: mariadb:11
            command: --transaction-isolation=READ-COMMITTED --binlog-format=ROW
            environment:
              MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
              MYSQL_DATABASE: nextcloud
              MYSQL_USER: nextcloud
              MYSQL_PASSWORD: ${DB_PASSWORD}
            volumes: [nextcloud-db:/var/lib/mysql]
            restart: unless-stopped
        volumes:
          nextcloud-data:
          nextcloud-db:
        """, "DB_PASSWORD=change-me\nDB_ROOT_PASSWORD=change-me-too\n", "Open http://localhost:8080 and create the admin account. Put it behind HTTPS before exposing it."),
    "gitea": ("Self-hosted Git service", """
        services:
          gitea:
            image: gitea/gitea:latest
            ports: ["3002:3000", "2222:22"]
            volumes: [gitea-data:/data]
            restart: unless-stopped
        volumes:
          gitea-data:
        """, "", "Open http://localhost:3002 and finish the install page. SSH is on port 2222."),
    "grocy": ("Household or shop inventory", """
        services:
          grocy:
            image: lscr.io/linuxserver/grocy:latest
            ports: ["9283:80"]
            environment:
              PUID: 1000
              PGID: 1000
              TZ: ${TZ}
            volumes: [grocy-config:/config]
            restart: unless-stopped
        volumes:
          grocy-config:
        """, "TZ=America/New_York\n", "Open http://localhost:9283. Default login is in the Grocy docs; change it."),
    "photoprism": ("Private photo library", """
        services:
          photoprism:
            image: photoprism/photoprism:latest
            ports: ["2342:2342"]
            environment:
              PHOTOPRISM_ADMIN_PASSWORD: ${ADMIN_PASSWORD}
              PHOTOPRISM_DATABASE_DRIVER: mysql
              PHOTOPRISM_DATABASE_SERVER: db:3306
              PHOTOPRISM_DATABASE_NAME: photoprism
              PHOTOPRISM_DATABASE_USER: photoprism
              PHOTOPRISM_DATABASE_PASSWORD: ${DB_PASSWORD}
            volumes:
              - ./originals:/photoprism/originals
              - photoprism-storage:/photoprism/storage
            depends_on: [db]
            restart: unless-stopped
          db:
            image: mariadb:11
            environment:
              MARIADB_ROOT_PASSWORD: ${DB_PASSWORD}
              MARIADB_DATABASE: photoprism
              MARIADB_USER: photoprism
              MARIADB_PASSWORD: ${DB_PASSWORD}
            volumes: [photoprism-db:/var/lib/mysql]
            restart: unless-stopped
        volumes:
          photoprism-storage:
          photoprism-db:
        """, "ADMIN_PASSWORD=change-me-12chars\nDB_PASSWORD=change-me-too\n", "Put photos in ./originals. Admin password must be at least 8 characters."),
    "vaultwarden": ("Password manager server (Bitwarden-compatible)", """
        services:
          vaultwarden:
            image: vaultwarden/server:latest
            ports: ["8081:80"]
            environment:
              SIGNUPS_ALLOWED: "false"
            volumes: [vw-data:/data]
            restart: unless-stopped
        volumes:
          vw-data:
        """, "", "Signups are off by default; enable briefly to create your account, then turn off. Use HTTPS in production and back up /data."),
    "n8n": ("Workflow automation", """
        services:
          n8n:
            image: n8nio/n8n:latest
            ports: ["5678:5678"]
            environment:
              GENERIC_TIMEZONE: ${TZ}
            volumes: [n8n-data:/home/node/.n8n]
            restart: unless-stopped
        volumes:
          n8n-data:
        """, "TZ=America/New_York\n", "Open http://localhost:5678 and create the owner account."),
    "ntfy": ("Push notifications to your phone", """
        services:
          ntfy:
            image: binwiederhier/ntfy
            command: serve
            ports: ["127.0.0.1:8090:80"]
            volumes: [ntfy-cache:/var/cache/ntfy]
            restart: unless-stopped
        volumes:
          ntfy-cache:
        """, "", "Publish with curl -d 'hello' http://localhost:8090/mytopic and subscribe in the ntfy app."),
}
idx = ["# Self-Hosting Docker Compose Pack\n\nTen ready-to-run stacks. Each folder has `docker-compose.yml`, `.env.example` (copy to `.env`) and a README.\n\n| Stack | What it is |\n|---|---|\n"]
for name, (desc, compose, env, note) in STACKS.items():
    w(b, f"{name}/docker-compose.yml", compose)
    w(b, f"{name}/.env.example", env or "# no variables needed\n")
    w(b, f"{name}/README.md", f"# {name}\n{desc}.\n\n    cp .env.example .env   # edit secrets\n    docker compose up -d\n\n{note}\n\nImages use `latest` tags; pin a version before relying on it. Back up the named volumes.\n")
    idx.append(f"| {name} | {desc} |\n")
idx.append("\nRequires Docker. These are starting points, not hardened production setups: use HTTPS, strong secrets, firewalls and backups. " + LIC)
w(b, "README.md", "".join(idx))
print("compose", len(STACKS), zip_pack("self-hosting-compose-pack"))

# ---------- CSV cleaner ----------
b = OUT / "csv-cleaner"
(b).mkdir(parents=True)
(b / "csv_clean.py").write_text('''"""python csv_clean.py in.csv out.csv [--dedupe] [--lower-emails] [--phones] [--dates date_col,...]
Trims whitespace, collapses repeated spaces, optionally dedupes rows, lowercases email columns, normalizes US phones to
(XXX) XXX-XXXX and dates to YYYY-MM-DD. Prints a report. Stdlib only."""
import csv, re, sys
from datetime import datetime

args = [a for a in sys.argv[1:] if not a.startswith("--")]
flags = [a for a in sys.argv[1:] if a.startswith("--")]
date_cols = []
for i, a in enumerate(sys.argv):
    if a == "--dates" and i + 1 < len(sys.argv):
        date_cols = sys.argv[i + 1].split(",")
        args = [x for x in args if x != sys.argv[i + 1]]
src, dst = args[0], args[1]
FORMATS = ["%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d %b %Y", "%b %d, %Y", "%Y/%m/%d"]


def to_iso(v):
    for f in FORMATS:
        try:
            return datetime.strptime(v, f).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return v


def phone(v):
    d = re.sub(r"\\D", "", v)
    if len(d) == 11 and d[0] == "1":
        d = d[1:]
    return f"({d[:3]}) {d[3:6]}-{d[6:]}" if len(d) == 10 else v


rows = list(csv.DictReader(open(src, newline="", encoding="utf-8-sig")))
fields = list(rows[0].keys()) if rows else []
changed = 0
for r in rows:
    for k in fields:
        v = r[k] or ""
        n = re.sub(r"\\s+", " ", v).strip()
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
    wr = csv.DictWriter(f, fieldnames=fields, lineterminator="\\n")
    wr.writeheader()
    wr.writerows(rows)
print(f"rows in: {before}, rows out: {len(rows)}, cells changed: {changed}", file=sys.stderr)
''', encoding="utf-8")
w(b, "messy.csv", "name,email,phone,signup\n  Ana  Lopez ,ANA@Example.com,phone unavailable,03/05/2026\nBen Ray,ben@example.com,phone unavailable,2026-03-06\n  Ana  Lopez ,ANA@Example.com,phone unavailable,03/05/2026\n")
w(b, "README.md", f"""
# CSV Cleaner
    python csv_clean.py messy.csv clean.csv --dedupe --lower-emails --phones --dates signup
Trims and collapses spaces, removes exact duplicate rows, lowercases email columns, normalizes US phone numbers and dates (YYYY-MM-DD).
Columns are matched by name (columns containing "email" or "phone"). Review the output before using it. Plain Python 3.

{LIC}""")
r = subprocess.run([sys.executable, "csv_clean.py", "messy.csv", "clean.csv", "--dedupe", "--lower-emails", "--phones", "--dates", "signup"], cwd=b, capture_output=True, text=True, check=True)
rows = list(csv.DictReader(open(b / "clean.csv")))
assert len(rows) == 2 and rows[0]["email"] == "ana@example.com" and rows[0]["phone"] == "phone unavailable" and rows[0]["signup"] == "2026-03-05", rows
(b / "clean.csv").unlink()
print("csv-clean", r.stderr.strip(), zip_pack("csv-cleaner"))

# ---------- test data generator ----------
b = OUT / "test-data-generator"
b.mkdir(parents=True)
(b / "gen_testdata.py").write_text('''"""python gen_testdata.py --rows 100 --seed 1 --format csv|json > people.csv  (fake people and orders, no real data)"""
import csv, json, random, sys
from datetime import date, timedelta

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

n, seed, fmt = int(arg("--rows", 100)), int(arg("--seed", 1)), arg("--format", "csv")
rnd = random.Random(seed)
first = ["Ana", "Ben", "Chen", "Dara", "Eli", "Fay", "Gus", "Hana", "Ivan", "Jo", "Kai", "Lena", "Milo", "Nia", "Omar", "Pia"]
last = ["Lopez", "Ray", "Wu", "Singh", "Kim", "Okafor", "Novak", "Silva", "Haas", "Reyes", "Costa", "Dube"]
cities = ["Springfield", "Riverton", "Lakeside", "Fairview", "Georgetown", "Madison"]
rows = []
for i in range(1, n + 1):
    f, l = rnd.choice(first), rnd.choice(last)
    rows.append({"id": i, "name": f"{f} {l}", "email": f"{f}.{l}{i}@example.test".lower(), "phone": f"555-01{rnd.randint(0, 99):02d}",
                 "city": rnd.choice(cities), "signup": (date(2026, 1, 1) + timedelta(days=rnd.randint(0, 300))).isoformat(),
                 "order_total": round(rnd.uniform(5, 500), 2)})
if fmt == "json":
    print(json.dumps(rows, indent=2))
else:
    wr = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]), lineterminator="\\n")
    wr.writeheader()
    wr.writerows(rows)
''', encoding="utf-8")
w(b, "README.md", f"""
# Test Data Generator
    python gen_testdata.py --rows 500 --seed 7 --format csv > people.csv
Reproducible fake people and orders (same seed, same data). Emails use the reserved example.test domain; phone numbers use
the 555-01xx fictional range, so nothing points at real people. Edit the name and city lists for other locales. Plain Python 3.

{LIC}""")
r = subprocess.run([sys.executable, "gen_testdata.py", "--rows", "50", "--seed", "3"], cwd=b, capture_output=True, text=True, check=True)
r2 = subprocess.run([sys.executable, "gen_testdata.py", "--rows", "50", "--seed", "3"], cwd=b, capture_output=True, text=True, check=True)
assert r.stdout == r2.stdout and len(r.stdout.strip().splitlines()) == 51
print("testdata", zip_pack("test-data-generator"))

# ---------- dedupe tool ----------
b = OUT / "fuzzy-dedupe-tool"
b.mkdir(parents=True)
(b / "dedupe.py").write_text('''"""python dedupe.py in.csv column [--threshold 0.88] > report.csv
Finds likely duplicate values in one column (exact after normalizing case/spacing/punctuation, plus fuzzy matches) and prints groups.
Never deletes anything: it only reports. Stdlib only."""
import csv, difflib, re, sys

args = [a for a in sys.argv[1:] if not a.startswith("--")]
th = float(sys.argv[sys.argv.index("--threshold") + 1]) if "--threshold" in sys.argv else 0.88
if "--threshold" in sys.argv:
    args = [a for a in args if a != sys.argv[sys.argv.index("--threshold") + 1]]
src, col = args[0], args[1]
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", re.sub(r"\\s+", " ", s.lower()).strip())
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
wr = csv.writer(sys.stdout, lineterminator="\\n")
wr.writerow(["group", "row_number", col])
g = 0
for members in groups.values():
    if len(members) > 1:
        g += 1
        for m in members:
            wr.writerow([g, m + 2, vals[m][1]])
print(f"{g} duplicate group(s) in {len(rows)} rows", file=sys.stderr)
''', encoding="utf-8")
w(b, "sample.csv", "company\nAcme Corp\nacme corp.\nAcme Corporation\nGlobex\nInitech\nglobex\n")
w(b, "README.md", f"""
# Fuzzy Dedupe Tool
    python dedupe.py sample.csv company > report.csv
Finds likely duplicates in one column: exact matches after ignoring case, spaces and punctuation, plus similar spellings (default
similarity 0.88; lower with `--threshold 0.8`). It only reports groups with row numbers; you decide what to merge or delete.
Comparison is pairwise, so it suits files up to a few thousand rows. Plain Python 3.

{LIC}""")
r = subprocess.run([sys.executable, "dedupe.py", "sample.csv", "company"], cwd=b, capture_output=True, text=True, check=True)
assert "2 duplicate group(s)" in r.stderr, r.stderr
print("dedupe", r.stderr.strip(), zip_pack("fuzzy-dedupe-tool"))

# ---------- text extractor ----------
b = OUT / "text-extractor"
b.mkdir(parents=True)
(b / "extract.py").write_text('''"""python extract.py notes.txt > found.csv   Pulls emails, US phone numbers, URLs, dates and dollar amounts out of text. Stdlib only."""
import csv, re, sys

text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
PATTERNS = {
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}",
    "phone": r"(?:\\+?1[ .-]?)?\\(?\\d{3}\\)?[ .-]?\\d{3}[ .-]?\\d{4}",
    "url": r"https?://[^\\s<>\\"')]+",
    "date": r"\\b(?:\\d{4}-\\d{2}-\\d{2}|\\d{1,2}/\\d{1,2}/\\d{2,4})\\b",
    "amount": r"\\$\\s?\\d[\\d,]*(?:\\.\\d{2})?",
}
wr = csv.writer(sys.stdout, lineterminator="\\n")
wr.writerow(["type", "value", "line"])
counts = {}
for kind, pat in PATTERNS.items():
    for m in re.finditer(pat, text):
        line = text.count("\\n", 0, m.start()) + 1
        wr.writerow([kind, m.group(0).strip(), line])
        counts[kind] = counts.get(kind, 0) + 1
print(counts, file=sys.stderr)
''', encoding="utf-8")
w(b, "sample.txt", "Call unavailable or email ops@example.com by 2026-03-15.\nInvoice total $1,250.00 at https://example.com/inv/9\nOther: phone unavailable, due 4/2/26, $40\n")
w(b, "README.md", f"""
# Text Extractor
    python extract.py notes.txt > found.csv
Finds emails, US phone numbers, URLs, dates and dollar amounts in any text file and lists them with line numbers. Pattern-based,
so expect some misses and false hits; check the results. Add your own patterns in the PATTERNS table. Plain Python 3, offline.

{LIC}""")
r = subprocess.run([sys.executable, "extract.py", "sample.txt"], cwd=b, capture_output=True, text=True, check=True)
assert "ops@example.com" in r.stdout and "1,250.00" in r.stdout and "https://example.com/inv/9" in r.stdout and "2026-03-15" in r.stdout, r.stdout
print("extract", r.stderr.strip(), zip_pack("text-extractor"))

# ---------- backup script ----------
b = OUT / "simple-backup-script"
b.mkdir(parents=True)
(b / "backup.py").write_text('''"""python backup.py --src ~/Documents --src ~/Projects --dest /mnt/backup --keep 7
Creates a timestamped .tar.gz of each source, verifies it can be read, and deletes the oldest beyond --keep. Stdlib only."""
import os, sys, tarfile, time
from pathlib import Path

def opts(name):
    return [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == name and i + 1 < len(sys.argv)]

srcs, dest, keep = [Path(os.path.expanduser(s)) for s in opts("--src")], Path(os.path.expanduser((opts("--dest") or ["."])[0])), int((opts("--keep") or ["7"])[0])
if not srcs:
    sys.exit("usage: backup.py --src DIR [--src DIR ...] --dest DIR [--keep N]")
dest.mkdir(parents=True, exist_ok=True)
stamp = time.strftime("%Y%m%d-%H%M%S")
for s in srcs:
    name = s.name or "root"
    out = dest / f"{name}-{stamp}.tar.gz"
    with tarfile.open(out, "w:gz") as t:
        t.add(s, arcname=name)
    with tarfile.open(out) as t:
        n = len(t.getmembers())
    print(f"wrote {out} ({out.stat().st_size} bytes, {n} entries, verified)")
    olds = sorted(dest.glob(f"{prefix}-*.tar.gz"))
    for o in olds[:-keep]:
        o.unlink()
        print("removed old", o.name)
''', encoding="utf-8")
w(b, "README.md", f"""
# Simple Backup Script
    python backup.py --src ~/Documents --src ~/Projects --dest /mnt/backup --keep 7
Makes a timestamped compressed archive of each folder, checks the archive can be read back, and keeps only the newest N per folder.
Schedule it with cron (Linux/macOS) or Task Scheduler (Windows). Keep a copy off-site, and test a restore now and then.
It does not encrypt; store archives somewhere you trust or encrypt the destination. Plain Python 3.

{LIC}""")
srcdir = OUT / "_t_src"
srcdir.mkdir()
(srcdir / "a.txt").write_text("hello")
for _ in range(4):
    subprocess.run([sys.executable, "backup.py", "--src", str(srcdir), "--dest", str(OUT / "_t_dest"), "--keep", "2"], cwd=b, check=True, capture_output=True)
    time.sleep(1.1)
kept = list((OUT / "_t_dest").glob("_t_src-*.tar.gz"))
assert len(kept) == 2, kept
shutil.rmtree(srcdir)
shutil.rmtree(OUT / "_t_dest")
print("backup keeps 2 of 4", zip_pack("simple-backup-script"))

# ---------- model and dataset card templates ----------
b = OUT / "model-and-dataset-card-templates"
w(b, "MODEL_CARD.md", """
---
license: <license>
language: <languages>
base_model: <base model, if any>
tags: []
---
# Model name
## Summary
One paragraph: what it does and who it is for.
## Intended use
- In scope:
- Out of scope:
## How to use
```python
# minimal working example
```
## Training data
Source, size, collection date, licensing, filtering steps.
## Training procedure
Hardware, hyperparameters, seeds, training time.
## Evaluation
| Benchmark | Metric | Score | Notes |
|---|---|---|---|
## Limitations and biases
Known failure modes; groups or inputs it handles poorly.
## Risks and mitigations
## Citation / contact
""")
w(b, "DATASET_CARD.md", """
---
license: <license>
language: <languages>
size_categories: <n<1K | 1K<n<10K | ...>
---
# Dataset name
## Summary
What it contains and why it exists.
## Structure
| Field | Type | Description |
|---|---|---|
## Collection
How and when data was gathered; consent and licensing; what was removed (PII, duplicates).
## Splits
| Split | Rows |
|---|---|
## Known issues
Imbalances, label noise, gaps.
## Intended and prohibited uses
## Maintenance
Version history and contact.
""")
w(b, "README.md", f"""
# Model and Dataset Card Templates
Two fill-in-the-blank Markdown templates (with Hugging Face style front matter) for documenting a model or a dataset: summary, intended use,
data, training, evaluation, limitations and risks. Copy, fill in, publish next to your files. Documentation templates only; they do
not check your claims or license compliance.

{LIC}""")
print("cards", zip_pack("model-and-dataset-card-templates"))
