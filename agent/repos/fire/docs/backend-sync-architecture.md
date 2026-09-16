?# Backend Sync Architecture

> **Last updated:** 2026-08-12  
> **See also:** [docs/integrations.md](integrations.md), [docs/prod-plan.md](prod-plan.md), [docs/security-hardening.md](security-hardening.md)

---

## Overview

The FIRE Tracker's sync layer connects the local `db.json` store to external financial data providers. All connections are:

- **Opt-in** — nothing syncs unless the user provides credentials
- **BYOK** — users supply their own API keys; no intermediary service holds credentials
- **Read-only** — the system never initiates transactions or modifies external accounts
- **Encrypted at rest** — OAuth tokens stored in `data/tokens.json` using AES-256-GCM

---

## Current Implementation (v1.1.0)

### Token Storage

- Encrypted tokens stored in `data/tokens.json` via `app/lib/crypto-utils.js`
- Algorithm: AES-256-GCM with `SYNC_MASTER_KEY` (64 hex chars = 32 bytes)
- Format: colon-delimited string — `<iv-hex>:<auth-tag-hex>:<ciphertext-hex>`
- Separate from `db.json` encryption, which uses a JSON wrapper `{ enc, iv, tag, data }`

### OAuth Implementations (UI Ready, needs env vars)

The eBay and Plaid OAuth flows are fully implemented with UI access in the Settings page.

**eBay OAuth (Phase 1)**
- `GET /api/sync/ebay/authorize` — initiates eBay OAuth flow with CSRF state
- `GET /api/sync/ebay/callback` — exchanges code for tokens, encrypts with `SYNC_MASTER_KEY`, stores in `data/tokens.json`
- `POST /api/sync/ebay/sync` — pulls completed orders → `sideGigLedger`
- `GET /api/sync/ebay/status` — returns connection status, last sync, environment
- Env vars: `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `EBAY_ENVIRONMENT`, `SYNC_MASTER_KEY`

**Plaid Link (Phase 2)**
- `POST /api/sync/plaid/create-link-token` — generates Plaid Link token for embedded UI
- `POST /api/sync/plaid/exchange` — exchanges public_token → encrypted access_token
- `POST /api/sync/plaid/positions` — syncs investment positions → `importedPositions`
- `POST /api/sync/plaid/accounts` — syncs account balances → `customAccounts`
- `GET /api/sync/plaid/status` — returns connection status, item count
- Env vars: `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ENV`, `SYNC_MASTER_KEY`

### Webhook Framework (functional)

The webhook receiver is fully implemented and in production use.

- `POST /api/sync/webhook/:templateId` — receives payload, runs JSONata mapping, merges into db.json
- HMAC-SHA256 verification against raw request bytes (`req.rawBody`) using `crypto.timingSafeEqual`
- JSONata expressions validated at template creation time; evaluation times out after 5 seconds
- Deduplicates by stable upstream ID or content fingerprint (prevents duplicate entries on re-delivery)
- Supported data types: `accounts`, `cds`, `positions`, `expenses`, `sideGigLedger`, `importedFiles`, `taxRate`, `projectionSettings`

---

## Planned Provider Architecture

### Phase 1 Providers (Q1 2027)

| Provider | Purpose | Auth Type | Token Storage |
|---|---|---|---|
| eBay Order API | Completed sales → sideGigLedger | OAuth 2.0 + refresh token | `data/tokens.json` (encrypted) |
| Etherscan | ETH + ERC-20 wallet balances | API key | env var only |
| BscScan | BNB + BEP-20 wallet balances | API key | env var only |
| Polygonscan | MATIC + ERC-20 balances | API key | env var only |
| Arbiscan | ARB + ERC-20 balances | API key | env var only |
| Basescan | BASE + ERC-20 balances | API key | env var only |
| Blockstream | Bitcoin balance | None | — |
| Solana RPC | SOL balance | None | — |
| CoinGecko | Crypto token USD prices | None (optional key) | env var only |
| Google Drive | Encrypted db.json backup | Service account / OAuth | `config/gdrive-sa.json` (gitignored) |
| NHTSA VPIC | VIN decode / vehicle identity | None | — |

### Phase 2 Providers (Q2 2027)

| Provider | Purpose | Auth Type | Token Storage |
|---|---|---|---|
| Plaid | Fidelity positions + bank balances | OAuth 2.0 via Plaid Link | `data/tokens.json` (encrypted) |
| Alpha Vantage / Polygon.io | Stock quotes (Yahoo fallback) | API key | env var only |

---

## Endpoint Map

```text
/api/sync/
├── init                      GET    OAuth initiation (current: stub → Phase 1/2: eBay, Plaid)
├── callback                  GET    OAuth callback (current: stub)
├── data                      GET    Return synced data (current: stub)
│
├── ebay/                            Phase 1
│   ├── authorize             GET    Initiate eBay OAuth flow
│   ├── callback              GET    Exchange code + store encrypted tokens
│   ├── sync                  POST   Pull completed orders → sideGigLedger
│   └── refresh               POST   Refresh eBay access token
│
├── plaid/                           Phase 2
│   ├── create-link-token     POST   Generate Plaid Link token for embedded UI
│   ├── exchange              POST   Exchange public_token → encrypted access_token
│   ├── accounts              POST   Sync account balances → customAccounts
│   ├── positions             POST   Sync investment positions → importedPositions
│   └── transactions          POST   Sync transactions → expense categorization
│
└── webhook/                         Live (v1.1.0)
    ├── templates             GET    List webhook templates (secrets omitted)
    ├── templates             POST   Create new webhook template
    ├── templates/:id         PUT    Update template
    ├── templates/:id         DELETE Remove template
    └── :templateId           POST   Receive and process webhook payload

