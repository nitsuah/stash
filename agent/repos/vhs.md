# vhs

> Reviewed: 2026-09-23

## Overview

Personal VHS collection indexer — catalogs a VHS tape collection with AI-assisted metadata (Claude Vision or Ollama llava:7b fallback), eBay valuation lookups, barcode scanning, and a web UI. Node.js/Express + PostgreSQL (Neon) backend, containerized with Docker (primary) or deployable as a Netlify Function (alternative, `serverless-http`). Optional Google OAuth for multi-user/sharing; single-user mode with no login wall by default. Jest unit tests (85.4% whole-tree line coverage) + Playwright E2E tests, with CI (Hadolint, Shellcheck, HTMLHint, ESLint, dep-install check, Docker build smoke test).

## Current Goals / Roadmap Focus

**Phase 1 — Capture:** ✅ Complete — PostgreSQL-backed registry with immutable `VHS-XXXX` IDs, barcode scanning, AI photo scanning (Ollama/Claude), OMDb verification, StacksUp spine enrichment, mobile UI, unit + E2E tests.

**Phase 2 — Valuation:** ⚠️ Partial — eBay Browse API valuation shipped (`src/modules/ebay.js`, `GET /api/valuate`, `POST /api/tapes/:id/valuate`), but the Browse API only returns **active-listing asking prices**, not realized sale prices (its `soldItemsOnly` filter is unsupported). Source is honestly labeled `ebay-browse` / `basis: "active-asking"`. True sold-price data needs eBay's separate Marketplace Insights API (own application/approval required) — tracked as a new task, not yet started.

**Phase 3 — Use the data:** ✅ Complete — CSV/JSON export+import, print price tags, printable HTML list, public collection sharing (`/c/<uuid>`), and a "Sell Drafts" (eBay/Mercari) per-tape listing-draft export shipped 2026-09.

**2027 — Computer vision & performance (triaged out, deferred):** multi-tape detection from batch photos (OpenCV), auto-crop tape thumbnails (depends on detection), GPU performance tuning for AI scanning (the `web-gpu` Docker Compose profile exists; needs real GPU hardware to benchmark/tune).

## Open P0/P1 Tasks

No P0 tasks. Open P1 items (TASKS.md P1 section):

- [ ] **P1** GPU performance optimization for AI scanning — infra hook (`web-gpu` Compose profile) exists; remaining work needs real GPU hardware — deferred to 2027
- [ ] **P1** Multi-tape detection (OpenCV) — real computer-vision work, not tractable in a docs/hardening pass — deferred to 2027
- [x] Multi-photo batch support — already substantially shipped (native multi-select, staged queue, per-item progress); remaining gap is cosmetic

Other genuinely open items (no formal priority in TASKS.md, but worth tracking):
- [ ] True sold-price valuation via eBay Marketplace Insights API (Coverage & Testing section — feature work, needs a separate eBay API application)
- [ ] Tech debt: delete orphaned `src/modules/routes/jobs.js` / `routes/lookup.js` (confirmed unused, zero references)
- [ ] **P2** Auto-crop tape thumbnails — deferred to 2027 (depends on multi-tape detection)

Closed since last review (both fixed 2026-09-11, per `docs/TASKS.md`): the `/api/logs/stream` vs `/api/logs` path mismatch (client now opens `/api/logs`, matching the server's SSE route) and the dead mobile export menu wiring (missing `#hbr-drawer` markup added so the already-written handlers/CSS have elements to bind to).

## Blockers

None documented for shipped functionality. Sold-price valuation (Phase 2 completion) is externally blocked pending eBay Marketplace Insights API application/approval — lead time unknown.

## Recent Changes

**Latest pass — "2026 roadmap completion + docs refresh" (Unreleased):**
- Fixed `worker.js` `OLLAMA` ReferenceError that silently aborted the AI scan pipeline on every pending job (caught by outer try/catch, logged only as generic "Worker error") — found via new test coverage, not manual QA
- Raw `err.message` no longer leaked to API clients — `tapes.js`, `jobs.js`, `server.js`, `valuate.js` now route through a shared `serverError()` helper
- `/api/logs` gated with `requireAuth`; Dockerfile now copies `jest.config.js` so Docker-measured and config-gated coverage agree
- Removed dead code in `routes/system.js` (unused `healthHandler`/`caCertHandler`)
- Added **Sell Drafts (eBay/Mercari) export** — copy-ready title/description/price/tags per `for_sale` tape
- Test coverage jumped to **85.4%** whole-tree lines (231 tests, 8 suites) — `worker.js` and `auth.js` went from 44%/34% to 100%
- `docs/TASKS.md` Tech Debt items re-verified against source; several previously-open items were already fixed on `main` and closed without rework
- Added a 2027 section to `docs/ROADMAP.md` for CV/GPU-heavy work triaged out of this pass

**Security-and-auth-hardening (PR #41):**
- Google OAuth CSRF state validation, `JWT_SECRET` startup guard, migration 006 (drops `UNIQUE` on `users.email`), write-gate UI (Add/Import hidden when logged out), drawer closes on backdrop click/Escape, SSE connection cleanup, object URL cleanup

**Tech-debt/coderabbit fixes (PR #40):**
- XSS escaping in wall-view print exports and card rendering; Ollama proxy POST body fix; SPA catch-all rate limiting; bulk-delete count fix; long-press crop target fix; JSON export/import round-trip completeness (`value_low`/`value_high`/`imdb_id`/photo fields)

**feat/vhs-scanner-v2 (now largely shipped):**
- Neon PostgreSQL backend (Node.js/Express replacing nginx), capture queue, barcode scanner with multi-pass preprocessing, full CRUD, batch AI metadata fill, bulk selection, full-text search/filter/sort, wall view, CSV/JSON export/import, print tags, mobile responsive layout, IndexedDB migration, CI pipeline

<!-- vault-links:start -->
## Vault links

_Generated by `scripts/build-vault-indexes.py`; edits inside this block are overwritten._

- Docs: [[repos/vhs/README|README]] (every doc hangs off its Docs Index)
- Overview: [[projects/KB/vhs-overview|KB overview]]
- Latest LOC report: [[reports/eng-loc-vhs-2026-07-29|2026-07-29]] (older ones chain from it)
- Latest MINI report: [[reports/eng-mini-vhs-2026-06-29|2026-06-29]] (older ones chain from it)
<!-- vault-links:end -->
