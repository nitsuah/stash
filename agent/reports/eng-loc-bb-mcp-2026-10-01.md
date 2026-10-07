---
HEAD: c3a28cfb07db571b21768acc95cf9340430b72f2
kind: eng-loc
repo: bb-mcp
date: 2026-10-01
---

# ENG LOC Report — bb-mcp (2026-10-01)

> 🧭 [[repos/bb-mcp|bb-mcp]] · ← [[reports/eng-loc-bb-mcp-2026-07-29|2026-07-29]] <!-- nav -->

**Mode**: `--report` (dry run, no refactoring performed)
**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.mjs`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `*.lock`, `*-lock.json`, `*.min.*`, `dist/`, `build/`, `vendor/`, `node_modules/`, `__pycache__/`, `*.pyc`, `*.map`, `*.d.ts`, binary assets

Source scanned: 47 files, 12,200 LOC. Analyzed from a `--depth 1` clone (single commit) — git history/churn signals are **not available** this run.

---

## Top LOC Files

| File | LOC | Lang | Role |
|---|---|---|---|
| `src/index.ts` | 1072 | TS | Server entrypoint (HTTP+stdio transports, OAuth, health/metrics) |
| `src/tools/admin.ts` | 728 | TS | Admin MCP tool handlers |
| `tests/tools-grade-writeback.test.ts` | 603 | TS | Test suite |
| `src/tools/grade-writeback.ts` | 613 | TS | Grade write-back tool handlers |
| `src/tools/parent.ts` | 605 | TS | Parent-role tool handlers |
| `tests/tools-admin.test.ts` | 581 | TS | Test suite |
| `src/tools/instructor.ts` | 589 | TS | Instructor-role tool handlers |
| `src/tools/student.ts` | 515 | TS | Student-role tool handlers |
| `src/tools/webhook-tools.ts` | 514 | TS | Webhook tool handlers |
| `src/schemas.ts` | 427 | TS | Zod schemas (under threshold, noted for context) |

9 of 47 source files exceed `max_lines=500` (8 non-test + 1 test file borderline, see below). 3 files are ≤30 lines (`src/constants.ts`, `config/eslint.config.mjs`, `config/vitest.config.ts`) — all are thin config/constant files with a single clear concern, not merge candidates.

---

## Risk Rank & Rationale

### `src/index.ts` — **High**
- Mixed concerns confirmed by structure: ~400 lines of imports/tool wiring, then four top-level functions. `startHttpServer()` alone spans **lines 625–1007 (~382 lines)** — HTTP transport setup, SSE streaming, OAuth callback handling, and `/health`/`/metrics` endpoints are all inlined in one function, well over the ~80-line signal threshold.
- `startStdioServer()` (lines 1008–1072) duplicates transport bootstrapping logic parallel to the HTTP path.
- Test coverage: no `tests/index.test.ts` found — assumed untested (not confirmed from a single-commit clone).

### `src/tools/admin.ts` — **Medium-High**
- Single-concern file (admin tool handlers) but at 728 lines is the largest tool module; has a matching `tests/tools-admin.test.ts` (581 lines), so coverage looks present.
- Flag is based on sheer handler count in one file rather than mixed concerns — lower risk than `index.ts`.

### `src/tools/grade-writeback.ts`, `parent.ts`, `instructor.ts`, `student.ts`, `webhook-tools.ts` — **Medium**
- All follow the same pattern: one file per role/feature holding several independent MCP tool handlers (schema + handler pairs). Each has a same-named test file, so coverage is likely present (`grade-writeback` and `admin` tests confirmed; others assumed similar — not individually verified this run).
- Structural rationale: these aren't one tangled concern, but each file bundles multiple independent tools that could be split one-handler-per-file without behavior risk — low effort, low risk extraction if ever needed.

### Test files >500 lines (`tools-admin.test.ts`, `tools-grade-writeback.test.ts`) — **Low**
- Large test files are expected to be verbose (fixtures + multiple `describe` blocks per handler). Not flagged as refactor risk; noted for completeness only.

---

## Refactor Opportunities by Phase (reference only — `--report` mode, no execution)

1. **`src/index.ts`, phase 1**: Extract `startHttpServer`'s OAuth callback branch and `/health`/`/metrics` endpoint handlers into `src/http/routes.ts`, leaving `startHttpServer` as the transport bootstrap + route-mount call. Smallest safe cut — no behavior change, pure move.
2. **`src/index.ts`, phase 2**: Extract SSE/streaming helpers (`writeSseEvent`, `chunkText`) into `src/http/sse.ts` (already near-isolated, lines 594–624).
3. **Tool modules (`admin.ts`, `parent.ts`, etc.), optional**: If any individual module keeps growing, split by tool (one handler + schema per file under `src/tools/admin/`) with an index barrel re-exporting the same names — deferred, current size doesn't yet warrant it given existing test coverage.

## Validation Plan (if executed)
- `npm run typecheck && npm test` (vitest, per `config/vitest.config.ts`) must stay green after each extraction.
- Smoke-test both transports locally (`node dist/index.js` and `node dist/index.js --stdio`) before any commit, since `index.ts` covers both entrypoints.

---

## Summary

| Repo | Top concern | Priority | Notes |
|---|---|---|---|
| bb-mcp | `src/index.ts` mixes HTTP transport, OAuth, and health/metrics in one 1072-line entrypoint | Medium | Tool-handler modules are large but single-concern and test-covered; entrypoint is the real mixed-concern risk |

**Churn/history**: not assessable — analysis ran against a `--depth 1` clone (single commit visible).
**Canaries**: n/a — `stash` (the only tracked canary file's repo) was not in this run's target set.
