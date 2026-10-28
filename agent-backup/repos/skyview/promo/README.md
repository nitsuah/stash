---
up: "[[repos/skyview]]"
title: "skyview · README"
source: https://github.com/nitsuah/skyview/blob/main/promo/README.md
kind: repo-doc
repo: skyview
---

# Promo spots

Short videos for the [Pages showcase](https://nitsuah.github.io/skyview/), rendered locally in Docker. All spots are published to `showcase/media/` (`spots.json` `published`); the page embeds `book-18s`. The contract is the [visual showcase standard](https://github.com/nitsuah/.github/blob/main/showcase/STANDARD.md); [`spots.json`](https://github.com/nitsuah/skyview/blob/main/promo/spots.json) records what each spot covers and when it was rendered.

| Spot | Shows | Length |
|---|---|---|
| `site-14s` | hero with the cursor drone, service packages, gallery | 14 s |
| `book-18s` | post a job, operator directory, booking dialog with the availability hint, operator hours, dashboard | 18 s |
| `portal-12s` | token generator CLI, expired code, lockout | 12 s |
| `hero-30s` | every scene above in one cut, with one hook and one outro | 30 s |
| `hero-30s-vert` | 9:16 narrated short: hero, gallery, booking, portal | 29.8 s |

## Render

```bash
promo/build.sh site-14s                    # frames, audio, mp4, poster, web cut
promo/build.sh site-14s --stills 1.5,5,9   # a few frames and a contact sheet, for review
promo/build.sh site-14s --audio            # re-synth the audio and remux
promo/build.sh site-14s --publish          # also copy the web cut and poster to showcase/media/
```

Output goes to `promo/out/<spot>/` (gitignored). The build fails if the encoded frame count is not `duration × fps`.

## How it fits together

- **One composition.** `hero-30s/compose.html` holds every scene and exposes `window.render(t)`, a pure function of time. `hero-30s/synth.py` writes the music and sound effects from the same scene list.
- **A spot is a scene list.** Each `<spot>/spot.json` lists `["scene-id", start, end]` rows. The feature spots set `"base": "hero-30s"` and play only their own scenes, so they share no intro with each other. A new cut is a `spot.json` plus a `share-copy.txt`.
- **Real UI.** Scenes are the CI screenshots in `docs/screenshots/` (mocked demo data, see `tests/visual-docs/`) with a moving camera, highlights and a cursor. The terminal scene is real `scripts/portal-token.js` output under a throwaway salt. `assets/hero-clean.jpg` is the homepage hero without the cursor drone (`assets/capture-hero.mjs`), because the spot animates its own.
- **Camera and highlight positions** in `compose.html` are fractions of each screenshot. When a screenshot's layout changes, check the stills before publishing.

## After the UI changes

The screenshots regenerate in CI, the videos do not. Re-render the spots whose features changed, publish, and update `rendered` in `spots.json`.
