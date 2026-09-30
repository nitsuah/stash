---
up: "[[repos/fire]]"
title: "fire · storyboard"
source: https://github.com/nitsuah/fire/blob/main/promo/brag-22s/storyboard.md
kind: repo-doc
repo: fire
---

# brag-22s — storyboard

**What it is:** A self-hosted FIRE (Financial Independence, Retire Early) tracker. It puts your whole net worth in one dashboard, projects when you can retire, and lets Claude read it through a read-only MCP server.
**For:** People chasing early retirement who don't want their balances living in someone else's cloud.
**Sets it apart:** It tracks *everything* (brokerage, CDs, gold by the ounce, an ENS wallet, the car), stress-tests your retire date, runs on your machine (`data/db.json`), and has 16 read-only MCP tools.
**Most impressive / funniest:** It counts the 2014 Chevy Malibu.
**Visual hook:** "When can I retire?" is typed. The age races up from 30 while sliding green → amber → coral, then gives up on "Age ??". The dashboard is the answer.
**Share caption:** see share-copy.txt

**Tone:** default (punchy, clean). **Format:** 1920×1080, 30fps, 22s. **Music:** 120 BPM, A minor, cuts on the bar.
**Identity:** bg `#080b11`, violet `#8b5cf6`, emerald `#10b981`, coral `#f43f5e`, amber `#f59e0b`; Outfit headings, Inter body. 🔥 brand mark.

All numbers come from the **demo portfolio** in `promo/demo-seed.js`, seeded into a throwaway DB. They are real app output from the real UI and the real MCP server, not the owner's data.

## Storyboard

| # | Time | Scene |
|---|---|---|
| 1 Hook | 0.0–3.0 | "When can I retire?" is typed big and centered. At 1.3s **Age 30** appears in emerald and counts up faster and faster (to ~67 by 2.2s), shaking harder as it shifts to amber and then coral. At 2.2s it snaps to **Age ??** with a punch and a wobble. Audio: counter ticks climb the A minor scale over a noise riser, then an unresolved F/B/E chord. Timings live in `spot.json` → `hook`. |
| 2 Reveal | 3.0–7.0 | The real dashboard swings in from a 3D tilt on the right. Left column: 🔥 fire, then "Your whole net worth. One dashboard. Your machine." |
| 3 Everything | 7.0–11.0 | "Everything counts." Real Holdings rows stack in one by one: savings, Roth IRA, vitalik.eth, 2 oz Gold Eagles, CD. The last row is the **2014 Chevy Malibu**, with the note "yes, even the Malibu." |
| 4 Stress-test | 11.0–15.0 | The real Retirement Growth Path chart. The cursor clicks 🐻 Bear (−2%) and the curve bends, then clicks 🐂 Bull (+2%). Headline: "Stress-test your retire date." |
| 5 Ask Claude | 15.0–18.5 | A terminal panel: "how close am I to FIRE?" is typed, then the `fire_status_summary` tool call and its real JSON output. Headline: "16 read-only MCP tools." |
| 6 Outro | 18.5–22.0 | 🔥 fire · "Your money. Your machine." · chips `github.com/nitsuah/fire` and `docker compose up fire` · then "TRY IT LIVE" with **lifefire.netlify.app** large underneath (soft E5/A5 chime) |

## Revisions
- **v1:** the hook answered "Age 44." with the subline "12 years away."
- **v2:** the hook counts up from 30 and changes color along a scale, ending on "Age ??". The rest is unchanged.
- **v3:** the outro chip reads `docker compose up fire` (thanks to the new root `compose.yaml`), and the live site URL is added large at the bottom.
- **v4:** the brand reads "fire" everywhere (reveal column, outro logo, share copy) instead of "FIRE Tracker". The live URL stays **lifefire.netlify.app**.
