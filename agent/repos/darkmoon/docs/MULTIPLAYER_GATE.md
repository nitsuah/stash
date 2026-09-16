# Multiplayer Readiness Gate

Last Updated: 2026-08-27

## Purpose

Multiplayer Tag stays `[planned]` in `FEATURES.md` until the server it depends
on is demonstrably deployable, reachable, observable, and debuggable. This
document defines that bar as four criteria, each with a **testable acceptance
check** — a command anyone can run to get a pass/fail answer, not a judgement
call.

This gate covers the **server's readiness to host multiplayer**. It deliberately
does not cover multiplayer _gameplay_ correctness; see "Out of scope" below.

**Current status: all four criteria pass** (verified 2026-08-27).

| #   | Criterion     | Status  |
| --- | ------------- | ------- |
| 1   | Deployment    | ✅ Pass |
| 2   | CORS          | ✅ Pass |
| 3   | Logging       | ✅ Pass |
| 4   | Observability | ✅ Pass |

> **Accepted risk: unauthenticated `/health`.** The endpoint returns active
> player/game counts, capacity, uptime, and version with no auth. This is
> deliberate — Render's `healthCheckPath` and the container `HEALTHCHECK`
> both probe it unauthenticated, and none of the exposed fields are
> per-player identifying data (no player IDs, positions, or chat content).
> The disclosure is aggregate operational status, not gameplay data, so it
> does not block this gate. Revisit if `/health` ever grows a field that
> identifies an individual player.

---

## Criterion 1 — Deployment

**Description.** The server must build into a production image, start from a
clean environment, be reachable through a reverse proxy that can carry
WebSockets, and shut down without dropping the platform's deploy signal.

Requirements:

1. The production image builds (`--target runner`) and starts with no arguments.
2. Configuration is environment-driven (`PORT`, `ALLOWED_ORIGINS`, `LOG_LEVEL`),
   with working defaults, and documented in `.env.example`.
3. The container `HEALTHCHECK` targets `/health` and validates the payload.
4. `SIGTERM` drains connections and exits `0` within 10s (platforms send
   `SIGTERM` on deploy and scale-down; a server that ignores it is killed
   mid-match).
5. The reverse proxy configuration required for WebSocket upgrade is documented.

### Acceptance check

```bash
# 1. Production image builds and boots
docker build --target runner -t darkmoon-prod .
docker run -d --name gate -p 4444:4444 darkmoon-prod

# 2. Graceful shutdown: send SIGTERM, then block until the container actually
# exits (docker wait) instead of inspecting state that may still say "running".
docker kill --signal=SIGTERM gate
EXIT_CODE=$(timeout 10 docker wait gate)   # blocks until exit or 10s timeout
echo "$EXIT_CODE"   # → 0
docker logs gate 2>&1 | tail -n 5 | jq -e 'select(.event == "server.shutdown")'
```

**Pass when** the image builds, the server boots with no arguments, `docker
wait` reports exit code `0` within 10s, and a `server.shutdown` record appears
in the logs.

### Reverse proxy configuration

Socket.io needs the HTTP `Upgrade`/`Connection` headers forwarded, or it
silently degrades to long-polling (and fails outright behind proxies with a
short idle timeout). The timeout must exceed Socket.io's 60s ping interval.

**nginx:**

```nginx
location / {
    proxy_pass         http://127.0.0.1:4444;
    proxy_http_version 1.1;

    # Required for the WebSocket upgrade handshake
    proxy_set_header   Upgrade    $http_upgrade;
    proxy_set_header   Connection "upgrade";

    proxy_set_header   Host              $host;
    proxy_set_header   X-Real-IP         $remote_addr;
    proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Proto $scheme;

    # Must exceed the 60s Socket.io ping interval
    proxy_read_timeout 120s;
    proxy_send_timeout 120s;
}
```

**Caddy:**

```caddy
darkmoon.example.com {
    reverse_proxy 127.0.0.1:4444
}
```

**Render** (current target, `render.yaml`) terminates TLS and forwards
WebSocket upgrades automatically; it needs only `healthCheckPath: /health` and
per-environment `ALLOWED_ORIGINS`. If the app ever sits behind a proxy that sets
`X-Forwarded-For`, enable `app.set("trust proxy", 1)` so `express-rate-limit`
buckets by real client IP instead of the proxy's.

---

