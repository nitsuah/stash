---
name: motor-pool-overview
description: Central synthesis document for the motor-pool application.
metadata:
  type: project
kind: overview
repo: motor-pool
---

# motor-pool Overview

motor-pool is a local-first control room designed for managing multi-model AI workflows securely on your own machine. It functions as a cockpit for developers to build, run, and evaluate AI agents.

## Core Pillars

- **Safety Rails**: Built-in input classification, prompt-injection checks, and output sanitization via the [[repos/motor-pool/docs/API.md|motor-pool API]].
- **Experience-Aware Sessions**: Persistent sessions with context, role metadata, and message history, tailored to different experience modes (e.g., Research, Developer).
- **Live Observability**: Real-time observability using Metrics dashboards, WebSocket streaming, and OpenTelemetry traces (with Jaeger).

## Key Capabilities

- **Local-First Execution**: Orchestrates models locally via Docker (Ollama, Docker Model Runner).
- **Model Routing**: Server-enforced endpoint restrictions and experience-based model switching.
- **Service Orchestration**: Manages stack services, model pulls, and container lifecycle.

## TIRE-kick setup (2026-10-28)

- Obsidian is connected to Codex through its MCP server; the vault contains a sanitized resume prompt and project status.
- Windows Docker Desktop is running Ollama CPU-only. Warm model probes measured about 18.7 tokens/s on `llama3.2:3b` and 8.8 tokens/s on `llama3.1:8b-instruct-q4_K_M`. With both models resident, memory was 12.35 GiB / 15.52 GiB. GPU/runtime detection and cross-vendor acceleration remain tracked in [motor-pool issue #117](https://github.com/nitsuah/motor-pool/issues/117).
- Tool-enabled streaming in PR #118 improved measured median first-token latency by 59.8% (Developer), 62.6% (Research), and 45.6% (Website), using three local CPU Ollama pairs per experience. Details and total loop times are in `docs/METRICS.md`; [issue #116](https://github.com/nitsuah/motor-pool/issues/116) tracks the remaining browser startup baseline and bundle-splitting decision.
- Latest pushed commit is `290ab95` on `feature/ollama-connector`; the fresh isolated Compose suite passed 70/70, root lint had 0 errors / 75 warnings, and the dashboard production image built. Vite warns that the single JS chunk is 934.07 KB minified (249.11 KB gzipped).
- All five CodeRabbit review threads are resolved and CI passes at `290ab95`, but PR #118 still carries an earlier `CHANGES_REQUESTED` decision. Do not merge until required review conditions are clear.
- 9router remains owner-configured. Validate its endpoint only after the owner says setup is ready. Keep credentials and private transcripts out of this mirrored vault.

Resume context: [[projects/KB/motor-pool-tire-kick-resume-prompt]]

## Related Resources

- **Source Code**: motor-pool README
- **Architecture**: System Architecture
- **Roadmap**: Roadmap and Future Goals
- **Safety Strategy**: [[repos/motor-pool/docs/archive/AI_STACK_STRATEGY|AI Stack Strategy]]
