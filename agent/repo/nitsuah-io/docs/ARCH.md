# Project Architecture

This document provides a comprehensive overview of the `nitsuah-io` project architecture, including the technology stack, project structure, and key components.

## Technology Stack

- **Framework:** [Next.js](https://nextjs.org/) 16 (App Router)
- **Language:** [TypeScript](https://www.typescriptlang.org/)
- **Web3:**
  - [wagmi](https://wagmi.sh/) v2
  - [viem](https://viem.sh/) v2
  - [@tanstack/react-query](https://tanstack.com/query/v4/docs/react/overview)
- **UI:**
  - [React](https://reactjs.org/) 18
  - [Material-UI](https://mui.com/)
  - [Emotion](https://emotion.sh/)
- **3D Graphics:** [@splinetool/react-spline](https://github.com/splinetool/spline-react)
- **Linting & Formatting:**
  - [ESLint](https://eslint.org/)
  - [Prettier](https://prettier.io/)
- **Testing:**
  - [Jest](https://jestjs.io/)
  - [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- **Deployment:** [Netlify](https://www.netlify.com/)
- **CI/CD:** [GitHub Actions](https://github.com/features/actions)

## Project Structure

The project is organized into the following key directories:

- **`config/`**: Centralized configuration files for Jest, ESLint, Prettier, and wagmi.
- **`docs/`**: Project documentation, including this file and `CONTRIBUTING.md`.
- **`public/`**: Static assets, including images, fonts, and JSON data.
- **`src/`**: The main application source code.
  - **`app/`**: The Next.js App Router, containing all pages and components.
    - **`_components/`**: Shared React components.
      - **`_labs/`**: Components specific to the "Labs" section.
      - **`_site/`**: Components for the main site layout (header, footer, etc.).
      - **`_spline/`**: Spline 3D scene components.
      - **`_styles/`**: Global and component-specific CSS files.
      - **`_web3/`**: Web3-related components (wallet connection, network switching, etc.).
    - **`[page]/`**: Individual pages for the site.
  - **`generated.ts`**: Auto-generated wagmi hooks.
  - **`wagmi.ts`**: wagmi configuration.

## Key Components & Systems

### Theme System

The application features a complete dark/light mode theme system with user preference persistence.

**Architecture:**
- **Context Provider:** `src/contexts/ThemeContext.tsx` provides global theme state using React Context API
- **Theme Storage:** User preference persisted in `localStorage` with key `"nitsuah-theme"`
- **Default Theme:** Dark mode by default
- **CSS Custom Properties:** `src/styles/theme.css` defines comprehensive design tokens for both themes
- **SSR Safety:** Mounted state check prevents hydration mismatch

**Theme Tokens:**
```css
/* Colors */
--color-background, --color-surface, --color-surface-elevated
--color-border, --color-border-hover
--color-text-primary, --color-text-secondary, --color-text-tertiary
--color-accent, --color-accent-hover
--color-success, --color-warning, --color-error

/* Shadows */
--shadow-sm, --shadow-md, --shadow-lg

/* Transitions */
--transition-fast (150ms), --transition-normal (300ms), --transition-slow (500ms)
```

**Provider Hierarchy:**
```
ThemeProvider
  └─ WagmiProvider
      └─ QueryClientProvider
          └─ ToastProvider
              └─ Application Components
```

### Styling Architecture

The project uses a hybrid styling approach combining global CSS, CSS Modules, and CSS Custom Properties.

**CSS Modules Strategy:**
- Component-specific styles in `.module.css` files colocated with components
- Scoped class names prevent style conflicts
- All demo components (`DemoButton`, `DemoCard`, `DemoTable`) use CSS modules
- Site components (`Footer`, `Search`, `Connect`) migrated to CSS modules
- Theme tokens integrated via CSS custom properties

**Benefits:**
- Zero inline styles (maintainability ✅)
- Proper separation of concerns
- CSS hover states instead of JavaScript handlers
- Theme-aware via custom properties
- Type-safe class names in TypeScript

### Web3 Integration

The Web3 functionality is built around the `wagmi` and `viem` libraries.

- **`src/wagmi.ts`**: This file configures the wagmi client, defining the supported chains, connectors, and transports.
- **`src/app/providers.tsx`**: This component wraps the application in the necessary `WagmiProvider` and `QueryClientProvider`, making the wagmi hooks available throughout the app.
- **`src/app/_components/_web3/`**: This directory contains the core Web3 UI components, such as `Connect`, `Account`, `NetworkSwitcher`, and `MintNFT`. The `Connect` component features wallet logos, loading spinners, and install prompts for better UX.
- **`src/app/_components/_web3/_assets/wallets/`**: SVG wallet icons for MetaMask, Coinbase Wallet, WalletConnect, Safe, and Injected connectors.
- **`src/app/profile/`**: Full wallet dashboard displaying connected address, ENS name, balance, network, and account management.
- **`src/app/labs/`**: The "Labs" pages (`domains`, `register`, `mint`, etc.) demonstrate complex smart contract interactions using wagmi hooks with custom ABIs.

### Configuration

All major configuration files have been centralized in the `config/` directory to keep the project root clean. The `package.json` scripts have been updated to reference these new paths.

### CI/CD

The project uses GitHub Actions for continuous integration. The workflow is defined in `.github/workflows/ci.yml` and includes the following steps:

1. **Checkout:** Checks out the code.
2. **Setup Node:** Sets up the specified Node.js version.
3. **Install Dependencies:** Installs the project dependencies.
4. **Lint:** Runs ESLint to check for code quality issues.
5. **Typecheck:** Runs the TypeScript compiler to check for type errors.
6. **Build:** Builds the Next.js application.

### Deployment

The site is deployed to Netlify. The `netlify.toml` file in the project root configures the build settings, including the build command, publish directory, and environment variables.

## Testing Strategy

### Unit Testing (Jest + React Testing Library)

**Coverage:** 98% statements | 81% branches | 82% functions  
**Test Count:** 213 tests across 16 suites

```bash
npm test                    # Run all unit tests
npm test -- --coverage      # Generate coverage report
npm test -- --watch         # Watch mode for development
```

**Test Suites:**

- **Utilities:** URL manipulation, validation functions, sanitization
- **Hooks:** Custom hooks like `useHoverStyle`
- **Components:** Demo, restaurant, resume, Web3, and site components

**Testing Philosophy:**
- Comprehensive edge case coverage
- Real-world scenario testing  
- Accessibility validation (ARIA labels, semantic HTML)
- Mock external dependencies (wagmi, viem)

### End-to-End Testing (Playwright)

**Test Count:** 59 tests (20 accessibility, 6 visual regression, 33 E2E)

```bash
npm run test:e2e            # All Playwright tests
npm run test:a11y           # Accessibility tests only
npm run test:e2e:ui         # Interactive UI mode
```

**Docker Testing** (CI-consistent environment):

```bash
npm run test:e2e:docker:build    # Build Docker image
npm run test:e2e:docker          # Run tests in Docker
```

**Test Coverage:**
- WCAG 2.1 AA compliance (axe-core)
- Visual regression across devices
- Cross-browser compatibility (Chromium, Firefox, WebKit)
- User interaction flows

### CI/CD Pipeline

**GitHub Actions** runs on every PR:

1. **Lint:** ESLint checks
2. **Typecheck:** TypeScript validation
3. **Unit Tests:** Jest suite (213 tests)
4. **Build:** Next.js production build
5. **E2E Tests:** Playwright suite (59 tests)

**Quality Gates:** All tests pass, no TypeScript errors, no ESLint violations

## Data Flow & State Management

### Client-Side State

**React Context:**

- `ThemeContext` - Global theme state (light/dark mode)
- No Redux/Zustand needed - Context API sufficient for current scale

**React Query:**

- Powered by `@tanstack/react-query`
- Manages Web3 data fetching and caching
- Automatic background refetching
- Optimistic updates for transactions

**Local State:**

- Component-level state via `useState` for UI interactions
- Form state management in contact forms
- Cart state in restaurant demo

### Server-Side Rendering

**Next.js App Router:**

- Server Components by default
- Client Components marked with `"use client"`
- Hydration-safe patterns (theme system uses mounted state)
- Static generation for marketing pages
- Dynamic rendering for Web3 pages

## Component Patterns

### Demo Components

Reusable UI components showcasing different patterns:

**DemoButton** - Button with variants and sizes

- Variants: primary, secondary, success, danger, ghost
- Sizes: small, medium, large
- Disabled state handling
- CSS module styling with theme tokens

**DemoCard** - Card container with hover effects

- Optional hover animations
- Clickable variants
- Theme-aware borders and backgrounds

**DemoTable** - Data table with sorting and interaction

- Generic TypeScript types for type safety
- Custom column rendering
- Hover and striped row variants
- Responsive overflow handling

### Project Demos

**Restaurant** (`src/app/projects/clients/_comp/restaurant/`)

- Menu browsing with categories
- Shopping cart with item management
- Order total calculation
- Responsive grid layout

**Resume** (`src/app/projects/clients/_comp/resume/`)

- Professional resume template
- Contact form with validation
- Experience timeline
- Skills grid with categories

## Performance Optimizations

**Code Splitting:**

- Dynamic imports for heavy components (Spline 3D)
- Route-based code splitting via Next.js App Router
- Lazy loading for below-the-fold content

**Image Optimization:**

- Next.js Image component for automatic optimization
- WebP format with fallbacks
- Responsive images with srcset

**CSS Optimization:**

- CSS modules for automatic code splitting
- Critical CSS inlined by Next.js
- Minification in production builds

**Bundle Size:**

- Tree-shaking enabled
- No moment.js (using native Date APIs)
- Selective imports from lodash/UI libraries

## Security

**Dependency Auditing:**

- Regular `npm audit` checks
- Automated security updates via Dependabot
- Zero high/critical vulnerabilities policy

**Web3 Security:**

- User transaction approval required
- Network mismatch warnings
- Wallet connection state validation
- No private key handling (wallet-managed)

**Content Security:**

- Input sanitization in utility functions
- XSS prevention in validation layer
- SQL injection escaping patterns tested

## Status

**Last Updated:** December 4, 2025

### Production Ready ✅

- Next.js 16 App Router with TypeScript
- wagmi v2 + viem v2 Web3 integration
- Wallet connection (icons, toasts, install prompts)
- Profile page with wallet dashboard
- Jest + Playwright + accessibility tests (98% coverage, 213 tests)
- Dark/light theme system with persistence
- CSS Modules architecture (zero inline styles)
- CI/CD with GitHub Actions + Netlify
- Security hardened (0 moderate/high vulnerabilities)

### Recent Improvements (December 2025)

- ✅ Comprehensive unit test coverage (199 tests)
- ✅ Dark mode theme system with CSS custom properties
- ✅ Migrated all inline styles to CSS modules
- ✅ Cleaned up HTML reports from git history
- ✅ Centralized theme tokens for maintainability
