# Delivery Pipeline Handoff

## Repository Context

- Repository: nitsuah/bb-mcp
- Default branch: main
- Working branch: feat/bb-mcp/manifest-contract-20260403
- PR link: not captured in this handoff snapshot (delivery state recorded as handoff-only in `nitsuah/stash` PR #69)
- Related issue/task: TASKS.md — [Q2-CEO] MCP provider contract

## Work Summary

- Title: Publish discoverable MCP provider manifest endpoint
- Problem statement: agent-board and other clients need a stable contract to discover bb-mcp capabilities and tools without coupling to internals.
- Priority: P1
- Type: Feature
- Requested by: Q2-CEO roadmap/tasks

## Evidence

- Observed behavior: server exposed `/mcp`, `/health`, and `/metrics` but no dedicated provider contract endpoint.
- Reproduction steps: `GET /manifest` returned 404 before this change.
- Confidence: High

## Scope

- In scope:
  - Add manifest builder from exported tool schemas.
  - Add HTTP `GET /manifest` endpoint.
  - Add tests for manifest shape and tool coverage.
  - Update README and TASKS evidence.
- Out of scope:
  - SSE-specific tool streaming endpoint changes.
  - RBAC and OAuth completion.
- Files changed:
  - `src/manifest.ts`
  - `src/index.ts`
  - `tests/manifest.test.ts`
  - `README.md`
  - `TASKS.md`
- Dependencies: existing tool schema exports in student/instructor/shared modules.
- Constraints: keep stdio mode and existing HTTP endpoints unchanged.

## Acceptance Criteria

- [x] Discoverable manifest endpoint exists.
- [x] Manifest includes provider capabilities and endpoint contract.
- [x] Manifest includes dynamic tool list with schemas.
- [x] Tests verify manifest contract shape and tool coverage.

> Status note: this handoff records completion in the source `nitsuah/bb-mcp` delivery timeline; PR metadata in this document is normalized to reflect that this repository only stores the handoff artifact.

### Manifest Contract (schema_version = `1.0`)

```json
{
  "schema_version": "1.0",
  "provider": {
    "name": "bb-mcp",
    "version": "x.y.z",
    "capabilities": {
      "transport": ["stdio", "http"],
      "resources": true,
      "tools": true
    }
  },
  "manifest_endpoint": "/manifest",
  "tools": [
    {
      "name": "get_my_courses",
      "description": "Returns enrolled courses",
      "input_schema": { "type": "object" },
      "output_schema": { "type": "object" },
      "roles_allowed": ["student"]
    }
  ]
}
```

- Compatibility: additive fields only within `1.x`; breaking changes require `schema_version` major bump.
- Deprecation: mark tools with `deprecated: true` and `removal_after` before removal.
- Authentication semantics: unauthenticated requests return 401 with no tool metadata leakage.
- Error semantics: invalid requests return 400 with machine-readable `code` and `message`.
- Required tests (`tests/manifest.test.ts` in `nitsuah/bb-mcp`): assert `schema_version`, required top-level keys, dynamic tool schema presence, compatibility/deprecation fields, and auth/error responses.

## Delivery/DevOps Update

- Changes made:
  - Added `buildProviderManifest()` in `src/manifest.ts`.
  - Added `GET /manifest` route in HTTP server.
  - Added `tests/manifest.test.ts`.
  - Updated endpoint documentation in README and task status in TASKS.
- Validation performed:
  - Planned validation in `nitsuah/bb-mcp`: `npm test` (vitest), including manifest contract assertions listed above.
- Remaining risks:
  - Role metadata in manifest is static policy metadata and must stay in sync with authorization middleware if role matrix evolves.
- PR opened: not opened from this repository; tracked as a planning/handoff artifact.

## QA Update

- Scope tested: manifest builder and contract shape tests.
- Pass/fail summary: pending validation evidence in source repo
- Defects found: none
- Release recommendation: Hold until source-repo contract tests and release metadata are linked

## PMO Follow-Up

- TASKS updates needed: complete done for provider contract; continue with SSE transport task next.
- ROADMAP updates needed: none.
- Repo notes update needed: include `/manifest` in integration notes.
- Final disposition: handoff documented; source-repo implementation evidence still required.
