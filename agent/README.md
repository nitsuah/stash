# Personal Agent System

Agent prompts for personal operations and a product delivery pipeline.
Each prompt defines a specific role, operating rules, and expected outputs.

---

## Personal Agents

| Agent | File | Purpose | Cadence |
|-------|------|---------|---------|
| 💼 CFO | [projects/Finance.md](projects/Finance.md) | Track finances, runway, CDs | Weekly or on-demand |
| 🧑‍💻 Career | [projects/Career.md](projects/Career.md) | Evaluate jobs, draft outreach | When job-hunting |
| 🔧 Builder | [projects/Builder.md](projects/Builder.md) | Find leads, close web design clients | When building |

---

## Delivery Pipeline Agents

| Agent | Prompt | Purpose |
|-------|--------|---------|
| PMO | [prompts/PMO.md](prompts/PMO.md) | Audit products, maintain ROADMAP/TASKS, enforce governance |
| Intake | [projects/Intake.md](projects/Intake.md) | Convert findings into prioritized, acceptance-ready tasks |
| Software Engineer | [prompts/SoftwareEng.md](prompts/SoftwareEng.md) | Implement features, refactor, fix bugs |
| DevOps | [prompts/DevOps.md](prompts/DevOps.md) | Validate infra, CI/CD, ship via branch + PR |
| QA | [prompts/QA.md](prompts/QA.md) | Verify quality, prevent regressions |
| Oncall | [prompts/Oncall.md](prompts/Oncall.md) | Incident response, user feedback triage |
| Automation | [prompts/AUTO.md](prompts/AUTO.md) | Internal tooling and workflow automation |
| Growth | [prompts/Growth.md](prompts/Growth.md) | Monetization, adoption, growth experiments |

**Recommended flow:** PMO → Intake → SoftwareEng → DevOps → QA → Oncall → loop

See [AGENT-MAIN.md](AGENT-MAIN.md) for the full autonomous delivery flow and run-order checklist.

---

## Prompt Modules

Reusable context modules passed alongside agent prompts:

| Module | File | Use |
|--------|------|-----|
| Handoff template | [prompts/HANDOFF.md](prompts/HANDOFF.md) | Shared artifact between pipeline agents |
| PM standards | [prompts/PM.md](prompts/PM.md) | Overseer compliance formatting |
| Test strategy | [prompts/TEST.md](prompts/TEST.md) | Incremental testing and coverage |
| LOC analysis | [prompts/LOC.md](prompts/LOC.md) | Hotspot analysis and refactor planning |
| Repo hygiene | [prompts/MINI.md](prompts/MINI.md) | Safe repo organization |
| Task flow | [prompts/FLOW-TASKS.md](prompts/FLOW-TASKS.md) | Task management conventions |

---

## Repo Context Files

Per-repo context loaded when running agents against a specific repository:

| Repo | File |
|------|------|
| stash | [repos/stash.md](repos/stash.md) |
| nitsuah.io | [repos/nitsuah-io.md](repos/nitsuah-io.md) |
| darkmoon | [repos/darkmoon.md](repos/darkmoon.md) |
| bb-mcp | [repos/bb-mcp.md](repos/bb-mcp.md) |
| overseer | [repos/overseer.md](repos/overseer.md) |
| skyview | [repos/skyview.md](repos/skyview.md) |
| agent-board | [repos/agent-board.md](repos/agent-board.md) |
| kryptos / gcp / osrs / games | [repos/](repos/) |

---

## Docs

| Doc | File |
|-----|------|
| Enhancement roadmap | [docs/ENHANCEMENT_ROADMAP.md](docs/ENHANCEMENT_ROADMAP.md) |
| Gaps & improvement plan | [docs/GAPS_AND_IMPROVEMENT_PLAN.md](docs/GAPS_AND_IMPROVEMENT_PLAN.md) |
| Security checklist | [docs/SECURITY_CHECKLIST.md](docs/SECURITY_CHECKLIST.md) |
| Mass feedback | [docs/MASS-FEEDBACK.md](docs/MASS-FEEDBACK.md) |
| Q2 2026 planning | [docs/2026Q2.md](docs/2026Q2.md) |

---

## Usage

### Option A: Claude.ai (simplest)
1. Open a new Claude chat
2. Paste the contents of the relevant `.md` file as the system prompt
3. Chat normally — optionally attach the repo context file from `repos/`

### Option B: Run locally with Python
```bash
pip install anthropic python-dotenv
export ANTHROPIC_API_KEY=sk-...
AGENT=pmo python run_agent.py
```

### Option C: Docker
```bash
docker build -t personal-agents .
docker run -it -e ANTHROPIC_API_KEY=sk-... -e AGENT=pmo personal-agents
```

---

## File Structure

```
agent/
├── AGENT-MAIN.md          # Autonomous delivery flow + run-order checklist
├── README.md
├── docs/                  # Planning docs, roadmaps, feedback archives
├── projects/              # Personal agent definitions (Finance, Career, Builder, Intake)
├── prompts/               # Delivery pipeline agent prompts + reusable modules
└── repos/                 # Per-repo context files
```
