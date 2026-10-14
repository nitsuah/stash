---
up: "[[repos/fire]]"
title: "fire · features"
source: https://github.com/nitsuah/fire/blob/main/promo/features.md
kind: repo-doc
repo: fire
---

# Promo feature ledger

Everything a promo can claim about fire, the line we use for it, and how to show it on screen. Every row is backed by the README or `docs/FEATURES.md`, so check there before adding a claim. When a spot uses a feature, add the spot's name to **Used in**. Longer spots can then pull from the unused rows without re-researching.

Capture assets live in `promo/out/capture/crops/` after a run (`card-*.png` per-card shots come from `capture-tour.js`). Anything marked *(needs capture)* needs a new step in `promo/capture.js` or `promo/capture-tour.js`.

| # | Feature | Promo line | How to show it | Source | Used in |
|---|---|---|---|---|---|
| 1 | Retire-date question → answer | "When can I retire?" | Count-up age hook → dashboard reveal | README · Projections | brag-22s, tour-85s |
| 2 | Net worth dashboard | "Your whole net worth. One dashboard." | `dash.png` swinging in on a 3D tilt, or zooming to the FIRE progress bar | README · Net Worth Dashboard | brag-22s, tour-85s, connect-55s |
| 3 | Self-hosted, one JSON file | "Your machine." / "Your money. Your machine." | Tagline + `docker compose up fire` chip; `lifefire.netlify.app` big in the outro; "1 file" stat | README intro | brag-22s, tour-85s, yours-60s |
| 4 | Every asset type counts (savings, Roth, ENS wallet, gold, CDs, car) | "Everything counts." / "yes, even the Malibu." | `hrow-*.png` + `vrow-1.png` stacking in | README · Net Worth, Precious metals, Crypto | brag-22s, tour-85s |
| 5 | Bear/bull scenario bands | "Stress-test your retire date." | `proj-base/bear/bull.png` with cursor clicks (`proj:bear`, `proj:bull`) | FEATURES · Bull/Bear Scenario Bands | brag-22s, tour-85s, plan-65s |
| 6 | MCP server, 16 read-only tools | "Ask Claude about your money." | Terminal + real MCP output (`mcp-status.json`, `mcp-<tool>.json`) | README · MCP Server | brag-22s, tour-85s, insights-60s, hustle-60s, yours-60s |
| 7 | Scenario comparison table | "A raise, a crash, inflation: see your FIRE age move." | `scenarios.png` | FEATURES · Multi-Scenario FIRE Comparison | site, plan-65s |
| 8 | Growth presets (Conservative → Early Retiree) | "One click, four strategies." | `hero-seeded.png` → `hero-preset-0/2/3.png`, cursor on `preset-N` | FEATURES · Growth Presets | plan-65s |
| 9 | Coast FIRE / Lean / Fat lines | "Every flavor of FIRE." | `proj-base.png` → `proj-lines.png`, clicks on `line-coast`, `line-benchmark` | FEATURES · Chart Line Toggles | plan-65s |
| 10 | Money run-out detection | "If the money would ever run out, they tell you when." | Narration over `card-milestones.png`. The demo never depletes; a depleting seed would show "Money runs out at Age N" *(needs capture)* | FEATURES · Money Run-Out Detection | plan-65s (voice only) |
| 11 | Portfolio insights | "It tells you what you're over-exposed to." | `card-insights.png` (tiles at the top) | README · Insights | site, tour-85s, insights-60s |
| 12 | Tax-loss harvesting alerts | "Harvest your losses." | `card-tlh.png` (SCHD is seeded below cost basis) | README · Insights | insights-60s |
| 13 | Rebalancing tool | "Set a target mix, get the trades." | `card-rebalance-trades.png` (after Recalculate) | README · Insights | insights-60s |
| 14 | CD ladder + maturity markers | "Every CD, on the timeline." | CD markers zoomed on `proj-base.png`; `card-cash.png`; `card-cd-ladder.png` | README · CD Ladder Visualizer | plan-65s, connect-55s |
| 15 | Side Hustle Hub + fee calculators | "Know your margin before you list." | `card-fee-ebay/etsy/fb/mercari/poshmark.png` | README · Side Hustle Tracker | site, tour-85s, hustle-60s |
| 16 | eBay + Etsy OAuth order sync; Mercari/Poshmark/FB CSV import | "Sales import themselves." | `card-ebay-sync.png` → `card-etsy-sync.png` | README · eBay Order Sync, Etsy Order Sync | hustle-60s |
| 17 | CSV imports (Fidelity, Chase, Capital One, eBay) | "Drop in a CSV. Parsed locally." | `card-add-csv.png` | README · CSV Imports | site, connect-55s |
| 18 | Plaid sync | "Or link it." | `card-plaid.png` | README · Plaid integration | site, connect-55s |
| 19 | Web3 wallets, keyless multichain value | "Paste an ENS name." | `hrow-4.png` (fire-demo-wallet.eth); `card-add-account.png` (Crypto + ENS identifier) | README · Crypto, Web3 wallet tracking | brag-22s, tour-85s, connect-55s |
| 20 | Gold/silver at live spot | "Gold at today's spot." | `hrow-5.png`, `card-other-assets.png` | README · Precious metals | tour-85s, connect-55s |
| 21 | Vehicles (value, loan, depreciation; VIN stored) | "Cars at what they're worth." | `card-other-assets.png`, `card-add-vehicle.png` (VIN field). The form stores the VIN; decoding is server-side | README · Vehicle VIN decode | connect-55s |
| 22 | Expenses + auto-categorization | "Statements are categorized automatically." | `card-budget.png`, `card-spending.png` | README · CSV Imports (Expenses) | insights-60s, connect-55s (voice) |
| 23 | Live prices over SSE | "Prices update while you watch." | Zoom on the `dash.png` header | README · Yahoo Finance prices | site, connect-55s |
| 24 | AES-256-GCM encryption at rest | "Encrypted at rest." | Stat tile | README · SYNC_MASTER_KEY | site, tour-85s, yours-60s |
| 25 | Encrypted Google Drive backup | "Backed up, still encrypted." | Text; `card-drive.png` | README · Google Drive encrypted backup | site (states the round trip is still a rollout gate) |
| 26 | Security defaults (API key, loopback, Caddy HTTPS, CSP/SRI, rate limits) | "Locked down by default." | Bullets beside `card-privacy.png` | README · Security headers, HTTPS | site, yours-60s |
| 27 | Read-only to real accounts | "Never moves a cent." | "$0 ever moved" stat | README intro | site, tour-85s, yours-60s |
| 28 | Responsive mobile layout | "Pocket-sized." | `phone-dash.png` in a phone frame | README · Responsive shell | chaos-24s, chaos-60s, yours-60s |
| 29 | Browser-only live demo | "Try it live." | `lifefire.netlify.app` (outro, large) | netlify.toml, README | every spot, site |
| 30 | REST API + JSON/CSV export | "Everything's an endpoint." | `card-data.png` + bullets | README · REST API | yours-60s |
| 31 | PWA packaging | "Install fire." | *(future capture)* install prompt / offline shell | docs/FEATURES.md · Planned | |
| 32 | 🌪️ Chaos mode (seeded life events on the projection) | "Every retirement plan assumes nothing goes wrong." | `proj-calm.png` → `proj-chaos.png` with a cursor click on Chaos; callouts placed from `chaos.json` | FEATURES · Chaos Mode | chaos-24s, site, tour-85s, chaos-60s |
| 33 | Chaos hover details + net effect | "Hover any marker. See what happened, what led to it, and what it cost." | `proj-tooltip.png` zoomed to `chaos:hover`, plus the net effect from `chaos.json` | FEATURES · Chaos Mode | chaos-24s, chaos-60s |
| 34 | Chaos on the phone + event list | "Dashboard. Projections. Your phone." | `phone-dash.png` in a phone frame + `chaos-chips.png` | FEATURES · Chaos Mode | chaos-24s, chaos-60s |
| 35 | Section layouts + Dashboard widgets | "Make it yours. Collapse, reorder, pin any card." | `dash-edit.png` + `picker.png`, cursor on Add | FEATURES · Customizable Layout | chaos-24s, site, yours-60s |
| 36 | 🛡️ Mitigations (pet insurance, HSA, umbrella…) | "Mitigate the hits." | `mitigations.png` zoom + the dog-surgery cost with/without pet insurance | FEATURES · Chaos Mode | chaos-24s, site, chaos-60s |
| 37 | Life-event sequences (parent care → funeral → inherited house) | "See what led to it." | Tooltip "after ⚱️ Family funeral costs" in `proj-tooltip.png` | FEATURES · Chaos Mode | chaos-24s, chaos-60s |
| 38 | Side gig tax tags + tax summary | "One ledger. Tax-ready." / "What do I owe?" | `card-ledger.png` (seeded tags + item costs); terminal with `get_side_gig_tax_summary` | FEATURES · Side Hustle Tracker | hustle-60s |
| 39 | Asset allocation drill-down | "Drill into any slice." | `card-allocation.png` → `card-allocation-drill.png` | FEATURES · Asset Allocation Drill-Down | insights-60s |
| 40 | Milestone predictions | "Milestones, with dates." | `card-milestones.png` + bullets | FEATURES · Growth + Milestone Panel | plan-65s |
| 41 | Cash flow + savings rate | "Where the money goes." | `card-cashflow.png` + bullets | FEATURES · Financial Overview | insights-60s |
| 42 | Side Hustle Accelerators | "Need a new stream?" | `card-accelerators.png` + bullets | FEATURES · Side Hustle Accelerators | hustle-60s |
| 43 | Emergency runway via MCP | "What happens if I lose my job?" | Terminal with `get_emergency_runway` | README · MCP Server | yours-60s |
| 44 | Concentration risk via MCP | "Am I too concentrated?" | Terminal with `get_concentration_risk` | README · MCP Server | insights-60s |
| 45 | CoinTracker wallets (optional) | "CoinTracker works too." | Voice only; `card-cointracker.png` exists | FEATURES · CoinTracker Wallets | connect-55s (voice) |
| 46 | Claude skills (fire-coach, reseller-autopilot, passive-income-lab) | "…plus a FIRE coach skill." | Terminal subtitle | skills/README.md | tour-85s, yours-60s |

