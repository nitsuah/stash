#!/usr/bin/env bash
set -euo pipefail

MM="$(cd "$(dirname "$0")/.." && pwd)"
PLAYWRIGHT_IMAGE="mcr.microsoft.com/playwright:v1.64.0-noble"

# Build every local asset before covers.mjs attempts to render product visuals.
docker run --rm -v "$MM:/w" -w /w/pack-factory python:3-slim python build_batch1.py
docker run --rm -v "$MM:/w" -w /w/icon-pack python:3-slim python build_icons.py

# covers.mjs resolves Playwright relative to audit-scanner/package.json.
docker run --rm -v "$MM:/w" -w /w/audit-scanner "$PLAYWRIGHT_IMAGE" npm install --no-audit --no-fund --silent
docker run --rm -v "$MM:/w" -w /w/cover-factory "$PLAYWRIGHT_IMAGE" node covers.mjs
