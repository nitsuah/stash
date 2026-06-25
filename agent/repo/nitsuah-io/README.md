
# Nitsuah.io — Personal Portfolio

---
**Last Updated:** 2026-04-13
---

A fast, modern Next.js + TypeScript personal website showcasing selected projects, Web3 experiments, and professional work.

**TL;DR:** Austin J. Hardy's portfolio site built with Next.js, featuring curated projects, Web3 integrations, and clean design for hiring managers and collaborators to review work and demos.

---

## Quick Links

- **Live Site:** [nitsuah.io](https://nitsuah.io)
- **GitHub:** [@nitsuah](https://github.com/nitsuah)
- **Author:** Austin J. Hardy — Developer & Researcher

---

## What This Repo Contains

- **Next.js 16** + TypeScript site with modern React components
- **Web3 Integration:** wagmi + ConnectKit for crypto/blockchain features
- **Interactive Elements:** Spline 3D scenes and animations
- **Labs Section:** Experimental Web3 tools (domains, minting, staking)
- **Project Showcase:** Curated list of selected work with live demos

---

## Selected Projects

This site highlights key projects demonstrating different technical skills:

### **Kryptos** — Cryptanalysis Research Toolkit

Advanced Python cryptography and algorithm research

- **Repository:** [github.com/nitsuah/kryptos](https://github.com/nitsuah/kryptos)
- **What to Look At:** Research-grade cipher solving pipelines, comprehensive test suites, scoring heuristics
- **Tech Stack:** Python, cryptographic algorithms, data analysis

### **GCP Tools** — Google Cloud Platform Automation

Enterprise-grade Google Drive API automation and reporting

- **Repository:** [github.com/nitsuah/gcp](https://github.com/nitsuah/gcp)
- **What to Look At:** CLI-style scripts, security configs, migration helpers
- **Tech Stack:** Python, Google APIs, enterprise automation

### **Stash** — System Administration Toolkit

Collection of practical IT automation and enterprise tools

- **Repository:** [github.com/nitsuah/stash](https://github.com/nitsuah/stash)
- **What to Look At:** PowerShell scripts, VBA automation, Atlassian integrations
- **Tech Stack:** PowerShell, VBA, DevOps tooling

---


## What’s New

- See [CHANGELOG.md](CHANGELOG.md) for recent updates and version history

## User Feedback & Testimonials

- “The best developer portfolio I’ve seen — clean, fast, and interactive!”
- “Love the Web3 demos and the project showcase.”
- [Submit your feedback](https://github.com/Nitsuah-Labs/nitsuah-io/issues/new?template=feedback.md)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Please:
- Fork the repo and create a feature branch
- Add or improve tests for new features
- Run all tests and ensure coverage does not decrease
- Open a pull request with a clear description and screenshots if UI changes

---

## Run Locally (3 Steps)

Requires Node.js 22+

```bash
# 1. Install dependencies
npm ci

# 2. Start development server
npm run dev

# 3. Open http://localhost:3000
```

### Build & Preview Production

```bash
npm run build
npm run start   # Preview production build
```

Note: Uses wagmi CLI to generate Web3 hooks on build

---

## Tech Stack & Features

- **Framework:** Next.js 16 with App Router
- **Language:** TypeScript
- **Web3:** wagmi, viem, ConnectKit
- **UI:** Material-UI, Emotion, custom CSS
- **3D Graphics:** Spline Runtime
- **Testing:** Jest (unit), Playwright (E2E/a11y)
- **Deployment:** Netlify with automatic deployments
- **CI:** GitHub Actions (build, typecheck, lint, tests)

### Web3 Features

- Wallet connection and network switching
- NFT minting and domain registration
- Smart contract interactions
- Multi-chain support

### Testing & Quality

- **Unit Tests:** Jest + React Testing Library
- **Playwright Coverage:** Smoke, browser flows, and critical accessibility checks
- **Docker-First Validation:** Run Playwright in Docker for CI-consistent verification
- **CI Model:** Fast required CI + nightly/manual browser-heavy Playwright

```bash
# Quick local checks
npm test
npm run test:smoke
npm run test:a11y:quick

# Recommended before pushing (Docker-first)
npm run precheck:docker

# Manual Docker flow
npm run test:e2e:docker:build
npm run test:e2e:docker
```

---

## Project Structure

```text
src/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Homepage with project showcase
│   ├── about/             # About page
│   ├── projects/          # Project details and blogs
│   ├── labs/              # Web3 experiments
│   └── _components/       # Reusable components
├── generated.ts           # Auto-generated wagmi hooks
└── wagmi.ts              # Web3 configuration
```

---

## Content Management

### Adding/Updating Projects

1. Edit project data in `src/lib/data/projects.ts` (or create if needed)
2. Update the project showcase component
3. Add project assets to `public/assets/`
4. Commit changes - CI will handle the rest

### Web3 Contract Updates

1. Update contract ABIs in `src/app/_components/_labs/_utils/`
2. Run `npm run wagmi` to regenerate hooks
3. Update contract addresses in relevant components

---

## Deployment & CI

### Automatic Deployments

- **Production:** Commits to `main` → [nitsuah.io](https://nitsuah.io)
- **Staging:** Commits to `dev` → [dev.nitsuah.io](https://dev.nitsuah.io)
- **Status:** [![Netlify Status](https://api.netlify.com/api/v1/badges/82ca203b-6c2a-4b49-b60a-ab80cf2a6c5c/deploy-status?branch=main)](https://app.netlify.com/sites/nitsuah-io/deploys)

### GitHub Actions CI

- ✅ Build verification
- ✅ TypeScript checking
- ✅ ESLint validation
- ✅ wagmi hook generation

---

## Performance & Accessibility

- **Lighthouse Score:** 90+ (Performance, Accessibility, SEO)
- **Image Optimization:** Next.js Image component with Sharp
- **SEO:** Complete meta tags and Open Graph support
- **Responsive:** Mobile-first design
- **Loading:** Optimized with proper code splitting

---

## Development Notes

### Key Commands

```bash
npm run dev        # Development server
npm run build      # Production build
npm run start      # Preview production
npm run lint       # ESLint check
npm run wagmi      # Generate Web3 hooks
```

### Environment Setup

- Node.js 22+ required
- Uses wagmi CLI for smart contract integration
- Spline scenes loaded from external CDN

---

## Contact & Credits

- **Austin J. Hardy**

- Portfolio: [nitsuah.io](https://nitsuah.io)
- GitHub: [@nitsuah](https://github.com/nitsuah)
- Organization: [Nitsuah Labs](https://github.com/Nitsuah-Labs)

Built with modern web technologies and a focus on performance, accessibility, and clean code architecture.

<!--
AGENT INSTRUCTIONS:
This file is the face of the project.
1. Analyze the codebase to understand its purpose, tech stack, and setup requirements.
2. Update the "Project Name" and "Description".
3. Fill in the "Getting Started", "Installation", and "Usage" sections with accurate commands.
4. Keep the tone professional and helpful.
-->
## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md
