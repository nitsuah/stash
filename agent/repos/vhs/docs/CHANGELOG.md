# Changelog

All notable changes to this project are documented here.

## [Unreleased] — 2026 roadmap completion + docs refresh

### Fixed

- **`worker.js` `OLLAMA` ReferenceError** — a log line referenced an undefined `OLLAMA` variable, throwing on every pending job and silently aborting the AI scan pipeline before it ever called Ollama (caught by the outer try/catch, logged only as a generic "Worker error"). Found via new test coverage, not by manual QA — the failure mode left no obvious symptom besides scans never completing.
- **Raw `err.message` leaked to API clients** — `tapes.js`, `jobs.js`, `server.js`, and the two remaining DB paths in `valuate.js` returned PostgreSQL error text directly to callers. All now go through a shared `serverError()` helper (`src/modules/http-errors.js`) that logs server-side and returns a fixed message.
- **`/api/logs` unauthenticated** — gated with `requireAuth` (no-op in single-user mode).
- **Docker/config coverage mismatch** — Dockerfile now copies `jest.config.js`, so `docker run … npx jest --coverage` honors `collectCoverageFrom`/`coverageThreshold` instead of silently measuring the whole tree ungated.

### Removed

- **Dead code in `routes/system.js`** — `healthHandler`/`caCertHandler` were unused duplicates of `routes/health.js` and the inline `/api/ca-cert` handler in `server.js`.

### Added

- **Sell Drafts (eBay/Mercari) export** — one-command draft template generator for `for_sale` tapes; copy-ready title, condition-aware description, suggested price, tags, and notes per tape.
- `tests/worker.test.js`, `tests/auth.test.js` — previously untested modules (44%/34% line coverage) now at 100%.

### Docs

- Corrected several `docs/TASKS.md` Tech Debt items that were already fixed on `main` but never marked done (state.js setters, circular imports, crop-overlay.js ESM, list-view.js listeners/imports, wall-view.js selection styling, string-utils.js tag stripping) — re-verified against current source rather than re-implemented.
- Flagged two new findings for follow-up: orphaned `routes/jobs.js`/`routes/lookup.js` (never `require()`d — excluded from coverage scope, not yet deleted), and an `/api/logs/stream` vs. `/api/logs` client/server path mismatch.
- Added a `2027` section to `docs/ROADMAP.md` for CV/GPU-heavy work (multi-tape detection, auto-crop thumbnails, GPU performance tuning) triaged out of this pass as needing real model/hardware work.
- `docs/METRICS.md` rewritten with freshly measured numbers (85.4% whole-tree line coverage, 231 tests, 8 suites) rather than carried-forward figures.

---

## [Unreleased] — security-and-auth-hardening (PR #41)

### Added

- **Google OAuth CSRF state validation** — `randomUUID()` state cookie generated on `/auth/google`, verified in callback; mismatches redirect to `/?auth=error`
- **JWT_SECRET startup guard** — server refuses to start when auth is enabled but `JWT_SECRET` is empty
- **Migration 006** — drops the `UNIQUE` constraint on `users.email`; prevents login failure when two Google accounts share the same email address
- **Shared `flashInvRow`** — moved from duplicate per-module copies into `utils.js`
- **SSE connection close** — log panel ✕ button now closes the EventSource connection to prevent a resource leak
- **Object URL cleanup** — `dl()` in `utils.js` revokes the blob URL after 100 ms via `setTimeout`
- **Write-gate UI** — Add and Import buttons are hidden when auth is enabled but the user is not logged in; restored on sign-in
- **Drawer: backdrop click + Escape** — hamburger drawer now closes on backdrop click (exposed `closeDrawer` on `window`) and via the Escape key

### Fixed

- **`nextId()` overflow** — old regex `/^VHS-\d{4}$/` excluded IDs ≥ VHS-10000, causing `Math.max(...[])` = `-Infinity`; fixed with `/^VHS-(\d+)$/` and `ids.length ? Math.max(...ids) : 0` fallback
- **`toggle()` non-OK response** — share toggle now checks `r.ok` and reverts the optimistic UI update on server error
- **CSV formula injection** — `csvCell()` helper prefixes values starting with `=`, `+`, `-`, `@` with a tab character
- **`escHtml` single quotes** — added `&#39;` replacement so attribute injection via `'` is blocked
- **`tapesDeleteHandler` 404** — returns 404 instead of 200 when `rowCount === 0` (tape not found)
- **OAuth redirect validation** — `PUT /api/auth/share` now rejects non-boolean `collection_public` with 400
- **ESLint false positives** — added `tests_playwright/**` override with `browser: true` env and explicit globals

### Security (CodeQL)

- Added inline `// codeql[js/clear-text-storage-of-sensitive-data]` suppression on `setAuthCookie` — JWT is in an HttpOnly cookie, not plaintext
- Added inline `// codeql[js/missing-csrf-middleware]` — SameSite=lax on `vhs_token` provides CSRF protection
- Added inline `// codeql[js/missing-rate-limiting]` — all routes carry per-route limiters

---

## [Unreleased] — tech-debt/coderabbit-pr36-fixes (PR #40)

### Fixed

#### Security

