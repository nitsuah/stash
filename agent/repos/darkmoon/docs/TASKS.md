# Tasks

> 🧭 [darkmoon](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

## In Progress

_None._

## Done

_Shipped work is condensed into `docs/FEATURES.md`
(gameplay/server capabilities), and `docs/CHANGELOG.md` (change-by-change history) —
see those files rather than a duplicated narrative here._

## Todo

- [ ] Revisit the eslint 10 bump (issue #446, closed-unmerged PR #445) once `eslint-plugin-jsx-a11y` supports it. (P3 · Tech Debt · Confidence: High) Blocked externally: as of the 2026-09-24 PMO audit, `npm view eslint-plugin-jsx-a11y peerDependencies` still caps `eslint` at `^9`. Acceptance Criteria: when a jsx-a11y release allows eslint 10, bump both, `npm run lint` passes in Docker, and #446 is closed.

- [ ] **[2027-Q1] 21st.dev component integration pass** — replace or augment key game site UI surfaces (lobby, scoreboard, game-over, nav) with 21st.dev components to improve visual quality and interactivity.
  - Priority: P1
  - Problem: current UI is functional but prototype-grade; 21st.dev components can significantly improve look, feel, and animation quality without a full rewrite.
  - Acceptance Criteria: at least lobby, scoreboard, and game-over screens use 21st.dev components; hover states, transitions, and layout quality are demonstrably improved; no regression in game functionality.

- [ ] **[2027-Q1] UI/UX interactivity improvements** — improve micro-interactions, card layouts, and overall interactivity across the site using 21st.dev patterns.
  - Priority: P1
  - Problem: the site feels static outside of actual gameplay; improving interactivity increases perceived quality and engagement before a player even starts a game.
  - Acceptance Criteria: game cards, stat panels, and navigation have consistent hover/focus states; page transitions are smooth; Lighthouse performance score does not regress.

- [ ] **[2027-Q1] Open-source safety scrub** — sanitize repository content to remove potentially sensitive, proprietary, or over-specific company and resume details before broader sharing/open sourcing.
  - Priority: P1
  - Problem: historical examples may include details that are too specific for public exposure.
  - Acceptance Criteria: sensitive examples are removed or anonymized; docs are reviewed for proprietary references; a final pass confirms public-share readiness.

- [ ] Re-baseline the remaining large-file refactor work.
  - Priority: P2
  - Problem: older refactor tasks no longer match the codebase hotspots.
  - Acceptance Criteria: only current, high-value refactors remain and each one ties back to reliability, testability, or performance.

- [ ] **[Phase E remaining] Over-the-shoulder aim camera + combat music** — remaining Phase E items after PR #391 landed most of the polish pass.
  - Priority: P2
  - Note: HUD, ammo, reload bar, kill feed, damage numbers, hit marker, ShotgunVFX, reserve ammo, tag-mode health, reload snap mechanic, homepage redesign, and GameUI/Solo componentization are all done. Remaining: over-the-shoulder aim-mode camera offset and a combat music layer that cross-fades when shooting/hit events occur.
  - Acceptance Criteria: see `docs/projects/multi/MULTIPLAYER_SHOOTER_ROADMAP.md` Phase E "Remaining" section.

- [ ] Ship the first validated multiplayer-capable experience now that the readiness gate and server-side tag parity are both done — remaining work is a shipped client experience driving the existing socket events. See `docs/ROADMAP.md` 2027 Q1.

## Notes

- See [INSTRUCTIONS](./INSTRUCTIONS.md) for agent handoff and workflow best practices.
- The deployed site presents solo mode as live and multiplayer or tournament work as planned.
