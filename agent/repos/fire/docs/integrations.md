?# Integrations Reference

> **Status:** Planning  
> **Last updated:** 2026-08-12  
> **See also:** [docs/prod-plan.md](prod-plan.md), [docs/backend-sync-architecture.md](backend-sync-architecture.md)

This document describes every planned external integration — what credentials are needed, what data is fetched, and what setup is required.

---

## eBay API

**Purpose:** Automatically import completed sales into the side gig ledger.  
**Phase:** PROD Phase 1 (Q1 2027) — **UI Ready** (OAuth status check, authorize/sync endpoints)  
**Auth type:** OAuth 2.0 Authorization Code

### Setup

1. Register at [developer.ebay.com](https://developer.ebay.com)
2. Create a new application → select **REST APIs**
3. Set redirect URI to `http://localhost:3001/api/sync/ebay/callback`
4. Copy **Client ID** and **Client Secret** from the application credentials page
5. Start in **Sandbox** environment and switch to **Production** after testing

### Env Vars

```dotenv
EBAY_CLIENT_ID=       # From eBay developer application
EBAY_CLIENT_SECRET=   # From eBay developer application
EBAY_REFRESH_TOKEN=   # Generated during initial OAuth flow; long-lived
EBAY_ENVIRONMENT=sandbox  # Change to "production" after testing
SYNC_MASTER_KEY=      # 64 hex chars — required to encrypt stored OAuth tokens
```

### What's Fetched

- Completed orders from the [Order API v1](https://developer.ebay.com/api-docs/sell/fulfillment/resources/order/methods/getOrders)
- Fields used: `orderId`, `creationDate`, `pricingSummary.total`, `lineItems[].title`, `lineItems[].deliveryCost`
- Mapped to `sideGigLedger` entries: platform=ebay, date=creationDate, gross=total, description=item title
- Deduplication: `orderId` used as the stable upstream ID

### OAuth Scope

`https://api.ebay.com/oauth/api_scope/sell.fulfillment.readonly` — read-only access to order data.

### Current Implementation Status

- ✅ OAuth authorize endpoint: `GET /api/sync/ebay/authorize`
- ✅ OAuth callback endpoint: `GET /api/sync/ebay/callback`
- ✅ Sync endpoint: `POST /api/sync/ebay/sync`
- ✅ Status check endpoint: `GET /api/sync/ebay/status` (returns connected state, last sync, environment)
- ✅ Settings page UI with connection status display
- ⏳ Requires `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `SYNC_MASTER_KEY` environment variables to function

---

## Etherscan (Ethereum Wallet Balances)

**Purpose:** Fetch ETH and ERC-20 token balances for tracked wallet addresses.  
**Phase:** PROD Phase 1 (Q1 2027)  
**Auth type:** API key (BYOK)

### Setup

1. Register at [etherscan.io](https://etherscan.io)
2. Navigate to **My Account → API Keys** → create a free API key
3. Free tier: 5 requests/second, 100,000 calls/day

### Env Vars

```dotenv
ETHERSCAN_API_KEY=    # From etherscan.io account
```

### What's Fetched

- Native ETH balance: `?module=account&action=balance&address=0x...`
- ERC-20 token balances: use `tokenbalance` with an explicit token contract address (`?module=account&action=tokenbalance&contractaddress=0x...&address=0x...`). Current token balances require querying each known contract; `tokentx` returns transfer history only and must not be used to derive balances without full pagination and reconstruction.
- Prices: CoinGecko `/api/v3/simple/price?ids=ethereum&vs_currencies=usd` (no key required)

---

## BscScan (BNB Smart Chain)

**Purpose:** Fetch BNB and BEP-20 token balances.  
**Phase:** PROD Phase 1 (Q1 2027)  
**Auth type:** API key (BYOK)

### Setup

1. Register at [bscscan.com](https://bscscan.com)
2. **My Account → API Keys** → create free API key

### Env Vars

```dotenv
BSCSCAN_API_KEY=
```

---

## Polygonscan (Polygon / MATIC)

**Purpose:** MATIC and ERC-20 balances on Polygon.

### Setup

1. Register at [polygonscan.com](https://polygonscan.com)
2. Create a free API key

### Env Vars

```dotenv
POLYGONSCAN_API_KEY=
```

---

## Arbiscan (Arbitrum One)

**Purpose:** ETH and ERC-20 balances on Arbitrum.

### Setup

1. Register at [arbiscan.io](https://arbiscan.io)
2. Create a free API key

### Env Vars

```dotenv
ARBISCAN_API_KEY=
```

---

## Basescan (Base)

**Purpose:** ETH and ERC-20 balances on Base.

### Setup

1. Register at [basescan.org](https://basescan.org)
2. Create a free API key

### Env Vars

```dotenv
BASESCAN_API_KEY=
```

---

## Blockstream (Bitcoin)

**Purpose:** Fetch Bitcoin balance for a tracked wallet address.  
**Phase:** PROD Phase 1  
**Auth type:** None required

### What's Fetched

- `GET https://blockstream.info/api/address/{address}` — returns `chain_stats.funded_txo_sum` − `chain_stats.spent_txo_sum` in satoshis
- Convert satoshis to BTC (÷ 100,000,000)
- BTC price from CoinGecko

No API key, no registration. Blockstream is a public Bitcoin block explorer.

---

## Solana (Public RPC)

**Purpose:** Fetch SOL balance for a tracked wallet address.  
**Phase:** PROD Phase 1  
**Auth type:** None (public RPC endpoint)

### What's Fetched

- `POST https://api.mainnet-beta.solana.com` with `getBalance` RPC call
- Returns lamports; convert to SOL (÷ 1,000,000,000)
- SOL price from CoinGecko

No API key required for basic balance lookups.

---

## CoinGecko (Crypto Prices)

**Purpose:** USD prices for native chain tokens and tracked ERC-20/BEP-20/SPL tokens.  
**Phase:** PROD Phase 1  
**Auth type:** None for free tier

### Free Tier Limits

- 30 calls/minute, no API key required
- For higher volume: register at [coingecko.com](https://www.coingecko.com/en/api) for a free key with higher limits

### What's Fetched

```text
GET https://api.coingecko.com/api/v3/simple/price?ids=ethereum,bitcoin,solana&vs_currencies=usd
```

Coin IDs are specified in `config/chains.json` per chain.

### Env Vars

```dotenv
COINGECKO_API_KEY=    # Optional; increases rate limit
```

---

## Google Drive (Encrypted Backup)

**Purpose:** Store an AES-256-GCM encrypted copy of db.json in the user's personal Google Drive.  
**Phase:** PROD Phase 1  
**Auth type:** Service account JSON key (recommended) or user OAuth

### Setup (Service Account — Recommended)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project (or use existing)
3. Enable the **Google Drive API**
4. Go to **IAM & Admin → Service Accounts** → create a service account
5. Create and download a JSON key for the service account
6. In Google Drive, create a folder called `fire-tracker-backups`
7. Share that folder with the service account email address (Editor role)
8. Place the JSON key file in `config/gdrive-sa.json` (git-ignored)

### Env Vars

```dotenv
GDRIVE_SERVICE_ACCOUNT_JSON=./config/gdrive-sa.json   # Path to service account key file
GDRIVE_BACKUP_FOLDER_ID=                              # Optional: Drive folder ID (auto-created if blank)
```

### Security Note

The uploaded file is encrypted with AES-256-GCM using `SYNC_MASTER_KEY` **before** it leaves the machine. Google cannot read the backup. If `SYNC_MASTER_KEY` is lost, the backup cannot be decrypted.

---

## Plaid (Bank / Fidelity Aggregation)

**Purpose:** Real-time position and balance sync from Fidelity, bank accounts, and other institutions via Plaid's aggregation network.  
**Phase:** PROD Phase 2 (Q2 2027) — **UI Ready** (Plaid Link SDK embedded, create-link-token/exchange endpoints)  
**Auth type:** OAuth 2.0 via Plaid Link (BYOK)

### Setup

1. Register at [plaid.com](https://plaid.com/docs/)
2. Create an application in the Plaid Dashboard
3. Get **Client ID** and **Secret** for the sandbox environment
4. Apply for production access after sandbox testing

### Env Vars

```dotenv
PLAID_CLIENT_ID=
PLAID_SECRET=
PLAID_ENV=sandbox    # Change to "production" after testing
SYNC_MASTER_KEY=     # 64 hex chars — required to encrypt stored OAuth tokens
```

### Products Requested

- `investments` — brokerage positions and balances (requires Plaid Partner approval for some institutions)
- `auth` — bank account balances

### What's Synced

- Investment positions → `importedPositions` (replaces Fidelity CSV import when active)
- Account balances → `customAccounts`
- Transactions (optional) → expense categorization

### Note on Fidelity

Fidelity's support via Plaid depends on Plaid's institution coverage and Fidelity's data-sharing agreements. As of 2026, Fidelity supports balance and investment data via Plaid for eligible accounts. Check Plaid's [institution search](https://plaid.com/docs/institutions/) for current coverage.

### Current Implementation Status

- ✅ Create Link Token endpoint: `POST /api/sync/plaid/create-link-token`
- ✅ Exchange Public Token endpoint: `POST /api/sync/plaid/exchange`
- ✅ Sync Positions endpoint: `POST /api/sync/plaid/positions`
- ✅ Sync Accounts endpoint: `POST /api/sync/plaid/accounts`
- ✅ Status check endpoint: `GET /api/sync/plaid/status` (returns connected state, item count)
- ✅ Plaid Link SDK embedded in Settings page (`initPlaidLink()`)
- ✅ Connection status check (`checkPlaidConnection()`)
- ⏳ Requires `PLAID_CLIENT_ID`, `PLAID_SECRET`, `SYNC_MASTER_KEY` environment variables to function

---

## Alpha Vantage / Polygon.io (Stock Prices)

**Purpose:** Stable, API-key-gated alternative to Yahoo Finance's crumb-based scraping.  
**Phase:** PROD Phase 2  
**Auth type:** API key (BYOK)

### Alpha Vantage

- Free tier: 25 requests/day (sufficient for end-of-day price refresh)
- Register at [alphavantage.co](https://www.alphavantage.co/support/#api-key)

```dotenv
ALPHA_VANTAGE_API_KEY=
```

### Polygon.io

- Free tier: delayed quotes; paid tiers offer real-time
- Register at [polygon.io](https://polygon.io)

```dotenv
POLYGON_API_KEY=
```

The price provider is selected by whichever env var is set; Yahoo Finance is the fallback if neither is configured.

---

## Vehicle Value API

**Purpose:** Auto-update vehicle market values (replaces manual entry).  
**Phase:** PROD Phase 1  
**Auth type:** BYOK (provider-dependent)

### Free Option: NHTSA VPIC

No API key required. Decodes VIN to confirm make/model/year.

```text
GET https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{VIN}?format=json
```

Does not provide market value — only vehicle identity confirmation.

### Paid Options

| Provider | Notes | Auth |
|---|---|---|
| DataOne.io | Pay-per-request, vehicle valuations | API key |
| MarketCheck | New/used market data | API key |
| KBB (Kelley Blue Book) | Requires partner agreement with Cox Automotive | Partner key |

```dotenv
VEHICLE_VALUE_API_KEY=    # Provider-specific; set VEHICLE_VALUE_PROVIDER=dataone|marketcheck
VEHICLE_VALUE_PROVIDER=dataone
```

---

## Current Integration Status Summary

| Integration | Status | Env Vars Required |
|---|---|---|
| Yahoo Finance prices | ✅ Live | None |
| Fidelity CSV (manual) | ✅ Live | None |
| Chase / CapOne CSV (manual) | ✅ Live | None |
| eBay fee calculator (manual) | ✅ Live | None |
| eBay Order API | ❌ Phase 1 | `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `EBAY_REFRESH_TOKEN` |
| Etherscan (ETH wallets) | ❌ Phase 1 | `ETHERSCAN_API_KEY` |
| BscScan (BNB wallets) | ❌ Phase 1 | `BSCSCAN_API_KEY` |
| Polygonscan (MATIC wallets) | ❌ Phase 1 | `POLYGONSCAN_API_KEY` |
| Arbiscan (ARB wallets) | ❌ Phase 1 | `ARBISCAN_API_KEY` |
| Basescan (BASE wallets) | ❌ Phase 1 | `BASESCAN_API_KEY` |
| Routescan (Avalanche wallets) | ❌ Phase 1 | `ROUTESCAN_API_KEY` (optional) |
| Blockstream (Bitcoin) | ❌ Phase 1 | None |
| Solana RPC | ❌ Phase 1 | None |
| CoinGecko prices | ❌ Phase 1 | None (optional key) |
| Google Drive backup | ❌ Phase 1 | `GDRIVE_SERVICE_ACCOUNT_JSON` |
| NHTSA VIN decode | ❌ Phase 1 | None |
| Vehicle value API | ❌ Phase 1 | `VEHICLE_VALUE_API_KEY` |
| Plaid (Fidelity/bank sync) | ❌ Phase 2 | `PLAID_CLIENT_ID`, `PLAID_SECRET` |
| Alpha Vantage / Polygon.io | ❌ Phase 2 | `ALPHA_VANTAGE_API_KEY` or `POLYGON_API_KEY` |
