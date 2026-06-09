# vhs — VHS Collection Indexer

**Last Validated:** 2026-06-09 | Initial vault entry
**Repo:** https://github.com/nitsuah/vhs
**Branch convention:** `pmo/vhs/planning-alignment-YYYY-MM-DD`

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Docker build | Unknown | Not yet validated in this vault entry |
| Test suite | Unknown | METRICS and TASKS present, coverage unknown |
| Docs baseline | PASS | README, ROADMAP, TASKS, FEATURES, METRICS present |

---

## Stack

- **Storage:** Flat JSON (`data/tapes.json`) — immutable ID registry, append-only
- **Scripts:** Python (Claude Vision scan, eBay valuation, CSV/HTML export)
- **CI:** GitHub Actions
- **No server, no login, no cloud dependency**

---

## Key Features

- Tape catalog with ID, title, year, label, format, condition, valuation, status
- AI-assisted scanning: `scripts/scan.py` sends batch photos to Claude Vision
- eBay sold-listing valuation: `scripts/valuate.py`
- Export to CSV, HTML, or printable list: `scripts/export.py`
- Status states: `in_collection`, `for_sale`, `sold`, `donated`, `missing`

---

## PMO Findings

- Flat JSON is intentional design choice — collection is expected to be <500 tapes, public-safe.
- Status field handles all tape lifecycle transitions in one file (no separate sold/archive file).
- Wishlist feature explicitly deferred ("downsize mode, not acquisition mode").

---

## Priority Focus

1. Validate Docker build and run `scripts/scan.py` against a sample batch.
2. Establish test coverage baseline (check METRICS.md).
3. Document eBay API key requirement in TASKS/README if `valuate.py` uses external API.

---

## Key Commands

```bash
# Scan a photo batch with Claude Vision
python scripts/scan.py photos/batch-01.jpg

# Look up eBay sold valuations
python scripts/valuate.py

# Export catalog
python scripts/export.py --format csv     # → exports/collection.csv
python scripts/export.py --format html
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/vhs/ROADMAP|ROADMAP]] · [[repos/vhs/TASKS|TASKS]] · [[repos/vhs/FEATURES|FEATURES]] · [[repos/vhs/METRICS|METRICS]] · [[repos/vhs/CHANGELOG|CHANGELOG]] · [[repos/vhs/README|README]]
