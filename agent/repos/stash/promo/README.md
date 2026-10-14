---
up: "[[repos/stash]]"
title: "stash · README"
source: https://github.com/nitsuah/stash/blob/main/promo/README.md
kind: repo-doc
repo: stash
---

# promo/

Promo spots for stash. stash has no app to film, so each spot composes real artifacts (issues, terminal output, screenshots from the repos it serves) in a `compose.html` whose `window.render(t)` is a pure function of time.

```bash
promo/build.sh journeys-19s --stills 1.5,5,9,15   # look at a few frames
promo/build.sh journeys-19s --publish             # render, then copy the web cut + poster to pages/assets/
```

Everything runs in Docker (`promo/Dockerfile`: Playwright Chromium, numpy/scipy, ffmpeg). Output goes to `promo/out/<spot>/` (gitignored). Spots and features are tracked in `spots.json` ([showcase standard](https://github.com/nitsuah/.github/blob/main/showcase/STANDARD.md)).

| Spot | Page | Source |
|---|---|---|
| `brag-20s` | [index.html](https://github.com/nitsuah/stash/blob/main/pages/index.html) hero | one-off, source not kept |
| `journeys-19s` | [journeys.html](https://github.com/nitsuah/stash/blob/main/pages/journeys.html) | `journeys-19s/` |
