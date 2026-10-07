---
name: motor-pool-overview
description: Central synthesis document for the motor-pool application.
metadata:
  type: project
kind: overview
repo: agent-board
---

# motor-pool Overview

motor-pool is a local-first control room designed for managing multi-model AI workflows securely on your own machine. It functions as a cockpit for developers to build, run, and evaluate AI agents.

## Core Pillars

- **Safety Rails**: Built-in input classification, prompt-injection checks, and output sanitization via the [[repos/agent-board/docs/API.md|agent-board API]].
- **Experience-Aware Sessions**: Persistent sessions with context, role metadata, and message history, tailored to different experience modes (e.g., Research, Developer).
- **Live Observability**: Real-time observability using Metrics dashboards, WebSocket streaming, and OpenTelemetry traces (with Jaeger).

## Key Capabilities

- **Local-First Execution**: Orchestrates models locally via Docker (Ollama, Docker Model Runner).
- **Model Routing**: Server-enforced endpoint restrictions and experience-based model switching.
- **Service Orchestration**: Manages stack services, model pulls, and container lifecycle.

## Related Resources

- **Source Code**: motor-pool README
- **Architecture**: System Architecture
- **Roadmap**: Roadmap and Future Goals
- **Safety Strategy**: [[repos/agent-board/docs/archive/AI_STACK_STRATEGY|AI Stack Strategy]]
