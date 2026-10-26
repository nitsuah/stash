"""Zero-LLM asset factory: seeded mazes, wall art and math worksheets -> HTML/SVG sources + listings.csv.
Stdlib only. Same seed always gives the same output. Run in python:3-slim, then render.mjs makes PDFs and PNG previews.
Usage: python build_assets.py [seed]   (default seed 2027)"""
import calendar
import csv
import datetime
import html
import math
import pathlib
import random
import shutil
import sys

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"
SEED = 2027
LIC = "Personal and commercial use. Do not resell or redistribute the files themselves.\n"
PAGE_CSS = ("@page{size:Letter;margin:0.5in}body{font-family:system-ui,Arial,sans-serif;color:#111;margin:0}"
            ".pg{page-break-after:always;text-align:center;padding:0.2in}.pg>svg{display:block;margin:0 auto;width:auto;max-width:100%;max-height:8.2in}h1{font-size:26pt;margin:0 0 4pt}"
            "h2{font-size:16pt;margin:0 0 8pt}.sub{font-size:11pt;color:#333;margin-bottom:10pt}"
            ".grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10pt}.mz{border:1px solid #bbb}.mz svg{display:block;width:100%;max-height:1.8in}"
            ".wk{display:grid;grid-template-columns:repeat(4,1fr);gap:16pt 12pt;text-align:left;font-size:16pt;"
            "font-variant-numeric:tabular-nums}.wk div{padding:6pt 2pt;border-bottom:1px solid #999}.key .wk{font-size:11pt}")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def doc(title, body):
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{html.escape(title)}</title><style>{PAGE_CSS}</style></head><body>{body}</body></html>"


# ---------- mazes ----------
D = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
OPP = {"N": "S", "S": "N", "E": "W", "W": "E"}


def make_maze(rng, w, h):
    cells = {(x, y): set("NSEW") for x in range(w) for y in range(h)}
    seen, stack = {(0, 0)}, [(0, 0)]
    while stack:
        x, y = stack[-1]
        nb = [(d, (x + dx, y + dy)) for d, (dx, dy) in D.items() if (x + dx, y + dy) in cells and (x + dx, y + dy) not in seen]
        if not nb:
            stack.pop()
            continue
        d, n = rng.choice(nb)
        cells[(x, y)].discard(d)
        cells[n].discard(OPP[d])
        seen.add(n)
        stack.append(n)
    cells[(0, 0)].discard("N")
    cells[(w - 1, h - 1)].discard("S")
    return cells


def solve(cells, w, h):
    prev, queue, goal = {(0, 0): None}, [(0, 0)], (w - 1, h - 1)
    while queue:
        cur = queue.pop(0)
        if cur == goal:
            break
        for d, (dx, dy) in D.items():
            n = (cur[0] + dx, cur[1] + dy)
            if d not in cells[cur] and n in cells and n not in prev:
                prev[n] = cur
                queue.append(n)
    path, cur = [], goal
    while cur:
        path.append(cur)
        cur = prev[cur]
    return path[::-1]


def maze_svg(cells, w, h, c, path=None):
    lines = []
    for (x, y), walls in cells.items():
        x0, y0 = x * c + 10, y * c + 10
        if "N" in walls:
            lines.append(f"M{x0} {y0}h{c}")
        if "W" in walls:
            lines.append(f"M{x0} {y0}v{c}")
        if y == h - 1 and "S" in walls:
            lines.append(f"M{x0} {y0 + c}h{c}")
        if x == w - 1 and "E" in walls:
            lines.append(f"M{x0 + c} {y0}v{c}")
    sol = ""
    if path:
        pts = " ".join(f"{x * c + 10 + c / 2},{y * c + 10 + c / 2}" for x, y in path)
        sol = f"<polyline points='{pts}' fill='none' stroke='#d6336c' stroke-width='{max(2, c // 4)}' stroke-linejoin='round'/>"
    W, H = w * c + 20, h * c + 20
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='100%' role='img' aria-label='Maze'>"
            f"<path d='{''.join(lines)}' stroke='#111' stroke-width='2' fill='none' stroke-linecap='square'/>{sol}</svg>")


