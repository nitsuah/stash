---
up: "[[repos/fire]]"
title: "fire · CHANGELOG"
source: https://github.com/nitsuah/fire/blob/main/docs/CHANGELOG.md
kind: repo-doc
repo: fire
---

# Changelog

> 🧭 [fire](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 2026-10 — Multichain crypto account value

#### Added
- **Multichain value for ENS/0x crypto accounts.** ⟳ Refresh now totals native coins plus priced ERC-20 tokens across Ethereum, Base, Optimism, Arbitrum, Polygon, BNB Chain and Avalanche (`app/lib/multichain-balance.js`). It uses keyless Blockscout explorers and publicnode.com RPCs, and filters spam tokens: unpriced, flagged as scam, few holders, or absurd values. The row shows a per-chain breakdown, plus ⚠ when a chain couldn't be read. The ENS lookup card uses the same source, with top tokens per chain. Previously only mainnet ETH counted.

#### Changed

- The hosted `fire-api` no longer imports `web3-prices`/`config/chains.json` for the ENS lookup (and `netlify.toml` no longer bundles the file). Etherscan-family keys are now used only by the server-side wallet tracker.

#### Docs
- Brought every doc up to date: the README architecture tree (route split, CoinTracker, multichain, Netlify functions) and integrations; integrations.md (multichain section); privacy policy (lookup services); FEATURES; TASKS/ROADMAP status; METRICS coverage; and `copilot-instructions.md` (it claimed SQLite/Postgres; the app uses `db.json`).

### 2026-10 — CoinTracker wallet sync (#139)

#### Fixed (follow-up)
- ENS/address crypto refresh failed with `ETH RPC error: Internal error`: the retired `cloudflare-eth.com` gateway was replaced with `ethereum-rpc.publicnode.com` (override with `ETH_RPC_URL`), the same default the ENS resolver uses.
- **Hosted site: gold/silver and crypto refresh were broken.** `fire-api` imported the `ethers`-based ENS resolver, which Netlify's function bundle doesn't ship, so the whole function crashed (`Cannot find module 'ethers'`), metals included. It now resolves ENS with the dependency-free resolver in `crypto-balance.js`. Crypto account ⟳ Refresh works on the hosted site through a new stateless `POST /api/accounts/refresh-crypto`. The hosted metal refresh no longer throws on an undefined variable, and both refreshes now save the new value in browser-only mode.
- The first live connect logged in, but CoinTracker's MCP server rejected the token. The authorize request now asks Auth0 for an MCP-audience token (`audience`, configurable with `COINTRACKER_AUDIENCE`). A 401 now shows the rejected token's shape (format, `aud`, `scope`) in the card, and CoinTracker's own login errors are passed through instead of a generic `access_denied`.

#### Added
- **CoinTracker connector (optional).** Settings → CoinTracker Wallets connects through OAuth 2.1 + PKCE (dynamic client registration, `mcp:read offline_access`) and reads wallet balances from CoinTracker's read-only MCP server. CoinTracker offers no REST API or personal token. The same `/api/sync/cointracker/*` routes run on Express and as a Netlify Function, and neither stores anything: the token is sealed with `SYNC_MASTER_KEY` and kept in the browser.
- Each CoinTracker wallet becomes a Crypto account, tagged "CoinTracker" with its sync time and per-asset holdings, so the dashboard shows the multichain total and each wallet's value. Balances refresh automatically on load when they are more than 6 hours old.
- **Dedupe, with CoinTracker as the source of truth:** a manual crypto account with the same address or ENS is adopted (it keeps its name and APY and takes CoinTracker's value) and is restored on disconnect. Ticker-only or address-less manual entries are listed as possible duplicates. Wallets can be excluded, and partial syncs never remove wallets. The MCP server's net worth no longer double-counts tracked wallets that CoinTracker also reports.
- "Inspect CoinTracker tools" lists CoinTracker's MCP tools (no portfolio data) and the one used for balances. `COINTRACKER_BALANCE_TOOL` pins it.

### 2026-10 — Chaos mode, customizable layout, fire-coach skill

#### Added (follow-up)
- **Section layouts:** every tab is now a board of sections. Each section has a column layout (1, 2, 2 wide-left, 2 wide-right, 3, 3 wide-center, 4) and its cells stack cards. A card alone in a section spans the full width, and the fixed per-tab grids (such as the locked Growth Settings column) are gone. Customize mode is a drag-and-drop builder with highlighted targets, a drop placeholder and "New section" gaps.
- **Chaos sequences:** parent care → funeral → inheritance or inherited house; wedding → child → daycare ends; job loss → new job. Follow-ups show "after …" in tooltips and chips.
- **More good events:** inherited house (sell, move in or rent out), refinance, car loan paid off, roommate/house hack, settlement payout, family gift. The catalog now has 37 events.
- **Costs that outrun inflation:** rent (+1%/yr), child costs (+1%), elder care (+3%), insurance after a claim (+2%), and medical and vet bills (+2%/yr) escalate in the real-terms projection. Descriptions quote the inflation setting.
- **🛡️ Mitigations** in Insights: tick coverage you have (pet insurance, HSA/low-OOP plan, disability, dental, umbrella, water-backup, gap, credit freeze, safe-harbor withholding, emergency fund). Chaos shrinks the covered hits and charges the premiums every year. Each card shows what it saves and costs in the current simulated life.
- `promo/chaos-24s` (renamed from `chaos-22s`) adds a Mitigate scene and uses chaos seed 23, which includes a funeral → inherited house sequence.

#### Changed (follow-up)
- Promotions are a signing bump or 5–6 years of extra savings rather than a permanent raise, since wages are flat in real terms.
- Merged the strict CSP (#150): the Chaos/🎲 buttons use `data-csp-click-action`, and chip colors and layout previews are set via the CSSOM. A new browser test asserts no CSP violations.

#### Fixed (follow-up)
- Same-year chain follow-ups, and follow-ups of top-up events, were dropped; they now run in year order.
- On phones, 3- and 4-column sections now collapse to one column (a CSS specificity bug left them at two).
- The widget picker traps Tab, keeps focus on the row you acted on and returns focus to its opener. Malformed saved layouts are rejected or sanitized before use.
- Landing page: zoomed images toggle actual size with Enter/Space, and the picker screenshot keeps its position when made zoomable.
- Bear / Base / Bull: after the strict-CSP change (#150) the click delegation passed the offset as a string, so "8" + "0" projected an 80% return. The offset is now coerced to a number, with a browser test.

#### Added
- **🌪️ Chaos mode:** a toggle next to Bear/Bull on Projections and on the Dashboard growth chart rolls seeded, realistic life events onto the projection. There are 30 events in 8 categories, each with a life-average probability, an age window, a lifetime cap, a repeat gap and 2–3 predefined outcomes. The app shows ▲/▼ category-colored markers, a dashed "Without chaos" line, event details in the chart tooltip, an event-chip timeline that follows the 1Y–All window, and 🎲 reroll. The chart's FIRE-crossing markers, the Milestone Predictions estimates (marked 🌪️) and the run-out age all follow the chaos path. The toggle and seed are saved in localStorage (`app/lib/chaos-events.js`, 20 unit tests, plus a browser test that the engine with no events reproduces the app's projection exactly).
- **How chaos changes net worth:** one-time costs and gains land in the year they happen and then compound (or fail to) with the rest of the portfolio. Recurring costs and income change the yearly savings, or the yearly withdrawal once retired, for their duration. A job loss costs the lost months of savings plus real spending; the FIRE number's tax padding is left out, since there's no paycheck to tax. Paycheck events (job loss, pay cut, bonus, RSUs) are skipped when Expenses → gross income is under $5k.
- **Customizable layout:** clicking a card title collapses it on every tab. ✎ Customize adds pointer drag (mouse and touch) and ↑/↓ reorder, and Dashboard cards can move between columns. ＋ Add widget pins any card from another tab to the Dashboard and leaves a "Move back here" placeholder; ✕ removes Dashboard cards and ↺ Reset restores a tab. Saved in localStorage (`app/lib/layout-manager.js`).
- **fire-coach Claude skill** (`skills/fire-coach/`): `SKILL.md` maps questions to MCP tools, with a FIRE financial playbook and an app guide as references. `skills/README.md` covers installation.
- **Landing page:** new Chaos mode and "Make it yours" sections, the `chaos-24s` demo video, and the skill in the Claude section. The nav adds "Chaos", and the Plaid footnote reflects the Netlify Functions from #146. Screenshots are larger (wider page, wider image column), and every screenshot and the Chaos video open full size on tap or click; tapping again shows actual pixels.
- **Promo:** `promo/chaos-24s` spot. `capture.js` now also shoots the chaos chart, tooltip, phone and Customize/picker views, using shared price mocks and chaos seed 60.
- 8 Playwright tests for chaos and layout (`tests/e2e-ui/chaos-and-layout.spec.js`).

#### Changed
- Card titles are focusable and show a collapse chevron; they keep their heading role.
- After you arrange the Dashboard by hand, wide screens (≥1400px) keep the two columns instead of the fixed three-column grid.
- Service worker cache is bumped to `fire-tracker-v4` and precaches the two new scripts.

### 2026-09 — Drive backup, privacy and security doc accuracy (PR #149)

#### Fixed
- Google Drive setup docs describe the OAuth client flow the code actually uses (no service-account mode) and list `SYNC_MASTER_KEY` as required.
- Privacy policy discloses the opt-in encrypted Drive backup under self-hosted mode (`drive.file` scope, encrypted token in `data/tokens-gdrive.json`), lists the Google endpoints it calls, and explains how to delete it.
- `security-hardening.md` Remaining Gaps is one well-formed table again, with H-01, H-03, H-05, H-06, H-07, H-12 and H-13 and their status.
- TASKS/METRICS/CHANGELOG no longer imply CI enforces coverage codebase-wide: the thresholds apply only to the 8 files in `coverage.include`.

### 2026-09 — Split sync routes, Plaid on the Netlify deploy (PR #146)

#### Added
- **Plaid routes on the Netlify deploy:** `netlify/functions/plaid.mjs` serves Link, exchange, accounts, positions and transactions at the same `/api/sync/plaid/*` paths. No access tokens are stored on the server. The browser holds an AES-256-GCM token (rolling 180-day expiry) that also carries the transaction cursor.
- Hosted Plaid needs `PLAID_HOSTED_ACCESS_KEY` outside the sandbox and a 64-hex `SYNC_MASTER_KEY`. It checks both before calling Plaid.

#### Changed
- `app/routes/sync.js` is split into `app/routes/ebay.js` and `app/routes/plaid.js`, and the token file helpers are in `app/lib/token-store.js`. Route paths are unchanged.
- Plaid accounts and positions record `plaidItemId`. A partial sync replaces only the items that synced, and responses report `syncedItemIds` and a `warning`.

#### Fixed
- `/plaid/positions` no longer wipes saved positions when every item fails, and Plaid rows saved before item ids existed are replaced instead of duplicated.
- `/plaid/status` reports `lastUpdated` again, and token saves no longer collide on a shared temp file.

### 2026-09 — eBay on the Netlify deploy (PR #130)

#### Added
- **eBay routes on lifefire.netlify.app:** Marketplace Account Deletion, Connect (authorize/callback) and Sync are served by Netlify Functions at the same `/api/sync/ebay/*` paths the Express server uses. The deletion endpoint is live, and eBay accepted it on 2026-09-26.
- Browser-only eBay mode keeps only an encrypted token blob in `localStorage`. The server stores nothing.
- If eBay access is revoked (`invalid_grant`), the token and the API-synced ledger rows are removed and the user is told. Uploaded report rows and manual entries are kept.

#### Changed
- The deletion and sync logic lives in `app/lib/ebay-handlers.js`, which both Express and the Functions use.

#### Fixed (PR #132)
- eBay Sync Now returned 502 in production. The Order API rejects the filter `orderfulfillmentstatus:{FULFILLED}`, so sync now uses `{FULFILLED|IN_PROGRESS}`.
- Plaid Link called `create-link-token` with GET, but the route only accepts POST.

### 2026-09 — Hardening, tests, real MCP tools (PR #129)

#### Added
- **FIRE progress sub-line:** past 100% it shows safe-withdrawal income and how many times it covers spending; before that, estimated years to FIRE.
- **Daily local backups** of db.json (`data/backups/`, newest 14 kept) and cleanup of stale temp files.
- **MCP:** `get_diversification_score`, `get_swr_sensitivity` and `simulate_rebalance` now return real results.
- **Playwright data-integrity suite**, and the UI suite now runs in CI.

#### Changed
- Net-worth, interest and expense math lives in one shared module (`app/lib/aggregates.js`) used by both the browser and the server.
- The container's time zone defaults to America/New_York.
- Removed the MCP stub tools that only returned `not_implemented`.

#### Fixed
- Switching tabs kept the previous tab's scroll position.
- The notification icon 404'd.

### 2026-09 — Income vs. assets cleanup

#### Changed
- **Side hustle income is no longer counted in net worth** (dashboard banner, allocation chart, projections, `getAggregateNetWorth`). It's income: once paid out it already sits in a cash balance, so adding the ledger too double counted it. It stays on the income side (Annual Income sub-line, cash flow).
- **Crypto staking/lending yield counts toward Annual Income** alongside HYSA and CD interest (`getEstimatedAnnualInterest().staking`; MCP `estimatedAnnualInterest.staking`).

#### Added
- **Net Worth History**: the server records a daily net-worth snapshot (`netWorthHistory`, updated hourly for the current day). There's a dashboard chart with 1M/3M/1Y/All ranges and change stats, and MCP `get_net_worth_trend` is now implemented (latest, 7/30/365-day and since-start changes, optional `days` limit).
- **Price-move alerts**: holdings that move at least N% in a day (default 5%, configurable in Settings) raise a bell alert and push once per symbol per day.
- **Side Gig Ledger tools**: totals strip (sales, fees & shipping, item costs entered, net profit, missing-cost warning), "Tag all untagged as…", an "Only items missing a cost" filter, and Enter-to-next-row cost entry.
- "Live · 3:42 PM · Today −$2,855" freshness pill on Top Investment Positions (greys out as "Prices as of …" once quotes are over 30 minutes old), plus each position's daily % move under its last price.
- Asset Allocation (and the banner bar) split out **Crypto** (blue) and **Precious Metals** (gold) slices with their own drill-downs; Other Assets is now neutral grey.

#### Fixed
- **The service worker served stale code forever.** Shell assets were cache-first under a fixed cache name, so browsers with the worker installed kept running old JS after every deploy. They are now network-first, with the cache as an offline fallback (cache v3).
- **Full saves from an out-of-date tab are refused** (`stateRevision` / `baseRevision` → 409) instead of overwriting newer data; the tab re-syncs and asks you to redo the change.
- **Stale tabs re-sync when you come back to them.** A tab left open reloads the data from the server when it becomes visible again (skipped while an edit is in progress), so editing in an old tab no longer posts its hours-old copy over newer changes.
- Matured CDs no longer count toward estimated interest (dashboard, Annual Income, cash flow, MCP).
- MCP `get_net_worth` floors underwater real estate / vehicle equity at $0, matching the dashboard.
- **Open tabs overwrote newer data every 5 minutes.** The background price refresh called `saveState()`, posting the tab's entire state, so an older tab silently reverted edits made elsewhere (e.g. a corrected eBay import). It now writes only price-derived fields via `PATCH /api/state/live-values`.

### 2026-09 — Live market values, Other Assets, interest roll-up (PR #126)

#### Added
- **Live gold/silver** (`/api/metals`): Metal accounts are valued at what a dealer pays — oz × spot × 95% (gold) / 88% (silver) — refreshed every 5 minutes.
- **Other Assets** dashboard card: metals (with the spot × payout math), real estate and vehicle equity, and other valuables, with a total.
- **Interest estimates**: HYSA/cash accounts with an APY show green est. yearly earnings in Cash & Fixed Income; HYSA + CD interest is rolled into the Annual Income banner and a new Savings Interest cash-flow row. MCP `get_accounts` reports `estimatedAnnualInterest`.
- Per-type holdings badges (savings green, cash teal, crypto blue, CD amber, metals animated gold/silver sheen).

#### Fixed
- **Stock prices stopped updating** when Yahoo's v7 quote API returned 401; `/api/prices` now falls back to the crumb-free v8 chart endpoint, so position value/PnL stay live.
- **eBay report import double-counted shipping labels** ("Total selling costs" already includes them), understating side-gig net; it now matches eBay's Net sales. Re-importing the same report refreshes changed rows in place.
- Income Sources / Monthly Expenses start expanded on desktop (collapsed only on phones) instead of looking empty.
- `side-gig-tax.js` threw `round2 is not defined` under Node (MCP `get_side_gig_tax_summary`, tests); the metals refresh timer blocked process exit and was never scheduled in the browser (undeclared `metalsRefreshTimer`).

#### Changed
- MCP `get_net_worth` reports metals/other valuables as `otherAssets` instead of folding them into cash.

### 2026-09 — eBay notification signature verification (PR #123)

#### Security
- **Marketplace Account Deletion notifications are now signature-verified** (CWE-345). `POST /api/sync/ebay/marketplace-account-deletion` checks eBay's `X-EBAY-SIGNATURE` (ECDSA, public key per `kid` fetched from the Notification API and cached) over the raw request body, falling back to `JSON.stringify(body)` as eBay's SDKs do, before purging tokens or disabling sync. Unsigned, tampered or unknown-`kid` notifications get `412`; key-lookup failures or missing `EBAY_CLIENT_ID`/`EBAY_CLIENT_SECRET` get `503` so eBay retries. Previously the endpoint trusted only the secret URL + verification token.

### 2026-09 — Coverage gate + docs reset

#### Fixed
- Branch coverage restored above the 70% threshold (74.85%, 484 tests via `tests/unit/finance-calcs-branches.test.mjs`) and CI now runs `npm run test:coverage`, so the threshold fails the build for the 8 files in `coverage.include` (not the whole codebase) (#118, #119).
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

- Agent instructions (`.github/copilot-instructions.md`) now require closing tracked work in the same PR: update `docs/TASKS.md`, `docs/ROADMAP.md` and this changelog before the last push, and confirm `git diff origin/main...HEAD --stat` includes them before merge; added `.github/pull_request_template.md` with a "Closes TASKS item(s)" checklist.
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