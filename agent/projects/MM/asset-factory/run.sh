#!/usr/bin/env bash
# Zero-LLM pipeline: build sources -> render PDFs/PNGs -> zip each pack. Needs Docker. Usage: ./run.sh [seed]
set -euo pipefail
cd "$(dirname "$0")"
MM="$(cd .. && pwd -W 2>/dev/null || pwd)"
export MSYS_NO_PATHCONV=1
docker run --rm -v "$MM":/w -w /w/asset-factory python:3-slim python build_assets.py "${1:-2027}"
docker run --rm -v "$MM":/w -w /w/asset-factory mcr.microsoft.com/playwright:v1.64.0-noble node render.mjs out
docker run --rm -i -v "$MM":/w -w /w/asset-factory python:3-slim python - <<'PY'
import pathlib, zipfile
out = pathlib.Path("out")
for d in sorted(p for p in out.iterdir() if p.is_dir()):
    keep = [p for p in d.rglob("*") if p.is_file() and p.name != "book.html" and not (p.suffix == ".svg" and p.with_suffix(".jpg").exists())]
    with zipfile.ZipFile(out / f"{d.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for p in keep:
            z.write(p, f"{d.name}/{p.relative_to(d).as_posix()}")
    print(d.name, (out / f"{d.name}.zip").stat().st_size)
PY
