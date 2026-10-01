---
up: "[[repos/farm-3j]]"
title: "farm-3j · TASKS"
source: https://github.com/nitsuah/farm-3j/blob/main/docs/TASKS.md
kind: repo-doc
repo: farm-3j
---

# TASKS

> 🧭 [farm-3j](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](../CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-27

_Shipped work (all iter1-109+ RTS feature history) is condensed into
`docs/FEATURES.md`'s "Shipped" section and the root `CHANGELOG.md` — see those
files rather than a duplicated narrative here._

## Done

- [x] Ensure farmers always render in front of barn and remain selectable when barn is clicked
  - Priority: P1
  - Type: Bug

## In Progress

## Todo

### Farm RTS — Round 2 (2027 Q1)

#### Technical Cleanup

- [ ] Continue SVG component extraction — worker body shapes, enemy unit torsos, and building base rects are next candidates
  - Priority: P2
  - Type: Tech debt
- [ ] Profile render loop at 30+ units on 25×25 map; investigate canvas/OffscreenCanvas fallback for mobile
  - Priority: P2
  - Type: Tech debt
- [ ] Add unit tests for core helpers: `tileDist`, `tileToSvg`, A\* pathfinding (damage formulas ✅ covered by towerHelpers/spawnHelpers tests)
  - Priority: P2
  - Type: Tech debt

#### Gameplay Features

- [ ] Save-slot picker UI on the New Game screen (3 cloud-backed slots already shipped)
  - Priority: P1
  - Type: Feature
- [ ] Named unit formations — move selected group in line/wedge/box formation
  - Priority: P2
  - Type: Feature
- [ ] Enemy hero unit — Warlord (wave 20+, unique abilities, drops loot)
  - Priority: P2
  - Type: Feature
- [ ] Dropped hero items — equippable pickups from slain elite enemies (Speed Boots, War Banner, Healing Totem)
  - Priority: P2
  - Type: Feature
- [ ] Achievement / challenge system — milestone badges for specific run conditions
  - Priority: P3
  - Type: Feature
- [ ] Campaign mode Phase 1 — 3 hand-crafted scenarios with scripted objectives
  - Priority: P2
  - Type: Feature

#### Content & Polish

- [ ] Background ambient audio loop with independent volume slider
  - Priority: P3
  - Type: Content
- [ ] More unit voice lines and enemy audio cues (Warchief stomp, Sapper countdown)
  - Priority: P3
  - Type: Content
- [ ] Minimap: show dropped items and loot crate positions
  - Priority: P3
  - Type: Feature
- [ ] Implement grazing logic and food meter for animal units
  - Priority: P2
  - Type: Feature
- [ ] Add buttons to train animal units from Barn
  - Priority: P2
  - Type: Feature

### Legacy Tycoon Tasks (on hold)

- [ ] Complete Farm Tycoon phase 2 core systems (animal needs, feeding, fence, save/load)
  - Priority: P3
  - Type: Feature
- [ ] Refresh README and deployment notes with actual release path.
  - Priority: P3
  - Type: Docs
- [ ] Build content and discovery surfaces (gallery, blog, SEO, accessibility)
  - Priority: P3
  - Type: Feature
- [ ] Plan and implement ecommerce phase 1.
  - Priority: P3
  - Type: Feature
