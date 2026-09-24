# Tasks

Last Updated: 2026-09-23

## In Progress

_None._

## Todo

_The Q2 2026 platform-reliability items (performance/asset audit, accessibility
pass, UX verification pass) are complete — see `docs/ROADMAP.md` 2026 Q2.
Mobile responsiveness work shipped, but `docs/METRICS.md`'s browser
compatibility table still lists Mobile Safari/Mobile Chrome as
partial/untested (⚠️) rather than confirmed — re-verify and update that table
before treating mobile as fully validated. The client-side exception (`ReferenceError: Cannot access 'ev' before
initialization`) that once blocked Docker loads is also resolved — Docker-first
validation now succeeds locally and in CI (see Audit Notes below); the old
handoff describing it as still in-progress was archived to
`docs/archive/INSTRUCTIONS.md`._

- [ ] Re-scope expansion work after platform issues are fixed.
  - Priority: P2
  - Milestone: 2026 Q3
  - Problem: feature growth should not outrun packaging, deployment, and runtime stability work.
  - Acceptance Criteria: larger feature initiatives stay sequenced behind the release-path fixes.

- [ ] Fix game selection UI to allow programmatic and keyboard navigation for accessibility and automated testing.

- [ ] **Add unit/E2E tests for Memory Match and Dodge Blocks** — both iframe-hosted games are live and playable but lack unit-level or gameplay-level E2E automated test coverage; the existing Jest suite does not cover the standalone HTML bundles.
  - Priority: P2
  - Milestone: 2026 Q3

- [ ] **Add high-score persistence to Memory Match** — the current implementation shows a win alert but does not persist a best-time or move-count score to localStorage.
  - Priority: P3
  - Milestone: 2026 Q3

- [ ] **Mobile touch controls for Dodge Blocks** — the game uses only keyboard arrow keys; touch swipe or on-screen buttons are needed for mobile play.
  - Priority: P3
  - Milestone: 2026 Q3

## Audit Notes

- Docker-first validation now succeeds locally, and CI has a dedicated Docker smoke workflow.
- Deployment model is now consistently documented as Next.js runtime on Netlify.
- The Asteroid route audio startup no longer emits repeated `Sound not found: bgm` errors after readiness gating and memoized sound controls.
- 2026-08-22 audit: Arcade now has 9 live games (up from 7 documented). Memory Match and Dodge Blocks are iframe-hosted standalone vanilla JS games. Documentation corrected across README.md, FEATURES.md, ROADMAP.md, docs/API.md. Unit test count updated to 481 (35 suites). Version numbers updated to match package-lock.json.
