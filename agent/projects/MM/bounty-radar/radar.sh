#!/usr/bin/env bash
# Zero-LLM bounty radar: finds open paid GitHub issues, ranks by payout vs. competition (comment count).
# Needs an authenticated gh CLI (host) and Docker (ranking runs in python:3-slim). Usage: ./radar.sh  -> report.tsv
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p raw
F='--state open --limit 100 --json repository,title,url,commentsCount,createdAt'
gh search issues --label "💎 Bounty" $F > raw/a.json 2>/dev/null || echo '[]' > raw/a.json
gh search issues --label "bounty" $F > raw/b.json 2>/dev/null || echo '[]' > raw/b.json
gh search issues '"bounty" in:title' $F > raw/c.json 2>/dev/null || echo '[]' > raw/c.json
MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W 2>/dev/null || pwd)":/w -w /w python:3-slim python rank.py > report.tsv
head -30 report.tsv
