# VHS Collection Indexer — Features

Status guide: `[shipped]` is available now, `[planned]` is backlog work.

## Browser App

- `[shipped]` **VHS Shelf Scanner** — web UI served via Docker/Express (`src/server.js`, `public/`) or Netlify Functions (`netlify/functions/server.js`)
- `[shipped]` **Mobile UI** — responsive layout, rear-camera preference, touch crop support
- `[shipped]` **HTTPS / Mobile Support** — auto-generated self-signed TLS cert for LAN camera access
- `[shipped]` **Zoom Slider** — adjustable zoom for photo capture
- `[shipped]` **Hamburger Drawer** — collapsible mobile menu; closes on backdrop click or Escape

## Auth & Sharing

- `[shipped]` **Google OAuth** — optional sign-in; leave `GOOGLE_CLIENT_ID` blank for single-user mode
- `[shipped]` **Public Collection Sharing** — toggle a shareable `/c/<uuid>` URL per user
- `[shipped]` **Write-gate UI** — Add/Import buttons hidden when auth is on and user is not logged in
- `[shipped]` **Legacy tape migration** — `LEGACY_OWNER_EMAIL` claims un-owned tapes on first login

## Scanning

- `[shipped]` **Barcode Scanning** — webcam-based barcode scanning with auto-confirm and staging flow
- `[shipped]` **AI Photo Scanning** — batch photo upload; uses Claude Vision API when `ANTHROPIC_API_KEY` is set, otherwise falls back to Ollama (llava:7b) via server-side job queue
- `[shipped]` **Capture Queue** — Space stages frames; Enter sends all to AI at once
- `[shipped]` **UPC Lookup** — UPCitemdb.com auto-fills title on barcode scan

## Data & Registry

- `[shipped]` **Tape Registry** — PostgreSQL backend with immutable `VHS-XXXX` IDs
- `[shipped]` **Status Tracking** — `in_collection`, `for_sale`, `sold`, `donated`, `missing`, `wanted`
- `[shipped]` **Condition Tracking** — `great`, `good`, `fair`, `poor` with free-text notes
- `[shipped]` **Sold Price Tracking** — actual sale price alongside estimate
- `[shipped]` **Tags / Genres** — preset genre chips (Horror, SOV, Anime, etc.) plus custom tags

## UI & Editing

- `[shipped]` **Tabbed Edit Form** — multi-tab detail editor (main, photos, notes)
- `[shipped]` **Bulk Selection** — checkbox multi-select, bulk status change, bulk delete
- `[shipped]` **Wall View** — masonry grid of tape thumbnails; clicking opens detail
- `[shipped]` **Full-text Search** — title, label, barcode, notes, tags simultaneously
- `[shipped]` **Filter Bar** — by status, condition, label, tag, year range
- `[shipped]` **Sort** — by date, title, value, condition, ID; persists via localStorage
- `[shipped]` **Clickable Stats Bar** — status/condition chips filter inventory on click

## Enrichment & Verification

- `[shipped]` **StacksUp Integration** — spine rotation enrichment
- `[shipped]` **OMDb Verification** — AI scan results cross-checked against movie database
- `[shipped]` **Batch AI Metadata Fill** — ⚡ Fill button auto-fills year, label, value for incomplete tapes
- `[shipped]` **Analytics** — basic collection analytics

## Exports & Imports

- `[shipped]` **CSV Export** — full collection with all fields; formula-injection safe
- `[shipped]` **For-Sale CSV** — filtered export with eBay condition labels
- `[shipped]` **Sell Drafts (eBay/Mercari)** — one-command draft template generator for `for_sale` tapes: copy-ready title, condition-aware description, suggested price, tags, and notes per tape, with a one-click "Copy listing text" button
- `[shipped]` **JSON Export / Import** — full round-trip backup including photos
- `[shipped]` **CSV Import** — accepts app export format or manual spreadsheets
- `[shipped]` **Print Price Tags** — printable 2.4" dashed-border tags for `for_sale` tapes
- `[shipped]` **Printable HTML List** — clean table sorted by ID with Print button

## Fun

- `[shipped]` **Easter Eggs** — Akira MP3 + negative buzz sound on failed barcode scans

## Quality

- `[shipped]` **Jest Unit Tests** — server-side logic; 8 test files; ≥ 85% whole-tree line coverage (`src/server.js` + `src/modules/**`, see `docs/METRICS.md`)
- `[shipped]` **Playwright E2E Tests** — full coverage of all major features and modals
- `[shipped]` **CI** — Hadolint, Shellcheck, HTMLHint, ESLint, `node --check` syntax check, `npm ci --omit=dev` dep check, Jest unit tests, Docker build smoke test

## Enrichment

- `[shipped]` **eBay Valuation** — 🛒 eBay button in the detail modal estimates low/high/avg from eBay Browse API listings and stores the result on the tape (`source: "ebay-browse"`). **Asking prices from active listings, not sold prices** — true sold data needs the Marketplace Insights API (tracked in TASKS.md)

## Planned

- `[planned]` **Sold-price valuation** — eBay Marketplace Insights API for realized sale prices rather than asking prices
- `[planned — 2027]` **Multi-tape detection** — detect and crop individual tapes from batch photos (OpenCV); see `docs/ROADMAP.md`
- `[planned — 2027]` **Auto-crop thumbnails for wall view** — depends on multi-tape detection above; see `docs/ROADMAP.md`
- `[planned — 2027]` **GPU performance tuning for AI scanning** — the `web-gpu` Docker Compose profile exists; benchmarking and model/prompt tuning against real GPU hardware is the remaining work; see `docs/ROADMAP.md`
