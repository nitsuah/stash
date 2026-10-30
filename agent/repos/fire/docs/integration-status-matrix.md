---
up: "[[repos/fire]]"
title: "fire · integration-status-matrix"
source: https://github.com/nitsuah/fire/blob/main/docs/integration-status-matrix.md
kind: repo-doc
repo: fire
---

# Integration connection-status matrix

> 🧭 [fire](../README.md) · [Integrations](./integrations.md) · [Security hardening](./security-hardening.md) · **Status matrix** <!-- nav -->

What every connector reports about itself, in both deploy modes, and where
that answer comes from. Part of #262; the per-provider fixes are #293
(Plaid), #294 (CoinTracker), #219 (Etsy) and #292 (deploy-mode signal).

The rule this doc enforces: **the card must distinguish five states** —
not configured, not connected, connected-never-synced, last sync failed,
and re-link required. A single `connected: false` cannot express that, and
"Not Linked" on a deploy with no credentials sends the user to a Link flow
that can only fail.

## Where the credential lives

| Provider | Self-hosted | Hosted (Netlify) | Status endpoint |
| --- | --- | --- | --- |
| eBay | `data/tokens-ebay.json` (encrypted with `SYNC_MASTER_KEY` when set) | browser `localStorage`, sealed blob | `/api/sync/ebay/status` (Express only — the browser answers from its own blob) |
| Etsy | `data/tokens-etsy.json` | browser `localStorage`, sealed blob | `/api/sync/etsy/status`; hosted function reports `configured` only |
| Plaid | `data/tokens-plaid.json` | browser, sealed `plaidToken` | `/api/sync/plaid/status` in both runtimes |
| CoinTracker | none — browser-held in **both** modes | browser `localStorage`, sealed blob | `/api/sync/cointracker/status` in both runtimes (#294) |
| Google Drive backup | `data/tokens-gdrive.json` | sealed per request, browser-held | `/api/backup/drive/status` in both runtimes |

CoinTracker is the one deliberate inversion: it keeps no server-side token
even when self-hosted, because its token was browser-sealed from the start.
Its status call therefore takes the blob in an `Authorization` header.

## What each endpoint can say

| Provider | `configured` | `connected` | last-sync outcome | re-auth signal |
| --- | --- | --- | --- | --- |
| eBay | **no** — absent from the payload (#301) | token file present | `lastSync` timestamp only (#301) | partial: a revoked grant drops the token, next status reads disconnected |
| Etsy | yes | token file present | `lastSync` timestamp only (#302) | known codes surface on sync, not on status |
| Plaid | yes | items present | `lastSync: { at, ok, errorCode }` (#293) | yes — `reauthRequired` from a per-item `lastErrorCode` |
| CoinTracker | yes | sealed blob unseals (#294) | client-side `lastSync` key | yes — an unsealable blob is reported disconnected and dropped |
| Drive backup | yes — `clientConfigured` + `masterKeySet` | server: token file; hosted: `authorized` is always `false` and the browser decides | none | a 401 with `gdrive_token_invalid` drops the sealed grant |

## The five states, per provider

"Not yet synced" means connected with no completed sync. "Re-link" means
the grant is dead and retrying can never fix it — only the user can.

| Provider | Not configured | Not connected | Connected, never synced | Sync failed | Re-link required |
| --- | --- | --- | --- | --- | --- |
| Plaid | `configured: false`, Connect hidden | `connected: false` | `connected: true`, `lastSync: null` | `lastSync.ok === false` + `errorCode` | `reauthRequired: true` |
| CoinTracker | `configured: false`, Connect hidden | `connected: false` | `connected: true`, no last-sync key | sync error toast, blob kept | blob unsealable → dropped |
| Etsy | `configured: false`, Connect hidden | `connected: false` | `lastSync: null` | sync error surfaces the provider code | revoked grant → blob dropped |
| eBay | **not expressed** — see #301 | `connected: false` | `lastSync: null` | sync error surfaces the provider code | revocation drops the token |
| Drive backup | `clientConfigured`/`masterKeySet` false | `authorized: false` | authorized, never backed up | backup error surfaces `driveReason` | 401 `gdrive_token_invalid` drops the grant (hosted suite only) |

## Verification status

Recorded 2026-10-26 from code and the unit suites — **not** from a live run
against provider accounts. Each cell says which test pins the behavior it
describes; an empty cell means nothing pins it yet.

| Provider | Pinned by |
| --- | --- |
| Plaid (both runtimes) | `tests/unit/sync-plaid-route.test.mjs`, `tests/unit/netlify-plaid.test.mjs` |
| CoinTracker (both runtimes) | `tests/unit/cointracker-status.test.mjs` |
| Etsy | `tests/unit/sync-etsy-route.test.mjs`, `tests/unit/netlify-etsy-function.test.mjs` |
| eBay | `tests/unit/sync-ebay-route.test.mjs` — pins the 503 on authorize when credentials are missing, but no `configured` status case and no hosted status case |
| Drive backup | `tests/unit/gdrive-backup.test.mjs`, `tests/unit/netlify-gdrive-backup.test.mjs` — the `gdrive_token_invalid` handling is pinned only in the hosted suite; the self-hosted route has no revoked-grant case |

Not verified here, and not something a code read can establish:

- **Revoking a grant at the provider** (Etsy/eBay/Plaid/Drive dashboards) and
  confirming the next status call flips to re-link. Needs live accounts.
- **A live Link → exchange → sync run** on `lifefire.netlify.app` for Plaid,
  which `docs/TASKS.md` already tracks as open.
- **The hosted eBay card**, which has no server status endpoint to ask (#301).

## Known divergences

Filed as follow-ups rather than left implicit:

1. **eBay reports no `configured` state, in either mode.** A self-hosted deploy
   with no `EBAY_CLIENT_ID` reads identically to one whose token was revoked.
   The hosted side has no status endpoint at all — the browser answers from its
   own `localStorage` blob, so it cannot tell "no blob" from "no credentials".
   Filed as #301.
2. **Etsy and eBay report no last-sync *outcome***, only a timestamp, so a
   failed sync is indistinguishable from a successful one after a reload.
   Etsy is #302; eBay is covered by #301.
3. **The hosted Drive card always receives `authorized: false`** and overrides
   it from the browser blob. That is intentional (the server never holds the
   grant) but it means the endpoint's `authorized` field must never be trusted
   by a consumer other than the card.
