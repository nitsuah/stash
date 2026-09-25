# bb-mcp PMO Runbook

> Reviewed: 2026-09-23

## Overview

Standalone Model Context Protocol server wrapping the Blackboard Learn REST API — TypeScript, HTTP Streamable + stdio transports, 40 tools across student/instructor/admin/parent/webhook-subscription roles, plus grade write-back. OAuth2 PKCE auth, RBAC + FERPA gating, per-role rate limiting, structured audit logging, and Prometheus metrics. Consumed by agent-board and other MCP clients; runs standalone via hardened Docker Compose.

## Current Goals / Roadmap Focus

**2025–2026 Q1: Complete** — foundation (TypeScript MCP server, RBAC, OAuth2, student/instructor tools, CLI, standalone Docker).

**2026 Q2 — Read and Write Workflows: Complete** (PR #109 merged 2026-08-29)
- [x] Student, instructor, admin, and parent tool coverage shipped
- [x] Grade write-back tools (`create_grade_column`, `update_grade`, `delete_grade`, `exempt_grade`, `get_grade_column`)
- [x] MCP provider contract (`GET /manifest`)
- [x] RBAC enforcement, audit logging, PII scrubbing (audit logs + tool outputs), per-role rate limiting, FERPA gate coverage extended to the admin directory surface
- [~] Webhook subscription CRUD shipped; inbound event ingestion not started (2027)
- [x] MCP Inspector stdio validation — passed (2026-09-11): `node dist/index.js --stdio` vs. the official MCP Inspector CLI, 0 errors across all 40 tools (`tools/list`); `tools/call` spot-checked end-to-end against `list_courses`. Repeatable via `npm run inspect` / `make docker-inspect`.
- [ ] JSON schemas for all shipped tool inputs — not done
- [ ] Analytics/Product Owner tools — not started, depends on event pipeline (2027)

**2026 Q3 — Enterprise Follow-On: mostly complete**
- [x] Instructor assignment creation flow (`create_assignment`, one call creates content item + linked grade column)
- [x] Audit logging hardening + local audit trail exposed via `list_audit_logs`
- [x] Blackboard error mapping improved — categorized `BbApiError` with actionable messages (2026-09-10)
- [x] Per-request lifecycle tracing (`src/trace.ts`, 2026-09-10)
- [ ] Webhook-to-SSE bridge — not started, moved to 2027 (subscription CRUD exists; nothing yet receives/fans out inbound webhooks)
- [ ] Tool call batching, event-driven pipeline scaling, vector store integration, stable MCP client SDK — not started, moved to 2027

**2027 (scoped, not started):** webhook-to-SSE bridge, event-driven pipeline / Blackboard activity ingestion, analytics/product-owner tools, vector store integration for semantic search, stable MCP client SDK, tool call batching.

## Open P0/P1 Tasks

None open. TASKS.md's P1 section is empty — all P1 work (API wrapper, OAuth2, RBAC, rate limiting, PII scrubbing, MCP provider contract) shipped.

Notable open P2 items (not P0/P1, listed for context):
- [ ] Bind `caller_identity` to real end-user authentication instead of trusting the client's claim (flagged by CodeRabbit on PR #115; needs a design decision, e.g. requiring a verified SSO/Blackboard identity token)
- [ ] Add JSON schemas for all shipped tool inputs

## Blockers

- `caller_identity` is trusted at face value — `MCP_API_KEY` gates the transport but doesn't verify the claimed `userId`/`role` is truthful; deferred pending a real identity-verification design (see P2 above).
- 1 high + 1 moderate transitive npm vulnerability (`fast-uri` via `@modelcontextprotocol/sdk`→`ajv`; `qs` via `@modelcontextprotocol/sdk`→`express`) with no non-breaking fix available yet; tracked via dependabot.
- Webhook-to-SSE bridge has no inbound receiver yet (subscription CRUD only) — real-time event consumption remains unbuilt, deferred to 2027.

## Recent Changes (Unreleased)

- Admin tools (`list_users`, `get_user`, `list_enrollments`, `create_enrollment`, `update_enrollment`, `delete_enrollment`, `list_audit_logs`)
- Parent tools, guardian-scoped read-only (`get_my_children`, `get_children_courses`, `get_children_grades`, `get_children_upcoming_assignments`, `get_children_announcements`)
- Grade write-back tools plus `create_assignment` (content item + linked grade column in one call)
- Webhook subscription tools (admin-only CRUD against Blackboard's webhook API)
- Tool-output PII scrubbing (`src/output-scrub.ts`) — strips email addresses from every MCP tool response, wired centrally via `withMetrics()`
- Local access-audit trail (`src/auth.ts`) — bounded ring buffer surfaced through `list_audit_logs` as `localAuditTrail`
- FERPA gate extended to `list_users`, `get_user`, `list_enrollments`, `list_audit_logs` (previously role=admin only)
- Per-request lifecycle tracing (`src/trace.ts`) — request ID, latency, upstream call count, error flag
- Blackboard error mapping — categorized `BbApiError` with actionable messages instead of raw Blackboard error bodies
- `.gitattributes` pinning text files to LF (fixed ~6700 false-positive lint errors from CRLF checkouts)

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/bb-mcp/ROADMAP|ROADMAP]] · [[repos/bb-mcp/TASKS|TASKS]] · [[repos/bb-mcp/FEATURES|FEATURES]] · [[repos/bb-mcp/METRICS|METRICS]] · [[repos/bb-mcp/CHANGELOG|CHANGELOG]] · [[repos/bb-mcp/README|README]]

**docs/:** [[repos/bb-mcp/docs/blackboard-learn-mcp-plan|blackboard-learn-mcp-plan]] · [[repos/bb-mcp/docs/blackboard-mcp-full-plan|blackboard-mcp-full-plan]] · [[repos/bb-mcp/docs/HANDOFF-mcp-provider-contract-20260403|HANDOFF: mcp-provider-contract (2026-04-03)]]

<!-- vault-links:start -->
## Vault links

_Generated by `scripts/build-vault-indexes.py`; edits inside this block are overwritten._

- Docs: [[repos/bb-mcp/README|README]] (every doc hangs off its Docs Index)
- Overview: [[projects/KB/bb-mcp-overview|KB overview]]
- Latest LOC report: [[reports/eng-loc-bb-mcp-2026-07-29|2026-07-29]] (older ones chain from it)
<!-- vault-links:end -->
