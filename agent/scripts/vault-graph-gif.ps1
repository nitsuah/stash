<#
Render the vault's Obsidian graph as an animated GIF + WebP for the GitHub Pages site (runs vault-graph-gif.js in Docker).

Writes pages/assets/vault-graph.{gif,webp,png,json}. Node 22 + ffmpeg run in a throwaway container,
so nothing is installed on the host and the render is the same on every machine. Deterministic:
the same vault gives the same picture, so re-run it only when the graph has visibly grown.

Usage: powershell -File agent/scripts/vault-graph-gif.ps1 [-Preview] [-SnapshotJson <repo-relative path>]
  -Preview        Render only the settled last frame to pages/assets/vault-graph-preview.png (fast tuning).
  -SnapshotJson   Also dump nodes, edges and per-frame positions there, to redraw the animation elsewhere.
#>

param(
    [switch]$Preview,
    [string]$SnapshotJson
)

$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path

docker info *> $null
if ($LASTEXITCODE -ne 0) { throw 'Docker Desktop is not running (try bootstrap-stage0.ps1 -StartIfDown).' }

$previewEnv = if ($Preview) { '-e', 'PREVIEW=1' } else { @() }
$snapEnv = if ($SnapshotJson) { '-e', "SNAPSHOT_JSON=/work/$($SnapshotJson -replace '\\', '/')" } else { @() }
$cmd = 'apt-get update -qq >/dev/null && apt-get install -y -qq --no-install-recommends ffmpeg >/dev/null ' +
       '&& mkdir -p /tmp/g && cd /tmp/g && npm i --silent --no-audit --no-fund d3-force@3 pureimage@0.4 ' +
       '&& cp /work/agent/scripts/vault-graph-gif.js . && node vault-graph-gif.js'

docker run --rm -v "${repo}:/work" -e VAULT=/work/agent -e OUT_DIR=/work/pages/assets @previewEnv @snapEnv `
    node:22-bookworm-slim sh -c $cmd
if ($LASTEXITCODE -ne 0) { throw "render failed (exit $LASTEXITCODE)" }
