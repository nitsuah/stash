# Personal Agent System

Agent prompts for personal operations and a product delivery pipeline.
Each prompt defines a specific role, operating rules, and expected outputs.

---
Scope: [[scope.md]]

## Personal Agents

| Agent | File | Purpose | Cadence |
| ----- | ---- | ----- | ------- |
| 💼 CFO | [projects/Finance.md](projects/Finance.md) | Track finances, runway, CDs | Weekly or on-demand |
| 🧑‍💻 Career | [projects/Career.md](projects/Career.md) | Evaluate jobs, draft outreach | When job-hunting |
| 🔧 Builder | [projects/Builder.md](projects/Builder.md) | Find leads, close web design clients | When building |

---

## Delivery Pipeline Agents

| Agent | Prompt | Purpose |
| ----- | ------ | ------- |
| PMO | [prompts/PMO.md](prompts/PMO.md) | Audit products, maintain ROADMAP/TASKS, enforce governance |
| Intake | [projects/Intake.md](projects/Intake.md) | Convert findings into prioritized, acceptance-ready tasks |
| Software Engineer | [prompts/ENG.md](prompts/ENG.md) | Implement features, refactor, fix bugs |
| DevOps | [prompts/OPS.md](prompts/OPS.md) | Validate infra, CI/CD, ship via branch + PR |
| QA | [prompts/QA.md](prompts/QA.md) | Verify quality, prevent regressions |
| Oncall | [prompts/Oncall.md](prompts/Oncall.md) | Incident response, user feedback triage |
| Automation | [prompts/AUTO.md](prompts/AUTO.md) | Internal tooling and workflow automation |
| Growth | [prompts/Growth.md](prompts/Growth.md) | Monetization, adoption, growth experiments |

**Recommended flow:** PMO → Intake → ENG → OPS → QA → Oncall → loop
