# Roadmap

Last Updated: 2026-08-28

## 2025 Q4 – 2026 Q1 ✅

> Completed. Live multi-game arcade, Docker release path, CI smoke validation, Netlify hosting model, audio init fixes, architecture docs, and deferred homepage audio loading all shipped.

## 2026 Q2 (Completed)

- [x] **Performance and large-asset delivery**: audit and improve game asset loading (audio, sprites, backgrounds); lazy-load non-critical assets; reduce time-to-first-playable.
- [x] **Responsiveness and mobile UX**: verify game routes on mobile viewports; fix any touch/input regressions; ensure Asteroid and other games are playable on phone/tablet.
- [x] **Accessibility audit**: run and resolve core a11y issues (keyboard navigation, ARIA for game controls, color contrast on HUD/scoreboard).
- [x] **UX verification pass**: walk through all live game routes as a first-time user; document any friction or broken states found.

## 2026 Q3 (Planned)

- [ ] Fix game selection UI for keyboard/programmatic navigation (accessibility + automated testing).
- [ ] Add unit/E2E test coverage for Memory Match and Dodge Blocks (iframe-hosted standalone games; not covered by the existing Jest suite).
- [ ] Add high-score persistence to Memory Match (currently shows a win alert but doesn't save best time/moves to localStorage).
- [ ] Add mobile touch controls to Dodge Blocks (keyboard-only today).
- [ ] Evaluate additional game work only once the above release-reliability items are closed, not on backlog volume alone.

## 2026 Q4 (Exploratory)

- [ ] **Per-game achievement system** — unlockable badges per game (e.g., "Survived 10 waves" in Asteroid, "First to 11 in Pong") stored in localStorage and displayed on a cross-game profile page; no server required, drives replayability across the arcade without adding backend complexity.
- [ ] **Federated leaderboard** — lightweight global top-score sharing via a Netlify Function or Cloudflare Worker; graceful localStorage-only fallback when offline; single shared endpoint serves all games via a `game` key.
- [ ] **Shared touch-control component** — new idea (2026-08-28): Dodge Blocks needs touch controls now (Q3 item above), and any future mobile game will hit the same gap. A single reusable on-screen d-pad/button component (rather than a one-off for Dodge Blocks) would pay for itself on the second game that needs it, and the achievement/leaderboard work above already assumes a shared cross-game component pattern.

<!--
1. Organize items by Quarter (Q1, Q2, etc.) or time period.
2. Mark items as [x] when completed, move to appropriate section.
3. Add new strategic goals as they emerge from user requests or project needs.
4. Keep items high-level (features, milestones) not individual bug fixes.
5. Update "Last Updated" date when making significant changes.
6. Focus on realistic, achievable goals based on project velocity.
-->
