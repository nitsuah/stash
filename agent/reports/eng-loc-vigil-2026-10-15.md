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

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `lib/github.test.ts` | 1,048 | TypeScript | GitHub client test suite |
| 2 | `app/api/mcp/route.ts` | 893 | TypeScript | MCP server — JSON-RPC transport + 10 tool handlers |
| 3 | `lib/sync.ts` | 707 | TypeScript | Repo sync orchestrator (parsers, health score, DB) |
| 4 | `components/dashboard/RepoTableRow.tsx` | 699 | TSX | Dashboard table row component |
| 5 | `lib/template-enricher.ts` | 646 | TypeScript | Doc/template content generation |
| 6 | `hooks/useRepoActions.ts` | 645 | TypeScript | Repo action hooks (file preview, apply practice) |
| 7 | `components/Header.tsx` | 626 | TSX | App header/nav component |
| 8 | `lib/best-practices.ts` | 607 | TypeScript | Best-practice detection rules |
| 9 | `app/page.tsx` | 584 | TSX | Main dashboard page |
| 10 | `lib/repo-chat.ts` | 578 | TypeScript | Repo chat/assistant logic |
| 11 | `app/api/preview-templates/route.ts` | 535 | TypeScript | Template preview API route |
| 12 | `components/repo-details/RoadmapSection.tsx` | 507 | TSX | Roadmap detail panel |

## Risk Rank and Rationale

| File | Risk | Rationale |
|------|------|-----------|
| `lib/github.test.ts` | **Low** | Single clear concern (test suite for GitHub client). Large size reflects test breadth, not complexity — not a refactor target under the "single clear concern" exception. |
| `app/api/mcp/route.ts` | **Critical** | Mixed concerns: JSON-RPC transport, auth/rate-limiting, and 10 distinct MCP tool implementations (health, tasks, portfolio, search, security, relationships) all live in one route file. 16 function/handler boundaries in 893 lines. Classic "routing + business logic" smell per Phase 1 criteria. |
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

## Ordered Next-Cycle Targets (this repo)
1. `app/api/mcp/route.ts` (893 LOC) — Critical, extract tool handlers
2. `lib/sync.ts` (707 LOC) — High, extract fallback cache
3. `components/dashboard/RepoTableRow.tsx` (699 LOC) — High, extract derived-data hook, needs manual QC
4. `hooks/useRepoActions.ts` (645 LOC) — Medium, split by action family
5. `app/page.tsx` (584 LOC) — Medium, confirm concerns before planning a cut
