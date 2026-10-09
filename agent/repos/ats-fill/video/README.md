---
up: "[[repos/ats-fill]]"
title: "ats-fill · README"
source: https://github.com/nitsuah/ats-fill/blob/main/video/README.md
kind: repo-doc
repo: ats-fill
---

# Feature tour video

A long-form YouTube walkthrough of every ats-fill feature, generated from the
real extension running on fictional demo data. Nothing is screen-recorded by
hand, so the video can be re-rendered whenever the UI changes. It renders in
native 4K (3840x2160, 30 fps) in the same Ledger look as the launch video.

It is built as **one short per feature** that can stand alone, plus a
**combined cut** that strings the shorts together. Each short ends on the
"Add to Chrome" call to action; the combined cut drops those repeated CTA
slides, opens with one intro card, and ends on a single CTA.

```
short   = [chapter title] → [steps…] → [CTA]
tour    = [intro] → ([chapter title] → [steps…]) × 7 → [CTA]
```

Within a chapter the steps play in one browser window: each screen holds still
on the whole page, the camera eases in on the step's `focus` area, then eases
back out while a cursor clicks whatever leads to the next screen, and the
screenshot, URL and caption crossfade. Chapters, the intro and the CTA dip
through the paper background.

## Why it looks sharp on YouTube

- **4K upload.** YouTube encodes 2160p uploads with its higher-bitrate VP9/AV1
  ladder, and viewers watching at 1080p get those encodes too.
- **Rendered, not resampled.** Product screens are captured at 3x (3840x2400)
  and every video frame is a Chrome render at 2x device pixels, so text is
  rasterised at the output size even mid-zoom. Grayscale antialiasing avoids
  colour fringes that 4:2:0 chroma smears.
- **Still holds.** Reading time is spent on perfectly still frames (rendered
  once, held for N frames), which compress to near-lossless; motion is limited
  to short eased moves. The old 3% push-in on every frame made each frame
  different and was the main source of blur after YouTube re-encoded it.
- **Correct colour.** RGB → BT.709 conversion with matching colour tags, so
  the paper and vermilion don't shift after transcoding.

## Files

| File | Role |
| --- | --- |
| `video/narration.mjs` | Voiceover script: reads the on-screen copy (intro, chapter titles, step captions, CTA), with pronunciation fixes for acronyms. |
| `scripts/voice/narrate.mjs` + `tts.py` | Synthesises each line with [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) (local, offline, Apache-2.0 weights) into `video-build/voice/`. Cached by text, so only edited lines are regenerated. |
| `video/storyboard.mjs` | What each chapter and step shows and says, its focus area, plus timing. Edit copy here. |
| `video/timeline.mjs` | Motion: one pose per frame (dips, title rise, camera zoom, crossfades, cursor, stamp). Unit-tested in `tests/video-timeline.test.mjs`. |
| `video/stage.mjs` | Frame templates on a 1920×1080 CSS canvas rendered at 2x (landing-page fonts and colors), each with a `pose()` hook. |
| `tests/e2e/feature-video.spec.mjs` | Drives the extension through every step, records focus and click rects, and renders every distinct frame plus `manifest.json`. The form-fill chapter runs a real fill on the fictional ATS fixture. Skipped unless `ATS_FILL_VIDEO=1`. |
| `scripts/build-feature-video.mjs` | ffmpeg: encodes each unit (intro, chapters, CTA) once, joins them without re-encoding into shorts and the combined cut, lays the narration on one loudness-normalised track per video, and writes the 1080p web cut, captions, chapters and thumbnail. |
| `scripts/publish-feature-tour.mjs` | `npm run video:publish`: copies the web cut into `site/assets/` for the landing page. |

## Render

Everything runs in Docker (Playwright + Chromium + ffmpeg + Kokoro TTS). Render one video at a time: a 4K encode needs ~2 GB, and two renders at once can run Docker Desktop out of memory.

```bash
docker build --target video -t ats-fill:video .
```

```bash
docker run --rm -v "$PWD/video-build:/app/video-build" ats-fill:video
```

Or run **Actions → Feature Tour Video**. Set `release_tag` to also attach the 4K master, shorts and captions to that GitHub Release.

Output in `video-build/out/` (gitignored):

| Output | Use |
| --- | --- |
| `ats-fill-feature-tour.mp4` | Narrated combined cut (2160p30, H.264, BT.709, AAC): upload to YouTube |
| `shorts/NN-<chapter>.mp4` | Per-feature shorts: social posts, docs, or separate uploads |
| `youtube.md` | Title, description with **chapter timestamps**, links and tags, ready to paste |
| `thumbnail.jpg` | 1280×720 thumbnail |
| `web/feature-tour.mp4` | 1080p narrated cut (< 50 MB) for the landing page |
| `web/feature-tour.jpg`, `web/feature-tour.en.vtt`, `web/feature-tour.chapters.vtt` | Its poster, English captions (also upload these to YouTube) and chapters |

## Where each cut lives

| Cut | Home | How it gets there |
| --- | --- | --- |
| 1080p web cut, poster, captions, chapters | `site/assets/` in git, played on GitHub Pages (`#tour`) | `npm run video:publish`, then commit |
| 4K master + shorts | YouTube, plus a GitHub Release asset | Upload by hand; the workflow's `release_tag` input attaches them to a release |
| 23s launch video | `site/assets/ats-fill.mp4` (hero) | Made separately with `/brag` |

The 4K master (~190 MB) can't go in git: GitHub rejects files over 100 MB and Pages doesn't serve Git LFS.

## Narration

On by default with the `af_heart` voice at 1.1x. Holds stretch so each line finishes before the next screen; captions are timed from the same cues. Change the voice with `-e KOKORO_VOICE=am_michael` (any [Kokoro voice](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)) or the pace with `-e KOKORO_SPEED=1.0`, or render silent with `-e ATS_FILL_VOICE=0`. If a word is mispronounced, add it to `SAY` in `video/narration.mjs`.

Background music is optional and ducks under the narration. Pass a track you have the rights to:

```bash
docker run --rm -v "$PWD/video-build:/app/video-build" -v "$PWD/music.mp3:/app/music.mp3:ro" ats-fill:video \
  sh -c "npm run video -- --music /app/music.mp3"
```

## Changing the video

- **Copy or timing**: edit `video/storyboard.mjs`. Hold time is derived from caption length (6–11s) unless a step sets `hold`; each step gets 1.5s more for its motion.
- **Zoom**: set a step's `focus` to a CSS selector on the captured screen. The camera frames it (up to 1.7x); leave it out to stay on the whole screen.
- **Cursor**: call `aim('<next step id>', locator)` in the spec just before the click that leads to that step. Targets off screen are skipped.
- **New step**: add it to the storyboard, then add a matching `shoot('<id>', …)` capture in the spec. The spec fails if a storyboard step has no capture.
- **Quick preview**: `-e ATS_FILL_VIDEO_SCALE=1` on `docker run` renders at 1080p in about half the time.
- **New chapter**: add a segment; title cards, chapter lists, shorts and YouTube chapters update automatically.

All names, companies and applications in the video are fictional demo data from `tests/e2e/helpers/demo-state.mjs`.
