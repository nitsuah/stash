# Skyview Features

**Last Validated:** 2026-09-02

## Core Experiences

- **Immersive Hero Section** — full-screen drone video background with cinematic motion polish and cursor-follow drone accent that hovers offset up-and-right of the pointer, connected by a transparent spotlight beam (`scripts/drone-cursor.js`)
- **Dynamic Gallery** — grid/masonry layout with lazy loading; seasonal filtering, display-order sorting, and active/inactive governance via `assets/gallery.json`
- **Service Packages** — card-based display of offerings (Real Estate, Events, Cinematography, Mapping)
- **Responsive Design** — mobile-first layout using CSS variables, Flexbox, and Grid

## Marketing & Personalization

- **Campaign Personalization** — UTM param + referrer detection applies per-source hero subline variants on page load; data session-persisted (`scripts/campaign.js`)
- **A/B Testing Framework** — deterministic per-visitor bucket assignment for hero headline and CTA experiments; feature-gated in `config.js` (`experiments.enabled`) — ready to enable (`scripts/ab-testing.js`)
- **Conversion Funnel Tracking** — privacy-first event capture across landing → gallery → booking/contact; referrer and campaign metadata captured on landing view

## Funnel Reporting

- **Local Dashboard** — in-browser conversion dashboard with step-by-step drop-off percentages
- **CSV / JSON Export** — `exportMetricsCSV()` and `exportMetricsJSON()` for offline analysis

## Admin & CMS

- **Decap CMS** — git-gateway backend; gallery assets managed without code changes; season, display order, and active status editable in the CMS editor
- **Admin Hardening** — CSP, `X-Robots-Tag: noindex,nofollow`, and `Cache-Control: no-store` enforced on all `/admin/*` routes via `netlify.toml`

## Client Portal

- **Rate Limiting** — 5-attempt / 15-minute lockout enforced client-side via localStorage
- **Time-Bound Token Expiry** — portal detects and rejects expired access codes; clear expiry messaging shown to clients
- **Server-Side Token Validation** — `netlify/functions/api-portal.mjs` verifies access codes via HMAC-SHA256 (`netlify/functions/utils/portal.js`); `PORTAL_SALT` is a mandatory production secret with no fallback, and the endpoint fails closed (denies access) if it's unset
- **Token Generator** — `scripts/portal-token.js` Node.js CLI produces signed `clientId.expiry_unix.hmac` codes with configurable TTL, sharing the same signing implementation as the verification endpoint

## Security & Infrastructure

- **Content Security Policy** — CSP + Permissions-Policy headers on all pages via `netlify.toml`
- **No-Store Routes** — client-portal and gallery pages excluded from CDN caching
- **Modular JavaScript** — ES modules throughout; zero build step required for the marketing site (the marketplace platform SPA at `/app` does have a Vite build, run via `scripts/build.js`)
- **Docker/Netlify Parity** — the Docker preview image (`Dockerfile`) now runs the same `scripts/build.js` build as Netlify, so it serves the marketplace platform SPA at `/app` identically to production instead of only the static marketing pages
- **Docker Validation** — `docker compose -f config/docker-compose.yml run --rm unit` runs the Vitest suite with coverage; web smoke build confirms zero import errors. See METRICS.md for the current test count.
- **Netlify Forms** — zero-config contact form handling

## Planned

- **Client Delivery File Backend** — `client-gallery.html` still serves a client-side prototype file listing; the login gate (above) is server-verified, but re-verifying the code and serving a real signed file manifest is a separate P2 workstream (see TASKS.md)
- **Marketplace Platform Activation (Calendly Cutover)** — the platform SPA and frontend swap logic are shipped; production activation (DB migration, Stripe/Resend env vars, flipping `features.platform`) is an operational step, not a code change — see ROADMAP.md
- **Multi-Segment Personalization** — expand campaign variants to cover service spotlight targeting (Q4 2026)
- **Live A/B Experiments** — enable framework already shipped; wire to analytics and analyse results (Q4 2026)
