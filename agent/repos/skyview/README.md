# 🚁 SkyView Dynamics - Cinematic Drone Services

[![Netlify Status](https://api.netlify.com/api/v1/badges/bea254e2-2234-434c-82d1-ffb8a8c2dd26/deploy-status)](https://app.netlify.com/projects/skyviewd/deploys) [![Playwright Tests](https://github.com/nitsuah/skyview/actions/workflows/playwright.yml/badge.svg)](https://github.com/nitsuah/skyview/actions/workflows/playwright.yml) [![Docker Smoke](https://github.com/nitsuah/skyview/actions/workflows/docker-smoke.yml/badge.svg)](https://github.com/nitsuah/skyview/actions/workflows/docker-smoke.yml)

**Last Updated:** 2026-04-13 (Overseer/PM compliance review)

##  What’s New
- Motion polish, browser monitoring, and conversion reporting baseline (2026-04-06)
- Launch visual identity refresh and dark-mode booking embed (2026-04-06)
- Docker smoke validation and coverage reporting (2026-03-27)

## 🤝 Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines, code of conduct, and how to get involved.

## 🔗 Quick Links
- [Live Site](https://skyview.nitsuah.io)
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md)
- [Owner Guide](OWNER_GUIDE.md)
- [Getting Started](docs/GETTING_STARTED.md)
- [Metrics](METRICS.md)
- [Features](FEATURES.md)
- [Roadmap](ROADMAP.md)
- [Tasks](TASKS.md)

A stunning, high-tech website for professional drone services featuring a minimalist design with full-bleed photography, dark high-contrast aesthetics, and glassmorphic UI elements.

## 🎨 Design Features

- **Color Palette**: Deep charcoal/black (#1A1A1A) with electric blue/cyan (#00FFFF) accents
- **Typography**: Modern Inter font family with bold weights and capitalization
- **Visual Style**: Glassmorphic cards with futuristic HUD-inspired design
- **Animations**: Smooth micro-animations, parallax effects, and glow effects
- **Responsive**: Mobile-first design that adapts beautifully to all screen sizes

## 🚀 Quick Start

**📘 New Owner?** Start with **[OWNER_GUIDE.md](OWNER_GUIDE.md)** - your complete 30-minute launch guide!

**🛠️ Developer?** See **[Getting Started Guide](docs/GETTING_STARTED.md)** for technical setup.

### Run Locally

You will need a local server to properly load JSON and modules.

```bash
# Using Node.js (Recommended)
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
- **CMS**: Decap CMS (git-based content management).
- **Testing**:
  - **E2E**: Playwright (`npx playwright test`)
  - **Unit**: Vitest (`npx vitest run --config config/vitest.config.ts`)
- **Netlify**: Hosting, Forms, and Identity.

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
- ✅ Admin CMS (Decap CMS)
- ✅ Feature flags system
- ✅ Email notifications

## 📦 NPM Scripts

```bash
# Development
npm run serve          # Start dev server on port 8080

# Testing
npm test              # Run Playwright E2E tests
npx vitest run --config config/vitest.config.ts  # Run unit tests
docker compose -f config/docker-compose.yml run --rm unit  # Run unit tests with coverage in Docker

# Optimization
npm run optimize:images  # Convert images to WebP
```

## 📚 Documentation

### Start Here
- 📖 **[Getting Started Guide](docs/GETTING_STARTED.md)** - **Start here!** Complete setup walkthrough
- 📖 [Quick Start](QUICKSTART.md) - 5-minute local setup
- 📖 [Manual Setup Checklist](docs/MANUAL_SETUP.md) - All configuration steps

### Deployment & Management
- 🚀 [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Netlify deployment
- ⚙️ [Configuration Reference](docs/CONFIG.md) - All config.js options
- 📧 [Email Notifications](docs/EMAIL_NOTIFICATIONS.md) - Form notification setup
- 📊 [Analytics Setup](docs/ANALYTICS_SETUP.md) - Analytics options
- 🔍 [SEO Guide](docs/SEO_GUIDE.md) - Search engine optimization and submission

### Content Management
- 🖼️ [WebP Optimization](docs/WEBP_OPTIMIZATION.md) - Image optimization guide
- 🎬 [WebP Implementation](docs/WEBP_IMPLEMENTATION.md) - Technical details
- 🔒 [Client Portal](docs/CLIENT_PORTAL.md) - Client file delivery system
- 📁 [Asset Management](docs/ASSET_MANAGEMENT.md) - Organizing media files

### Performance & Monitoring
- ⚡ [Performance Checklist](docs/PERFORMANCE_CHECKLIST.md) - Speed optimization
- 📈 [Optimization Flow](docs/OPTIMIZATION_FLOW.md) - Performance workflow

### Project Overview
- 📋 [Roadmap](ROADMAP.md) - Project phases and progress
- ✅ [Tasks](TASKS.md) - Todo list
- 📊 [Project Status](PROJECT_STATUS.md) - Complete overview

## ⚙️ Configuration

### Feature Flags
Edit `config.js` to enable/disable features:

```javascript
features: {
    testimonials: false,    // Testimonials section
    contactForm: false,     // Contact form
    calendly: true,         // Booking widget
    clientPortal: false,    // Client file access
    adminCMS: true,         // Admin dashboard
    preview3D: false,       // 3D preview (future)
    analytics: false        // Analytics tracking
}
```

### Quick Setup
1. Update Calendly URL in `config.js`
2. Enable features you want
3. Run `npm run optimize:images`
4. Deploy to Netlify

See [MANUAL_SETUP.md](docs/MANUAL_SETUP.md) for detailed steps.

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

---

> **Built with ❤️ for SkyView Dynamics by nitsuah**
## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md

## Repository Index

### Root Files
- [[repos/skyview/CHANGELOG.md|CHANGELOG.md]]
- [[repos/skyview/FEATURES.md|FEATURES.md]]
- [[repos/skyview/METRICS.md|METRICS.md]]
- [[repos/skyview/ROADMAP.md|ROADMAP.md]]
- [[repos/skyview/TASKS.md|TASKS.md]]