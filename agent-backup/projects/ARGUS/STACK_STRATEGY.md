# AI Stack Strategy
> Local orchestration architecture for motor-pool, Kryptos, and personal automation

**Last updated:** June 2026  
**Author:** nitsuah  
**Status:** Working doc — evolving with motor-pool Q2/Q3 roadmap
[[ARGUS-PLAN]]
---
repo: [[Odysseus]]  
## TL;DR

**motor-pool is the local orchestrator.** Everything else is either a service it wraps, a tool it registers, or a parallel consumer of the same local LLM endpoints. Claude Code, Kryptos, and personal tools can all reach local models directly — motor-pool just happens to be the UI and lifecycle manager for them.

```
┌─────────────────────────────────────────────────────────────┐
│                       YOU (human)                           │
├──────────────┬──────────────────┬───────────────────────────┤
│  motor-pool │     Odysseus     │     Claude Code           │
│  (local ops) │  (personal use)  │  (coding agent)           │
├──────────────┴──────────────────┴───────────────────────────┤
│              shared local LLM layer                         │
│         Ollama  │  OpenLLM  │  Docker Model Runner          │
├─────────────────────────────────────────────────────────────┤
│              vector / memory layer                          │
│    turbovec (embedded)  │  pgvector (Thoth only)            │
├─────────────────────────────────────────────────────────────┤
│              sandbox / safety layer                         │
│                     NemoClaw                                │
└─────────────────────────────────────────────────────────────┘
```

---

## The Tools — Honest Breakdown

### motor-pool (yours)
**Role:** Local orchestrator, ops cockpit, MCP container manager  
**Layer:** Control plane

**What it actually does today:**
- Persistent LLM session management across Ollama + Docker Model Runner endpoints
- Webhook ingestion → task routing → event bus → agent lifecycle (start/stop/restart)
- NemoClaw sandboxed execution with `--cap-drop=all`
- OpenTelemetry tracing, structured JSON logging, health endpoints
- React dashboard with live Docker container status

**What it becomes in Q2/Q3:**
- GPU/CUDA-aware model loading (RTX 4080 target)
- MCP container manager — spins tool containers up/down on demand
- File I/O + workspace mounts for code authoring
- Multi-tenancy + RBAC
- bb-mcp / Blackboard frontend layer

**The key architectural insight:** motor-pool's MCP container manager (Q2) and its model lifecycle logic are the same primitive applied to two different container types. Design them together — one registry + lifecycle API — so you're not maintaining two separate on-demand spin-up systems.

**Pros:**
- Already your codebase — you control the roadmap
- Local-first, no external API calls
- NemoClaw safety sandbox already wired
- OpenTelemetry + structured logging already in place
- Webhook + REST API surface ready for integration

**Cons:**
- JavaScript/Express stack — adds friction if you want Python-native tooling inline
- No MCP server yet (Q2 planned) — currently a consumer, not a provider
- Model lifecycle is implicit today (no smart keep-warm/evict logic)
- No vector search layer yet

**Verdict:** This is the hub. Everything else is a spoke.

---

### OpenLLM (BentoML)
**Role:** High-throughput OpenAI-compatible model server  
**Layer:** Inference endpoint

**What it does:**
- Serves any HuggingFace model as a `/v1/chat/completions` REST endpoint
- Hot-swap models via CLI without restarting the container
- Run multiple model endpoints simultaneously on different ports
- Native CUDA/GPU container support — relevant for your Q2 GPU work

**How it fits motor-pool:**
- Register as a second endpoint type alongside `llm_qwen_coder` in compose
- Best home for models you build yourself that don't fit Ollama's Modelfile pattern
- Claude Code and Kryptos can hit it directly without going through motor-pool UI
- The right inference layer for your 1-off custom models

**Pros:**
- OpenAI-compat — zero code changes in any consumer
- Multiple simultaneous model endpoints
- CUDA-native, aligns with Q2 GPU enablement work
- Hot model swap

