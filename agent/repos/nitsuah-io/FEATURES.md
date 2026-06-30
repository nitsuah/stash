
# Features

---
**Last Updated:** 2026-04-13
---

## Core Capabilities

### 🎨 Portfolio & Showcase

Modern personal portfolio with curated project showcase and professional presentation.

- **Project Gallery**: Featured projects with live demos, GitHub links, and tech stack details
- **Interactive 3D Scenes**: Spline-powered 3D graphics and animations for visual engagement
- **Professional Resume**: Structured CV with downloadable PDF option and contact information
- **About Page**: Personal introduction, skills matrix, and professional background
- **Blog Platform**: Technical writing and project updates with markdown support

### ⛓️ Web3 Integration

Full-stack blockchain features with multi-chain wallet support and smart contract interactions.

- **Wallet Connection**: MetaMask, Coinbase Wallet, WalletConnect, and Safe connector support with branded icons
- **Multi-Chain Support**: Ethereum mainnet, Polygon, Sepolia, and custom network configuration
- **Network Switching**: Auto-detection and user prompts for wrong networks with seamless switching
- **ENS Resolution**: Display ENS names instead of wallet addresses for better UX
- **Smart Contract Interactions**: Direct blockchain transactions with gas estimation and error handling
- **Balance Display**: Real-time ETH balance with automatic formatting and currency conversion
- **Wallet Dashboard**: Full profile page showing address, balance, network, and connection management

### 🧪 Labs Section

Experimental Web3 tools demonstrating blockchain development capabilities.

- **Domain Registration**: ENS-style domain system with on-chain registration and management
- **NFT Minting**: Custom NFT creation with metadata upload and contract deployment
- **Token Staking**: Lock tokens for rewards with APY calculations and withdrawal mechanics
- **DAO Governance**: Voting system with proposal creation and multi-sig execution
- **AI Integration**: On-chain AI model inference with smart contract oracles
- **Domain Lookup**: Query registered domains with ownership verification and transfer history
- **Token Dashboard**: ERC-20 token management with balance tracking and transfer capabilities

### 🎯 User Experience

Polished interface with attention to accessibility, performance, and user feedback.

- **Loading States**: Skeleton screens, spinners, and progress indicators for all async operations
- **Error Handling**: User-friendly error messages with recovery suggestions and retry mechanisms
- **Toast Notifications**: Non-intrusive feedback for wallet actions, transactions, and system events
- **Copy to Clipboard**: One-click address copying with visual confirmation
- **Wallet Install Prompts**: Detect missing wallet extensions and guide users to installation
- **Search Functionality**: Fast project search with fuzzy matching and keyboard navigation
- **Responsive Design**: Mobile-first approach with smooth transitions across all device sizes

### ♿ Accessibility

WCAG 2.1 AA compliance with comprehensive keyboard navigation and screen reader support.

- **Skip Navigation**: Keyboard shortcut to jump to main content on all pages
- **Semantic HTML**: Proper heading hierarchy, landmark regions, and ARIA labels
- **Keyboard Navigation**: Full site navigation without mouse, including modals and dropdowns
- **Screen Reader Support**: Descriptive labels, live regions, and status announcements
- **Color Contrast**: Meets WCAG AA standards for text and interactive elements
- **Focus Management**: Visible focus indicators and logical tab order throughout site
- **Alt Text**: Descriptive image alternatives for all visual content

### 🏠 Landing Page

- **Featured Projects Landing Page**: `LandingHero` + `FeaturedProjects` components replace the Spline hero; top 4 featured projects (motor-pool, overseer, bb-mcp, darkmoon) appear in a 2×2 card grid above the fold.
- **Spline 3D Scene on `/3d` Route**: Spline scene moved from home page to a dedicated opt-in `/3d` page, removing bundle weight from the critical landing path and improving home page LCP.

### 🎨 Dark Mode & Theming

Complete theme system with user preference persistence and comprehensive design tokens.

- **Theme Toggle**: Switch between light and dark modes with smooth transitions
- **LocalStorage Persistence**: User preference saved across sessions
- **CSS Custom Properties**: Comprehensive design tokens for colors, shadows, and transitions
- **SSR-Safe Implementation**: Hydration-safe patterns prevent flash of unstyled content
- **Theme Context**: React Context API for global theme state management

### 🧪 Testing & Quality

Comprehensive test coverage with automated CI/CD and Docker-based testing infrastructure achieving 100% pass rate.

- **Unit Tests**: Jest with React Testing Library for component and utility testing (98% coverage, 213 passing)
- **E2E Tests**: Playwright for visual regression, user flows, and cross-browser compatibility (59 passing)
- **Accessibility Tests**: axe-core integration with automated WCAG 2.1 AA compliance checks (20 passing)
- **Visual Regression**: Screenshot comparison across browsers and viewports with Docker baselines (6 passing)
- **Docker Testing**: Production build strategy ensures CI/local parity with Playwright Docker image
- **Pre-commit Hooks**: Auto-format, typecheck, and unit tests before commit (~3s)
- **CI Pipeline**: GitHub Actions running full test suite, build verification, and deploy previews (100% pass rate)

### ⚡ Performance

Optimized for speed with modern build tools and delivery techniques.

- **Next.js App Router**: Server-side rendering, static generation, and intelligent code splitting
- **Image Optimization**: Automatic WebP/AVIF conversion with responsive sizing via next/image
- **Bundle Analysis**: Tree-shaking and chunk optimization for minimal JavaScript payload
- **CDN Delivery**: Global Netlify CDN with edge caching and HTTP/2 push
- **Lazy Loading**: Component-level code splitting with React.lazy and dynamic imports
- **Build Performance**: Turbopack-powered builds (~35s) with incremental compilation
- **Font Optimization**: Self-hosted fonts with preloading and font-display swap


