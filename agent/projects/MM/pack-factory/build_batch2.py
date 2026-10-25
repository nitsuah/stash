"""Batch 2 pack builder (ideas 30, 33, 34, 39, 64, 89, 108, 109, 113, 115). Stdlib only. Run in python:3-slim."""
import json
import math
import pathlib
import random
import shutil
import struct
import subprocess
import sys
import textwrap
import wave
import zipfile
import zlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out2"

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
    shutil.rmtree(OUT, ignore_errors=True)
    # ---------- 30: sound effects ----------
    b = OUT / "retro-sound-effects-pack"
    b.mkdir(parents=True)
    SR = 22050


    def synth(path, dur, f0, f1=None, shape="square", vol=0.5, noise=False, decay=3.0):
        f1 = f1 or f0
        n = int(SR * dur)
        frames = bytearray()
        phase = 0.0
        rnd = random.Random(7)
        for i in range(n):
            t = i / n
            f = f0 + (f1 - f0) * t
            phase += 2 * math.pi * f / SR
            if noise:
                s = rnd.uniform(-1, 1)
            elif shape == "square":
                s = 1.0 if math.sin(phase) >= 0 else -1.0
            elif shape == "saw":
                s = 2 * ((phase / (2 * math.pi)) % 1) - 1
            else:
                s = math.sin(phase)
            env = (1 - t) ** decay if decay else 1.0
            env *= min(1.0, i / 80)
            frames += struct.pack("<h", int(max(-1, min(1, s * env * vol)) * 32767))
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SR)
            wf.writeframes(bytes(frames))


    SFX = {
        "coin": (0.25, 988, 1319, "square", 0.4, False, 2.0), "jump": (0.3, 300, 700, "square", 0.4, False, 2.5),
        "laser": (0.35, 1800, 200, "saw", 0.35, False, 2.0), "explosion": (0.9, 200, 50, "square", 0.6, True, 2.0),
        "hit": (0.2, 220, 80, "square", 0.5, True, 3.0), "powerup": (0.6, 330, 1320, "square", 0.4, False, 1.0),
        "click": (0.05, 1200, 1200, "square", 0.3, False, 1.0), "notify": (0.4, 880, 1175, "sine", 0.5, False, 2.0),
        "error": (0.35, 200, 150, "saw", 0.45, False, 1.5), "success": (0.5, 523, 1046, "sine", 0.5, False, 1.5),
        "blip": (0.1, 600, 800, "square", 0.3, False, 2.0), "fall": (0.7, 800, 100, "sine", 0.5, False, 1.0),
        "swoosh": (0.4, 500, 2000, "saw", 0.2, True, 2.0), "pickup": (0.2, 700, 1400, "square", 0.35, False, 2.0),
        "death": (1.0, 400, 60, "saw", 0.5, False, 1.2), "select": (0.08, 900, 900, "sine", 0.4, False, 1.5),
    }
    for name, args in SFX.items():
        synth(b / f"{name}.wav", *args)
    w(b, "README.txt", "16 retro sound effects (22.05 kHz mono WAV), generated from code and original. Works in any game engine, video editor or app.\nLoop or layer them; pitch-shift for variations.\n\n" + LIC)
    print("30", len(SFX), "wavs", zip_pack("retro-sound-effects-pack"))

    # ---------- 34: pixel sprites ----------
    b = OUT / "pixel-sprite-pack"
    b.mkdir(parents=True)
    PAL = {".": None, "r": (214, 48, 49), "y": (253, 203, 110), "o": (225, 112, 85), "g": (0, 184, 148), "b": (9, 132, 227), "k": (45, 52, 54), "w": (255, 255, 255), "n": (133, 94, 66), "p": (162, 155, 254), "s": (178, 190, 195)}
    SPR = {
        "heart": [".rr..rr.", "rrrrrrrr", "rrrrrrrr", "rrrrrrrr", ".rrrrrr.", "..rrrr..", "...rr...", "........"],
        "star": ["...yy...", "...yy...", "yyyyyyyy", ".yyyyyy.", "..yyyy..", ".yy..yy.", "yy....yy", "........"],
        "coin": ["..yyyy..", ".yyooyy.", "yyyoyyyy", "yyyoyyyy", "yyyoyyyy", "yyyooyyy", ".yyyyyy.", "..yyyy.."],
        "key": ["..yyy...", ".y...y..", ".y...y..", "..yyy...", "...y....", "...yy...", "...y....", "...yy..."],
        "sword": ["......ss", ".....sss", "....sss.", "s..sss..", ".sss....", "..sn....", ".nn.n...", "n.......".replace("n", "n")],
        "potion": ["...kk...", "...ss...", "..gggg..", ".gggggg.", ".gggggg.", ".gggggg.", "..gggg..", "........"],
        "mushroom": ["..rrrr..", ".rwrrwr.", "rrrrrrrr", "rwrrrrwr", "..wwww..", "..wwww..", "...ww...", "........"],
        "slime": ["........", "..gggg..", ".gggggg.", "gkggggkg", "gggggggg", "gggggggg", ".gggggg.", "........"],
        "tree": ["..gggg..", ".gggggg.", "gggggggg", ".gggggg.", "..gggg..", "...nn...", "...nn...", "..nnnn.."],
        "chest": [".nnnnnn.", "nnnnnnnn", "nyyyyyyn", "nnnynnnn", "nnnynnnn", "nnnnnnnn", "nnnnnnnn", "........"],
        "gem": ["..bbbb..", ".bwbbbb.", "bbwbbbbb", ".bbbbbb.", "..bbbb..", "...bb...", "........", "........"],
        "skull": [".wwwwww.", "wwwwwwww", "wkkwwkkw", "wkkwwkkw", "wwwwwwww", ".wwkkww.", ".wwwwww.", ".w.w.w.."],
    }


    def png(path, rows, scale):
        h, wd = len(rows), len(rows[0])
        raw = bytearray()
        for row in rows:
            line = bytearray()
            for ch in row:
                c = PAL[ch]
                px = bytes(c) + b"\xff" if c else b"\x00\x00\x00\x00"
                line += px * scale
            for _ in range(scale):
                raw += b"\x00" + line
        def chunk(t, d):
            c = struct.pack(">I", len(d)) + t + d
            return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
        data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", wd * scale, h * scale, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(bytes(raw))) + chunk(b"IEND", b"")
        path.write_bytes(data)


    for name, rows in SPR.items():
        assert len(rows) == 8 and all(len(r) == 8 for r in rows), name
        png(b / f"{name}_128.png", rows, 16)
        png(b / f"{name}_32.png", rows, 4)
    w(b, "README.txt", "12 original 8x8 pixel sprites as transparent PNG, at 32px and 128px (nearest-neighbor scaled). Use in games, UI or social graphics.\n\n" + LIC)
    print("34", len(SPR) * 2, "pngs", zip_pack("pixel-sprite-pack"))

    # ---------- 39: generative wall art ----------
    b = OUT / "geometric-wall-art-set"
    b.mkdir(parents=True)
    SCHEMES = [("#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"), ("#1d3557", "#457b9d", "#a8dadc", "#f1faee", "#e63946"),
               ("#2b2d42", "#8d99ae", "#edf2f4", "#ef233c", "#d90429"), ("#003049", "#d62828", "#f77f00", "#fcbf49", "#eae2b7"),
               ("#22223b", "#4a4e69", "#9a8c98", "#c9ada7", "#f2e9e4")]
    for i, pal in enumerate(SCHEMES, 1):
        rnd = random.Random(i * 101)
        Wd, Ht = 1800, 2400
        parts = [f"<rect width='{Wd}' height='{Ht}' fill='{pal[4] if i % 2 else pal[3]}'/>"]
        for _ in range(14):
            c = rnd.choice(pal[:4])
            x, y, r = rnd.randint(100, Wd - 100), rnd.randint(200, Ht - 200), rnd.randint(120, 520)
            kind = rnd.choice(["circle", "rect", "arc"])
            if kind == "circle":
                parts.append(f"<circle cx='{x}' cy='{y}' r='{r}' fill='{c}' opacity='0.85'/>")
            elif kind == "rect":
                parts.append(f"<rect x='{x - r}' y='{y - r // 2}' width='{r * 2}' height='{r}' fill='{c}' opacity='0.85'/>")
            else:
                parts.append(f"<path d='M{x - r} {y} A{r} {r} 0 0 1 {x + r} {y} Z' fill='{c}' opacity='0.9'/>")
        svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='{Wd}' height='{Ht}' viewBox='0 0 {Wd} {Ht}' role='img' aria-label='Geometric abstract poster {i}'>{''.join(parts)}</svg>"
        (b / f"poster-{i}.svg").write_text(svg, encoding="utf-8")
    w(b, "README.txt", "5 original geometric posters as SVG (3:4, scales to any print size; 18x24 in works well). Open in a browser or Inkscape, export PNG/PDF for print shops.\nColors are editable in any text editor.\n\n" + LIC)
    print("39", len(SCHEMES), "svgs", zip_pack("geometric-wall-art-set"))

    # ---------- 89: chart generator ----------
    b = OUT / "csv-to-svg-charts"
    w(b, "data.csv", "label,value\nQ1,120\nQ2,180\nQ3,150\nQ4,210\n")
    (b / "make_chart.py").write_text('''"""python make_chart.py data.csv "Chart title" > chart.svg   (bar chart; pass --horizontal for horizontal bars)"""
    import csv, html, sys
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    horiz = "--horizontal" in sys.argv
    rows = [(r["label"], float(r["value"])) for r in csv.DictReader(open(args[0], encoding="utf-8-sig"))]
    if not rows:
        raise SystemExit("CSV must contain at least one data row")
    if any(value < 0 for _, value in rows):
        raise SystemExit("Negative chart values are not supported; provide nonnegative values")
    title = html.escape(args[1] if len(args) > 1 else "Chart")
    W, H, M = 800, 480, 60
    mx = max(v for _, v in rows) or 1
    out = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}' role='img' aria-label='{title}'>",
           f"<rect width='{W}' height='{H}' fill='#ffffff'/><text x='{W // 2}' y='34' text-anchor='middle' font-family='sans-serif' font-size='22' font-weight='700' fill='#111'>{title}</text>"]
    n = len(rows)
    for i, (lab, v) in enumerate(rows):
        if horiz:
            bh = (H - 2 * M) / n * 0.7
            y = M + i * (H - 2 * M) / n
            bw = (W - 2 * M - 80) * v / mx
            out.append(f"<text x='{M - 6}' y='{y + bh / 2 + 5}' text-anchor='end' font-family='sans-serif' font-size='14' fill='#111'>{html.escape(lab)}</text><rect x='{M}' y='{y}' width='{bw}' height='{bh}' fill='#1d4ed8'/><text x='{M + bw + 6}' y='{y + bh / 2 + 5}' font-family='sans-serif' font-size='14' fill='#111'>{v:g}</text>")
        else:
            bw = (W - 2 * M) / n * 0.7
            x = M + i * (W - 2 * M) / n + (W - 2 * M) / n * 0.15
            bh = (H - 2 * M - 30) * v / mx
            y = H - M - bh
            out.append(f"<rect x='{x}' y='{y}' width='{bw}' height='{bh}' fill='#1d4ed8'/><text x='{x + bw / 2}' y='{y - 6}' text-anchor='middle' font-family='sans-serif' font-size='14' fill='#111'>{v:g}</text><text x='{x + bw / 2}' y='{H - M + 20}' text-anchor='middle' font-family='sans-serif' font-size='14' fill='#111'>{html.escape(lab)}</text>")
    out.append("</svg>")
    print("".join(out))
    ''', encoding="utf-8")
    w(b, "README.md", f"""
    # CSV to SVG Charts
    `python make_chart.py data.csv "Quarterly sales" > chart.svg` (add `--horizontal` for horizontal bars).
    CSV needs `label,value` columns with nonnegative numeric values. Output is a plain SVG with a title and text labels (accessible, prints sharply).
    Plain Python 3, no installs.

    {LIC}""")
    for flag in ([], ["--horizontal"]):
        r = subprocess.run([sys.executable, "make_chart.py", "data.csv", "Test"] + flag, cwd=b, capture_output=True, text=True, check=True)
        assert r.stdout.startswith("<svg") and r.stdout.rstrip().endswith("</svg>")
    print("89", zip_pack("csv-to-svg-charts"))

    # ---------- 64: freelancer calculators ----------
    b = OUT / "freelancer-calculators"
    CALC_CSS = "body{font:18px/1.5 system-ui,sans-serif;max-width:34rem;margin:2rem auto;padding:0 1rem;color:#111;background:#fff}label{display:block;margin:.8rem 0 .2rem;font-weight:600}input{font:inherit;padding:.4rem;width:100%;box-sizing:border-box}output{display:block;margin-top:1.2rem;padding:1rem;background:#eef2ff;border-radius:6px;font-size:1.3rem}h1{font-size:1.5rem}"


    def calc(name, title, fields, js, note):
        inputs = "".join(f"<label for='{i}'>{lab}</label><input id='{i}' type='number' step='any' value='{v}'>" for i, lab, v in fields)
        html_ = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title}</title><style>{CALC_CSS}</style></head>"
                 f"<body><main><h1>{title}</h1>{inputs}<output id='out' aria-live='polite'></output><p>{note}</p></main>"
                 f"<script>const $=i=>parseFloat(document.getElementById(i).value)||0;function run(){{{js}}}document.querySelectorAll('input').forEach(e=>e.addEventListener('input',run));run();</script></body></html>")
        w(b, name, html_)


    calc("hourly-rate.html", "Hourly rate calculator", [("income", "Target yearly income ($)", 80000), ("expenses", "Yearly business expenses ($)", 12000), ("hours", "Billable hours per week", 25), ("weeks", "Working weeks per year", 46)],
         "const r=($('income')+$('expenses'))/Math.max(1,$('hours')*$('weeks'));document.getElementById('out').textContent='Minimum hourly rate: $'+r.toFixed(2);", "Before taxes. Adjust for your own situation.")
    calc("project-quote.html", "Project quote with buffer", [("hours", "Estimated hours", 40), ("rate", "Hourly rate ($)", 75), ("buffer", "Risk buffer (%)", 20), ("costs", "Fixed costs ($)", 0)],
         "const q=$('hours')*$('rate')*(1+$('buffer')/100)+$('costs');document.getElementById('out').textContent='Quote: $'+q.toFixed(2);", "Quote = hours x rate x (1 + buffer) + costs.")
    calc("margin-markup.html", "Margin and markup", [("cost", "Cost ($)", 60), ("price", "Price ($)", 100)],
         "const m=$('price')?($('price')-$('cost'))/$('price')*100:0;const k=$('cost')?($('price')-$('cost'))/$('cost')*100:0;document.getElementById('out').textContent='Margin: '+m.toFixed(1)+'%   Markup: '+k.toFixed(1)+'%';", "Margin is profit as a share of price; markup is profit as a share of cost.")
    calc("late-fee.html", "Late fee calculator", [("amount", "Invoice amount ($)", 1000), ("rate", "Monthly late fee (%)", 1.5), ("months", "Months late", 2)],
         "const f=$('amount')*($('rate')/100)*$('months');document.getElementById('out').textContent='Late fee: $'+f.toFixed(2)+'   Total due: $'+($('amount')+f).toFixed(2);", "Simple (non-compounding) fee. Check your contract and local rules before charging fees.")
    w(b, "README.txt", "Four single-file calculators. Open any .html in a browser; nothing is uploaded, no internet needed. Edit the defaults in the HTML.\nNot financial, legal or tax advice.\n\n" + LIC)
    print("64", zip_pack("freelancer-calculators"))

    # ---------- 108: Google Business Profile checklist ----------
    b = OUT / "google-business-profile-checklist"
    items = {
        "Basics": ["Claim and verify the profile", "Exact business name (no keyword stuffing)", "Primary category plus 2-3 secondary categories", "Phone number and website link", "Service area or address set correctly"],
        "Details": ["Opening hours, including holiday hours", "Business description (750 characters, plain and specific)", "Attributes (wheelchair access, outdoor seating, etc.)", "Products or services list with prices"],
        "Photos": ["Logo and cover photo", "10+ real photos: storefront, inside, team, work", "Replace outdated photos each season"],
        "Reviews": ["Link to ask for reviews", "Reply to every review, good and bad", "Never buy or fake reviews"],
        "Ongoing": ["Post an update or offer monthly", "Check questions and answers", "Review insights quarterly"],
    }
    body = "".join(f"<h2>{sec}</h2><ul>" + "".join(f"<li><label><input type='checkbox' data-k='{sec}-{j}'> {t}</label></li>" for j, t in enumerate(ts)) + "</ul>" for sec, ts in items.items())
    w(b, "checklist.html", f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Google Business Profile checklist</title><style>body{{font:18px/1.6 system-ui,sans-serif;max-width:40rem;margin:2rem auto;padding:0 1rem;color:#111;background:#fff}}ul{{list-style:none;padding:0}}li{{margin:.4rem 0}}</style></head><body><main><h1>Google Business Profile checklist</h1><p>Ticks are saved in this browser.</p>{body}</main><script>document.querySelectorAll('input[type=checkbox]').forEach(function(c){{try{{c.checked=localStorage.getItem(c.dataset.k)==='1'}}catch(e){{}}c.addEventListener('change',function(){{try{{localStorage.setItem(c.dataset.k,c.checked?'1':'0')}}catch(e){{}}}})}})</script></body></html>")
    w(b, "README.txt", "Open checklist.html in a browser; ticks are saved locally. Platform features change; confirm in your own profile.\n\n" + LIC)
    print("108", zip_pack("google-business-profile-checklist"))

    # ---------- 109: bookkeeping CSV templates ----------
    b = OUT / "bookkeeping-csv-templates"
    w(b, "income-log.csv", "date,client,invoice_number,description,amount,payment_method,notes\n2026-01-15,Example Client,1001,Website work,1200.00,bank transfer,\n")
    w(b, "expense-log.csv", "date,vendor,category,description,amount,payment_method,receipt_saved\n2026-01-03,GitHub,Software,Team plan,4.00,card,yes\n")
    w(b, "mileage-log.csv", "date,from,to,purpose,miles\n2026-01-10,Home,Client site,Kickoff meeting,18.4\n")
    w(b, "invoice-tracker.csv", "invoice_number,client,issued,due,amount,status,paid_on\n1001,Example Client,2026-01-15,2026-02-14,1200.00,sent,\n")
    w(b, "README.md", f"""
    # Bookkeeping CSV Templates
    Four CSVs (income, expenses, mileage, invoices) with clear columns. Open in Excel, Google Sheets or LibreOffice.
    The column names are plain so they are easy to map when importing into tools like Wave or QuickBooks (map columns in the importer; formats differ).
    Keep receipts. This is a recordkeeping template, not tax or accounting advice; ask an accountant what you must track.

    {LIC}""")
    print("109", zip_pack("bookkeeping-csv-templates"))

    # ---------- 113: uptime webhook monitor ----------
    b = OUT / "uptime-webhook-monitor"
    w(b, "targets.json", json.dumps({"webhook": "https://discord.com/api/webhooks/REPLACE/ME", "timeout_ms": 8000, "urls": ["https://example.com", "https://example.org"]}, indent=2))
    (b / "monitor.mjs").write_text('''// Zero-dependency uptime check with Discord/Slack-compatible webhook alerts. Node 18+.
    // node monitor.mjs [--dry]   (run from cron or a scheduled task; --dry prints instead of posting)
    import { readFileSync } from "node:fs";
    const cfg = JSON.parse(readFileSync(new URL("./targets.json", import.meta.url), "utf8"));
    const dry = process.argv.includes("--dry");
    const bad = [];
    for (const url of cfg.urls) {
      const t0 = Date.now();
      try {
        const r = await fetch(url, { method: "GET", redirect: "follow", signal: AbortSignal.timeout(cfg.timeout_ms ?? 8000) });
        console.log(url, r.status, Date.now() - t0 + "ms");
        if (r.status >= 400) bad.push(`${url} returned ${r.status}`);
      } catch (e) {
        console.log(url, "ERROR", e.name);
        bad.push(`${url} unreachable (${e.name})`);
      }
    }
    if (bad.length) {
      const text = "Uptime alert:\\n" + bad.join("\\n");
      if (dry) console.log("[dry] would post:", text);
      else {\n    const response = await fetch(cfg.webhook, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ content: text, text }) });\n    if (!response.ok) throw new Error(`Webhook delivery failed: HTTP ${response.status}`);\n  }
    }
    process.exit(bad.length ? 1 : 0);
    ''', encoding="utf-8")
    w(b, "README.md", f"""
    # Uptime Webhook Monitor
    Checks your URLs and posts to a Discord or Slack webhook when one is down or returns an error.
    1. Edit `targets.json`: your URLs and webhook URL.
    2. Test: `node monitor.mjs --dry`
    3. Schedule it (cron, Task Scheduler, or a CI schedule) every 5 to 15 minutes.
    No dependencies; Node 18 or newer. It alerts on every run while a site is down, so pick a sensible schedule.

    {LIC}""")
    print("113", zip_pack("uptime-webhook-monitor"))

    # ---------- 115: link-in-bio ----------
    b = OUT / "link-in-bio-template"
    w(b, "links.json", json.dumps({"name": "Your Name", "bio": "What you do, in one line.", "links": [{"label": "My website", "url": "https://example.com"}, {"label": "Latest video", "url": "https://example.com/video"}, {"label": "Email me", "url": "mailto:you@example.com"}], "bg": "#0f1720", "fg": "#f5f7fa", "accent": "#34d399"}, indent=2))
    (b / "build.py").write_text('''"""python build.py -> index.html (reads links.json). Upload anywhere."""
    import json, html
    d = json.load(open("links.json", encoding="utf-8"))
    e = html.escape
    links = "".join(f"<li><a href='{e(l['url'])}'>{e(l['label'])}</a></li>" for l in d["links"])
    css = f"body{{margin:0;background:{d['bg']};color:{d['fg']};font:20px/1.5 system-ui,sans-serif;text-align:center}}main{{max-width:30rem;margin:auto;padding:2rem 1rem}}ul{{list-style:none;padding:0}}li{{margin:1rem 0}}a{{display:block;padding:1rem;border:2px solid {d['accent']};border-radius:10px;color:{d['fg']};text-decoration:none;font-weight:600}}a:hover,a:focus{{background:{d['accent']};color:{d['bg']}}}"
    page = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{e(d['name'])}</title><meta name='description' content='{e(d['bio'])}'><style>{css}</style></head><body><main><h1>{e(d['name'])}</h1><p>{e(d['bio'])}</p><nav aria-label='Links'><ul>{links}</ul></nav></main></body></html>"
    open("index.html", "w", encoding="utf-8").write(page)
    print("wrote index.html")
    ''', encoding="utf-8")
    w(b, "README.md", f"""
    # Link-in-Bio Template
    Edit `links.json`, run `python build.py`, upload `index.html` (Netlify drag-and-drop, GitHub Pages, any host). Accessible by default:
    real links, visible focus states, high-contrast colors. Check contrast if you change the colors.

    {LIC}""")
    subprocess.run([sys.executable, "build.py"], cwd=b, check=True)
    print("115", zip_pack("link-in-bio-template"))

    # ---------- 33: branded video reformat kit ----------
    b = OUT / "branded-video-reformat-kit"
    src = ROOT.parent / "content-pipeline"
    for f in ("render.py", "run.sh", "brand.json"):
        shutil.copy(src / f, b / f) if b.exists() else (b.mkdir(parents=True), shutil.copy(src / f, b / f))
    w(b, "README.md", f"""
    # Branded Video Reformat Kit
    Turn one finished video into vertical (1080x1920), square (1080x1080) and landscape (1920x1080) versions with a title bar and a brand footer.
    Needs Docker only (ffmpeg runs in a container). Edit `brand.json` for colors and names; add variants to A/B test.

        sh run.sh my-video.mp4 my-brand A "Short title"

    Outputs land in `out/`. The default footer shows your brand name and URL. Change the fonts or layout in `render.py`.

    {LIC}""")
    print("33", zip_pack("branded-video-reformat-kit"))


if __name__ == "__main__":
    main()
