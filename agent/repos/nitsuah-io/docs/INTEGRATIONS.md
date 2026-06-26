# Integrations

**Last Updated:** 2026-04-03

Maps the connection points between `nitsuah-io` and each sister repo in the Nitsuah-Labs ecosystem.
Overseer agents use this file to know which repos to pull context from when executing portfolio tasks.

---

## Active Integrations

*(None shipped yet — this file tracks planned and in-progress connections.)*

---

## Planned Integrations

### bb-mcp — AI Chat Backend

| Field            | Value                                                       |
| ---------------- | ----------------------------------------------------------- |
| Status           | Planned (Q2 2026)                                           |
| Direction        | nitsuah-io → bb-mcp                                         |
| Entry Point      | `/api/chat` server route in nitsuah-io                      |
| Auth Model       | Server-side API key (env var `BB_MCP_API_KEY`); never client-exposed |
| Data Contract    | JSON `{ role, content }` messages; streaming SSE response   |
| Update Cadence   | Per visitor request                                         |
| Task Ref         | TASKS.md P1 "Add AI chat widget via bb-mcp"                 |

### kryptos — Cipher Challenge Stats

| Field            | Value                                                       |
| ---------------- | ----------------------------------------------------------- |
| Status           | Planned (Q2 2026)                                           |
| Direction        | kryptos → nitsuah-io                                        |
| Entry Point      | Labs sidebar widget on `/lab` pages                         |
| Auth Model       | Public read; no auth required                               |
| Data Contract    | Static JSON artifact or REST endpoint: `{ challenge, solves, lastUpdated }` |
| Update Cadence   | On kryptos CI build (artifact) or polling (REST)            |
| Task Ref         | TASKS.md P2 "Live kryptos feed widget"                      |

### skyview — Privacy-First Analytics

| Field            | Value                                                       |
| ---------------- | ----------------------------------------------------------- |
| Status           | Planned (Q2 2026)                                           |
| Direction        | nitsuah-io → skyview                                        |
| Entry Point      | Client-side event emitter imported from `lib/analytics.ts`  |
| Auth Model       | Write-only ingest key (env var `SKYVIEW_INGEST_KEY`)        |
| Data Contract    | `{ event, path, ts }` — no PII, no cookies                 |
| Update Cadence   | Per page view / CTA click                                   |
| Task Ref         | TASKS.md P2 "Wire skyview analytics"                        |

### agent-board — Agent Activity Showcase

| Field            | Value                                                       |
| ---------------- | ----------------------------------------------------------- |
| Status           | Planned (Q3 2026)                                           |
| Direction        | agent-board → nitsuah-io                                    |
| Entry Point      | `/lab/agents` page (read-only activity feed)                |
| Auth Model       | Public read endpoint or signed read token                   |
| Data Contract    | SSE or polling: `{ agentId, action, status, ts }[]`         |
| Update Cadence   | Near-real-time (SSE preferred)                              |
| Task Ref         | TASKS.md P3 "Agent-board showcase section"                  |

### farm — Staking Demo

| Field            | Value                                                       |
| ---------------- | ----------------------------------------------------------- |
| Status           | Planned (Q3 2026)                                           |
| Direction        | farm contracts → nitsuah-io Labs                            |
| Entry Point      | `/lab/staking` page                                         |
| Auth Model       | On-chain; connected wallet signs transactions               |
| Data Contract    | wagmi hooks against farm contract ABIs on Amoy testnet      |
| Update Cadence   | Per block / wallet interaction                              |
| Task Ref         | TASKS.md P3 "Farm staking demo integration"                 |

### darkmoon — Design Token Pipeline

| Field            | Value                                                       |
| ---------------- | ----------------------------------------------------------- |
| Status           | Planned (Q4 2026)                                           |
| Direction        | darkmoon → nitsuah-io                                       |
| Entry Point      | `src/styles/theme.css` design token source                  |
| Auth Model       | None; tokens published as npm package or static artifact    |
| Data Contract    | CSS custom property export (`--color-*`, `--spacing-*`, etc.) |
| Update Cadence   | On darkmoon release; semver-pinned                          |
| Task Ref         | ROADMAP.md Q4 "darkmoon theming engine"                     |

---

## Deprioritized (No 2026 Integration Planned)

| Repo  | Reason                                                                 |
| ----- | ---------------------------------------------------------------------- |
| gcp   | GCP tooling is enterprise-internal; no public portfolio integration value |
| stash | Needs sanitization before any public reference; deprioritized until clean |
| osrs  | Separate product domain; portfolio link only (no data integration)     |

---

<!-- AGENT INSTRUCTIONS:
1. Keep one table per integration.
2. Status values: "Active", "Planned (Qx YYYY)", "Deprioritized".
3. Auth Model must explicitly state whether keys are server-side or client-side.
4. Task Ref must link to the canonical TASKS.md or ROADMAP.md entry.
5. Move integrations from Planned → Active when the feature ships and tests pass.
-->