## Criterion 2 — CORS

**Description.** A single explicit origin allow-list must guard both the HTTP
app and the Socket.io handshake. Two policies that can drift are a
deployment-day outage: the page loads, then the socket refuses to connect.

Requirements:

1. Allowed origins come from `ALLOWED_ORIGINS`, with a documented default.
2. The **same** policy object is applied to Express and to Socket.io.
3. Wildcards (`*`) work for Netlify deploy previews, and every other character
   matches literally — `darkmoon-dev.netlify.app` must not match
   `darkmoon-devXnetlify.app`.
4. Patterns are anchored, so a suffix like
   `darkmoon-dev.netlify.app.evil.example` is rejected.
5. A rejected origin returns `403` with a JSON body and a log record — not a
   `500` with a stack trace.
6. Requests with no `Origin` header (curl, health checks, native clients) are
   allowed.

### Acceptance check

```bash
npx vitest run src/__tests__/server.cors.test.ts

# Live check against a running server — one request, asserting status code
# AND the echoed header (checking either alone would miss a server that gets
# the other wrong).
STATUS=$(curl -s -D headers-allowed.txt -o body-allowed.json -w '%{http_code}' \
  -H 'Origin: https://darkmoon-dev.netlify.app' localhost:4444/health)
test "$STATUS" = "200" && grep -qi '^Access-Control-Allow-Origin: https://darkmoon-dev.netlify.app' headers-allowed.txt && echo "allowed origin: PASS"

curl -s -D - -o body-rejected.json -w '%{http_code}\n' -H 'Origin: https://evil.example' localhost:4444/health   # → 403
jq -e '.error' body-rejected.json   # rejection body is JSON, not an HTML stack trace
docker logs <container> 2>&1 | tail -n 5 | jq -e 'select(.event == "security.cors_rejected" and .origin == "https://evil.example")'
```

**Pass when** the suite is green, an allowed origin gets `200` with the origin
echoed back in `Access-Control-Allow-Origin`, and an unlisted origin gets `403`
with a JSON body and a matching `security.cors_rejected` log record.

Implementation: `server/cors.js`.

---

## Criterion 3 — Logging

**Description.** Every game event must produce a structured, machine-parseable
record. Debugging a live multiplayer match from prose `console.log` lines is not
viable — an aggregator has to filter by player and event without regex-parsing
sentences.

Requirements:

1. Every record is a single line of JSON carrying `timestamp`, `level`, and a
   stable `event` key.
2. **No** unstructured output on any path, including error handling.
3. The required game events are covered: player connect, player disconnect, tag
   events (accepted _and_ rejected, with a reason), and score changes.
4. Level is configurable via `LOG_LEVEL`.
5. Log context can never overwrite the reserved keys, and unserializable context
   degrades to an error record instead of throwing inside a game handler.
6. Message bodies (chat) are not logged — metadata only.

### Event catalogue

| Event                        | Level | Key fields                                       |
| ---------------------------- | ----- | ------------------------------------------------ |
| `server.started`             | info  | `port`, `allowedOrigins`, `logLevel`             |
| `server.shutdown`            | info  | `signal`, `activePlayers`, `uptimeSeconds`       |
| `player.connected`           | info  | `playerId`, `activePlayers`                      |
| `player.disconnected`        | info  | `playerId`, `activePlayers`, `wasIt`             |
| `game.player_tagged`         | info  | `taggerId`, `taggedId`, `mode`                   |
| `game.tag_rejected`          | warn  | `taggerId`, `taggedId`, `reason`                 |
| `game.score_changed`         | info  | `playerId`, `previousScore`, `newScore`, `delta` |
| `game.started`               | info  | `mode`, `itPlayerId`, `playerCount`              |
| `game.ended`                 | info  | `mode`, `durationMs`, `finalScores`              |
| `chat.message`               | info  | `playerId`, `messageLength` (never the body)     |
| `security.rate_limited`      | warn  | `playerId`, `action`                             |
| `security.validation_failed` | warn  | `playerId`, `field`                              |
| `security.cors_rejected`     | warn  | `origin`, `transport`                            |

### Acceptance check

```bash
npx vitest run src/__tests__/server.logger.test.ts

# Every emitted line must parse as JSON
docker logs <container> 2>&1 | while read -r line; do
  echo "$line" | jq -e . >/dev/null || { echo "NOT JSON: $line"; exit 1; }
done
```

