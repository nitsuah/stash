---
up: "[[repos/fire]]"
title: "fire · storyboard"
source: https://github.com/nitsuah/fire/blob/main/promo/chaos-24s/storyboard.md
kind: repo-doc
repo: fire
---

# chaos-24s — storyboard

**What it is:** fire's 🌪️ Chaos mode, 🛡️ mitigations and section-based layouts. Chaos rolls seeded, realistic life events (with follow-ups like a funeral → an inherited house) onto the retirement projection. Mitigations like pet insurance shrink the hits they cover. Every tab is built from sections you can rearrange.
**For:** FIRE planners whose spreadsheet assumes a perfectly smooth line.
**Sets it apart:** The events are specific and believable, come in sequences, and include good news. Costs that outrun inflation escalate. Every marker explains itself on hover.
**Most impressive / funniest:** The plan said $1.8M at 62. Two kids, a dog that tore its ACL and an aging parent later, it's $886K less, even with a rental house inherited along the way.
**Visual hook:** "Every retirement plan assumes nothing goes wrong." Then "nothing" is struck through in coral.
**Share caption:** see share-copy.txt

**Tone:** default (punchy, clean). **Format:** 1920×1080, 30fps, 24s. **Music:** 120 BPM, A minor; a calm pad for the hook, with the groove dropping on the Chaos click.
**Identity:** bg `#080b11`, violet `#8b5cf6`, emerald `#10b981`, coral `#f43f5e`, amber `#f59e0b`, chaos pink `#ec4899`; Outfit headings, Inter body.

All numbers and events are real app output for the fictional demo portfolio (`promo/demo-seed.js`) with chaos seed 23 (`CHAOS_SEED` in `capture.js`). Event callouts are positioned from the real chart's data points (`chaos.json`). In the Mitigate scene the "after" amount is the real dog-surgery cost from `chaos.json` with pet insurance's 80% coverage applied, which is what the engine does when it's ticked.

## Storyboard

| # | Time | Scene |
|---|---|---|
| 1 Hook | 0.0–3.5 | "Every retirement plan / assumes nothing goes wrong." pops in word by word over a calm violet curve drawing itself. At 2.45s "nothing" is struck through in coral and the curve shudders. |
| 2 Chaos | 3.5–8.5 | "🌪️ Chaos mode" + "Realistic life events, rolled onto your plan." The real Projections chart slides up. The cursor clicks **🌪️ Chaos** at 4.5s and the groove drops. Five real callouts with leader lines pop at their markers: inherited house, dog emergency surgery, windfall, aging parent care, funeral. |
| 3 Hover | 8.5–11.5 | Zoom into the real hover tooltip at Age 34: child birth, a funeral, then "Inherited a house … after ⚱️ Family funeral costs, age 33". Right: "Hover any marker." / "See what happened, what led to it, and what it cost." and the real net effect **−$886K** by age 62. |
| 4 Everywhere | 11.5–14.5 | A phone frame with the real mobile Dashboard (one column, chaos on). Right: "Dashboard. Projections. Your phone." The real event-chip list wipes in, then "🎲 Reroll for a different life." |
| 5 Mitigate | 14.5–18.0 | "🛡️ Mitigate the hits." / "Tick the coverage you have. Chaos applies it, and what it costs." The real Dental and Pet insurance cards; the cursor ticks Pet insurance. Below: "🐕 Dog emergency surgery −$6.6K → −$1.3K with pet insurance · ~$50/mo". |
| 6 Make it yours | 18.0–21.0 | "Make it yours." / "Collapse, reorder, pin any card." The real Dashboard in Customize mode (sections with layout pickers) tilts in; the real widget picker pops over it and the cursor clicks **Add**. |
| 7 Outro | 21.0–24.0 | 🔥 fire · "Plan for the life you'll actually live." · chips `github.com/nitsuah/fire` and `docker compose up fire` · TRY IT LIVE **lifefire.netlify.app** |

## Revisions

- **v1 (chaos-22s):** seed 60, 22s, no mitigations.
- **v2 (chaos-24s):** seed 23 for a funeral → inherited house sequence; adds the Mitigate scene; tooltip and callouts follow the new events; the phone shot shows the one-column fix.