/api/wallets/                        Phase 1
├──                           GET    List wallets with last known balances
├──                           POST   Add wallet (address, chain, label)
├── :id                       DELETE Remove wallet
└── refresh                   POST   Trigger balance refresh (all or specific id)

/api/backup/                         Phase 1
├── drive                     POST   Encrypt + upload to Google Drive
├── drive/list                GET    List available Drive backups
└── drive/restore             POST   Download, decrypt, and apply backup
```

---

## Security Properties

| Property | Guarantee |
|---|---|
| API keys at rest | Environment variables only — never written to db.json or tokens.json |
| OAuth tokens at rest | AES-256-GCM encrypted in `data/tokens.json` |
| OAuth tokens in transit | HTTPS to provider endpoints only |
| OAuth tokens in memory | Decrypted only for the duration of the API call |
| Backup data in transit | AES-256-GCM encrypted before upload — provider cannot decrypt |
| Wallet addresses in db.json | Stored in plaintext (public blockchain data by nature) |
| MCP access to tokens | None — MCP reads db.json only, not tokens.json |
| Data transmitted to price APIs | Ticker symbols or coin IDs only |
| Data transmitted to block explorers | Public wallet addresses only |

---

## Chain Registry (`config/chains.json`)

The web3 layer uses a declarative chain registry. Adding a new EVM-compatible chain requires only a new JSON entry — no code changes.

```json
[
  {
    "id": "ethereum",
    "name": "Ethereum",
    "nativeSymbol": "ETH",
    "coingeckoId": "ethereum",
    "apiBase": "https://api.etherscan.io/api",
    "envKey": "ETHERSCAN_API_KEY",
    "addressFormat": "evm",
    "decimals": 18
  },
  {
    "id": "bitcoin",
    "name": "Bitcoin",
    "nativeSymbol": "BTC",
    "coingeckoId": "bitcoin",
    "apiBase": "https://blockstream.info/api",
    "envKey": null,
    "addressFormat": "base58",
    "decimals": 8
  },
  {
    "id": "solana",
    "name": "Solana",
    "nativeSymbol": "SOL",
    "coingeckoId": "solana",
    "apiBase": "https://api.mainnet-beta.solana.com",
    "envKey": null,
    "addressFormat": "base58",
    "decimals": 9
  }
]
```

**`addressFormat`** controls address validation before storage:
- `evm` — must match `/^0x[0-9a-fA-F]{40}$/`
- `base58` — must match Solana or Bitcoin address patterns

---

## Data Flow Diagrams

### Wallet Balance Refresh

```text
User clicks "Refresh Balances"
  → POST /api/wallets/refresh
      → for each wallet in db.json:
          → load chain from config/chains.json
          → if chain.envKey set: read API key from process.env
          → fetch balance from chain.apiBase (native + tokens)
          → fetch USD price from CoinGecko
          → compute lastUsdValue = balance × price
          → mutateState() → update wallet.lastBalance, .lastUsdValue, .lastFetched
      → return updated wallet list (no API keys in response)
```

### eBay Order Sync

```text
User clicks "Sync eBay"
  → POST /api/sync/ebay/sync
      → decrypt access_token from data/tokens.json (using SYNC_MASTER_KEY)
      → if token expired: call /api/sync/ebay/refresh first
      → GET https://api.ebay.com/sell/fulfillment/v1/order (filter: completed)
      → for each order:
          → map to sideGigLedger entry format
          → dedup check: skip if orderId already in sideGigLedger
          → mutateState() → append to sideGigLedger
      → return { synced: N, skipped: M }
      → access_token cleared from memory
```

### Google Drive Backup

```text
User clicks "Backup to Drive"
  → POST /api/backup/drive
      → readState() → get current db.json contents
      → if SYNC_MASTER_KEY set: db.json already encrypted on disk → read raw ciphertext
      → if not: encrypt now with SYNC_MASTER_KEY before upload (REQUIRED)
      → upload to Google Drive as fire-backup-YYYY-MM-DD.json
      → return { success: true, fileId, uploadedAt }
```