**Pass when** the suite is green and every log line parses as JSON.

Sample output from a full lifecycle:

```json
{"service":"darkmoon-server","port":4444,"logLevel":"info","timestamp":"2026-08-27T17:44:53.173Z","level":"info","event":"server.started"}
{"service":"darkmoon-server","playerId":"fH_QSHUUaSIA2ypO","activePlayers":1,"timestamp":"2026-08-27T17:44:57.325Z","level":"info","event":"player.connected"}
{"service":"darkmoon-server","playerId":"fH_QSHUUaSIA2ypO","activePlayers":0,"wasIt":false,"timestamp":"2026-08-27T17:44:57.928Z","level":"info","event":"player.disconnected"}
{"service":"darkmoon-server","signal":"SIGTERM","activePlayers":0,"uptimeSeconds":7,"timestamp":"2026-08-27T17:45:00.707Z","level":"info","event":"server.shutdown"}
```

Implementation: `server/logger.js`.

---

## Criterion 4 — Observability

**Description.** `/health` must answer "is the server up, and what is it doing
right now?" without shell access — server status, active player count, and
active game count.

Requirements:

1. `GET /health` returns JSON with `status`, `uptimeSeconds`, `activePlayers`,
   `activeGames`, and a `game` summary.
2. It is reachable for **all** `Accept` headers, including `*/*` and
   `text/html`. (Regression guard: the API router must be mounted before the SPA
   fallback — see below.)
3. `status` is `ok`, or `degraded` at/above `maxPlayers`. Both return `200`, so
   a busy-but-healthy server is not cycled by the platform.
4. Counts reflect live socket state.
5. The payload is a pure function of a state snapshot, so it is unit-testable
   without binding a port.

> **Why requirement 2 exists.** The SPA fallback was previously registered
> before the API router. `req.accepts("html")` is truthy for `Accept: */*` —
> which curl, the Docker `HEALTHCHECK`, and platform probes all send — so every
> `/health` request was answered with `index.html` and the endpoint never ran.
> The platform health check "passed" while reporting nothing. Any change to
> middleware order must keep the router first.

### Acceptance check

```bash
npx vitest run src/__tests__/server.health.test.ts

# Require HTTP 200 (a 503 with a plausible-looking body must not pass) and a
# status strictly in {ok, degraded} — jq's truthiness accepts "error" too, so
# the check has to name the allowed values explicitly.
curl -s -o /dev/null -w '%{http_code}\n' localhost:4444/health   # → 200
curl -s localhost:4444/health | jq -e '(.status == "ok" or .status == "degraded") and (.activePlayers >= 0) and (.activeGames >= 0)'
curl -s -H 'Accept: text/html' localhost:4444/health | jq -e '.status'   # must be JSON, not HTML
```

**Pass when** the suite is green, the endpoint returns HTTP `200`, and the body
is JSON with `status` exactly `ok` or `degraded` plus non-negative counts.

Verified live with one connected socket:

```json
{
  "status": "ok",
  "uptimeSeconds": 16,
  "activePlayers": 1,
  "activeGames": 0,
  "maxPlayers": 64,
  "game": { "isActive": false, "mode": "none", "startedAt": null },
  "version": null
}
```

Implementation: `server/health.js`.

---

## Running the whole gate

```bash
# Unit criteria (CORS, logging, observability)
docker compose -f config/docker-compose.yml --profile test run --rm test \
  npx vitest run --config ./config/vitest.config.ts --configLoader runner \
  src/__tests__/server.cors.test.ts \
  src/__tests__/server.logger.test.ts \
  src/__tests__/server.health.test.ts

# Full suite (must stay green)
docker compose -f config/docker-compose.yml --profile test run --rm test
```

## Out of scope

This gate certifies that the server can be **operated**. It does not certify
that multiplayer tag is **correct**. Two known gameplay gaps remain tracked
separately in `TASKS.md` and must also close before Multiplayer Tag ships:

- `player-tagged` enforces no cooldown/freeze window, so server-side tag rules
  do not match the client's `GameManager` parity rules.
- A disconnecting IT player does not hand off or clear `itPlayerId`, so a match
  can be left with nobody IT.

Both are logged (`game.tag_rejected` with a reason, and `wasIt` on
`player.disconnected`), so the gate's observability makes them diagnosable — it
does not make them fixed.
