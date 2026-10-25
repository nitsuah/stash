"""Batch 1 pack builder (ideas 28, 35, 86, 87, 90, 93). Stdlib only. Run in python:3-slim: python build_batch1.py"""
import json
import pathlib
import shutil
import subprocess
import sys
import textwrap
import zipfile

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"

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


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # ---------- 28: Obsidian freelancer vault ----------
    b = OUT / "obsidian-freelancer-vault"
    w(b, "README.md", f"""
    # Obsidian Freelancer Vault
    Open this folder as a vault in Obsidian (free). Notes link to each other; no plugins required.
    Optional: the Dataview plugin turns the tables in Dashboard.md live.

    ## Folders
    - Clients/ one note per client (copy Templates/Client.md)
    - Projects/ one note per project (copy Templates/Project.md)
    - Meetings/ meeting notes (Templates/Meeting.md)
    - Reviews/ weekly reviews (Templates/Weekly review.md)

    {LIC}""")
    w(b, "Dashboard.md", """
    # Dashboard
    ## Active projects (Dataview)
    ```dataview
    TABLE client, status, due FROM "Projects" WHERE status != "done" SORT due ASC
    ```
    ## Clients
    ```dataview
    LIST FROM "Clients"
    ```
    Without Dataview, open the Projects and Clients folders directly.
    """)
    w(b, "Templates/Client.md", """
    ---
    type: client
    status: lead
    email:
    rate:
    ---
    # Client name
    ## Context
    ## Contacts
    ## Projects
    - [[ ]]
    ## Notes
    """)
    w(b, "Templates/Project.md", """
    ---
    type: project
    client: "[[ ]]"
    status: active
    due:
    fixed_price:
    ---
    # Project name
    ## Scope
    - [ ]
    ## Out of scope
    ## Milestones
    - [ ]
    ## Log
    """)
    w(b, "Templates/Meeting.md", """
    # Meeting - {{date}}
    **With:** [[ ]]
    ## Agenda
    ## Notes
    ## Decisions
    ## Next actions
    - [ ]
    """)
    w(b, "Templates/Weekly review.md", """
    # Weekly review - week of {{date}}
    ## Done
    ## Money in / out
    ## Waiting on others
    ## Next week's top 3
    1.
    2.
    3.
    ## What to stop doing
    """)
    w(b, "Clients/Example Client.md", """
    ---
    type: client
    status: active
    ---
    # Example Client
    Sample note. Duplicate Templates/Client.md for real clients.
    ## Projects
    - [[Example Project]]
    """)
    w(b, "Projects/Example Project.md", """
    ---
    type: project
    client: "[[Example Client]]"
    status: active
    due: 2026-12-01
    ---
    # Example Project
    ## Scope
    - [x] Kickoff call
    - [ ] First draft
    """)
    print("28", zip_pack("obsidian-freelancer-vault"))

    # ---------- 35: printable planners ----------
    b = OUT / "printable-planners"
    css = """
    @page{size:letter;margin:.5in}
    body{font:14px/1.4 system-ui,Segoe UI,Arial,sans-serif;color:#111;margin:0;padding:24px;max-width:8in}
    h1{font-size:22px;margin:0 0 4px}.sub{color:#444;margin-bottom:16px}
    table{border-collapse:collapse;width:100%}th,td{border:1px solid #333;padding:6px;vertical-align:top}
    th{background:#eee;text-align:left}.lines div{border-bottom:1px solid #999;height:28px}
    .box{display:inline-block;width:14px;height:14px;border:1.5px solid #111;margin-right:8px;vertical-align:middle}
    @media print{body{padding:0}}
    """


    def page(name, title, body):
        w(b, name, f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title}</title><style>{css}</style></head><body><main>{body}</main></body></html>")


    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    page("weekly-planner.html", "Weekly planner", "<h1>Weekly planner</h1><div class='sub'>Week of: ______________</div><table><tr><th>Day</th><th>Top 3</th><th>Notes</th></tr>" + "".join(f"<tr style='height:72px'><td>{d}</td><td></td><td></td></tr>" for d in days) + "</table>")
    page("daily-planner.html", "Daily planner", "<h1>Daily planner</h1><div class='sub'>Date: ______________</div><h2>Top 3</h2>" + "".join("<p><span class='box'></span></p>" for _ in range(3)) + "<h2>Schedule</h2><table>" + "".join(f"<tr><td style='width:70px'>{h}:00</td><td></td></tr>" for h in range(7, 20)) + "</table><h2>Notes</h2><div class='lines'>" + "<div></div>" * 5 + "</div>")
    page("habit-tracker.html", "Habit tracker", "<h1>Habit tracker</h1><div class='sub'>Month: ______________</div><table><tr><th>Habit</th>" + "".join(f"<th style='padding:2px;text-align:center'>{i}</th>" for i in range(1, 32)) + "</tr>" + "".join("<tr style='height:30px'><td></td>" + "<td></td>" * 31 + "</tr>" for _ in range(8)) + "</table>")
    page("monthly-budget.html", "Monthly budget", "<h1>Monthly budget</h1><div class='sub'>Month: ______________</div><table><tr><th>Category</th><th>Planned</th><th>Actual</th><th>Difference</th></tr>" + "".join(f"<tr style='height:30px'><td>{c}</td><td></td><td></td><td></td></tr>" for c in ["Income", "Rent / housing", "Utilities", "Food", "Transport", "Software & tools", "Taxes set aside", "Savings", "Other"]) + "</table>")
    w(b, "README.txt", "Open any .html file in a browser and print (Letter size; change @page size to A4 in the style block if needed). Fill by hand or on screen.\n\n" + LIC)
    print("35", zip_pack("printable-planners"))

    # ---------- 86: menu website template ----------
    b = OUT / "menu-website-template"
    w(b, "menu.json", json.dumps({
        "name": "Corner Cafe", "tagline": "Fresh baked daily", "phone": "Phone not provided", "address": "123 Main Street, Your Town",
        "hours": ["Mon-Fri 7am-4pm", "Sat-Sun 8am-2pm"],
        "sections": [{"title": "Breakfast", "items": [{"name": "Egg sandwich", "price": "7.50", "note": "Cheddar, brioche"}, {"name": "Granola bowl", "price": "6.00", "note": "Yogurt, berries"}]},
                     {"title": "Coffee", "items": [{"name": "Drip coffee", "price": "2.75", "note": ""}, {"name": "Latte", "price": "4.50", "note": "Oat milk available"}]}]
    }, indent=2))
    BUILD_MENU = '''"""Build an accessible one-page menu site: python build.py  (reads menu.json, writes index.html)"""
    import json, html
    d = json.load(open("menu.json", encoding="utf-8"))
    e = html.escape
    secs = "".join(
        f"<section aria-labelledby='s{i}'><h2 id='s{i}'>{e(s['title'])}</h2><ul>"
        + "".join(f"<li><span class='p'>${e(it['price'])}</span><span class='n'>{e(it['name'])}</span>" + (f"<br><span class='d'>{e(it['note'])}</span>" if it['note'] else "") + "</li>" for it in s["items"])
        + "</ul></section>" for i, s in enumerate(d["sections"]))
    hours = "".join(f"<li>{e(h)}</li>" for h in d["hours"])
    phone = d.get("phone", "")
    phone_html = f"<a href='tel:{e(phone)}'>{e(phone)}</a>" if sum(ch.isdigit() for ch in phone) >= 7 else e(phone)
    CSS = ":root{--bg:#fffdf8;--fg:#1d1b18;--accent:#7a2e0e}body{margin:0;background:var(--bg);color:var(--fg);font:18px/1.6 system-ui,sans-serif}header,main,footer{max-width:42rem;margin:auto;padding:1.5rem}a{color:var(--accent)}h1,h2{color:var(--accent)}ul{list-style:none;padding:0}li{margin:.6rem 0}.p{float:right;font-weight:600}.d{color:#4a4640;font-size:.9em}.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.5rem}"
    page = (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{e(d['name'])} menu</title><meta name='description' content='{e(d['name'])}: menu, hours and location.'><style>{CSS}</style></head><body>"
        "<a class='skip' href='#main'>Skip to menu</a>"
        f"<header><h1>{e(d['name'])}</h1><p>{e(d['tagline'])}</p></header>"
        f"<main id='main'>{secs}</main>"
        f"<footer><h2>Visit us</h2><p>{e(d['address'])}<br>{phone_html}</p><ul>{hours}</ul></footer></body></html>"
    )
    open("index.html", "w", encoding="utf-8").write(page)
    print("wrote index.html")
    '''
    (b / "build.py").write_text(BUILD_MENU, encoding="utf-8")
    w(b, "README.md", f"""
    # Menu Website Template
    Edit `menu.json` (name, hours, sections, items), run `python build.py`, upload `index.html` anywhere (Netlify drag-and-drop works).
    Accessibility basics built in: skip link, landmarks, heading order, high contrast, labelled sections.
    Run an automated check (axe-core) after you change colors.

    {LIC}""")
    subprocess.run([sys.executable, "build.py"], cwd=b, check=True)
    print("86", zip_pack("menu-website-template"))

    # ---------- 87: JSON-LD generator ----------
    b = OUT / "local-seo-jsonld-generator"
    w(b, "business.json", json.dumps({
        "type": "LocalBusiness", "name": "Corner Cafe", "url": "https://example.com", "telephone": "Phone not provided",
        "address": {"street": "123 Main Street", "city": "Your Town", "state": "VA", "zip": "20000", "country": "US"},
        "hours": [{"days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "07:00", "closes": "16:00"}, {"days": ["Saturday", "Sunday"], "opens": "08:00", "closes": "14:00"}],
        "priceRange": "$$", "sameAs": ["https://www.facebook.com/yourpage"]}, indent=2))
    (b / "make_jsonld.py").write_text('''"""python make_jsonld.py business.json > snippet.html  : paste the output into your page <head>."""
    import json, sys
    b = json.load(open(sys.argv[1], encoding="utf-8"))
    missing = [k for k in ("name", "url", "telephone") if not b.get(k)]
    if missing:
        sys.exit("missing: " + ", ".join(missing))
    a = b["address"]
    data = {"@context": "https://schema.org", "@type": b.get("type", "LocalBusiness"), "name": b["name"], "url": b["url"], "telephone": b["telephone"],
            "address": {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["city"], "addressRegion": a["state"], "postalCode": a["zip"], "addressCountry": a["country"]},
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"], "opens": h["opens"], "closes": h["closes"]} for h in b["hours"]]}
    for k in ("priceRange", "sameAs"):
        if b.get(k):
            data[k] = b[k]
    print('<script type="application/ld+json">')
    print(json.dumps(data, indent=2).replace("<", "\\u003c"))
    print("</script>")
    ''', encoding="utf-8")
    w(b, "README.md", f"""
    # Local SEO JSON-LD Generator
    Fill `business.json`, run `python make_jsonld.py business.json > snippet.html`, paste the snippet into your site's head.
    Then test with Google's Rich Results Test or the Schema.org validator. Structured data helps search engines understand your
    business; it does not guarantee rankings.
    Types: LocalBusiness, Restaurant, CafeOrCoffeeShop, Store, and other schema.org subtypes (set "type").

    {LIC}""")
    r = subprocess.run([sys.executable, "make_jsonld.py", "business.json"], cwd=b, capture_output=True, text=True, check=True)
    body = r.stdout.split("\n", 1)[1].rsplit("\n</script>", 1)[0]
    json.loads(body)  # validates the generated JSON
    print("87", zip_pack("local-seo-jsonld-generator"))

    # ---------- 90: flyer generator ----------
    b = OUT / "event-flyer-generator"
    w(b, "flyer.json", json.dumps({"title": "Open Mic Night", "subtitle": "Every Friday", "date": "Fri 7pm", "place": "Corner Cafe, 123 Main St", "details": ["Free entry", "Sign up at the counter"], "bg": "#0f1720", "fg": "#f5f7fa", "accent": "#10b981"}, indent=2))
    (b / "make_flyer.py").write_text('''"""python make_flyer.py flyer.json  -> flyer.svg (Letter, 816x1056). Open in a browser and print, or import into Inkscape."""
    import json, sys, html
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    e = html.escape
    lines = "".join(f"<text x='408' y='{760 + i * 52}' text-anchor='middle' font-size='34' fill='{d['fg']}'>{e(t)}</text>" for i, t in enumerate(d["details"]))
    svg = (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='816' height='1056' viewBox='0 0 816 1056' role='img' aria-label='{e(d['title'])} flyer'>"
        f"<rect width='816' height='1056' fill='{d['bg']}'/><rect x='48' y='48' width='720' height='960' fill='none' stroke='{d['accent']}' stroke-width='8'/>"
        f"<text x='408' y='330' text-anchor='middle' font-family='sans-serif' font-weight='700' font-size='96' fill='{d['fg']}'>{e(d['title'])}</text>"
        f"<text x='408' y='430' text-anchor='middle' font-family='sans-serif' font-size='48' fill='{d['accent']}'>{e(d['subtitle'])}</text>"
        f"<text x='408' y='590' text-anchor='middle' font-family='sans-serif' font-weight='700' font-size='64' fill='{d['fg']}'>{e(d['date'])}</text>"
        f"<text x='408' y='660' text-anchor='middle' font-family='sans-serif' font-size='40' fill='{d['fg']}'>{e(d['place'])}</text>"
        f"<g font-family='sans-serif'>{lines}</g></svg>"
    )
    open("flyer.svg", "w", encoding="utf-8").write(svg)
    print("wrote flyer.svg")
    ''', encoding="utf-8")
    w(b, "README.md", f"""
    # Event Flyer Generator
    Edit `flyer.json` (title, date, place, colors), run `python make_flyer.py flyer.json`, open `flyer.svg` in a browser and print.
    Pick colors with strong contrast so the flyer is readable from a distance.

    {LIC}""")
    subprocess.run([sys.executable, "make_flyer.py", "flyer.json"], cwd=b, check=True)
    print("90", zip_pack("event-flyer-generator"))

    # ---------- 93: social image templates ----------
    b = OUT / "social-image-templates"
    w(b, "posts.json", json.dumps({"brand": {"bg": "#0f1720", "fg": "#f5f7fa", "accent": "#10b981", "name": "Your Brand"},
                                   "posts": [{"slug": "tip-1", "headline": "Invoice on day one", "sub": "Do not wait for the work to finish."}, {"slug": "tip-2", "headline": "Write the scope down", "sub": "Out of scope matters most."}]}, indent=2))
    (b / "make_cards.py").write_text('''"""python make_cards.py posts.json -> out/<slug>_square|story|wide.svg (1080x1080, 1080x1920, 1200x630)."""
    import json, sys, html, pathlib, re
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    b = d["brand"]
    e = html.escape
    pathlib.Path("out").mkdir(exist_ok=True)
    SIZES = {"square": (1080, 1080), "story": (1080, 1920), "wide": (1200, 630)}
    for p in d["posts"]:
        slug = p.get("slug", "")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", slug):
            raise SystemExit(f"Invalid post slug: {slug!r}")
        for name, (W, H) in SIZES.items():
            fs = max(40, min(H // 8, int(W * 0.85 / max(len(p["headline"]), 1) / 0.55)))
            svg = (
                f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}' role='img' aria-label='{e(p['headline'])}'>"
                f"<rect width='{W}' height='{H}' fill='{b['bg']}'/><rect x='0' y='0' width='{W}' height='{H // 60 + 6}' fill='{b['accent']}'/>"
                f"<text x='{W // 2}' y='{H // 2}' text-anchor='middle' font-family='sans-serif' font-weight='700' font-size='{fs}' fill='{b['fg']}'>{e(p['headline'])}</text>"
                f"<text x='{W // 2}' y='{H // 2 + fs}' text-anchor='middle' font-family='sans-serif' font-size='{fs // 2}' fill='{b['accent']}'>{e(p['sub'])}</text>"
                f"<text x='{W // 2}' y='{H - H // 14}' text-anchor='middle' font-family='sans-serif' font-size='{max(24, H // 32)}' fill='{b['fg']}'>{e(b['name'])}</text></svg>"
            )
            pathlib.Path(f"out/{slug}_{name}.svg").write_text(svg, encoding="utf-8")
    print("wrote", len(d["posts"]) * 3, "cards")
    ''', encoding="utf-8")
    w(b, "README.md", f"""
    # Social Image Templates
    Three sizes per post (square, story, wide) from one JSON file. Edit `posts.json`, run `python make_cards.py posts.json`.
    SVGs open in any browser and export to PNG from Inkscape or the browser's screenshot tool.
    Keep headlines short; the script shrinks the type to fit.

    {LIC}""")
    subprocess.run([sys.executable, "make_cards.py", "posts.json"], cwd=b, check=True)
    shutil.rmtree(b / "out")
    print("93", zip_pack("social-image-templates"))


if __name__ == "__main__":
    main()
