?# PROD Plan — FIRE Tracker Productionization

> **Status:** Planning  
> **Last updated:** 2026-08-12  
> **See also:** [ROADMAP.md](../ROADMAP.md), [TASKS.md](../TASKS.md), [docs/security-hardening.md](security-hardening.md), [docs/integrations.md](integrations.md)

---

## Purpose

This document phases the FIRE Tracker from its current offline-first, CSV-import-driven state toward a production-grade personal finance platform on par with Fidelity NetBenefits and Rocket Money — while preserving the local-first, privacy-first, self-hosted architecture.

The system remains **read-only** with respect to financial accounts. It will never initiate transactions, move money, or store unencrypted credentials. All sensitive data stays encrypted on the user's own machine. External connections are minimal and opt-in (BYOK).

---

## Guiding Principles

1. **BYOK first** — Every external API is opt-in, authenticated with the user's own keys. OAuth tokens are encrypted at rest in `data/tokens.json`; API keys (block explorers, price APIs) live only in environment variables and are never written to disk by the application.
2. **Minimal OAuth scope** — Request only the narrowest scope needed (read positions, read balances). Never request write access to any financial account.
3. **Offline-capable** — Manual import fallback for every automated connector. Dashboard must function with zero external connections.
4. **Transmit as little as possible** — API calls go from the local Docker container directly to the provider. No relay server. No telemetry.
5. **MCP as a data router** — The MCP server is a read-only query interface over locally stored data. It is not a proxy for external APIs and never exposes raw credentials.

---

## Current State (v1.1.0)

| Capability | Status | Notes |
|---|---|---|
| Manual account entry | ✅ Live | CRUD via REST API |
| Fidelity CSV import | ✅ Live | Multi-account aggregation |
| Chase / CapOne CSV import | ✅ Live | Auto-categorizes expenses |
| eBay/Etsy/FB fee calculators | ✅ Live | Manual entry only (no API) |
| Yahoo Finance live prices | ✅ Live | Crumb-based, 5-min TTL |
| AES-256-GCM db.json encryption | ✅ Live | Opt-in via SYNC_MASTER_KEY |
| MCP server (8 read-only tools) | ✅ Live | stdio transport |
| Webhook sync framework | ✅ Live | JSONata mapping + HMAC |
| OAuth scaffold | ✅ Live | eBay OAuth + Plaid Link SDK with UI |
| eBay API integration | ✅ UI Ready | Backend endpoints complete; needs env vars |
| Web3 wallet tracking | ❌ Planned | PROD Phase 1 |
| Vehicle value API | ✅ UI Ready | Estimate overlay styled; needs premium API key |
| Encrypted cloud backup | ❌ Planned | PROD Phase 1 |
| Fidelity/Plaid sync | ✅ UI Ready | Backend + Plaid Link SDK complete; needs env vars |
| Rate limiting | ❌ Planned | PROD Phase 3 |
| HTTPS | ❌ Planned | PROD Phase 3 |
| Unified Settings Page | ✅ Live | Notifications, export/import, privacy/terms, danger zone |
| Milestone Presets | ✅ Live | 5 profiles (Conservative/Standard/Aggressive/Barista/Coast) |
| Diversification Tips | ✅ Live | Dismissible tiles with curated links |
| Retirement Drawdown/Depletion | ✅ Live | Accurate money run-out detection |

---

## PROD Phase 1 — Real-Time Data Connectors (Q1 2027)

### 1.1 eBay API Connector

The current eBay implementation is a fee calculator only (manual entry). Phase 1 adds automated import of completed sales from the eBay Order API.

**Auth:** OAuth 2.0 Authorization Code grant via eBay Developer program.

**Steps to get credentials:**
1. Register at https://developer.ebay.com
2. Create a production application → get `client_id` + `client_secret`
3. Generate a long-lived `refresh_token` via the authorization flow
4. Set `EBAY_ENVIRONMENT=production` (default: sandbox)

