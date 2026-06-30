---
name: bb-mcp-overview
description: Central synthesis document for the Blackboard Learn MCP Server.
metadata:
  type: project
---

# Blackboard Learn MCP Server (Bb-MCP)

Bb-MCP is a standalone [Model Context Protocol](https://modelcontextprotocol.io) server that wraps the Blackboard Learn REST API, enabling structured access to courses, grades, assignments, and announcements for any MCP-compatible client.

## Core Pillars

- **Client-Agnostic Integration**: Moves integration logic out of clients (`motor-pool`, Claude Desktop, Cursor) and into a centralized, reusable server.
- **Security & Compliance**:
    - **OAuth2**: Supports Authorization Code and Client Credentials flows.
    - **Role-Based Access Control**: Strict role gating (Student vs. Instructor).
    - **FERPA Compliance**: Tools accessing protected student data require explicit authorization.
- **Auditability**: Every tool call is logged as structured JSON to stdout, tracking user identity, role, and access status.

## Key Capabilities

- **Student Tools**: `get_my_courses`, `get_upcoming_assignments`, `get_my_grades`, `get_assignment_feedback`, `create_assignment_submission`, etc.
- **Instructor Tools**: `list_roster`, `get_grades`, `get_at_risk_students`, `draft_announcement`, etc.
- **Observability**: Prometheus metrics (`/metrics`) for tool usage, error rates, and duration.

## Integration

- Used within the [[KB/motor-pool-overview|motor-pool]] stack via the connector configuration in `config/connectors.json`.
- Can be run standalone or within the `motor-pool` Docker stack.

## Related Resources

- **Source Code**: [[repos/bb-mcp/README.md|Bb-MCP README]]
- **Metrics/Health**: [[repos/bb-mcp/METRICS.md|Metrics Overview]]
- **Roadmap**: [[repos/bb-mcp/ROADMAP.md|Roadmap and Future Goals]]
