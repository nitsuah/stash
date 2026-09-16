# Darkmoon API Reference

## HTTP Endpoints

### `GET /health`

Operational status endpoint. Used by the Docker `HEALTHCHECK`, the Render
`healthCheckPath`, and any external uptime monitor. Always returns JSON.

```json
{
  "status": "ok",
  "timestamp": "2026-08-27T17:43:09.096Z",
  "uptimeSeconds": 4,
  "activePlayers": 0,
  "activeGames": 0,
  "maxPlayers": 64,
  "game": { "isActive": false, "mode": "none", "startedAt": null },
  "version": null
}
```

| Field           | Meaning                                                           |
| --------------- | ----------------------------------------------------------------- |
| `status`        | `ok`, or `degraded` once `activePlayers >= maxPlayers`            |
| `uptimeSeconds` | Whole seconds since process start                                 |
| `activePlayers` | Currently connected players                                       |
| `activeGames`   | Matches in progress (0 or 1 under the current single-match model) |
| `game`          | Mode and start time of the active match, if any                   |
| `version`       | `APP_VERSION` when set, otherwise `null`                          |

HTTP status is `200` for both `ok` and `degraded` — a busy but healthy server
should not be cycled by the platform. Only a server that cannot produce a report
returns `503`.

> Route ordering note: the API router is mounted **before** the SPA fallback.
> `req.accepts("html")` is truthy for `Accept: */*`, so a fallback registered
> first would answer `/health` with `index.html`.

### `GET /`

Service status summary: `service`, `status`, `connections`, `activePlayers`,
`activeGames`, `uptimeSeconds`, `timestamp`.

## CORS

One allow-list, configured via `ALLOWED_ORIGINS`, guards both the HTTP app and
the Socket.io handshake, so anything that can reach `/health` can also open a
socket. Entries match literally except for `*`, which is a wildcard within the
entry (used for Netlify deploy previews).

- Allowed origin: request succeeds, `Access-Control-Allow-Origin` is echoed.
- Rejected origin: `403 {"error":"Origin not allowed"}` plus a
  `security.cors_rejected` log record.
- Requests with **no** `Origin` header are allowed (curl, container health
  checks, native clients).

## WebSocket (Socket.io) Events

Multiplayer is still `[planned]`; the events below are implemented server-side
but not yet driven by a shipped client experience.

### Client to server

| Event           | Payload                                    | Notes                                                                                                                                                                                                                                  |
| --------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `move`          | `{ position: [x,y,z], rotation: [x,y,z] }` | Validated and rate limited (100/s)                                                                                                                                                                                                     |
| `chat-message`  | `{ message, playerId, playerName }`        | Validated, profanity filtered, 10/min                                                                                                                                                                                                  |
| `game-start`    | `{ mode }`                                 | Mode must be `tag`/`collectible`/`race`/`solo`                                                                                                                                                                                         |
| `player-tagged` | `{ taggedId }`                             | Tagger is always the sending socket (`client.id`), never a client-supplied `taggerId` — this prevents impersonating the IT player. Rejected unless the sender is currently IT, or if `taggedId` is missing/unknown/equal to the tagger |
| `game-end`      | none                                       | Resets game state and scores                                                                                                                                                                                                           |

### Server to client

| Event           | Payload                                  |
| --------------- | ---------------------------------------- |
| `move`          | Map of all client positions/rotations    |
| `chat-message`  | Filtered message with a server timestamp |
| `game-start`    | `{ ...gameData, itPlayerId, startTime }` |
| `player-tagged` | `{ ...data, scores }`                    |
| `game-end`      | none                                     |
| `error`         | `{ message }` for validation/rate limits |
| `game-error`    | `{ message }` for rejected game actions  |

> `scores` on `player-tagged` is additive; existing clients that ignore the
> field are unaffected.

## Logging

All server output is newline-delimited JSON with `timestamp`, `level`, and a
stable `event` key. See `docs/MULTIPLAYER_GATE.md` for the event catalogue.

## Deployment Contracts

- **Docker**: exposes port 4444, runs as a non-root user, `HEALTHCHECK` asserts
  the `/health` payload, and `SIGTERM` triggers a graceful shutdown.
- **Render**: `healthCheckPath: /health`; `ALLOWED_ORIGINS` set per environment.
- **Netlify**: static frontend only, no server-side multiplayer.
