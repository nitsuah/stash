# Nitsuah.io — Personal Portfolio

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

- **Unit Tests:** Jest with React Testing Library (213 passing)
- **E2E Tests:** Playwright for visual regression and user flows (61 passing)
- **Accessibility:** axe-core integration - WCAG 2.1 AA compliant (20 passing)
- **Docker Testing:** CI-consistent environment with production builds
- **Test Coverage:** 98% statement coverage, 100% test pass rate
- **Test Suites:** 16 unit test suites + comprehensive E2E/accessibility coverage

```bash
# Run tests locally
npm test                  # Unit tests (213 tests)
npm run test:e2e         # E2E tests (61 tests)
npm run test:a11y        # Accessibility tests (20 tests)

# Match CI environment exactly
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