**Env vars:**
```dotenv
EBAY_CLIENT_ID=
EBAY_CLIENT_SECRET=
EBAY_REFRESH_TOKEN=
EBAY_ENVIRONMENT=sandbox
```

**Endpoints (new):**
- `POST /api/sync/ebay/authorize` — initiates eBay OAuth
- `GET /api/sync/ebay/callback` — code exchange + encrypted token storage
- `POST /api/sync/ebay/sync` — pulls completed orders → sideGigLedger (deduplicated by `orderId`)
- `POST /api/sync/ebay/refresh` — refreshes access token

**eBay APIs used:**
- [Order API v1 getOrders](https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/methods/getOrders) — completed sales
- Scope: `https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly`

**Security:**
- Tokens stored encrypted in `data/tokens.json` (existing `crypto-utils.js`)
- `EBAY_REFRESH_TOKEN` never logged
- Sandbox mode by default until `EBAY_ENVIRONMENT=production` is set

---

### 1.2 Web3 / Crypto Wallet Tracking

Replaces manual "Crypto" account entries with actual wallet balance lookups across major chains.

**Architecture:**

New `wallets` array in db.json:
```json
{
  "id": "uuid-v4",
  "address": "0xabc...",
  "chain": "ethereum",
  "label": "Main ETH",
  "lastBalance": 2.541,
  "lastUsdValue": 8234.56,
  "lastFetched": "2026-08-12T10:00:00Z"
}
```

**Supported chains at launch:**

| Chain | Explorer API | Key Required | Env Var |
|---|---|---|---|
| Ethereum | etherscan.io | Yes (free tier) | `ETHERSCAN_API_KEY` |
| BNB Smart Chain | bscscan.com | Yes (free tier) | `BSCSCAN_API_KEY` |
| Polygon | polygonscan.com | Yes (free tier) | `POLYGONSCAN_API_KEY` |
| Arbitrum One | arbiscan.io | Yes (free tier) | `ARBISCAN_API_KEY` |
| Base | basescan.org | Yes (free tier) | `BASESCAN_API_KEY` |
| Avalanche | routescan.io | Optional | `ROUTESCAN_API_KEY` |
| Bitcoin | blockstream.info | No | — |
| Solana | public RPC | No | — |

**Chain registry (`config/chains.json`):**
```json
[
  {
    "id": "ethereum",
    "name": "Ethereum",
    "nativeSymbol": "ETH",
    "coingeckoId": "ethereum",
    "apiBase": "https://api.etherscan.io/api",
    "envKey": "ETHERSCAN_API_KEY",
    "addressFormat": "evm"
  },
  {
    "id": "bitcoin",
    "name": "Bitcoin",
    "nativeSymbol": "BTC",
    "coingeckoId": "bitcoin",
    "apiBase": "https://blockstream.info/api",
    "envKey": null,
    "addressFormat": "base58"
  }
]
```

Adding a new EVM chain requires only a new entry in `config/chains.json` — no code changes.

**Balance calculation:**
- EVM chains: native balance + ERC-20 token balances (Etherscan `tokenbalance` endpoint)
- Prices: CoinGecko free API (`/api/v3/simple/price`) for native token USD value
- Token USD value = `balance × price`; aggregated per wallet
- Wallet totals roll into net worth under "Crypto Wallets" (replaces manual Crypto accounts)

**New MCP tool: `get_wallets`**
Returns: chain, address (last 8 chars), label, USD balance, last-fetched timestamp. Full addresses are not exposed via MCP.

**Security:**
- Wallet addresses are public blockchain data — safe to store unencrypted
- Block explorer API keys are env vars only — never stored in db.json
- Address format validated before storage (hex for EVM, base58 for BTC/SOL)

---

### 1.3 Vehicle Value API

**Goal:** auto-update vehicle market values on dashboard load instead of manual entry.

