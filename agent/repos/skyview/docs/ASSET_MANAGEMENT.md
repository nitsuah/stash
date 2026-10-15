---
up: "[[repos/skyview]]"
title: "skyview · ASSET_MANAGEMENT"
source: https://github.com/nitsuah/skyview/blob/main/docs/ASSET_MANAGEMENT.md
kind: repo-doc
repo: skyview
---

# Asset Management Guide

> 🧭 [skyview](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](../METRICS.md) <!-- nav -->

Gallery content lives in the repository. `assets/gallery.json` lists the items, and the image and video files sit in `assets/gallery/`. Pushing a change to `main` triggers a Netlify deploy.

## Managing Gallery Images

1. Add the image or video file to `assets/gallery/`.
2. Add or edit its entry in `assets/gallery.json` (every field is described in section 5).
3. Commit and push. Netlify deploys the change.

## Using External Assets (Cloudinary/S3)

If you have large video files or want to host images externally, set the `src` field of the item in `assets/gallery.json` to the full URL (e.g., `https://res.cloudinary.com/...`). This keeps large media out of the git repository.

## 4. Video Assets

Video is **natively supported**. The gallery renders `<video>` elements with playback controls for any entry that has `"type": "video"` in `assets/gallery.json`. No external hosting (YouTube/Vimeo) is required for MP4/MOV files.

Add a video entry to `assets/gallery.json`:

```json
{
  "src": "assets/gallery/your-clip.mp4",
  "alt": "Aerial flyover of the marina",
  "category": "landscape",
  "type": "video",
  "active": true
}
```

Place the file in `assets/gallery/` and push — the gallery loads it automatically.

## 5. Gallery JSON Fields

All fields supported in `assets/gallery.json` (edit directly in the file):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| src | string | yes | Path or URL to the image/video file |
| alt | string | yes | Alt text (accessibility and SEO) |
| category | string | yes | One of: events, real_estate, landscape, commercial |
| season | string | no | One of: all, spring, summer, fall, winter (default: all) |
| displayOrder | number | no | Sort priority 1–999; lower = appears first |
| active | boolean | no | false hides the item without deleting it (default: true) |
| featured | boolean | no | Marks entry for spotlight use (default: false) |
| type | string | no | Set to `"video"` for MP4/MOV files; omit or leave blank for images |
