# Changelog

All notable changes to this project are documented here.

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
