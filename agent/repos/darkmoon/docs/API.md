# Darkmoon API Reference

## HTTP Endpoints

- `GET /health` — Returns 200 OK if the server is running.

## WebSocket (Socket.io) Events

- **Solo Mode**: No active WebSocket events; all logic is client-side.
- **Multiplayer (Planned)**:
  - `connect` — Player joins a room
  - `player-update` — Sync player state
  - `tag` — Tag action event
  - `disconnect` — Player leaves

## Deployment Contracts

- **Docker**: Exposes port 4444, runs as non-root user, healthcheck on `/`.
- **Netlify**: Static frontend only, no server-side multiplayer.
