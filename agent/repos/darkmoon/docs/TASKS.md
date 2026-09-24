# Tasks

Last Updated: 2026-09-23

## In Progress

_None._

## Done

_Shipped work is condensed into `docs/ROADMAP.md` (milestones), `docs/FEATURES.md`
(gameplay/server capabilities), and `CHANGELOG.md` (change-by-change history) —
see those files rather than a duplicated narrative here._

## Todo

- [ ] **[Q2-CEO] 21st.dev component integration pass** — replace or augment key game site UI surfaces (lobby, scoreboard, game-over, nav) with 21st.dev components to improve visual quality and interactivity.
  - Priority: P1
  - Problem: current UI is functional but prototype-grade; 21st.dev components can significantly improve look, feel, and animation quality without a full rewrite.
  - Acceptance Criteria: at least lobby, scoreboard, and game-over screens use 21st.dev components; hover states, transitions, and layout quality are demonstrably improved; no regression in game functionality.

- [ ] **[Q2-CEO] UI/UX interactivity improvements** — improve micro-interactions, card layouts, and overall interactivity across the site using 21st.dev patterns.
  - Priority: P1
  - Problem: the site feels static outside of actual gameplay; improving interactivity increases perceived quality and engagement before a player even starts a game.
  - Acceptance Criteria: game cards, stat panels, and navigation have consistent hover/focus states; page transitions are smooth; Lighthouse performance score does not regress.

- [ ] **[Q2-CEO] Open-source safety scrub** — sanitize repository content to remove potentially sensitive, proprietary, or over-specific company and resume details before broader sharing/open sourcing.
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
  - Acceptance Criteria: see `docs/MULTIPLAYER_SHOOTER_ROADMAP.md` Phase E "Remaining" section.

- [ ] Ship the first validated multiplayer-capable experience now that the readiness gate and server-side tag parity are both done — remaining work is a shipped client experience driving the existing socket events. See `docs/ROADMAP.md` 2026 Q3.

## See also: docs/INSTRUCTIONS.md for agent handoff and workflow best practices.

- The deployed site presents solo mode as live and multiplayer or tournament work as planned.
