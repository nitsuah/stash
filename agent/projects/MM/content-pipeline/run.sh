#!/usr/bin/env bash
# usage: run.sh <master.mp4 inside this folder> <brand> <variant> "<title>"
# Needs Docker only. Outputs land in ./out/ . Example: ./run.sh sample.mp4 nitsuah-labs A "5 invoice mistakes"
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out
W="$(pwd -W 2>/dev/null || pwd)"
export MSYS_NO_PATHCONV=1
docker run --rm -v "$W:/work" -w /work python:3-slim python render.py "$@" > out/cmds.txt
while IFS= read -r cmd; do
  [[ -z "$cmd" ]] && continue
  docker run --rm -v "$W:/work" -w /work --entrypoint sh jrottenberg/ffmpeg:7-ubuntu -c "$cmd"
done < out/cmds.txt
ls -la out
