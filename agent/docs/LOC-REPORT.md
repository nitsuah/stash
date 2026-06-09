# LOC Refactor Report — 2026 Q3

Generated: 2026-06-02
Scope: All repos in `C:\Users\ajhar\code\`
Exclusions: `node_modules`, `.next`, `dist`, `build`, `venv`, `.venv`, `vendor`, `coverage`, generated typechain files (`*__factory.ts`), generated GraphQL types (`generated.ts`)

---

## Summary Table

| Repo | Worst File | LOC | Risk |
|---|---|---|---|
| agent-board | server.js | 2726 | CRITICAL |
| agent-board | App.jsx | 1337 | HIGH |
| auto-apply-plugin | service-worker.js | 1263 | HIGH |
| auto-apply-plugin | content.js | 1202 | HIGH |
| auto-apply-plugin | tracker-handlers.js | 957 | HIGH |
| auto-apply-plugin | tracker-ui.js | 891 | HIGH |
| kryptos | hypotheses.py | 897 | HIGH |
| kryptos | transposition_analysis.py | 859 | HIGH |
| kryptos | cli/main.py | 663 | MEDIUM |
| kryptos | scoring.py | 656 | MEDIUM |
| kryptos | vigenere_key_recovery.py | 612 | MEDIUM |
| kryptos | autonomous_coordinator.py | 608 | MEDIUM |
| darkmoon | PlayerCharacter.tsx | 833 | HIGH |
| darkmoon | Solo.tsx | 763 | HIGH |
| games | Game.jsx | 828 | HIGH |
| games | SoundManager.js | 808 | HIGH |
| overseer | enrich-template/route.ts | 754 | HIGH |
| overseer | GuidedTour.tsx | 750 | HIGH |
| overseer | github.ts | 741 | HIGH |
| overseer | ai-prompt-chain.ts | 670 | HIGH |
| overseer | useRepoActions.ts | 637 | MEDIUM |
| bb-mcp | index.ts | 697 | HIGH |
| bb-mcp | instructor.ts | 589 | MEDIUM |
| gcp | copy_folder.py | 540 | MEDIUM |
| auto-apply-plugin | gemini.js | 550 | MEDIUM |
| auto-apply-plugin | form-filler.js | 537 | MEDIUM |
| auto-apply-plugin | tracker.js | 537 | MEDIUM |
| stash | validate_project.py | 1051 | LOW* |
| nitsuah-io | NFTDemo.tsx | 509 | LOW |
| nitsuah-io | crypto/page.tsx | 508 | LOW |

*stash files are reference/example code, not production — flagged for awareness only.

---

## Per-Repo Breakdown

---

### agent-board

#### Top Files

| File | LOC | Risk |
|---|---|---|
| dashboard/server.js | 2726 | CRITICAL |
| dashboard/src/App.jsx | 1337 | HIGH |
| dashboard/tracing.js | 192 | OK |
| dashboard/persistence.js | 179 | OK |

#### Analysis

**`server.js` (2726)** — Screams refactor. Single Express file containing: session CRUD, message routing, LLM proxy logic, Docker status polling, safety classification, metrics aggregation, WebSocket event bus, OpenTelemetry integration, system service discovery, and experience routing. Every concern is co-located. Any change touches this file.

**`App.jsx` (1337)** — Monolithic React component. Likely contains: all UI state, sidebar logic, settings panels, chat view, metrics view, session switching, model switching, and system panel — all in one component tree.

#### Refactor Phases

**Phase 1 — server.js decomposition (highest ROI)**
- Extract `routes/sessions.js` — session CRUD endpoints
- Extract `routes/messages.js` — message send + LLM proxy
- Extract `routes/metrics.js` — all `/api/metrics/*` handlers
- Extract `routes/docker.js` — Docker status + service control
- Extract `middleware/safety.js` — input classification, PII redaction, output filter
- Extract `services/llm-proxy.js` — endpoint resolution + forwarding logic
- Keep `server.js` as thin mount point (<100 lines)
- Validation: existing integration tests in `tests/` cover sessions + messages — run after each extraction

**Phase 2 — App.jsx decomposition**
- Extract `<ChatView>`, `<MetricsView>`, `<SystemPanel>`, `<SessionSidebar>` as standalone components
- Extract custom hooks: `useSession`, `useEndpoint`, `useMetrics`
- Validation: E2E tests in `tests/e2e-chat.js`

---

### auto-apply-plugin

#### Top Files

| File | LOC | Risk |
|---|---|---|
| background/service-worker.js | 1263 | HIGH |
| content/content.js | 1202 | HIGH |
| popup/tracker/tracker-handlers.js | 957 | HIGH |
| popup/tracker/tracker-ui.js | 891 | HIGH |
| lib/gemini.js | 550 | MEDIUM |
| lib/tracker.js | 537 | MEDIUM |
| lib/form-filler.js | 537 | MEDIUM |
| lib/job-search.js | 497 | OK |

#### Analysis

**`service-worker.js` (1263)** — Chrome extension background script handling: message routing from content scripts, job search orchestration, Gemini API calls, storage read/write, alarm scheduling, badge updates, tab lifecycle. Classic "god worker" pattern.

**`content.js` (1202)** — DOM injection, form detection, field mapping, mutation observer logic, overlay rendering, and message passing back to the service worker. Multiple concerns in one file.

**`tracker-handlers.js` (957) + `tracker-ui.js` (891)** — Together ~1848 lines for the tracker popup feature alone. Handlers and UI are split but both oversized; handlers likely have embedded business logic that belongs in `lib/tracker.js`.

**`gemini.js` (550)** — At the boundary. If it contains prompt construction, API call logic, response parsing, and retry logic all together, it should split. Acceptable if well-structured.

**`lib/tracker.js` + `lib/form-filler.js` (537 each)** — Borderline. Watch for growth.

#### Refactor Phases

**Phase 1 — service-worker.js**
- Extract `sw/message-router.js` — message dispatch table
- Extract `sw/alarm-handler.js` — alarm scheduling and badge logic
- Extract `sw/storage.js` — all chrome.storage read/write wrappers
- Keep orchestration in `service-worker.js` (<200 lines)
- Validation: unit tests in `tests/` cover job-search and logic paths

**Phase 2 — content.js**
- Extract `content/form-detector.js` — form/field detection
- Extract `content/overlay.js` — overlay injection and rendering
- Extract `content/message-bridge.js` — postMessage / chrome.runtime bridge
- Validation: manual smoke test on target job sites (no automated content tests currently)

**Phase 3 — tracker popup**
- Move business logic from `tracker-handlers.js` → `lib/tracker.js`
- Split `tracker-ui.js` into `tracker-ui-list.js` (list view) + `tracker-ui-detail.js` (detail/edit view)

---

### kryptos

#### Top Files

| File | LOC | Risk |
|---|---|---|
| k4/hypotheses.py | 897 | HIGH |
| k4/transposition_analysis.py | 859 | HIGH |
| cli/main.py | 663 | MEDIUM |
| k4/scoring.py | 656 | MEDIUM |
| k4/vigenere_key_recovery.py | 612 | MEDIUM |
| autonomous_coordinator.py | 608 | MEDIUM |
| pipeline/attack_generator.py | 579 | MEDIUM |
| agents/ops_director.py | 551 | MEDIUM |

#### Analysis

**`hypotheses.py` (897)** — Likely defines a large number of hypothesis classes or a data-heavy registry. If it is a flat list of hypothesis definitions, the refactor is low risk (split into `hypotheses/transposition.py`, `hypotheses/vigenere.py`, etc.).

**`transposition_analysis.py` (859)** — Analysis algorithms. Risk depends on coupling — if functions call each other heavily, extraction is careful work.

**`cli/main.py` (663)** — CLI entry point with too much logic. Should be thin argparse wiring; business logic belongs in modules.

**`autonomous_coordinator.py` (608)** — Orchestration file. If it mixes scheduling, state management, and execution dispatch, it can be decomposed.

Note: kryptos is a research/cryptanalysis codebase. Some complexity is inherent to the domain. Prioritize CLI and coordinator files over pure analysis modules.

#### Refactor Phases

**Phase 1 — cli/main.py**
- Split into subcommand modules: `cli/analyze.py`, `cli/attack.py`, `cli/report.py`
- Keep `cli/main.py` as argparse entry point (<100 lines)
- Validation: functional tests in `tests/functional/` cover CLI paths

**Phase 2 — autonomous_coordinator.py**
- Extract `coordinator/scheduler.py` — task scheduling
- Extract `coordinator/dispatcher.py` — agent dispatch
- Validation: run existing test suite; add integration test for coordinator flow

**Phase 3 — hypotheses.py + scoring.py** (lower urgency if tests exist)
- Split `hypotheses.py` by cipher family
- Extract scoring rubrics from `scoring.py` into data-driven config
- Validation: functional test coverage in `tests/functional/test_k4_hypotheses.py` (591 lines — good coverage signal)

---

### darkmoon

#### Top Files

| File | LOC | Risk |
|---|---|---|
| src/components/characters/PlayerCharacter.tsx | 833 | HIGH |
| src/pages/Solo.tsx | 763 | HIGH |
| src/components/SoundManager.ts | 472 | MEDIUM |
| src/components/SpacemanModel.tsx | 383 | LOW |
| src/components/GameUI.tsx | 305 | OK |
| server.js | 416 | OK |

#### Analysis

**`PlayerCharacter.tsx` (833)** — Game character component. Likely mixes: input handling, physics state, animation state machine, collision response, and render logic. High coupling risk.

**`Solo.tsx` (763)** — Page-level game scene. Likely orchestrates all game entities, manages game loop state, and mounts sub-components. Should be a thin scene coordinator.

**`SoundManager.ts` (472)** — Borderline. Sound managers are often legitimately large. Acceptable unless it also handles music logic (which may belong in `DynamicMusicSystem` if that's in games/).

#### Refactor Phases

**Phase 1 — PlayerCharacter.tsx**
- Extract `usePlayerInput` hook — keyboard/gamepad input
- Extract `usePlayerPhysics` hook — velocity, collision state
- Extract `usePlayerAnimation` hook — frame/animation state machine
- Keep `PlayerCharacter.tsx` as composition root
- Validation: `PlayerCharacter.frame.test.tsx` (331 lines) + `movement.integration.test.ts` (327 lines) provide good coverage

**Phase 2 — Solo.tsx**
- Extract scene setup into `useSoloScene` hook
- Extract game loop management into `useGameLoop` hook
- Validation: manual gameplay test + `PauseMenu.test.tsx`

---

### games

#### Top Files

| File | LOC | Risk |
|---|---|---|
| lib/asteroid/_comp/Game/Game.jsx | 828 | HIGH |
| utils/audio/SoundManager.js | 808 | HIGH |
| app/_components/home/ArcadeLayout.tsx | 506 | MEDIUM |
| utils/audio/DynamicMusicSystem.js | 366 | OK |
| lib/asteroid/_comp/Weapons/ShootingSystem.jsx | 334 | OK |
| lib/asteroid/_comp/Player/Player.jsx | 308 | OK |

#### Analysis

**`Game.jsx` (828)** — Game loop orchestrator for Asteroid. Likely manages entity state, collision detection, score, wave progression, and render coordination in one component. Classic game god-object pattern.

**`SoundManager.js` (808)** — Second-largest file. A sound manager at 808 lines suggests it handles: asset loading, channel management, spatial audio, music queuing, and dynamic mixing — all concerns that could be split. Compare with `DynamicMusicSystem.js` (366) which may have overlapping responsibility.

**`ArcadeLayout.tsx` (506)** — Borderline. Home/nav layout at 506 lines suggests it renders multiple game cards, handles routing, and possibly manages featured/promo state inline.

#### Refactor Phases

**Phase 1 — Game.jsx**
- Extract `useAsteroidGameLoop` hook — tick/update logic
- Extract `useAsteroidEntities` hook — enemy/asteroid state management
- Extract `useCollisionDetection` hook — collision logic
- Validation: `handleTargetHit.test.js` (664), `handleGameOver.test.js` (310), `handleHealthDepletion.test.js` (327) — solid test coverage

**Phase 2 — SoundManager.js**
- Audit overlap with `DynamicMusicSystem.js`
- Extract `AudioLoader.js` — asset loading + caching
- Extract `ChannelMixer.js` — channel management
- Keep `SoundManager.js` as public API facade

**Phase 3 — ArcadeLayout.tsx**
- Extract `<GameCard>` and `<FeaturedGame>` as standalone components

---

### overseer

#### Top Files

| File | LOC | Risk |
|---|---|---|
| app/api/enrich-template/route.ts | 754 | HIGH |
| components/GuidedTour.tsx | 750 | HIGH |
| lib/github.ts | 741 | HIGH |
| lib/ai-prompt-chain.ts | 670 | HIGH |
| hooks/useRepoActions.ts | 637 | MEDIUM |
| lib/sync.ts | 548 | MEDIUM |
| components/dashboard/RepoTableRow.tsx | 531 | MEDIUM |
| components/Header.tsx | 503 | MEDIUM |

#### Analysis

**`enrich-template/route.ts` (754)** — API route doing too much. Likely contains prompt construction, DB read/write, GitHub API calls, and response shaping all in one handler.

**`GuidedTour.tsx` (750)** — A UI tour component at 750 lines. Likely has step definitions data-inlined as JSX rather than in a config file.

**`github.ts` (741)** — GitHub API client. At 741 lines it likely mixes: client instantiation, auth, rate-limit handling, and all API method implementations. Should split into domain-grouped modules (`github/repos.ts`, `github/files.ts`, `github/prs.ts`).

**`ai-prompt-chain.ts` (670)** — Prompt orchestration. Mixes prompt templates, chain logic, and result parsing.

**`useRepoActions.ts` (637)** — React hook at 637 lines is too large. Multiple action domains bundled.

**`RepoTableRow.tsx` (531)** — A single table row at 531 lines. Likely has inline modals, tooltips, and action logic that should be extracted.

**`Header.tsx` (503)** — Header at 503 lines. Likely contains nav state, search, user menu, and notification logic all inline.

#### Refactor Phases

**Phase 1 — github.ts** (most broadly coupled)
- Split into `github/client.ts` (auth + rate-limit), `github/repos.ts`, `github/files.ts`, `github/pulls.ts`
- Validation: `lib/github.test.ts` (576 lines) — good existing test coverage; tests must pass after move

**Phase 2 — enrich-template/route.ts**
- Extract prompt construction to `lib/ai-prompt-chain.ts` (already exists — move more there)
- Extract DB operations to a repository function in `lib/db/templates.ts`
- Validation: add route-level tests

**Phase 3 — GuidedTour.tsx**
- Extract step definitions to `lib/tour-steps.ts` (data config)
- Keep `GuidedTour.tsx` as renderer (<150 lines)

**Phase 4 — useRepoActions.ts**
- Split into `useRepoCommunityActions`, `useRepoSyncActions`, `useRepoBranchActions`

---

### bb-mcp

#### Top Files

| File | LOC | Risk |
|---|---|---|
| src/index.ts | 697 | HIGH |
| src/tools/instructor.ts | 589 | MEDIUM |
| src/tools/student.ts | 515 | MEDIUM |
| src/schemas.ts | 427 | MEDIUM |
| src/cli.ts | 265 | OK |

#### Analysis

**`index.ts` (697)** — MCP server entry point. At 697 lines it is doing server initialization, tool registration, request dispatch, and likely some handler logic that belongs in `tools/`.

**`instructor.ts` + `student.ts` (589 + 515)** — Tool implementation files. Combined ~1100 lines of tool handlers. Acceptable if each file covers one domain, but worth verifying functions are not exceeding 100 lines individually.

**`schemas.ts` (427)** — Large schema file. Acceptable for a schema registry but could split by domain if it grows.

#### Refactor Phases

**Phase 1 — index.ts**
- Extract tool registration into `src/registry.ts`
- Extract server config/init into `src/server.ts`
- Keep `index.ts` as entry point (<50 lines)
- Validation: `tests/tools-instructor.test.ts` + `tests/tools-student.test.ts`

**Phase 2 — schemas.ts** (if it grows)
- Split by domain: `schemas/instructor.ts`, `schemas/student.ts`, `schemas/common.ts`

---

### gcp

#### Top Files

| File | LOC | Risk |
|---|---|---|
| gcp/copy_folder.py | 540 | MEDIUM |
| tests/test_main.py | 375 | OK |
| tests/test_copy_folder_extended.py | 369 | OK |

#### Analysis

**`copy_folder.py` (540)** — Single utility module at 540 lines. Likely handles: auth, GCS client init, recursive folder traversal, copy logic, error handling, and logging. Decomposition would improve testability.

#### Refactor Phases

**Phase 1 — copy_folder.py**
- Extract `gcs_client.py` — auth + client factory
- Extract `folder_walker.py` — recursive traversal logic
- Keep `copy_folder.py` as orchestration
- Validation: `test_copy_folder.py` + `test_copy_folder_extended.py` cover paths

---

### nitsuah-io

#### Top Files (excluding generated.ts)

| File | LOC | Risk |
|---|---|---|
| app/projects/clients/_comp/NFTDemo.tsx | 509 | LOW |
| app/crypto/page.tsx | 508 | LOW |
| app/projects/clients/_comp/RealEstateDemo.tsx | 487 | LOW |
| app/projects/clients/_comp/PortfolioDemo.tsx | 437 | LOW |
| app/projects/page.tsx | 429 | LOW |
| app/_components/_site/_comp/homebar/Brand.tsx | 418 | LOW |

#### Analysis

All files are in the 400-510 range — borderline but none are urgent. The demo components (`NFTDemo`, `RealEstateDemo`, `PortfolioDemo`) are naturally larger as they simulate full product UIs inline. `crypto/page.tsx` at 508 lines is worth watching.

No immediate refactor action needed. Monitor for growth past 600.

---

### stash

#### Note

Files in `stash/` are reference snippets and usage examples, not production code. High LOC in example files is expected. Flagged for awareness only — no refactor action needed.

| File | LOC | Note |
|---|---|---|
| atlassian/jira/validate_project.py | 1051 | Reference/example |
| cloud/aws/examples.py | 562 | Reference/example |
| SAAS/github/examples.py | 491 | Reference/example |
| SAAS/okta/examples.py | 481 | Reference/example |

---

### Repos with No Action Needed

| Repo | Largest File | LOC | Notes |
|---|---|---|---|
| avatar | tests/test_utils.py | 311 | Well within range |
| osrs | tests/test_utils.py | 152 | Small codebase |
| skyview | config.js | 330 | All files acceptable |
| deployer | types/\*__factory.ts | 810 | Typechain-generated; exclude |
| vhs | — | — | No source files yet |

---

## Prioritized Refactor Queue

### Tier 1 — Do First (>1000 LOC or CRITICAL)

| # | File | Repo | LOC | Key Risk |
|---|---|---|---|---|
| 1 | dashboard/server.js | agent-board | 2726 | Monolith, all concerns co-located |
| 2 | dashboard/src/App.jsx | agent-board | 1337 | Monolith React component |
| 3 | background/service-worker.js | auto-apply-plugin | 1263 | God worker, hard to test |
| 4 | content/content.js | auto-apply-plugin | 1202 | Mixed DOM concerns |

### Tier 2 — High Priority (700-1000 LOC)

| # | File | Repo | LOC |
|---|---|---|---|
| 5 | popup/tracker/tracker-handlers.js | auto-apply-plugin | 957 |
| 6 | k4/hypotheses.py | kryptos | 897 |
| 7 | popup/tracker/tracker-ui.js | auto-apply-plugin | 891 |
| 8 | k4/transposition_analysis.py | kryptos | 859 |
| 9 | characters/PlayerCharacter.tsx | darkmoon | 833 |
| 10 | lib/asteroid/Game/Game.jsx | games | 828 |
| 11 | utils/audio/SoundManager.js | games | 808 |
| 12 | src/pages/Solo.tsx | darkmoon | 763 |
| 13 | app/api/enrich-template/route.ts | overseer | 754 |
| 14 | components/GuidedTour.tsx | overseer | 750 |
| 15 | lib/github.ts | overseer | 741 |
| 16 | src/index.ts | bb-mcp | 697 |

### Tier 3 — Monitor (500-700 LOC)

| # | File | Repo | LOC |
|---|---|---|---|
| 17 | lib/ai-prompt-chain.ts | overseer | 670 |
| 18 | k4/cli/main.py | kryptos | 663 |
| 19 | hooks/useRepoActions.ts | overseer | 637 |
| 20 | k4/scoring.py | kryptos | 656 |
| 21 | k4/vigenere_key_recovery.py | kryptos | 612 |
| 22 | autonomous_coordinator.py | kryptos | 608 |
| 23 | src/tools/instructor.ts | bb-mcp | 589 |
| 24 | pipeline/attack_generator.py | kryptos | 579 |
| 25 | lib/sync.ts | overseer | 548 |
| 26 | lib/gemini.js | auto-apply-plugin | 550 |
| 27 | gcp/copy_folder.py | gcp | 540 |
| 28 | lib/tracker.js | auto-apply-plugin | 537 |
| 29 | lib/form-filler.js | auto-apply-plugin | 537 |
| 30 | components/dashboard/RepoTableRow.tsx | overseer | 531 |
| 31 | src/tools/student.ts | bb-mcp | 515 |
| 32 | components/Header.tsx | overseer | 503 |

---

## Suggested TASKS Updates

For each Tier 1 file, add a task:

```
[ ] [refactor] agent-board: decompose server.js into route modules and service layer
[ ] [refactor] agent-board: decompose App.jsx into feature components and hooks
[ ] [refactor] auto-apply-plugin: split service-worker.js into router + handlers + storage
[ ] [refactor] auto-apply-plugin: split content.js into form-detector, overlay, message-bridge
[ ] [refactor] overseer: split github.ts into domain-grouped client modules
[ ] [refactor] darkmoon: extract hooks from PlayerCharacter.tsx
[ ] [refactor] games: extract hooks from Game.jsx
[ ] [refactor] bb-mcp: extract registry and server init from index.ts
```

---

## Guardrails for Execution

- Run existing tests before and after each extraction. If coverage drops, pause.
- One extraction per PR. Do not combine multiple file splits in one PR.
- Preserve all exports and public interfaces when extracting — internal refactor only.
- Avoid rewrites. Move code; do not rewrite it during the same PR.
- Flag any file with 0 test coverage before refactoring — add tests first.
