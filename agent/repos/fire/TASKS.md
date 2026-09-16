updated: 2026-09-11

# Tasks

---

## In Progress

_(none — all Q4 2026 tasks complete; see ROADMAP.md for phase details)_

---

## Q4 2026 — Current Cycle ✅ COMPLETE

> Note: a prior audit found this section contradicting ROADMAP.md — two items
> below were checked off `[x]` here while their own note said "deferred" (not
> actually implemented), while ROADMAP.md correctly left them unchecked under
> Q4 2026 / PROD Phase 4. Un-checked below to match reality; they're tracked
> once, under PROD Phase 2 / Phase 4 respectively, not also claimed done here.

- [x] Webhook sync end-to-end testing (template CRUD → ingest → db.json verification)
- [x] Retirement projection drawdown & depletion age (money run-out detection)
- [x] Milestone presets — 5 financial profiles with dynamic targets
- [x] Diversification tips redesign — dismissible tiles with curated links
- [x] Unified Settings page — notifications, export/import, projection defaults, privacy/terms, danger zone
- [x] eBay & Plaid integration UI — connection status, Plaid Link SDK
- [x] Vehicle estimate overlay — complete CSS styling
- [x] Fix retirement projection syntax error (duplicate return block)
- [x] All 251 tests passing (16 test files)

---

## PROD Phase 1 — Real-Time Data Connectors (now live)

### eBay API Connector
- [x] Validate eBay fee rates in `finance-platforms.js` against current published rates
- [x] UI toggle in settings to enable/disable eBay sync and show last-sync timestamp
- [ ] Write tests for `app/lib/ebay-connector.js` and the 4 eBay sync routes
  - `app/lib/ebay-connector.js` already has full lib-level coverage (17 tests, pre-existing). Added route-level tests for the new `/ebay/toggle` route plus `/ebay/status` and the `/ebay/sync` disabled-gate (`tests/unit/sync-ebay-route.test.mjs`). `/ebay/authorize`, `/ebay/callback`, and `/ebay/refresh` still have no route-level (HTTP) tests — they need a session-backed OAuth redirect flow to exercise properly.
- [ ] Model real eBay fee brackets in `calculateEbayFeesTotal` (`app/lib/side-gig.js`), not just a flat rate + order fee.
  - Priority: P2
  - Context: flagged by CodeRabbit on PR #103 (2026-09-10) — the calculator (pre-existing, not introduced by that PR) applies one percentage across the whole transaction value with the pre-#103-corrected $0.30 order fee. Real eBay fee structure has marginal percentage tiers above each category's sale cap, and several categories' effective rate changes at that cap. The $0.30-vs-$0.40 order-fee threshold was fixed directly (order value ≤$10 vs. >$10); the marginal-bracket-per-category modeling was not — it needs each category's actual cap/tier data (not currently captured anywhere in this codebase) and a real per-category fee-rule schema, not a scalar percentage dropdown.
  - Acceptance Criteria: `ebay-category-rate` stores a fee-rule identifier (not a bare percentage), and `calculateEbayFeesTotal` resolves that rule's tiers/caps rather than multiplying one flat rate across the full transaction value.

### Web3 / Crypto Wallet Tracking
- [x] UI: wallet manager section in Financial Overview tab (add/remove wallets, balance display)
- [x] Write tests for `app/routes/wallets.js` and `app/lib/web3-prices.js`

### Vehicle Value API
- [x] UI: "Refresh Value" button on vehicle cards with last-updated timestamp
- [x] Write tests for `app/routes/vehicles.js` and `app/lib/vehicle-api.js`

### Google Drive Encrypted Backup
- [x] UI: backup panel in settings (trigger, list, restore buttons)
- [x] Write tests for `app/routes/backup.js` and `app/lib/gdrive-backup.js`

---

## PROD Phase 2 — Financial Institution Integration (partially live)

