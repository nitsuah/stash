# motor-pool

> Reviewed: 2026-06-25

## Overview

Local-first AI ops cockpit — chat surface, safety rails, and live observability for multi-model workflows running in Docker. React + Express dashboard with Ollama backend, WebSocket streaming, OpenTelemetry/Jaeger tracing, and opt-in MCP tool servers.

## Current Goals / Roadmap Focus

**Q2 2026 (active):**
- Persistence for agent history, logs, state snapshots
- Agent command interface (start/stop/restart)
- Heartbeat + resource monitoring
- Conversation replay mode (step-through debugging)
- Validated production deployment path (P2)

**Q3 2026 (planned):**
- Multi-tenancy / RBAC planning
- Named pub/sub event channels for reactive multi-agent pipelines
- Plugin architecture for task extensions
- BYOK external LLM integration (Claude, Gemini, etc.)
- MCP container manager (spin tool containers on demand)
- tmux multi-agent worktrees
- 3D Memory Palace context (Neo4j + Graphiti + WebGL)

**Q1 2027 critical path:** Docker optimization + GPU → service lifecycle → plugin arch + BYOK → MCP container manager

**2027 Q2:** Blackboard / bb-mcp frontend layer (streaming UI, persona selector, demo mode)

## Open P0/P1 Tasks

- [ ] **P2** GPU-oriented model portfolio after CUDA enabled
- [ ] **P2** Document model lifecycle and resource management APIs
- [ ] **P2** Document production deployment path
- [ ] **P2** MCP container manager (Playwright, Jira/Confluence, bb-mcp on demand)
- [ ] **P2** bb-mcp streaming UI (SSE, typing indicator)
- [ ] **P2** Multi-persona Blackboard agent selector
- [ ] **P2** Blackboard agent demo mode
- [ ] **P2** Replace Docker socket mount in content-gen with MPT sidecar (security issue)
- [ ] **P2** Expand test coverage to ≥20 tests for core agent flows
- [ ] **P1 PERFORMANCE** Setup turbovec to decrease LLM memory usage (follow-up)

Completed P1: Docker optimization pass (minimal stack = agent-db + ollama + dashboard; nemoclaw/jaeger gated); API docs rewrite.

## Blockers

- NemoClaw sandbox container crash-loops on Windows (CRLF in entrypoint; P3/deferred)
- OpenLLM CPU-incompatible with local workflow (P3/deferred; `OPENLLM_ENABLED=false`)
- Content-gen mounts Docker socket (security risk; P2 — MPT sidecar replacement pending)
- Event bus cross-agent behavior unproven (P3)

## Recent Changes (Unreleased)

- Device profile system (minimal/laptop/desktop) auto-selects Ollama model by RAM/VRAM
- Custom LLM endpoint registry (`CUSTOM_LLM_ENDPOINTS`) — add OpenRouter, vLLM, LM Studio etc. via `.env`
- NVIDIA GPU compose overlay (`config/docker-compose.gpu.yml`)
- Hardware detection script (`scripts/detect-profile.ps1`)
- Workspace file I/O: `/api/workspace/*` routes with git commit/push, path-traversal sandbox, file browser in System panel
- Ollama warmup service (opt-in `warmup` profile)
- OpenLLM endpoint (gated, deferred)
