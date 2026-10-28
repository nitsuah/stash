---
up: "[[repos/skyview]]"
title: "skyview · README"
source: https://github.com/nitsuah/skyview/blob/main/README.md
kind: repo-doc
repo: skyview
---

# 🚁 SkyView Dynamics - Cinematic Drone Services

> 🧭 **skyview** · [Features](./docs/FEATURES.md) · [Roadmap](./docs/ROADMAP.md) · [Tasks](./docs/TASKS.md) · [Changelog](./docs/CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

[![Netlify Status](https://api.netlify.com/api/v1/badges/bea254e2-2234-434c-82d1-ffb8a8c2dd26/deploy-status)](https://app.netlify.com/projects/skyviewd/deploys) [![Playwright Tests](https://github.com/nitsuah/skyview/actions/workflows/playwright.yml/badge.svg)](https://github.com/nitsuah/skyview/actions/workflows/playwright.yml) [![Docker Smoke](https://github.com/nitsuah/skyview/actions/workflows/docker-smoke.yml/badge.svg)](https://github.com/nitsuah/skyview/actions/workflows/docker-smoke.yml)

**Last Updated:** 2026-08-22 (documentation audit)

## What's New
- New CI workflow to regenerate screenshots and diagrams (first bot run pending); Pages showcase simplified to the booking flow, with an 18s video (2026-10-14)
- GitHub Pages project showcase with launch reel (2026-10-01)
- Documentation audit and accuracy pass (2026-08-22)
- Marketplace platform backend added: Netlify Functions, Neon DB, Stripe Connect, React SPA at /app (2026-06-08)
- Motion polish, browser monitoring, and conversion reporting baseline (2026-04-06)
- Launch visual identity refresh and dark-mode booking embed (2026-04-06)
- Docker smoke validation and coverage reporting (2026-03-27)

## 🤝 Contributing
See [CONTRIBUTING.md](https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md) (org default) for guidelines, code of conduct, and how to get involved.

## 🔗 Quick Links
- Live Site: https://skyviewd.netlify.app is offline (Netlify returns site-not-found); see the [Project Showcase](https://nitsuah.github.io/skyview/) for the booking flow
- [Project Showcase](https://nitsuah.github.io/skyview/) (GitHub Pages: how clients and pilots get matched, with an 18s video; page source in `showcase/`, video source in [`promo/`](promo/README.md))
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Owner Guide](docs/OWNER_GUIDE.md)
- [Getting Started](docs/GETTING_STARTED.md)
- [Metrics](METRICS.md)
- [Features](docs/FEATURES.md)
- [Roadmap](docs/ROADMAP.md)
- [Tasks](docs/TASKS.md)

A stunning, high-tech website for professional drone services featuring a minimalist design with full-bleed photography, dark high-contrast aesthetics, and glassmorphic UI elements.

## 🎨 Design Features

- **Color Palette**: Deep charcoal/black (#1A1A1A) with electric blue/cyan (#00FFFF) accents
- **Typography**: Modern Inter font family with bold weights and capitalization
- **Visual Style**: Glassmorphic cards with futuristic HUD-inspired design
- **Animations**: Smooth micro-animations, parallax effects, and glow effects
- **Responsive**: Mobile-first design that adapts beautifully to all screen sizes

## 🚀 Quick Start

**📘 New Owner?** Start with **[OWNER_GUIDE.md](docs/OWNER_GUIDE.md)** - your complete 30-minute launch guide!

**🛠️ Developer?** See **[Getting Started Guide](docs/GETTING_STARTED.md)** for technical setup.

### Run Locally

Use `npm run dev` for the full development experience (includes Netlify Functions and form handling):

```bash
# Full dev server (Netlify CLI included as devDependency)
npm run dev            # Runs netlify dev on port 8888

# Static-only fallback (no Netlify Functions)
npx http-server . -p 3000

# Using Python
python -m http.server 3000
```

Then open: [localhost:3000](http://localhost:3000)

### Run With Docker

```bash
# Serve the production image locally
docker compose -f config/docker-compose.yml up --build web

# Run unit coverage in a container
docker compose -f config/docker-compose.yml run --rm unit
```

### Deploy to Production

See **[🚀 Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** for Netlify deployment steps.

## 🔧 Technical Stack

- **HTML5**: Semantic structure.
- **CSS3**: Modern variables, flexbox/grid, glassmorphism.
- **JavaScript**: ES6 Modules (`scripts/`).
- **Testing**:
  - **E2E**: Playwright (`npx playwright test --config config/playwright.config.ts`)
  - **Journeys**: nightly Playwright "AI user" journeys with visual baselines (`npm run test:journeys`, Docker image only); failures file `bot:journey` issues, and [BUGS.md](https://github.com/nitsuah/skyview/blob/bot/journeys/BUGS.md) lists what is open
  - **Unit**: Vitest (`npx vitest run --config config/vitest.config.ts`) — both run in CI on every PR to `main`
- **Netlify**: Hosting, Forms, and Functions.

## 🎯 Features

### Core Features
- ✅ Full-screen hero with video background
- ✅ Glassmorphic service cards
- ✅ Dynamic gallery with lightbox
- ✅ Contact form with Netlify Forms
- ✅ Calendly booking integration
- ✅ Mobile hamburger menu
- ✅ Smooth scroll navigation
- ✅ WebP images with fallbacks
- ✅ Performance monitoring

### Business Features
- ✅ Privacy policy page (GDPR-compliant)
- ✅ Testimonials section
- ✅ Client portal prototype
- ✅ Feature flags system
- ✅ Email notifications
- ✅ Campaign personalization (UTM/referrer-based hero variants)
- ✅ A/B testing framework (feature-gated; enable via config.js)
- ✅ Conversion funnel tracking with local dashboard and CSV/JSON export
- ✅ Marketplace platform (Netlify Functions + React SPA at /app; enable via platform flag)
- ✅ CSP and security headers (enforced in netlify.toml)
- ✅ FAA cert expiry cron (daily Netlify scheduled function)

## 📦 NPM Scripts

```bash
# Development
npm run dev            # Start Netlify dev server (port 8888; requires netlify-cli)

# Testing
npm test              # Run Playwright E2E tests
npm run test:journeys # Nightly journeys (baselines are Linux: run in the Playwright Docker image)
npm run test:unit     # Run Vitest unit tests with coverage
docker compose -f config/docker-compose.yml run --rm unit  # Run unit tests with coverage in Docker

# Build
npm run build          # Build platform SPA (React app to dist/app/)
npm run db:migrate     # Run Neon database migrations (platform feature)

# Linting
npm run lint:js        # ESLint (config/eslint.config.mjs)
npm run lint:css       # Stylelint (config/stylelint.config.mjs)
pre-commit run --all-files --config config/.pre-commit-config.yaml  # pre-commit hooks (install with: pre-commit install --config config/.pre-commit-config.yaml)

# Optimization
npm run optimize:images  # Convert images to WebP
```

## 📚 Documentation

### Start Here
- 📖 **[Getting Started Guide](docs/GETTING_STARTED.md)** - **Start here!** Complete setup walkthrough
- 🛠️ [Platform Setup](docs/FINAL_SETUP.md) - Neon, Netlify env vars, Resend, Google OAuth, Stripe, and local dev for the `/app` marketplace
- 📘 [Owner's Guide](docs/OWNER_GUIDE.md) - 30-minute non-technical launch guide

### Deployment & Management
- 🚀 [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Netlify deployment
- ⚙️ [Configuration Reference](docs/CONFIG.md) - All config.js options
- 📧 [Email Notifications](docs/EMAIL_NOTIFICATIONS.md) - Form notification setup
- 📊 [Analytics Setup](docs/ANALYTICS_SETUP.md) - Analytics options
- 🔍 [SEO Guide](docs/SEO_GUIDE.md) - Search engine optimization and submission

### Content Management
- 🖼️ [WebP Optimization](docs/WEBP_OPTIMIZATION.md) - Image optimization guide
- 🔒 [Client Portal](docs/CLIENT_PORTAL.md) - Client file delivery system
- 📁 [Asset Management](docs/ASSET_MANAGEMENT.md) - Organizing media files

### Performance & Monitoring
- ⚡ [Performance Checklist](docs/PERFORMANCE_CHECKLIST.md) - Speed optimization
- 📈 [Optimization Flow](docs/OPTIMIZATION_FLOW.md) - Performance workflow

### Project Overview
- 📋 [Roadmap](./docs/ROADMAP.md) - Project phases and progress
- ✅ [Tasks](./docs/TASKS.md) - Todo list
- 📈 [Metrics](METRICS.md) - Test coverage and performance baseline

## ⚙️ Configuration

### Feature Flags
Edit `config.js` to enable/disable features:

```javascript
features: {
    testimonials: false,    // Testimonials section
    calendly: true,         // Booking widget
    clientPortal: false,    // Client file access
    preview3D: false,       // 3D preview (future)
    analytics: false,       // Analytics tracking
    platform: false        // Marketplace mode (replaces Calendly with operator CTA)
}
```

### Quick Setup
1. Update Calendly URL in `config.js`
2. Enable features you want
3. Run `npm run optimize:images`
4. Deploy to Netlify

See [Configuration Reference](docs/CONFIG.md) for detailed steps.

## 🚀 Deployment

### Deploy to Netlify
1. Push to GitHub
2. Connect to Netlify
3. Deploy! (automatic)

See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for complete instructions.

### Performance & SEO
- ✅ WebP images (30-40% smaller)
- ✅ Lazy loading
- ✅ Optimized assets
- ✅ CDN delivery
- ✅ Schema.org structured data
- ✅ Open Graph & Twitter Cards
- ✅ XML sitemap
- 🎯 Lighthouse Score: 90+

## Screenshots & diagrams

Regenerated by CI ([visual-docs.yml](https://github.com/nitsuah/skyview/blob/main/.github/workflows/visual-docs.yml)) from mocked demo data; file names are the feature ids in [`promo/spots.json`](https://github.com/nitsuah/skyview/blob/main/promo/spots.json).

<!-- visual-docs:start -->

<!-- Generated by scripts/visual-docs-readme.mjs — edit the source files, not this block. -->

### Diagrams

**Architecture** — [`docs/diagrams/architecture.svg`](./docs/diagrams/architecture.svg) · source [`docs/diagrams/architecture.mmd`](./docs/diagrams/architecture.mmd)

![Architecture](https://github.com/nitsuah/skyview/blob/main/docs/diagrams/architecture.svg)

**Booking flow** — [`docs/diagrams/booking-flow.svg`](./docs/diagrams/booking-flow.svg) · source [`docs/diagrams/booking-flow.mmd`](./docs/diagrams/booking-flow.mmd)

![Booking flow](https://github.com/nitsuah/skyview/blob/main/docs/diagrams/booking-flow.svg)

### Screenshots

**Dynamic gallery** — [`docs/screenshots/dynamic-gallery.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/dynamic-gallery.png)

![Dynamic gallery](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/dynamic-gallery.png)

**Immersive hero section** — [`docs/screenshots/immersive-hero-section.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/immersive-hero-section.png)

![Immersive hero section](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/immersive-hero-section.png)

**Local dashboard** — [`docs/screenshots/local-dashboard.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/local-dashboard.png)

![Local dashboard](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/local-dashboard.png)

**Native operator scheduling availability** — [`docs/screenshots/native-operator-scheduling-availability.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/native-operator-scheduling-availability.png)

![Native operator scheduling availability](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/native-operator-scheduling-availability.png)

**Native operator scheduling** — [`docs/screenshots/native-operator-scheduling.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/native-operator-scheduling.png)

![Native operator scheduling](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/native-operator-scheduling.png)

**Rate limiting** — [`docs/screenshots/rate-limiting.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/rate-limiting.png)

![Rate limiting](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/rate-limiting.png)

**Responsive design** — [`docs/screenshots/responsive-design.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/responsive-design.png)

![Responsive design](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/responsive-design.png)

**Service packages** — [`docs/screenshots/service-packages.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/service-packages.png)

![Service packages](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/service-packages.png)

**Time bound token expiry** — [`docs/screenshots/time-bound-token-expiry.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/time-bound-token-expiry.png)

![Time bound token expiry](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/time-bound-token-expiry.png)

**Token generator** — [`docs/screenshots/token-generator.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/token-generator.png)

![Token generator](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/token-generator.png)

**Two sided marketplace operators** — [`docs/screenshots/two-sided-marketplace-operators.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/two-sided-marketplace-operators.png)

![Two sided marketplace operators](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/two-sided-marketplace-operators.png)

**Two sided marketplace post job** — [`docs/screenshots/two-sided-marketplace-post-job.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/two-sided-marketplace-post-job.png)

![Two sided marketplace post job](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/two-sided-marketplace-post-job.png)

**Two sided marketplace** — [`docs/screenshots/two-sided-marketplace.png`](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/two-sided-marketplace.png)

![Two sided marketplace](https://github.com/nitsuah/skyview/blob/main/docs/screenshots/two-sided-marketplace.png)

<!-- visual-docs:end -->

---

> **Built with ❤️ for SkyView Dynamics by nitsuah**
## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md

<!-- docs-index:start -->

## Docs Index

Every doc at the repo root (other than this README) and under `docs/` (the files mirrored into the Obsidian vault), so none of them is orphaned.

- [Analytics Setup Guide](./docs/ANALYTICS_SETUP.md) — `docs/ANALYTICS_SETUP.md`
- [Asset Management Guide](./docs/ASSET_MANAGEMENT.md) — `docs/ASSET_MANAGEMENT.md`
- [Changelog](./docs/CHANGELOG.md) — `docs/CHANGELOG.md`
- [Client Portal Documentation](./docs/CLIENT_PORTAL.md) — `docs/CLIENT_PORTAL.md`
- [Feature Flags & Configuration Guide](./docs/CONFIG.md) — `docs/CONFIG.md`
- [🚀 Production Deployment Guide](./docs/DEPLOYMENT_GUIDE.md) — `docs/DEPLOYMENT_GUIDE.md`
- [Email Notification Setup for Netlify Forms](./docs/EMAIL_NOTIFICATIONS.md) — `docs/EMAIL_NOTIFICATIONS.md`
- [Skyview Features](./docs/FEATURES.md) — `docs/FEATURES.md`
- [SkyView Dynamics — Platform Setup](./docs/FINAL_SETUP.md) — `docs/FINAL_SETUP.md`
- [Getting Started with SkyView Website](./docs/GETTING_STARTED.md) — `docs/GETTING_STARTED.md`
- [Image Optimization Flow](./docs/OPTIMIZATION_FLOW.md) — `docs/OPTIMIZATION_FLOW.md`
- [SkyView Website - Owner's Guide](./docs/OWNER_GUIDE.md) — `docs/OWNER_GUIDE.md`
- [Performance Optimization Checklist](./docs/PERFORMANCE_CHECKLIST.md) — `docs/PERFORMANCE_CHECKLIST.md`
- [Skyview Roadmap](./docs/ROADMAP.md) — `docs/ROADMAP.md`
- [SEO Implementation Guide](./docs/SEO_GUIDE.md) — `docs/SEO_GUIDE.md`
- [Tasks](./docs/TASKS.md) — `docs/TASKS.md`
- [Image Optimization Guide - WebP Format](./docs/WEBP_OPTIMIZATION.md) — `docs/WEBP_OPTIMIZATION.md`

**`docs/archive/`**

- [🎯 Project Status Summary](./docs/archive/PROJECT_STATUS.md) — `docs/archive/PROJECT_STATUS.md`
- [Archived Documentation](./docs/archive/README.md) — `docs/archive/README.md`
- [Session Summary: WebP Optimization & Performance Enhancement](./docs/archive/SESSION_SUMMARY.md) — `docs/archive/SESSION_SUMMARY.md`
- [WebP Optimization - Implementation Summary](./docs/archive/WEBP_IMPLEMENTATION.md) — `docs/archive/WEBP_IMPLEMENTATION.md`

**`repo root`**

- [Skyview Metrics](./METRICS.md) — `METRICS.md`

<!-- docs-index:end -->
