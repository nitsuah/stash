# vhs

> Reviewed: 2026-06-25

## Overview

Personal VHS collection indexer — lightweight tool to catalog a VHS tape collection with AI-assisted metadata (Claude Vision), eBay valuation lookups, barcode scanning, and a web UI. Runs locally via Docker (Node.js/Express + Neon PostgreSQL backend). Flat JSON as source of truth; git-versioned.

## Current Goals / Roadmap Focus

**Phase 1 — Capture:** Get every tape into `tapes.json` with ID + title via AI photo scanning
**Phase 2 — Valuation:** Attach realistic price ranges from eBay sold listings  
**Phase 3 — Use the data:** Exports (CSV, HTML, printable), sell workflow, future web UI

**Current active work (feat/vhs-scanner-v2):**
Multi-photo batch scanning, GPU performance improvement, multi-tape detection and crop from batch photos, barcode scanning mode (webcam + barcode library, no AI).

## Open P0/P1 Tasks

From TASKS.md (no priority levels assigned — informal list):

- [ ] Handle multiple photo uploads — batch process, show tapes individually (collapse form; expand on card click), each photo associated with specific tape record
- [ ] Improve performance utilizing GPU
- [ ] Detect and crop individual tapes from batch photos (OpenCV or similar computer vision)
- [ ] Add barcode scanning mode (webcam + barcode library, scan-code option alongside AI mode)

No formal P0/P1 priority labels. All items are active focus for v2.

## Blockers

None documented. Active development on `feat/vhs-scanner-v2` branch.

## Recent Changes (feat/vhs-scanner-v2 — Unreleased)

Storage & Backend:
- Neon PostgreSQL backend replacing nginx; Node.js/Express REST CRUD at `/api/tapes`; Ollama proxy at `/api/ollama`; auto-creates schema on startup
- DB health dot (live green/red indicator; red retries on click)
- Photo compression: `compressImage()` resizes to max 1200px JPEG 0.75 before storing in Neon JSONB

Capture & Scanning:
- Capture queue: Space stages webcam frames as thumbnails; Enter sends all to AI at once
- Barcode scanner: multi-pass canvas preprocessing, ZXing `TRY_HARDER`, HD 1920×1080 stream, UPCitemdb.com auto-fills title
- Torch toggle, snap button (single-frame decode)

Collection Management:
- Full CRUD with confirm dialog; multi-photo per tape
- Batch AI metadata fill (⚡ Fill Data via Claude or Ollama)
- Bulk selection: checkbox multi-select, bulk status change, bulk delete
- Wanted status, sold price tracking, tags/genres (preset + custom)

Discovery & Filtering:
- Full-text search (title, label, barcode, notes, tags)
- Clickable stats bar, filter bar (status, condition, label, tag, year range), sort with persistence
- Wall view (masonry grid); thumbnails in list view

Exports & Imports:
- CSV export (full + for-sale with eBay condition labels)
- JSON export/import (full round-trip including photos)
- CSV import; print price tags; printable HTML list

Mobile & UX:
- Responsive layout; rear camera preference; touch events on crop box
- eBay sold-listings search; 🔍 Lookup button; duplicate detection
- IndexedDB migration from old browser-local version
- Keyboard shortcuts: Space/Enter/N/?/Esc
- CI: Hadolint, Shellcheck, HTMLHint, `npm ci --omit=dev` check, Docker build smoke test
