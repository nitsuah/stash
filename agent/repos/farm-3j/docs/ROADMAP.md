# ROADMAP

> 🧭 [farm-3j](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](../CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

> 2027 planning reset (2026-09-24): 2026 Q1 (Next.js core, Farm Tycoon Phase 1 + 2a–2f) and the 2026 Q2–Q3 Farm RTS MVP
> (feature-complete, incl. cloud saves/save slots and modularization Phases 1, 2a, 2b) are shipped and condensed in
> [FEATURES](./FEATURES.md) / [CHANGELOG](../CHANGELOG.md). Every open 2026 Q3 "Round 2" and 2026 Q4 product item was
> carried into 2027 Q1 below for triage at planning.

## 2027 Q1 - Farm RTS Round 2 + Product Surface (Planned)

### Technical Health _(carried from 2026 Q3)_

- [ ] Continue SVG component extraction — worker body shapes, enemy unit torsos, building base rects are next candidates for shared components (see iter109 pattern)
- [ ] Profile render loop on 25×25 map with 30+ units; investigate canvas or OffscreenCanvas fallback if SVG drops below 30fps on mobile
- [ ] Add unit tests for remaining core helpers: `tileDist`, `tileToSvg`, A\* pathfinding (damage formulas and map selectors already covered)

### Gameplay Features _(carried from 2026 Q3)_

- [ ] **Save-slot picker UI** — the 3 cloud-backed slots (0/1/2) shipped 2026-08-07; the slot picker on the New Game screen is still TBD
- [ ] **Named formations** — move a selected group in line, wedge, or box formation; prevents units stacking on the same tile
- [ ] **Enemy hero unit** — Warlord spawns at wave 20+; unique abilities (War Cry, Shield Bash); harder than Warchief, drops rare item
- [ ] **Dropped hero items** — slain enemy elites drop equippable items Barnabas can pick up (Speed Boots, War Banner, Healing Totem); persists between hero deaths
- [ ] **Challenge / achievement system** — milestone badges (e.g. "Survive 20 waves without losing a building", "Kill 5 Sappers before they explode")
- [ ] **Campaign mode (Phase 1)** — linear sequence of 3 hand-crafted scenarios with scripted objectives beyond "defend the barn"

### Content & Polish _(carried from 2026 Q3)_

- [ ] Background ambient audio loop (farm sounds, wind, distant battle) with independent volume slider
- [ ] More unit voice lines and enemy audio cues (Warchief stomp roar, Sapper countdown tick)
- [ ] Minimap: show dropped hero items and loot crate positions
- [ ] Ensure farmers always render in front of barn and remain selectable when barn is clicked
- [ ] Implement grazing logic and a food meter for animal units
- [ ] Add buttons to train animal units from the Barn
- [ ] **Post-game replay** — snapshot key events (wave starts, hero deaths, boss spawns) so the game-over screen can offer a lightweight timeline scrub of the run, without a deterministic replay engine
- [ ] **Adaptive difficulty nudge** — use leaderboard win/loss + wave-reached history to suggest a difficulty on the New Game screen

### Product and Content Surface _(carried from 2026 Q4)_

- [ ] Improve the product gallery and catalog surface.
- [ ] Add a blog or news publishing path.
- [ ] Ship ecommerce phase 1.
- [ ] Evaluate subscription or recurring-order follow-ons.
- [ ] Harden accessibility and SEO for a broader launch.

## On Hold - Legacy Tycoon (unscheduled)

- [ ] Finish the animal needs loop (hunger, thirst, happiness lifecycle).
- [ ] Finish feeding mechanics and inventory interactions.
- [ ] Finish fence placement and terrain editing workflows.
- [ ] Add save/load state and building expansion follow-on work.
- [ ] Validate the full gameplay loop end-to-end in Docker (start game → build → feed animals → save → reload).