### 🔧 Developer Experience

Modern development workflow with type safety, code quality tools, and comprehensive documentation.

---

## 🚀 Planned & Upcoming

### 🧠 AI/ML & Market Trends
- **AI Chat Widget**: bb-mcp-powered portfolio Q&A with streaming and persistent toggle
- **On-chain Resume**: EAS verifiable credentials page for wallet-based skill attestations
- **Bento Grid Layout**: 2026 design trend for Projects and Skills
- **Live Cross-Repo Widgets**: Real-time stats from kryptos, skyview analytics, and motor-pool
- **PWA & Offline Support**: Installable, offline-ready portfolio with push notifications
- **Showcase Page**: User-submitted demos and real-world use cases

- **TypeScript**: Full type coverage with strict mode for compile-time error detection
- **ESLint + Prettier**: Automated code formatting and linting with consistent style enforcement
- **Wagmi CLI**: Auto-generated Web3 hooks from contract ABIs with full TypeScript types
- **Path Aliases**: Clean imports with @/ prefix for absolute paths (e.g., @/components)
- **Git Hooks**: Optimized pre-commit/pre-push validation with Husky and lint-staged
- **Environment Config**: Centralized configuration in config/ directory for all build tools
- **Hot Reload**: Fast refresh for React components with state preservation during edits
- **Documentation**: Comprehensive guides (ARCH.md, CONTRIBUTING.md, DEMO_REF.md)

### 🚀 Deployment & CI/CD

Automated deployment pipeline with continuous integration and preview environments.

- **Netlify Hosting**: Automatic deployments on push with instant rollback capability
- **Deploy Previews**: Unique URL for every PR with full production build for review
- **Branch Deploys**: Staging environment on dev branch with production parity
- **GitHub Actions**: Automated testing, linting, type checking, and build verification
- **Environment Variables**: Secure secret management for API keys and configuration
- **Build Optimization**: Cached dependencies and incremental builds for fast deployments
- **Status Badges**: Real-time build and deploy status in README

### 🔒 Security

Proactive security measures with automated vulnerability scanning and best practices.

- **Dependency Audits**: Automated npm audit in CI with zero high/critical vulnerabilities
- **Content Security Policy**: Restrictive CSP headers to prevent XSS and injection attacks
- **HTTPS Enforcement**: All traffic forced to secure connections with HSTS headers
- **Environment Isolation**: Secrets never committed, API keys in environment variables only
- **Rate Limiting**: API route protection with request throttling and abuse prevention
- **Secure Headers**: X-Frame-Options, X-Content-Type-Options, and Referrer-Policy configured
- **Wallet Security**: Client-side signing only, private keys never exposed to server

---

## Planned Capabilities

> Features planned for 2026 Q2–Q4. Not yet shipped. Overseer agents execute against these blocks.

### 🤖 AI Integration (bb-mcp)

Conversational AI layer powered by the bb-mcp sister repo for interactive portfolio engagement.

- **Portfolio Chat Widget**: Floating AI assistant answers visitor questions about projects, skills, and availability
- **Streaming Responses**: Token-by-token streaming with typing indicator for perceived responsiveness
- **Server-Side API Key**: `/api/chat` proxy keeps credentials off the client
- **Context Injection**: System prompt includes project list, skills, and contact info for grounded answers
- **Graceful Degradation**: Widget hides cleanly when bb-mcp is unavailable; no broken UI

### 📊 Analytics (skyview)

Privacy-first event telemetry via the skyview sister repo.

- **Page View Events**: Anonymous page-view stream with path, referrer, and viewport; no PII
- **CTA Click Tracking**: Key conversion events (project demo clicks, resume download, wallet connect)
- **Skyview Dashboard Embed**: Public analytics card surfaced on the portfolio for transparency
- **GDPR-Safe by Default**: No cookies, no fingerprinting, aggregate-only reporting

### 📐 Design System Refresh

Visual and interaction upgrades aligned with 2026 design conventions.

- **Bento Grid Layout**: Asymmetric bento grid for Projects and Skills sections
- **Fluid Typography**: `clamp()`-based type scale with variable font support
- **Micro-Interactions**: Scroll-triggered reveals, hover lift, and crossfade page transitions
- **Glassmorphism Polish**: Refined glass-card treatment on Labs and Crypto pages
- **Dark-First**: Expanded dark mode token set; darkmoon theming engine integration planned for Q4

### 📱 Progressive Web App

Installable, offline-capable experience for mobile visitors.

- **Web App Manifest**: Full `manifest.json` with icons, theme color, and display mode
- **Service Worker**: Cache-first strategy for project data and static assets
- **Offline Fallback**: Graceful offline page with cached project list
- **Install Prompt**: Deferred install banner respecting user dismissal

### 🔗 Cross-Repo Integrations

Connections to sister repos that enrich portfolio content and demonstrations.

- **kryptos Feed**: Live cipher challenge stats surfaced in Labs sidebar (kryptos repo)
- **farm Staking Demo**: Live staking flow in Labs pulling from farm contracts on Amoy
- **motor-pool Showcase**: `/lab/agents` page showing autonomous agent activity log (read-only)
- **darkmoon Tokens**: Shared design token pipeline for consistent cross-repo branding (Q4)

### 🏅 On-Chain Resume

Verifiable professional credentials anchored to a wallet address.

- **EAS Attestations**: Skill and experience attestations via Ethereum Attestation Service on Base
- **`/resume/onchain` Route**: Displays attestations for a configured wallet; graceful fallback
- **Wallet-Gated View**: Optional private attestations visible only to connected wallet owner
- **Export**: One-click share link with attestation proof bundle
