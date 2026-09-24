# fire

> Reviewed: 2026-09-23

## Overview

Self-hosted FIRE (Financial Independence, Retire Early) tracker and API server (Node/Express + vanilla JS SPA), run locally via Docker on port 3001. All financial data lives in `data/db.json` (optional AES-256-GCM encryption via `SYNC_MASTER_KEY`); read-only with respect to external accounts, local CRUD fully supported. Being productionized toward real-time API-driven sync (eBay, Web3 wallets, Fidelity/Plaid, Google Drive backup) across four PROD phases — see `docs/prod-plan.md`. Ships an MCP server (`app/mcp-server.mjs`, 12 functional tools) for Claude/LLM integration.

## Current Goals / Roadmap Focus

**Q2 2026** ✅ Completed — full tracker foundation.

**Q3 2026** ✅ Completed — side hustle hub & auto-calculators.

**Q4 2026: Advanced Scenarios & Integrations** — nearly done
- [x] Multi-scenario FIRE comparison, webhook sync templates (JSONata + HMAC), MCP server (12 tools + 7 stubs), mobile-responsive layout, drawdown/depletion age modeling, milestone presets, diversification tips redesign, unified Settings page, eBay/Plaid integration UI, vehicle estimate overlay, webhook sync end-to-end testing
- [ ] Tax drag estimation engine (custom federal/state brackets, capital gains)
- [ ] Lightweight PWA packaging

**PROD Phase 1 — Real-Time Data Connectors (Q1 2027)** ✅ live, cleanup remaining
- [x] eBay OAuth sync, Web3 wallet tracking (8 chains), vehicle VIN decode, Google Drive encrypted backup — all shipped with UI (fee-rate validation, sync toggle, wallet manager, refresh-value button, backup panel all done as of the 2026-09-10 cycle)
- [ ] Route-level (HTTP) tests still missing for `/ebay/authorize`, `/ebay/callback`, `/ebay/refresh` (need a session-backed OAuth flow to test properly)

**PROD Phase 2 — Financial Institution Integration (Q2 2027)** — nearly done
- [x] Plaid link-token/exchange/positions/accounts sync, price provider abstraction (Yahoo/Alpha Vantage/Polygon), SSE live price push
- [x] `POST /api/sync/plaid/transactions` → expense categorization (paginated sync with cursor persistence, handles added/modified/removed); Fidelity CSV import UI now disabled while Plaid sync is active; Plaid route tests added
- [ ] Tests for `app/lib/prices-provider.js` (Alpha Vantage + Polygon paths) still missing

**PROD Phase 3 — Security Hardening (Q3 2027)** — nearly done
- [x] Rate limiting, security headers, session-secret fail-fast, admin key rotation, MCP audit log, wallet address truncation, HTTPS via Caddy reverse proxy (rebound to loopback-only after a CodeRabbit LAN-exposure finding on PR #105), `FIRE_API_KEY` required-by-default flip, MCP write-tool-absence test (caught and fixed a real violation: `set_price_target_alert` was writing to disk), branch/function coverage gap closed (branch 71.04%/functions 84.16%, up from 68.33%/75.67%)
- [ ] Full penetration-testing checklist — triaged; most items checkable in the sandboxed dev environment, but the Transport/TLS section and full network-isolation verification need a live deployment

**PROD Phase 4 — Feature Parity (Q4 2027)** — not started
- Portfolio rebalancing suggestions, tax-loss harvesting alerts, income/expense rolling trend, PWA, CD/FIRE-milestone notifications, optional multi-user mode

## Open P0/P1 Tasks

None. TASKS.md's only remaining explicitly-prioritized open item is P2: model real eBay marginal fee-bracket tiers in `calculateEbayFeesTotal` instead of a flat rate (flagged by CodeRabbit on PR #103; still open — needs a per-category fee-rule schema, not just the already-fixed $0.30/$0.40 order-fee threshold). The companion P2 item — the branch/function test-coverage gap (previously 68.33% branch vs. 70% target, 75.67% functions vs. 80% target) — closed this cycle: branch 71.04%, functions 84.16%, full suite 381/381 passing. Everything else open in TASKS.md/ROADMAP.md is untagged backlog (PROD Phase 2 `prices-provider.js` tests, PROD Phase 3 penetration-test checklist, Phase 4 items, tax drag engine, PWA).

## Blockers

None documented.

## Recent Changes (Unreleased)

- **MCP Server** (`app/mcp-server.mjs`) — grew from 8 to 12 functional tools (`fire_status_summary`, `get_net_worth`, `get_accounts`, `get_portfolio`, `get_cds`, `get_expenses`, `get_projection_settings`, `get_side_gig_income`, `get_wallets`, `get_concentration_risk`, `simulate_rebalance`, `get_emergency_runway`) plus 7 registered stubs; `.mcp.json` project config and `scripts/test-mcp.mjs` smoke test.
- **PROD Phase 1 UI completion (2026-09-10 cycle)** — eBay fee-rate validation against current published rates, eBay sync enable/disable toggle with last-sync timestamp, wallet manager UI (add/remove/balance display), vehicle "Refresh Value" button, Google Drive backup panel (trigger/list/restore); tests added for wallets, vehicle-api, and gdrive-backup routes.
- **Settings Page**, **Milestone Presets** (5 financial profiles), **Diversification Tips Redesign** (dismissible tiles), **Vehicle Estimate Overlay** styling, **eBay & Plaid Integration UI** (connection status + Plaid Link SDK).
- **Retirement projection drawdown fix** — portfolio now correctly withdraws `annualExpenses`/year post-retirement instead of continuing to accumulate; fixed a duplicate-return syntax error in the depletion-age calculation.
- Security: XSS `escHtml()` applied across all table renderers; CSRF `oauthState` consumed immediately post-verification; webhook HMAC requires `req.rawBody`; session cookies now `httpOnly`/`sameSite: lax` with a startup warning on weak/missing `SESSION_SECRET`.
- Hardening: atomic `db.json` writes (tmp file + rename), corrupt-vs-missing-file distinction in `readState`, Express global error handler, JSONata webhook mapping validated + time-boxed at 5s, Yahoo Finance fetches timeout at 10s.
- Fixed: `DELETE /api/accounts/:id` returned 444 instead of 404 for a missing account.
- Test suite grew past the 251-test/16-file baseline with new Plaid transaction-sync tests and targeted coverage-gap tests added this cycle (381/381 passing per the latest TASKS.md note); coverage now clears all four thresholds — statements 86.01%, lines 85.6%, branch 71.04%, functions 84.16% (branch/functions up from 68.33%/75.67%; METRICS.md itself hasn't been re-run since 2026-08-28, so its table still shows the old numbers).

## Verified Runbook (PMO 2026-09-24)

> Commands verified during the 2026-09-24 PMO audit (`agent/reports/pmo-audit-2026-09-24.md` §7). **obn-review: keep this section when refreshing the summary.**

- `docker build --target test -t fire-test . && docker run --rm -u root fire-test npm run test:coverage`
- `-u root` is needed until the Dockerfile `chown` fix lands: `WORKDIR /app` is owned by root, then `USER node`, which gives EACCES on `/app/coverage`.
- CI runs `npm test`, not coverage, so a branch-coverage threshold failure (68.68% < 70%) is invisible in CI.
