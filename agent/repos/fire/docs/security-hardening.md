?# Security Hardening Plan

> **Status:** Planning  
> **Last updated:** 2026-08-12  
> **See also:** [docs/prod-plan.md](prod-plan.md)

---

## Threat Model

The FIRE Tracker is a locally self-hosted personal finance dashboard. It is **not designed for public internet exposure**. Its threat model is:

- **Primary:** Unauthorized local access — shared machine, physical access, or local network exposure via misconfigured Docker port binding
- **Secondary:** Injected content — malicious CSV files, webhook payloads, or JSONata expressions crafted to extract data or crash the server
- **Tertiary:** Dependency supply chain — npm package compromise in production deps

**Out of scope:** Nation-state actors, hardware attacks, OS-level compromise, browser extensions.

If you intend to expose this server beyond `localhost`, complete all Critical and High items before doing so.

---

## Current Security Inventory

### Implemented

| Control | Where | Strength |
|---|---|---|
| XSS prevention | `html-utils.js` `escHtml()` on all table renderers | Strong |
| CSRF prevention | OAuth `oauthState` consumed immediately on use | Strong |
| HMAC webhook verification | `crypto.timingSafeEqual` on raw request bytes | Strong |
| Atomic writes | write-to-tmp then `renameSync` | Strong |
| Write concurrency | `mutateState()` promise queue | Strong |
| Webhook secret suppression | `omitSecret()` on all list/get responses | Strong |
| Data encryption at rest | AES-256-GCM via `SYNC_MASTER_KEY` | Strong (opt-in) |
| Input validation | Non-empty strings, `Number.isFinite`, YYYY-MM-DD + UTC round-trip | Strong |
| JSONata sandbox | 5-second evaluation timeout with `finally` cleanup | Moderate |
| Session security | `httpOnly: true`, `sameSite: lax` | Moderate |
| API key gate | `X-Api-Key` header (required by default; `FIRE_AUTH_DISABLED=true` opt-out) | Strong |
| HTTPS on localhost | Caddy reverse proxy (`config/Caddyfile`, `tls internal`) via `config/docker-compose.yml` | Strong (opt-in — plain HTTP on 3001 still works directly) |
| MCP server is read-only | No tool calls `writeState`/`mutateState`; locked in by `tests/unit/mcp-server-read-only.test.mjs` | Strong |
| Global error handler | 500 JSON response — no stack trace exposed | Moderate |
| event delegation pattern | `data-*` attributes for onclick — no inline handler injection | Strong |
| Yahoo Finance abort | `AbortSignal.timeout(10000)` on all fetch calls | Moderate |

### Gaps