### Fidelity / Plaid
- [x] `POST /api/sync/plaid/transactions` — parse into expense categories
  - Added to `app/routes/sync.js`: paginates each linked item via Plaid's
    `/transactions/sync` (cursor persisted per item in `tokens-plaid.json`
    so repeat calls only fetch what changed), then maps the results into
    this app's existing expense-category schema via the new
    `parsePlaidTransactions`/`plaidCategoryToExpenseCategory` in
    `app/lib/finance-parsing.js` — reusing the same
    `state.spendingTransactions` store and `{id, date, merchant, amount,
    category}` shape the Fidelity/Chase/Capital One CSV importer already
    produces, not a new pipeline. Category resolution tries, in order:
    Plaid's modern `personal_finance_category.detailed`
    (`PLAID_CATEGORY_MAP`), then `.primary` (`PLAID_PRIMARY_CATEGORY_MAP`),
    then a light read of the legacy `category` array, then the same
    merchant-keyword fallback (`_descToCategory`) Chase/CapOne rows use
    when their own statement category doesn't map. Dedup by
    `plaid-${transaction_id}`, same pattern as the eBay ledger sync.
    Gated behind a new `plaidSyncEnabled` setting (default `true`,
    `POST /plaid/toggle`) mirroring the eBay sync toggle.
  - Caveat: only verified against a mocked `/transactions/sync` response
    shaped to match Plaid's published API docs (see
    `tests/unit/sync-plaid-route.test.mjs`) — this environment has no real
    Plaid sandbox credentials, so live-API behavior (auth/pagination edge
    cases, real-world `personal_finance_category` values) is unverified.
  - Follow-up (CodeRabbit, PR #108 review): the initial version only
    applied `data.added`, silently ignoring `data.modified` (e.g. a
    pending amount finalizing on posting) and `data.removed` (e.g. a
    reversed charge) while still advancing the cursor past them —
    permanently losing those changes. Now applies all three: `modified`
    upserts the existing record (or removes it if the update no longer
    qualifies as a trackable expense, e.g. reverted to pending), `removed`
    deletes the matching record. Also fixed: (1) an item that completes
    pagination with zero new transactions was wrongly treated as "this
    item's fetch produced nothing" and could trip the "all items failed"
    502 path if every OTHER item also happened to add nothing — now a
    total-failure verdict is based on how many items actually completed
    pagination, not how many transactions came back; (2) exhausting the
    20-page defensive cap while Plaid still reported `has_more: true` used
    to silently advance the cursor past whatever was fetched, permanently
    skipping the un-fetched remainder — now treated as a failure for that
    item, discarding its partial batch and keeping the original cursor so
    the next sync restarts it from the true beginning (per Plaid's own
    guidance for interrupted pagination); (3) `saveTokens()`'s token-file
    write is no longer unguarded — a failure there now returns a specific
    5xx instead of silently reporting `status: 'success'` while the cursor
    didn't actually move. 5 new tests (411 total, up from 406).
- [x] Disable manual Fidelity CSV import UI when Plaid sync is active (prevent duplicates)
  - "Active" = a Plaid item is linked AND `plaidSyncEnabled` isn't
    explicitly `false` (same definition `GET /plaid/status`'s new
    `syncEnabled` field reports). `setFidelityImportDisabled()` in
    `app/lib/csv-import.js` disables the `#csv-drag-zone` (click/drop/file
    picker all bail out early, plus `pointer-events:none` + dimmed style
    via `.fo-import-drop.disabled` in `app/lib/css/widgets.css`) and swaps
    in an explanatory label. Wired up in `app/lib/side-gig.js`'s
    `checkPlaidConnection()` (runs on page load and right after a
    successful Plaid Link) and `loadPlaidSettingsPanel()` (Settings tab,
    runs on load and after toggling), so the gate reacts immediately to
    both connecting/disconnecting and to the new Settings toggle.
  - Gap: no automated UI/e2e test clicks the drag zone to confirm it's
    inert — only the underlying `syncEnabled`/`connected` status the gate
    reads is covered by route tests. This repo doesn't currently run
    Playwright e2e specs against browser-side CSV import interactions
    (`tests/e2e-ui/` is for other flows), so extending that would be a
    larger addition than this pass's scope.
- [x] Write tests for Plaid routes in `app/routes/sync.js`
  - `tests/unit/sync-plaid-route.test.mjs` (18 tests): status/toggle
    persistence, the disabled-sync 403 gate, the no-token 401, the
    transactions happy path (categorization + dedup across repeat syncs),
    partial-item-failure warnings, the all-items-failed 502, applying
    modified/removed transactions, a zero-change item succeeding alongside
    a failing sibling, discarding a page-cap-interrupted item's batch
    while a sibling item still completes, and a sync-cursor save failure
    reporting a specific error without claiming success — all via a
    stubbed global `fetch` standing in for Plaid, same approach
    `tests/unit/vehicles-route.test.mjs` uses for its VIN-decode endpoint.
    `tests/unit/plaid-transactions-parsing.test.mjs` (12 tests) covers the
    categorization/parsing logic directly.
  - Same gap as the eBay item above: `/plaid/create-link-token`,
    `/plaid/exchange`, `/plaid/positions`, and `/plaid/accounts` are
    pre-existing routes with no route-level (HTTP) tests — out of scope
    for this pass, which focused on the new transaction-sync routes.

### Real-Time Price Improvements
- [ ] Write tests for `app/lib/prices-provider.js` (Alpha Vantage + Polygon paths)

---

## PROD Phase 3 — Security Hardening (mostly done; remaining items)

See [docs/security-hardening.md](docs/security-hardening.md) for full remediation detail.

- [x] Caddy reverse proxy in `config/docker-compose.yml` for HTTPS on localhost
  - Flagged by CodeRabbit on PR #105 (2026-09-11): adding Caddy alone didn't close the LAN-cleartext gap — `fire`'s own port was still published on every host interface (`"3001:3001"`), letting any device on the LAN bypass Caddy entirely. Fixed by rebinding to loopback only (`"127.0.0.1:3001:3001"`); a full unpublish was rejected since `fire`'s port is the configured target for the eBay/Google Drive OAuth redirect callbacks, which the browser hits directly. See `docs/security-hardening.md`'s H-02 for detail.
- [x] `config/Caddyfile` with TLS auto-cert for localhost
- [x] Flip `FIRE_API_KEY` to required by default; add `FIRE_AUTH_DISABLED=true` opt-out
- [x] Vitest test asserting no write tools are registered in MCP server
  - Found and fixed a real violation while writing this test: `set_price_target_alert`
    called `writeState()` (persisting to `db.json`) despite the MCP server being
    documented read-only. It now validates input and returns `not_implemented`
    like its sibling stubs, without touching disk. See
    `tests/unit/mcp-server-read-only.test.mjs`.
- [ ] Run full penetration testing checklist from docs/security-hardening.md
  - Reviewed the checklist (see docs/security-hardening.md) and triaged which items
    are checkable from this sandboxed dev environment vs. which need a real deployment:
    - **Checkable here (sandbox/unit-test level):** all of Authentication & Authorization
      except session-cookie forgery edge cases already covered incidentally; all of
      Injection; all of Information Disclosure; all of Denial of Service; MCP-Specific
      "no write tools" (now covered) and "audit log excludes response content" (log
      format is inspectable directly). Rate-limit-window-reset is checkable but needs
      fake timers or a real 60s wait.
    - **Needs a live/running deployment:** the entire Transport section (HTTP→HTTPS
      redirect, `Strict-Transport-Security` header, `Secure` cookie flag) requires an
      actual TLS handshake through the new Caddy container — doable locally via
      `docker compose -f config/docker-compose.yml up -d` + `curl -kv https://localhost`,
      but not a unit test. MCP "makes no external network calls" is only rigorously
      verifiable with the process's network access physically disabled (OS-level
      firewall / no-network container) — mocking `fetch` in a test is a reasonable
      proxy but not proof. OAuth CSRF replay and `tokens.json` encryption-after-callback
      both need a real (or fully mocked) OAuth provider round-trip, which exists only
      partially in the current test suite.
  - Not attempted as part of this pass — flagging for a follow-up task.
