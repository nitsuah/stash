# TASKS

> 🧭 [farm-3j](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](../CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

_Shipped work (all iter1-109+ RTS feature history) is condensed into
`docs/FEATURES.md`'s "Shipped" section and the root `CHANGELOG.md` — see those
files rather than a duplicated narrative here._

## Farm RTS — Round 2 (2027 Q1)

### Technical Cleanup

- [ ] Continue SVG component extraction — worker body shapes, enemy unit torsos, and building base rects are next candidates
- [ ] Profile render loop at 30+ units on 25×25 map; investigate canvas/OffscreenCanvas fallback for mobile
- [ ] Add unit tests for core helpers: `tileDist`, `tileToSvg`, A\* pathfinding (damage formulas ✅ covered by towerHelpers/spawnHelpers tests)

### Gameplay Features

- [ ] Save-slot picker UI on the New Game screen (3 cloud-backed slots already shipped)
- [ ] Named unit formations — move selected group in line/wedge/box formation
- [ ] Enemy hero unit — Warlord (wave 20+, unique abilities, drops loot)
- [ ] Dropped hero items — equippable pickups from slain elite enemies (Speed Boots, War Banner, Healing Totem)
- [ ] Achievement / challenge system — milestone badges for specific run conditions
- [ ] Campaign mode Phase 1 — 3 hand-crafted scenarios with scripted objectives

### Content & Polish

- [ ] Background ambient audio loop with independent volume slider
- [ ] More unit voice lines and enemy audio cues (Warchief stomp, Sapper countdown)
- [ ] Minimap: show dropped items and loot crate positions
- [ ] Ensure farmers always render in front of barn and remain selectable when barn is clicked
- [ ] Implement grazing logic and food meter for animal units
- [ ] Add buttons to train animal units from Barn

## Legacy Tycoon Tasks (on hold)

- [ ] Complete Farm Tycoon phase 2 core systems (animal needs, feeding, fence, save/load)
- [ ] Refresh README and deployment notes with actual release path.
- [ ] Build content and discovery surfaces (gallery, blog, SEO, accessibility)
- [ ] Plan and implement ecommerce phase 1.
