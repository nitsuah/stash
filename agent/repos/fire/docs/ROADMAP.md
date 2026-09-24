# 🗺️ FIRE Tracker Roadmap

updated: 2026-09-23

---

## Q2 2026 ✅ — Foundation & Core Calculators

> Completed. Full tracker foundation shipped — see FEATURES.md for all shipped capabilities.

## Q3 2026 ✅ — Side Hustle Hub & Auto-Calculators

> Completed. All Q3 items shipped — see FEATURES.md.

## Q4 2026: Advanced Scenarios & Integrations 🧪

- [x] Multi-scenario FIRE comparison (salary bumps, market downturns, inflation spikes)
- [x] Webhook-based sync templates with JSONata data mapping and HMAC verification
- [x] MCP server — 12 functional tools + 7 registered stubs for Claude/LLM integration
- [x] Mobile-responsive layout
- [x] Retirement projection drawdown & depletion age (money run-out detection)
- [x] Milestone presets — 5 financial profiles with dynamic targets
- [x] Diversification tips redesign — dismissible tiles with curated links
- [x] Unified Settings page — notifications, export/import, projection defaults, privacy/terms, danger zone
- [x] eBay & Plaid integration UI — connection status, Plaid Link SDK
- [x] Vehicle estimate overlay — complete CSS styling
- [ ] Tax drag estimation engine (custom federal/state brackets, capital gains)
- [x] Webhook sync end-to-end testing
- [x] Responsive shell (hamburger nav, single-bar summary, wide-screen dashboard/FO rows)
- [x] Insights tab (rename, portfolio insights, rebalancing, tax-loss harvesting)
- [x] Precious-metals accounts with live spot pricing
- [x] eBay Marketplace Account Deletion endpoint + eBay sales-report CSV upload
- [x] Cash-first retirement drawdown, growth/milestone presets in one panel
- [ ] Lightweight PWA packaging

---

## PROD Phase 1 — Real-Time Data Connectors (Q1 2027) ✅

Goal: replace manual CSV imports with automated, API-driven data ingestion for key sources.
Full detail: [docs/prod-plan.md](docs/prod-plan.md)

