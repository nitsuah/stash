# Delivery Pipeline Handoff

## Repository Context

- Repository: nitsuah/darkmoon
- Default branch: main
- Working branch: feat/darkmoon/fix-player-bot-tag-20260403
- PR link: (pending)
- Related issue/task: TASKS.md — [Q2-CEO] Fix player tag system

## Work Summary

- Title: Fix solo-mode player<->bot tagging symmetry
- Problem statement: in solo mode, Bot1 used a static target position and a bot-only tag callback path, so bot->player tagging was inconsistent or absent even while player->bot logic existed.
- Priority: P0
- Type: Bug
- Requested by: Q2 CEO priorities

## Evidence

- Observed behavior: bot targeting in non-debug mode was `targetPosition={[0, 0.5, 0]}` and `onTagTarget` attempted `bot-1 -> bot-2` only.
- Reproduction steps: run solo tag mode and observe bot not reliably tagging active player unless near world origin.
- Confidence: High

## Scope

- In scope:
  - Wire live player position into bot AI target selection in solo mode.
  - Make bot tag callback route to current player in non-debug mode.
  - Keep debug bot-vs-bot path intact.
  - Add regression test for bot->player tag transfer.
  - Update TASKS and ROADMAP status.
- Out of scope:
  - 21st.dev UI integration work.
  - mobile-device physical validation task.
- Files changed:
  - `src/pages/Solo/components/SoloScene.types.ts`
  - `src/pages/Solo.tsx`
  - `src/pages/Solo/components/SoloScene.tsx`
  - `src/pages/Solo/components/Bots.tsx`
  - `src/__tests__/bots.tagging.test.tsx`
  - `TASKS.md`
  - `ROADMAP.md`
- Dependencies: none
- Constraints: preserve existing bot debug mode behavior.

## Acceptance Criteria

- [x] Players can tag bots via existing player tagging path.
- [x] Bots can tag players in solo mode through same GameManager transfer mechanics.
- [x] Regression test covers bot->player transfer.

## Delivery/DevOps Update

- Changes made:
  - Added `playerPosition` wiring from `Solo` -> `SoloScene` -> `Bots`.
  - In non-debug mode, Bot1 now targets live player position and uses `targetIsIt={playerIsIt}`.
  - Bot1 tag callback now tags `currentPlayerId` in solo mode and `bot-2` in debug mode.
  - Added `src/__tests__/bots.tagging.test.tsx` to verify bot->player tag transfer.
- Validation performed:
  - Docker-based focused test run:
    - `docker run --rm -v "${PWD}:/app" -w /app node:22-slim sh -lc "npm ci --no-audit --no-fund; npm run test:run -- src/__tests__/bots.tagging.test.tsx"`
  - Result: pass (1 test, 1 passed).
- Remaining risks:
  - Full suite not rerun in this pass; only targeted regression executed.
- PR opened: (opening now)

## QA Update

- Scope tested: bot->player tag transfer in solo mode.
- Pass/fail summary: pass.
- Defects found: none.
- Release recommendation: Go.

## PMO Follow-Up

- TASKS updates needed: done.
- ROADMAP updates needed: done.
- Repo notes update needed: optional note in Q2 progress rollup.
- Final disposition: ready for merge.

## Related
- [[repos/darkmoon|darkmoon runbook]] — repo context
- [[prompts/HANDOFF|HANDOFF template]] — pipeline handoff format
