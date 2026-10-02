---
up: "[[repos/fire]]"
title: "fire · README"
source: https://github.com/nitsuah/fire/blob/main/promo/README.md
kind: repo-doc
repo: fire
---

# Promo spots

This folder holds reproducible launch videos for fire. Each spot is rendered from the **real app**: `capture.js` boots `app/server.js` against a fictional demo portfolio (`demo-seed.js`) in a throwaway DB, screenshots the real UI, and calls the real MCP server. Those pieces are then animated frame by frame in a browser, scored with synthesized music, and encoded with ffmpeg.

Everything runs in Docker. It never reads `data/db.json`.

## Re-run

```bash
promo/build.sh                                  # full render of brag-22s (~3 min)
promo/build.sh brag-22s --stills 1.8,2.6,6.2    # render just a few frames to check a change
promo/build.sh brag-22s --audio                 # re-synth music/SFX and remux only
promo/build.sh brag-22s --recapture             # re-shoot the app (after UI or seed changes)
promo/build.sh brag-22s --publish               # also update site/assets/ (landing page hero)
```

Output goes to `promo/out/<spot>/` (gitignored):
- `<spot>.mp4` is the full-quality video. Frame 0 is the poster.
- `<spot>.jpg` is the poster.
- `<spot>-web.mp4` is the smaller cut used by the landing page.
- `share-copy.txt` is the post text.
- `stills/` and `frames/` are the rendered frames.

Requirements: Docker Desktop running, plus network access for Google Fonts and the first image build.

## Tweak

| To change… | Edit |
|---|---|
| Scene timing, poster frame, hook numbers | `<spot>/spot.json`. The visuals and audio both read it. |
| What's on screen, motion, copy | `<spot>/compose.html`. `window.render(t)` is a pure function of time. |
| Music and sound effects | `<spot>/synth.py` (120 BPM, A minor, cuts on the bar) |
| Numbers in the dashboard, tables, charts and MCP output | `demo-seed.js`, then `--recapture` |
| Which UI pieces get captured | `capture.js`, then `--recapture` |
| Post text | `<spot>/share-copy.txt` |

Workflow: change something, then check it with `--stills` at the times that matter. When it looks right, do a full render.

## Spots

- **`brag-22s`**: the launch spot (landing-page hero, `site/assets/fire-tracker.mp4`).
- **`chaos-24s`**: 🌪️ Chaos mode and the customizable layout (`site/assets/chaos.mp4`). Callout positions come from the real chart (`chaos.json`, written by `capture.js` with `CHAOS_SEED`), and slots are set in `spot.json` → `chaos.pops`.

## New spots

Copy `brag-22s/` to a new folder, such as `promo/tour-45s/`. Adjust `spot.json` and `compose.html`, and pick features from **[features.md](features.md)**. That ledger lists every claim we can make, the line we use for it, how to show it, and which spots already use it. Add the new spot to its "Used in" column.

## Files

- `build.sh` runs on the host. It builds the `fire-promo` image and runs `pipeline.sh` inside it.
- `pipeline.sh` runs the steps: capture → frames → audio → encode.
- `Dockerfile` bundles Playwright/Chromium, ffmpeg, numpy/scipy and the app's production deps.
- `capture.js` / `demo-seed.js` / `mcp.mjs` handle the real-app capture.
- `render.js` is the frame renderer.
