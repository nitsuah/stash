---
up: "[[repos/fire]]"
title: "fire · FEATURES"
source: https://github.com/nitsuah/fire/blob/main/docs/FEATURES.md
kind: repo-doc
repo: fire
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

- **16 Read-Only Tools** — `fire_status_summary`, `get_net_worth`, `get_net_worth_trend`, `get_accounts`, `get_portfolio`, `get_cds`, `get_expenses`, `get_projection_settings`, `get_side_gig_income`, `get_side_gig_tax_summary`, `get_wallets`, `get_concentration_risk`, `get_diversification_score`, `get_swr_sensitivity`, `simulate_rebalance`, `get_emergency_runway`. No stubs: tools with nothing behind them were removed. A test asserts no write tools exist.
- **Claude Code Integration** — `.mcp.json` at repo root auto-connects the server when Claude Code starts in this directory.
- **Smoke Test** — `scripts/test-mcp.mjs` runs the full MCP handshake and validates all 16 registered read-only tools in `EXPECTED_TOOLS`.
- **fire-coach Claude Skill** — `skills/fire-coach/` (SKILL.md + a FIRE financial playbook + an app guide) makes Claude a FIRE coach: it maps questions to the MCP tools, applies the playbook (4% rule, savings rate, order of operations, taxes, sequence risk, income-gap plan) and points to the exact tab/card/button. Install steps in `skills/README.md`.

## Net Worth Tracking

- **Unified Add Form** — Import CSV (default), Account/Asset, CD, Real Estate and Vehicle in one card.
- **Custom Accounts** — Manual entry with value, APY, and account type (Cash, Savings, Crypto, Precious Metal, Brokerage, Real Estate, Other); full CRUD via REST API with server-side validation.
- **Precious Metals** — Gold/Silver by troy oz valued at live spot (metals.dev or free Yahoo futures fallback) with a Refresh button.
- **Crypto Accounts** — ENS name, 0x address or ticker accepted in either Name or Identifier. ⟳ Refresh on an ENS/0x account totals native coins and priced tokens (spam filtered) across Ethereum, Base, Optimism, Arbitrum, Polygon, BNB Chain and Avalanche, keyless, on both the self-hosted and hosted deploys. A per-chain breakdown appears under the row, and a ⚠ when a chain couldn't be read. Ticker accounts are valued as quantity × live price. The wallet tracker (multi-chain balances) appears under the form for Type = Cryptocurrency.
- **CoinTracker Wallets (optional)** — Connect CoinTracker in Settings (OAuth, read-only) to import every wallet and exchange account with its current USD balance and per-asset holdings. CoinTracker is the source of truth: a matching manual crypto account is replaced while connected and restored on disconnect, and unmatched ones are flagged as possible duplicates. Rows are tagged "CoinTracker" with their sync time. P&L and tax stay in CoinTracker.
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
- **🌪️ Chaos Mode** — A toggle next to Bear/Bull (Projections) and on the Dashboard growth chart that rolls seeded, realistic life events onto the net worth path. There are 37 events in 8 categories (health, pets, family, career, housing, auto, windfalls, legal/money). Each has a life-average yearly probability, an age window, a lifetime cap, a repeat gap and 2–3 predefined outcomes (e.g. gallbladder surgery $2.5k / $6k / $14k).
  - **Sequences:** follow-up chains such as parent care → funeral → inheritance or inherited house, wedding → child → daycare ends, and job loss → new job. Same-year follow-ups are handled too.
  - **Good events:** an inherited house (sell, move in, or rent it out), refinance, car loan paid off, roommate/house hack, settlement payout and family gift, alongside bonuses, RSUs, a side hustle and windfalls.
  - **Accounting, in today's dollars:**
    - Lump sums land in their year and compound with the portfolio. Recurring flows change savings, or retirement withdrawals, for their duration.
    - Costs that outrun inflation escalate on top of it: rent +1%/yr, child costs +1%, elder care +3%, insurance after a claim +2%, and medical and vet bills +2%/yr the later they happen. Descriptions quote the inflation setting.
    - Wages are flat in real terms, so a promotion is a signing bump or 5–6 years of extra savings.
    - Job loss costs lost savings plus real spending. Paycheck events are skipped when gross income is under $5k.
  - **🛡️ Mitigations** (Insights): pet insurance, low-OOP plan/HSA, disability, dental, umbrella, water-backup, gap, credit freeze, safe-harbor withholding and an emergency fund. Ticked ones shrink the covered hits and charge their premiums every year, and each card shows saves vs. costs for the current simulated life.
  - **UI:** ▲/▼ markers colored by category, a dashed "without chaos" line, tooltip details including "after …" causes, an event-chip timeline that follows the 1Y–All window (≥1 event in year one, ≥3 per 5 years), 🌪️ chaos-aware Milestone Predictions and 🎲 reroll.
  - Seed, toggle and mitigations persist per browser (`app/lib/chaos-events.js`, unit-tested, plus a browser test that no-event chaos equals the base projection).
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
- **Settings Page** — Projection defaults, notifications, eBay/Plaid/CoinTracker connectors and sync toggles, privacy/terms, data management, Google Drive backup and danger zone, with colour-coded groups.
- **Customizable Layout (sections)** — Every tab is a board of sections. Each section picks a column layout (1, 2, 2 wide-left, 2 wide-right, 3, 3 wide-center, 4), and its cells stack cards. Empty cells collapse outside Customize mode, so a card alone in a section spans the full width; the old fixed per-tab grids are gone. Sections drop to 2 columns on narrow boards and to 1 on phones, using container queries.
  - **✎ Customize** is a builder canvas: dotted grid, outlined sections with a layout picker and ↑/↓/🗑, a highlighted target cell, a pulsing drop placeholder, a floating drag chip (mouse and touch), and "＋ New section" drop gaps. Cards also move with ↑/↓.
  - Click a title to collapse a card. Dashboard ＋ Add widget pins cards from other tabs (keyboard-trapped picker that restores focus), ✕ removes cards, ↺ Reset restores a tab.
  - Persisted per browser (`fire_layout_v2`, migrating v1) in `app/lib/layout-manager.js`. CSP-safe: no inline handlers or style attributes.
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

- **Vitest Suite** — 715 unit and integration tests; coverage tracked via `@vitest/coverage-v8`.
- **Playwright UI Suite** — 67 real-browser regression tests (layout, navigation, drill-down, imports, presets, responsive behaviour) run in a pinned Docker image.
- **MCP Smoke Test** — `scripts/test-mcp.mjs` exercises the 8 tools in `EXPECTED_TOOLS` end-to-end via the SDK client.

## Planned

- **Netlify Plaid backend** — Plaid Link, account/position sync, and transaction sync currently remain Express-only; the hosted browser deployment needs Netlify Functions before Plaid can be advertised as live there.

- **Tax Drag Estimation Engine** — Custom federal/state bracket support with capital gains configuration.
- **PWA Packaging** — Offline access and lightweight installable app.
- **Netlify Functions + Blobs Backend** — Cloud data backend so MCP can read from deployed instance.
