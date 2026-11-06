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
(Plaid), #294 (CoinTracker), #219 (Etsy), #292 (deploy-mode signal), and Stripe credential/status #345.

The rule this doc enforces: **the card must distinguish five states** —
not configured, not connected, connected-never-synced, last sync failed,
and re-link required. A single `connected: false` cannot express that, and
"Not Linked" on a deploy with no credentials sends the user to a Link flow
that can only fail.

## Where the credential lives

| Provider | Self-hosted | Hosted (Netlify) | Status endpoint |
| --- | --- | --- | --- |
| eBay | `data/tokens-ebay.json` (encrypted with `SYNC_MASTER_KEY` when set) | browser `localStorage`, sealed blob + sanitized last-sync outcome | `/api/sync/ebay/status`: Express returns configured/connected/lastSyncOutcome; Netlify Function returns `configured` only; hosted connection/outcome state remains browser-local (#326) |
| Etsy | `data/tokens-etsy.json` | browser `localStorage`, sealed blob + local last-sync outcome | `/api/sync/etsy/status`; hosted function reports `configured`, browser adds its local outcome |
| Plaid | `data/tokens-plaid.json` | browser, sealed `plaidToken` | `/api/sync/plaid/status` in both runtimes |
| Stripe | Self-hosted `DATA_DIR/tokens-stripe.json` (AES-256-GCM; `SYNC_MASTER_KEY`) | unavailable — no Netlify function or credential store | `/api/sync/stripe/status`: local configuration/key-format metadata only (#345) |
| CoinTracker | none — browser-held in **both** modes | browser `localStorage`, sealed blob | `/api/sync/cointracker/status` in both runtimes (#294) |
| Google Drive backup | `data/tokens-gdrive.json` | sealed per request, browser-held | `/api/backup/drive/status` in both runtimes |

CoinTracker is the one deliberate inversion: it keeps no server-side token
even when self-hosted, because its token was browser-sealed from the start.
Its status call therefore takes the blob in an `Authorization` header.

## What each endpoint can say

| Provider | `configured` | `connected` | last-sync outcome | re-auth signal |
| --- | --- | --- | --- | --- |
| eBay | yes — Express and Netlify status function both expose `configured` (#322/#324) | self-hosted token file; hosted sealed blob in browser | self-hosted `lastSyncOutcome` from token store (#323); hosted sanitized browser-local outcome survives reload and is replaced on success (#326) | revoked grant drops token and clears the browser outcome; next status is disconnected; live provider revocation remains unverified |
| Etsy | yes | token file present | self-hosted `lastSyncOutcome` from token store; hosted browser-local `lastSyncOutcome` survives reload (#321) | known codes surface on sync; hosted dead-grant path clears the browser outcome |
| Plaid | yes | items present | `lastSync: { at, ok, errorCode }` (#293) | yes — `reauthRequired` from a per-item `lastErrorCode` |
| Stripe | valid 64-hex `SYNC_MASTER_KEY` | valid restricted key present locally (format only) | none — sync not wired | no live provider check; local format is not a re-auth signal |
| CoinTracker | yes | sealed blob unseals (#294) | client-side `lastSync` key | yes — an unsealable blob is reported disconnected and dropped |
| Drive backup | yes — `clientConfigured` + `masterKeySet` | server: token file; hosted: `authorized` is always `false` and the browser decides | none | a 401 with `gdrive_token_invalid` drops the sealed grant |

## The five states, per provider

"Not yet synced" means connected with no completed sync. "Re-link" means
the grant is dead and retrying can never fix it — only the user can.

| Provider | Not configured | Not connected | Connected, never synced | Sync failed | Re-link required |
| --- | --- | --- | --- | --- | --- |
| Plaid | `configured: false`, Connect hidden | `connected: false` | `connected: true`, `lastSync: null` | `lastSync.ok === false` + `errorCode` | `reauthRequired: true` |
| CoinTracker | `configured: false`, Connect hidden | `connected: false` | `connected: true`, no last-sync key | sync error toast, blob kept | blob unsealable → dropped |
| Etsy | `configured: false`, Connect hidden | `connected: false` | `lastSync: null` | `lastSyncOutcome.ok === false` + safe `errorCode` (browser-local when hosted) | revoked grant → token and outcome cleared |
| eBay | `configured: false`, Connect hidden | `connected: false` | self-hosted: `connected: true`, `lastSync: null`; hosted: connected from sealed browser token, `lastSync: null` | self-hosted: `lastSyncOutcome.ok === false` + safe `errorCode`; hosted browser-local `lastSyncOutcome` survives reload (#326) | revoked grant clears token and outcome; next status is disconnected (live account behavior unverified) |
| Drive backup | `clientConfigured`/`masterKeySet` false | `authorized: false` | authorized, never backed up | backup error surfaces `driveReason` | 401 `gdrive_token_invalid` drops the grant (hosted suite only) |
| Stripe | missing/invalid `SYNC_MASTER_KEY` | configured but no valid restricted key | valid local key; sync endpoint not implemented | N/A — no sync outcome | N/A — provider key validity is not checked live |

## Verification status

Recorded 2026-10-31 from code and the unit suites — **not** from a live run
against provider accounts. Each cell says which test pins the behavior it
describes; an empty cell means nothing pins it yet.

| Provider | Pinned by |
| --- | --- |
| Plaid (both runtimes) | `tests/unit/sync-plaid-route.test.mjs`, `tests/unit/netlify-plaid.test.mjs` |
| CoinTracker (both runtimes) | `tests/unit/cointracker-status.test.mjs` |
| Etsy | `tests/unit/etsy-sync-label.test.mjs`, `tests/unit/sync-etsy-route.test.mjs`, `tests/unit/netlify-etsy-function.test.mjs` |
| eBay | `tests/unit/ebay-status.test.mjs` covers safe outcome normalization/storage and hosted sync, OAuth, and lost-grant transitions (#326); `tests/unit/sync-ebay-route.test.mjs` and `tests/unit/netlify-ebay-functions.test.mjs` cover configured/status behavior |
| Drive backup | `tests/unit/gdrive-backup.test.mjs`, `tests/unit/netlify-gdrive-backup.test.mjs` — the `gdrive_token_invalid` handling is pinned only in the hosted suite; the self-hosted route has no revoked-grant case |
| Stripe (self-hosted) | `tests/unit/sync-stripe-route.test.mjs` — credential/status/disconnect behavior; no live provider validation |

Not verified here, and not something a code read can establish:

- **Revoking a grant at the provider** (Etsy/eBay/Plaid/Drive dashboards) and
  confirming the next status call flips to re-link. Needs live accounts.
- **A live Link → exchange → sync run** on `lifefire.netlify.app` for Plaid,
  which `docs/TASKS.md` already tracks as open.
- **Live eBay provider/account behavior** (credential configuration, OAuth round trip, and provider-side grant revocation) remains unverified; the hosted status function is covered only with synthetic environment values. Keep live acceptance on #301.

## Known divergences

Filed as follow-ups rather than left implicit:

1. **Hosted eBay status remains intentionally split.** The Netlify function reports `configured` only; connection and sanitized last-sync outcome are browser-local. The outcome survives reload, later success replaces failure, and OAuth reconnect/lost grant clear it (#326).
2. **eBay live provider/account behavior is not verified by code/tests.** Synthetic tests pin configured/status and hosted outcome transitions, but OAuth, real sync, and provider-side revocation need owner-controlled live acceptance (#301). Etsy hosted outcome is browser-local and the Netlify function remains stateless (#302/#321).

3. **The hosted Drive card always receives `authorized: false`** and overrides
   it from the browser blob. That is intentional (the server never holds the
   grant) but it means the endpoint's `authorized` field must never be trusted
   by a consumer other than the card.

4. **Stripe is self-hosted-only and not yet sync-enabled.** Status reflects local key format/presence and master-key configuration; there is no hosted function, live provider verification, sync route/outcome, or remote key revocation (#345/#346/#409).
