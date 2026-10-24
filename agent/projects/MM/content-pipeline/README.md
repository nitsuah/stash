# Content pipeline (MM phase 1)

Goal: turn one idea into branded short-form content, in several shapes, cheaply and repeatably, so a future
multi-channel pusher (Hootsuite-like) can post it. No posting happens in phase 1; everything ends as a
`social_posts` draft in Neon.

## Reuse first (already built, in motor-pool `tools/`)

| Need | Existing piece | How to call it |
|---|---|---|
| Script + voice + stock footage + subtitles from a topic | `content-gen` (MoneyPrinterTurbo wrapper, MCP `:3200`) | `/content-gen` skill or MCP `generate_video` |
| Manual or AI-driven edits, captions, effects, export | `opencut` + `opencut-controller` (MCP, 161 tools) | `/opencut` skill |
| Launch/feature spots from a repo or URL | `/brag`, `/brag-slim`, `/promo` skills | skills |
| Local business sites and pitches | `website` (site-gen, MCP `:3201`) | `/site-gen` skill |
| Local LLM for copy at zero API cost | `llm-openllm` | motor-pool stack |

**Preference (user, 2026-10-22):** the `/promo` and `/brag` skills are lighter and more refined than the
motor-pool tools right now, so use them first for master videos; reach for `content-gen`/OpenCut only when
they cannot do the job. Build out this MM folder as needed rather than changing motor-pool.

Motor-pool has no ffmpeg code of its own; MoneyPrinterTurbo uses ffmpeg inside its container.

## What is actually missing (build only this)

1. **brand.json**: one editable file for colors, fonts, logo text, intro and outro lines, per brand
   (`nitsuah-labs` primary, `fps-tech` for the YouTube gaming channel). Variants (A/B) are extra keys, not extra files.
2. **reformat step**: take any finished master video and produce 9:16, 1:1 and 16:9 cuts with the brand
   intro/outro and a burned-in title, using plain ffmpeg in a container. This is the core of the later channel pusher.
3. **prompts/**: the process prompts (idea pick, script, hook variants, captions per platform, post draft) so a
   less capable agent can run each step. See `../prompts/`.
4. **Neon wiring**: each rendered asset becomes a `drafts` row (kind `video`) and a `social_posts` draft.

## Flow

```
ideas (Neon) -> pick idea -> script prompt -> content-gen or opencut render (master)
   -> reformat.sh (3 aspect ratios + brand) -> caption prompt per platform
   -> drafts + social_posts rows (status draft) -> human approval -> (later) pusher posts
```

## Rules

- Phase 1 channels: no X/Twitter or Instagram posting. Reddit only after the user approves each post.
- Drafts speak as the brand, never as the user personally, and never in first person as the user.
- Everything A/B-able lives in `brand.json` variants; log which variant each asset used in `drafts.notes`.
