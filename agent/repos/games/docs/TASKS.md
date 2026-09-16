# Tasks

Last Updated: 2026-08-28

## In Progress

- [x] **[RESOLVED] Global client-side exception debugging** — All games fail to load in Docker due to a client-side ReferenceError. Last step: capture browser console logs from Dockerized app, diagnose, and fix. See docs/INSTRUCTIONS.md for handoff.

## Todo

- [x] **[Q2] Performance audit and asset optimization** — identify and fix the largest asset/load-time bottlenecks across game routes.
  - Priority: P1
  - Problem: audio, sprites, and backgrounds are loaded eagerly on some routes; this hurts time-to-first-playable especially on mobile.
  - Acceptance Criteria: each game route loads its primary interactive surface within 3s on a simulated mid-tier mobile connection; large assets are lazy-loaded (sound effects, arcade music, and FPS terrain heightmap are handled); METRICS.md updated with measured values.

- [x] **[Q2] Mobile responsiveness and touch input** — verify all game routes work on phone/tablet viewports with touch input.
  - Priority: P1
  - Problem: games were built and tested primarily on desktop; touch controls and layout breakpoints have not been verified on real devices.
  - Acceptance Criteria: Asteroid and at least two other games are fully playable on iOS Safari and Android Chrome; no layout overflow or control dead zones; documented in METRICS.md.

- [x] **[Q2] Accessibility pass** — resolve core a11y issues across game routes and the arcade homepage.
  - Priority: P2
  - Problem: game UI (HUD, scoreboard, menus) lacks ARIA labels, keyboard navigation, and sufficient color contrast in several spots.
  - Acceptance Criteria: no critical or serious a11y violations per axe-core; game control descriptions are accessible; color contrast meets WCAG AA.

- [x] **[Q2] UX verification pass** — walk through all live game routes as a first-time user and document any friction or broken states found.
  - Priority: P2
  - Problem: no structured first-run walkthrough has been performed; hidden friction points and broken states may exist across routes that aren't caught by automated checks.
  - Acceptance Criteria: all live game routes exercised end-to-end; any friction or broken states logged as follow-up issues; findings summarized in METRICS.md or a dedicated audit note.

- [ ] Re-scope expansion work after platform issues are fixed.
  - Priority: P2
  - Milestone: 2026 Q3
  - Problem: feature growth should not outrun packaging, deployment, and runtime stability work.
  - Acceptance Criteria: larger feature initiatives stay sequenced behind the release-path fixes.

- [ ] Fix game selection UI to allow programmatic and keyboard navigation for accessibility and automated testing.

- [x] **Document Memory Match and Dodge Blocks** — documentation corrected across README.md, FEATURES.md, ROADMAP.md, and API.md in the 2026-08-22 audit.
  - Priority: P2
  - Milestone: 2026 Q3

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
