# Farm 3J - Interactive Farm Website

_Automatically synced with your [v0.dev](https://v0.dev) deployments_

[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com/austin-hardys-projects/v0-farm-contact-website)
[![Built with v0](https://img.shields.io/badge/Built%20with-v0.dev-black?style=for-the-badge)](https://v0.dev/chat/projects/9OcXcTTsfCh)

## Overview

Farm 3J is an interactive farm website with a full-featured isometric **Real-Time Strategy game** — think Warcraft II / Age of Empires II, built entirely in SVG + React.

- **Farm RTS Game** (`/rtsfarm/play`): Full RTS with workers, combat units, buildings, enemy waves, hero unit, fog of war, tech upgrades, and strategic depth
- **Animated Homepage**: Dynamic farm scene with weather effects, day/night cycle, animated crops, trees, mountains, and wildlife
- **Farm Tycoon Game** (`/farm`): Isometric farm simulation (legacy mode)
- **Responsive Design**: Optimized for mobile and desktop

## Farm RTS — Key Features

### Economy & Workers

- **Farmers** harvest gold, lumber, and stone from resource nodes; return to barn to deposit
- **Auto-gather** on node depletion; Lumber Shed reduces lumber gather time; Windmill passive gold income
- **Loot Crates** spawn on the map every 45s; send farmers to collect for bonus resources
- **Building Destruction Loot Drops** — 30% resource refund when enemies destroy a building

### Combat Units

- **Swordsman** ⚔️ — dedicated fighter, Charge ability [C], trains from Barracks
- **Cavalry** 🐴 — 2× speed, Sprint [S] + Trample passive, trains from Stable
- **Catapult** 🪨 — AoE splash siege, trains from Siege Workshop
- **Trebuchet** 🏹 — long-range 9-tile siege unit
- **Hero: Barnabas** 🦸 — 150 HP, +20 ATK, Rallying Cry ⚡ (AoE damage), Harvest Boon 🌾 (2× gather speed), Battle Shout 📯 at level 2 (40% faster attacks for all nearby allies), Morale Aura (30% faster attacks within 3 tiles)

### Buildings

| Building                   | Unlocks                                                                     |
| -------------------------- | --------------------------------------------------------------------------- |
| Farmhouse                  | Food cap +5, barn research upgrades                                         |
| Barracks                   | Swordsman training, Hero recruitment, Veteran Training + War Drums research |
| Stable                     | Cavalry training                                                            |
| Siege Workshop             | Catapult + Trebuchet training                                               |
| Watchtower                 | Arrow fire, Garrison, Guard Tower upgrade                                   |
| Ballista                   | Piercing AoE arrow tower                                                    |
| Frost Tower                | Slowing tower (50% slow, 3s)                                                |
| Blacksmith                 | Steel Edge (+5 ATK/level) + Iron Hide (-2 dmg taken/level)                  |
| Lumber Shed                | -200ms lumber gather per shed                                               |
| Windmill                   | +2 gold passive per 5s                                                      |
| Granary                    | +8 population cap                                                           |
| Market                     | Resource trading (lumber→gold, stone→gold)                                  |
| Palisade Wall / Stone Wall | Blocks enemy pathfinding; upgradeable to Stone (350 HP)                     |
| Spike Trap                 | 20 dmg on trigger, 30s rearm                                                |

### Enemy Waves

- **Grunts** — scale in HP and count each wave; Enraged when Witch Doctor buffs them
- **War Bull** 🐂 — boss every 10th wave (3× HP, 25 dmg)
- **Shaman** 🧙 — heals grunts; spawns wave 8+
- **Troll Archer** 🏹 — kiting ranged unit; spawns wave 10+
- **Witch Doctor** 🔮 — Berserk buff for grunts (+8 dmg); spawns wave 12+
- **Goblin Sapper** 💣 — suicide bomber (80 AoE dmg); spawns wave 12+
- **War Ram** 🪵 — battering ram targeting buildings; spawns wave 6+
- **Demolisher** 💥 — AoE siege catapult; spawns wave 14+
- **Necromancer** 💀 — raises dead grunts as skeletons; spawns wave 16+
- **Enemy Fortress Towers** — spawn at waves 5, 10, 15

### Strategic Systems

- **Fog of War** — unexplored dark, explored-but-not-visible dimmed; all enemy units hidden in fog
- **Day/Night Cycle** — grunts 30% faster at night; visual dark overlay
- **Neutral Creep Camps** — clear for 60🪙 bonus; grants unit XP
- **Neutral Shrines** — capture Shrine of War (+5 ATK) or Shrine of Plenty (+15% gather speed)
- **Unit Veterancy** — XP → Level 1 (+10 HP, +5 ATK) → Level 2 (+10 HP, +5 ATK)
- **Tech Research** — Barracks (Veteran Training, War Drums), Blacksmith (Steel Edge, Iron Hide), Barn (Sharper Tools, Swift Harvest, Iron Will), Guard Tower upgrade
- **Control Groups** — Ctrl+1-9 assign; double-tap to center camera; group bar in HUD
- **Attack-Move [A]**, **Hold Position [H]**, **Patrol [P]**, **Sprint [S]**, **Charge [C]**
- **Tab** cycles idle workers; **Ctrl+A** selects all; **Ctrl+click** add/remove unit from selection
- **Shift+right-click** queues waypoints; **Box selection** drag-lasso
- **Garrison** — units in barn or watchtower for HP regen / tower buff
- **Save/Load** — full game state auto-saved to localStorage every 30s
- **Upkeep System** — WC3-style gold income penalty at 41+ and 81+ food
- **Wave Preview** — composition shown 6s before each wave arrives

### Polish & Feel

- **Difficulty Selection** — Easy 🌻 / Normal ⚔️ / Hard 💀 picker before each game; scales resources, enemy HP/damage/speed, and wave interval
- **Procedural Sounds** — Web Audio API tones for select, move, attack, death, build, ability, garrison, wave warning, victory/defeat; 🔊/🔇 mute toggle
- **Unit Voice Lines** — WC3-style acknowledgement text on move/attack commands ("Moving out!", "Charge!", "For glory!")
- **Tower Range Rings** — faint dashed ellipses show attack radius for all defensive towers; also shown in build-mode ghost preview
- **Ambient Chickens** — 5 decorative farm chickens wander near the barn
- **Hit-Flash** — workers flash red, grunts flash white on damage
- **Move-Target Ring** — expanding green circle confirms move destination
- **Minimap Fog of War** — dark overlay on unexplored minimap tiles
- **Resource Depletion Alerts** — "Depleted!" floating text when nodes run dry
- **High-Score Leaderboard** — top 5 runs saved to localStorage; shown on game-over screen

## Tech Stack

- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS v4
- **Package Manager**: pnpm 9
- **Rendering**: SVG-based isometric grid (25×25 tiles, 64px tile size)
- **Pathfinding**: 8-directional A\* with wall avoidance
- **Audio**: Web Audio API procedural tone synthesis (no audio files)
- **State**: React useState/useRef + requestAnimationFrame animation loop
- **Shared SVG Components**: `HpBar`, `StructureDamageSmoke`, `StructureFireEffect` — parameterized primitives reused across all map layers
- **Database**: Neon Postgres (serverless) via `@neondatabase/serverless` for cloud saves and high scores
- **Testing**: Vitest with @vitest/coverage-v8; 440 tests across `lib/`, `components/`, and RTS domain hooks

## Site Pages

| Route           | Description                                                                                      |
| --------------- | ------------------------------------------------------------------------------------------------ |
| `/`             | Animated homepage with farm scene, weather effects, day/night cycle, animated crops and wildlife |
| `/about`        | About page with contact modal (submits to `POST /api/contact`)                                   |
| `/farm`         | Farm Tycoon legacy isometric simulation game                                                     |
| `/rtsfarm`      | PG Farms RTS landing page — feature overview, unit roster, building catalog                      |
| `/rtsfarm/play` | Playable Farm RTS game                                                                           |
| `/privacy`      | Privacy & Security page — localStorage, cloud saves, device ID, and contact data policy          |

## API Routes

| Route                        | Description                                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `POST /api/contact`          | Contact form endpoint with server-side validation; optional webhook forwarding via `FARM_CONTACT_WEBHOOK_URL` |
| `GET/POST/DELETE /api/saves` | Cloud save slots (0–2) backed by Neon Postgres with localStorage fallback                                     |
| `GET/POST /api/highscores`   | High-score leaderboard backed by Neon Postgres with localStorage fallback                                     |

## Local Development

```bash
# Install dependencies (requires Node 20+)
corepack enable
corepack prepare pnpm@9.0.0 --activate
pnpm install

# Start dev server
pnpm dev
# → http://localhost:3000

# Run tests
pnpm test

# Run tests with coverage
pnpm test:coverage

# Type-check
pnpm type-check

# Lint
pnpm lint

# Format
pnpm format
```

**Environment variables** (copy `.env.example` to `.env.local`):

| Variable                   | Required               | Description                              |
| -------------------------- | ---------------------- | ---------------------------------------- |
| `DATABASE_URL`             | For cloud saves/scores | Neon Postgres connection string          |
| `FARM_CONTACT_WEBHOOK_URL` | Optional               | Webhook URL for contact form submissions |

This repository will stay in sync with your deployed chats on [v0.dev](https://v0.dev).
Any changes you make to your deployed app will be automatically pushed to this repository from [v0.dev](https://v0.dev).

## Deployment

Your project is live at:

**[https://vercel.com/austin-hardys-projects/v0-farm-contact-website](https://vercel.com/austin-hardys-projects/v0-farm-contact-website)**

## Build your app

Continue building your app on:

**[https://v0.dev/chat/projects/9OcXcTTsfCh](https://v0.dev/chat/projects/9OcXcTTsfCh)**

## Contact Form Delivery

The About page contact modal now submits to `POST /api/contact` with server-side validation.

- `FARM_CONTACT_WEBHOOK_URL` (optional): when set, submissions are forwarded to this webhook.
- If the webhook is not configured, submissions are still accepted and logged server-side (`delivery: local-log`) so the UI keeps a validated success/error flow in non-production setups.

## How It Works

1. Create and modify your project using [v0.dev](https://v0.dev)
2. Deploy your chats from the v0 interface
3. Changes are automatically pushed to this repository
4. Vercel deploys the latest version from this repository

## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:

- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md
