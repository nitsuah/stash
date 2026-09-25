---
up: "[[repos/fire]]"
source: https://github.com/nitsuah/fire/blob/main/docs/CHANGELOG.md
---

# Changelog

> 🧭 [fire](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 2026-09 — eBay notification signature verification (PR #123)

#### Security
- **Marketplace Account Deletion notifications are now signature-verified** (CWE-345). `POST /api/sync/ebay/marketplace-account-deletion` checks eBay's `X-EBAY-SIGNATURE` (ECDSA, public key per `kid` fetched from the Notification API and cached) over the raw request body, falling back to `JSON.stringify(body)` as eBay's SDKs do, before purging tokens or disabling sync. Unsigned, tampered or unknown-`kid` notifications get `412`; key-lookup failures or missing `EBAY_CLIENT_ID`/`EBAY_CLIENT_SECRET` get `503` so eBay retries. Previously the endpoint trusted only the secret URL + verification token.

### 2026-09 — Coverage gate + docs reset

#### Fixed
- Branch coverage restored above the 70% threshold (74.85%, 484 tests via `tests/unit/finance-calcs-branches.test.mjs`) and CI now runs `npm run test:coverage`, so the threshold is actually enforced (#118, #119).
- Docker `test` image can write coverage output (`chown node:node /app`) (#119).

#### Changed
- Netlify deploy-status badge in README (#117); generated `coverage_summary.txt` untracked (#121); vitest / coverage-v8 5.0.1, prettier 3.9.8 (#114–#116).
- Planning docs reset for 2027 (`pmo-ff`): completed roadmap/TASKS items condensed into FEATURES/CHANGELOG, open 2026 Q4 items carried into 2027 Q1, relative doc links fixed, breadcrumb navigation + README docs index added.

### 2026-09 — Side gig tax tagging

#### Added
- **Tax tags on Side Gig Ledger sales** (`app/lib/side-gig-tax.js`): tag each sale as business/resale, personal, gift or free ($0 basis) with an optional item cost. The ledger shows an estimated-taxable summary, flags untagged sales and personal/gift sales missing a cost, and treats personal losses as non-taxable and non-deductible.
- **MCP tool `get_side_gig_tax_summary`** (read-only, optional `year`).

#### Fixed
- `get_side_gig_income` grouped every entry under "Other" with $0 gross because it read legacy `platform`/`gross` fields; it now reads `category`/`revenue`.
- The eBay calculator no longer folds item cost into Fees/Expenses; it is stored as `costBasis` (net is unchanged).

### 2026-09 — Product / UI + Reliability pass (PR #111)

#### Added
- **eBay Marketplace Account Deletion endpoint** (`GET/POST /api/sync/ebay/marketplace-account-deletion`) with the SHA-256 challenge handshake, token purge on notification, and `EBAY_VERIFICATION_TOKEN` / `EBAY_NOTIFICATION_ENDPOINT_URL` config; `trust proxy` so the OAuth redirect and endpoint URL follow the real host/protocol.
- **Precious metals** — `Metal` account type (gold/silver + troy oz) with live spot valuation (`app/lib/metals-prices.js`, metals.dev + Yahoo `GC=F`/`SI=F` fallback) and `POST /api/accounts/:id/refresh-metal`.
- **eBay sales-report CSV upload** (`app/lib/ebay-report.js`) into the Side Gig Ledger with dedupe by item + report range; the main CSV import recognises the format too.
- **Unified add form** — Import CSV is now the first/default option; crypto Name/Identifier are interchangeable (ENS, 0x address or ticker) client- and server-side; wallet tracking appears under the form for Type = Cryptocurrency.
- **Insights tab** (renamed from Taxes) with Portfolio Insights, Tax-Loss Harvesting, Portfolio Rebalancing and five new watchers (emergency fund, savings rate, CDs maturing, aggressive SWR, crypto share).
- **Side Hustle Accelerators** — seven rotating, dismissible ideas with video/guide links and a motivational empty state.
- **Dashboard** — interactive drill-down Asset Allocation (replaces Quick Stats); 3-column top row on wide screens; Retirement Growth Path expander.
- **Responsive shell** — hamburger nav drawer, single-bar summary at narrow widths (bell pinned right; moves into the top bar in portrait), collapsible cash-flow cards, collapsible position details (+ column) at phone width, Financial Overview 3-column cash-flow row on wide screens.
- **Settings** reordered with colour-coded groups; eBay/Plaid connectors moved here from Financial Overview.
- **Projections panel** — Growth Scenario and Milestone Focus sections in one card; growth presets drive the milestone preset; Early Retiree retires at 50.
- `app/lib/fetch-utils.js` `fetchJson`; JSON 404 for unmatched `/api/*`.
- Real-browser UI suite (`tests/e2e-ui`, Playwright) grown to 50 tests; unit suite to 472 tests.

#### Changed
- **Retirement drawdown is cash-first** — cash (Cash/Savings/money-market) is spent before invested assets, which grow at the non-cash return; both projection copies updated; cash fraction clamped; zero-asset retirements now record depletion.
- Emergency Fund milestones now scale off annual expenses (they were scaled off the FIRE number, ~12× too large).
- Financial Overview holdings/properties/vehicles use the full content width; Expenses tab leads with Basic Budget (consistent two-line labels) with Tax Estimator beside Spending Upload.
- Vehicles: Estimate button lives in Actions.
- Ledger table tolerates sync-shaped entries (`platform`/`gross`/`fees`).
- Playwright Docker image pinned to 1.63.0 to match `package.json`.

#### Fixed
- Wallet add/sync/lookup no longer throws `Unexpected token '<'` on API 404s.
- SWR selector compared values as text (4 never matched "4.0", 3.25 matched nothing) — now numeric with a Custom option.
- Notification dropdown rendering under dashboard cards (stacking-context trap on the banner).
- Dead sidebar collapse arrow; summary banner shrinking under its content once data loaded; positions table sideways scroll and insurance fields overlapping at narrow widths.
- Metal edit/PUT validation (positive weight, valid type, stale value/timestamp cleared); eBay deletion acknowledged only after full cleanup; malformed JSON rejected by `fetchJson`.
- Several review-round fixes (CodeRabbit) across projections, CSV a11y, position expand keys and hustle storage.

### Since the last changelog update (merged to `main`, Aug 27 → Sep 18)
- **Plaid transaction sync** (`POST /api/sync/plaid/transactions`, #108) with auto-categorization, cursor persistence and modified/removed handling; Fidelity CSV import disabled while Plaid sync is active. Follow-up fixes: apply `data.modified`/`data.removed`, not just `data.added` (was silently losing posted/reversed changes while still advancing the cursor); an item finishing pagination with zero new transactions no longer counts toward the "all items failed" 502 path; exhausting the 20-page defensive cap while Plaid still reports `has_more: true` now discards that item's partial batch and keeps the original cursor instead of silently skipping the unfetched remainder; a `saveTokens()` write failure now returns a specific 5xx instead of reporting `status: 'success'` with a stalled cursor.
- **Security** — `FIRE_API_KEY` required by default (`FIRE_AUTH_DISABLED=true` opt-out), Caddy HTTPS with loopback-only app port, MCP read-only guard test (found and fixed a write tool) (#105); CSP/SRI headers (#91); fail-fast and rate-limit fallback tests (#107).
- **UI wiring** for eBay sync, wallet manager, vehicle refresh and Drive backup (#103).
- **Expenses CSV spending upload** with auto-categorization and merchant mapping; ENS wallet lookup; collapsible nav and dashboard scroll fixes.
- Tax fix (TN missing from no-income-tax states) and true FIRE-basis expense total (#93).
- MCP portfolio-analysis tools and persisted price-target handling fix (#89); MCP now 12 functional tools + 7 stubs.
- Test coverage gap closed (branch/function thresholds met), webhook sync end-to-end and Playwright UI suites added.
- Dependency bumps (vitest 5, eslint 10.10, Playwright 1.63, express-rate-limit 8.7, hono, qs, fast-uri, globals) and METRICS refreshes.

### Added

- **MCP Server** (`app/mcp-server.mjs`) — 8 read-only tools (`fire_status_summary`, `get_net_worth`, `get_accounts`, `get_portfolio`, `get_cds`, `get_expenses`, `get_projection_settings`, `get_side_gig_income`) over stdio via `@modelcontextprotocol/sdk`.
- `.mcp.json` project-scoped MCP config; `scripts/test-mcp.mjs` smoke-tests all 8 tools end-to-end.
- **Privacy modal** — GDPR-style consent gate backed by `docs/privacy-policy.md`; acceptance persisted to localStorage.
- **API key middleware** — `FIRE_API_KEY` env var gates all `/api/*` routes.
- `app/lib/html-utils.js` — shared `escHtml()` XSS escape utility loaded before all table scripts.
- `SESSION_SECRET` startup warning; `httpOnly` + `sameSite: lax` added to session cookie config.
- `OAUTH_CALLBACK_URL` environment variable for configuring the OAuth redirect URI instead of deriving it from the port.
- JSONata mapping expressions validated at template creation time (`POST /api/sync/templates`).
- Webhook type validated against supported values at template creation time.
- JSONata evaluation times out after 5 seconds; timer handle cleared in `finally` to prevent leaks.
- `AbortSignal.timeout(10000)` on all outbound Yahoo Finance fetch calls.
- `defaultState()` extracted from `initDatabase` and reused in `readState` fallback.
- Express error-handling middleware in `server.js` catches unhandled route errors and returns 500 JSON.
- `findAvailablePort` rejects immediately on empty candidates array.
- API endpoints for managing user profiles and authentication.
- CRUD operations for income, expense, and investment transactions.
- Data models for financial records (income, expenses, investments, assets, liabilities).
- **Settings Page** — Unified configuration page with notification preferences, export/import, projection defaults, privacy/terms, and danger zone.
- **Milestone Presets** — 5 financial profiles (Conservative, Standard, Aggressive, Barista FIRE, Coast FIRE) with dynamic targets based on user's income/net worth.
- **Diversification Tips Redesign** — Data-driven dismissible tiles with curated educational links, persisted via localStorage.
- **Vehicle Estimate Overlay** — Complete CSS styling for the vehicle value estimate tooltip/overlay.
- **eBay & Plaid Integration UI** — Functional connection status checks and Plaid Link SDK integration in Settings page.

### Changed

- **Projection drawdown** — portfolio now withdraws `annualExpenses` per year after retirement age instead of continuing to accumulate; both `projections.js` (browser) and `finance-calcs.js` (server/MCP) updated.
- **db.js atomic writes** — `writeState` serialises to a `.tmp` file then `fs.renameSync` to prevent corrupt state on mid-write failure.
- **db.js `readState`** — distinguishes missing file (returns `defaultState()`) from corrupt/unreadable file (throws, propagating to Express error handler).
- **`routes/state.js`** POST merges `req.body` over current persisted state (not `defaultState()`); deep-merges `expenses` and `projectionSettings`; type-guards both nested fields against non-object payloads.
- **`routes/accounts.js`** POST validates non-empty name; PUT validates name when supplied and validates `value`/`apy` with `Number.isFinite`.
- **`routes/cds.js`** POST and PUT validate maturity as strict `YYYY-MM-DD` string with UTC round-trip check; rejects numeric timestamps and normalised invalid dates.
- **`crypto-utils.js`** — `SYNC_MASTER_KEY` validated lazily at call time (not module load) so server starts without it; random fallback key removed.
- **`sync.js`** — `oauthState` consumed immediately after CSRF verification; auth code removed from logs; `rawBody` required for HMAC (no `JSON.stringify` fallback); `mapping` type-checked before `jsonata()` call.
- **`real-estate.js` manager** — IDs now use `Date.now() + random suffix` (matches vehicles.js) to avoid millisecond collisions.
- **`yahoo-prices.js`** — crumb validation rejects empty, HTML, or oversized (>100 char) responses.
- **`mcp-server.mjs`** — negative equity preserved (removed `Math.max(0, ...)` clamping); `monthlyExpenses` derived from `fireNumber × swr / 12`; CD sort uses `Number.isFinite` to exclude `NaN` durations.
- **`webhook-integration.js`** — CD id ordering fixed so upstream id overrides fallback; `expenses` validated as plain object before spread; `sideGigLedger` entries deduplicated by stable id or content fingerprint.
- **`charts/allocation.js`** — stale filter reset when portfolio total is zero; non-position categories (CDs, Other, RealEstate, Vehicles) no longer unconditionally match every row.
- `readState` returns full default state schema on parse failure instead of empty object.
- `GET /api/sync/init` sets `req.session.oauthState` instead of replacing the entire session.
- `GET /api/sync/data` wraps token file read and decryption in try/catch.
- `routes/prices.js` validates `req.query.symbols` is a string before `.split()`.
- `managers/accounts.js` `saveEditAccount` validates `value` is finite before mutating state.
- `managers/vehicles.js` `saveEditVehicle` preserves `trim`, `color`, `monthlyPayment`, `notes` when edit form omits those inputs.
- `managers/cds.js` CD start date default uses local date instead of UTC `toISOString()`.
- `managers/real-estate.js` `saveEditRealEstate` preserves `notes` when input is not in the DOM.
- `tables/dashboard.js` `renderQuickStatsList` uses null-safe element lookups.
- `tables/liquid.js` CD entries missing `maturity` or `rate` are skipped.
- `tables/projections-table.js` `coastYears` clamped to 0.
- `charts/cd-ladder.js` empty-state hides canvas and inserts placeholder; tooltip normalises undefined `cd.rate` to 0; `var` replaced with `let`.
- `charts/allocation.js` unused `ALLOC_CATEGORY_KEYS` constant removed.
- `webhook-integration.js` warn/error logs no longer include full data payload.
- `yahoo-prices.js` cookie extraction uses `headers.getSetCookie()` on Node 18+.

### Fixed

- `DELETE /api/accounts/:id` returned HTTP 444 for a missing account; corrected to 404.
- **Retirement projection depletion math** — corrected money run-out calculation when real return < SWR; now accurately computes depletion age using continuous compounding for base/bull/bear scenarios.

### Security

- XSS: `escHtml()` applied across all table renderers (`positions`, `liquid`, `vehicles`, `side-gig-table`, `dashboard`, `real-estate`, `fixed-income`).
- XSS: `data-acc-name` attribute pattern in `positions.js` prevents onclick injection via account names.
- CSRF: `oauthState` deleted from session immediately after verification to prevent replay.
- HMAC: webhook handler rejects requests where `req.rawBody` is absent.
- Session: `httpOnly` and `sameSite: lax` flags added; startup warns on weak or missing `SESSION_SECRET`.

### Added (earlier)

- API endpoints for managing user profiles and authentication.
- CRUD operations for income, expense, and investment transactions.
- Data models for financial records (income, expenses, investments, assets, liabilities).
- Initial calculations for net worth and basic FIRE progress indicators.
- Basic data persistence layer (file-based db.json).

## [0.1.0] - 2026-06-03

### Added

- Project initialization

[Unreleased]: https://github.com/nitsuah/fire/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nitsuah/fire/releases/tag/v0.1.0