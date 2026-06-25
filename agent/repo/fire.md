# fire

> Reviewed: 2026-06-25

## Overview

100% client-side FIRE (Financial Independence, Retire Early) calculator and tracker. Runs locally via Docker (nginx/Alpine), stores all data in `localStorage`, no external server dependencies. Features net worth projections, CSV imports (Fidelity, Chase, Capital One), CD ladder visualizer, side gig hub, and eBay profit calculator.

## Current Goals / Roadmap Focus

**Q2 2026:** ✅ Completed — full tracker foundation shipped

**Q3 2026 (mostly complete):**
- [x] Side gig tracker (Etsy, FB Marketplace, Craigslist)
- [x] eBay Fee & Shipping Margin Calculator
- [x] Chase + Capital One CSV statement upload
- [x] CD Ladder visualizer with maturity alerts

**Q4 2026:**
- [ ] Tax drag estimation engine (custom federal/state brackets, capital gains)
- [x] Multi-scenario FIRE date comparison
- [ ] Webhook-based or automated local sync templates
- [x] Mobile-responsive adjustments
- [ ] Lightweight PWA packaging

**Ongoing direction:**
- Keep building FIRE dashboard, add features for financial independence tracking
- Ensure usable API for MCP/LLM consumption
- Keep UI minimalist

## Open P0/P1 Tasks

- [ ] Tax drag estimation engine with custom bracket support (Q4 backlog)
- [ ] PWA packaging for offline access (Q4 backlog)
- [ ] Webhook/automated local sync templates (Q4 backlog)

No P0/P1 blockers. Most Q3 work is complete. Remaining items are Q4 exploratory.

## Blockers

None documented.

## Recent Changes (Unreleased / CHANGELOG)

- API endpoints for user profiles and authentication (placeholder in CHANGELOG)
- CRUD for income, expense, investment transactions
- Data models for financial records
- Initial net worth + FIRE progress calculations
- Basic data persistence layer placeholder
- Middleware for request validation and error handling

Note: CHANGELOG `[Unreleased]` appears generic/boilerplate. Actual shipped features documented in FEATURES.md (see Q3 items above marked [x]).
