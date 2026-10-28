"""python sitemap_gen.py ./site https://example.com   -> writes sitemap.xml and robots.txt into ./site, prints broken internal links.
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
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{html.escape(u)}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(root, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n")
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
