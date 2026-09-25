# 🔥 FIRE Tracker

> 🧭 **fire** · [Features](./docs/FEATURES.md) · [Roadmap](./docs/ROADMAP.md) · [Tasks](./docs/TASKS.md) · [Changelog](./docs/CHANGELOG.md) · [Metrics](./docs/METRICS.md) <!-- nav -->

[![CI](https://github.com/nitsuah/fire/actions/workflows/ci.yml/badge.svg)](https://github.com/nitsuah/fire/actions/workflows/ci.yml)
[![Netlify Status](https://api.netlify.com/api/v1/badges/2daa3b19-e0a6-46e5-95b3-189b61df5d5f/deploy-status)](https://app.netlify.com/projects/lifefire/deploys)

> A self-hosted Financial Independence, Retire Early (FIRE) tracker and API server. Runs locally via Docker. All financial data is stored in `data/db.json` on your machine with optional AES-256-GCM encryption (`SYNC_MASTER_KEY`). Read-only with respect to external financial accounts (no transactions initiated); local CRUD is fully supported. Being productionized toward real-time API-driven sync (eBay, Web3 wallets, Fidelity/Plaid) in PROD Phases 1–4. See [docs/prod-plan.md](docs/prod-plan.md).

---

## Features

- **Net Worth Dashboard** — real-time tracking of accounts, CDs, real estate, vehicles, precious metals, and investments; on wide screens Retirement Growth Path, an interactive drill-down Asset Allocation chart, and Cash & Fixed Income share the top row (the growth chart has a full-width expander)
- **Responsive shell** — hamburger nav drawer on phones, a single minimalist FIRE/net-worth summary bar (breakdown, income and spend on hover/tap) at narrow widths, and a pinned alerts bell
- **Retirement Projections** — SWR curves (3 – 4%), bull/bear scenarios, cash-first portfolio drawdown after retirement age, growth presets (Conservative / Standard / Aggressive / Early Retiree) and milestone presets in one panel
- **Insights** — portfolio insight tiles (diversification, emergency fund, savings rate, CD maturities, SWR, crypto share), tax-loss harvesting alerts, and a portfolio rebalancing tool
- **Investment P&L Table** — sortable, color-coded, allocation filter with pie chart, risk concentration badges
- **CD Ladder Visualizer** — timeline of upcoming maturities with yield overlays
- **Side Hustle Tracker** — income logs, built-in eBay/Etsy/Facebook fee calculators, an eBay sales-report CSV upload (deduplicated against earlier imports), and rotating, dismissible side-hustle ideas with guide/video links
- **CSV Imports** — one unified add form (Import CSV is the default option) for Fidelity positions, Chase and Capital One statements, and eBay sales reports, plus Expenses-tab spending upload with auto-categorization (all processed locally)
- **Precious metals** — Gold/Silver account type valued by weight × live spot (metals.dev with a free Yahoo futures fallback)
- **Crypto accounts** — enter an ENS name, 0x address or ticker in either Name or Identifier; wallet tracking appears under the form when Type = Cryptocurrency
- **REST API** — full CRUD for accounts, CDs, wallets, vehicles, sync templates, state; `FIRE_API_KEY` header auth required by default (opt out with `FIRE_AUTH_DISABLED=true` for local-only use); `FIRE_ADMIN_KEY`-gated key-rotation endpoint
- **MCP Server** — 13 functional tools for Claude/LLM integration via `app/mcp-server.mjs` (plus 7 registered stubs)
- **Yahoo Finance prices** — live portfolio valuation with crumb-based auth, stale-data fallback, and SSE (`GET /api/prices/stream`) for live push; configurable via `ALPHA_VANTAGE_API_KEY` or `POLYGON_API_KEY` as stable alternatives
- **Webhook sync framework** — JSON data-mapped templates for automated data ingestion (full CRUD + live receiver at `POST /api/sync/webhook/:templateId`)
- **eBay Order Sync** — OAuth 2.0 flow (`GET /api/sync/ebay/authorize` → callback → `POST /api/sync/ebay/sync`) auto-imports completed sales into the side gig ledger; includes the **Marketplace Account Deletion** endpoint eBay requires (`/api/sync/ebay/marketplace-account-deletion`, see [docs/integrations.md](docs/integrations.md))
- **Plaid integration** — link-token flow, position/account sync, and transaction sync with auto-categorization into Expenses (`POST /api/sync/plaid/*`); manual CSV import is disabled while Plaid sync is active. Connector controls live in Settings
- **Web3 wallet tracking** — full wallet CRUD (`/api/wallets`) with on-chain balance refresh; supports ETH/EVM, BTC, SOL, BNB, Polygon, Arbitrum, Base, Avalanche
- **Google Drive encrypted backup** — `POST /api/backup/drive`, `GET /api/backup/drive/list`, `POST /api/backup/drive/restore` (requires `GDRIVE_SERVICE_ACCOUNT_JSON` + `SYNC_MASTER_KEY`)
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
docker compose -f config/docker-compose.yml up -d
```

Open **http://localhost:3001** (plain HTTP) or **https://localhost** (via the
bundled Caddy reverse proxy — see [HTTPS via Caddy](#https-via-caddy) below)
in your browser.

```bash
# Stop
docker compose -f config/docker-compose.yml down

# Rebuild after dependency changes
docker compose -f config/docker-compose.yml build
docker compose -f config/docker-compose.yml up -d --force-recreate
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
| `EBAY_REDIRECT_URI` | OAuth callback URI. Default is derived from the incoming request (host + protocol, honouring the reverse proxy); set explicitly for any real deployment |
| `EBAY_VERIFICATION_TOKEN` | 32–80 char token you also register in the eBay Developer Portal for Marketplace Account Deletion notifications |
| `EBAY_NOTIFICATION_ENDPOINT_URL` | Public HTTPS URL of `/api/sync/ebay/marketplace-account-deletion` exactly as registered with eBay (used in the challenge hash) |
| `METALS_API_KEY` | Optional metals.dev key for gold/silver spot; without it the free Yahoo futures fallback (`GC=F` / `SI=F`) is used |
| `ETHERSCAN_API_KEY` | Ethereum / ERC-20 balance fetching |
| `BSCSCAN_API_KEY` / `POLYGONSCAN_API_KEY` / `ARBISCAN_API_KEY` / `BASESCAN_API_KEY` | EVM chain balance fetching |
| `COINGECKO_API_KEY` | Optional; raises CoinGecko rate limit for crypto price lookups |
| `GDRIVE_SERVICE_ACCOUNT_JSON` | Path to GCP service account JSON for encrypted Drive backup |
| `GDRIVE_BACKUP_FOLDER_ID` | Optional Drive folder ID (auto-created if blank) |
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

`docker compose -f config/docker-compose.yml up -d` also starts a
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
docker compose -f config/docker-compose.yml cp caddy:/data/caddy/pki/authorities/local/root.crt ./caddy-local-ca.crt
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

**Functional tools (13):** `fire_status_summary`, `get_net_worth`, `get_accounts`, `get_portfolio`, `get_cds`, `get_expenses`, `get_projection_settings`, `get_side_gig_income`, `get_side_gig_tax_summary`, `get_wallets`, `get_concentration_risk`, `simulate_rebalance`, `get_emergency_runway`

**Registered stubs (return `not_implemented`):** `get_market_correlation`, `get_swr_sensitivity`, `set_price_target_alert`, `auto_reconcile_csv`, `get_dividend_forecast`, `get_net_worth_trend`, `get_diversification_score`

Smoke-test locally:
```bash
docker compose -f config/docker-compose.yml exec fire node scripts/test-mcp.mjs
```

---

## Data & Privacy

- All financial data is stored in `data/db.json` inside the project directory (Docker volume-mounted).
- External network calls occur only when you explicitly enable integrations: eBay OAuth (order sync), Plaid (brokerage/bank positions), blockchain APIs (wallet balances — Etherscan, BscScan, Blockstream, etc.), Google Drive backup, vehicle VIN lookup (NHTSA), and price providers (Yahoo Finance / Alpha Vantage / Polygon). All are opt-in and BYOK.
- Optionally encrypt `db.json` at rest with `SYNC_MASTER_KEY` (AES-256-GCM).
- Export/restore a full JSON backup any time from the dashboard.

---

## Architecture

```
fire/
├── app/
│   ├── index.html              # Single-page app entry point
│   ├── server.js               # Express server (port 3001)
│   ├── mcp-server.mjs          # MCP server — 13 functional tools + 7 registered stubs
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
│   │   ├── web3-prices.js      # On-chain balance fetch (ETH, BTC, SOL, EVM chains)
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
│       └── sync.js             # Webhook templates CRUD, POST /api/sync/webhook/:templateId, eBay OAuth, Plaid
├── config/
│   ├── docker-compose.yml      # fire + Caddy (HTTPS)
│   ├── Dockerfile              # node:22-alpine
│   ├── Dockerfile.playwright   # pinned Playwright image for UI tests
│   ├── playwright.config.js    # real-browser UI regression suite (tests/e2e-ui)
│   └── eslint.config.mjs
├── scripts/
│   └── test-mcp.mjs            # MCP smoke test (the 8 original tools in EXPECTED_TOOLS)
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
docker compose -f config/docker-compose.yml exec fire npm test

# Run tests with coverage
docker compose -f config/docker-compose.yml exec fire npm run test:coverage

# Lint
docker compose -f config/docker-compose.yml exec fire npm run lint

# Real-browser UI tests (Playwright, in Docker)
docker build -f config/Dockerfile.playwright -t fire-playwright-e2e .
docker run --rm fire-playwright-e2e
```

---

## Planned Integrations

The system is being productionized toward real-time, API-driven data in four phases. All planned connections are opt-in, BYOK, and read-only with respect to external accounts.

| Integration | Phase | Status |
|---|---|---|
| eBay Order API (auto-import sales) | Phase 1 | Live (BYOK) |
| Web3 wallet tracking (ETH, BTC, SOL, + EVM chains) | Phase 1 | Live (BYOK keys per chain) |
| Google Drive encrypted backup | Phase 1 | Live (requires `GDRIVE_SERVICE_ACCOUNT_JSON`) |
| Vehicle value API (NHTSA VIN free; paid providers via `VEHICLE_VALUE_PROVIDER`) | Phase 1 | Live |
| Fidelity / Plaid positions + balance sync | Phase 2 | Live (BYOK; sandbox ready) |
| Stable stock quote API (Alpha Vantage / Polygon.io) | Phase 2 | Live (fallback: Yahoo Finance) |
| Rate limiting (300/min general, 30/min sync) | Phase 3 | Live |
| Security headers (CSP, X-Frame-Options, Referrer-Policy) | Phase 3 | Live |
| HTTPS via Caddy reverse proxy | Phase 3 | Live |
| Plaid transaction sync → Expenses | Phase 2 | Live (BYOK; verified against mocked API) |
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

Every doc at the repo root and under `docs/` (the files mirrored into the Obsidian vault), so none of them is orphaned.

- [Changelog](./docs/CHANGELOG.md) — `docs/CHANGELOG.md`
- [Features](./docs/FEATURES.md) — `docs/FEATURES.md`
- [METRICS.md](./docs/METRICS.md) — `docs/METRICS.md`
- [🗺️ FIRE Tracker Roadmap](./docs/ROADMAP.md) — `docs/ROADMAP.md`
- [Tasks](./docs/TASKS.md) — `docs/TASKS.md`
- [Backend Sync Architecture](./docs/backend-sync-architecture.md) — `docs/backend-sync-architecture.md`
- [Integrations Reference](./docs/integrations.md) — `docs/integrations.md`
- [FIRE Tracker — Privacy Policy & Terms of Use](./docs/privacy-policy.md) — `docs/privacy-policy.md`
- [PROD Plan — FIRE Tracker Productionization](./docs/prod-plan.md) — `docs/prod-plan.md`
- [Security Hardening Plan](./docs/security-hardening.md) — `docs/security-hardening.md`

**`docs/archive/`**

- [fire-feedback](./docs/archive/fire-feedback.md) — `docs/archive/fire-feedback.md`
- [fire-plan](./docs/archive/fire-plan.md) — `docs/archive/fire-plan.md`

<!-- docs-index:end -->