**Cons:**
- Heavier than Ollama for standard models — use Ollama for commodity models, OpenLLM for custom ones
- Full model weight in VRAM — don't run simultaneously with AirLLM
- Adds another service to the compose stack

**Integration path:** Add as `llm_openllm` service in `docker-compose.yml` alongside `llm_qwen_coder`. Expose on `8082` (host) → `3000` (container). Register in motor-pool's endpoint config as `openllm`.

---

### AirLLM
**Role:** Memory-efficient layer-streaming inference  
**Layer:** Inference (Python library, not a server)

**What it does:**
- Streams model weights layer-by-layer so 70B+ models run on 4–8 GB VRAM
- No server, no daemon — pure Python `import airlite` usage
- Trades throughput for memory headroom

**How it fits motor-pool:**
- Wrap it in a thin FastAPI container — same pattern as Docker Model Runner integration already exists
- Register as an optional endpoint: `airlite` in the model registry
- Only activate when a task explicitly requests a large model AND you don't have the VRAM to run it via OpenLLM
- Can drop it in as a tool/endpoint in motor-pool's model registry once the MCP container manager lands

**Pros:**
- Only path to running 70B+ locally on consumer hardware
- No server overhead — starts when needed
- MIT license, Python-native

**Cons:**
- Slow — layer streaming has real latency cost
- Single model at a time
- Cannot run simultaneously with OpenLLM without VRAM fights
- Needs a wrapper to become an endpoint motor-pool can call

**Verdict:** Not a Q2 priority. Add it after GPU enablement is stable, as an opt-in large-model endpoint. The FastAPI wrapper is ~50 lines.

---

### Thoth
**Role:** AI/ML research pipeline with persistent memory  
**Layer:** Specialized agent + knowledge store

**What it does:**
- Ingests papers from ArXiv, Semantic Scholar, NeurIPS, etc. via 7 source plugins
- Letta-based persistent memory — actual cross-session recall, not just context stuffing
- 60 MCP tools across 16 categories
- Hybrid RAG: pgvector (semantic) + BM25 (keyword)
- Obsidian vault integration — writes to `_thoth/` in your existing vault

**How it fits motor-pool:**
- Register as an MCP container in the Q2 MCP container manager
- motor-pool spins it up when a research task arrives, tears it down when idle
- Thoth's MCP tools surface through motor-pool's tool registry
- Runs in its own Docker network with its own PostgreSQL — isolated from motor-pool's SQLite

**Critical note:** Thoth's PostgreSQL + pgvector is heavy infrastructure. Keep it isolated. Don't let it bleed into motor-pool's data layer.

**Pros:**
- Obsidian integration is free since you already have a vault
- Persistent memory is genuinely different from what any other tool here offers
- MCP-native — designed to be consumed by orchestrators
- Best-in-class for AI/ML literature research

**Cons:**
- Heavy stack (PostgreSQL, pgvector, Letta, Obsidian plugin)
- Slow startup — not suitable for always-on
- Specialist tool — overkill for anything that isn't research

**Verdict:** High value for Kryptos research specifically. Register it as an on-demand MCP container once motor-pool's container manager ships. Don't run it always-on.

---

### Odysseus
**Role:** Self-hosted personal AI workspace  
**Layer:** General-purpose UI / daily driver

**What it does:**
- Chat, autonomous agents, deep research, email tools, memory in one app
- ChromaDB vector memory, SearXNG local search, MCP auto-registration at startup
- Supports Ollama / llama.cpp / vLLM as local backends
- No cloud, no monthly fee

**How it fits the stack:**
- Parallel to motor-pool, not under it
- Personal daily driver: chat, email drafting, general research, quick Q&A
- Points at the same Ollama/OpenLLM endpoints as motor-pool — they share the inference layer, they don't share a control plane
- Useful while motor-pool is mid-development (Q2 items not yet shipped)

