---
up: "[[repos/nitsuah-io]]"
title: "nitsuah-io · social-preview-placeholder"
source: https://github.com/Nitsuah-Labs/nitsuah-io/blob/main/public/social-preview-placeholder.md
kind: repo-doc
repo: nitsuah-io
---

# Social Preview Image

`public/og-image.jpg` (1200×630 JPEG) is the site-wide `og:image` / `twitter:image`, wired through `DEFAULT_OG_IMAGE` in `src/lib/seo.ts`. It's a crop of the landing hero from `public/social-preview.png` (a full-page screenshot, also used as the JSON-LD person image and organization logo in `src/lib/schema.ts`).

The earlier `social-preview.svg` placeholder never existed in `public/`, so every page's `og:image` returned 404. Most social networks ignore SVG previews anyway.

## Replacing it

- Keep it 1200×630 and under ~300 KB, as a JPEG or PNG (not SVG).
- Keep the text readable at small sizes; LinkedIn and Slack render it at about 500px wide.
- Overwrite `public/og-image.jpg` (the path is referenced in one place, `src/lib/seo.ts`).
- Blog posts use their own `image` from `src/data/blogs.json` when it's a raster file that exists, and otherwise fall back to this one. `src/__tests__/seo.test.ts` fails if a referenced image is missing.
