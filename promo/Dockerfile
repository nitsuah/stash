# Render image for stash promo spots: Chromium (Playwright) draws each frame of
# a spot's compose.html, numpy/scipy synthesize the music, ffmpeg encodes.
# stash has no app to capture, so there is no capture step: spots compose
# real artifacts (screenshots, issues, terminal output) checked into the repo.
# Build from the repo root: docker build -f promo/Dockerfile -t stash-promo .
ARG PLAYWRIGHT_VERSION=1.63.0
FROM mcr.microsoft.com/playwright:v${PLAYWRIGHT_VERSION}-noble
ARG PLAYWRIGHT_VERSION
RUN apt-get update \
 && apt-get install -y --no-install-recommends ffmpeg python3-numpy python3-scipy fonts-noto-color-emoji \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /deps
RUN npm init -y >/dev/null \
 && npm install --no-save --ignore-scripts --no-audit --no-fund playwright@${PLAYWRIGHT_VERSION}
WORKDIR /repo
