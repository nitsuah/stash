"""Batch 4 pack builder: static site starters, contrast checker, accessibility checklist, SRT tools, changelog generator,
env/secrets linter, sitemap generator, SQL practice pack. Stdlib only. Run in python:3-slim."""
import json, pathlib, shutil, sqlite3, subprocess, sys, textwrap, zipfile

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out4"
shutil.rmtree(OUT, ignore_errors=True)
LIC = "Personal and commercial use. Do not resell or redistribute the files themselves.\n"


def w(base, rel, text):
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text).lstrip("\n"), encoding="utf-8")


def wr(base, rel, text):  # write without dedent (for code)
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def zip_pack(slug):
    z = OUT / f"{slug}.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted((OUT / slug).rglob("*")):
            if p.is_file():
                zf.write(p, f"{slug}/{p.relative_to(OUT / slug).as_posix()}")
    return z.stat().st_size


def run(b, *args, stdin=None):
    return subprocess.run([sys.executable, *args], cwd=b, input=stdin, capture_output=True, text=True, check=True)


# ---------- 131: static site starters ----------
b = OUT / "static-site-starters"
BASE_CSS = ":root{--bg:#ffffff;--fg:#1a1a1a;--muted:#4a4a4a;--accent:#0b5cad;--soft:#f2f5f9}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:18px/1.6 system-ui,sans-serif}a{color:var(--accent)}a:focus,button:focus{outline:3px solid #ffbf47;outline-offset:2px}.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.5rem;z-index:9}header,main,footer{max-width:60rem;margin:auto;padding:1.25rem}nav a{margin-right:1rem}.hero{background:var(--soft);padding:2rem 1.25rem;border-radius:8px}.btn{display:inline-block;background:var(--accent);color:#fff;padding:.7rem 1.2rem;border-radius:6px;text-decoration:none;font-weight:600}.grid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fit,minmax(14rem,1fr))}.card{border:1px solid #c8d0da;border-radius:8px;padding:1rem}.muted{color:var(--muted)}"


def site(name, title, nav, body):
    nav_html = "".join(f"<a href='{h}'>{t}</a>" for h, t in nav)
    wr(b, name, f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title}</title><meta name='description' content='{title}'><link rel='stylesheet' href='style.css'></head><body><a class='skip' href='#main'>Skip to content</a><header><strong>Your Name</strong><nav aria-label='Main'>{nav_html}</nav></header><main id='main'>{body}</main><footer><p class='muted'>&copy; Your Name. <a href='#main'>Back to top</a></p></footer></body></html>")


NAV = [("landing.html", "Home"), ("portfolio.html", "Work"), ("docs.html", "Docs")]
wr(b, "style.css", BASE_CSS)
site("landing.html", "Landing page", NAV, "<section class='hero'><h1>One clear promise for your visitors</h1><p>Explain who it is for and the result they get, in two sentences.</p><a class='btn' href='#contact'>Get in touch</a></section><section aria-labelledby='f'><h2 id='f'>What you get</h2><div class='grid'><div class='card'><h3>Benefit one</h3><p>Short, specific, true.</p></div><div class='card'><h3>Benefit two</h3><p>Short, specific, true.</p></div><div class='card'><h3>Benefit three</h3><p>Short, specific, true.</p></div></div></section><section aria-labelledby='c'><h2 id='c'>Contact</h2><p id='contact'><a href='mailto:you@example.com'>you@example.com</a></p></section>")
site("portfolio.html", "Portfolio", NAV, "<h1>Selected work</h1><div class='grid'><article class='card'><h2>Project one</h2><p>What it was, your role, the result.</p><a href='#'>Read the case study</a></article><article class='card'><h2>Project two</h2><p>What it was, your role, the result.</p><a href='#'>Read the case study</a></article></div>")
site("docs.html", "Documentation", NAV, "<h1>Documentation</h1><section aria-labelledby='s1'><h2 id='s1'>Getting started</h2><p>Install, configure, run.</p><pre><code>npm install your-tool</code></pre></section><section aria-labelledby='s2'><h2 id='s2'>Reference</h2><ul><li><a href='#'>Command one</a></li><li><a href='#'>Command two</a></li></ul></section>")
w(b, "README.md", f"""
# Static Site Starters
Three plain HTML/CSS pages sharing one stylesheet: landing, portfolio and docs. No build step, no JavaScript, no dependencies.
Replace the placeholder text, rename "Your Name", deploy anywhere (Netlify drag-and-drop, GitHub Pages).
Built for accessibility: skip link, landmarks, heading order, visible focus, 4.5:1+ text contrast. Re-run an automated check
(axe-core) after you change colors.

{LIC}""")
print("131", zip_pack("static-site-starters"))