- [x] Close the branch/function coverage gap (68.33% branch vs. 70% threshold, 75.67% functions vs. 80%).
  - Priority: P2
  - Context: statement and line coverage clear the target but branch and function coverage don't — `config/vitest.config.ts` thresholds are stricter than the blanket 80% METRICS.md target implies. `app/server.js` (41.83% stmts) is the single biggest gap.
  - Acceptance Criteria: `npm run test:coverage` reports branch ≥70% and functions ≥80%; new tests target untested branches in `app/server.js` and the sync route error paths rather than padding easy files.
  - Evidence: on a fresh `main` checkout, `npm run test:coverage` already reported branch 70.36%/functions 84.16% (above the last-measured 68.33%/75.67% — the repo had drifted since the numbers above were recorded). Added 4 targeted tests for `app/server.js`'s previously-uncovered fail-fast paths (`SESSION_SECRET`/`FIRE_API_KEY`/`FIRE_ADMIN_KEY` required-in-production `process.exit(1)` checks, each only reachable in-process with `process.exit` mocked — the existing subprocess-based test for the same behavior earns no coverage credit) and the `express-rate-limit`-unavailable pass-through fallback. Result: branch 71.04%, functions 84.16%, statements 86.01%, lines 85.6% (`server.js` itself: 47.82% branch / 71.56% stmts, up from 36.95% / 66.66%). Full suite: 381/381 passing (was 377), lint clean. Note: several branches in `app/server.js` and `app/lib/finance-core.js` remain flagged "uncovered" in the report despite dedicated tests exercising them (verified by running those test files in isolation) — this is a `@vitest/coverage-v8` merge artifact when the same module is loaded via mixed CJS `require()`/ESM `import()` across many isolated per-file workers, not a real gap; not chased further since it isn't fixable by adding tests.

