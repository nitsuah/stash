---
up: "[[repos/stash]]"
title: "stash · OAUTH-INVENTORY"
source: https://github.com/nitsuah/stash/blob/main/docs/security/OAUTH-INVENTORY.md
kind: repo-doc
repo: stash
---

# OAuth / OIDC client inventory

Tracking: nitsuah/stash#302. Never put client IDs, secrets, or tokens in this file or in public issues.
Last verified: 2026-10-28 (read-only console review). Console state that cannot be read from code is marked "unverified".

## Verified clients

| Repo | Provider | Console project / app | Client | Publishing / state | Logo on consent screen | Notes |
|------|----------|-----------------------|--------|--------------------|------------------------|-------|
| ats-fill | Google | `auto-apply` | `ats-fill` (web) | In production, External | none uploaded | Chrome Web Store publish; users bring their own profile-import clients |
| fire | Google | `lifefire` | `lifefire` (web) | In production, External | none uploaded | Drive backup |
| fire | eBay | developer app `lifefire` (sandbox + production keysets) | - | consent title "lifefire" | n/a | branding is set per redirect name in the eBay developer portal |
| vhs | Google | `vhsdb` | `vhsbox` (web) | In production, External | none uploaded | optional sign-in |
| skyview | Google | `skyview` | `skyview-auth` (web) | In production, External | none uploaded | sign-in |
| vigil | GitHub | OAuth app `overseer` (+ `overseer-test` for local dev) | - | exact HTTPS callback | app still named for vigil's former name | redirect matching mode to be reviewed |

## Not found or not audited

| Repo | Status |
|------|--------|
| gcp | no live Google client found in any project; confirm whether its OAuth is unused or lives in a removed project |
| bb-mcp | Blackboard / OIDC consoles not reviewed |
| fire (CoinTracker) | provider-controlled flow; only the redirect back is ours; not audited |
| stash | OAuth/OIDC/SAML code here is reference material; confirm none is deployed |

## Code signals (auto-detected; unverified)

| Repo | Provider signals (files) | Google scopes referenced | Auth libraries (files) | Env var names (sensitive) | Console verification |
|---|---|---|---|---|---|
| 9router | open-sse/config/appConstants.js, open-sse/providers/registry/antigravity.js, open-sse/providers/registry/gemini-cli.js, open-sse/providers/registry/github.js | cclog, cloud-platform, experimentsandconfigs, userinfo.email, userinfo.profile | open-sse/executors/chatgpt-web.js, open-sse/executors/chatgpt-web/adapter.js, open-sse/executors/perplexity-web.js | AG_KEY, API_KEY, API_KEY_SECRET, AUTH_COOKIE_SECURE, DEBUG_BACKGROUND_TOKEN_REFRESH, DISABLE_BACKGROUND_TOKEN_REFRESH, DS_KEY, GLM_API_KEY | TBD |
| ats-fill | CHROMEWEBSTORE.md, lib/oauth.js, manifest.json, scripts/publish-chrome-web-store.mjs | chromewebstore | - | CWS_CLIENT_ID, CWS_CLIENT_SECRET, CWS_REFRESH_TOKEN | TBD |
| bb-mcp | - | - | src/config.ts, src/index.ts, tests/config.test.ts | BB_CLIENT_ID, BB_CLIENT_SECRET, BB_OAUTH_AUTHORIZATION_PATH, BB_OAUTH_REDIRECT_URI, BB_OAUTH_SCOPE, BB_OAUTH_TOKEN_PATH, MCP_API_KEY, RATE_LIMIT_ADMIN_PER_MINUTE | TBD |
| fire | app/lib/gdrive-backup.js, docs/privacy-policy.md, tests/unit/gdrive-backup.test.mjs, tests/unit/netlify-gdrive-backup.test.mjs | drive.file | app/lib/cointracker-connector.js | ALPHA_VANTAGE_API_KEY, COINGECKO_API_KEY, COINTRACKER_AUTH_BASE, COINTRACKER_CLIENT_ID, EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN, EBAY_VERIFICATION_TOKEN | TBD |
| gcp | gcp/gcp_setup.py, tests/test_gcp_setup.py | calendar, drive, drive.file, drive.metadata.readonly, gmail.modify | gcp/copy_folder.py, pyproject.toml | CLIENT_ID_ENV_VAR, ENCRYPTION_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET | TBD |
| skyview | netlify/functions/api-auth-google.mjs | - | - | GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, JWT_SECRET, PORTAL_SALT, RESEND_API_KEY, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET | TBD |
| stash | agent/repos/ats-fill/CHROMEWEBSTORE.md, agent/repos/fire/docs/privacy-policy.md, sso/oauth2.py | - | backend/express/app.js, backend/express/package.json, backend/flask/app.py | JWT_SECRET, PAGERDUTY_ROUTING_KEY, SLACK_WEBHOOK_URL, VIGIL_MCP_KEY | TBD |
| vhs | tests/auth.test.js | - | package.json, src/modules/auth.js | EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, JWT_SECRET, OMDB_API_KEY, TMDB_KEY | TBD |
| vigil | - | - | app/HomeDashboard.tsx, app/layout.tsx, app/pmo/page.tsx | ANTHROPIC_API_KEY, AUTH_REDIRECT_PROXY_URL, AUTH_URL, BYOK_ANTHROPIC_API_KEY, BYOK_ENCRYPTION_KEY, BYOK_GEMINI_API_KEY, BYOK_OPENAI_API_KEY, GEMINI_API_KEY | TBD |
