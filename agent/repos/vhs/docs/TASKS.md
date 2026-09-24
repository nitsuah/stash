# Tasks

Last Updated: 2026-09-23

## Todo

## Ideas

- [ ] Add "randomizer" that auto picks a title from the collection.
- [ ] Add "watch" options in the "trailer" view with buttons to where the movie can be watched (this is a major feature to index and search where videos might be streaming or available online free to watch, tubi or youtube, vimeo, dailymotion, etc)

### Coverage & Testing

- [ ] **True sold-price valuation (eBay Marketplace Insights)** — the shipped valuation uses the Browse API, which returns **active listings (asking prices), not realized sale prices**; asking prices skew high. The Browse API has no supported sold/completed-item filter (an earlier draft sent `soldItemsOnly:true`, which eBay does not honour). Real sold data needs the Marketplace Insights API, which requires a separate eBay application and approval. Until then the source label is `ebay-browse` / `basis: active-asking` and the UI says "asking". When Insights access lands, add a new source label rather than redefining this one. (Feature work, not a testing gap — miscategorized here historically; see `docs/ROADMAP.md` Future ideas.)

### Tech Debt / Cleanup

- [ ] **Delete orphaned `src/modules/routes/jobs.js` and `routes/lookup.js`** — confirmed unused: `server.js` implements `/api/jobs*` and `/api/lookup*` inline and never `require()`s either file (verified 2026-09-02: zero references anywhere in `src/` or `tests/`). Currently excluded from `jest.config.js` `collectCoverageFrom` with a comment rather than deleted, to keep the 2026-09 cleanup PR reviewable. Delete both files in a follow-up, or wire `server.js` to use them instead of the inline duplicates (bigger refactor, same net effect).
- [x] **`/api/logs/stream` vs `/api/logs` mismatch** — fixed 2026-09-11: `public/js/ui.js` now opens `new EventSource('/api/logs')`, matching the server's single `app.get('/api/logs', ...)` route (`src/server.js`), which already branches on the `Accept: text/event-stream` header that `EventSource` sends automatically. The live log panel now receives real SSE events instead of silently hitting the SPA catch-all.
- [x] **Mobile export menu wiring is dead** — fixed 2026-09-11: added the missing "Data" section to the `#hbr-drawer` markup in `public/index.html` (`btn-add-tape-mob`, `btn-fill-data-mob`, `btn-revalidate-mob`, `btn-import-mob`, `btn-export-mob`, and the `exp-dd-mob` sub-menu with `exp-json-mob`/`exp-csv-mob`/`exp-sell-mob`/`exp-drafts-mob`/`exp-print-mob`) so the already-written click-through handlers in `public/js/ui.js` and the already-written `#hbr-drawer .exp-dd` CSS have elements to bind to. Also added the two new `-mob` ids to the AI-availability visibility toggle in `public/js/ai.js` so Fill/Check hide together with their desktop counterparts, and added `exp-drafts-mob` to the `ui.js` forEach for full parity with the desktop dropdown.

## P1

- [ ] **GPU performance optimization for AI scanning** — `config/docker-compose.yml` already has a `web-gpu` profile for pointing at a native GPU-accelerated Ollama (DirectML/CUDA) instead of the CPU container. Remaining work (model/prompt tuning, throughput benchmarking under real GPU load) needs actual GPU hardware to measure — deferred to **2027** (see `docs/ROADMAP.md`).
- [ ] **Multi-tape detection** — detect and crop individual tapes from a single batch photo (OpenCV). Real computer-vision work, not tractable as part of a docs/hardening pass — deferred to **2027** (see `docs/ROADMAP.md`).

## P2

- [ ] **Auto-crop tape thumbnails** — per-tape crop from a batch photo (OpenCV/ImageMagick). Real computer-vision work — deferred to **2027** (see `docs/ROADMAP.md`).

## Done (2026-09-02 security/coverage/docs pass)

Condensed into `docs/ROADMAP.md` (phases/milestones), `docs/FEATURES.md` (shipped
capabilities), and `docs/CHANGELOG.md` (change-by-change history, including the
later SSE-stream and mobile export-menu fixes from 2026-09-11) — see those
files rather than a duplicated narrative here.
