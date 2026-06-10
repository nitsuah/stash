# opencut — Legacy OpenCut Video Editor (Archived)

**Last Validated:** 2026-06-10 | Initial vault entry
**Upstream:** https://github.com/opencut-app/opencut (active rewrite)
**Branch convention:** N/A (archived; active work in upstream)

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Status | Archived | Legacy codebase — no longer maintained in this fork |
| Active rewrite | External | `opencut-app/opencut` is the canonical active repo |
| MCP controller | See [[repos/opencut-controller]] | `opencut-controller` wraps the editor via Playwright |

---

## Stack

- **Web app:** Next.js (App Router)
- **Desktop:** GPUI native app (in progress at time of archive)
- **Core:** Rust + WASM (GPU compositor, effects, masks)
- **Database:** Postgres + Redis (via Docker Compose)
- **Runtime:** Bun

---

## PMO Findings

- This copy is archived — the upstream `opencut-app/opencut` is the live repo we interact with via `opencut-controller`.
- docs/ contains architecture notes for key subsystems: actions, effects-renderer, keyframes, countries-search.
- No standard PMO planning files (ROADMAP/TASKS/FEATURES/METRICS) — only README and docs/.

---

## Priority Focus

1. Keep this copy for local reference only — do not contribute back to archived fork.
2. Sync docs/ from upstream if major architecture changes occur.
3. Use `opencut-controller` (MCP server) for all programmatic editor interactions.

---

## Key Commands

```bash
# Local dev (Bun required)
cp apps/web/.env.example apps/web/.env.local
docker compose up -d db redis serverless-redis-http
bun install && bun dev:web
# → http://localhost:3000

# Docker full-stack
docker compose up -d
# → http://localhost:3100
```

---

## Active PMO

No active PMO. Archived repo — reference only. See [[repos/opencut-controller]] for active automation work.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/opencut/README|README]] · [[repos/opencut/OpenCut-AGENTS|OpenCut-AGENTS]]

**docs/:** [[repos/opencut/docs/actions|Actions]] · [[repos/opencut/docs/effects-renderer|Effects Renderer]] · [[repos/opencut/docs/keyframes|Keyframes]] · [[repos/opencut/docs/countries-search|Countries Search]]
