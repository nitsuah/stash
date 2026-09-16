# Features

`nitsuah/fire` is a lightweight FIRE (Financial Independence, Retire Early) tracker and API server built with Node/Express and vanilla JavaScript, designed for local self-hosted use with full LLM integration via MCP.

## Core Infrastructure

- **Express Server** — Node/Alpine container on port 3001 (configurable via `PORT`); serves the SPA and REST API from the same process.
- **db.json Persistence** — All state stored server-side in `data/db.json` with atomic writes (write-to-tmp then rename) and full export/restore via the dashboard.
- **Optional Encryption** — `SYNC_MASTER_KEY` enables AES-256-GCM encryption of `db.json` at rest; key validated lazily so the server starts without it.
- **API Key Middleware** — `FIRE_API_KEY` env var gates all `/api/*` routes behind an `X-Api-Key` header check.
- **Session Security** — `express-session` with `httpOnly` + `sameSite: lax` cookie flags; startup warns if `SESSION_SECRET` is unset.

## MCP Server

- **8 Read-Only Tools** — `fire_status_summary`, `get_net_worth`, `get_accounts`, `get_portfolio`, `get_cds`, `get_expenses`, `get_projection_settings`, `get_side_gig_income`; exposed over stdio via `@modelcontextprotocol/sdk`.
- **Claude Code Integration** — `.mcp.json` at repo root auto-connects the server when Claude Code starts in this directory.
- **Smoke Test** — `scripts/test-mcp.mjs` runs the full MCP handshake and calls all 8 tools with response validation.

## Net Worth Tracking

- **Custom Accounts** — Manual entry with value, APY, and account type; full CRUD via REST API.
- **Fidelity CSV Import** — Parses Fidelity brokerage position exports; aggregates symbols, quantities, and cash; deduplicates settled cash from P&L.
- **Chase / Capital One CSV Import** — Parses credit card statement debits and auto-categorizes spending into monthly cash flow.
- **Real Estate Tracker** — Manual entry with property name, value, equity, mortgage, and notes; collision-resistant IDs.
- **Vehicle Tracker** — Make/model/year, current value, loan balance, and depreciation estimate; fleet summary view; negative equity preserved in net worth calculation.

## Investments Dashboard

- **P&L Table** — Red/green color scale, sortable faceted columns with inline totals, pie-chart filter that greys non-selected slices.
- **Risk Concentration Badges** — ⚡ for positions ≥15% of portfolio, ⚠ for ≥20%; market return comparison badges per position.
- **Diversification Suggestion Block** — Allocation-aware tips surfaced inline with the investments view.
- **Collapse-All Toggle** — Collapses investment rows; cost basis included in facet totals.
- **Allocation Filter Reset** — Filter clears automatically when portfolio total is zero.

## Retirement Projections

- **Projection Engine** — Accumulation phase (adds savings) and decumulation phase (withdraws `annualExpenses`) split at retirement age; `realReturn = nominalReturn − inflation`. Correctly models portfolio drawdown after retirement with continuous compounding.
- **SWR Curves** — 3%, 3.5%, 4% withdrawal rate projections with retirement age predictions and milestone forecasts.
- **Bull/Bear Scenario Bands** — Clickable ±2% offset buttons update growth paths in real time; depletion age tracked for base/bull/bear scenarios.
- **Time-Period Filters** — 1M / 1Y / 5Y / 10Y / 15Y+ range buttons on dashboard charts.
- **Chart Line Toggles** — Toggle NW, 75%/100%/125% FIRE goals, Coast FIRE, and US Median benchmark independently.
- **CD Maturity Markers** — Overlaid on the retirement growth chart to show liquidity events.
- **Multi-Scenario FIRE Comparison** — Side-by-side comparison of FIRE dates across varying salary bumps, market downturns, and inflation spikes.
- **Money Run-Out Detection** — Tracks depletion age year-by-year for base, bull, and bear scenarios when portfolio reaches zero; portfolios that survive the full projection span are flagged accordingly.

## CD & Fixed Income

- **CD Tracker** — Full CRUD with principal, rate, start date, maturity date (strict `YYYY-MM-DD` validation with UTC round-trip); annual yield badge on dashboard.
- **CD Ladder Visualizer** — Timeline view of upcoming maturities with aggregate yield overlays.
- **Next Maturity** — MCP and dashboard surface the nearest upcoming maturity; `NaN` durations excluded from sort.

## Side Hustle Tracker

