---
up: "[[repos/vhs]]"
source: https://github.com/nitsuah/vhs/blob/main/docs/ROADMAP.md
kind: repo-doc
repo: vhs
---

# ROADMAP

> 🧭 [vhs](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

> 2027 planning reset (2026-09-24): Phase 1 (Capture — Postgres registry, barcode + AI photo scanning, OMDb
> verification, StacksUp enrichment, mobile UI, tests) and Phase 3 (Use the data — exports, public sharing, sell
> workflow incl. Sell Drafts) are complete and condensed in [FEATURES](./FEATURES.md) / [CHANGELOG](./CHANGELOG.md).
> Phase 2 (Valuation) shipped on eBay **asking** prices; its open work and the triaged computer-vision items were
> carried into 2027 Q1 below.

## 2027 Q1 - Real Valuation & Computer Vision (Planned)

### Phase 2 close-out — valuation *(carried from 2026)*

Shipped: `src/modules/ebay.js` + `src/modules/routes/valuate.js` call the eBay **Browse API** and store low/high/avg from **active listings**, honestly labeled `ebay-browse` / `basis: "active-asking"`. The Browse API's `soldItemsOnly` filter is silently unsupported, so true sold prices need Marketplace Insights.

- [ ] **eBay Marketplace Insights application** *(conditional: apply only once an eligible eBay access route is confirmed; the migration below happens in 2027 Q1 only if access is granted)* — the current valuation is asking-price-based because the Browse API has no real sold-item filter. Marketplace Insights is a separate, limited-release API — different endpoint (`/item_sales/search`), different OAuth scope (`https://api.ebay.com/oauth/api_scope/buy` via client-credentials grant), and a different response schema (`SalesHistoryPagedCollection`/`ItemSales`) than the Browse API used today — so migrating is more than a source-label swap. If access is granted, scope the work as: new endpoint + OAuth scope, response mapping changes, sold-price semantics, any newly-persisted fields, and UI/export label updates.
- [ ] **Valuation confidence badge** — since `basis: "active-asking"` is a real caveat users may not read closely, a small UI badge next to any displayed valuation ("asking price, not sold price") would surface the limitation at the point of decision rather than only in docs.
- [ ] **Condition grading rubric** — a standard scale so anyone rating tapes uses the same grades *(carried from Phase 3 "future ideas")*.

### Computer vision & performance *(needs scoping — triaged out of the 2026-09 pass; needs model work / GPU hardware)*

- [ ] **Multi-tape detection** — detect and crop individual tapes from a single batch photo (OpenCV). Needs: an object-detection or contour-segmentation approach tuned for VHS spines/covers on a shelf, a labeled test set of real batch photos, and a decision on where inference runs (server-side Python sidecar vs. a JS-only approach like OpenCV.js). Blocks auto-crop thumbnails below, since that needs tape boundaries as an input.
- [ ] **Auto-crop tape thumbnails** — once multi-tape detection exists, crop each detected tape from the batch photo into its own thumbnail for wall view (OpenCV/ImageMagick). Not independently useful without the detection step above.
- [ ] **GPU performance optimization for AI scanning** — `config/docker-compose.yml` already has a `web-gpu` profile (point `OLLAMA_UPSTREAM` at a native GPU-accelerated Ollama instead of the CPU container) — the infra hook exists. What's left needs actual GPU hardware to do responsibly: benchmark `llava:7b` scan latency CPU vs. GPU, decide whether a smaller/quantized model trades acceptable accuracy for throughput, and tune `num_predict`/timeout values in `src/modules/config.js` and `ollama.js` against real numbers instead of guesses.

---

## Reference

### Valuation tiers (rough guide)

| Value | What it usually means |
| --- | --- |
| $1–5 | Common mainstream releases, ex-rental |
| $5–20 | OOP titles, cult films, certain genres |
| $20–100 | Horror, SOV, anime, foreign, sealed |
| $100+ | Rare SOV, cult horror, sealed big titles |

**Tags to flag for closer research:** horror, SOV (shot-on-video), anime, foreign language, documentary, sealed/shrinkwrapped, small label (not Paramount/Warner/Disney)

---

## Tech decisions

| Decision | Choice | Why |
| --- | --- | --- |
| Data format | PostgreSQL (Neon) | Handles concurrent writes, user-scoped queries, upserts cleanly |
| Version control | Git | Free history, easy backup, works on any machine |
| AI vision | Ollama (llava:7b) / Claude API | Good at messy/worn labels |
| Valuation data | eBay active listings (asking price) via Browse API | Best available signal today; true sold-price data is a future target pending Marketplace Insights API access (see 2027 Q1 above) |
| Backend | Node.js / Express | Same language as the frontend; lightweight |
| Exports | Built into web UI | No dependency on Python; works on any device |
| Hosting | Docker + Express | Consistent environment, mobile HTTPS support |
| Auth | Google OAuth (optional) | Single-user by default; no login wall unless you want one |

## Other

- Refer to README.md for setup, data model, and running instructions.
- Refer to docs/TASKS.md for next steps and immediate action items.
- Refer to docs/FEATURES.md for shipped vs planned feature status.
- Use Docker for a consistent development environment (see Dockerfile and config/docker-compose.yml).
