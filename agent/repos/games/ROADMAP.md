# Roadmap

Last Updated: 2026-06-08

## 2025 Q4 – 2026 Q1 ✅

> Completed. Live multi-game arcade, Docker release path, CI smoke validation, Netlify hosting model, audio init fixes, architecture docs, and deferred homepage audio loading all shipped.

## 2026 Q2 (Planned)

- [ ] **Performance and large-asset delivery**: audit and improve game asset loading (audio, sprites, backgrounds); lazy-load non-critical assets; reduce time-to-first-playable.
- [ ] **Responsiveness and mobile UX**: verify game routes on mobile viewports; fix any touch/input regressions; ensure Asteroid and other games are playable on phone/tablet.
- [ ] **Accessibility audit**: run and resolve core a11y issues (keyboard navigation, ARIA for game controls, color contrast on HUD/scoreboard).
- [ ] **UX verification pass**: walk through all live game routes as a first-time user; document any friction or broken states found.

## 2026 Q3 (Planned)

- [ ] Prioritize progression and platform features only after release reliability is stable.
- [ ] Evaluate additional game work based on evidence, not backlog volume.

## 2026 Q4 (Exploratory)

- [ ] **Per-game achievement system** — unlockable badges per game (e.g., "Survived 10 waves" in Asteroid, "First to 11 in Pong") stored in localStorage and displayed on a cross-game profile page; no server required, drives replayability across the arcade without adding backend complexity.
- [ ] **Federated leaderboard** — lightweight global top-score sharing via a Netlify Function or Cloudflare Worker; graceful localStorage-only fallback when offline; single shared endpoint serves all games via a `game` key.

<!--
1. Organize items by Quarter (Q1, Q2, etc.) or time period.
2. Mark items as [x] when completed, move to appropriate section.
3. Add new strategic goals as they emerge from user requests or project needs.
4. Keep items high-level (features, milestones) not individual bug fixes.
5. Update "Last Updated" date when making significant changes.
6. Focus on realistic, achievable goals based on project velocity.
-->
