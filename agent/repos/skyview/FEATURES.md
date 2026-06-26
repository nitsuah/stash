# Skyview Features

**Last Validated:** June 2026

## Core Experiences

- **Immersive Hero Section** — full-screen drone video background with cinematic motion polish and cursor-follow drone accent
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
- **Token Generator** — `scripts/portal-token.js` Node.js CLI produces signed `clientId.expiry_unix.checksum` codes with configurable TTL

## Security & Infrastructure

- **Content Security Policy** — CSP + Permissions-Policy headers on all pages via `netlify.toml`
- **No-Store Routes** — client-portal and gallery pages excluded from CDN caching
- **Modular JavaScript** — ES modules throughout; zero build step required
- **Docker Validation** — `docker compose run --rm unit` runs 90 unit tests; web smoke build confirms zero import errors
- **Netlify Forms** — zero-config contact form handling

## Planned

- **Secure Client Delivery Backend** — Netlify Function or edge middleware for server-side portal token validation; signed time-bound download links (`PORTAL_SALT` secret required)
- **Multi-Segment Personalization** — expand campaign variants to cover service spotlight targeting (Q4 2026)
- **Live A/B Experiments** — enable framework already shipped; wire to analytics and analyse results (Q4 2026)