**The key distinction:** motor-pool is your *ops cockpit* — task routing, agent lifecycle, model orchestration, bb-mcp integration. Odysseus is your *personal assistant* — the thing you open to have a conversation, draft something, or do a quick research task. They serve different moments.

**Pros:**
- Full-featured today, no build required
- Good Ollama support — points at your existing local models
- ChromaDB memory works out of the box

**Cons:**
- Very new (launched weeks ago) — unstable, hardware-sensitive
- ChromaDB + SearXNG adds weight
- Wants to be an orchestrator — don't let it become one in your stack
- Will overlap with motor-pool's eventual scope

**Verdict:** Use it now as a personal-layer tool while motor-pool matures. Reassess when motor-pool's MCP server and UI features ship Q2/Q3. Don't build anything critical on it.

---

### turbovec
**Role:** Compressed vector index for RAG  
**Layer:** Embedded library (no server, no daemon)

**What it does:**
- 16× compression: 31 GB of float32 vectors → 4 GB at 2-bit quantization
- No codebook training, no k-means, instant indexing — just `pip install turbovec`
- SIMD-accelerated: beats FAISS on ARM by 12–20%, competitive on x86
- Data-oblivious quantizer — works on any corpus without a training pass

**Where it plugs in:**

| Use case | How |
|---|---|
| Kryptos cipher/hypothesis RAG | Embedded in FastAPI container — index over `artifacts/`, no new infra |
| motor-pool MCP tool registry | In-process tool discovery / capability matching |
| motor-pool file workspace search | Semantic search over agent-accessible files once file I/O lands |
| Thoth alternative | Could replace pgvector RAG layer — reduces Thoth's infra footprint |

**Pros:**
- Zero infra — pure Python/Rust library
- No ports, no migrations, no server to manage
- Drop-in for any project that's doing flat-file or keyword search today
- MIT, pip-installable

**Cons:**
- Not a database — no persistence built in; you manage serialization
- Doesn't replace pgvector for complex filtered queries
- Under-1M vector scale is where it shines; larger corpora need benchmarking

**Verdict:** The easiest high-value addition in the entire stack. Add it to Kryptos FastAPI and motor-pool's tool registry work simultaneously. No architectural risk.

---

## The Direction

### Core principle
> **motor-pool is the local orchestrator. Everything else is either a registered service, a direct endpoint consumer, or out of scope.**

The MCP server motor-pool is planning in Q2 is the architectural keystone. Once motor-pool exposes its own MCP surface, it becomes a first-class provider that Claude Code, Kryptos, and any other tool can consume — not just a UI on top of Docker.

### Stack topology

```
┌─────────────────────────────────────────────────────────────────┐
│  PERSONAL LAYER                                                 │
│  Odysseus ──────────────────────────────────────────────────┐  │
│  (chat, email, general research, daily driver)              │  │
└─────────────────────────────────────────────────────────────┼──┘
                                                              │
┌─────────────────────────────────────────────────────────────▼──┐
│  ORCHESTRATION LAYER                                            │
│  motor-pool                                                    │
│  ├── model registry (Ollama, OpenLLM, AirLLM wrapper)          │
│  ├── MCP container manager (Thoth, Playwright, bb-mcp, etc.)   │
│  ├── task queue + webhook ingestion                             │
│  ├── NemoClaw sandbox                                           │
│  ├── turbovec (tool registry + file search)                     │
│  └── MCP server (exposes motor-pool to external consumers)     │
└────────────────────────────────────┬───────────────────────────┘
                                     │ MCP / REST / OpenAI-compat
┌────────────────────────────────────▼───────────────────────────┐
│  DIRECT CONSUMERS (bypass motor-pool UI, use endpoints raw)    │
│  Claude Code ──── hits Ollama/OpenLLM directly                  │
│  Kryptos ─────── hits Ollama/OpenLLM + turbovec embedded        │
│  Scripts/CLI ─── hit motor-pool REST API or model endpoints    │
└─────────────────────────────────────────────────────────────────┘
                                     │
┌────────────────────────────────────▼───────────────────────────┐
│  INFERENCE LAYER                                                │
│  Ollama (llm_qwen_coder) ── commodity models, Modelfile-based   │
│  OpenLLM ────────────────── custom/built models, CUDA-native    │
│  AirLLM wrapper (opt-in) ── 70B+ on constrained VRAM           │
│  Docker Model Runner ────── already wired, optional             │
└─────────────────────────────────────────────────────────────────┘
                                     │
┌────────────────────────────────────▼───────────────────────────┐
│  SPECIALIST SERVICES (on-demand, MCP container managed)         │
│  Thoth ──── research + persistent memory (via Obsidian vault)   │
└─────────────────────────────────────────────────────────────────┘
```

