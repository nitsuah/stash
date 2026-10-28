"""python contrast.py "#777777" "#ffffff"      -> ratio and WCAG verdicts
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