| Gap | Impact | Severity |
|---|---|---|
| No rate limiting on /api/* | Brute-force API key, DoS | High |
| SESSION_SECRET fallback to hardcoded string | Session forgery if default used | High |
| Webhook payload size unlimited | Memory exhaustion via large payload | Medium |
| Webhook sideGigLedger entries unvalidated | Schema confusion injection | Medium |
| 6 moderate/critical dev dependency vulns | Supply chain (dev only, not shipped) | Low |
| No npm audit in CI | Vuln regressions undetected | Low |
| No MCP audit log | No visibility into LLM data access patterns | Low |
| JSONata not statically analyzed | Complex expression side effects | Low |
| No key rotation mechanism | Key compromise requires manual db.json reconstruction | Low |

---

## Hardening Roadmap

### Critical — Do before any external-facing deployment

---

#### H-01: Rate Limiting

**Gap:** No request rate limiting on any API endpoint.  
**Risk:** API key brute force, memory exhaustion via rapid state writes, webhook flooding.

```bash
npm install express-rate-limit
```

Apply in `app/server.js`:
```js
import rateLimit from 'express-rate-limit';

const apiLimiter = rateLimit({
  windowMs: 60 * 1000,
  limit: (req) => req.headers['x-api-key'] === process.env.FIRE_API_KEY ? 300 : 30,
  standardHeaders: 'draft-7',
  legacyHeaders: false,
});

const webhookLimiter = rateLimit({
  windowMs: 60 * 1000,
  limit: 60,
});

app.use('/api/sync/webhook', webhookLimiter);
app.use('/api', apiLimiter);
```

---

#### H-02: HTTPS via Caddy Reverse Proxy

**Status: Done.** See `config/Caddyfile` and the `caddy` service in `config/docker-compose.yml`.

**Gap:** Server binds HTTP on 0.0.0.0 inside its container. Any device on the LAN could reach the API and receive tokens in plaintext — adding Caddy alongside the *existing* `fire` service alone would not have closed this, since `fire`'s own port was still published to every host interface (`"3001:3001"`).  
**Fix:** Add Caddy as a TLS-terminating reverse proxy in docker-compose, **and** rebind `fire`'s published port to loopback only (`"127.0.0.1:3001:3001"`, not `"3001:3001"`) so Docker never forwards LAN traffic to it in the first place — regardless of what the container listens on internally. A full unpublish (`expose:` instead of `ports:`) was considered but rejected: `fire`'s port is the configured target for two real OAuth redirect callbacks (eBay, Google Drive — see README.md/.env.example/docs/integrations.md), which browsers reach directly after the provider's auth step; loopback-only binding keeps those working for same-machine use while still closing the LAN-reachability gap this item exists to fix.

`config/docker-compose.yml` addition:
```yaml
services:
  caddy:
    image: caddy:2-alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - fire

volumes:
  caddy_data:
  caddy_config:
```

`config/Caddyfile` for localhost TLS:
```text
localhost {
  reverse_proxy fire:3001
  tls internal
}
```

For LAN IP access with a self-signed cert, add the IP to the Caddyfile and pin the cert in the browser. For a public domain with Let's Encrypt, replace `localhost` with the domain.

---

#### H-03: SESSION_SECRET Fail-Fast

**Gap:** Server starts with a hardcoded fallback `'a-very-secret-key'` — a warning is logged but the server runs.  
**Fix:** Fail-fast in production mode.

In `app/server.js`, after session middleware setup:
```js
if (process.env.NODE_ENV === 'production' &&
    (!process.env.SESSION_SECRET || process.env.SESSION_SECRET === 'a-very-secret-key')) {
  console.error('FATAL: SESSION_SECRET must be a random string in production. Set it in .env.');
  process.exit(1);
}
```

---

### High — Implement in PROD Phase 3

---

#### H-04: FIRE_API_KEY Required by Default

**Status: Done.** See the `AUTH_DISABLED` fail-fast check and `/api` gate in `app/server.js`.

**Gap:** API key auth is opt-in; a fresh install has zero authentication.  
**Fix:** Flip the default. Require the key unless explicitly opted out.

In `app/server.js` API key middleware:
```js
const authRequired = process.env.FIRE_AUTH_DISABLED !== 'true';
if (authRequired) {
  // existing X-Api-Key check; fail if FIRE_API_KEY is unset too
  if (!process.env.FIRE_API_KEY) {
    console.error('FATAL: Set FIRE_API_KEY or set FIRE_AUTH_DISABLED=true for local-only use.');
    process.exit(1);
  }
}
```

Update `.env.example` to document the opt-out.

---

#### H-05: Webhook Payload Size Cap

**Gap:** Webhook receiver applies no body size limit. A large payload could exhaust server memory.  
**Fix:** Limit raw body capture to 16KB on webhook routes (before the existing HMAC check):

```js
// In app/routes/sync.js, before the webhook receiver middleware:
app.use(
  '/api/sync/webhook',
  express.raw({ type: '*/*', limit: '16kb' }),
);
```

---

#### H-06: Webhook sideGigLedger Field Validation

**Gap:** Incoming `sideGigLedger` entries from webhooks are merged into state without field-level checks — any shape is accepted.  
**Fix:** Validate required fields before merging:

```js
function isValidLedgerEntry(e) {
  return (
    typeof e.id === 'string' && e.id.length > 0 &&
    typeof e.description === 'string' &&
    Number.isFinite(e.net) &&
    /^\d{4}-\d{2}-\d{2}/.test(e.date)
  );
}
```

Reject entries that fail validation with a 400 + descriptive error.

---

#### H-07: npm audit in CI

**Gap:** No automated vulnerability gate; regressions can silently enter production deps.  
**Fix:** Add to `.github/workflows/ci.yml`:

```yaml
- name: Audit production dependencies
  run: npm audit --audit-level=high --omit=dev
```

Fail the workflow on high/critical findings in production deps. Dev-only vulns are allowed-list candidates.

---

#### H-08: Security Headers (helmet.js)

```bash
npm install helmet
```

In `app/server.js` before route registration:
```js
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
      styleSrc:  ["'self'", "'unsafe-inline'", "fonts.googleapis.com"],
      fontSrc:   ["'self'", "fonts.gstatic.com"],
      imgSrc:    ["'self'", "data:"],
      connectSrc: ["'self'", "query1.finance.yahoo.com", "finance.yahoo.com"],
    },
  },
  crossOriginEmbedderPolicy: false, // Chart.js CDN compatibility
}));
```

Headers added: `Strict-Transport-Security`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`.

---

### Medium — Implement in PROD Phase 3

---

#### H-09: SYNC_MASTER_KEY Rotation

**Gap:** No mechanism to rotate the encryption key — key compromise means either keeping the compromised key or losing the database.

**New endpoint:** `POST /api/admin/rotate-key` (gated by `FIRE_API_KEY`):
1. Accept `{ newKey: "64-hex-chars" }` in request body
2. Validate `newKey` format
3. Decrypt db.json with the current `SYNC_MASTER_KEY` in memory
4. Re-encrypt with `newKey` using AES-256-GCM with a fresh IV
5. Write atomically (tmp → rename)
6. Return `{ success: true }` — user updates env var and restarts container

The old key is never written to disk during rotation.

---

#### H-10: MCP Audit Log

**Gap:** No visibility into which LLM tools access what data, or when.

Write to `data/mcp-audit.log` (JSON Lines, append-only):
```json
{"ts":"2026-08-12T10:00:00.000Z","tool":"get_portfolio","responseBytes":2341}
```

**Never log:** response content, financial balances, or position values. Only metadata.

