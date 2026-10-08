---
up: "[[repos/vhs]]"
title: "vhs · README"
source: https://github.com/nitsuah/vhs/blob/main/promo/brag-20s/README.md
kind: repo-doc
repo: vhs
---

# Launch video sources

Everything needed to rebuild `site/brag.mp4` and `site/brag.jpg`. Renders and frames go to
`brag-output/` (gitignored); only these sources are tracked.

| File | What it is |
|---|---|
| `composition.html` | The whole video as one page. `render(t)` draws any frame from scratch. Open with `?t=7.5` to inspect a frame, `?play` to preview in real time. |
| `capture.mjs` | Seeks `render(t)` at 30fps in headless Chromium and writes PNGs. |
| `audio.py` | Synthesizes the soundtrack (numpy + scipy). Event times mirror `render(t)`. |
| `share-copy.txt` | Post copy. |

## Storyboard (20s, 1920×1080)

| Time | Scene | Headline |
|---|---|---|
| 0.0–3.2 | Seventeen spines drop onto a shelf; `VHS Box` / *Catalog every tape you own.* | — |
| 3.0–3.8 | The shelf shrinks into the app's camera feed | — |
| 3.8–7.7 | Crop on five spines, `Space` ×3 stages three shots, `Enter` analyzes | Snap the shelf. **Five spines a shot.** |
| 7.7–11.9 | Review cards type in, cursor hits `✓ All`, toast: 15 tapes added | AI reads every spine. **You hit ✓ All.** |
| 11.9–15.5 | Collection table (ID, year, label, condition, status, value), Export menu → Sell Drafts | An ID, a condition, **a price.** |
| 15.5–20.0 | StacksUp wall fills; wordmark, *Be Kind, Rewind!*, `github.com/nitsuah/vhs` | — |

One `TAPES` list feeds the shelf, the crops, the review cards and the table, so the five
spines each crop selects are exactly the titles that come out the other end. Years and
labels are the films' real VHS releases; conditions and values are illustrative.

## Rebuild

From the repo root (Git Bash on Windows; drop `MSYS_NO_PATHCONV=1` and use `$(pwd)` elsewhere).
`capture` wraps the Playwright container; its arguments go straight to `capture.mjs`:

```bash
mkdir -p brag-output/work
capture() { MSYS_NO_PATHCONV=1 docker run --rm -v "$(pwd -W)/promo/brag-20s:/src" -v "$(pwd -W)/brag-output/work:/work" -v vhs-brag-npm:/deps -w /deps mcr.microsoft.com/playwright:v1.63.0-noble bash -c "test -d node_modules/playwright || npm i playwright@1.63.0; cp /src/*.html /src/*.mjs /deps/ && node capture.mjs $*"; }
```

1. Check stills from every scene and mid-transition before a full render:
   `capture /work/stills 4.3 9.9 18.5` → `brag-output/work/stills/t4.3.png` …
2. Render every frame, then make the settled outro (frame 555, 18.5s) the poster and frame 0.
   Replacing frame 0 instead of adding a frame keeps the duration and audio sync unchanged:

```bash
capture /work/frames all
cp brag-output/work/frames/0555.png brag-output/work/frames/0000.png
python promo/brag-20s/audio.py brag-output/work/brag.wav
ffmpeg -y -framerate 30 -i brag-output/work/frames/%04d.png -i brag-output/work/brag.wav -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart -shortest brag-output/brag.mp4
ffmpeg -y -i brag-output/work/frames/0555.png -q:v 3 brag-output/brag.jpg
cp brag-output/brag.mp4 brag-output/brag.jpg site/
```

## Rules learned rendering this

- No FBI-warning cold open. It read as a gimmick before the viewer knew what the product was.
- Show the app UI large. At 720p with the real app's font sizes nothing was readable; the
  composition uses roughly 1.6× the app's sizes inside a 1620px window.
- Scale long spine titles down, never clip them: `fs = min(cap, available / (length × 0.72))`.
- Never index a palette by a divisor of the grid width (the outro wall is 24 wide; the
  palette has 13 entries) or columns repeat.
- Derive label ink from relative luminance (`inkFor`) instead of hard-coding it.
