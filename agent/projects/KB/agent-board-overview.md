---
name: motor-pool-overview
description: Central synthesis document for the motor-pool application.
metadata:
  type: project
---

# motor-pool Overview

motor-pool is a local-first control room designed for managing multi-model AI workflows securely on your own machine. It functions as a cockpit for developers to build, run, and evaluate AI agents.

## Core Pillars

- **Safety Rails**: Built-in input classification, prompt-injection checks, and output sanitization via [[repos/darkmoon/docs/API.md|NemoClaw]] integration.
- **Experience-Aware Sessions**: Persistent sessions with context, role metadata, and message history, tailored to different experience modes (e.g., Research, Developer).
- **Live Observability**: Real-time observability using [[repos/motor-pool/METRICS.md|Metrics]] dashboards, WebSocket streaming, and OpenTelemetry traces (with Jaeger).

## Key Capabilities

- **Local-First Execution**: Orchestrates models locally via Docker (Ollama, Docker Model Runner).
- **Model Routing**: Server-enforced endpoint restrictions and experience-based model switching.
- **Service Orchestration**: Manages stack services, model pulls, and container lifecycle.

## Related Resources

- **Source Code**: [[repos/motor-pool/README.md|motor-pool README]]
- **Architecture**: [[repos/motor-pool/docs/ARCHITECTURE.md|System Architecture]]
- **Roadmap**: [[repos/motor-pool/ROADMAP.md|Roadmap and Future Goals]]
- **Safety Strategy**: [[repos/motor-pool/docs/AI_STACK_STRATEGY.md|AI Stack Strategy]]