## Spots

| Spot | Length | Features used | Folder |
|---|---|---|---|
| brag-22s | 22s, 16:9, narrated | 1–6, 19 | `promo/brag-22s/` |
| chaos-24s | 24s, 16:9, narrated | 3, 28, 29, 32–37 | `promo/chaos-24s/` |
| tour-85s | ~83s, 16:9, narrated | 1–6, 11, 15, 19, 20, 24, 27, 29, 32, 46 | `promo/tour-85s/` |
| plan-65s | ~65s, narrated | 5, 7–10, 14, 29, 40 | `promo/plan-65s/` |
| chaos-60s | ~62s, narrated | 28, 29, 32–34, 36, 37 | `promo/chaos-60s/` |
| insights-60s | ~60s, narrated | 6, 11–13, 22, 29, 39, 41, 44 | `promo/insights-60s/` |
| hustle-60s | ~60s, narrated | 6, 15, 16, 29, 38, 42 | `promo/hustle-60s/` |
| connect-55s | ~57s, narrated | 2, 14, 17–23, 29, 45 | `promo/connect-55s/` |
| yours-60s | ~61s, narrated | 3, 6, 24, 26–30, 35, 43, 46 | `promo/yours-60s/` |
| site (landing page) | n/a | 2, 4–7, 11, 15, 17, 18, 23–27, 29, 32, 35, 36 | `site/` |

Not in any spot yet: 25 (Drive backup, rollout-gated), 31 (PWA, planned), and notifications/alerts (`card-alerts.png` is captured).
