"""Write NUL-delimited ffmpeg argument files for run.sh; never emit shell commands.
Usage: render.py <input.mp4> <brand> <variant> "<title>" (paths are relative to /work)."""
import hashlib
import json
import pathlib
import re
import sys


def hexc(color):
    return "0x" + color.lstrip("#")


def main():
    if len(sys.argv) != 5:
        raise SystemExit('usage: render.py <input.mp4> <brand> <variant> "<title>"')
    inp, brand, variant, title = sys.argv[1:5]
    cfg = json.loads(pathlib.Path("/work/brand.json").read_text(encoding="utf-8"))
    brands = cfg.get("brands", {})
    if brand not in brands:
        raise SystemExit(f"unknown brand {brand!r}; choose one of: {', '.join(sorted(brands))}")
    b = brands[brand]
    variants = b.get("variants", {})
    if variant not in variants:
        raise SystemExit(f"unknown variant {variant!r} for brand {brand!r}; choose one of: {', '.join(sorted(variants))}")
    v = variants[variant]
    colors = {**b["colors"], **{k: value for k, value in v.items() if k == "accent"}}
    tagline = v.get("tagline", b["tagline"])
    source = pathlib.Path(inp)
    if not source.is_file():
        raise SystemExit(f"input video not found: {inp}")
    out_dir = pathlib.Path("/work/out")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "title.txt").write_text(title, encoding="utf-8")
    (out_dir / "intro.txt").write_text(b["intro_text"], encoding="utf-8")
    (out_dir / "outro.txt").write_text(b["outro_text"], encoding="utf-8")
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", source.stem).strip("-")[:60] or "video"
    suffix = hashlib.sha256((str(source) + "\0" + title).encode("utf-8")).hexdigest()[:10]
    font = str(b.get("font", "DejaVu Sans")).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    for name, fmt in cfg["formats"].items():
        w, h = int(fmt["w"]), int(fmt["h"])
        title_size = min(h // 24, int(w * 0.85 / (max(len(title), 1) * 0.6)))
        vf = (
            f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color={hexc(colors['bg'])},"
            f"drawtext=font='{font}':textfile=/work/out/title.txt:fontcolor={hexc(colors['fg'])}:fontsize={title_size}:"
            f"x=(w-text_w)/2:y=h*0.06:box=1:boxcolor={hexc(colors['accent'])}@0.85:boxborderw={max(1, h // 90)},"
            f"drawtext=font='{font}':textfile=/work/out/intro.txt:fontcolor={hexc(colors['fg'])}:fontsize={max(1, h // 40)}:"
            f"x=(w-text_w)/2:y=h*0.90,"
            f"drawtext=font='{font}':textfile=/work/out/outro.txt:fontcolor={hexc(colors['fg'])}:fontsize={max(1, h // 40)}:"
            f"x=(w-text_w)/2:y=h*0.95"
        )
        output = f"out/{slug}_{suffix}_{brand}_{variant}_{name}.mp4"
        argv = ["-y", "-i", inp, "-vf", vf, "-c:v", "libx264", "-crf", "23", "-preset", "veryfast", "-c:a", "copy", output]
        (out_dir / f"ffmpeg-{name}.args").write_bytes(b"\0".join(a.encode("utf-8") for a in argv) + b"\0")
    print(f"Prepared {len(cfg['formats'])} ffmpeg argument files; tagline for captions: {tagline}", file=sys.stderr)


if __name__ == "__main__":
    main()