# ---------- 140: contrast checker ----------
b = OUT / "wcag-contrast-checker"
wr(b, "contrast.py", '''"""python contrast.py "#777777" "#ffffff"      -> ratio and WCAG verdicts
python contrast.py --palette palette.json     -> checks every text/background pair in a JSON file
Also suggests the closest darker or lighter text color that reaches 4.5:1. Stdlib only."""
import json, sys


def rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(c):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = sorted((lum(rgb(a)), lum(rgb(b))), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def verdict(r):
    return {"AA normal": r >= 4.5, "AA large": r >= 3.0, "AAA normal": r >= 7.0, "UI/graphics 3:1": r >= 3.0}


def suggest(fg, bg, target=4.5):
    c = list(rgb(fg))
    toward = 0 if lum(rgb(bg)) > 0.5 else 255
    for _ in range(255):
        if ratio("#%02x%02x%02x" % tuple(c), bg) >= target:
            return "#%02x%02x%02x" % tuple(c)
        c = [v + (1 if toward == 255 else -1) if v != toward else v for v in c]
    return None


def report(fg, bg):
    r = ratio(fg, bg)
    print(f"{fg} on {bg}: {r:.2f}:1  " + "  ".join(f"{k}={'pass' if v else 'FAIL'}" for k, v in verdict(r).items()))
    if r < 4.5:
        print(f"  suggestion: use {suggest(fg, bg)} for text on {bg}")


if "--palette" in sys.argv:
    for p in json.load(open(sys.argv[sys.argv.index("--palette") + 1])):
        report(p["fg"], p["bg"])
else:
    report(sys.argv[1], sys.argv[2])
''')
wr(b, "palette.json", json.dumps([{"fg": "#1a1a1a", "bg": "#ffffff"}, {"fg": "#777777", "bg": "#ffffff"}, {"fg": "#ffffff", "bg": "#0b5cad"}], indent=2))
w(b, "README.md", f"""
# WCAG Contrast Checker
    python contrast.py "#777777" "#ffffff"
    python contrast.py --palette palette.json
Reports the contrast ratio and whether it meets WCAG 2.x AA (4.5:1 normal text, 3:1 large text and UI components) and AAA (7:1),
and suggests the closest color that reaches 4.5:1. Text over images or gradients needs manual checking. Plain Python 3.

{LIC}""")
r1 = run(b, "contrast.py", "#000000", "#ffffff").stdout
assert "21.00:1" in r1, r1
r2 = run(b, "contrast.py", "#777777", "#ffffff").stdout
assert "FAIL" in r2 and "suggestion" in r2, r2
print("140", zip_pack("wcag-contrast-checker"))