- **XSS in wall-view print exports** — all inventory-derived fields (`id`, `title`, `year`, `label`, `condition`, `value_low`, `value_high`, `tags`) are now HTML-escaped before interpolation into `document.write` print windows (`exp-print`, `exp-tags`)
- **XSS in wall-view card rendering** — `data-id` and `src` attributes now pass through `esc()` before injection into `innerHTML` in all three wall modes (cover, spine, stack)
- **Ollama proxy POST body** — added `fixRequestBody` to the proxy `on.proxyReq` hook (http-proxy-middleware v2 API) so POST bodies consumed by `express.json()` are correctly forwarded to Ollama
- **SPA catch-all rate limit** — registered `app.use('/', limiter)` before the static, proxy, and SPA catch-all routes so all handlers share a single rate-limit pass with no double-counting

#### Data integrity

- **Bulk-delete count** — saved `ids.size` before `getSelectedIds().clear()` so the toast reports the actual number deleted instead of always 0
- **Long-press crop target** — `_lpStart` now calls `setSelectedId(_lpId)` before `openCropOverlay('face')` so the crop is applied to the long-pressed row
- **`isNewTape` state bypass** — Escape-key detail-close handler now calls `setIsNewTape(false)` (module setter) instead of writing `window.isNewTape = false` directly
- **Retry handler HTTP status** — retry button now checks `response.ok` before advancing card to `'processing'`; non-2xx responses fall through to the existing catch/toast path
- **JSON export/import round-trip** — JSON export now includes `value_low`, `value_high`, `imdb_id`, `photos`, `photo_thumbnail`, `photo_face`, `photo_spine`, `photo_crop`; import rec now preserves `imdb_id` and `photo_crop`

#### Tests

- **`normalizeTitleForLookup` regression suite** — added 12 Jest test cases (14 assertions) covering every `STANDALONE_EXCLUDE` term (`movie`, `film`, `title`, `video`, `tape`) for both standalone-preserve and parenthesized-strip behavior

---

## [Unreleased] — feat/vhs-scanner-v2

### Added

#### Storage & Backend

- **Neon PostgreSQL backend** — Node.js/Express server replaces nginx; REST CRUD at `/api/tapes`; Ollama proxy at `/api/ollama`; auto-creates schema on startup
- **DB health dot** — live green/red indicator next to tape count; red dot retries connection on click
- **Photo compression** — `compressImage()` resizes to max 1200px at JPEG 0.75 before storing in Neon JSONB

#### Capture & Scanning

- **Capture queue** — Space stages webcam frames as thumbnails; Enter sends all to AI at once
- **Barcode scanner** — multi-pass canvas preprocessing (grayscale/contrast, adaptive threshold, sharpen+threshold), ZXing `TRY_HARDER`, HD 1920×1080 stream request, tight horizontal targeting band
- **Torch toggle** — manual flashlight control when device supports it
- **Snap button** — single-frame decode for barcode or photo
- **UPC/barcode database lookup** — UPCitemdb.com auto-fills title on barcode scan

#### Collection Management

- **Quick-add tape** — `+ Add` button / `N` keyboard shortcut; blank form with next VHS-XXXX ID; no photo required
- **Full CRUD** — create, edit, delete with confirm dialog; multi-photo per tape
- **Batch AI metadata fill** — ⚡ Fill Data auto-fills year, label, and estimated value for incomplete tapes via Claude or Ollama
- **Bulk selection** — checkbox multi-select, bulk status change, bulk delete
- **Wanted status** — track tapes you're searching for
- **Sold price tracking** — record actual sale price alongside estimate
- **Tags / genres** — preset genre chips (Horror, SOV, Anime, etc.) plus custom tags

#### Discovery & Filtering

- **Full-text search** — searches title, label, barcode, notes, and tags simultaneously
- **Clickable stats bar** — status and condition chips filter inventory on click
- **Filter bar** — by status, condition, label, tag, year range
- **Sort** — by date, title, value (↑/↓), condition (best→worst, worst→best), ID
- **Sort persistence** — chosen sort saved to localStorage
- **Wall view** — masonry grid of tape thumbnails; clicking opens detail
- **Thumbnails in list view** — 48×34px thumbnail on every list row

#### Exports & Imports

- **CSV export** — full collection with all fields
- **For-sale CSV** — filtered export with eBay condition labels
- **JSON export/import** — full round-trip backup including photos
- **CSV import** — accepts the app's own export format or manual spreadsheets
- **Print price tags** — printable 2.4" dashed-border tags for for-sale tapes
- **Printable HTML list** — clean table sorted by ID with Print button

#### Mobile & Responsive

- **Responsive layout** — `@media (max-width:700px)` stacks panels vertically; camera fixed 280px (160px landscape)
- **Rear camera preference** — `facingMode: 'environment'` on mobile for scanning VHS tapes
- **Permission UX** — contextual `#no-cam-msg` (denied / not found / no API); "📷 Enable Camera" retry button
- **Touch events on crop box** — `touchstart/touchmove/touchend` mirrors mouse drag/resize so crop works on mobile

#### UX

- **Better empty state** — action buttons (Capture / Add Manually / Upload) on first run
- **eBay sold-listings search** — one-click search for comps on any tape
- **🔍 Lookup button** — AI-fills year, label, format, and value from title
- **Duplicate detection** — warns on similar titles when confirming a card
- **IndexedDB migration** — Settings → import any data from the old browser-local version
- **Keyboard shortcuts** — `Space` stage, `Enter` analyze, `N` add tape, `?` help, `Esc` close

#### CI

- Hadolint Dockerfile linting
- Shellcheck for shell scripts
- HTMLHint for `index.html`
- `npm ci --omit=dev` dep-install check
- Docker build smoke test

---

## [0.1.0] — Initial release (main branch)

- Initial tape registry (`data/tapes.json`) with immutable ID scheme (`VHS-XXXX`)
- Project README with data model, repo structure, and design decisions
