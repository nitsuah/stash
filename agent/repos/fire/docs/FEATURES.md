---
up: "[[repos/fire]]"
source: https://github.com/nitsuah/fire/blob/main/docs/FEATURES.md
---

# Features

> 🧭 [fire](../README.md) · **Features** · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

`nitsuah/fire` is a lightweight FIRE (Financial Independence, Retire Early) tracker and API server built with Node/Express and vanilla JavaScript, designed for local self-hosted use with full LLM integration via MCP.

## Core Infrastructure

- **Express Server** — Node/Alpine container on port 3001 (configurable via `PORT`); serves the SPA and REST API from the same process.
- **db.json Persistence** — All state stored server-side in `data/db.json` with atomic writes (write-to-tmp then rename) and full export/restore via the dashboard.
- **Optional Encryption** — `SYNC_MASTER_KEY` enables AES-256-GCM encryption of `db.json` at rest; key validated lazily so the server starts without it.
- **API Key Middleware** — `FIRE_API_KEY` is required by default (`FIRE_AUTH_DISABLED=true` opts out) and gates all `/api/*` routes behind an `X-Api-Key` header check.
- **HTTPS & Headers** — Caddy reverse proxy for `https://localhost`, loopback-only app port, CSP/X-Frame-Options/Referrer-Policy headers, SRI-pinned CDN scripts, rate limiting (300/min, 30/min on sync).
- **JSON API Errors** — unmatched `/api/*` returns JSON 404s; browser `fetchJson` reports non-JSON responses clearly.
- **Session Security** — `express-session` with `httpOnly` + `sameSite: lax` cookie flags; startup warns if `SESSION_SECRET` is unset.

## MCP Server

- **13 Functional Read-Only Tools** — `fire_status_summary`, `get_net_worth`, `get_accounts`, `get_portfolio`, `get_cds`, `get_expenses`, `get_projection_settings`, `get_side_gig_income`, `get_side_gig_tax_summary`, `get_wallets`, `get_concentration_risk`, `simulate_rebalance`, `get_emergency_runway` (plus 7 registered `not_implemented` stubs); a test asserts no write tools exist.
- **Claude Code Integration** — `.mcp.json` at repo root auto-connects the server when Claude Code starts in this directory.
- **Smoke Test** — `scripts/test-mcp.mjs` runs the full MCP handshake and validates the 8 original read-only tools listed in its `EXPECTED_TOOLS` (the five newer tools are covered by unit tests, not the smoke script).

## Net Worth Tracking

- **Unified Add Form** — Import CSV (default), Account/Asset, CD, Real Estate and Vehicle in one card.
- **Custom Accounts** — Manual entry with value, APY, and account type (Cash, Savings, Crypto, Precious Metal, Brokerage, Real Estate, Other); full CRUD via REST API with server-side validation.
- **Precious Metals** — Gold/Silver by troy oz valued at live spot (metals.dev or free Yahoo futures fallback) with a Refresh button.
- **Crypto Accounts** — ENS name, 0x address or ticker accepted in either Name or Identifier; refresh resolves live value; wallet tracker (multi-chain balances) appears under the form for Type = Cryptocurrency.
- **Fidelity CSV Import** — Parses Fidelity brokerage position exports; aggregates symbols, quantities, and cash; deduplicates settled cash from P&L.
- **Chase / Capital One CSV Import** — Parses credit card statement debits and auto-categorizes spending into monthly cash flow.
- **Spending Upload** — Expenses-tab CSV upload with auto-categorization, editable merchant-keyword mapping, and per-transaction delete.
- **Plaid Transaction Sync** — Bank/card transactions auto-categorized into Expenses; manual CSV import is disabled while active.
- **Real Estate Tracker** — Manual entry with property name, value, equity, mortgage, and notes; collision-resistant IDs.
- **Vehicle Tracker** — Make/model/year, current value, loan balance, and depreciation estimate; fleet summary view; negative equity preserved in net worth calculation.

## Investments Dashboard

- **P&L Table** — Red/green color scale, sortable faceted columns with inline totals, pie-chart filter that greys non-selected slices.
- **Risk Concentration Badges** — ⚡ for positions ≥15% of portfolio, ⚠ for ≥20%; market return comparison badges per position.
- **Diversification Suggestion Block** — Allocation-aware tips surfaced inline with the investments view.
- **Collapse-All Toggle** — Collapses investment rows; cost basis included in facet totals.
- **Phone-Width Positions** — Symbol, value and PnL only; a + column expands description, quantity, last price and cost basis.
- **Asset Allocation Drill-Down** — Click a slice (or use the category buttons) to see the accounts, positions, CDs or vehicles behind it; breadcrumb/back navigation.
- **Allocation Filter Reset** — Filter clears automatically when portfolio total is zero.

## Retirement Projections

