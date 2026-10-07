---
up: "[[repos/fire]]"
title: "fire · features"
source: https://github.com/nitsuah/fire/blob/main/promo/features.md
kind: repo-doc
repo: fire
---

# Promo feature ledger

Everything a promo can claim about fire, the line we use for it, and how to show it on screen. Every row is backed by the README or `docs/FEATURES.md`, so check there before adding a claim. When a spot uses a feature, add the spot's name to **Used in**. Longer spots can then pull from the unused rows without re-researching.

Capture assets live in `promo/out/capture/crops/` after a run. Anything marked *(needs capture)* needs a new step in `promo/capture.js`.

| # | Feature | Promo line | How to show it | Source | Used in |
|---|---|---|---|---|---|
| 1 | Retire-date question → answer | "When can I retire?" | Count-up age hook → dashboard reveal | README · Projections | brag-22s |
| 2 | Net worth dashboard | "Your whole net worth. One dashboard." | `dash.png` swinging in on a 3D tilt | README · Net Worth Dashboard | brag-22s |
| 3 | Self-hosted, one JSON file | "Your machine." / "Your money. Your machine." | Tagline + `docker compose up fire` chip; `lifefire.netlify.app` big in the outro | README intro | brag-22s |
| 4 | Every asset type counts (savings, Roth, ENS wallet, gold, CDs, car) | "Everything counts." / "yes, even the Malibu." | `hrow-*.png` + `vrow-1.png` stacking in | README · Net Worth, Precious metals, Crypto | brag-22s |
| 5 | Bear/bull scenario bands | "Stress-test your retire date." | `proj-base/bear/bull.png` with cursor clicks | FEATURES · Bull/Bear Scenario Bands | brag-22s |
| 6 | MCP server, 16 read-only tools | "Ask Claude about your money." | Terminal + real `mcp-status.json` | README · MCP Server | brag-22s |
| 7 | Scenario comparison table | "A raise, a crash, inflation: see your FIRE age move." | `scenarios.png` rows appearing | FEATURES · Multi-Scenario FIRE Comparison | site |
| 8 | Growth presets (Conservative → Early Retiree) | "One click from cautious to retire-at-50." | *(needs capture)* Growth Settings card, clicking presets | FEATURES · Growth Presets | |
| 9 | Coast FIRE / Lean / Fat lines | "Lean, Fat, Coast: every flavor of FIRE." | *(needs capture)* chart line toggles | FEATURES · Chart Line Toggles | |
| 10 | Money run-out detection | "Know if the money outlives you." | *(needs capture)* depletion age in bear case | FEATURES · Money Run-Out Detection | |
| 11 | Portfolio insights | "It tells you what you're over-exposed to." | `tab-insights.png` cards | README · Insights | site |
| 12 | Tax-loss harvesting alerts | "Losses you can harvest before year-end." | *(needs capture)* seed a losing position | README · Insights | |
| 13 | Rebalancing tool | "Set a target mix, get the trades." | *(needs capture)* click Recalculate | README · Insights | |
| 14 | CD ladder + maturity markers | "Every CD maturity, on the timeline." | CD markers on `proj-base.png`; *(needs capture)* ladder view | README · CD Ladder Visualizer | |
| 15 | Side Hustle Hub + fee calculators | "Your eBay flips, net of fees." | `tab-sidegig.png` fee calc | README · Side Hustle Tracker | site |
| 16 | eBay OAuth order sync | "Sales import themselves." | *(needs capture)* Settings → eBay | README · eBay Order Sync | |
| 17 | CSV imports (Fidelity, Chase, Capital One, eBay) | "Drop in the CSV. Parsed locally." | *(needs capture)* unified add form | README · CSV Imports | site |
| 18 | Plaid sync | "Or connect it and forget it." | *(needs capture)* Settings connectors | README · Plaid integration | site |
| 19 | Web3 wallets, 8 registered chains | "ENS name in, balance out." | `hrow-4.png` (vitalik.eth); *(needs capture)* wallet form | README · Crypto, Web3 wallet tracking | |
| 20 | Gold/silver at live spot | "Gold by the ounce, at today's spot." | `hrow-5.png` (Gold Eagles · 2oz) | README · Precious metals | |
| 21 | Vehicle VIN decode | "Paste a VIN, get the car." | *(needs capture)* vehicle form | README · Vehicle VIN decode | |
| 22 | Expenses + auto-categorization | "Where the money actually goes." | `tab-expenses.png` | README · CSV Imports (Expenses) | |
| 23 | Live prices over SSE | "Prices update while you watch." | "Live · Today +$…" badge on `dash.png` | README · Yahoo Finance prices | site |
| 24 | AES-256-GCM encryption at rest | "Encrypted at rest." | Text/stat card | README · SYNC_MASTER_KEY | site |
| 25 | Encrypted Google Drive backup | "Backed up, still encrypted." | Text | README · Google Drive encrypted backup | site (states the round trip is still a rollout gate) |
| 26 | Security defaults (API key, loopback, Caddy HTTPS, CSP/SRI, rate limits) | "Locked down by default." | Text/stat card | README · Security headers, HTTPS | site |
| 27 | Read-only to real accounts | "Never moves a cent." | Stat "0 transactions ever initiated" | README intro | site |
| 28 | Responsive mobile layout | "Pocket-sized." | *(needs capture)* 390px viewport | README · Responsive shell | |
| 29 | Browser-only live demo | "Try it live." | `lifefire.netlify.app` (outro, large) | netlify.toml, README | brag-22s, site |
| 30 | REST API | "Everything's an endpoint." | Text / curl snippet | README · REST API | |
| 31 | PWA packaging | "Install fire." | *(future capture)* install prompt / offline shell | docs/FEATURES.md · Planned | |
| 32 | 🌪️ Chaos mode (seeded life events on the projection) | "Every retirement plan assumes nothing goes wrong." | `proj-calm.png` → `proj-chaos.png` with a cursor click on Chaos; callouts placed from `chaos.json` | FEATURES · Chaos Mode | chaos-24s, site |
| 33 | Chaos hover details + net effect | "Hover any marker. See what happened, what led to it, and what it cost." | `proj-tooltip.png` zoom + net effect from `chaos.json` | FEATURES · Chaos Mode | chaos-24s |
| 34 | Chaos on the phone + event list | "Dashboard. Projections. Your phone." | `phone-dash.png` in a phone frame + `chaos-chips.png` | FEATURES · Chaos Mode | chaos-24s |
| 35 | Section layouts + Dashboard widgets | "Make it yours. Collapse, reorder, pin any card." | `dash-edit.png` + `picker.png`, cursor on Add | FEATURES · Customizable Layout | chaos-24s, site |
| 36 | 🛡️ Mitigations (pet insurance, HSA, umbrella…) | "Mitigate the hits." | `mitigations.png` zoom + the dog-surgery cost with/without pet insurance | FEATURES · Chaos Mode | chaos-24s, site |
| 37 | Life-event sequences (parent care → funeral → inherited house) | "See what led to it." | Tooltip "after ⚱️ Family funeral costs" in `proj-tooltip.png` | FEATURES · Chaos Mode | chaos-24s |

## Spots

| Spot | Length | Features used | Folder |
|---|---|---|---|
| brag-22s | 22s, 16:9 | 1–6 | `promo/brag-22s/` |
| site (landing page) | n/a | 2, 4–7, 11, 15, 17, 18, 23–27, 29, 32, 35, 36 | `site/` |
| chaos-24s | 24s, 16:9 | 3, 29, 32–37 | `promo/chaos-24s/` |
