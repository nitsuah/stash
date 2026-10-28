"""python make_chart.py data.csv "Chart title" > chart.svg   (bar chart; pass --horizontal for horizontal bars)"""
import csv, html, sys
args = [a for a in sys.argv[1:] if not a.startswith("--")]
horiz = "--horizontal" in sys.argv
rows = [(r["label"], float(r["value"])) for r in csv.DictReader(open(args[0], encoding="utf-8-sig"))]
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
