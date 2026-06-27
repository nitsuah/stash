---
name: agent-board-overview
description: Central synthesis document for the Agent Board application.
metadata:
  type: project
---

# Agent Board Overview

Agent Board is a local-first control room designed for managing multi-model AI workflows securely on your own machine. It functions as a cockpit for developers to build, run, and evaluate AI agents.

## Core Pillars

- **Safety Rails**: Built-in input classification, prompt-injection checks, and output sanitization via [[repos/darkmoon/docs/API.md|NemoClaw]] integration.
- **Experience-Aware Sessions**: Persistent sessions with context, role metadata, and message history, tailored to different experience modes (e.g., Research, Developer).
- **Live Observability**: Real-time observability using [[repos/agent-board/METRICS.md|Metrics]] dashboards, WebSocket streaming, and OpenTelemetry traces (with Jaeger).

## Key Capabilities

- **Local-First Execution**: Orchestrates models locally via Docker (Ollama, Docker Model Runner).
- **Model Routing**: Server-enforced endpoint restrictions and experience-based model switching.
- **Service Orchestration**: Manages stack services, model pulls, and container lifecycle.

## Related Resources

- **Source Code**: [[repos/agent-board/README.md|Agent Board README]]
- **Architecture**: [[repos/agent-board/docs/ARCHITECTURE.md|System Architecture]]
- **Roadmap**: [[repos/agent-board/ROADMAP.md|Roadmap and Future Goals]]
- **Safety Strategy**: [[repos/agent-board/docs/AI_STACK_STRATEGY.md|AI Stack Strategy]]