**Implementation:**
- **Free tier:** NHTSA VPIC API (`https://vpic.nhtsa.dot.gov/api/`) — VIN decode confirms make/model/year
- **Value estimate:** BYOK integration (env var `VEHICLE_VALUE_API_KEY`) targeting a provider like DataOne.io or MarketCheck. KBB requires a partner agreement.
- **Fallback:** "Last updated: X days ago" badge with manual "Refresh" button if no API key is set

**No personal vehicle data leaves the machine beyond the VIN** (VIN is a public vehicle identifier).

---

### 1.4 Encrypted Cloud Backup (Google Drive)

**Goal:** automated encrypted backup of db.json to the user's personal Google Drive.

**Auth options:**
1. **Service account** (recommended for self-hosted): create a GCP service account, share the Drive folder with the service account email, set `GDRIVE_SERVICE_ACCOUNT_JSON` to the path of the JSON key file
2. **User OAuth**: `/api/backup/drive/authorize` → Google OAuth flow → encrypted token storage

**Critical:** db.json is encrypted with AES-256-GCM using `SYNC_MASTER_KEY` **before** upload, regardless of whether local encryption is enabled. Google cannot decrypt the backup.

**Endpoints:**
- `POST /api/backup/drive` — encrypt + upload as `fire-backup-YYYY-MM-DD.json` to `fire-tracker-backups/` folder
- `GET /api/backup/drive/list` — list available backups (date, size)
- `POST /api/backup/drive/restore` — download + decrypt + apply (requires `SYNC_MASTER_KEY`)

**Env vars:**
```dotenv
GDRIVE_SERVICE_ACCOUNT_JSON=./config/gdrive-sa.json
```

---

## PROD Phase 2 — Financial Institution Integration (Q2 2027)

### 2.1 Fidelity Integration

**Reality check:** Fidelity does not offer a public OAuth 2.0 API as of 2026. Options ranked by viability:

1. **Plaid** (recommended) — supports Fidelity account aggregation; widely used; free sandbox available
2. **OFX/QFX file parsing** — Fidelity supports OFX export; parse and ingest without an API key; lower maintenance than current CSV approach
3. **Fidelity Direct API** — in beta for registered investment advisors; monitor for public access

**Plaid implementation:**

Env vars:
```dotenv
PLAID_CLIENT_ID=
PLAID_SECRET=
PLAID_ENV=sandbox
```

Flow:
1. User clicks "Connect Fidelity" in settings
2. Server calls Plaid to create a link token (`POST /api/sync/plaid/create-link-token`)
3. Plaid Link JS SDK opens bank authentication flow in browser
4. On success, browser sends `public_token` to server (`POST /api/sync/plaid/exchange`)
5. Server exchanges for `access_token` + `item_id`, encrypts, stores in `data/tokens.json`
6. Subsequent syncs: `POST /api/sync/plaid/positions` → `importedPositions`, `POST /api/sync/plaid/accounts` → `customAccounts`

**Scope stored:**
- Encrypted `access_token` in `data/tokens.json` only
- No account numbers, routing numbers, or transaction history stored raw

**When Plaid sync is active:** manual Fidelity CSV import UI is hidden to prevent duplicate data.

---

### 2.2 Real-Time Price Improvements

Yahoo Finance's crumb-based auth is brittle (HTML scraping, subject to breakage). Phase 2 replaces it:

- **Primary:** Alpha Vantage (BYOK: `ALPHA_VANTAGE_API_KEY`) — free tier: 25 requests/day; premium tiers available
- **Alternative:** Polygon.io (BYOK: `POLYGON_API_KEY`) — real-time WebSocket feed available
- **Crypto:** CoinGecko free API (`/api/v3/simple/price`) — 30 req/min, no key for basic tier
- **SSE:** `GET /api/prices/stream` endpoint pushes price updates to browser in real time (replaces polling)

