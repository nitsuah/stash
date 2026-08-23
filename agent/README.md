# Personal Agent System

Agent prompts for personal operations and a product delivery pipeline.
Each prompt defines a specific role, operating rules, and expected outputs.
Use as system prompts in Claude.ai or load via the Anthropic SDK.

---

## Personal Agents

| Agent | File | Purpose | Cadence |
|-------|------|---------|---------|
| CFO | [projects/Finance.md](projects/Finance.md) | Track finances, runway, CDs; generate weekly financial summaries | Weekly or on-demand |
| Career | [projects/Career.md](projects/Career.md) | Evaluate job listings, draft outreach, track applications | When job-hunting |
| Builder | [projects/Builder.md](projects/Builder.md) | Find leads, close web design clients, manage project pipeline | When building |

---

## Delivery Pipeline Agents

| Agent | Prompt | Purpose |
|-------|--------|---------|
| PMO | [prompts/PMO.md](prompts/PMO.md) | Audit products, maintain ROADMAP/TASKS, enforce governance |
| Intake | [projects/Intake.md](projects/Intake.md) | Convert findings into prioritized, acceptance-ready tasks |
| Software Engineer | [prompts/ENG.md](prompts/ENG.md) | Implement features, refactor, fix bugs |
| DevOps | [prompts/OPS.md](prompts/OPS.md) | Validate infra, CI/CD, ship via branch + PR |
| QA | [prompts/QA.md](prompts/QA.md) | Verify quality, prevent regressions |
| Oncall | [prompts/Oncall.md](prompts/Oncall.md) | Incident response, user feedback triage |
| Automation | [prompts/AUTO.md](prompts/AUTO.md) | Internal tooling and workflow automation |
| Growth | [prompts/Growth.md](prompts/Growth.md) | Monetization, adoption, growth experiments |

**Recommended flow:** PMO → Intake → ENG → OPS → QA → Oncall → loop

---

## Reusable Prompt Modules

| Module | File | Purpose |
|--------|------|---------|
| DAILY | [prompts/DAILY.md](prompts/DAILY.md) | Daily standup and planning prompt |
| HANDOFF | [prompts/HANDOFF.md](prompts/HANDOFF.md) | Structured handoff template between agents |
| CLEANUP | [prompts/CLEANUP.md](prompts/CLEANUP.md) | Codebase cleanup and housekeeping prompt |
| MINI | [prompts/MINI.md](prompts/MINI.md) | Lightweight engineering task runner for low-cost model delegation |
| TEST | [prompts/TEST.md](prompts/TEST.md) | Test strategy and coverage prompt |
| LOC | [prompts/LOC.md](prompts/LOC.md) | LOC analysis automation for the delivery pipeline |
| TIRE | [prompts/TIRE.md](prompts/TIRE.md) | Tire-kick evaluation prompt for new tools/libraries |

---

## Per-Repo Context Files

The `repos/` directory contains per-repository context files loaded alongside agent prompts. Each `.md` file gives an agent background on a specific repo's architecture, conventions, and current state.

| File | Covers |
|------|--------|
| [repos/stash.md](repos/stash.md) | This repository |
| [repos/overseer.md](repos/overseer.md) | Overseer agent platform |
| [repos/agent-board.md](repos/agent-board.md) | Agent board dashboard |
| [repos/kryptos.md](repos/kryptos.md) | Kryptos cipher research system |
| [repos/darkmoon.md](repos/darkmoon.md) | Darkmoon multiplayer game |
| [repos/farm-3j.md](repos/farm-3j.md) | Farm RTS game |
| [repos/nitsuah-io.md](repos/nitsuah-io.md) | nitsuah.io portfolio site |
| [repos/](repos/) | All repos |

---

## How To Use

**In Claude.ai:**
1. Start a new conversation.
2. Paste the contents of the relevant `.md` prompt as your first message, or set it as a Project Instruction.
3. If you need repo-specific context, also paste the relevant `repos/<repo>.md`.

**Via Anthropic SDK:**
```python
import anthropic

with open("agent/prompts/PMO.md") as f:
    system_prompt = f.read()

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=8096,
    system=system_prompt,
    messages=[{"role": "user", "content": "Audit the stash repo and update ROADMAP.md."}]
)
```

---

## Additional Documentation

See [REPO-README.md](REPO-README.md) for scope, projects index, and notes index.
See [projects/scope.md](projects/scope.md) for the full project scope definition.
