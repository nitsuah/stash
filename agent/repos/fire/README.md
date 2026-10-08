---
up: "[[repos/fire]]"
title: "fire · README"
source: https://github.com/nitsuah/fire/blob/main/README.md
kind: repo-doc
repo: fire
---

# 🔥 fire

> 🧭 **fire** · [Features](./docs/FEATURES.md) · [Roadmap](./docs/ROADMAP.md) · [Tasks](./docs/TASKS.md) · [Changelog](./docs/CHANGELOG.md) · [Metrics](./docs/METRICS.md) <!-- nav -->

[![CI](https://github.com/nitsuah/fire/actions/workflows/ci.yml/badge.svg)](https://github.com/nitsuah/fire/actions/workflows/ci.yml)
[![Netlify Status](https://api.netlify.com/api/v1/badges/2daa3b19-e0a6-46e5-95b3-189b61df5d5f/deploy-status)](https://app.netlify.com/projects/lifefire/deploys)

> A self-hosted Financial Independence, Retire Early (FIRE) tracker and API server. Runs locally via Docker. All financial data is stored in `data/db.json` on your machine with optional AES-256-GCM encryption (`SYNC_MASTER_KEY`). Read-only with respect to external financial accounts (no transactions initiated); local CRUD is fully supported. Being productionized toward real-time API-driven sync (eBay, Web3 wallets, Fidelity/Plaid) in PROD Phases 1–4. See [docs/prod-plan.md](docs/prod-plan.md).

---

## Why fire?

**fire is a local-first FIRE tracker for people who want one place to see the whole picture without handing their financial database to a hosted dashboard.**

- **Your data, your machine** — the primary datastore is local `db.json`, with optional AES-256-GCM encryption at rest.
- **Read-only integrations** — eBay, Plaid, blockchain providers, market-data providers, and vehicle lookup are used for tracking/sync; fire does not initiate financial transactions. **Drive backup** writes encrypted backups to Google Drive.
- **Everything counts** — investments, cash, CDs, real estate, vehicles, precious metals, crypto wallets, income, expenses, and side-hustle sales live in one net-worth model.
- **Ask your LLM** — the built-in MCP server exposes read-only financial tools for Claude/other MCP clients without giving the model trading or write access to external accounts.
- **Built for investigation, not just a number** — projections, scenario stress tests, diversification signals, tax-loss alerts, rebalancing what-ifs, CD maturities, emergency runway, and side-gig tax tagging turn raw balances into context.

**Try it:** [live browser demo](https://lifefire.netlify.app/) · **Run it locally:** `docker compose up -d` · **Use with Claude:** see [MCP Server](#mcp-server-claude-integration) and the [fire-coach skill](skills/README.md)

---

## Live links

- **Project site:** https://nitsuah.github.io/fire/
- **Browser demo:** https://lifefire.netlify.app/

## Features

- **Net Worth Dashboard** — real-time tracking of accounts, CDs, real estate, vehicles, precious metals, and investments; on wide screens Retirement Growth Path, an interactive drill-down Asset Allocation chart, and Cash & Fixed Income share the top row (the growth chart has a full-width expander)
- **Responsive shell** — hamburger nav drawer on phones, a single minimalist FIRE/net-worth summary bar (breakdown, income and spend on hover/tap) at narrow widths, and a pinned alerts bell
- **Retirement Projections** — SWR curves (3 – 4%), bull/bear scenarios, cash-first portfolio drawdown after retirement age, growth presets (Conservative / Standard / Aggressive / Early Retiree) and milestone presets in one panel
- **🌪️ Chaos mode** — one toggle (next to Bear/Bull, and on the Dashboard chart) rolls realistic life events onto your projection: gallbladder surgery, a cat's cancer, a child, an inherited house, a refinance, a job loss, an unexpected windfall… 37 events in 8 categories with life-average odds, age windows, predefined outcomes and follow-ups (a parent's care → funeral → inheritance). Costs that outrun inflation (rent, child and elder care, medical bills) escalate; 🛡️ mitigations like pet insurance shrink the hits they cover and charge their premiums. ▲/▼ markers with hover/tap details, a dashed "without chaos" line and 🎲 reroll. See [Chaos mode](#chaos-mode)
- **Customizable layout** — every tab is made of sections with a chosen column layout (1–4 columns, wide-left/right/center); a card alone in a section spans the full width. **✎ Customize** gives a drag-and-drop builder canvas with highlighted drop targets, click a title to collapse, and on the Dashboard **＋ Add widget** pins any card from another tab. Saved across sessions. See [Customizable layout](#customizable-layout)
- **Insights** — portfolio insight tiles (diversification, emergency fund, savings rate, CD maturities, SWR, crypto share), tax-loss harvesting alerts, and a portfolio rebalancing tool
- **Investment P&L Table** — sortable, color-coded, allocation filter with pie chart, risk concentration badges
- **CD Ladder Visualizer** — timeline of upcoming maturities with yield overlays
- **Side Hustle Tracker** — income logs, built-in eBay/Etsy/Facebook fee calculators, an eBay sales-report CSV upload (deduplicated against earlier imports), and rotating, dismissible side-hustle ideas with guide/video links
- **CSV Imports** — one unified add form (Import CSV is the default option) for Fidelity positions, Chase and Capital One statements, and eBay sales reports, plus Expenses-tab spending upload with auto-categorization (all processed locally)
- **Precious metals** — Gold/Silver account type valued by weight × live spot (metals.dev with a free Yahoo futures fallback)
- **Crypto accounts** — enter an ENS name, 0x address or ticker in either Name or Identifier. ⟳ Refresh on an ENS/0x account totals native coins plus priced tokens across Ethereum, Base, Optimism, Arbitrum, Polygon, BNB Chain and Avalanche, with no API keys, and shows the per-chain breakdown under the row. A ticker account is valued as quantity × live price. Wallet tracking appears under the form when Type = Cryptocurrency
- **REST API** — full CRUD for accounts, CDs, wallets, vehicles, sync templates, state; `FIRE_API_KEY` header auth required by default (opt out with `FIRE_AUTH_DISABLED=true` for local-only use); `FIRE_ADMIN_KEY`-gated key-rotation endpoint
- **MCP Server** — 16 read-only tools for Claude/LLM integration via `app/mcp-server.mjs`
- **Yahoo Finance prices** — live portfolio valuation with crumb-based auth, stale-data fallback, and SSE (`GET /api/prices/stream`) for live push; configurable via `ALPHA_VANTAGE_API_KEY` or `POLYGON_API_KEY` as stable alternatives
- **Webhook sync framework** — JSON data-mapped templates for automated data ingestion (full CRUD + live receiver at `POST /api/sync/webhook/:templateId`)
- **eBay Order Sync** — OAuth 2.0 flow (`GET /api/sync/ebay/authorize` → callback → `POST /api/sync/ebay/sync`) auto-imports completed sales into the side gig ledger; includes the **Marketplace Account Deletion** endpoint eBay requires (`/api/sync/ebay/marketplace-account-deletion`, see [docs/integrations.md](docs/integrations.md))
- **Plaid integration** — link-token flow, position/account sync, and transaction sync with auto-categorization into Expenses (`POST /api/sync/plaid/*`); manual CSV import is disabled while Plaid sync is active. Connector controls live in Settings
- **CoinTracker wallets (optional)** — connect CoinTracker (OAuth, read-only MCP) to import all wallets and exchange accounts with current balances. It becomes the source of truth for matching manual crypto entries. See [docs/integrations.md](docs/integrations.md#cointracker-wallet-discovery--balances)
- **Web3 wallet tracking** — full wallet CRUD (`/api/wallets`) with on-chain balance refresh; supports ETH/EVM, BTC, SOL, BNB, Polygon, Arbitrum, Base, Avalanche
- **Google Drive encrypted backup** — `POST /api/backup/drive`, `GET /api/backup/drive/list`, `POST /api/backup/drive/restore` (requires `GDRIVE_CLIENT_ID` + `GDRIVE_CLIENT_SECRET` for Google OAuth, and a 64-hex `SYNC_MASTER_KEY`)
- **Vehicle VIN decode & value refresh** — NHTSA VIN decode (`GET /api/vehicles/vin/:vin`) and value refresh (`POST /api/vehicles/:id/refresh-value`)
- **Rate limiting** — 300 req/min general, 30 req/min on sync routes (via `express-rate-limit`)
- **Security headers** — CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy applied on every response; CDN scripts pinned with SRI
- **HTTPS on localhost** — bundled Caddy reverse proxy (`https://localhost`); the app port binds to loopback only
- **JSON API errors** — unmatched `/api/*` routes return JSON 404s, and the browser's `fetchJson` helper reports non-JSON responses clearly instead of throwing parse errors

---

## Quick Start

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
# Clone and configure
git clone https://github.com/nitsuah/fire.git
cd fire
cp .env.example .env
```

API auth is **required by default** — edit `.env` and either set `FIRE_API_KEY`
(recommended; generate one with the command in [Environment Variables](#environment-variables))
or set `FIRE_AUTH_DISABLED=true` to run without auth for local-only use. The
server refuses to start with neither set.

```bash
# Start
docker compose up -d
```

The root `compose.yaml` names the project `fire` and includes
`config/docker-compose.yml`, so this runs from the repo root. `docker compose up fire`
starts just the app, and the longer `docker compose -f config/docker-compose.yml …`
form still works.

Open **http://localhost:3001** (plain HTTP) or **https://localhost** (via the
bundled Caddy reverse proxy — see [HTTPS via Caddy](#https-via-caddy) below)
in your browser.

```bash
# Stop
docker compose down

# Rebuild after dependency changes
docker compose build
docker compose up -d --force-recreate
```

---

## Environment Variables

Copy `.env.example` to `.env` and set values as needed. Most are optional for
basic local use — the one exception is `FIRE_API_KEY` (or its explicit
`FIRE_AUTH_DISABLED` opt-out), which the server requires just to start.

| Variable | Purpose |
|---|---|
| `PORT` | Server port (default `3001`) |
| `FIRE_API_KEY` | **Required by default.** All `/api/*` routes require `X-Api-Key: <value>`. The server refuses to start unless this or `FIRE_AUTH_DISABLED` is set |
| `FIRE_AUTH_DISABLED` | Set to `true` to run with no API auth at all (local-only use). Leave unset if anyone else could reach the server — see security-hardening.md |
| `FIRE_ADMIN_KEY` | **Required in production.** Gates `POST /api/admin/rotate-key` via `X-Admin-Key` header |
| `SYNC_MASTER_KEY` | 64-hex-char key to encrypt `db.json` at rest with AES-256-GCM |
| `SESSION_SECRET` | Secret for signing session cookies (random string; server exits in production if unset) |
| `EBAY_CLIENT_ID` / `EBAY_CLIENT_SECRET` | eBay Developer app credentials for Order API sync |
| `EBAY_ENVIRONMENT` | `sandbox` (default) or `production` |
| `EBAY_REDIRECT_URI` | OAuth `redirect_uri` sent to eBay. For a real eBay app this is your RuName. The default is derived from the incoming request (host + protocol, honouring the reverse proxy). **Required on Netlify** |
| `EBAY_VERIFICATION_TOKEN` | 32–80 char token you also register in the eBay Developer Portal for Marketplace Account Deletion notifications |
| `EBAY_NOTIFICATION_ENDPOINT_URL` | Public HTTPS URL of `/api/sync/ebay/marketplace-account-deletion` exactly as registered with eBay (used in the challenge hash). On Netlify: `https://lifefire.netlify.app/api/sync/ebay/marketplace-account-deletion`. The eBay variables also apply to the Netlify Functions deploy; see [docs/integrations.md](docs/integrations.md#browser-only-deploy-netlify-functions) |
| `METALS_API_KEY` | Optional metals.dev key for gold/silver spot; without it the free Yahoo futures fallback (`GC=F` / `SI=F`) is used |
| `ETHERSCAN_API_KEY` | Ethereum / ERC-20 balance fetching |
| `BSCSCAN_API_KEY` / `POLYGONSCAN_API_KEY` / `ARBISCAN_API_KEY` / `BASESCAN_API_KEY` | EVM chain balance fetching |
| `COINGECKO_API_KEY` | Optional; raises CoinGecko rate limit for crypto price lookups |
| `GDRIVE_CLIENT_ID` / `GDRIVE_CLIENT_SECRET` | Google OAuth 2.0 Web application credentials for Drive backup |
| `GDRIVE_REDIRECT_URI` | Optional OAuth callback override; defaults to `/api/backup/drive/callback` on the local server |
| `GDRIVE_BACKUP_FOLDER_ID` | Optional Drive folder ID; otherwise `fire-tracker-backups` is created/located automatically |
| `VEHICLE_VALUE_API_KEY` / `VEHICLE_VALUE_PROVIDER` | Paid vehicle value provider (dataone, marketcheck) |
| `PLAID_CLIENT_ID` / `PLAID_SECRET` | Plaid credentials for brokerage/bank sync |
| `PLAID_ENV` | `sandbox` (default) or `production` |
| `ALPHA_VANTAGE_API_KEY` / `POLYGON_API_KEY` | Stable stock-quote API alternative to Yahoo Finance |

Generate keys:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

---

## HTTPS via Caddy

`docker compose up -d` also starts a
[Caddy](https://caddyserver.com/) reverse proxy (`config/Caddyfile`) that
terminates TLS for `https://localhost`. Plain HTTP on `http://localhost:3001`
still works for same-machine use (OAuth redirect callbacks are configured
against it — see below), but the `fire` container's port is bound to
`127.0.0.1` only, not every network interface, so another machine on the LAN
can't reach it in cleartext — only this machine can, over either `:3001`
directly or `https://localhost` via Caddy.

The certificate comes from Caddy's local CA (`tls internal`), so browsers
warn until you trust it once. `caddy trust` only updates the trust store
*inside the caddy container* — it does not touch your host or browser.
Instead, copy the CA cert out and import it yourself:
```bash
docker compose cp caddy:/data/caddy/pki/authorities/local/root.crt ./caddy-local-ca.crt
```
then import `caddy-local-ca.crt` via your OS/browser's certificate manager
(see [Caddy's docs](https://caddyserver.com/docs/running) for OS-specific
steps).

For LAN IP access, add the IP as another site block in `config/Caddyfile`
(self-signed — pin the cert in your browser). For a public domain with a
real Let's Encrypt cert, replace `localhost` in the Caddyfile with the
domain and drop the `tls internal` line.

---

## MCP Server (Claude Integration)

Connect Claude Code to your live financial data. The project ships a `.mcp.json` that Claude Code picks up automatically on startup — edit the `cwd` to match your local path:

```json
{
  "mcpServers": {
    "fire-tracker": {
      "command": "node",
      "args": ["app/mcp-server.mjs"],
      "cwd": "/your/path/to/fire"
    }
  }
}
```

**Tools (16, all read-only):** `fire_status_summary`, `get_net_worth`, `get_net_worth_trend`, `get_accounts`, `get_portfolio`, `get_cds`, `get_expenses`, `get_projection_settings`, `get_side_gig_income`, `get_side_gig_tax_summary`, `get_wallets`, `get_concentration_risk`, `get_diversification_score`, `get_swr_sensitivity`, `simulate_rebalance`, `get_emergency_runway`

`simulate_rebalance` is a what-if: it reports allocation and diversification score before/after moving money between asset classes, and never trades or saves anything.

**Claude skill:** [`skills/fire-coach`](skills/README.md) makes Claude a FIRE coach for this app. It maps questions to the right MCP tools, applies a FIRE playbook (the 4% rule, savings rate, order of operations, taxes, sequence risk, what to do when income stops) and points to the exact tab and button. Install it with `mkdir -p ~/.claude/skills && cp -r skills/fire-coach ~/.claude/skills/`.

**Money-maker skills:** [`skills/reseller-autopilot`](skills/README.md#reseller-autopilot) prices items and drafts listings, with net-after-fees on eBay, Etsy, Mercari, Poshmark and FB Marketplace and runs a weekly low-touch selling routine. [`skills/passive-income-lab`](skills/README.md#passive-income-lab) sizes low-touch income streams against your runway and shows how far each moves your FIRE date.

Smoke-test locally:
```bash
docker compose exec fire node scripts/test-mcp.mjs
```

---

## Chaos mode

![Retirement growth path with Chaos mode on](https://github.com/nitsuah/fire/blob/main/site/assets/proj-chaos.webp)

Every projection is a smooth line; life isn't. **🌪️ Chaos** applies a seeded timeline of 37 kinds of life events to the base path. The plain path stays on the chart as a dashed "Without chaos" line.

| Category | Examples | Typical impact |
| --- | --- | --- |
| Health | gallbladder surgery, ER visit, dental emergency, serious illness, knee/hip replacement | $1.2k – $14k one-time, rising ~2%/yr above inflation the later it happens; serious illness can add months of lost income |
| Pets | cat cancer, dog emergency surgery | $1.5k – $10k one-time (vet bills rise ~2%/yr above inflation) |
| Family | wedding, child birth, daycare ending, divorce, aging parent care, unpaid family loan, funeral, inheritance, **inherited house**, family gift | child −$8k to −$16k/yr for 18 years; divorce −20–35% of net worth; inheritance +$15k – $200k; inherited house: sell (+$220k), move in (+$15k/yr) or rent it out (+$11k/yr) |
| Career | job loss, new job/promotion, bonus, side hustle takes off, pay cut, RSUs | 2–10 months of income lost; a promotion is a signing bump or extra savings for 5–6 years (wages are flat in real terms) |
| Housing | roof/HVAC, water damage, rent hike / forced move, **refinance**, **roommate / house hack** | $2.5k – $35k one-time; rent +$3k – $6k/yr; refinance +$2.4k – $4.8k/yr for 15 years; roommate +$7k – $12k/yr |
| Auto | accident, major repair, replacement car, **car loan paid off** | $1k – $30k; a paid-off loan frees $4k – $5k/yr for a few years |
| Windfall | surprise tax refund, sold a collection, lottery/crypto, **settlement or claim payout** | +$400 – $40k |
| Legal & money | identity theft, surprise tax bill, lawsuit | $500 – $30k |

- **Sequences:** some events trigger follow-ups. Aging-parent care can lead to a funeral, and a funeral to an inheritance or an inherited house. A wedding can lead to a child; a child leads to daycare ending a few years later; a job loss is usually followed by a new job. Follow-ups show "after …" in the tooltip and the event list.
- Each event has a **life-average yearly probability** and an **age window**: weddings and kids skew young, joint replacements older, and career events stop at retirement. Randomness only picks which event happens, when, and which of its predefined outcomes applies.
- Density follows the window: at least 1 event in the first year and 3 in every 5 years, about 0.75 a year over a lifetime, with at most 2 in any one year.
- **How it moves net worth** (all in today's dollars, like the chart):
  - One-time costs and gains hit in the year they happen, then compound with the rest of the portfolio.
  - Recurring ones change yearly savings before retirement, or yearly withdrawals after it, for their duration.
  - Costs that rise with inflation are already flat in today's dollars. Those that have historically outrun it climb on top of that: rent +1%/yr, child costs +1%, elder care +3%, insurance after a claim +2%. Descriptions quote your inflation setting, e.g. "rising ~3.5%/yr: inflation + 1%".
  - A job loss costs the lost months of savings plus real spending. Paycheck events (job loss, pay cut, bonus, RSUs) are skipped if Expenses → gross income is under $5k.
  - Milestone Predictions switch to the chaos path and are marked 🌪️.
- **🛡️ Mitigations** (Insights → Portfolio Insights): pet insurance, a low out-of-pocket plan or HSA, disability insurance, dental, an umbrella policy, water-backup coverage, gap insurance, a credit freeze, safe-harbor withholding and a 6-month emergency fund.
  - Tick what you have. Chaos then shrinks the hits each one covers (pet insurance cuts vet bills ~80%) and charges its yearly premium.
  - Each card shows what it saves and costs in your current simulated life. Insurance usually costs more than it pays out on average; its job is capping the big hits.
- Hover or tap the line for the events nearest that age, what led to them and their dollar impact. The chips under the chart list every event in the 1Y/5Y/10Y/15Y/All window (the Dashboard folds them under "details").
- The timeline is seeded, so it doesn't change on reload or when you switch windows; **🎲** rerolls. The toggle, seed and mitigations are saved in the browser. Engine and tests: [`app/lib/chaos-events.js`](app/lib/chaos-events.js), [`tests/unit/chaos-events.test.mjs`](tests/unit/chaos-events.test.mjs).

## Customizable layout

Every tab is a set of **sections**. Each section picks a column layout: full width, 2 equal, 2 wide-left, 2 wide-right, 3 equal, 3 wide-center or 4. Each column stacks cards. A card alone in its section spans the full width, so there are no fixed per-tab widths. On narrower screens sections drop to two columns, and on phones to one.

- Click any card title to collapse it.
- **✎ Customize** turns the tab into a builder canvas: a dotted grid with outlined sections and a layout picker for each one. Drag a card's ⠿ handle (mouse or finger) and the target cell lights up, with a pulsing placeholder where it will land. Drop it on a "＋ New section" gap to give it its own row. ↑/↓ moves a card without dragging; sections have ↑/↓ and 🗑.
- On the Dashboard, **＋ Add widget** pins any card from another tab, leaving a "Move back here" link on its home tab. **✕** removes cards you don't use. **↺ Reset** restores a tab.
- Everything is saved in the browser and survives reloads.

---

## Data & Privacy

- All financial data is stored in `data/db.json` inside the project directory (Docker volume-mounted).
- External network calls occur only when you explicitly enable integrations: eBay OAuth (order sync), Plaid (brokerage/bank positions), blockchain lookups (crypto account refresh: ENS via ensdata.net, balances via Blockscout and publicnode.com RPCs — these two need no API key; the wallet tracker: Etherscan, BscScan, Blockstream, etc., which do), CoinTracker (read-only wallet balances), Google Drive backup, vehicle VIN lookup (NHTSA), and price providers (Yahoo Finance needs none; Alpha Vantage / Polygon need keys). Each integration is opt-in independently of the others; beyond being enabled, an integration needs user-provided credentials only where its provider issues them.
- Optionally encrypt `db.json` at rest with `SYNC_MASTER_KEY` (AES-256-GCM).
- Export/restore a full JSON backup any time from the dashboard.

---

## Architecture

```
fire/
├── app/
│   ├── index.html              # Single-page app entry point
│   ├── server.js               # Express server (port 3001)
│   ├── mcp-server.mjs          # MCP server — 16 read-only tools
│   ├── lib/
│   │   ├── db.js               # State persistence (db.json, atomic writes)
│   │   ├── crypto-utils.js     # AES-256-GCM encrypt/decrypt
│   │   ├── finance-calcs.js    # Server-side projection engine (MCP + API)
│   │   ├── finance-core.js     # Core FIRE math primitives
│   │   ├── finance-parsing.js  # CSV parsing helpers
│   │   ├── projections.js      # Blended return, passive income offset, depletion age
│   │   ├── html-utils.js       # XSS escape utility (shared by table renderers)
│   │   ├── yahoo-prices.js     # Yahoo Finance price fetcher (crumb-based)
│   │   ├── prices-provider.js  # Price provider abstraction (Yahoo / Alpha Vantage / Polygon)
│   │   ├── webhook-integration.js # Webhook payload handler
│   │   ├── ebay-connector.js   # eBay Order API OAuth + order fetch
│   │   ├── cointracker-connector.js # CoinTracker OAuth (PKCE + DCR) + read-only MCP client
│   │   ├── cointracker-handlers.js  # CoinTracker routes, shared by Express + Netlify
│   │   ├── cointracker-merge.js     # Folds CoinTracker wallets into accounts (dedupe, browser + Node)
│   │   ├── crypto-balance.js   # Crypto account value: ticker × price, or ENS/0x multichain total
│   │   ├── multichain-balance.js # Keyless multichain total (Blockscout + publicnode RPCs)
│   │   ├── web3-prices.js      # Wallet-tracker balance fetch (ETH, BTC, SOL, EVM chains; BYOK keys)
│   │   ├── gdrive-backup.js    # Google Drive encrypted backup/restore
│   │   ├── vehicle-api.js      # NHTSA VIN decode + vehicle value estimate
│   │   ├── csv-import.js       # Fidelity / Chase / CapOne CSV parsing (also routes eBay reports)
│   │   ├── ebay-report.js      # eBay listings sales report parser + dedupe merge (browser + Node)
│   │   ├── metals-prices.js    # Gold/silver spot (metals.dev + Yahoo futures fallback)
│   │   ├── fetch-utils.js      # fetchJson helper (safe JSON parsing for browser managers)
│   │   ├── expenses.js         # Expense calculation helpers
│   │   ├── side-gig.js         # Side hustle fee-calc logic
│   │   ├── privacy.js          # Privacy consent helpers
│   │   ├── server-utils.js     # findAvailablePort, strictNum
│   │   ├── charts/             # Chart.js renderers (allocation drill-down, projections, CD ladder)
│   │   ├── tables/             # Table renderers (dashboard banner, positions, ledger, insights tiles, …)
│   │   ├── managers/           # UI managers (accounts, navigation, wallets, hustle accelerators, spending upload, …)
│   │   └── css/                # base / layout / components / widgets stylesheets
│   └── routes/
│       ├── state.js            # GET / POST /api/state
│       ├── accounts.js         # CRUD /api/accounts
│       ├── cds.js              # CRUD /api/cds
│       ├── prices.js           # GET /api/prices, GET /api/prices/stream (SSE)
│       ├── wallets.js          # CRUD /api/wallets + /api/wallets/:id/refresh + /api/wallets/refresh-all
│       ├── vehicles.js         # GET /api/vehicles/vin/:vin, POST /api/vehicles/:id/refresh-value
│       ├── (accounts.js also)  # POST /api/accounts/:id/refresh-crypto, /refresh-metal
│       ├── backup.js           # POST /api/backup/drive, GET /api/backup/drive/list, POST /api/backup/drive/restore
│       ├── sync.js             # Webhook templates CRUD, POST /api/sync/webhook/:templateId; mounts the three below
│       ├── ebay.js             # /api/sync/ebay/* (OAuth, sync, marketplace deletion)
│       ├── plaid.js            # /api/sync/plaid/*
│       └── cointracker.js      # /api/sync/cointracker/* (authorize, callback, sync, inspect, disconnect)
├── netlify/
│   ├── functions/              # Hosted (lifefire.netlify.app) API: fire-api (metals, ENS lookup, crypto refresh),
│   │                           #   ebay-*, plaid, cointracker — same handlers as the Express routes
│   └── lib/http.mjs            # Shared Function helpers
├── config/
│   ├── docker-compose.yml      # fire + Caddy (HTTPS)
│   ├── Dockerfile              # node:22-alpine
│   ├── Dockerfile.playwright   # pinned Playwright image for UI tests
│   ├── playwright.config.js    # real-browser UI regression suite (tests/e2e-ui)
│   └── eslint.config.mjs
├── scripts/
│   └── test-mcp.mjs            # MCP smoke test (all 16 read-only tools)
├── data/                       # db.json lives here (git-ignored)
├── docs/                       # Architecture notes
├── .env.example                # Environment variable reference
├── .mcp.json                   # MCP server config for Claude Code
└── package.json                # fire-tracker v1.1.0
```

---

## Development

```bash
# Run tests inside Docker
docker compose exec fire npm test

# Run tests with coverage
docker compose exec fire npm run test:coverage

# Lint
docker compose exec fire npm run lint

# Real-browser UI tests (Playwright, in Docker)
docker build -f config/Dockerfile.playwright -t fire-playwright-e2e .
docker run --rm fire-playwright-e2e
```

---

## Planned Integrations

The system is being productionized toward real-time, API-driven data in four phases. All planned connections are opt-in, need user-provided credentials only where the provider issues them, and are read-only with respect to external accounts.

| Integration | Phase | Status |
|---|---|---|
| eBay Order API (auto-import sales) | Phase 1 | Live (user-provided credentials) |
| Web3 wallet tracking (ETH, BTC, SOL, + EVM chains) | Phase 1 | Live (user-provided keys per chain) |
| Crypto account multichain value (ENS/0x, 7 EVM chains, tokens) | Phase 1 | Live (keyless: Blockscout + public RPCs) |
| CoinTracker wallets (read-only MCP) | Phase 1 | Implemented; blocked until CoinTracker enables MCP early access for the account |
| Google Drive encrypted backup | Phase 1 | Implemented self-hosted via Google OAuth; live round-trip verification pending |
| Vehicle value API (NHTSA VIN free; paid providers via `VEHICLE_VALUE_PROVIDER`) | Phase 1 | Live |
| Fidelity / Plaid positions + balance sync | Phase 2 | Live (user-provided credentials; sandbox ready) |
| Plaid on Netlify (hosted) | Phase 2 | **Hosted only** — endpoints route to `netlify/functions/plaid.mjs` at `/api/sync/plaid/*` (see [docs/integrations.md](docs/integrations.md#browser-only-deploy-netlify-function)); unit- and route-tested, live Link → sync run against the hosted deploy still pending |
| Stable stock quote API (Alpha Vantage / Polygon.io) | Phase 2 | Live (fallback: Yahoo Finance) |
| Rate limiting (300/min general, 30/min sync) | Phase 3 | Live |
| Security headers (CSP, X-Frame-Options, Referrer-Policy) | Phase 3 | Live |
| HTTPS via Caddy reverse proxy | Phase 3 | Live |
| Plaid transaction sync → Expenses | Phase 2 | Live (user-provided credentials; verified against mocked API) |
| eBay Marketplace Account Deletion endpoint | Phase 1 | Live — needs a public HTTPS URL registered in the eBay Developer Portal |
| Precious-metals spot pricing | Phase 2 | Live (free fallback; optional metals.dev key) |

See [docs/prod-plan.md](docs/prod-plan.md) for the full productionization roadmap and [docs/integrations.md](docs/integrations.md) for per-integration setup instructions.

---

## Roadmap & Tasks

- Productionization plan → [docs/prod-plan.md](docs/prod-plan.md)
- Integration setup → [docs/integrations.md](docs/integrations.md)
- Security hardening → [docs/security-hardening.md](docs/security-hardening.md)
- Sync architecture → [docs/backend-sync-architecture.md](docs/backend-sync-architecture.md)
- Milestones → [ROADMAP.md](./docs/ROADMAP.md)
- Task backlog → [TASKS.md](./docs/TASKS.md)
- Shipped features → [FEATURES.md](./docs/FEATURES.md)

<!-- docs-index:start -->

## Docs Index

Every committed Markdown doc in this repo (other than this README, `.github/` and `templates/`), the same set mirrored into the Obsidian vault, so none of them is orphaned.

**`docs/`**

- [Changelog](./docs/CHANGELOG.md) — `docs/CHANGELOG.md`
- [Features](./docs/FEATURES.md) — `docs/FEATURES.md`
- [METRICS.md](./docs/METRICS.md) — `docs/METRICS.md`
- [🗺️ fire Roadmap](./docs/ROADMAP.md) — `docs/ROADMAP.md`
- [Tasks](./docs/TASKS.md) — `docs/TASKS.md`
- [Backend Sync Architecture](./docs/backend-sync-architecture.md) — `docs/backend-sync-architecture.md`
- [Integrations Reference](./docs/integrations.md) — `docs/integrations.md`
- [fire — Privacy Policy & Terms of Use](./docs/privacy-policy.md) — `docs/privacy-policy.md`
- [PROD Plan — fire Productionization](./docs/prod-plan.md) — `docs/prod-plan.md`
- [Security Hardening Plan](./docs/security-hardening.md) — `docs/security-hardening.md`
- [Weekly financial check-in prompt (local)](./docs/weekly-checkin-prompt.md) — `docs/weekly-checkin-prompt.md`

**`docs/archive/`**

- [fire-feedback](./docs/archive/fire-feedback.md) — `docs/archive/fire-feedback.md`
- [fire-plan](./docs/archive/fire-plan.md) — `docs/archive/fire-plan.md`

**`promo/`**

- [Promo spots](./promo/README.md) — `promo/README.md`

**`promo/brag-22s/`**

- [brag-22s — storyboard](./promo/brag-22s/storyboard.md) — `promo/brag-22s/storyboard.md`

**`promo/`**

- [Promo feature ledger](./promo/features.md) — `promo/features.md`

**`skills/`**

- [fire-coach Skill README](./skills/README.md) — `skills/README.md`
- [fire-coach Skill Definition](./skills/fire-coach/SKILL.md) — `skills/fire-coach/SKILL.md`
- [fire-coach App Guide](./skills/fire-coach/references/app-guide.md) — `skills/fire-coach/references/app-guide.md`
- [fire-coach Financial Playbook](./skills/fire-coach/references/financial-playbook.md) — `skills/fire-coach/references/financial-playbook.md`
- [reseller-autopilot Skill Definition](./skills/reseller-autopilot/SKILL.md) — `skills/reseller-autopilot/SKILL.md`
- [reseller-autopilot Platform Fees](./skills/reseller-autopilot/references/platform-fees.md) — `skills/reseller-autopilot/references/platform-fees.md`
- [reseller-autopilot Listing Playbook](./skills/reseller-autopilot/references/listing-playbook.md) — `skills/reseller-autopilot/references/listing-playbook.md`
- [passive-income-lab Skill Definition](./skills/passive-income-lab/SKILL.md) — `skills/passive-income-lab/SKILL.md`
- [passive-income-lab Streams](./skills/passive-income-lab/references/streams.md) — `skills/passive-income-lab/references/streams.md`
- [passive-income-lab FIRE Math](./skills/passive-income-lab/references/fire-math.md) — `skills/passive-income-lab/references/fire-math.md`

<!-- docs-index:end -->
