---
up: "[[repos/fire]]"
title: "fire · integrations"
source: https://github.com/nitsuah/fire/blob/main/docs/integrations.md
kind: repo-doc
repo: fire
---


# Integrations Reference

> 🧭 [fire](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->
>
> **Status:** Reference / current implementation  
> **Last updated:** 2026-10-01  
> **See also:** [docs/prod-plan.md](prod-plan.md), [docs/backend-sync-architecture.md](backend-sync-architecture.md)

This document describes every planned external integration — what credentials are needed, what data is fetched, and what setup is required.

---

## eBay API

**Purpose:** Automatically import completed sales into the side gig ledger.  
**Phase:** PROD Phase 1 — **Live** (self-hosted Express + browser-only Netlify Functions)  
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
- ✅ Revoked access: if a token refresh fails with `invalid_grant` (the user disconnected the app or closed/deleted their eBay account), sync returns `401 {"code":"ebay_revoked"}`. The stored tokens and the ledger rows the Order API sync created (`id` exactly `ebay-<orderId>`; uploaded report rows are `ebay-csv-…` and are kept) are then deleted: on the server in self-hosted mode, and in `localStorage` in browser-only mode. The user gets an alert. Manually logged sales and uploaded CSV reports are kept.

### Browser-only deploy (Netlify Functions)

lifefire.netlify.app has no Express server, so `netlify.toml` rewrites the eBay
routes to Netlify Functions in `netlify/functions/`. The public paths stay the same.
The Functions and the Express routes share one implementation (`app/lib/ebay-handlers.js`,
`app/lib/ebay-connector.js`).
The Functions use the modern Netlify signature (`export default (req: Request) => Response`,
`.mjs`), not the Lambda-compatible `exports.handler` format. The Lambda-compatible
format caps a site's env vars at 4KB, and lifefire exceeds that.

| Public path | Function | Notes |
|---|---|---|
| `GET /api/sync/ebay/authorize` | `ebay-authorize` | Redirects to eBay; CSRF `state` in a 10-min HttpOnly cookie |
| `GET /api/sync/ebay/callback` | `ebay-callback` | Exchanges the code, returns the tokens **encrypted with `SYNC_MASTER_KEY`** to the SPA in the URL fragment (`/#ebay-connected=…`). The SPA accepts it only if this tab started the connect (a `sessionStorage` marker set on the Connect click) |
| `POST /api/sync/ebay/sync` | `ebay-sync` | Body `{tokens: <blob>}`; returns ledger `entries` (+ a new blob if refreshed). The SPA merges them into `localStorage` |
| `GET/POST /api/sync/ebay/marketplace-account-deletion` | `ebay-marketplace-account-deletion` | See below |

No eBay data is stored server-side. The browser holds an opaque blob
(`localStorage` key `fire_tracker_ebay_token`, kept out of JSON backups) that
only the Functions can decrypt. Status and the sync on/off toggle are computed
in the browser in this mode (`app/lib/side-gig.js`).

Netlify environment variables (Site configuration → Environment variables):

| Variable | Value |
|---|---|
| `EBAY_CLIENT_ID` / `EBAY_CLIENT_SECRET` | Production keyset |
| `EBAY_ENVIRONMENT` | `production` |
| `EBAY_REDIRECT_URI` | Your eBay **RuName** (User Tokens → "Get a Token from eBay via Your Application"), with its *auth accepted URL* set to `https://lifefire.netlify.app/api/sync/ebay/callback` |
| `SYNC_MASTER_KEY` | 64 hex chars (`openssl rand -hex 32`). Rotating it disconnects every browser (the sync returns `ebay_token_invalid` and the user reconnects) |
| `EBAY_VERIFICATION_TOKEN` | 32–80 chars of `[A-Za-z0-9_-]` (`openssl rand -hex 32`) |
| `EBAY_NOTIFICATION_ENDPOINT_URL` | `https://lifefire.netlify.app/api/sync/ebay/marketplace-account-deletion` |

---

### Marketplace Account Deletion (required by eBay)

eBay requires every production app to expose a notification endpoint for
Marketplace Account Deletion/Closure. This app serves one at
`/api/sync/ebay/marketplace-account-deletion` (exempt from the API-key gate,
since eBay's servers call it):

- **GET `?challenge_code=…`** — eBay's handshake. The response is
  `{ "challengeResponse": sha256(challengeCode + verificationToken + endpointUrl) }` (hex).
- **POST** — a `MARKETPLACE_ACCOUNT_DELETION` notification. The handler deletes
  the locally stored eBay tokens, turns eBay sync off, and only then returns
  `200 {"status":"acknowledged"}`; any cleanup failure returns 500 so eBay retries.

Configuration (all in `.env`):

| Variable | Meaning |
|---|---|
| `EBAY_VERIFICATION_TOKEN` | 32–80 characters; must match what you enter in the eBay Developer Portal |
| `EBAY_NOTIFICATION_ENDPOINT_URL` | The exact public HTTPS URL registered with eBay (it is part of the challenge hash) |
| `EBAY_REDIRECT_URI` | OAuth callback; defaults to the request's own host/protocol behind the Caddy proxy |

This endpoint must be reachable from the public internet over HTTPS, so it
can't be verified end to end from a laptop — register the URL in the portal
(or use a tunnel while developing). The handshake and notification logic are
covered by unit and route tests.
Every deletion notification's `X-EBAY-SIGNATURE` header is verified before
anything is purged: the connector fetches eBay's public key for the header's
`kid` from the Notification API (so `EBAY_CLIENT_ID`/`EBAY_CLIENT_SECRET` are
required; keys are cached for an hour) and checks the ECDSA signature over the
raw body, falling back to `JSON.stringify(body)`, the form eBay's SDKs sign.
Missing/invalid signatures and unknown `kid`s get `412`; if the key can't be
fetched the endpoint answers `503` so eBay retries.

On the **Netlify Function** the rules differ, because that deploy stores no eBay user data:

- If `EBAY_VERIFICATION_TOKEN` or `EBAY_NOTIFICATION_ENDPOINT_URL` is missing, the Function returns `500` and logs which variable is missing. It never hashes with an empty token.
- A valid notification is acknowledged with `200` and nothing is purged. The log line contains only the topic and `notificationId`, never the username or user ID.
- The signature is still verified when `EBAY_CLIENT_ID`/`EBAY_CLIENT_SECRET` are set. Without them the Function acknowledges after checking the payload shape; since there is nothing to purge, a forged notification has no effect.
- Removing eBay data from users' browsers is the `ebay_revoked` cleanup above; a server push can't reach a browser.

**Go-live steps (production keyset):**

1. In Netlify, set `EBAY_VERIFICATION_TOKEN` (`openssl rand -hex 32`) and `EBAY_NOTIFICATION_ENDPOINT_URL` (see the table above).
2. Deploy.
3. Check the hash: `curl "https://lifefire.netlify.app/api/sync/ebay/marketplace-account-deletion?challenge_code=test"` must return the same value as `printf '%s' "test$EBAY_VERIFICATION_TOKEN$EBAY_NOTIFICATION_ENDPOINT_URL" | sha256sum`.
4. developer.ebay.com → Application Keys → Production keyset → Notifications → Marketplace Account Deletion: enter an alert email, the endpoint URL and the verification token → Save → Send Test Notification.

### Sales-report CSV upload

Besides the API sync, the Side Gig Ledger accepts eBay Seller Hub
*Listings sales report* CSVs (Seller Hub → Performance → Sales → Download).
Revenue is item sales plus shipping paid by the buyer; expenses are total
selling costs plus shipping labels you bought. Rows are keyed by eBay item ID
plus the report's date range: re-uploading a report is skipped, and a later
report whose range contains an earlier one replaces those rows.

## CoinTracker (Wallet Discovery & Balances)

**Purpose:** Pull every wallet and exchange account the user already tracks in CoinTracker, with current USD balances, so they don't have to add each address and chain by hand.
**Status:** Implemented and optional. Live-tested 2026-10-01: login works, but the MCP server needs `mcp:read`, which CoinTracker grants only to accounts enrolled in MCP early access (see "Token audience" below).
**Auth type:** OAuth 2.1 Authorization Code + PKCE, public client, dynamic client registration

### What CoinTracker offers

CoinTracker has **no public REST API and no personal read token**. Its only programmatic surface is the remote MCP server at `https://mcp.cointracker.com/mcp`, which accepts only OAuth bearer tokens. Its metadata (`/.well-known/oauth-protected-resource`) names the Auth0 tenant `https://login.cointracker.com/` and the scopes `mcp:read`/`mcp:write`. The tenant supports dynamic client registration (`/oidc/register`), PKCE `S256`, public clients (`token_endpoint_auth_method: none`), refresh tokens (`offline_access`) and revocation. CoinTracker describes MCP as read-only and, as of 2026-10, in early access for paid plans. A `403` from the MCP server is reported as "CoinTracker MCP may require a paid plan or early access".

The Cloudflare layer in front of CoinTracker rejects the default Node/undici user agent with `403`, so every server-side request sends `User-Agent: fire-tracker/…`. The MCP endpoint has no CORS, so the browser can't call it directly and the server brokers every call.

### Flow (identical on Express and Netlify)

| Path | What it does |
|---|---|
| `GET /api/sync/cointracker/authorize` | Registers a public client (or uses `COINTRACKER_CLIENT_ID`), creates the PKCE verifier and `state`, stores them in a 10-minute **encrypted** HttpOnly cookie, and redirects to CoinTracker |
| `GET /api/sync/cointracker/callback` | Checks `state`, exchanges the code with the verifier, seals `{access, refresh, expiry, client_id}` with `SYNC_MASTER_KEY`, and returns it to the SPA at `/#cointracker-connected=…`. Only the tab that started the connect accepts it |
| `POST /api/sync/cointracker/sync` | Body `{token}`. Refreshes the token when it has expired (or once after a `401`), calls the MCP balance tool, and returns normalized `wallets`, plus a new `token` if it refreshed |
| `POST /api/sync/cointracker/inspect` | Body `{token}`. Returns the MCP tool catalog (names, descriptions, argument names; no portfolio data) and which tool is used for balances |
| `POST /api/sync/cointracker/disconnect` | Body `{token}`. Revokes the refresh token (best effort) |

Express serves these from `app/routes/cointracker.js`, and the Netlify deploy from `netlify/functions/cointracker.mjs`. Both wrap `app/lib/cointracker-handlers.js` and `app/lib/cointracker-connector.js` (OAuth, a minimal Streamable-HTTP MCP client, and the normalizer). **Nothing is stored server-side** in either runtime. The browser keeps the sealed token in `localStorage` (`fire_cointracker_token`, outside `fire_tracker_state`, so JSON backups never carry it). Rotating `SYNC_MASTER_KEY` disconnects every browser.

The callback is exempt from the Express `FIRE_API_KEY` gate, because it is a browser redirect from CoinTracker (like the Drive callback). The encrypted state/PKCE cookie is its trust boundary.

### What's fetched and how it's used

- **Read:** wallets and accounts with name, chain(s), public addresses or ENS, current USD value, and per-asset holdings (symbol, quantity, USD value).
- **Never read:** transactions, cost basis, P&L, tax lots or reports. That stays in CoinTracker. fire never requests `mcp:write`, private keys or signing.
- Each wallet becomes one `customAccounts` row: `type: 'Crypto'`, `source: 'cointracker'`, `cointracker: {providerId, kind, chains, addresses, holdings, syncedAt}`. The dashboard's crypto total is the sum of these rows, and each row holds one wallet's value. The account table tags them **CoinTracker**, with the sync time in the tooltip.

### Dedupe (CoinTracker is the source of truth)

The logic is in `app/lib/cointracker-merge.js`, which is pure and unit-tested:

- A manual Crypto account whose identifier (address or ENS, case-insensitive) matches a CoinTracker wallet address is **adopted**. It keeps its id, name and APY, takes CoinTracker's value, and its manual `value`/`identifier`/`quantity` move to `manualSnapshot`. Disconnecting restores it exactly.
- Manual Crypto rows with no address, or with a ticker that CoinTracker also holds, are listed as **possible duplicates** in the card. They are never changed automatically.
- A wallet missing from a **partial** sync (nothing recognized, or an empty result) is kept, and so is one CoinTracker still lists but returned without a USD value this time. A wallet is removed only after a complete sync without it.
- All CoinTracker calls from the browser run one at a time across tabs (Web Locks), and every server request has a 15-second timeout. Auth0 rotates refresh tokens, so two parallel refreshes of the same token would break the connection. A token refreshed before a failure is still returned to the browser.
- Excluding a wallet in the card, or deleting its row, adds its id to `state.coinTrackerExcluded`, and later syncs skip it.
- When a wallet in `/api/wallets` has an address that CoinTracker reports, the MCP server's `get_net_worth` doesn't count it a second time, and `get_wallets` flags it `coveredByCoinTracker`.

Direct-chain tracking (Etherscan and the others below) is unchanged and still works without CoinTracker.

### Token audience

The first live connect (2026-10-01) logged in fine, but the MCP server rejected the token (`401 invalid_token`), even after a refresh. Auth0 issues a JWT for an API only when the authorize request names it as `audience`; otherwise it returns an opaque token for `/userinfo`. The connector now sends `audience` (default: the MCP URL) alongside `resource`. If the MCP server still rejects the token, the card shows the token's shape (`jwt`/`opaque`, `aud`, `scope`; never the token itself). If CoinTracker's login rejects the audience, its error is passed through to the card. Use `COINTRACKER_AUDIENCE` to try another value, or `none` to omit it.

Live result (2026-10-01): with `audience`, Auth0 issues a correct MCP-audience JWT, but `permissions: []` and the scope has no `mcp:read`. CoinTracker's Auth0 RBAC grants `mcp:read` only to accounts enrolled in MCP early access. The card now reports this as "Your CoinTracker account doesn't have MCP access yet" (`cointracker_no_access`). Once CoinTracker enables the account, connect again; no code change is needed.

### Tool selection (provisional)

CoinTracker doesn't publish its MCP tool catalog, so the connector picks the balance tool by name and description. The tool must be about wallets or accounts **and** balances or holdings, take no required arguments, and not be about transactions, tax, gains or history. The output is read from `structuredContent` or JSON text, and normalized defensively (common key spellings for name, address, chain, USD value and holdings). After connecting a real account, use **Inspect CoinTracker tools** in the card. If the connector picks the wrong tool, pin the right one with `COINTRACKER_BALANCE_TOOL`.

### Env vars

```dotenv
SYNC_MASTER_KEY=              # required: seals the token and the OAuth cookie
COINTRACKER_CLIENT_ID=        # optional: pre-registered public client; otherwise dynamic registration on each connect
COINTRACKER_REDIRECT_URI=     # optional: defaults to <request origin>/api/sync/cointracker/callback
COINTRACKER_BALANCE_TOOL=     # optional: exact MCP tool name to read balances from
COINTRACKER_AUDIENCE=         # optional: Auth0 audience (default: the MCP URL); `none` omits it
```

---

## Multichain Wallet Value (keyless)

**Purpose:** Value an ENS name or 0x address as one USD total across chains: native coins plus ERC-20 tokens. Used by the crypto account ⟳ Refresh and the ENS lookup card.
**Status:** Live on Express and Netlify (`app/lib/multichain-balance.js`)
**Auth type:** None. No API keys, no registration.

| Chains | Source | What's read |
|---|---|---|
| Ethereum, Base, Optimism, Arbitrum One, Polygon | Blockscout public API v2 (`eth.blockscout.com`, `base.blockscout.com`, `explorer.optimism.io`, `arbitrum.blockscout.com`, `polygon.blockscout.com`) | `GET /api/v2/addresses/{addr}` (native balance + USD rate) and `/token-balances` (every token, with USD rate) |
| BNB Smart Chain, Avalanche | publicnode.com RPCs (`eth_getBalance`) + Yahoo Finance `BNB-USD`/`AVAX-USD` | Native balance only |

- ENS names are resolved with `ensdata.net` (`crypto-balance.js`). The hosted function doesn't use the `ethers` resolver, which Netlify's bundle doesn't ship.
- **Spam filter:** a token counts only if it is ERC-20, Blockscout prices it, it isn't flagged `scam`, it has at least 50 holders, and it's worth at most $10M in this wallet (a guard against fake prices on illiquid tokens).
- **Partial results:** each chain is fetched on its own with a 10 s timeout. A failed chain comes back `ok: false` with a warning, the rest still count, and the result is marked `partial` (shown as ⚠ on the row and in the ENS card). The lookup fails only if every chain fails.
- **What's stored:** the account's `value` (the total), `chainBreakdown` (chains holding ≥ $0.01, largest first, top 3 tokens each) and `valuePartial`. Full token lists are not stored.
- **Endpoints:** `POST /api/accounts/:id/refresh-crypto` (Express) and the stateless `POST /api/accounts/refresh-crypto` `{identifier, quantity}` (Netlify `fire-api`; the browser saves the result). Both runtimes also serve `GET /api/wallets/ens/:name`.
- **Not covered:** NFTs, DeFi positions (LP/staking), chains outside the seven above, and tokens Blockscout doesn't price. CoinTracker (above) covers those once MCP access is enabled.

The Etherscan-family keys below are still used by the server-side **wallet tracker** (`/api/wallets`, `app/lib/web3-prices.js`), not by crypto accounts.

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
**Auth type:** User OAuth 2.0 (the only mode the code supports; there is no service-account option)

### Setup (Google OAuth)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project (or use existing)
3. Enable the **Google Drive API**
4. Go to **APIs & Services → Credentials** → create an **OAuth client ID** of type *Web application*
5. Add the redirect URI `http://localhost:3001/api/backup/drive/callback` (or your `GDRIVE_REDIRECT_URI`) and copy the client ID and secret
6. Optionally create a Drive folder and put its ID in `GDRIVE_BACKUP_FOLDER_ID`; otherwise `fire-tracker-backups` is created automatically
7. Configure the Google OAuth consent screen and authorize the account through `/api/backup/drive/authorize`.
8. `SYNC_MASTER_KEY` encrypts the stored Drive OAuth token and every backup before upload.

### Env Vars

```dotenv
GDRIVE_CLIENT_ID=                                    # Google OAuth 2.0 Web application client ID
GDRIVE_CLIENT_SECRET=                                # Google OAuth 2.0 Web application client secret
GDRIVE_REDIRECT_URI=                                  # Optional; defaults to the local callback URL
GDRIVE_BACKUP_FOLDER_ID=                              # Optional: Drive folder ID (auto-created if blank)
SYNC_MASTER_KEY=                                      # Required: 64 hex chars (openssl rand -hex 32); encrypts backups and the Drive token
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

### Browser-only deploy (Netlify Function)

`netlify.toml` rewrites every `/api/sync/plaid/*` path to `netlify/functions/plaid.mjs`. That rule comes before the generic `/api/*` fallback.

- No access token is stored on the server. The function returns the linked items to the browser in an AES-256-GCM token, sealed with a key derived from `SYNC_MASTER_KEY`. The browser keeps it in `localStorage` (`fire_plaid_hosted_token`). The token also carries the transaction cursor.
- The token has a rolling 180-day expiry that renews on every call.
- If the token is expired or can't be read, the function returns `401 {"code":"INVALID_TOKEN"}`. The browser then clears the token so the user can link again. A new link doesn't need the old token to be readable.
- Accounts, positions and transactions return `syncedItemIds`, `failedItems` (`{ itemId, code }`, where `code` is Plaid's `error_code`) and a `warning` when the sync is partial. The browser merges data only for the items that synced.

The site is public, so the function is locked with an owner key:

| Variable | Value |
|---|---|
| `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ENV` | As for Express |
| `SYNC_MASTER_KEY` | 64 hex characters. The function returns 503 before calling Plaid if it is missing or malformed. |
| `PLAID_HOSTED_ACCESS_KEY` | Required whenever `PLAID_ENV` is not `sandbox`. Every request must send it in the `x-fire-plaid-access` header. The browser asks for the key once and stores it in `localStorage`. Without it, anyone could link Items, which are billed per Item, on this deploy's Plaid credentials. |

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
| eBay Order API | ✅ Live | `EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `SYNC_MASTER_KEY` |
| Etherscan (ETH wallets) | ❌ Phase 1 | `ETHERSCAN_API_KEY` |
| BscScan (BNB wallets) | ❌ Phase 1 | `BSCSCAN_API_KEY` |
| Polygonscan (MATIC wallets) | ❌ Phase 1 | `POLYGONSCAN_API_KEY` |
| Arbiscan (ARB wallets) | ❌ Phase 1 | `ARBISCAN_API_KEY` |
| Basescan (BASE wallets) | ❌ Phase 1 | `BASESCAN_API_KEY` |
| Routescan (Avalanche wallets) | ❌ Phase 1 | `ROUTESCAN_API_KEY` (optional) |
| Blockstream (Bitcoin) | ❌ Phase 1 | None |
| Solana RPC | ❌ Phase 1 | None |
| CoinGecko prices | ❌ Phase 1 | None (optional key) |
| Google Drive backup | 🟡 Implemented; round-trip verification pending | `GDRIVE_CLIENT_ID`, `GDRIVE_CLIENT_SECRET`, `SYNC_MASTER_KEY` |
| NHTSA VIN decode | ❌ Phase 1 | None |
| Vehicle value API | ❌ Phase 1 | `VEHICLE_VALUE_API_KEY` |
| Plaid (Fidelity/bank sync) | ✅ Live on the hosted deploy — `netlify/functions/plaid.mjs`, reached at `/api/sync/plaid/*` via the `netlify.toml` redirects. No `app/api/sync/plaid` route exists, so self-hosted Express does not serve it. | `PLAID_CLIENT_ID`, `PLAID_SECRET` |
| Alpha Vantage / Polygon.io | ✅ Live | `ALPHA_VANTAGE_API_KEY` or `POLYGON_API_KEY` |

---

## Precious Metals (Gold / Silver Spot)

Gold and silver accounts (`Metal` type, weight in troy oz) are valued as
weight × spot by `app/lib/metals-prices.js`, via `POST /api/accounts/:id/refresh-metal`.

- **Free default** — Yahoo Finance COMEX futures (`GC=F` gold, `SI=F` silver); no key needed.
- **Optional** — set `METALS_API_KEY` to prefer the metals.dev API; failures fall back to Yahoo.