### eBay API Connector
- [x] eBay OAuth 2.0 app credentials (BYOK: `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `EBAY_REFRESH_TOKEN`)
- [x] `GET /api/sync/ebay/authorize` — OAuth initiation with CSRF state
- [x] `GET /api/sync/ebay/callback` — code exchange + encrypted token storage
- [x] `POST /api/sync/ebay/sync` — pull completed orders into sideGigLedger automatically
- [x] `POST /api/sync/ebay/refresh` — access token refresh
- [x] eBay Order API deduplication via stable `orderId`
- [x] Sandbox/production environment toggle (`EBAY_ENVIRONMENT`)
- [x] Fee rate table validation against current eBay published rates
- [x] UI toggle in settings to enable/disable eBay sync and show last-sync timestamp
- [x] Marketplace Account Deletion endpoint (needs a public HTTPS URL + `EBAY_VERIFICATION_TOKEN` registered in the eBay Developer Portal)
- [x] Sales-report CSV upload into the Side Gig Ledger (deduplicated)
- [ ] Model real eBay marginal fee brackets per category (needs per-category cap/tier data)

### Web3 / Crypto Wallet Tracking
- [x] `wallets[]` schema in db.json (address, chain, label, lastBalance, lastFetched)
- [x] Wallet CRUD: `POST/GET/DELETE /api/wallets` + `POST /api/wallets/:id/refresh` + `POST /api/wallets/refresh-all`
- [x] Chain address validation (EVM regex, BTC P2PKH/bech32, Solana base58)
- [x] Etherscan API — ETH + ERC-20 token balances (BYOK: `ETHERSCAN_API_KEY`)
- [x] BNB Smart Chain via BscScan (BYOK: `BSCSCAN_API_KEY`)
- [x] Polygon via Polygonscan (BYOK: `POLYGONSCAN_API_KEY`)
- [x] Arbitrum via Arbiscan (BYOK: `ARBISCAN_API_KEY`)
- [x] Base via Basescan (BYOK: `BASESCAN_API_KEY`)
- [x] Avalanche via Routescan (optional BYOK: `ROUTESCAN_API_KEY`)
- [x] Bitcoin via Blockstream.info (no key required)
- [x] Solana via public RPC (no key required)
- [x] `config/chains.json` registry — add chains without code changes
- [x] Wallet USD totals aggregated into net worth
- [x] MCP tool: `get_wallets`
- [x] UI: wallet manager (now under the add form for Type = Cryptocurrency; ENS/0x/ticker accepted in Name or Identifier)

### Vehicle Value API
- [x] NHTSA VIN decode (`GET /api/vehicles/vin/:vin`, free, confirms vehicle identity)
- [x] Vehicle value BYOK integration (`VEHICLE_VALUE_API_KEY`, `VEHICLE_VALUE_PROVIDER`)
- [x] `POST /api/vehicles/:id/refresh-value` — fetch + update currentValue
- [x] UI: "Refresh Value" / Estimate button (in the Actions column) with last-updated timestamp

### Encrypted Cloud Backup
- [x] Google Drive API via service account key (BYOK: `GDRIVE_SERVICE_ACCOUNT_JSON`)
- [x] `POST /api/backup/drive` — AES-encrypt db.json + upload to Drive
- [x] `GET /api/backup/drive/list` — list available backups
- [x] `POST /api/backup/drive/restore` — download → decrypt → apply
- [x] UI: backup panel in settings (trigger, list, restore buttons)

---

## PROD Phase 2 — Financial Institution Integration (Q2 2027) 🏦

Goal: real-time read-only position and balance sync from major brokerages and banks.

### Fidelity / Plaid Integration
- [x] Plaid credentials via env vars (BYOK: `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ENV`)
- [x] `POST /api/sync/plaid/create-link-token` — generate Plaid Link token
- [x] `POST /api/sync/plaid/exchange` — exchange public token for encrypted access token
- [x] `POST /api/sync/plaid/positions` — sync investment holdings → `importedPositions`
- [x] `POST /api/sync/plaid/accounts` — sync balances → `customAccounts`
- [x] Encrypted token storage (per-provider token files, AES-256-GCM)
- [x] Transaction import → expense categorization
- [x] Disable manual Fidelity CSV import UI when Plaid sync is active (prevent duplicates)

### Real-Time Price Improvements
- [x] Price provider abstraction (`app/lib/prices-provider.js`) — swap Yahoo / Alpha Vantage / Polygon via env var
- [x] CoinGecko free API for crypto token prices (used in web3-prices.js; optional key via `COINGECKO_API_KEY`)
- [x] SSE endpoint `GET /api/prices/stream` for live price push to browser dashboard
- [x] Precious-metals spot (metals.dev BYOK, free Yahoo futures fallback)
- [ ] Unit tests for `app/lib/prices-provider.js` (Alpha Vantage / Polygon / fallback paths)

### Car Values
- [x] Free fallback: NHTSA VIN decode via `GET /api/vehicles/vin/:vin`
- [x] Premium: DataOne or MarketCheck via `VEHICLE_VALUE_PROVIDER` (BYOK)
- [ ] KBB API requires Cox Automotive partner agreement

---

## PROD Phase 3 — Security Hardening (Q3 2027) 🔐

Goal: harden the system for shared-machine and LAN-facing use.
Full detail: [docs/security-hardening.md](docs/security-hardening.md)

- [x] Rate limiting on all `/api/*` routes (`express-rate-limit`: 300/min general, 30/min sync)
- [x] Security headers (CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy) applied inline in server.js
- [x] `SESSION_SECRET` fail-fast in production if default/unset
- [x] `FIRE_API_KEY` warning in production if unset; `FIRE_ADMIN_KEY` required in production for key rotation
- [x] Webhook payload size cap (16KB) enforced in webhook receiver
- [x] Webhook `sideGigLedger` and all supported-type field-level schema validation
- [x] `npm audit --audit-level=high --omit=dev` CI gate (in `.github/workflows/ci.yml`)
- [x] `POST /api/admin/rotate-key` — re-encrypt db.json with new SYNC_MASTER_KEY (`FIRE_ADMIN_KEY`-gated)
- [x] MCP audit log (`data/mcp-audit.log`): tool name, timestamp, response byte size
- [x] Wallet address truncation in MCP responses (last 8 chars shown)
- [x] HTTPS via Caddy reverse proxy in docker-compose.yml (app port loopback-only)
- [x] `FIRE_API_KEY` required by default (`FIRE_AUTH_DISABLED=true` opt-out)
- [x] Vitest test asserting no write tools are registered in MCP server
- [x] CSP/SRI headers on CDN scripts
- [ ] Penetration testing checklist (see docs/security-hardening.md)

---

## PROD Phase 4 — Feature Parity (Q4 2027) 🚀

Goal: match Fidelity NetBenefits + Rocket Money from a tracking standpoint while preserving local-first privacy.

- [~] Portfolio rebalancing suggestions — v1 tool shipped on the Insights tab (target vs. actual); suggestions/refinements pending
- [~] Tax-loss harvesting alerts — v1 table shipped on the Insights tab; threshold config and notifications pending
- [ ] Income vs. expense 12-month rolling trend
- [ ] PWA — installable, offline-capable
- [~] Notification system — in-app alerts bell and browser-notification settings shipped; push/outbound delivery pending
- [ ] Optional multi-user mode (separate encrypted db.json per user, auth-gated)
- [ ] **Unified sync-health widget** — every integration (eBay, Plaid, each wallet chain, Drive backup) currently gets its own "show last-sync timestamp" UI task tracked separately in TASKS.md; consolidate into one settings panel showing last-sync time, status, and a manual "sync now" per connector. Closes 4 of the scattered PROD Phase 1/2 UI tasks with one component instead of four.
- [ ] **Outbound webhook / notification hook** — the webhook framework (`app/lib/webhook-integration.js`) is inbound-only today. A scheduled outbound POST of a net-worth/FIRE-progress snapshot to a user-supplied webhook URL (Discord, Slack, ntfy) would reuse the existing HMAC + JSONata infrastructure in reverse and is a natural pairing with the planned CD-maturity notification system.

## Ideas — not yet scheduled

- **Sequence-of-returns risk indicator** — the retirement projection already models bull/bear scenarios and drawdown after retirement age; surface a single risk badge (e.g. "vulnerable to a down year in your first 5 retired years") derived from the existing SWR curve math rather than adding a new calculation engine.
