"""python make_flyer.py flyer.json  -> flyer.svg (Letter, 816x1056). Open in a browser and print, or import into Inkscape."""
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
