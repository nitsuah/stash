
# Tasks

**Last Updated:** 2026-06-03

> **Delivery split:** public FE covers the marketing site and funnel. `/admin` is a separate CMS surface. Secure client portal/download auth is a separate backend workstream.

## In Progress

- [ ] Complete the launch checklist with verified production identity data.
  - Priority: P1
  - Blocker: client-approved phone, email, location, and social/schema values still pending — fields are centralized in `config.js` and ready to receive them.
  - Acceptance Criteria: production identity fields populated, `/admin` invite-only, separation documented.

## Todo

- [ ] Build secure client delivery backend.
  - Priority: P2
  - Context: portal has client-side rate limiting and time-bound token expiry (`client-portal.html`, `scripts/portal-token.js`). Backend signed-link delivery needs a separate service layer.
  - Acceptance Criteria: Netlify Function or edge middleware validates tokens server-side using `PORTAL_SALT` secret; time-bound access links and/or signed downloads; notification flow.