def maze_book(slug, title, tiers, per_tier):
    rng = random.Random(f"{SEED}-{slug}")
    pages, keys, n = [], [], 0
    for label, w, h, c in tiers:
        for _ in range(per_tier):
            n += 1
            cells = make_maze(rng, w, h)
            pages.append(f"<div class='pg'><h1>Maze {n}</h1><div class='sub'>{label}. Start at the top-left gap, finish at the bottom-right gap.</div>{maze_svg(cells, w, h, c)}</div>")
            keys.append(f"<div class='mz'><b>Maze {n}</b>{maze_svg(cells, w, h, max(4, c // 3), solve(cells, w, h))}</div>")
    cover = f"<div class='pg'><h1 style='margin-top:3in;font-size:40pt'>{html.escape(title)}</h1><div class='sub'>{n} mazes, easy to hard, with solutions. Nitsuah Labs.</div></div>"
    key_pages = "".join(f"<div class='pg'><h2>Solutions</h2><div class='grid'>{''.join(keys[i:i + 4])}</div></div>" for i in range(0, len(keys), 4))
    return doc(title, cover + "".join(pages) + key_pages), n


# ---------- worksheets ----------
def problems(rng, op, n, lo, hi):
    out = []
    for _ in range(n):
        a, b = rng.randint(lo, hi), rng.randint(lo, hi)
        if op == "-" and b > a:
            a, b = b, a
        if op == "/":
            b = max(b, 2)
            a = b * rng.randint(lo, hi)
        ans = {"+": a + b, "-": a - b, "x": a * b, "/": a // b}[op]
        out.append((f"{a} {op if op != '/' else chr(247)} {b} =", ans))
    return out


def worksheet_pack(slug, title, ops, lo, hi, sheets):
    rng = random.Random(f"{SEED}-{slug}")
    pages, keys = [], []
    for i in range(sheets):
        op = ops[i % len(ops)]
        ps = problems(rng, op, 24, lo, hi)
        pages.append(f"<div class='pg'><h1>Worksheet {i + 1}</h1><div class='sub'>Name: ______________ &nbsp; Date: __________</div><div class='wk'>{''.join(f'<div>{html.escape(q)}</div>' for q, _ in ps)}</div></div>")
        keys.append(f"<div><b>Worksheet {i + 1}</b><div class='wk'>{''.join(f'<div>{a}</div>' for _, a in ps)}</div></div>")
    key_pages = "".join(f"<div class='pg key'><h2>Answer key</h2>{''.join(keys[j:j + 2])}</div>" for j in range(0, len(keys), 2))
    return doc(title, "".join(pages) + key_pages)


# ---------- wall art ----------
PALETTES = [("#1d3557", "#457b9d", "#a8dadc", "#f1faee", "#e63946"), ("#264653", "#2a9d8f", "#e9c46a", "#f4a261", "#e76f51"),
            ("#2b2d42", "#8d99ae", "#edf2f4", "#ef233c", "#d90429"), ("#3d405b", "#81b29a", "#f2cc8f", "#e07a5f", "#f4f1de"),
            ("#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#6fffe9"), ("#5f0f40", "#9a031e", "#fb8b24", "#e36414", "#0f4c5c")]


def art_svg(rng, pal, kind):
    W, H = 2400, 3000
    bg = pal[3] if kind != "rings" else pal[0]
    parts = [f"<rect width='{W}' height='{H}' fill='{bg}'/>"]
    if kind == "rings":
        cx, cy = rng.randint(900, 1500), rng.randint(1100, 1900)
        for i in range(12, 0, -1):
            parts.append(f"<circle cx='{cx}' cy='{cy}' r='{i * 110}' fill='{pal[i % 5]}' opacity='0.9'/>")
    elif kind == "blocks":
        for _ in range(26):
            w, h = rng.randint(200, 900), rng.randint(200, 1100)
            parts.append(f"<rect x='{rng.randint(0, W - w)}' y='{rng.randint(0, H - h)}' width='{w}' height='{h}' fill='{rng.choice(pal)}' opacity='0.82'/>")
    else:
        step = 300
        for gx in range(0, W, step):
            for gy in range(0, H, step):
                r = rng.choice([step // 2, step // 3, step // 4])
                base = rng.choice(pal)
                shape = rng.choice([c for c in pal if c != base])
                parts.append(f"<rect x='{gx}' y='{gy}' width='{step}' height='{step}' fill='{base}'/>"
                             f"<path d='M{gx} {gy + step}A{r} {r} 0 0 1 {gx + step} {gy + step}V{gy}H{gx}Z' fill='{shape}' transform='rotate({rng.choice([0, 90, 180, 270])} {gx + step // 2} {gy + step // 2})'/>")
    return f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {W} {H}' width='{W}' height='{H}'>{''.join(parts)}</svg>"


def art_set(slug, count):
    rng = random.Random(f"{SEED}-{slug}")
    return [(f"art-{i + 1:02d}", art_svg(rng, PALETTES[i % len(PALETTES)], ["rings", "blocks", "tiles"][i % 3])) for i in range(count)]


def main():
    global SEED
    SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 2027
    if not 2 <= SEED <= 9998:
        raise SystemExit("seed/year must be between 2 and 9998; existing outputs were not touched")
    # ---------- build ----------
    PACKS = []


    def pack(slug, title, price, tags, blurb, files, readme_extra=""):
        base = OUT / slug
        for rel, text in files.items():
            write(base / rel, text)
        write(base / "README.txt", f"{title}\n\n{blurb}\n{readme_extra}\nFiles are generated from a fixed seed ({SEED}), so each set is unique to this release.\n\n{LIC}")
        PACKS.append({"sku": slug, "title": title, "price": price, "tags": "|".join(tags), "description": blurb})


    shutil.rmtree(OUT, ignore_errors=True)

    b1, n1 = maze_book("maze-book-1", "Maze Puzzle Book Vol. 1", [("Easy", 8, 10, 40), ("Medium", 14, 18, 24), ("Hard", 22, 28, 15)], 10)
    pack("maze-book-vol-1", "Maze Puzzle Book Vol. 1: 30 Printable Mazes with Solutions (PDF)", 6,
         ["maze book", "printable puzzles", "kids activity", "puzzle pdf", "brain games", "mazes", "road trip", "classroom", "party activity", "digital download", "puzzle book", "easy to hard", "letter size"],
         "30 printable mazes in three difficulty levels with a full solution section. US Letter PDF, print as many copies as you like for personal use.", {"book.html": b1})

    for slug, title, ops, lo, hi in [
            ("math-add-sub-grade-2", "Grade 2 Addition and Subtraction Worksheets: 20 Printable Pages with Answer Key (PDF)", ["+", "-"], 2, 40),
            ("math-multiply-grade-3", "Grade 3 Multiplication and Division Worksheets: 20 Printable Pages with Answer Key (PDF)", ["x", "/"], 2, 12),
            ("math-mixed-grade-4", "Grade 4 Mixed Operations Worksheets: 20 Printable Pages with Answer Key (PDF)", ["+", "-", "x", "/"], 5, 60)]:
        pack(slug, title, 4, ["math worksheets", "homeschool", "printable", "grade school", "practice sheets", "answer key", "teacher resource", "classroom", "digital download", "pdf worksheets", "arithmetic", "back to school", "kids math"],
             "20 printable practice sheets, 24 problems each, plus an answer key. US Letter PDF.", {"book.html": worksheet_pack(slug, title, ops, lo, hi, 20)})

    art = art_set("wall-art-1", 12)
    pack("geometric-wall-art-vol-1", "Geometric Wall Art Set Vol. 1: 12 Abstract Printable Posters, 24x30 in (4:5), Instant Download", 8,
         ["wall art", "printable art", "geometric print", "abstract art", "modern decor", "digital download", "poster print", "home decor", "office art", "living room art", "minimalist", "instant download", "4x5 print"],
         "12 abstract geometric posters in 2400x3000 px (4:5), ready to print at 8x10, 16x20 or 24x30 inches. Delivered as SVG plus PNG.", {f"{n}.svg": s for n, s in art})

    # ---------- dated planner (regenerates for any year) ----------

    YEAR = SEED


    def planner_html(year):
        cal = calendar.Calendar(firstweekday=6)
        css = ("<style>table{width:100%;border-collapse:collapse;table-layout:fixed}td,th{border:1px solid #888;height:1.05in;vertical-align:top;"
               "font-size:10pt;text-align:left;padding:2pt}th{height:.3in;background:#eee}.wkr{height:auto}.wkr td{height:.95in}"
               ".hab td{height:.22in;height:.22in;font-size:7pt;text-align:center;padding:0}.hab td.n{text-align:left;width:1.6in}</style>")
        pages = [f"<div class='pg'><h1 style='margin-top:3in;font-size:40pt'>{year} Planner</h1><div class='sub'>Monthly calendar, weekly pages and a habit tracker. Nitsuah Labs.</div></div>"]
        for m in range(1, 13):
            rows = "".join("<tr>" + "".join(f"<td>{d.day if d.month == m else ''}</td>" for d in wk) + "</tr>" for wk in cal.monthdatescalendar(year, m))
            pages.append(f"<div class='pg'><h1>{calendar.month_name[m]} {year}</h1><table><tr>{''.join(f'<th>{n}</th>' for n in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])}</tr>{rows}</table></div>")
        d = datetime.date(year, 1, 1)
        d -= datetime.timedelta(days=(d.weekday() + 1) % 7)
        while d.year <= year and (d <= datetime.date(year, 12, 31)):
            end = d + datetime.timedelta(days=6)
            days = "".join(f"<tr><td style='width:1.3in'><b>{(d + datetime.timedelta(days=i)).strftime('%a %b %d')}</b></td><td></td></tr>" for i in range(7))
            pages.append(f"<div class='pg'><h2>Week of {d.strftime('%b %d')} to {end.strftime('%b %d, %Y')}</h2><table class='wkr'>{days}</table><h2 style='margin-top:12pt'>Notes</h2><table class='wkr'><tr><td style='height:1.6in'></td></tr></table></div>")
            d += datetime.timedelta(days=7)
        for m in range(1, 13):
            nd = calendar.monthrange(year, m)[1]
            head = "<tr><td class='n'><b>Habit</b></td>" + "".join(f"<td>{i}</td>" for i in range(1, nd + 1)) + "</tr>"
            body = "".join("<tr><td class='n'></td>" + "<td></td>" * nd + "</tr>" for _ in range(14))
            pages.append(f"<div class='pg'><h2>Habit tracker: {calendar.month_name[m]} {year}</h2><table class='hab'>{head}{body}</table></div>")
        return doc(f"{year} Planner", css + "".join(pages))


    pack(f"planner-{YEAR}", f"{YEAR} Printable Planner: Monthly Calendar, Weekly Pages and Habit Tracker, PDF Instant Download", 7,
         [f"{YEAR} planner", "printable planner", "weekly planner", "monthly calendar", "habit tracker", "planner pdf", "digital download", "yearly planner", "letter size", "productivity", "instant download", "calendar printable"],
         f"A complete {YEAR} planner: 12 monthly calendars, a page for every week and a monthly habit tracker. US Letter PDF.", {"book.html": planner_html(YEAR)},
         "Re-run the factory with another seed to build the next year (the seed is the year).\n")


    # ---------- coloring pages ----------
    def mandala_svg(rng):
        cx = cy = 500
        parts = []
        for ring in range(rng.randint(4, 6)):
            n = rng.choice([6, 8, 10, 12, 16])
            r = 90 + ring * 65
            pw, ph = rng.randint(14, 34), rng.randint(30, 70)
            kind = rng.choice(["petal", "circle", "diamond"])
            for i in range(n):
                a = 360 / n * i
                x, y = cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))
                if kind == "petal":
                    s = f"<ellipse cx='0' cy='0' rx='{pw}' ry='{ph}' transform='rotate({a + 90})'/>"
                elif kind == "circle":
                    s = f"<circle cx='0' cy='0' r='{pw}'/>"
                else:
                    s = f"<rect x='{-pw}' y='{-pw}' width='{pw * 2}' height='{pw * 2}' transform='rotate({a + 45})'/>"
                parts.append(f"<g transform='translate({x:.1f} {y:.1f})'>{s}</g>")
            parts.append(f"<circle cx='{cx}' cy='{cy}' r='{r - 40}'/>")
        parts.append(f"<circle cx='{cx}' cy='{cy}' r='30'/>")
        return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1000 1000' width='100%' role='img' aria-label='Coloring page'>"
                f"<g fill='none' stroke='#111' stroke-width='4'>{''.join(parts)}</g></svg>")


    def coloring_book():
        rng = random.Random(f"{SEED}-mandala")
        pages = "".join(f"<div class='pg'><h2>Mandala {i + 1}</h2>{mandala_svg(rng)}</div>" for i in range(30))
        return doc("Mandala Coloring Book", f"<div class='pg'><h1 style='margin-top:3in;font-size:40pt'>Mandala Coloring Book</h1><div class='sub'>30 pages to color. Nitsuah Labs.</div></div>{pages}")


    pack("mandala-coloring-book-vol-1", "Mandala Coloring Pages: 30 Printable Designs for Adults and Kids, PDF Instant Download", 5,
         ["coloring pages", "mandala", "adult coloring", "printable coloring", "coloring book", "kids activity", "digital download", "relaxation", "mindfulness", "pdf coloring", "mandala print", "instant download", "letter size"],
         "30 mandala coloring pages with clean outlines. US Letter PDF, print as many copies as you like for personal use.", {"book.html": coloring_book()})


    # ---------- wallpapers ----------
    def wallpaper(rng, pal, w, h):
        a, b = rng.sample(pal, 2)
        shapes = []
        for _ in range(rng.randint(5, 9)):
            r = rng.randint(min(w, h) // 8, min(w, h) // 3)
            shapes.append(f"<circle cx='{rng.randint(0, w)}' cy='{rng.randint(0, h)}' r='{r}' fill='{rng.choice(pal)}' opacity='0.35'/>")
        return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>"
                f"<stop offset='0' stop-color='{a}'/><stop offset='1' stop-color='{b}'/></linearGradient></defs><rect width='{w}' height='{h}' fill='url(#g)'/>{''.join(shapes)}</svg>")


    rng = random.Random(f"{SEED}-wall")
    files = {}
    for i, pal in enumerate(PALETTES):
        for label, w, h in [("phone", 1170, 2532), ("tablet", 2048, 2732), ("desktop", 3840, 2160)]:
            files[f"theme-{i + 1}-{label}.svg"] = wallpaper(rng, pal, w, h)
    pack("gradient-wallpapers-vol-1", "Abstract Gradient Wallpaper Pack: 6 Themes for Phone, Tablet and Desktop, Instant Download", 4,
         ["wallpaper", "phone wallpaper", "iphone wallpaper", "desktop wallpaper", "abstract", "gradient", "tablet wallpaper", "background", "digital download", "aesthetic", "lock screen", "instant download", "wallpaper pack"],
         "6 abstract gradient themes, each in phone (1170x2532), tablet (2048x2732) and desktop (3840x2160) sizes. JPG files.", files)

    with open(OUT / "listings.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["sku", "title", "price", "tags", "description"])
        wr.writeheader()
        wr.writerows(PACKS)
    print(f"seed={SEED} packs={len(PACKS)} mazes={n1}")


if __name__ == "__main__":
    main()