Rotate the log file when it exceeds 1MB (rename to `mcp-audit.log.1`, start fresh).

---

#### H-11: MCP Response Identifier Truncation

**Gap:** `get_accounts` and `get_portfolio` return account names verbatim — if an account name contains an account number, it passes through MCP to the LLM context.

**Fix:** In `app/mcp-server.mjs`, sanitize string fields before returning:
- Account names: strip numeric sequences > 6 digits
- Wallet addresses: truncate to `...` + last 8 chars
- Position descriptions: pass through (no numbers to strip)

This is defense-in-depth — properly named accounts ("Fidelity Brokerage") are not affected.

---

### Low — Implement opportunistically

---

#### H-12: JSONata Static Analysis

**Gap:** JSONata expressions are executed after a 5-second timeout but not statically analyzed for dangerous patterns.

**Options:**
- Allowlist expression forms (only field access + arithmetic — no `$eval`, no `$split` on secrets)
- Parse-only pass before execution to detect `$eval` or recursive calls

---

#### H-13: Resolve Dev Dependency Vulnerabilities

6 moderate/critical vulnerabilities exist in dev deps. Dev deps are not shipped in the Docker image (they are not in the production `node_modules` layer). However, running `npm audit fix` for dev deps reduces noise and prevents tooling from being a vector.

Run:
```bash
npm audit fix --save-dev
# Review any breaking changes from major version bumps
```

---

## Penetration Testing Checklist

Run this before any external-facing deployment or after major changes to the sync layer.

### Authentication & Authorization

- [ ] All `/api/*` routes return `401` without valid `X-Api-Key` when key is configured
- [ ] Invalid session cookies are rejected (no 200 response to forged sessions)
- [ ] OAuth CSRF state tokens cannot be reused (send same callback request twice)
- [ ] Rate limiting triggers after threshold (send 35 rapid unauthenticated requests)
- [ ] Rate limit resets after time window (verify limiter uses sliding window, not fixed)

### Injection

- [ ] `POST /api/accounts` with `{ "name": "<script>alert(1)</script>" }` → `escHtml()` sanitizes in all rendered table cells
- [ ] `POST /api/sync/webhook/templates` with malicious JSONata expression (e.g., infinite recursion) → rejects or times out within 5s, no crash
- [ ] `POST /api/sync/webhook/:id` with payload > 16KB → 413 response
- [ ] `POST /api/cds` with `{ "maturity": "'; DROP TABLE cds; --" }` → YYYY-MM-DD validation rejects with 400
- [ ] `POST /api/accounts` with `{ "value": "Infinity" }` or `{ "value": NaN }` → `Number.isFinite` check rejects

### Information Disclosure

- [ ] `GET /api/sync/webhook-templates` does not include `secret` fields in any response
- [ ] Express error responses do not include stack traces (trigger a 500 and inspect response)
- [ ] MCP `get_accounts` does not include raw OAuth tokens
- [ ] `data/db.json` is encrypted when `SYNC_MASTER_KEY` is set (inspect the file directly)
- [ ] `data/tokens.json` is always encrypted (inspect after OAuth callback)

### Transport (when HTTPS/Caddy is enabled)

- [ ] HTTP requests redirect to HTTPS (`301` or `308`)
- [ ] `Strict-Transport-Security` header present on HTTPS responses
- [ ] No `Set-Cookie` without `Secure` flag on HTTPS
- [ ] No sensitive data in URL query parameters (confirm OAuth state is a session value, not URL param)

### Denial of Service

- [ ] Webhook endpoint rejects payloads > 16KB with `413 Payload Too Large`
- [ ] Rate limiter triggers and returns `429` after threshold
- [ ] JSONata evaluation with infinite recursion terminates within 5s
- [ ] `POST /api/state` with a 100MB JSON body is rejected by body-parser limit

### MCP-Specific

- [x] MCP server registers no write tools — see `tests/unit/mcp-server-read-only.test.mjs`: a name-based check, a byte-diff check that db.json is untouched after calling every registered tool (caught and fixed a real violation in `set_price_target_alert`), a write-syscall spy on `fs.writeFileSync`/`renameSync` (catches a same-content rewrite the byte-diff alone can't distinguish from never writing — flagged by CodeRabbit on PR #105), and a static check that the file never references `writeState`/`mutateState` at all
- [ ] MCP server does not make external network calls (run with network blocked; all 8 tools should still respond from db.json)
- [ ] MCP audit log records tool calls without logging response content

---

## What We Intentionally Do Not Harden Against

- **Physical machine access** — if an attacker has shell access, all bets are off. Use OS-level full-disk encryption (BitLocker, FileVault) as the first line of defense.
- **Compromise of SYNC_MASTER_KEY** — back it up offline (password manager, printed paper). If lost, `db.json` is unrecoverable. If stolen without the key, the ciphertext is safe.
- **Browser extension access** — the browser SPA is only as isolated as the browser itself. Use a dedicated browser profile if high security is needed.
- **npm package tampering at install time** — use a lockfile (`package-lock.json`) and verify with `npm ci` in Docker builds. The Dockerfile already uses `npm ci`.
