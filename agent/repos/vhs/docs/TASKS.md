# Tasks

Last Updated: 2026-09-02

## Todo

### Coverage & Testing

- [ ] **True sold-price valuation (eBay Marketplace Insights)** — the shipped valuation uses the Browse API, which returns **active listings (asking prices), not realized sale prices**; asking prices skew high. The Browse API has no supported sold/completed-item filter (an earlier draft sent `soldItemsOnly:true`, which eBay does not honour). Real sold data needs the Marketplace Insights API, which requires a separate eBay application and approval. Until then the source label is `ebay-browse` / `basis: active-asking` and the UI says "asking". When Insights access lands, add a new source label rather than redefining this one. (Feature work, not a testing gap — miscategorized here historically; see `docs/ROADMAP.md` Future ideas.)

### Tech Debt / Cleanup

- [ ] **Delete orphaned `src/modules/routes/jobs.js` and `routes/lookup.js`** — confirmed unused: `server.js` implements `/api/jobs*` and `/api/lookup*` inline and never `require()`s either file (verified 2026-09-02: zero references anywhere in `src/` or `tests/`). Currently excluded from `jest.config.js` `collectCoverageFrom` with a comment rather than deleted, to keep the 2026-09 cleanup PR reviewable. Delete both files in a follow-up, or wire `server.js` to use them instead of the inline duplicates (bigger refactor, same net effect).
- [x] **`/api/logs/stream` vs `/api/logs` mismatch** — fixed 2026-09-11: `public/js/ui.js` now opens `new EventSource('/api/logs')`, matching the server's single `app.get('/api/logs', ...)` route (`src/server.js`), which already branches on the `Accept: text/event-stream` header that `EventSource` sends automatically. The live log panel now receives real SSE events instead of silently hitting the SPA catch-all.
- [x] **Mobile export menu wiring is dead** — fixed 2026-09-11: added the missing "Data" section to the `#hbr-drawer` markup in `public/index.html` (`btn-add-tape-mob`, `btn-fill-data-mob`, `btn-revalidate-mob`, `btn-import-mob`, `btn-export-mob`, and the `exp-dd-mob` sub-menu with `exp-json-mob`/`exp-csv-mob`/`exp-sell-mob`/`exp-drafts-mob`/`exp-print-mob`) so the already-written click-through handlers in `public/js/ui.js` and the already-written `#hbr-drawer .exp-dd` CSS have elements to bind to. Also added the two new `-mob` ids to the AI-availability visibility toggle in `public/js/ai.js` so Fill/Check hide together with their desktop counterparts, and added `exp-drafts-mob` to the `ui.js` forEach for full parity with the desktop dropdown.

### Already fixed (verified 2026-09-02, previously mismarked as open)

The following items were carried in this file as open Tech Debt but were found, on inspection, to already be resolved on `main`. Re-verified against the current source rather than re-implemented:

- ~~state.js read-only exported bindings~~ — `public/js/state.js` already exports `setCards`/`setCaptureQueue`/`setUidSeq`/`nextUidSeq`, and both `review.js` and `capture.js` already call the setters instead of reassigning the bindings directly.
- ~~Circular self-imports in review.js/ui.js~~ — neither file imports from itself; `review.js` imports state from `state.js`, `ui.js` imports UI helpers from `review.js` (a legitimate one-directional dependency, not a cycle).
- ~~crop-overlay.js CommonJS `require()`~~ — the file is pure ESM (`import`/`export`); no `require()` calls exist anywhere under `public/js/`.
- ~~list-view.js stale `window` listeners~~ — the long-press mouse/touch listeners are already registered once at module scope (see the comment at the top of `list-view.js`), not per-row.
- ~~list-view.js missing imports~~ — `setSelectedId`, `setIsNewTape`, `openCropOverlay`, `renderDetailPhotos` are all imported; `updateBulkBar` is defined locally in the same file and needs no import.
- ~~wall-view.js missing selected-state styling~~ — all three wall render branches (StacksUp/spine/cover) already apply a `sel` class from `selectedId`, mirroring `list-view.js`.
- ~~string-utils.js over-aggressive tag stripping~~ — `STANDALONE_EXCLUDE` already keeps `movie`/`film`/`title`/`video`/`tape` out of standalone stripping; the PR #40 regression suite covers it.

## P1

