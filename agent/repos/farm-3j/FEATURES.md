# FEATURES.md

## Shipped

- **Core Next.js Architecture** — TypeScript, ESLint, CI baseline; consistent build pipeline for the farm project family.
- **Farm Tycoon Phase 1 MVP** — Playable farm tycoon foundation with core game loop.
- **Farm Tycoon Phase 2a–2f Isometric Grid** — Isometric grid foundation including tile rendering, camera, and terrain system.
- **Farm RTS Milestone 1** — Map/camera foundation: tile-based map rendering and camera controls for the RTS game mode.
- **Farm RTS Milestone 3** — Resource node depletion with visual feedback; harvestable nodes deplete and show low-resource state.

## Planned

### Farm RTS Game (MVP in progress)

- **Resource System** — Wood, stone, and food nodes; workers harvest and return to base
- **Worker Units** — Selectable farmer units with move/harvest commands
- **Building Placement** — Place and upgrade buildings on valid tiles
- **Animal Units** — Chickens, cows, pigs with grazing AI and food meter
- **Win/Lose Conditions** — Objective-based victory and defeat triggers
- **Box Selection** — Drag-select multiple units simultaneously
- **Control Groups** — Numbered group assignments for unit management

### Product & Commerce Surface

- **Product Catalog** - Browse available farm products with descriptions and images.
- **Order Placement** - Submit orders for farm products with delivery or pickup options.
- **Inventory Management** - Track product availability and update stock levels.
- **Customer Accounts** - Allow users to create accounts to manage orders and preferences.
- **Contact Form** - Enable users to send inquiries to the farm.
- **Blog/News Section** - Showcase farm activities, news, and recipes.
- **Subscription Model** - Enable recurring orders for certain products.

### Integrations

- **Payment Gateway Integration** - Integrate with a payment provider (e.g., Stripe, PayPal) for online transactions.
- **Email Service Integration** - Send order confirmations and notifications via email.

## DevOps/Infrastructure

- **CI/CD Pipeline** - Automated build, test, and deployment process.
- **Containerization** - Docker for consistent deployment environments.
- **TypeScript Linting** - Consistent code style enforced through linting.
