---
up: "[[repos/fire]]"
title: "fire · README"
source: https://github.com/nitsuah/fire/blob/main/promo/README.md
kind: repo-doc
repo: fire
---

# Promo spots

This folder holds reproducible, **narrated** launch videos for fire. Each spot is rendered from the **real app**: `capture.js` boots `app/server.js` against a fictional demo portfolio (`demo-seed.js`) in a throwaway DB, screenshots the real UI, and calls the real MCP server. Those pieces are then animated frame by frame in a browser, voiced with an offline text-to-speech model, scored with synthesized music, and encoded with ffmpeg.

Everything runs in Docker. It never reads `data/db.json`.

## Re-run

```bash
promo/build.sh                                  # full render of brag-22s (~3 min)
promo/build.sh tour-85s                         # full render of the narrated product tour (~10 min)
promo/build.sh brag-22s --stills 1.8,2.6,6.2    # render just a few frames to check a change
promo/build.sh brag-22s --audio                 # re-voice, re-synth music/SFX and remux only
promo/build.sh brag-22s --recapture             # re-shoot the app (after UI or seed changes)
promo/build.sh brag-22s --publish               # also update site/assets/ (landing page hero)
```

Output goes to `promo/out/<spot>/` (gitignored):
- `<spot>.mp4` is the full-quality video. Frame 0 is the poster.
- `<spot>.jpg` is the poster.
- `<spot>-web.mp4` is the smaller cut used by the landing page.
- `captions.srt` holds the narration as subtitles (upload it next to the video).
- `share-copy.txt` is the post text.
- `stills/` and `frames/` are the rendered frames.

Requirements: Docker Desktop running, plus network access for Google Fonts and the first image build (which downloads the ~350 MB voice model once).

## Narration

`narrate.py` voices each line with [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache-2.0) through `kokoro-onnx`. It runs fully offline inside the image. It writes `vo.wav`, `captions.srt` and `timeline.json`. `pipeline.sh` mixes the voice over the music and ducks the music under it with a sidechain compressor. Lines are cached in `promo/out/tts-cache/`, so re-runs only synthesize what changed.

| `spot.json` key | Meaning |
|---|---|
| `voice` / `speed` | Kokoro voice (default `af_heart`) and rate (default 1.05). Run `/opt/tts/bin/python -c "from kokoro_onnx import Kokoro; print(Kokoro('/models/kokoro-v1.0.onnx','/models/voices-v1.0.bin').get_voices())"` in the image to list voices. |
| `narration` (fixed-timeline spots) | `[{ "t": 3.2, "say": "…" }]`. The build fails if a line runs into the next one or past the end. |
| `say` on each scene (tour spots) | The scene lasts as long as its line: `max(min, lead + speech + tail)`. |
| `caption` | On-screen text when it should differ from what's spoken (for example, the URL is spoken as "lifefire dot netlify dot app" but captioned `lifefire.netlify.app`). |

## Tweak

| To change… | Edit |
|---|---|
| Scene timing, poster frame, hook numbers | `<spot>/spot.json`. The visuals and audio both read it. |
| What's on screen, motion, copy | `<spot>/compose.html` (custom spots) or the scene list in `spot.json` (tour spots). `window.render(t)` is a pure function of time. |
| Music and sound effects | `<spot>/synth.py` (custom spots) or `tour/bed.py` (all tour spots). 120 BPM, A minor. |
| Numbers in the dashboard, tables, charts and MCP output | `demo-seed.js`, then `--recapture` |
| Which UI pieces get captured | `capture.js` / `capture-tour.js`, then `--recapture` |
| Post text | `<spot>/share-copy.txt` |

Workflow: change something, then check it with `--stills` at the times that matter. When it looks right, do a full render.

## Spots

Short custom cuts (social, landing page):

- **`brag-22s`**: the launch spot (landing-page hero, `site/assets/fire-tracker.mp4`), now narrated.
- **`chaos-24s`**: 🌪️ Chaos mode and the customizable layout (`site/assets/chaos.mp4`), now narrated. Callout positions come from the real chart (`chaos.json`, written by `capture.js` with `CHAOS_SEED`), and slots are set in `spot.json` → `chaos.pops`.