- **Projection Engine** — Accumulation phase (adds savings) and decumulation phase (withdraws `annualExpenses`) split at retirement age; `realReturn = nominalReturn − inflation`. Drawdown is cash-first: cash is spent before invested assets, which compound at the non-cash return.
- **Growth Presets** — Conservative, Standard, Aggressive and Early Retiree (retires at 50, 3.25% SWR) set return, inflation and SWR in one click; the SWR selector matches numerically and adds a Custom option for unlisted rates.
- **Growth + Milestone Panel** — Growth Scenario and Milestone Focus sections in one card; milestone presets are buttons and follow the growth preset.
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
- **eBay Sales-Report Upload** — Seller Hub listings report → ledger rows (revenue = item sales + buyer shipping; expenses = selling costs + shipping labels); re-uploads skipped, later cumulative reports supersede older ranges.
- **eBay Order Sync & Compliance** — OAuth order sync plus the Marketplace Account Deletion endpoint (challenge handshake, token purge).
- **Side Hustle Accelerators** — Seven rotating ideas with video/guide links; dismissible with a positive empty state.
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
- **Header Summary Bar** — Mini allocation bars, Annual Income metric, and FIRE Progress bar; at narrow widths a single minimalist bar (FIRE progress split by allocation, hover/tap for breakdown, income and spend), moved into the top bar in portrait; alerts bell pinned right.
- **Responsive Navigation** — Collapsible sidebar on desktop; hamburger drawer on phones.
- **Wide-Screen Layouts** — Dashboard top row (Growth Path, Allocation, Cash & Fixed Income) and Financial Overview cash-flow row at ≥1400px; Retirement Growth Path expander.
- **Financial Overview** — Net Monthly Cash Flow with collapsible Income Sources / Monthly Expenses; full-width holdings, properties and vehicles.
- **Insights Tab** — Portfolio Insights tiles, Tax-Loss Harvesting alerts, Portfolio Rebalancing tool.
- **Financial Overview Tab** — Unified Accounts + CDs & Fixed Income tab with Monthly Cash Flow section (income vs. expenses, savings rate, annual surplus/deficit).
- **Mobile-Responsive Layout** — Adaptive layout for tablet and phone viewports.
- **Metric Tooltips** — Inline explanation indicators for SWR, FIRE number, Coast FIRE, etc.
- **Settings Page** — Projection defaults, notifications, eBay/Plaid connectors and sync toggles, privacy/terms, data management, Google Drive backup and danger zone, with colour-coded groups.
- **Milestone Preset Selector** — 5 financial profiles (Conservative, Standard, Aggressive, Barista FIRE, Coast FIRE) with dynamic targets based on user's income/net worth.

## Integrations (UI Ready)

- **eBay OAuth Status** — Connection status check with authorize/sync endpoints in Settings page.
- **Plaid Link Integration** — Plaid Link SDK embedded for bank/Fidelity aggregation; create-link-token and exchange endpoints.
- **Vehicle Value Estimates** — Estimate overlay with depreciation model and market data sources; accept/save to vehicle record.

## Diversification Intelligence

- **Diversification Tip Tiles** — Data-driven dismissible cards with severity (info/warning), context-aware messages, and curated educational links.
- **LocalStorage Persistence** — Dismissed tips remembered across sessions; restore-all button when tips are dismissed.
- **Smart Triggers** — High cash (>30%), equity concentration (>70%), low equity (<30% with NW >$50k), heavy fixed income (>40% CDs), missing real estate (>$100k NW), single-stock concentration (>20%), no international exposure, emergency fund <6 months, savings rate <15%, CD maturing within 60 days, SWR >4.5%, crypto >10% of net worth.

## Architecture

- **Modular SPA** — `app/lib/` split into `charts/`, `tables/`, and `managers/` sub-directories; shared utilities in `app/lib/` root.
- **Dual Projection Copies** — `app/lib/projections.js` (browser, Chart.js) and `app/lib/finance-calcs.js` (server, MCP + API) kept in sync.
- **Input Validation** — Route-level validation for account names (non-empty string), CD maturity dates (YYYY-MM-DD + UTC round-trip), numeric fields (strict parse), and nested state objects (plain-object guard).

## Testing

- **Vitest Suite** — 484 unit and integration tests; coverage tracked via `@vitest/coverage-v8`.
- **Playwright UI Suite** — 50 real-browser regression tests (layout, navigation, drill-down, imports, presets, responsive behaviour) run in a pinned Docker image.
- **MCP Smoke Test** — `scripts/test-mcp.mjs` exercises the 8 tools in `EXPECTED_TOOLS` end-to-end via the SDK client.

## Planned

- **Tax Drag Estimation Engine** — Custom federal/state bracket support with capital gains configuration.
- **PWA Packaging** — Offline access and lightweight installable app.
- **Netlify Functions + Blobs Backend** — Cloud data backend so MCP can read from deployed instance.
