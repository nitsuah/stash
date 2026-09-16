# VHS Collection Indexer

A personal tool to catalog a VHS collection — capturing what each tape is, what it might be worth, and building a record you can actually use (sell, store, share). Backed by PostgreSQL, served by Express, containerized with Docker.

## What's Shipped

### Core
- **VHS Shelf Scanner** — browser app (`public/`) served via Express (`src/server.js`)
- **Tape Registry** — PostgreSQL backend with immutable `VHS-XXXX` IDs; REST CRUD at `/api/tapes`
- **Status & Condition Tracking** — `in_collection`, `for_sale`, `sold`, `donated`, `missing`, `wanted`; `great/good/fair/poor` with notes
- **Full CRUD** — create, edit, delete with confirm dialog; multi-photo per tape

### Capture & Scanning
- **Barcode Scanning** — webcam-based barcode scanning with auto-confirm and staging flow
- **AI Photo Scanning** — batch upload, AI title recognition via Ollama (llava:7b) or Claude Vision API, accuracy checking
- **Capture Queue** — Space stages webcam frames; Enter sends all to AI at once
- **UPC Lookup** — UPCitemdb.com auto-fills title on barcode scan
- **Zoom Slider** — adjustable zoom for photo capture
- **Torch Toggle** — manual flashlight control when the device supports it

### Collection Management

- **Batch AI Metadata Fill** — ⚡ Fill button auto-fills year, label, and value for incomplete tapes
- **OMDb Verification** — cross-check AI scan results against the movie database
- **StacksUp Integration** — spine-rotation enrichment for wall/spine view
- **Tags / Genres** — preset genre chips (Horror, SOV, Anime, etc.) plus custom tags; auto-populated from OMDb via ⚡ Fill
- **Bulk Selection** — checkbox multi-select, bulk status change, bulk delete
- **Sold Price Tracking** — record actual sale price alongside estimate

### Discovery & Filtering
- **Full-text Search** — searches title, label, barcode, notes, and tags simultaneously
- **Filter Bar** — by status, condition, label, tag, year range
- **Sort** — by date, title, value, condition, ID; sort persists via localStorage
- **Wall View** — masonry grid of tape thumbnails; clicking opens detail
- **Clickable Stats Bar** — status/condition chips filter inventory on click

### Exports & Imports
- **CSV Export** — full collection with all fields; formula-injection safe
- **For-Sale CSV** — filtered export with eBay condition labels
- **Sell Drafts (eBay/Mercari)** — one-command draft template generator for `for_sale` tapes; copy-ready title, description, and suggested price per tape
- **JSON Export / Import** — full round-trip backup including photos
- **CSV Import** — accepts the app's own export format or manual spreadsheets
- **Print Price Tags** — printable 2.4" dashed-border tags for `for_sale` tapes
- **Printable HTML List** — clean table sorted by ID with Print button

### Auth & Sharing
- **Google OAuth** — optional; leave `GOOGLE_CLIENT_ID` blank to run as single-user
- **Public Collection Sharing** — toggle a shareable `/c/<uuid>` URL per user
- **Write-gate UI** — Add/Import buttons hidden when auth is enabled and user is not logged in

### Infrastructure
- **Mobile UI** — responsive layout, rear-camera preference, touch crop support
- **HTTPS / Mobile Support** — auto-generated self-signed TLS cert for LAN camera access
- **Hamburger Drawer** — collapsible mobile menu; closes on backdrop click or Escape key
- **CRT Scanlines Toggle** — overlay scanlines/vignette across the whole app (hamburger menu)
- **Playwright E2E Tests** — full coverage of all major features and modals
- **Jest Unit Tests** — server-side logic; 8 test files, ≥ 85% whole-tree line coverage (`src/server.js` + `src/modules/**`)
- **CI** — Hadolint, Shellcheck, HTMLHint, ESLint, `node --check` syntax, dep-install check, Jest unit tests, Docker build smoke test
- **Netlify Serverless** — Express app also deployable as a Netlify Function (`netlify/functions/server.js`, `serverless-http`)

---

## Running the app

```bash
cp .env.example .env   # fill in DATABASE_URL and HOST_IP at minimum
docker compose -f config/docker-compose.yml up -d --build
```

App at `http://localhost:8080` (or whatever `APP_PORT` you set in `.env`).
HTTPS at `https://localhost:8443`.

### Netlify deployment (alternative)

The Express app can also run as a Netlify Function. The `serverless-http` package wraps it as a Lambda-compatible handler. Static files are served from `public/`; all `/api/*` and `/auth/*` routes are proxied to the function via `netlify.toml`.

```bash
# Deploy via Netlify CLI
netlify deploy --prod
```

Migrations run automatically on each cold start (idempotent). Set the same `.env` variables (especially `DATABASE_URL`) as Netlify environment variables.

> **Note:** The Ollama proxy and local HTTPS cert generation are Docker-only features. The Netlify path assumes Claude Vision API (`ANTHROPIC_API_KEY`) for AI scanning.

### Auth (optional)

Auth is disabled by default — the app runs as a single-user tool with no login required.

To enable Google OAuth:

