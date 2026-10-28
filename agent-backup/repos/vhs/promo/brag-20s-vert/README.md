---
up: "[[repos/vhs]]"
title: "vhs · README"
source: https://github.com/nitsuah/vhs/blob/main/promo/brag-20s-vert/README.md
kind: repo-doc
repo: vhs
---

# brag-20s-vert — vertical short

A 1080×1920, 20 s narrated cut of the launch video for YouTube Shorts, Reels and TikTok. Published as `site/brag-vert.mp4` (poster `site/brag-vert.jpg`).

`brag-20s` is **locked** (`promo/spots.json`): this spot reads `../brag-20s/composition.html` and `../brag-20s/audio.py` as sources and never edits them, `site/brag.mp4` or `site/brag.jpg`.

| File | What it is |
|---|---|
| `compose.html` | The 1080×1920 shell: VHS Box brand above, the landscape composition full-width in the middle (iframe, `render(t)` driven in lockstep), captions from `spot.json` narration below, URL chip. |
| `spot.json` | Size, fps, poster time, tagline, URL, and the narration lines (`at` start, measured `dur`). |
| `capture.mjs` | Serves `promo/` over http (the iframe must be same-origin) and seeks `render(t)` at 30 fps. |
| `build.sh` | The whole render in Docker: narration, frames, soundtrack, mix, encode. |
| `tts/` | Kokoro TTS + scipy image and `mix.py` (ducks the music ~10 dB under each line), copied from nitsuah/vigil `promo/tts`. |
| `vo/` | Committed narration WAVs, so a rebuild is offline and identical. |
| `share-copy.txt` | Post copy. |

## Storyboard

| Time | Landscape scene (brag-20s) | Narration |
|---|---|---|
| 0.4–2.7 | Spines drop onto the shelf, wordmark | "Got a shelf full of VHS tapes?" |
| 3.9–7.4 | Crop five spines, three snaps | "Point your camera at it. It reads five spines a shot." |
| 8.0–11.8 | Review cards, ✓ All, 15 tapes added | "The AI reads every spine. You just hit confirm all." |
| 12.2–15.7 | Collection table, Export → Sell Drafts | "Every tape gets an ID, a condition and a price." |
| 16.0–19.7 | StacksUp wall, Be Kind, Rewind! | "Self-hosted and open source. Be kind, rewind." |

Frame 0 is the poster (19.6 s, every caption word lit, outro settled), as in brag-20s.

## Rebuild

From the repo root (Git Bash on Windows):

```bash
promo/brag-20s-vert/build.sh stills 1.5 5 9 13 17 19.6   # check frames first
promo/brag-20s-vert/build.sh                              # full render → promo/out/brag-20s-vert/
promo/brag-20s-vert/build.sh tts                          # only after changing narration text; copy the printed durations into spot.json
cp promo/out/brag-20s-vert/brag-20s-vert-web.mp4 site/brag-vert.mp4
cp promo/out/brag-20s-vert/brag-20s-vert.jpg site/brag-vert.jpg
```

Posting to Shorts, Reels or TikTok is a manual step: upload `promo/out/brag-20s-vert/brag-20s-vert.mp4` with `share-copy.txt`.
