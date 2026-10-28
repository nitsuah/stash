"""python make_cards.py posts.json -> out/<slug>_square|story|wide.svg (1080x1080, 1080x1920, 1200x630)."""
import json, sys, html, pathlib
d = json.load(open(sys.argv[1], encoding="utf-8"))
b = d["brand"]
e = html.escape
pathlib.Path("out").mkdir(exist_ok=True)
SIZES = {"square": (1080, 1080), "story": (1080, 1920), "wide": (1200, 630)}
for p in d["posts"]:
    for name, (W, H) in SIZES.items():
        fs = max(40, min(H // 8, int(W * 0.85 / max(len(p["headline"]), 1) / 0.55)))
        svg = (
            f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}' role='img' aria-label='{e(p['headline'])}'>"
            f"<rect width='{W}' height='{H}' fill='{b['bg']}'/><rect x='0' y='0' width='{W}' height='{H // 60 + 6}' fill='{b['accent']}'/>"
            f"<text x='{W // 2}' y='{H // 2}' text-anchor='middle' font-family='sans-serif' font-weight='700' font-size='{fs}' fill='{b['fg']}'>{e(p['headline'])}</text>"
            f"<text x='{W // 2}' y='{H // 2 + fs}' text-anchor='middle' font-family='sans-serif' font-size='{fs // 2}' fill='{b['accent']}'>{e(p['sub'])}</text>"
            f"<text x='{W // 2}' y='{H - H // 14}' text-anchor='middle' font-family='sans-serif' font-size='{max(24, H // 32)}' fill='{b['fg']}'>{e(b['name'])}</text></svg>"
        )
        pathlib.Path(f"out/{p['slug']}_{name}.svg").write_text(svg, encoding="utf-8")
print("wrote", len(d["posts"]) * 3, "cards")
