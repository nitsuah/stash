---
up: "[[repos/ats-fill]]"
title: "ats-fill · CHROME_WEB_STORE_ASSETS"
source: https://github.com/nitsuah/auto-apply-plugin/blob/main/docs/CHROME_WEB_STORE_ASSETS.md
kind: repo-doc
repo: ats-fill
---

# Chrome Web Store assets

> 🧭 [ats-fill](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

The listing images are generated from the deterministic Playwright fixture
(`tests/e2e/store-assets.spec.mjs`) and checked against the
[Chrome Web Store image specs](https://developer.chrome.com/docs/webstore/images)
by `scripts/validate-store-assets.mjs`.

| File | Size | Format | Dashboard slot |
| --- | ---: | --- | --- |
| store-icon-128.png | 128×128 | PNG, 96×96 artwork in 16px transparent padding | Store icon |
| screenshot-01-main.jpg | 1280×800 | JPEG, 24-bit RGB, full bleed | Screenshot 1 |
| screenshot-02-tracker.jpg | 1280×800 | JPEG, 24-bit RGB, full bleed | Screenshot 2 |
| screenshot-03-job-search.jpg | 1280×800 | JPEG, 24-bit RGB, full bleed | Screenshot 3 |
| screenshot-04-interview-prep.jpg | 1280×800 | JPEG, 24-bit RGB, full bleed | Screenshot 4 |
| screenshot-05-analytics.jpg | 1280×800 | JPEG, 24-bit RGB, full bleed | Screenshot 5 |
| small-promo.jpg | 440×280 | JPEG, 24-bit RGB | Small promo tile |
| marquee-promo.jpg | 1400×560 | JPEG, 24-bit RGB | Marquee promo tile |

Five screenshots is the Store maximum, so this is the complete listing set.

## Where they are built

- **Every CI run** builds the set and uploads it as the `chrome-web-store-assets`
  workflow artifact, so UI changes show up in the listing images before release.
- **Every release** (`.github/workflows/chrome-release.yml`) rebuilds the set from
  the release tag, validates it, and attaches `ats-fill-vX.Y.Z-store-assets.zip`
  to the GitHub Release. The run summary repeats the steps below.

## Updating the listing after a release

The Chrome Web Store API (v2) uploads and publishes the extension package only;
it has no endpoint for listing images or text, so this one step is manual:

1. Download `ats-fill-vX.Y.Z-store-assets.zip` from the
   [GitHub Release](https://github.com/nitsuah/ats-fill/releases) and unzip it.
2. Open the [Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   → ats-fill → **Store listing**.
3. Replace the store icon, the five screenshots (in file order) and both promo
   tiles using the table above, then **Save draft** and submit. Listing edits go
   through review alongside, or separately from, the package.

Listing: <https://chromewebstore.google.com/detail/ats-fill/amofaeopfmaicbiijgjaojenedkkadmn>

## Privacy / determinism

The capture uses `tests/e2e/helpers/demo-state.mjs`. Names, companies, URLs,
resume content and application history are fictional. No developer profile,
resume, API key or live application data is used.
