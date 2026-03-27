# bb-mcp PMO Runbook

MCP server for Blackboard Learn API integration.

## Audit Findings (2026-03-27)

**Foundation Status**: 50% complete
- stdio transport: Refactoring in progress
- API wrapper: Development active
- OAuth2 flow: In progress
- RBAC: Not started (blocks all P1 tools)

**Key Metrics**:
- Test coverage: 0% (no automated tests configured)
- CI: GitHub Actions configured (lint, type check, build pass)
- Foundation: API wrapper + OAuth2 required before MCP integration complete

**Shipped Features**: None (MCP integration not complete)

## Priority Structure

**In Progress** (Foundation):
- Stdio transport refactor (blocks everything)
- API wrapper development (core blocker)

**P1** (First tools batch):
- list_courses tool
- get_course_contents tool  
- OAuth2 flow implementation
- JSON schema validation

**P2** (Middleware):
- RBAC middleware (requires P1 auth)
- get_announcements tool
- Assignment submission support
- HTTP error mapping

**P3** (Advanced):
- User search integration
- Audit logging
- Read/write workflow support

## Blocker Assessment

| Blocker | Impact | Mitigation | ETA |
|---------|--------|-----------|-----|
| API wrapper incomplete | Cannot ship any tools | Complete by April 1 | Q1 2026 |
| OAuth2 token handling | Auth not available | Scheduled for P1 | Q1 2026 |
| Transport refactor | CI/CD integration delayed | In progress | March 2026 |
| RBAC design missing | Cannot gate tool access | Design phase starts after OAuth2 | Q2 2026 |

## Roadmap Reset (2026-03-27)

- **2025 Q1** ?? Partial: Setup + API wrapper 50% complete
- **2025 Q2** ?? Not started (blocked on P1 auth)
- **2026 Q1** ?? Critical path: API wrapper ? OAuth2 ? MCP compliance ? first 4 tools
- **2026 Q2** ?? RBAC infrastructure
- **2026 Q3+** ?? Advanced workflows

## Recommendations

1. **Immediate**: Complete API wrapper (foundation blocker)
2. **Next**: Ship OAuth2 + list/get_course_contents to unblock other tools
3. **Then**: Implement RBAC before enabling write operations
4. **Finally**: Build advanced read/write workflows

See bb-mcp TASKS.md and ROADMAP.md for full details.
