# Odysseus Ecosystem — Current State Diagram

repo: [odysseus]

Simplified view: odysseus's actual capabilities, its sibling stacks, and the
repos accessible via the shared drive mount (split into deployed vs internal).

Green = working today. Red solid = exists but broken. Red dashed = not wired
up / doesn't exist yet.

```mermaid
flowchart LR
    OD["odysseus<br>(llama3.2:3b · bash)"]

    subgraph CORE["odysseus capabilities"]
        direction TB
        SOCK["Docker socket"]
        MOUNT["shared drive mount"]
        BRAIN["memory (24) +<br>skills (112)"]
        TASKS["tasks<br>(scheduled/event)"]
        RESEARCH["deep research"]
        CAL["calendar<br>(sync broken)"]
        COOK["cookbook<br>(broken)"]
    end

    OD --> CORE

    subgraph SIBLINGS["sibling stacks"]
        direction TB
        AGENTBOARD["agent-board stack<br>(multi-model harness,<br>nemoclaw, ollama-agent :8081)"]
        VHS["vhs stack<br>(ollama-vhs :11434)<br>+ NeonDB"]
    end

    OD <-->|"chat / delegation"| AGENTBOARD
    OD <-->|"model inference<br>:11434"| VHS

    subgraph REPOS["repos (shared drive mount)"]
        direction TB
        subgraph DEPLOY["deployed"]
            direction TB
            D1["overseer<br>+ NeonDB"]
            D2["nitsuah-io"]
            D3["games"]
            D4["darkmoon"]
            D5["client sites"]
        end
        subgraph INTERNAL["internal"]
            direction TB
            FIRE["fire<br>(local + API, or<br>NeonDB only — TBD)"]
        end
    end

    MOUNT -.->|"not yet wired"| REPOS
    AGENTBOARD -.->|"not yet wired"| DEPLOY

    classDef have fill:#f0fdf4,stroke:#16a34a,stroke-width:2px,color:#000000
    classDef core fill:#f5f3ff,stroke:#a78bfa,stroke-width:2px,color:#000000
    classDef sibling fill:#e0f2fe,stroke:#0284c7,stroke-width:2px,color:#000000
    classDef broken fill:#fef2f2,stroke:#dc2626,stroke-width:2px,color:#000000
    classDef missing fill:#fef2f2,stroke:#dc2626,stroke-width:2px,stroke-dasharray: 3 3,color:#000000
    classDef groupbox fill:transparent,stroke:#9ca3af,stroke-width:1px,color:#000000

    OD:::core
    SOCK:::have
    MOUNT:::have
    BRAIN:::have
    TASKS:::have
    RESEARCH:::have
    CAL:::broken
    COOK:::broken
    AGENTBOARD:::sibling
    VHS:::sibling
    FIRE:::missing
    D1:::missing
    D2:::missing
    D3:::missing
    D4:::missing
    D5:::missing
    CORE:::groupbox
    SIBLINGS:::groupbox
    REPOS:::groupbox
    DEPLOY:::groupbox
    INTERNAL:::groupbox
```

odysseus_ecosystem_diagram