- [x] **Multi-photo batch support** — already substantially shipped: `public/js/capture.js` accepts multiple files via `fileInput` (native multi-select), stages them in `captureQueue`, and `processQueue()` analyzes each one in sequence with per-item progress (`Analyzing image N of M…`) and individual review cards. The remaining gap vs. the original wording ("collapsible form cards") is cosmetic — the review panel renders a table, not accordion cards — and is not worth a rewrite of a working flow.
- [ ] **GPU performance optimization for AI scanning** — `config/docker-compose.yml` already has a `web-gpu` profile for pointing at a native GPU-accelerated Ollama (DirectML/CUDA) instead of the CPU container. Remaining work (model/prompt tuning, throughput benchmarking under real GPU load) needs actual GPU hardware to measure — deferred to **2027** (see `docs/ROADMAP.md`).
- [ ] **Multi-tape detection** — detect and crop individual tapes from a single batch photo (OpenCV). Real computer-vision work, not tractable as part of a docs/hardening pass — deferred to **2027** (see `docs/ROADMAP.md`).

## P2

- [x] **Sell queue export** — shipped 2026-09: "Sell Drafts (eBay/Mercari)" export button generates a printable/copyable draft per `for_sale` tape (title, condition-aware description, suggested price, tags, notes) with a one-click "Copy listing text" per card. See `buildSellDraft()` in `public/js/ui.js`.
- [ ] **Auto-crop tape thumbnails** — per-tape crop from a batch photo (OpenCV/ImageMagick). Real computer-vision work — deferred to **2027** (see `docs/ROADMAP.md`).

## Done (2026-09-02 security/coverage/docs pass)

- [x] **Stopped leaking raw `err.message` to API clients** — `tapes.js`, `jobs.js`, `server.js`, and the two remaining DB paths in `valuate.js` now use a shared `src/modules/http-errors.js#serverError()` helper: logs the real error server-side, returns a fixed `{"error":"internal server error"}` to the client.
- [x] **`/api/logs` gated with `requireAuth`** — no-op in single-user mode (default); blocks anonymous access to scan/review detail once Google OAuth is configured.
- [x] **Dockerfile copies `jest.config.js`** — `docker run … npx jest --coverage` and the config-backed `npx jest --coverage` now measure the identical thing (previously 71.94% vs. 74.88% — see `docs/METRICS.md`).
- [x] **Extended coverage to `src/modules/*`** — `collectCoverageFrom` now covers `src/server.js` + `src/modules/**/*.js` (excluding the two confirmed-orphaned route files, see Tech Debt above).
- [x] **Restored line coverage well above 75%** — whole-tree, Docker-measured, config-honored: **85.4% lines** (was 71.94% on the same basis pre-fix). `worker.js` and `auth.js` — the two biggest gaps (44%/34%) — are now at 100% via new `tests/worker.test.js` / `tests/auth.test.js`. `system.js` reached 100% after removing dead code (see below) rather than by adding tests to it.
- [x] **Fixed a real production bug found via new test coverage** — `src/modules/worker.js` referenced an undefined `OLLAMA` variable in a log line, throwing on every pending job and aborting the scan pipeline (caught silently by the outer try/catch) before it ever called Ollama. The AI photo-scanning worker has been non-functional until this fix.
- [x] **Removed dead code from `routes/system.js`** — `healthHandler`/`caCertHandler` were unused duplicates of `routes/health.js` and the inline `/api/ca-cert` handler in `server.js`; only `registerStaticAndProxy` was ever imported.
- [x] **eBay listing valuation (Phase 2)** — `src/modules/ebay.js` (OAuth client-credentials + cached app token, Browse API search, low/high/avg aggregation), `src/modules/routes/valuate.js` (`GET /api/valuate` preview, `POST /api/tapes/:id/valuate` valuate-and-store with `source: "ebay-browse"`), and the previously dead `#d-ebay` button in the detail modal is now wired. **These are asking prices from active listings, not sold prices** — see the follow-up task above.
- [x] **SPA catch-all rate limit** — registered `app.use('/', limiter)` before static/proxy/SPA handlers (PR #40)
- [x] **CSV export / JSON export / print** — shipped in web UI (no Python scripts needed)
- [x] **Google OAuth + multi-user** — optional auth, public sharing via `/c/<uuid>` (PR #38)
- [x] **E2E Playwright test suite** — full coverage of all features and modals (PR #41)
- [x] **Security fixes** — XSS escaping, CSRF state validation, object URL cleanup, SSE leak, CSV formula injection (PR #40, PR #41)