Price provider precedence: `ALPHA_VANTAGE_API_KEY` is checked first; if unset, `POLYGON_API_KEY` is checked; if neither is set, Yahoo Finance is used as the fallback. A `PRICE_PROVIDER` override env var can force a specific provider regardless of key presence.

---

## PROD Phase 3 — Security Hardening (Q3 2027)

See [docs/security-hardening.md](security-hardening.md) for the full audit and remediation plan.

**Summary of gaps and fixes:**

| Gap | Severity | Fix |
|---|---|---|
| No rate limiting | High | express-rate-limit |
| No HTTPS | High | Caddy reverse proxy |
| SESSION_SECRET default fallback | High | Fail-fast in production |
| FIRE_API_KEY optional | Medium | Required by default |
| Webhook payload unlimited | Medium | 16KB cap |
| Webhook field validation incomplete | Medium | Schema check per type |
| npm audit not in CI | Low | Add audit step |
| No MCP audit log | Low | tool + timestamp + bytes |
| No key rotation | Low | Re-encrypt endpoint |

---

## PROD Phase 4 — Feature Parity (Q4 2027)

At this phase, the system provides:

| Feature | Fidelity/Rocket Money analog |
|---|---|
| Real-time brokerage positions | Fidelity NetBenefits |
| Bank account balances | Rocket Money aggregation |
| Expense categorization | Rocket Money spending |
| Net worth trend | Rocket Money NW graph |
| Investment P&L | Fidelity performance |
| FIRE projection | (no direct analog) |
| Crypto wallet tracking | Zerion / CoinTracker |
| CD/fixed income ladder | (no direct analog) |
| Vehicle values | Rocket Money assets |
| LLM integration via MCP | (no direct analog) |

---

## Data Architecture Evolution

### What stays local

| Data | Location | Encrypted |
|---|---|---|
| All financial positions and balances | `data/db.json` | Optional (SYNC_MASTER_KEY) |
| OAuth tokens (Plaid, eBay, Google) | `data/tokens.json` | Always (SYNC_MASTER_KEY) |
| Chain registry | `config/chains.json` | No (non-sensitive config) |

### What leaves the machine

| Request | Destination | What's sent |
|---|---|---|
| Price quotes | Yahoo Finance / Alpha Vantage | Ticker symbols only |
| Crypto prices | CoinGecko | CoinGecko IDs only |
| Wallet balance lookups | Etherscan / Blockstream / etc. | Public wallet addresses only |
| OAuth authorization | Fidelity/Plaid/eBay/Google | client_id + scoped authorization code |
| Google Drive backup | Google Drive | AES-256-GCM encrypted blob (provider cannot decrypt) |

### What never leaves the machine (to third-party providers)

- Account balances, positions, or net worth figures in raw form — these may appear in MCP responses to a locally connected LLM client, but are not transmitted to external providers or relay servers
- OAuth access tokens / refresh tokens (encrypted at rest, decrypted only in memory)
- SYNC_MASTER_KEY
- Social Security numbers, tax IDs, or government identifiers
- Account numbers or routing numbers

---

## MCP Security Model

The MCP server is a read-only query interface over `db.json`. It does not:
- Accept or execute write commands
- Proxy calls to external APIs
- Expose raw OAuth tokens
- Log the contents of financial positions

MCP responses contain "basic numbers and associated positions" — aggregate balances, position sizes, and projection metrics. Even if an adversary intercepted MCP output, they would see net worth figures and ticker symbols — not account numbers, credentials, or anything actionable for financial fraud.

**Phase 3 hardening additions:**
- Audit log: tool name + timestamp + response byte size (no content)
- Account/position identifiers truncated to last 4 chars in MCP responses
- `get_portfolio`: account names returned verbatim but no account numbers
- `get_wallets`: addresses truncated to last 8 chars
- No external network calls from the MCP process
- Test asserting zero write tools are registered
