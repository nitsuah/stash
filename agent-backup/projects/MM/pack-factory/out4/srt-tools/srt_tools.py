"""python srt_tools.py shift in.srt out.srt 2.5      (seconds, negative allowed)
python srt_tools.py vtt in.srt out.vtt
python srt_tools.py clean in.srt out.srt            (strip HTML tags, drop empty cues, renumber)
python srt_tools.py merge a.srt b.srt out.srt        (append b after a, renumber)
Stdlib only."""
import re, sys

TS = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")


def parse(text):
    cues = []
    for block in re.split(r"\n\s*\n", text.strip().replace("\r\n", "\n")):
        lines = block.split("\n")
        if len(lines) >= 2 and "-->" in lines[1]:
            a, b = (x.strip() for x in lines[1].split("-->"))
            cues.append([ms(a), ms(b), "\n".join(lines[2:])])
    return cues


def ms(t):
    h, m, s, f = map(int, TS.match(t).groups())
    return ((h * 60 + m) * 60 + s) * 1000 + f


def fmt(v, sep=","):
    v = max(0, int(round(v)))
    return f"{v // 3600000:02d}:{v // 60000 % 60:02d}:{v // 1000 % 60:02d}{sep}{v % 1000:03d}"


def dump(cues, sep=","):
    return "\n\n".join(f"{i}\n{fmt(a, sep)} --> {fmt(b, sep)}\n{t}" for i, (a, b, t) in enumerate(cues, 1)) + "\n"


cmd = sys.argv[1]
if cmd == "shift":
    cues = [[a + float(sys.argv[4]) * 1000, b + float(sys.argv[4]) * 1000, t] for a, b, t in parse(open(sys.argv[2], encoding="utf-8").read())]
    open(sys.argv[3], "w", encoding="utf-8").write(dump(cues))
elif cmd == "vtt":
    cues = parse(open(sys.argv[2], encoding="utf-8").read())
    open(sys.argv[3], "w", encoding="utf-8").write("WEBVTT\n\n" + dump(cues, ".").replace("\n\n", "\n\n", 1))
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
