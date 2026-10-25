# Content process prompts (phase 1: draft only, nothing posts)

Each step is written so a smaller or cheaper agent can run it alone. Inputs come from Neon (`moneymakers`,
project `divine-surf-90579532`); outputs go back to Neon. Never post; never write as the user in first person.

## 0. Rules for every step
- Brand voice is the brand's (Nitsuah Labs or FPS Tech), not the user's personal voice.
- No X/Twitter or Instagram. Reddit only with per-post user approval. Phase 1 ends at `status = 'draft'`.
- Claims must be true of the product as it exists. No invented testimonials, numbers or dates.
- Record the brand variant (A/B from `content-pipeline/brand.json`) in `drafts.notes`.

## 1. Pick the idea
> Query `ideas` where `status in ('backlog','selected')`. Rank by: already built or nearly built
> (`project_id` not null), free to demo, one clear first step. Return the top 3 with one sentence each on why.
> Update the chosen row to `selected`.

## 2. Script (30 to 45 seconds)
> Write a 30 to 45 second script for `<idea>` in the voice of `<brand>`. Structure: hook (one line, a concrete
> problem), 3 beats (each one short sentence a viewer can act on), call to action pointing at the free
> thing first and the paid thing second. Output 3 alternative hooks labeled H1 to H3 for A/B testing.
> No first-person claims about the user's life.

## 3. Master video
> Prefer `/promo` or `/brag-slim` (lighter, more refined) to render the master from the script or the
> project's repo/URL. Use `/content-gen` or OpenCut only if those cannot produce it. Save as
> `content-pipeline/<slug>.mp4`.

## 4. Reformat to all shapes
```
bash content-pipeline/run.sh <slug>.mp4 <brand> <A|B> "<short title>"
```
Produces vertical, square and landscape cuts in `content-pipeline/out/`.

## 5. Captions per platform
> From the script write: a YouTube title (max 70 chars) and description; a LinkedIn post (3 short
> paragraphs); a Reddit-style title plus neutral body that discloses the product is ours; a short
> alt-text line for the thumbnail. Include the product link in platform copy where appropriate. Thumbnail alt text should describe the image, not require a product link. Keep each under the
> platform's limit. No hashtags spam (max 3).

## 6. Record
> Insert one `drafts` row per asset (project_id, kind `video` or `caption`, body, notes = brand + variant +
> hook id) and one `social_posts` row per platform with `status = 'draft'`. Do not set `scheduled_for`.

## 7. Review loop (weekly)
> For each posted or tested asset, record views and clicks in `social_posts.result`. Compare variants A and B
> in `experiments`. Keep what won, drop what lost, queue the next idea.