### Claude Code + local models

Claude Code should be able to hit your local Ollama/OpenLLM endpoints regardless of whether motor-pool is running. The way to wire this is through Claude Code's model configuration — point it at `http://localhost:8081` (Ollama) or `http://localhost:8082` (OpenLLM) as an OpenAI-compat provider. motor-pool doesn't sit in this path. It's a parallel consumer of the same endpoints, not a proxy.

Once motor-pool exposes its own MCP server, Claude Code can *also* consume motor-pool tools (task creation, model routing, sandbox execution) as MCP tools — giving you the best of both: direct model access AND orchestrated tooling when you need it.

---

## Integration Priority Queue

### Now (no new infra)
1. `pip install turbovec` → add to Kryptos FastAPI for artifact/hypothesis RAG
2. Add OpenLLM as `llm_openllm` service in `docker-compose.yml` — second endpoint type for custom models
3. Configure Odysseus to point at `localhost:8081` (Ollama) for personal use

### Q2 (aligned with roadmap)
4. GPU/CUDA enablement → OpenLLM gets CUDA flags, Ollama gets `device: gpu` in compose
5. MCP container manager → register Thoth as first on-demand container
6. turbovec in motor-pool's tool registry / capability matching
7. AirLLM FastAPI wrapper → register as opt-in large-model endpoint
8. motor-pool MCP server → expose to Claude Code and Kryptos

### Q3+
9. File I/O workspace access → turbovec index over agent-accessible files
10. bb-mcp + Blackboard frontend via motor-pool UI
11. Thoth turbovec swap (replace pgvector RAG layer to reduce infra weight)

---

## What to Avoid

| Temptation | Why not |
|---|---|
| Making Odysseus the orchestrator | It overlaps with motor-pool's scope. Use it as a consumer, not a hub. |
| Running AirLLM + OpenLLM simultaneously | They fight for VRAM. Pick one per task profile. |
| Letting Thoth run always-on | Heavy stack — PostgreSQL + pgvector + Letta. On-demand only via MCP container manager. |
| Proxying Claude Code through motor-pool | Direct endpoint access is simpler and faster. motor-pool adds value as an MCP tool provider, not a proxy. |
| Adding turbovec as a separate service | It's a library. Keep it embedded. Never containerize it standalone. |
| Two separate lifecycle APIs (one for models, one for MCP tools) | Same primitive. Design one registry + lifecycle API and apply it to both. |

---

## Open Questions

- **motor-pool MCP server spec** — what tools does it expose? Suggest: task CRUD, model endpoint registry, container status, sandbox execution. Needs a SPEC.md.
- **Model eviction policy** — currently models stay loaded until manually pulled. Once GPU work lands, need a keep-warm/evict heuristic (LRU? explicit TTL per model?).
- **turbovec serialization** — where does the index live on disk? Suggest: `data/turbovec/` volume mount in compose, one index file per namespace (tools, kryptos-artifacts, workspace-files).
- **Thoth ↔ motor-pool auth** — once Thoth is an on-demand MCP container, how does motor-pool authenticate to it? Design this before the container manager ships.
