# ENG LOC Report — vigil (2026-10-15)
HEAD: 5c199d4fc304c5ee2468432987dcaf427035dad8

Mode: `--report` (dry run, no changes made)
Date: 2026-10-15
Source: shallow clone (`--depth 1`) of `nitsuah/vigil` @ `5c199d4fc304c5ee2468432987dcaf427035dad8`
Method: `git ls-files` (Phase 0 spec exclusions applied: lock files, dist/build/node_modules, docs, binary assets) + `wc -l` per file — actual line counts, not estimated.
Note: shallow clone — churn/author history (many-authors, frequent-edits signal) is **not available**; that structural signal is marked "assumed: not confirmed" throughout. Previously tracked under the name `overseer` in older reports (`eng-loc-overseer-*.md`); this is the first run under the current `vigil` naming.

## Inventory Summary
- Tracked source files (post-exclusion, code extensions only): 286
- Total LOC counted: 44,610

## Top 10 LOC Files

Code files only — see note below on the repo's largest file, a test suite, which doesn't qualify for a ranked slot (per `LOC.md` Phase 1).

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `app/api/mcp/route.ts` | 893 | TypeScript | MCP server — JSON-RPC transport + 10 tool handlers |
| 2 | `lib/sync.ts` | 707 | TypeScript | Repo sync orchestrator (parsers, health score, DB) |
| 3 | `components/dashboard/RepoTableRow.tsx` | 699 | TSX | Dashboard table row component |
| 4 | `lib/template-enricher.ts` | 646 | TypeScript | Doc/template content generation |
| 5 | `hooks/useRepoActions.ts` | 645 | TypeScript | Repo action hooks (file preview, apply practice) |
| 6 | `components/Header.tsx` | 626 | TSX | App header/nav component |
| 7 | `lib/best-practices.ts` | 607 | TypeScript | Best-practice detection rules |
| 8 | `app/page.tsx` | 584 | TSX | Main dashboard page |
| 9 | `lib/repo-chat.ts` | 578 | TypeScript | Repo chat/assistant logic |
| 10 | `app/api/preview-templates/route.ts` | 535 | TypeScript | Template preview API route |

Test file: `lib/github.test.ts` (1,048 lines) is the single largest file in the repo, ahead of every entry above — but it's a test suite, under the ~1,500-line bar for a standalone test-file callout, so it gets this note instead of a ranked slot.

## Risk Rank and Rationale

| File | Risk | Rationale |
|------|------|-----------|
| `app/api/mcp/route.ts` | **High** | Mixed concerns: JSON-RPC transport, auth/rate-limiting, and 10 distinct MCP tool implementations (health, tasks, portfolio, search, security, relationships) all live in one route file. 16 function/handler boundaries in 893 lines. Classic "routing + business logic" smell per Phase 1 criteria. |
| `lib/sync.ts` | **High** | Orchestrates 9+ imported parsers/checkers (roadmap, tasks, metrics, features, doc-health, best-practices, community-standards, health-score, test-cases, code-density) plus an inline fallback cache and DB schema call — mixed concerns (parsing, caching, scoring, persistence) in one module. |
| `components/dashboard/RepoTableRow.tsx` | **High** | UI rendering mixed with business logic (`detectRepoType`, `calculateDocHealth`, health-grade formatting) in a single component; 18 imported icons suggest a large render tree. Flag for manual QC if split — rendering/interaction logic involved. |
| `lib/template-enricher.ts` | Medium | Content-generation logic with AI-prompt string building inline; assumed: not confirmed whether logic is separable from prompt templates without inspection beyond header. |
| `hooks/useRepoActions.ts` | Medium | 15 action closures in one hook file — each is a distinct user action (apply doc, apply practice, etc.); a plausible split point is one hook per action family. |
| `components/Header.tsx` | Medium | UI component importing rate-limit display, profile menu, and auth state — mixed nav/auth/rate-limit concerns, but may be acceptable as a single "app shell" component. Assumed: not confirmed without full read. |
| `lib/best-practices.ts` | **Low** | Appears to be primarily type definitions and a rules/state model (`HealthState`, `BestPractice`) — closer to a flat config/rules module than a mixed-concern file. |
| `app/page.tsx` | Medium | Next.js top-level page; pages commonly mix data-fetching, state, and rendering — assumed risk, not confirmed without full read. |
| `lib/repo-chat.ts` | Medium | Assumed: not confirmed — chat logic, likely single concern (assistant invocation) but size warrants a look. |

