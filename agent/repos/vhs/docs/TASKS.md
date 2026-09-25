# Tasks

> 🧭 [vhs](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

## Todo

- [ ] **Review `scripts/audit-metadata.js` dry-run output against the real collection before any `--apply`** — PR #55 added the tool (dry-run by default, OMDb comparison, high-confidence-only corrections) but its own test plan left this unchecked: `--apply` was only ever dry-run against local test data because no `OMDB_API_KEY` was configured. Acceptance: a dry run over the ~500-title collection is reviewed by a human, then `--apply` is run (or specific corrections rejected with reasons).
- [ ] **Finish PR #55's remaining priorities** — P6 (mobile Easter eggs) and P7 (polish) were marked in progress on that branch when it merged; confirm what shipped and either close them out or re-scope.

## Ideas

- [ ] Add "randomizer" that auto picks a title from the collection.
- [ ] Add "watch" options in the "trailer" view with buttons to where the movie can be watched (this is a major feature to index and search where videos might be streaming or available online free to watch, tubi or youtube, vimeo, dailymotion, etc)

### Coverage & Testing

- [ ] **True sold-price valuation (eBay Marketplace Insights)** — the shipped valuation uses the Browse API, which returns **active listings (asking prices), not realized sale prices**; asking prices skew high. The Browse API has no supported sold/completed-item filter (an earlier draft sent `soldItemsOnly:true`, which eBay does not honour). Real sold data needs the Marketplace Insights API, which requires a separate eBay application and approval. Until then the source label is `ebay-browse` / `basis: active-asking` and the UI says "asking". When Insights access lands, add a new source label rather than redefining this one. (Feature work, not a testing gap — miscategorized here historically; see `docs/ROADMAP.md` Future ideas.)

### Tech Debt / Cleanup

- [ ] **Delete orphaned `src/modules/routes/jobs.js` and `routes/lookup.js`** — confirmed unused: `server.js` implements `/api/jobs*` and `/api/lookup*` inline and never `require()`s either file (verified 2026-09-02: zero references anywhere in `src/` or `tests/`). Currently excluded from `jest.config.js` `collectCoverageFrom` with a comment rather than deleted, to keep the 2026-09 cleanup PR reviewable. Delete both files in a follow-up, or wire `server.js` to use them instead of the inline duplicates (bigger refactor, same net effect).

## P1

- [ ] **GPU performance optimization for AI scanning** — `config/docker-compose.yml` already has a `web-gpu` profile for pointing at a native GPU-accelerated Ollama (DirectML/CUDA) instead of the CPU container. Remaining work (model/prompt tuning, throughput benchmarking under real GPU load) needs actual GPU hardware to measure — carried into **2027 Q1** (see `docs/ROADMAP.md`).
- [ ] **Multi-tape detection** — detect and crop individual tapes from a single batch photo (OpenCV). Real computer-vision work, not tractable as part of a docs/hardening pass — carried into **2027 Q1** (see `docs/ROADMAP.md`).

## P2

- [ ] **Auto-crop tape thumbnails** — per-tape crop from a batch photo (OpenCV/ImageMagick). Real computer-vision work — carried into **2027 Q1** (see `docs/ROADMAP.md`).

## Done

Condensed into `docs/FEATURES.md` (shipped
capabilities), and `docs/CHANGELOG.md` (change-by-change history, including the
later SSE-stream and mobile export-menu fixes from 2026-09-11) — see those
files rather than a duplicated narrative here.
