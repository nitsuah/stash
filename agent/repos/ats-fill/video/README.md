---
up: "[[repos/ats-fill]]"
title: "ats-fill · README"
source: https://github.com/nitsuah/auto-apply-plugin/blob/main/video/README.md
kind: repo-doc
repo: ats-fill
---

# Feature tour video

A long-form YouTube walkthrough of every ats-fill feature, generated from the
real extension running on fictional demo data. Nothing is screen-recorded by
hand, so the video can be re-rendered whenever the UI changes.

It is built as **one short per feature** that can stand alone, plus a
**combined cut** that strings the shorts together. Each short ends on the
"Add to Chrome" call to action; the combined cut drops those repeated CTA
slides, opens with one intro card, and ends on a single CTA.

```
short   = [chapter title] → [steps…] → [CTA]
tour    = [intro] → ([chapter title] → [steps…]) × 7 → [CTA]
```

## Files

| File | Role |
| --- | --- |
| `video/storyboard.mjs` | What each chapter and step shows and says, plus timing. Edit copy here. |
| `video/stage.mjs` | 1920×1080 frame templates (landing-page fonts and colors). |
| `tests/e2e/feature-video.spec.mjs` | Drives the extension through every step and renders the frames. The form-fill chapter runs a real fill on the fictional ATS fixture. Skipped unless `ATS_FILL_VIDEO=1`. |
| `scripts/build-feature-video.mjs` | ffmpeg: slow push-in per frame, dip-to-paper transitions, shorts, combined cut, chapters, thumbnail. |

## Render

Everything runs in Docker (Playwright + Chromium + ffmpeg):

```bash
docker build --target video -t ats-fill:video .
```

```bash
docker run --rm -v "$PWD/video-build:/app/video-build" ats-fill:video
```

Or run **Actions → Feature Tour Video** and download the `ats-fill-feature-tour` artifact.

Output in `video-build/out/` (gitignored):

| Output | Use |
| --- | --- |
| `ats-fill-feature-tour.mp4` | Combined cut (1080p30, H.264): upload to YouTube |
| `shorts/NN-<chapter>.mp4` | Per-feature shorts: social posts, docs, or separate uploads |
| `youtube.md` | Title, description with **chapter timestamps**, links and tags, ready to paste |
| `thumbnail.jpg` | 1280×720 thumbnail |

Background music is optional. Pass a track you have the rights to:

```bash
docker run --rm -v "$PWD/video-build:/app/video-build" -v "$PWD/music.mp3:/app/music.mp3:ro" ats-fill:video \
  sh -c "npm run video -- --music /app/music.mp3"
```

## Changing the video

- **Copy or timing**: edit `video/storyboard.mjs`. Hold time is derived from caption length (6–11s) unless a step sets `hold`.
- **New step**: add it to the storyboard, then add a matching `shoot('<id>', …)` capture in the spec. The spec fails if a storyboard step has no capture.
- **New chapter**: add a segment; title cards, chapter lists, shorts and YouTube chapters update automatically.

All names, companies and applications in the video are fictional demo data from `tests/e2e/helpers/demo-state.mjs`.
