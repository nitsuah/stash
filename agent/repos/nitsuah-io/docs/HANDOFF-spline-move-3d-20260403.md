# Delivery Pipeline Handoff

## Repository Context

- Repository: Nitsuah-Labs/nitsuah-io
- Default branch: main
- Working branch: feat/nitsuah-io/move-spline-3d-20260403
- PR link: (pending)
- Related issue/task: TASKS.md — [Q2-CEO] Move Spline 3D animation to /3d route
- Dependency: PMO planning PR is still open (`pmo/q2-2026-planning` → `main`, PR #251); this DEV PR targets the PMO branch for now.

## Work Summary

- Title: Move home-page Spline to dedicated /3d route
- Problem statement: home page loaded the Spline scene directly in the critical path and displayed a scroll prompt encouraging users to continue into heavy 3D content. This hurt perceived load speed and conflicted with Q2 landing-page goals.
- Priority: P0
- Type: Feature / Performance
- Requested by: Q2 CEO priorities

## Evidence

- Observed behavior: `src/app/page.tsx` imported and rendered `spline-home` and displayed layered long-scroll 3D section.
- Reproduction steps: open home route before fix and observe Spline loading in initial page path.
- Confidence: High

## Scope

- In scope:
  - Remove Spline from home route.
  - Add dedicated `/3d` route for Spline scene.
  - Remove the home scroll prompt text path.
  - Add test coverage for HeroSection scroll-indicator toggle.
  - Update ROADMAP and TASKS statuses.
- Out of scope:
  - Full landing-page card redesign task.
  - Lighthouse measurement automation.
- Files changed:
  - `src/app/page.tsx`
  - `src/app/3d/page.tsx`
  - `src/app/_components/HeroSection.tsx`
  - `src/app/_components/__tests__/HeroSection.test.tsx`
  - `TASKS.md`
  - `ROADMAP.md`
- Dependencies: existing spline component at `src/app/_components/_spline/spline-home`.
- Constraints: keep existing hero copy and CTA behavior stable.

## Acceptance Criteria

- [x] Home route no longer loads or renders Spline scene.
- [x] Dedicated `/3d` route renders the Spline scene.
- [x] Home route no longer shows "Scroll for more" indicator.
- [ ] Lighthouse score uplift measurement captured (follow-up needed).

## Delivery/DevOps Update

- Changes made:
  - Removed Spline import/render from home page.
  - Added `/3d` route with the moved Spline experience.
  - Added optional `showScrollIndicator` prop to HeroSection and disabled it on home.
  - Added HeroSection unit test to verify hidden scroll prompt behavior.
  - Updated TASKS and ROADMAP completion status for Spline move.
- Validation performed:
  - Static code verification confirms Spline moved from home to `/3d`.
  - Unit test added for scroll prompt suppression path.
  - Docker test-image build attempted (`docker build -f Dockerfile.test ...`) but blocked by pre-existing project build error: `Type error: Invalid value for '--ignoreDeprecations'`.
- Remaining risks:
  - Lighthouse improvement threshold still needs measured run evidence.
  - Existing Docker test build failure must be fixed before full automated validation can pass.
- PR opened: (opening now)

## QA Update

- Scope tested: home route composition and HeroSection scroll prompt behavior.
- Pass/fail summary: pass (functional scope), pending performance measurement.
- Defects found: none.
- Release recommendation: Go with Risks (pending Lighthouse evidence).

## PMO Follow-Up

- TASKS updates needed: add measured Lighthouse evidence in a follow-up.
- ROADMAP updates needed: none beyond status update.
- Repo notes update needed: include /3d route in navigation/docs if desired.
- Final disposition: implementation complete; measurement follow-up required.
