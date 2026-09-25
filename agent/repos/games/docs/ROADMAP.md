# Roadmap

> 🧭 [games](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

> 2027 planning reset (2026-09-24): 2025 Q4–2026 Q1 (live arcade, Docker release path, Netlify, CI smoke), 2026 Q2
> (performance, mobile UX, a11y audit, UX verification) and the completed 2026 Q3 coverage work (Tank Battle logic
> extraction, TS/audio/UI counted, 98.58% with an 85% CI gate) are shipped — see [FEATURES](./FEATURES.md) /
> [CHANGELOG](./CHANGELOG.md). Every open 2026 Q3/Q4 item was carried into 2027 Q1 below.

## 2027 Q1 - Arcade Polish & Cross-Game Systems (Planned)

### Committed *(carried from 2026 Q3)*

- [ ] Fix game selection UI for keyboard/programmatic navigation (accessibility + automated testing).
- [ ] Add unit/E2E test coverage for Memory Match and Dodge Blocks (iframe-hosted standalone games; not covered by the existing Jest suite).
- [ ] Add high-score persistence to Memory Match (currently shows a win alert but doesn't save best time/moves to localStorage).
- [ ] Add mobile touch controls to Dodge Blocks (keyboard-only today), built as the shared touch-control component below rather than a one-off.
- [ ] **Shared touch-control component** — a single reusable on-screen d-pad/button component; Dodge Blocks is the first consumer, any future mobile game the second. *(moved up from 2026 Q4 exploratory — Dodge Blocks depends on it)*
- [ ] Re-verify Mobile Safari / Mobile Chrome and update the ⚠️ rows in `docs/METRICS.md`'s browser compatibility table.

### Exploratory *(carried from 2026 Q4)*

- [ ] **Per-game achievement system** — unlockable badges per game (e.g. "Survived 10 waves" in Asteroid, "First to 11" in Pong) in localStorage, shown on a cross-game profile page; no server required.
- [ ] **Federated leaderboard** — lightweight global top-score sharing via a Netlify Function or Cloudflare Worker with localStorage-only fallback; one endpoint keyed by `game`.
- [ ] Evaluate additional game work only once the committed items above are closed, not on backlog volume alone.

<!--
1. Organize items by year + quarter (e.g. "2027 Q1").
2. When an item ships, remove it here and condense it into FEATURES.md / CHANGELOG.md.
3. Add new strategic goals as they emerge from user requests or project needs.
4. Keep items high-level (features, milestones) not individual bug fixes.
5. Update "Last Updated" date when making significant changes.
6. Focus on realistic, achievable goals based on project velocity.
-->