# ---------- 149: accessibility checklist ----------
b = OUT / "accessibility-checklist"
GROUPS = {
    "Perceivable": [("1.1.1", "Every meaningful image has a text alternative; decorative images are hidden from assistive tech"), ("1.2.2", "Prerecorded video has captions"), ("1.3.1", "Headings, lists, tables and form labels use real HTML structure"), ("1.4.3", "Text contrast is at least 4.5:1 (3:1 for large text)"), ("1.4.4", "Text can be zoomed to 200% without losing content"), ("1.4.10", "Content reflows at 320px wide without horizontal scrolling"), ("1.4.11", "Buttons, inputs and focus indicators have 3:1 contrast")],
    "Operable": [("2.1.1", "Everything works with a keyboard alone"), ("2.1.2", "Keyboard focus is never trapped"), ("2.4.1", "A skip link lets keyboard users bypass the navigation"), ("2.4.3", "Focus order follows the visual order"), ("2.4.4", "Link text makes sense out of context"), ("2.4.7", "Keyboard focus is clearly visible"), ("2.4.11", "Focused items are not hidden behind sticky headers (WCAG 2.2)"), ("2.5.8", "Click targets are at least 24 by 24 CSS pixels (WCAG 2.2)")],
    "Understandable": [("3.1.1", "The page language is set (html lang)"), ("3.2.3", "Navigation is consistent across pages"), ("3.3.1", "Form errors are identified in text"), ("3.3.2", "Inputs have visible labels and instructions"), ("3.3.7", "Do not ask users to re-enter information you already have (WCAG 2.2)"), ("3.3.8", "Login does not rely on solving a puzzle or memorizing (WCAG 2.2)")],
    "Robust": [("4.1.2", "Custom controls expose name, role and state"), ("4.1.3", "Status messages are announced without moving focus")],
}
body = "".join(f"<h2>{g}</h2><ul>" + "".join(f"<li><label><input type='checkbox' data-k='{c}'> <strong>{c}</strong> {t}</label></li>" for c, t in items) + "</ul>" for g, items in GROUPS.items())
wr(b, "checklist.html", f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Accessibility checklist (WCAG 2.2 AA)</title><style>body{{font:18px/1.6 system-ui,sans-serif;max-width:46rem;margin:2rem auto;padding:0 1rem;color:#1a1a1a;background:#fff}}ul{{list-style:none;padding:0}}li{{margin:.5rem 0}}input{{width:1.2rem;height:1.2rem}}</style></head><body><main><h1>Accessibility checklist (WCAG 2.2 AA)</h1><p>A plain-language working checklist. Ticks are saved in this browser. Automated tools catch only part of these; test with a keyboard and a screen reader too.</p>{body}</main><script>document.querySelectorAll('input[type=checkbox]').forEach(function(c){{try{{c.checked=localStorage.getItem('a11y-'+c.dataset.k)==='1'}}catch(e){{}}c.addEventListener('change',function(){{try{{localStorage.setItem('a11y-'+c.dataset.k,c.checked?'1':'0')}}catch(e){{}}}})}})</script></body></html>")
w(b, "README.txt", "Open checklist.html in a browser. Numbers are WCAG success criteria. This is a working aid, not a conformance audit or legal advice.\n\n" + LIC)
print("149", sum(len(v) for v in GROUPS.values()), "items", zip_pack("accessibility-checklist"))

# ---------- 146: SRT tools ----------
b = OUT / "srt-tools"
wr(b, "srt_tools.py", '''"""python srt_tools.py shift in.srt out.srt 2.5      (seconds, negative allowed)
python srt_tools.py vtt in.srt out.vtt
python srt_tools.py clean in.srt out.srt            (strip HTML tags, drop empty cues, renumber)
python srt_tools.py merge a.srt b.srt out.srt        (append b after a, renumber)
Stdlib only."""
import re, sys

TS = re.compile(r"(\\d{2}):(\\d{2}):(\\d{2}),(\\d{3})")


def parse(text):
    cues = []
    for block in re.split(r"\\n\\s*\\n", text.strip().replace("\\r\\n", "\\n")):
        lines = block.split("\\n")
        if len(lines) >= 2 and "-->" in lines[1]:
            a, b = (x.strip() for x in lines[1].split("-->"))
            cues.append([ms(a), ms(b), "\\n".join(lines[2:])])
    return cues


def ms(t):
    h, m, s, f = map(int, TS.match(t).groups())
    return ((h * 60 + m) * 60 + s) * 1000 + f


def fmt(v, sep=","):
    v = max(0, int(round(v)))
    return f"{v // 3600000:02d}:{v // 60000 % 60:02d}:{v // 1000 % 60:02d}{sep}{v % 1000:03d}"


def dump(cues, sep=","):
    return "\\n\\n".join(f"{i}\\n{fmt(a, sep)} --> {fmt(b, sep)}\\n{t}" for i, (a, b, t) in enumerate(cues, 1)) + "\\n"


cmd = sys.argv[1]
if cmd == "shift":
    cues = [[a + float(sys.argv[4]) * 1000, b + float(sys.argv[4]) * 1000, t] for a, b, t in parse(open(sys.argv[2], encoding="utf-8").read())]
    open(sys.argv[3], "w", encoding="utf-8").write(dump(cues))
elif cmd == "vtt":
    cues = parse(open(sys.argv[2], encoding="utf-8").read())
    open(sys.argv[3], "w", encoding="utf-8").write("WEBVTT\\n\\n" + dump(cues, ".").replace("\\n\\n", "\\n\\n", 1))
elif cmd == "clean":
    cues = [[a, b, re.sub(r"<[^>]+>", "", t).strip()] for a, b, t in parse(open(sys.argv[2], encoding="utf-8").read())]
    open(sys.argv[3], "w", encoding="utf-8").write(dump([c for c in cues if c[2]]))
elif cmd == "merge":
    a = parse(open(sys.argv[2], encoding="utf-8").read())
    b = parse(open(sys.argv[3], encoding="utf-8").read())
    off = a[-1][1] if a else 0
    open(sys.argv[4], "w", encoding="utf-8").write(dump(a + [[x + off, y + off, t] for x, y, t in b]))
else:
    sys.exit(__doc__)
''')
wr(b, "sample.srt", "1\n00:00:01,000 --> 00:00:03,000\n<i>Hello</i> there\n\n2\n00:00:04,000 --> 00:00:06,500\nSecond line\n\n3\n00:00:07,000 --> 00:00:08,000\n<b></b>\n")
w(b, "README.md", f"""
# SRT Tools
Four small subtitle commands: `shift` (fix timing by N seconds), `vtt` (convert to WebVTT), `clean` (strip HTML tags, drop empty cues, renumber),
`merge` (append one file after another). Run `python srt_tools.py` for usage. Works on standard SubRip files. Plain Python 3.

{LIC}""")
run(b, "srt_tools.py", "shift", "sample.srt", "s.srt", "2.5")
assert "00:00:03,500 --> 00:00:05,500" in (b / "s.srt").read_text()
run(b, "srt_tools.py", "clean", "sample.srt", "c.srt")
assert "<i>" not in (b / "c.srt").read_text() and (b / "c.srt").read_text().count("-->") == 2
run(b, "srt_tools.py", "vtt", "sample.srt", "v.vtt")
assert (b / "v.vtt").read_text().startswith("WEBVTT") and "00:00:01.000 --> 00:00:03.000" in (b / "v.vtt").read_text()
run(b, "srt_tools.py", "merge", "c.srt", "c.srt", "m.srt")
assert (b / "m.srt").read_text().count("-->") == 4
for f in ("s.srt", "c.srt", "v.vtt", "m.srt"):
    (b / f).unlink()
print("146", zip_pack("srt-tools"))

# ---------- 147: changelog generator ----------
b = OUT / "changelog-generator"
wr(b, "changelog.py", '''"""git log --pretty=%s v1.0..HEAD | python changelog.py "v1.1.0" > CHANGELOG-entry.md
Groups conventional-commit subjects (feat, fix, docs, perf, refactor, chore...) into a Markdown changelog entry. Stdlib only."""
import re, sys, datetime

TITLES = {"feat": "Added", "fix": "Fixed", "perf": "Performance", "docs": "Documentation", "refactor": "Changed", "test": "Tests", "chore": "Maintenance", "build": "Maintenance", "ci": "Maintenance"}
version = sys.argv[1] if len(sys.argv) > 1 else "Unreleased"
groups = {}
for line in sys.stdin.read().splitlines():
    m = re.match(r"^(\\w+)(\\(([^)]*)\\))?(!)?: (.+)$", line.strip())
    if not m:
        if line.strip():
            groups.setdefault("Other", []).append(line.strip())
        continue
    kind, scope, breaking, msg = m.group(1), m.group(3), m.group(4), m.group(5)
    key = "Breaking changes" if breaking else TITLES.get(kind, "Other")
    groups.setdefault(key, []).append((f"**{scope}:** " if scope else "") + msg)
order = ["Breaking changes", "Added", "Fixed", "Changed", "Performance", "Documentation", "Tests", "Maintenance", "Other"]
print(f"## {version} - {datetime.date.today().isoformat()}\\n")
for k in order:
    if k in groups:
        print(f"### {k}")
        for i in groups[k]:
            print(f"- {i}")
        print()
''')
w(b, "README.md", f"""
# Changelog Generator
    git log --pretty=%s v1.0..HEAD | python changelog.py "v1.1.0" > entry.md
Turns conventional-commit subjects (`feat(api): add search`, `fix: crash on empty input`, `feat!: drop v1`) into grouped Markdown:
Breaking changes, Added, Fixed, Changed and more. Reads from stdin, so it also works with any list of lines. Plain Python 3.

{LIC}""")
r = run(b, "changelog.py", "v1.1.0", stdin="feat(api): add search\nfix: crash on empty input\nfeat!: drop v1\nrandom message\n").stdout
assert "### Breaking changes" in r and "- **api:** add search" in r and "### Fixed" in r and "### Other" in r, r
print("147", zip_pack("changelog-generator"))

# ---------- 148: env/secrets linter ----------
b = OUT / "env-secrets-linter"
wr(b, "envlint.py", '''"""python envlint.py [folder]   Scans text files for likely committed secrets and .env problems. Offline, stdlib only.
Exit code 1 if anything is found, so it can run in CI or a git pre-commit hook. Heuristic: expect false positives and misses."""
import os, re, sys

RULES = [
    ("AWS access key id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |)PRIVATE KEY-----")),
    ("Slack token", re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}")),
    ("GitHub token", re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}")),
    ("Generic secret assignment", re.compile(r"(?i)(?:secret|password|passwd|api[_-]?key|token)\\s*[:=]\\s*['\\"]?[A-Za-z0-9/+_=-]{16,}['\\"]?")),
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
''')
w(b, "README.md", f"""
# Env and Secrets Linter
    python envlint.py .
Walks a folder and flags likely secrets (AWS key ids, private key blocks, Slack and GitHub tokens, generic `password=...` style assignments)
and `.env` files that should be git-ignored. Offline and dependency-free; exits 1 when it finds something, so it works in CI or a pre-commit hook.
Pattern-based: it will miss some secrets and flag some harmless strings. If a real secret leaks, rotate it; deleting the line is not enough.

{LIC}""")
t = b / "_fixture"
t.mkdir()
(t / "a.py").write_text('aws = "AKIA" + "ABCDEFGHIJKLMNOP"\nTOKEN = "abcd1234" + "abcd1234" + "abcd1234"\nprint("ok")\n')
(t / ".env").write_text("X=1\n")
r = subprocess.run([sys.executable, "envlint.py", str(t)], cwd=b, capture_output=True, text=True)
assert r.returncode == 1 and "AWS access key id" in r.stdout and "env file present" in r.stdout, r.stdout
clean = b / "_clean"
clean.mkdir()
(clean / "b.py").write_text("print('hello')\n")
assert subprocess.run([sys.executable, "envlint.py", str(clean)], cwd=b, capture_output=True).returncode == 0
shutil.rmtree(t)
shutil.rmtree(clean)
print("148", zip_pack("env-secrets-linter"))

# ---------- 143: sitemap generator ----------
b = OUT / "sitemap-and-link-checker"
wr(b, "sitemap_gen.py", '''"""python sitemap_gen.py ./site https://example.com   -> writes sitemap.xml and robots.txt into ./site, prints broken internal links.
Scans .html files; internal links to files that do not exist are reported. Stdlib only."""
import html, os, re, sys
from urllib.parse import urlparse, unquote

root, base = os.path.abspath(sys.argv[1]), sys.argv[2].rstrip("/")
pages = []
for d, _, files in os.walk(root):
    for f in files:
        if f.endswith(".html"):
            pages.append(os.path.relpath(os.path.join(d, f), root).replace(os.sep, "/"))
pages.sort()
urls = [base + "/" + ("" if p == "index.html" else p) for p in pages]
open(os.path.join(root, "sitemap.xml"), "w", encoding="utf-8").write(
    '<?xml version="1.0" encoding="UTF-8"?>\\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\\n' + "".join(f"  <url><loc>{html.escape(u)}</loc></url>\\n" for u in urls) + "</urlset>\\n")
open(os.path.join(root, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\\nAllow: /\\nSitemap: {base}/sitemap.xml\\n")
bad = 0
for p in pages:
    text = open(os.path.join(root, p), encoding="utf-8").read()
    for href in re.findall(r"""href=["']([^"'#?]+)""", text):
        u = urlparse(href)
        if u.scheme or href.startswith(("mailto:", "tel:", "//")):
            continue
        target = os.path.normpath(os.path.join(root, os.path.dirname(p), unquote(href))) if not href.startswith("/") else os.path.join(root, href.lstrip("/"))
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            print(f"broken link in {p}: {href}")
            bad += 1
print(f"{len(pages)} page(s), {bad} broken internal link(s)", file=sys.stderr)
sys.exit(1 if bad else 0)
''')
w(b, "README.md", f"""
# Sitemap and Link Checker
    python sitemap_gen.py ./my-site https://example.com
Writes `sitemap.xml` and `robots.txt` for a folder of static HTML pages and reports internal links that point to files that do not exist.
Does not check external links or links generated by JavaScript. Plain Python 3.

{LIC}""")
s = b / "_site"
s.mkdir()
(s / "index.html").write_text("<a href='about.html'>a</a> <a href='missing.html'>m</a> <a href='https://x.com'>x</a>")
(s / "about.html").write_text("<a href='index.html'>home</a>")
r = subprocess.run([sys.executable, "sitemap_gen.py", str(s), "https://example.com"], cwd=b, capture_output=True, text=True)
assert r.returncode == 1 and "missing.html" in r.stdout and "about.html" in (s / "sitemap.xml").read_text() and "Sitemap:" in (s / "robots.txt").read_text(), (r.stdout, r.stderr)
shutil.rmtree(s)
print("143", zip_pack("sitemap-and-link-checker"))

# ---------- 137: SQL practice pack ----------
b = OUT / "sql-practice-pack"
b.mkdir(parents=True)
db = b / "shop.db"
con = sqlite3.connect(db)
con.executescript("""
create table customers(id integer primary key, name text, city text, signup date);
create table products(id integer primary key, name text, category text, price real);
create table orders(id integer primary key, customer_id integer, order_date date, status text);
create table order_items(order_id integer, product_id integer, qty integer);
""")
import random
rnd = random.Random(11)
cities = ["Austin", "Boston", "Chicago", "Denver", "Seattle"]
for i in range(1, 41):
    con.execute("insert into customers values (?,?,?,?)", (i, f"Customer {i}", rnd.choice(cities), f"2026-{rnd.randint(1, 9):02d}-{rnd.randint(1, 28):02d}"))
cats = {"Books": 15, "Games": 30, "Tools": 45}
for i in range(1, 16):
    c = rnd.choice(list(cats))
    con.execute("insert into products values (?,?,?,?)", (i, f"Product {i}", c, round(cats[c] * rnd.uniform(0.6, 1.6), 2)))
for i in range(1, 121):
    con.execute("insert into orders values (?,?,?,?)", (i, rnd.randint(1, 40), f"2026-{rnd.randint(1, 9):02d}-{rnd.randint(1, 28):02d}", rnd.choice(["paid", "paid", "paid", "refunded", "pending"])))
    for _ in range(rnd.randint(1, 3)):
        con.execute("insert into order_items values (?,?,?)", (i, rnd.randint(1, 15), rnd.randint(1, 4)))
con.commit()
EX = [
    ("List all customers from Austin.", "select * from customers where city = 'Austin' order by id"),
    ("Count customers per city, largest first.", "select city, count(*) n from customers group by city order by n desc, city"),
    ("List products over $40, most expensive first.", "select name, price from products where price > 40 order by price desc"),
    ("What is the average product price per category?", "select category, round(avg(price), 2) avg_price from products group by category order by category"),
    ("How many orders are in each status?", "select status, count(*) n from orders group by status order by status"),
    ("Show each order with the customer's name (join).", "select o.id, c.name from orders o join customers c on c.id = o.customer_id order by o.id"),
    ("Total quantity sold per product name.", "select p.name, sum(oi.qty) qty from order_items oi join products p on p.id = oi.product_id group by p.name order by qty desc, p.name"),
    ("Revenue per order for paid orders (qty x price).", "select o.id, round(sum(oi.qty * p.price), 2) revenue from orders o join order_items oi on oi.order_id = o.id join products p on p.id = oi.product_id where o.status = 'paid' group by o.id order by o.id"),
    ("Top 5 customers by number of orders.", "select c.name, count(*) n from orders o join customers c on c.id = o.customer_id group by c.id order by n desc, c.name limit 5"),
    ("Customers who never ordered.", "select c.name from customers c left join orders o on o.customer_id = c.id where o.id is null order by c.id"),
    ("Orders per month.", "select substr(order_date, 1, 7) month, count(*) n from orders group by month order by month"),
    ("Categories with more than 4 products.", "select category, count(*) n from products group by category having n > 4 order by category"),
    ("Most expensive product in each category.", "select p.category, p.name, p.price from products p where p.price = (select max(price) from products where category = p.category) order by p.category"),
    ("Customers who bought a Tools product.", "select distinct c.name from customers c join orders o on o.customer_id = c.id join order_items oi on oi.order_id = o.id join products p on p.id = oi.product_id where p.category = 'Tools' order by c.name"),
    ("Running total of orders by month.", "select month, n, sum(n) over (order by month) running from (select substr(order_date, 1, 7) month, count(*) n from orders group by month) order by month"),
    ("Rank products by units sold (window function).", "select name, qty, rank() over (order by qty desc) rnk from (select p.name, sum(oi.qty) qty from order_items oi join products p on p.id = oi.product_id group by p.name) order by rnk, name"),
    ("Refund rate: share of orders that are refunded.", "select round(100.0 * sum(status = 'refunded') / count(*), 1) pct from orders"),
    ("Customers whose first order was in the first quarter of the year.", "select c.name from customers c join (select customer_id, min(order_date) first_order from orders group by customer_id) f on f.customer_id = c.id where f.first_order < '2026-04-01' order by c.name"),
    ("Average order value (paid orders only).", "select round(avg(rev), 2) aov from (select o.id, sum(oi.qty * p.price) rev from orders o join order_items oi on oi.order_id = o.id join products p on p.id = oi.product_id where o.status = 'paid' group by o.id)"),
    ("Orders containing more than one distinct product.", "select order_id, count(distinct product_id) n from order_items group by order_id having n > 1 order by order_id"),
]
q, a = ["# SQL Practice Pack: exercises\n\nOpen `shop.db` in SQLite (DB Browser for SQLite, or `sqlite3 shop.db`). Tables: customers, products, orders, order_items. Try each before reading answers.md.\n"], ["# Answers\n\nOne valid answer per exercise; yours may differ if it returns the same rows.\n"]
for i, (text, sql) in enumerate(EX, 1):
    rows = con.execute(sql).fetchall()
    assert rows is not None
    q.append(f"\n## {i}. {text}\n")
    a.append(f"\n## {i}. {text}\n```sql\n{sql};\n```\nReturns {len(rows)} row(s).\n")
con.close()
wr(b, "exercises.md", "".join(q))
wr(b, "answers.md", "".join(a))
w(b, "README.md", f"""
# SQL Practice Pack
A small shop database (40 customers, 15 products, 120 orders) as a SQLite file plus {len(EX)} exercises, from simple filters to joins, grouping,
subqueries and window functions. Every answer in `answers.md` was executed against the database when the pack was built. Needs SQLite 3.25+ for window functions.
All data is generated and fictional.

{LIC}""")
print("137", len(EX), "exercises", zip_pack("sql-practice-pack"))
