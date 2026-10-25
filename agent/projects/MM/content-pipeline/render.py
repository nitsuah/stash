"""Emit shell-quoted ffmpeg commands for a master video, using brand.json.
Run inside python:3-slim; run.sh feeds the printed commands to an ffmpeg container.
usage: render.py <input.mp4> <brand> <variant> "<title>"  (paths are relative to /work)"""
import json
import pathlib
import shlex
import sys


def esc(s):  # drawtext escaping; shell quoting is applied separately with shlex.join
    return s.replace("\\", "\\\\").replace("'", "’").replace(":", "\\:").replace("%", "\\%")


def hexc(c):
    return "0x" + c.lstrip("#")


def main():
    if len(sys.argv) != 5:
        raise SystemExit('usage: render.py <input.mp4> <brand> <variant> "<title>"')

    inp, brand, variant, title = sys.argv[1:5]
    cfg = json.loads(pathlib.Path("/work/brand.json").read_text(encoding="utf-8"))
    b = cfg["brands"][brand]
    colors = {**b["colors"], **{k: v for k, v in b.get("variants", {}).get(variant, {}).items() if k == "accent"}}
    tagline = b.get("variants", {}).get(variant, {}).get("tagline", b["tagline"])
    stem = pathlib.Path(inp).stem

    for name, f in cfg["formats"].items():
        w, h = f["w"], f["h"]
        vf = (
            f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color={hexc(colors['bg'])},"
            f"drawtext=text='{esc(title)}':fontcolor={hexc(colors['fg'])}:fontsize={min(h // 24, int(w * 0.85 / (max(len(title), 1) * 0.6)))}:"
            f"x=(w-text_w)/2:y=h*0.06:box=1:boxcolor={hexc(colors['accent'])}@0.85:boxborderw={h // 90},"
            f"drawtext=text='{esc(b['intro_text'])}  {esc(b['outro_text'])}':fontcolor={hexc(colors['fg'])}:"
            f"fontsize={h // 40}:x=(w-text_w)/2:y=h*0.93"
        )
        out = f"out/{stem}_{brand}_{variant}_{name}.mp4"
        argv = ["ffmpeg", "-y", "-i", inp, "-vf", vf, "-c:v", "libx264", "-crf", "23", "-preset", "veryfast", "-c:a", "copy", out]
        print(shlex.join(argv))

    print(f"# tagline for captions: {tagline}", file=sys.stderr)


if __name__ == "__main__":
    main()
