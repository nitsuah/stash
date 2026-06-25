# ROADMAP

## Phase 1 — Capture

**Goal:** get every tape into `tapes.json` with a consistent ID and a title.

### Photo protocol

1. Lay 8–12 tapes face-up in good light, labels visible
2. Shoot the photo — no cards, no numbering, no ceremony
3. Upload and let AI read what it can
4. Do a quick spot-check pass on the results, fix any misreads
5. Repeat

Good lighting and labels face-up is the only real requirement. Clear overhead shots in natural light work best.

### AI scan script (`scan.py`)

- Takes a photo path as input
- Sends it to Claude Vision (via the Anthropic API) with a prompt like:
  > "This photo contains numbered VHS tapes. For each visible number, read the tape label and return JSON: `[{id, title, label, year_if_visible}]`"
- Merges results into `tapes.json`, skipping IDs that already exist (immutability)

**API options:**
- **Claude (Anthropic)** — best for messy/handwritten labels, good at context
- **OpenAI GPT-4o** — comparable vision quality, slightly cheaper per image at scale
- **Recommendation:** Start with Claude. You already have access, and it's better at "I think this says..." reasoning on worn tape labels.

---

## Phase 2 — Valuation

**Goal:** attach a realistic price range to each tape.

### eBay sold listings

The most reliable signal for VHS value is eBay "sold" listings, not asking prices.

Options:
- **Manual:** search eBay, paste in estimated low/high, add `source: "manual"`
- **Semi-automated:** `valuate.py` script that opens an eBay search for each unvalued tape title — you confirm the range
- **Automated (harder):** scrape eBay sold listings via the official eBay Browse API (free, needs account) — returns recent sold prices you can average

### Valuation tiers (rough guide)

| Value | What it usually means |
|---|---|
| $1–5 | Common mainstream releases, ex-rental |
| $5–20 | OOP titles, cult films, certain genres |
| $20–100 | Horror, SOV, anime, foreign, sealed |
| $100+ | Rare SOV, cult horror, sealed big titles |

**Tags to flag for closer research:** horror, SOV (shot-on-video), anime, foreign language, documentary, sealed/shrinkwrapped, small label (not Paramount/Warner/Disney)

---

## Phase 3 — Use the data

Once the index exists, you can do anything with it:

### Exports

- `export.py --format csv` → open in Excel/Sheets for sorting/filtering
- `export.py --format html` → shareable browsable page (no server needed, just open in browser)
- `export.py --format print` → clean printable list sorted by ID

### Sell workflow

Set `status: "for_sale"` on tapes you want to move. Export a filtered list:
```bash
python scripts/export.py --status for_sale
```
That list becomes your eBay drafts or a Mercari batch upload.

### Future ideas (don't build yet)

- Simple web UI (a single `index.html` that reads `tapes.json` via fetch) — searchable, filterable, no backend
- Photo thumbnails auto-cropped per tape (OpenCV or ImageMagick, crop each tape from batch photo)
- Barcode scanning for tapes that still have UPC stickers (cross-reference ISRC/barcode databases)
- Condition grading rubric (create a standard so anyone rating tapes uses the same scale)
- **Tape wall gallery view** — scrollable masonry grid of tape thumbnails (one photo minimum per tape); makes the digital collection feel like the physical shelf and gives a quick visual inventory scan without opening individual records.
- **Sell queue export** — a one-command workflow (`export.py --status for_sale --format drafts`) that auto-populates eBay/Mercari draft templates (title, condition, valuation range, photo path) for each `for_sale` tape; reduces manual copy-paste from `tapes.json` to listing pages.

---

## Tech decisions

| Decision | Choice | Why |
|---|---|---|
| Data format | `tapes.json` | Human-readable, git-diffable, no DB to install |
| Version control | Git | Free history, easy backup, works on any machine |
| AI vision | Claude API (Anthropic) | Best at messy/worn labels, good reasoning |
| Valuation data | eBay sold listings | Most accurate real-world pricing signal |
| Scripting | Python | Widely available, good JSON/HTTP libraries |
| Exports | CSV + HTML | Works everywhere, no dependencies |
| Hosting (if ever) | GitHub Pages | Free, serves static HTML directly from repo |

## Other

- Refer to README.md for the data model and repo structure.
- Refer to TASKS.md for next steps and immediate action items.
- Refer to CONTRIBUTING.md for guidelines on how to contribute to the project.
- Use Docker for a consistent development environment (see Dockerfile and docker-compose.yml).
