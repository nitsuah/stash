# MoneyMakers trace: what exists, where it lives, how it is hooked up

Source of truth is Neon project `moneymakers` (`divine-surf-90579532`): tables `projects` (project state), `assets` (what we built and where it goes), `hookups` (accounts, auth state, how to reconnect), `ideas`, `experiments`, `money_events`, and view `project_pnl`. This file is a readable snapshot (2026-10-23); when it disagrees with Neon, trust Neon.

## Pipelines (no Claude usage once built)
| Pipeline | Where | Run | Output |
|---|---|---|---|
| Asset factory | `MM/asset-factory` | `bash run.sh [seed]` (Docker: python:3-slim, playwright v1.64.0-noble) | `out/*.zip` plus `out/listings.csv` |
| Pack factory | `MM/pack-factory/build_batch1-4.py` | python:3-slim | `out*/` zips for Gumroad |
| Tools site | `MM/tools-site/build_site.py` | python:3-slim, `TOOLS_BASE`/`TOOLS_HOST` for the nitsuah.io variant | `public/tools` in nitsuah-io |
| Audit scanner | `MM/audit-scanner/scan.mjs` | node in playwright image | JSON plus markdown reports |
| Content pipeline | `MM/content-pipeline` | `run.sh` (ffmpeg in Docker) | 9:16, 1:1, 16:9 cuts |

## Destinations and hookups
- **Gumroad** nitsua5.gumroad.com: 10 products live, $0 sales. Hard limit of 10 new products per day. 26 packs queued.
- **Etsy**: account exists, shop not created (needs the user's billing card, bank and ID). Drafts in `MM/etsy-listings/listings.md`; machine-readable titles, prices and tags in `MM/asset-factory/out/listings.csv`.
- **Stripe** (live): tip link in `nitsuah/.github` `.github/FUNDING.yml`. Dashboard works through Chrome; Stripe MCP is not authenticated.
- **nitsuah.io/tools**: 25 free tools, tip link only. Old standalone site redirects through `agent/projects/MM/tools-site/redirect-site/_redirects`.
- **Downloads site**: staged in `MM/packs-host` (31 zips under random names), not deployed; public deploy needs the user's approval (idea 157).

## Rules in force
No advertising, outreach or social posting until 2027. Drafts only for email. No sending or publishing without approval beyond what the user already allowed. Docker for all node and python runs.

## Improve next
Schedule the asset factory in CI (idea 174), list the Etsy packs once the shop exists, and add generators for ideas 169 to 173.
Go back on all old assets and improve quality 10x in various ways to increase desire/profitability of assets.