Narrated tours (full product descriptions, built from `tour/compose.html`):

| Spot | Length | Covers |
|---|---|---|
| **`tour-85s`** | ~83s | The whole product: dashboard, every asset type, stress tests, Chaos, Insights, Side Hustle Hub, Claude/MCP, privacy |
| **`plan-65s`** | ~65s | Projections: growth presets, Lean/Fat/Coast lines, milestones, bear/base/bull, scenarios, CD maturities |
| **`chaos-60s`** | ~62s | Chaos mode: life events, hover details and sequences, event timeline, mitigations, phone |
| **`insights-60s`** | ~60s | Insight tiles, allocation drill-down, rebalancing, tax-loss harvesting, cash flow, budget/tax, asking Claude |
| **`hustle-60s`** | ~60s | Side Hustle Hub: eBay/Etsy/FB fee calculators, eBay sync, tax-tagged ledger, side-gig taxes via MCP, accelerators |
| **`connect-55s`** | ~57s | Getting data in: CSV imports, Plaid, ENS/multichain crypto, metals, vehicles, cash/CDs/property, live prices |
| **`yours-60s`** | ~61s | Privacy and control: one file, encryption, read-only, security defaults, layout, MCP, export, mobile |

`tour-85s` also publishes to the landing page (`--audio --publish` → `site/assets/tour.mp4`, re-encoded at 720p).

## Tour spots

A tour spot's `spot.json` has `"type": "tour"` and a list of scenes. Each scene has a `kind`, its content, and a `say` line. `tour/compose.html` renders them, burns in captions, and adds the brand mark, chapter label and a progress bar.

| `kind` | Content |
|---|---|
| `title` | `emoji`, `kicker`, `title`, `sub`, `size` |
| `shot` | A real capture `img` with a camera (`cam`: `[at, fx, fy, zoom]` keyframes, or a named point instead of `fx, fy`), `swap` images at a time, `click`/`clicks` (`{ "box": "preset-2", "at": 0.5 }`), highlight boxes (`hl`), and `layout` `full`/`right`/`left` (with `bullets`) |
| `stack` | Rows stacking in (`imgs`, `crop`, `note`) |
| `grid` | Cards popping in (`imgs`, `cols`) |
| `terminal` | A Claude Code-style MCP call: `prompt`, `tool`, `keys` (dotted paths into the real output), `after` (reply with `{path}` values) |
| `stats` | Stat tiles: `items: [{ big, label, color }]` |
| `phone` | A capture in a phone frame, with `bullets` |
| `outro` | Logo, tagline, repo/compose chips and the live URL |

Named click and camera points come from real capture geometry: `tour-boxes.json` (growth presets, chart line toggles), `proj-boxes.json` (`proj:bear`, `proj:bull`) and `chaos.json` (`chaos`, `chaos:hover`).

## New spots

For a narrated tour, copy one of the tour folders, edit the scenes and `share-copy.txt`, and pick features from **[features.md](features.md)**. For a custom-animated cut, copy `brag-22s/` and adjust `spot.json` and `compose.html`. The ledger lists every claim we can make, the line we use for it, how to show it, and which spots already use it. Add the new spot to its "Used in" column.

## Files

- `build.sh` runs on the host. It builds the `fire-promo` image and runs `pipeline.sh` inside it.
- `pipeline.sh` runs the steps: capture → narration → frames → music + voice mix → encode.
- `Dockerfile` bundles Playwright/Chromium, ffmpeg, numpy/scipy, Kokoro TTS and the app's production deps.
- `capture.js` / `capture-tour.js` / `demo-seed.js` / `mcp.mjs` handle the real-app capture.
- `narrate.py` is the voice-over step, and `render.js` is the frame renderer.
- `tour/compose.html` and `tour/bed.py` are the shared tour composer and music bed.
