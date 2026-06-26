# VHS Collection Indexer — Features

Status guide: `[shipped]` is available now, `[planned]` is backlog work.

## Data & Registry

- `[shipped]` **Tape Registry**: Append-only `data/tapes.json` with immutable `VHS-XXXX` IDs
- `[shipped]` **Status Tracking**: `in_collection`, `for_sale`, `sold`, `donated`, `missing`
- `[shipped]` **Condition Tracking**: `great`, `good`, `fair`, `poor` with free-text notes
- `[planned]` **Valuation**: eBay sold-listings lookup via `scripts/valuate.py`

## Scripts

- `[planned]` **AI Scan**: `scripts/scan.py` — sends batch photos to Claude Vision, returns structured JSON
- `[planned]` **Valuate**: `scripts/valuate.py` — looks up eBay sold listings for price estimates
- `[planned]` **Export**: `scripts/export.py` — generates CSV, HTML, or printable list from registry

## Export & Sharing

- `[planned]` **CSV Export**: Machine-readable export for spreadsheets
- `[planned]` **HTML Export**: Human-readable collection page