- **Income Logs** — Manual entries for Etsy, FB Marketplace, Craigslist, eBay, and custom platforms; category-tagged.
- **Fee Calculator** — Built-in eBay/platform fee and shipping margin calculator to compute net income per sale.
- **Webhook Deduplication** — Incoming side-gig ledger entries deduplicated by stable upstream ID or content fingerprint.

## Prices

- **Yahoo Finance Integration** — Live portfolio valuation via crumb-based auth with stale-data fallback; `AbortSignal.timeout(10 s)` on all fetch calls.
- **Crumb Validation** — Rejects empty, HTML, or oversized responses before caching.
- **Price Cache** — Per-symbol freshness tracking; stale entries refetched on next request.

## Webhook / Sync Framework

- **JSONata Mapping Templates** — CRUD for data-transformation templates; expressions validated at creation time; evaluation times out after 5 s with timer cleanup.
- **HMAC Verification** — Webhook payloads verified against raw request bytes (`req.rawBody`); no JSON re-serialization fallback.
- **Payload Type Guards** — Expenses and side-gig ledger entries validated before merging into state.
- **OAuth Stub** — `/api/sync/init` + `/api/sync/callback` scaffold; CSRF state consumed immediately after verification.

## Privacy

- **Privacy Modal** — GDPR-style consent gate backed by `docs/privacy-policy.md`; acceptance persisted to localStorage with policy-version key.
- **XSS Hardening** — Shared `html-utils.js` `escHtml()` applied across all table renderers; `data-*` attribute pattern used for event delegation to avoid onclick injection.

## Dashboard & UX

- **Glassmorphic Dark Theme** — High-end HTML5 layout with CSS glassmorphism and HSL color tokens.
- **Header Summary Bar** — Mini allocation bars, Annual Income metric, and FIRE Progress bar with percentage.
- **Financial Overview Tab** — Unified Accounts + CDs & Fixed Income tab with Monthly Cash Flow section (income vs. expenses, savings rate, annual surplus/deficit).
- **Mobile-Responsive Layout** — Adaptive layout for tablet and phone viewports.
- **Metric Tooltips** — Inline explanation indicators for SWR, FIRE number, Coast FIRE, etc.
- **Settings Page** — Unified configuration with notification preferences, export/import, projection defaults, privacy/terms, and danger zone.
- **Milestone Preset Selector** — 5 financial profiles (Conservative, Standard, Aggressive, Barista FIRE, Coast FIRE) with dynamic targets based on user's income/net worth.

## Integrations (UI Ready)

- **eBay OAuth Status** — Connection status check with authorize/sync endpoints in Settings page.
- **Plaid Link Integration** — Plaid Link SDK embedded for bank/Fidelity aggregation; create-link-token and exchange endpoints.
- **Vehicle Value Estimates** — Estimate overlay with depreciation model and market data sources; accept/save to vehicle record.

## Diversification Intelligence

- **Diversification Tip Tiles** — Data-driven dismissible cards with severity (info/warning), context-aware messages, and curated educational links.
- **LocalStorage Persistence** — Dismissed tips remembered across sessions; restore-all button when tips are dismissed.
- **Smart Triggers** — High cash (>30%), equity concentration (>70%), low equity (<30% with NW >$50k), heavy fixed income (>40% CDs), missing real estate (>$100k NW), single-stock concentration (>20%), no international exposure.

## Architecture

- **Modular SPA** — `app/lib/` split into `charts/`, `tables/`, and `managers/` sub-directories; shared utilities in `app/lib/` root.
- **Dual Projection Copies** — `app/lib/projections.js` (browser, Chart.js) and `app/lib/finance-calcs.js` (server, MCP + API) kept in sync.
- **Input Validation** — Route-level validation for account names (non-empty string), CD maturity dates (YYYY-MM-DD + UTC round-trip), numeric fields (strict parse), and nested state objects (plain-object guard).

## Testing

- **Vitest Suite** — Unit and integration tests; coverage tracked via `@vitest/coverage-v8`.
- **MCP Smoke Test** — `scripts/test-mcp.mjs` exercises all 8 tools end-to-end via the SDK client.

## Planned

- **Tax Drag Estimation Engine** — Custom federal/state bracket support with capital gains configuration.
- **PWA Packaging** — Offline access and lightweight installable app.
- **Netlify Functions + Blobs Backend** — Cloud data backend so MCP can read from deployed instance.
- **Webhook Sync Testing** — End-to-end validation of sync template round-trips.
