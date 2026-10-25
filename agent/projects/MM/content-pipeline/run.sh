#!/usr/bin/env bash
# usage: run.sh <master.mp4 inside this folder> <brand> <variant> "<title>"
# Needs Docker only. Outputs land in ./out/ . Example: ./run.sh sample.mp4 nitsuah-labs A "5 invoice mistakes"
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out
W="$(pwd -W 2>/dev/null || pwd)"
export MSYS_NO_PATHCONV=1

# Python writes argument arrays as NUL-delimited files. No generated command is
# evaluated by a shell, so titles and paths cannot trigger shell substitution.
docker run --rm -v "$W:/work" -w /work python:3-slim python render.py "$@"
shopt -s nullglob
args_files=(out/ffmpeg-*.args)
if ((\${#args_files[@]} == 0)); then
  echo "Renderer did not produce any FFmpeg argument files" >&2
  exit 1
fi
for argfile in "\${args_files[@]}"; do
  mapfile -d '' -t args < "$argfile"
  ((\${#args[@]} > 0)) || { echo "Empty FFmpeg argument file: $argfile" >&2; exit 1; }
  docker run --rm -v "$W:/work" -w /work --entrypoint ffmpeg jrottenberg/ffmpeg:7-ubuntu "\${args[@]}"
done
ls -la out