1. Create an OAuth 2.0 Client ID at [Google Cloud Console](https://console.cloud.google.com) → APIs & Services → Credentials
2. Add Authorized redirect URI: `http://localhost:8080/auth/google/callback` (or your `APP_BASE_URL`)
3. Set in `.env`:
   ```
   GOOGLE_CLIENT_ID=...
   GOOGLE_CLIENT_SECRET=...
   JWT_SECRET=<run: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))">
   APP_BASE_URL=http://localhost:8080
   ```
4. Restart the container. A "Sign in with Google" button appears in the top bar.

To migrate existing un-owned tapes to your Google account on first login:

```
LEGACY_OWNER_EMAIL=you@gmail.com
```

---

## Mobile / HTTPS setup

Mobile browsers block camera access on plain HTTP. The app auto-generates a self-signed TLS cert on first boot and serves it for easy installation.

**One-time setup per device:**

1. Set `HOST_IP=<your LAN IP>` in `.env` (e.g. `HOST_IP=192.168.1.171`)
2. Start the app: `docker compose -f config/docker-compose.yml up -d --build`
3. On your phone, open: `http://192.168.1.171:8080/ca.crt`
4. **Android:** tap the downloaded file → Install → name it "VHS Scanner" → OK
   **iOS:** tap Allow → Settings → General → VPN & Device Management → trust it
5. Use `https://192.168.1.171:8443` on your phone — camera will work

**If your IP changes:**

```bash
docker volume rm vhs_certs   # forces cert regeneration with new IP on next start
```

> **Note:** The cert is self-signed by a local CA that only your devices trust. Traffic never leaves your LAN. The cert lasts 10 years.

---

## Repo structure

```
vhs/
├── config/
│   └── docker-compose.yml
├── docs/                    ← CHANGELOG, FEATURES, ROADMAP, TASKS
├── migrations/              ← SQL schema migrations (run on startup)
├── public/                  ← browser app static files
│   └── js/                  ← ES-module frontend
│       └── modules/         ← sub-modules (list-view, wall-view, etc.)
├── src/
│   ├── server.js            ← Express entry point
│   └── modules/             ← auth, config, routes
├── tests/                   ← Jest unit tests
├── tests_playwright/        ← Playwright E2E tests
├── .env.example             ← copy to .env and fill in
└── Dockerfile
```

---

## Data model

Each tape is one row in the PostgreSQL `tapes` table. The row schema is:

| SQL Column | Type | Notes |
|---|---|---|
| `id` | `TEXT` | Immutable identifier (primary key); `VHS-XXXX` format when assigned at creation, or the scanned UPC barcode if a barcode is captured before the `VHS-XXXX` is assigned |
| `data` | `JSONB` | Full tape object — all metadata fields live here |
| `scanned_at` | `TEXT` | ISO timestamp; default sort key |
| `owner_id` | `TEXT` | Google account `sub`; NULL in single-user mode |

All tape metadata is stored inside the `data` JSONB column as a single document. Key fields within that document:

| Field | Notes |
|---|---|
| `id` | Mirrors the SQL `id`; `VHS-XXXX` or barcode UPC when valid |
| `title` | Required; search, sort, display, lookup key for Fill |
| `year` | OMDb authoritative source; fill target |
| `label` | VHS distributor/studio; e.g. `Paramount Home Video` |
| `format` | `VHS`, `DVD`, `Blu-ray`, etc. |
| `condition` | `great`, `good`, `fair`, `poor` |
| `condition_notes` | Free text; detail modal only |
| `status` | `in_collection`, `for_sale`, `sold`, `donated`, `missing`, `wanted` |
| `tags` | Array of genre/custom tag strings |
| `value_low` / `value_high` | USD resale estimate range |
| `sold_price` | Actual sale price (shown when `status = sold`) |
| `barcode` | UPC/EAN scan identifier; dedup guard |
| `imdb_id` | OMDb confidence gate for Fill |
| `photos` | Array of base64-encoded compressed images (max 1200px, JPEG 0.75) |
| `photo_thumbnail` | Auto-set on confirm; universal thumbnail fallback |
| `photo_face` | User-pinned in detail modal; cover-wall primary |
| `photo_spine` | User-pinned in detail modal; spine-wall primary |
| `notes` | Searchable free-text field |

Immutable IDs: once a tape gets a `VHS-XXXX` ID, it keeps it forever. If a barcode is scanned first and no `VHS-XXXX` exists yet, the UPC becomes the `id` if it is not already in use.

---

## Decisions made

- **PostgreSQL over flat JSON** — migrated from `tapes.json` when multi-user auth arrived. PostgreSQL via Neon handles concurrent writes, upserts, and user-scoped queries cleanly. The ID scheme (`VHS-XXXX`) is still immutable. (`data/tapes.json` remains in the repo as an empty legacy file from the initial version.)
- **Two deployment modes** — Docker/Express (primary; see `config/docker-compose.yml`) and Netlify Functions (see `netlify/functions/server.js` and `netlify.toml`). The `serverless-http` package wraps the Express app as a Lambda-compatible handler.
- **Single-user mode** — auth is optional. If `GOOGLE_CLIENT_ID` is not set, the app runs with no login wall and all tapes are global.
- **Condition** — defaults to `"great"`. Notes field for anything specific.
- **Sold tapes** — stay in the database. `status` field handles everything: `in_collection`, `for_sale`, `sold`, `donated`. No archive table needed.
- **AI for the tedious parts** — photo scanning, title recognition, valuation lookups. Not for the data model.
- **Build incrementally** — don't solve distribution before you've finished cataloging.
