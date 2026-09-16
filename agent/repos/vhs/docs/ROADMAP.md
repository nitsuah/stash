# ROADMAP

## Phase 1 — Capture [COMPLETE]

**Goal:** get every tape into the database with a consistent ID and a title.

All Phase 1 goals shipped:

- PostgreSQL-backed tape registry with immutable `VHS-XXXX` IDs
- Barcode scanning — webcam-based with auto-confirm and staging flow
- AI photo scanning — batch upload, Ollama vision, accuracy checking
- Mobile UI — mobile-first layout, queue visualization, retry controls
- OMDb verification — AI scan results cross-checked against movie database
- StacksUp spine rotation enrichment
- Tabbed edit form and review queue
- Jest unit tests + Playwright E2E tests

---

## Phase 2 — Valuation [PARTIAL — shipped, not "sold" data]

**Goal:** attach a realistic price range to each tape.

### eBay listings

The most reliable signal for VHS value would be eBay "sold" listings, not asking prices — but that data isn't available yet (see below).

- **Manual:** search eBay, paste in estimated low/high, add `source: "manual"`
- **In-app eBay search:** the ⚡ Fill button / 🔍 Lookup button already opens eBay comps for any tape
- **Automated — shipped, but asking prices, not sold prices:** `src/modules/ebay.js` (OAuth client-credentials + cached app token) and `src/modules/routes/valuate.js` (`GET /api/valuate` preview, `POST /api/tapes/:id/valuate` valuate-and-store) call the eBay **Browse API** and aggregate low/high/avg from **active listings**. The Browse API's `soldItemsOnly` filter is silently unsupported — an earlier draft assumed it worked and mislabeled the result as sold-price data. Source is honestly labeled `ebay-browse` / `basis: "active-asking"` in the UI and stored data, not `ebay-sold`. True sold-price data requires eBay's separate Marketplace Insights API, which needs its own application and approval — see the new task below.

### Valuation tiers (rough guide)

| Value | What it usually means |
| --- | --- |
| $1–5 | Common mainstream releases, ex-rental |
| $5–20 | OOP titles, cult films, certain genres |
| $20–100 | Horror, SOV, anime, foreign, sealed |
| $100+ | Rare SOV, cult horror, sealed big titles |

**Tags to flag for closer research:** horror, SOV (shot-on-video), anime, foreign language, documentary, sealed/shrinkwrapped, small label (not Paramount/Warner/Disney)

---

## Phase 3 — Use the data [COMPLETE]

Once the index exists, you can do anything with it.

### Exports [COMPLETE]

All export formats are built into the web UI (no scripts needed):

- **CSV export** — full collection; click "Export CSV" in the collect toolbar
- **For-sale CSV** — filtered `for_sale` export with eBay condition labels
- **JSON export/import** — full round-trip backup including photos
- **Print price tags** — 2.4" printable tags for `for_sale` tapes
- **Printable HTML list** — clean table sorted by ID

### Sharing [COMPLETE]

- **Public collection URL** — toggle a shareable `/c/<uuid>` link via the Share panel
- The public page is read-only; it shows the collection without any edit controls

### Sell workflow [COMPLETE]

Set status to `for_sale` on tapes you want to move. Two export options:

- **For-sale CSV** — click "↓ Export" → "For Sale Export" for a spreadsheet with eBay condition labels
- **Sell Drafts** — click "↓ Export" → "Sell Drafts (eBay/Mercari)" for a per-tape, copy-ready listing draft (title, condition-aware description, suggested price, tags, notes) with a one-click "Copy listing text" button per card — shipped 2026-09

### Future ideas (don't build yet)

- Condition grading rubric (create a standard so anyone rating tapes uses the same scale)
- **eBay Marketplace Insights application** — new idea (2026-08-28): the current valuation is asking-price-based because the Browse API has no real sold-item filter. Marketplace Insights is a separate, limited-release API — different endpoint (`/item_sales/search`), different OAuth scope (`https://api.ebay.com/oauth/api_scope/buy` via client-credentials grant), and a different response schema (`SalesHistoryPagedCollection`/`ItemSales`) than the Browse API used today — so migrating is more than a source-label swap. Worth starting the developer application now since approval lead time is unknown, but scope the work as: new endpoint + OAuth scope, response mapping changes, sold-price semantics, any newly-persisted fields, and UI/export label updates.
- **Valuation confidence badge** — new idea (2026-08-28): since `basis: "active-asking"` is a real caveat users may not read closely, a small UI badge next to any displayed valuation ("asking price, not sold price") would surface the limitation at the point of decision rather than only in docs.

---

## 2027 — Computer vision & performance

Triaged out of the 2026-09 roadmap-completion pass: each item below needs real model work, GPU hardware, or benchmarking that doesn't fit a docs/hardening cycle. Kept as a separate section rather than folded into "Future ideas" because these are the *next* concrete phase once CV tooling is in place, not speculative.

- **Multi-tape detection** — detect and crop individual tapes from a single batch photo (OpenCV). Needs: an object-detection or contour-segmentation approach tuned for VHS spines/covers on a shelf, a labeled test set of real batch photos, and a decision on where inference runs (server-side Python sidecar vs. a JS-only approach like OpenCV.js). Blocks auto-crop thumbnails below, since that needs tape boundaries as an input.
- **Auto-crop tape thumbnails** — once multi-tape detection exists, crop each detected tape from the batch photo into its own thumbnail for wall view (OpenCV/ImageMagick). Not independently useful without the detection step above.
- **GPU performance optimization for AI scanning** — `config/docker-compose.yml` already has a `web-gpu` profile (point `OLLAMA_UPSTREAM` at a native GPU-accelerated Ollama instead of the CPU container) — the infra hook exists. What's left needs actual GPU hardware to do responsibly: benchmark `llava:7b` scan latency CPU vs. GPU, decide whether a smaller/quantized model trades acceptable accuracy for throughput, and tune `num_predict`/timeout values in `src/modules/config.js` and `ollama.js` against real numbers instead of guesses.

---

## Tech decisions

| Decision | Choice | Why |
| --- | --- | --- |
| Data format | PostgreSQL (Neon) | Handles concurrent writes, user-scoped queries, upserts cleanly |
| Version control | Git | Free history, easy backup, works on any machine |
| AI vision | Ollama (llava:7b) / Claude API | Good at messy/worn labels |
| Valuation data | eBay active listings (asking price) via Browse API | Best available signal today; true sold-price data is a future target pending Marketplace Insights API access (see roadmap idea below) |
| Backend | Node.js / Express | Same language as the frontend; lightweight |
| Exports | Built into web UI | No dependency on Python; works on any device |
| Hosting | Docker + Express | Consistent environment, mobile HTTPS support |
| Auth | Google OAuth (optional) | Single-user by default; no login wall unless you want one |

## Other

- Refer to README.md for setup, data model, and running instructions.
- Refer to docs/TASKS.md for next steps and immediate action items.
- Refer to docs/FEATURES.md for shipped vs planned feature status.
- Use Docker for a consistent development environment (see Dockerfile and config/docker-compose.yml).