Test coverage: repo has an active test suite (`vitest.config.ts`, `*.test.ts`/`*.test.tsx` files present, including for `github.ts` itself). Coverage for the specific hotspots above (`sync.ts`, `route.ts`, `RepoTableRow.tsx`) is **assumed: not confirmed** — no matching `*.test.ts` found alongside them in this scan.

Churn: **assumed: not confirmed** (shallow clone, no history available).

Canaries: N/A (vigil/stash canary list only applies to the `stash` repo; not scanned this run).

## Refactor Opportunities by Phase (handoff notes, not yet actioned)

- **`app/api/mcp/route.ts`**: smallest safe extraction is to pull each of the 10 tool handlers (`get_repo_health`, `list_tasks`, etc.) into `lib/mcp-tools/*.ts`, leaving `route.ts` as the JSON-RPC dispatch + auth/rate-limit barrel. Lowest risk first cut: the handlers with no shared state (e.g. `search_repos`, `get_security_summary`).
- **`lib/sync.ts`**: extract the org-level GitHub fallback cache (`ORG_GITHUB_FALLBACK_CACHE` + `getOrgGithubFallbackFiles`) into its own module first — it's self-contained and has no dependency on the rest of the sync flow.
- **`components/dashboard/RepoTableRow.tsx`**: extract `detectRepoType`/`calculateDocHealth` usage into a `useRepoRowDerived` hook, separating derived-data computation from JSX. Flag as needing manual QC (rendering/interaction logic) before any merge.

## Validation Plan (for a future `--refactor` pass)
- Run `vitest` (config present at `config/vitest.config.ts`) after each extraction.
- Smoke-test the Next.js dev server for any route/component touched.
- For `RepoTableRow.tsx`, manual QC of the dashboard table golden path (expand row, run practice, view roadmap) since it's a rendering/interaction surface.

## Repo Summary

| Repo | Top Concern | Priority | Notes |
|------|-------------|----------|-------|
| vigil | `app/api/mcp/route.ts` — 10 tool handlers in one route file | High | Clear extraction path; no history available (shallow clone) |

## Ordered Next-Cycle Targets (cross-repo, tier-weighted)

Shared across this run's three reports (vigil, vhs, kryptos) — see each report's own Repo Summary for per-repo context. Tier from `agent/projects/scope.md`: vigil = T1, vhs = T2, kryptos = untiered (not yet registered in vigil; ranks alongside T2/T3 per `LOC.md`).

1. `app/api/mcp/route.ts` (vigil, T1, 893 LOC) — High, extract tool handlers
2. `lib/sync.ts` (vigil, T1, 707 LOC) — High, extract fallback cache
3. `components/dashboard/RepoTableRow.tsx` (vigil, T1, 699 LOC) — High, extract derived-data hook, needs manual QC
4. `src/kryptos/k4/frontier_checks.py` (kryptos, untiered, 1,131 LOC) — High, extract `hill_exhaustive` first
5. `public/js/ui.js` (vhs, T2, 896 LOC) — High, extract CSV/bulk-action helpers
6. `src/server.js` (vhs, T2, 761 LOC) — High, extract route groups into `./modules/routes/*`
7. `src/kryptos/k4/crib_constraints.py` (kryptos, untiered, 877 LOC) — Medium-High, needs direct read before a phase plan

Tier reordered what raw LOC would have suggested: `frontier_checks.py` (1,131 LOC, the largest file in this run) would rank #1 by size alone, but vigil's three T1 findings are weighted ahead of it despite being smaller, since vigil is a T1 (Critical/production) repo and kryptos isn't yet tiered.
