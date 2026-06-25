# Tasks

Last Updated: 2026-06-08

## In Progress

- [ ] **[BLOCKED] Global client-side exception debugging** — All games fail to load in Docker due to a client-side ReferenceError. Last step: capture browser console logs from Dockerized app, diagnose, and fix. See docs/INSTRUCTIONS.md for handoff.

## Todo

- [ ] **[Q2] Performance audit and asset optimization** — identify and fix the largest asset/load-time bottlenecks across game routes.
  - Priority: P1
  - Problem: audio, sprites, and backgrounds are loaded eagerly on some routes; this hurts time-to-first-playable especially on mobile.
  - Acceptance Criteria: each game route loads its primary interactive surface within 3s on a simulated mid-tier mobile connection; large assets are lazy-loaded; METRICS.md updated with measured values.

- [ ] **[Q2] Mobile responsiveness and touch input** — verify all game routes work on phone/tablet viewports with touch input.
  - Priority: P1
  - Problem: games were built and tested primarily on desktop; touch controls and layout breakpoints have not been verified on real devices.
  - Acceptance Criteria: Asteroid and at least two other games are fully playable on iOS Safari and Android Chrome; no layout overflow or control dead zones; documented in METRICS.md.

- [ ] **[Q2] Accessibility pass** — resolve core a11y issues across game routes and the arcade homepage.
  - Priority: P2
  - Problem: game UI (HUD, scoreboard, menus) lacks ARIA labels, keyboard navigation, and sufficient color contrast in several spots.
  - Acceptance Criteria: no critical or serious a11y violations per axe-core; game control descriptions are accessible; color contrast meets WCAG AA.

- [ ] **[Q2] UX verification pass** — walk through all live game routes as a first-time user and document any friction or broken states found.
  - Priority: P2
  - Problem: no structured first-run walkthrough has been performed; hidden friction points and broken states may exist across routes that aren't caught by automated checks.
  - Acceptance Criteria: all live game routes exercised end-to-end; any friction or broken states logged as follow-up issues; findings summarized in METRICS.md or a dedicated audit note.

- [ ] Re-scope expansion work after platform issues are fixed.
  - Priority: P2
  - Milestone: 2026 Q3
  - Problem: feature growth should not outrun packaging, deployment, and runtime stability work.
  - Acceptance Criteria: larger feature initiatives stay sequenced behind the release-path fixes.

- [ ] Fix game selection UI to allow programmatic and keyboard navigation for accessibility and automated testing.

## Audit Notes

- Docker-first validation now succeeds locally, and CI has a dedicated Docker smoke workflow.
- Deployment model is now consistently documented as Next.js runtime on Netlify.
- The Asteroid route audio startup no longer emits repeated `Sound not found: bgm` errors after readiness gating and memoized sound controls.