---

## PROD Phase 4 — Feature Parity (Q4 2027)

- [ ] Portfolio rebalancing suggestions (target allocation config + current allocation diff)
- [ ] Tax-loss harvesting alert (flag positions with unrealized losses ≥ threshold)
- [ ] Income vs. expense 12-month rolling trend view
- [ ] PWA: `manifest.json` + service worker for installable offline mode
- [ ] CD maturity and FIRE milestone notification system
- [ ] Optional multi-user mode (separate encrypted db.json per user, HTTP Basic auth gate)

---

## Completed ✅

- [x] MCP server — 12 functional tools + 7 registered stubs (fire_status_summary, get_net_worth, get_accounts, get_portfolio, get_cds, get_expenses, get_projection_settings, get_side_gig_income, get_wallets, get_concentration_risk, simulate_rebalance, get_emergency_runway)
- [x] Webhook sync framework with JSONata mapping and HMAC-SHA256 verification
- [x] AES-256-GCM encryption of db.json at rest (SYNC_MASTER_KEY)
- [x] OAuth stub scaffold (/api/sync/init, /api/sync/callback)
- [x] Yahoo Finance live price fetching (crumb-based auth, stale fallback, 5-min TTL)
- [x] Fidelity CSV import (multi-account aggregation)
- [x] Chase / Capital One statement parsing with auto-categorization
- [x] eBay / Etsy / Facebook fee calculators (manual-entry, server-side)
- [x] Multi-scenario FIRE comparison (salary bumps, market downturns, inflation)
- [x] Chart line toggles (NW, 75/100/125% FIRE goals, Coast FIRE, US Median)
- [x] Risk concentration badges (⚡ ≥15%, ⚠ ≥20%) on investment positions
- [x] CD ladder visualizer with annual yield badges
- [x] Real estate and vehicle trackers
- [x] Mobile-responsive layout
- [x] XSS hardening (escHtml + data-* event delegation pattern)
- [x] Atomic db.json writes (write-to-tmp then renameSync)
- [x] Concurrent write safety (mutateState() promise queue)
- [x] Webhook deduplication by stable upstream ID or content fingerprint
- [x] Financial Overview tab (unified Accounts + CDs + Cash Flow)
- [x] Header summary bar (allocation bars, income, FIRE progress %)
- [x] Diversification suggestion block
- [x] 251 unit/integration tests, 81.1% statement / 80.9% line coverage (measured 2026-08-28; target 80% statements/lines met, branch 68.33% and function 75.67% remain below their 70%/80% thresholds — see PROD Phase 3 below)
