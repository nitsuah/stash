# VHS Collection Indexer — Project Plan

## What we're building

A lightweight, personal tool to catalog your girlfriend's VHS collection — capturing what each tape is, what it might be worth, and building a record you can actually use (sell, store, share). The whole thing lives in a git repo as flat files. No server, no login, no cloud dependency.

## Core philosophy

- Immutable index first — the tape registry is append-only. Once a tape gets an ID, it keeps it forever. You can enrich records over time, but IDs never change.
- Flat files in git — the source of truth is a JSON file you can read, diff, and version. Simple wins.
- AI for the tedious parts — photo scanning, title recognition, valuation lookups. Not for the data model.
- Build incrementally — don't solve distribution before you've finished cataloging.


## Data model

Each tape is one record in data/tapes.json:

```json
{
  "id": "VHS-0001",
  "scanned_at": "2025-04-28",
  "photo": "photos/batch-01.jpg",
  "photo_position": 3,
  "title": "Dirty Dancing",
  "year": 1987,
  "label": "Vestron Video",
  "format": "VHS",
  "condition": "great",
  "condition_notes": "",
  "tags": ["drama", "romance", "80s"],
  "valuation": {
    "estimated_low": 2,
    "estimated_high": 8,
    "source": "ebay_sold",
    "checked_at": "2025-04-28"
  },
  "status": "in_collection"
}
```
status can be: in_collection, for_sale, sold, donated, missing

## Repo structure

```bash
vhs-collection/
├── tapes.json              ← the index (truth)
├── photos/
│   ├── batch-01.jpg
│   ├── batch-02.jpg
│   └── ...
├── scripts/
│   ├── scan.py             ← sends photos to Claude Vision, returns structured JSON
│   ├── valuate.py          ← looks up eBay sold listings
│   └── export.py           ← generates CSV, HTML, or printable list
├── exports/
│   └── collection.csv      ← generated, not edited by hand
└── README.md
```

## Running the app

```bash
cp .env.example .env   # fill in DATABASE_URL and HOST_IP
docker compose up
```

App is at `http://localhost:8080` (or whatever `APP_PORT` you set).

## Mobile / HTTPS setup

Mobile browsers block camera access on plain HTTP. The app auto-generates a
self-signed TLS cert on first boot and serves it for easy installation.

**One-time setup per device:**

1. Set `HOST_IP=<your LAN IP>` in `.env` (e.g. `HOST_IP=192.168.1.171`)
2. Start the app: `docker compose up`
3. On your phone, open: `http://192.168.1.171:8082/ca.crt`
4. Android: tap the downloaded file → Install → name it "VHS Scanner" → OK
   iOS: tap Allow → go to Settings → General → VPN & Device Management → trust it
5. Use `https://192.168.1.171:8443` on your phone — camera will work

**If your IP changes:**
```bash
docker volume rm vhs_certs   # forces cert regeneration with new IP on next start
```
Then update `HOST_IP` in `.env` and restart.

> **Note:** The cert is self-signed by a local CA that only your devices trust.
> Traffic never leaves your LAN. The cert lasts 10 years.

## Decisions made

- **Condition** — track it, defaults to `"great"` since she keeps her stuff well. Notes field for anything specific.
- **Wishlist** — skip it for now. She's in downsize mode, not acquisition mode.
- **Sold tapes** — stay in the file. `status` field handles everything: `in_collection`, `for_sale`, `sold`, `donated`. No separate file needed.
- **Flat JSON vs SQLite** — flat JSON is the right call. Collection is likely under 500, nothing sensitive, can live as a public GitHub repo. Simple is correct here.
