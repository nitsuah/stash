# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

## [0.1.0] - YYYY-MM-DD

### Added

- Project initialization

[Unreleased]: https://github.com/nitsuah/fire/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nitsuah/fire/releases/tag/v0.1.0