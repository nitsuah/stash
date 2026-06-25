# Personal Agent System

Agent prompts for personal operations and a product delivery pipeline.
Each prompt defines a specific role, operating rules, and expected outputs.

---

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

See [AGENT-MAIN.md](AGENT-MAIN.md) for the full autonomous delivery flow and run-order checklist.

---

## Prompt Modules

Reusable context modules passed alongside agent prompts:

| Module | File | Use |
| ------ | ---- | ---- |
| Handoff template | [prompts/HANDOFF.md](prompts/HANDOFF.md) | Shared artifact between pipeline agents |
| PM standards | [docs/OVERSEER-COMPLIANCE.md](OVERSEER-COMPLIANCE.md) | Overseer compliance formatting |
| Test strategy | [prompts/TEST.md](prompts/TEST.md) | Incremental testing and coverage |
| LOC analysis | [prompts/LOC.md](prompts/LOC.md) | Hotspot analysis and refactor planning |
| Repo cleanup | [prompts/CLEANUP.md](prompts/CLEANUP.md) | Structured repo cleanup (root, tests, data, docs) |
| Repo hygiene | [prompts/MINI.md](prompts/MINI.md) | Safe repo organization |
| Task flow | [prompts/1FLOW.md](prompts/1FLOW.md) | Task management conventions |

---

## Repo Context Files

Per-repo context loaded when running agents against a specific repository:

| Repo               | File                                                       |
| ------------------ | ---------------------------------------------------------- |
| odysseus           | [[Odysseus]]                                               |
| stash              | [repos/stash.md](repos/stash.md)                           |
| nitsuah.io         | [repos/nitsuah-io.md](repos/nitsuah-io.md)                 |
| darkmoon           | [repos/darkmoon.md](repos/darkmoon.md)                     |
| bb-mcp             | [repos/bb-mcp.md](repos/bb-mcp.md)                         |
| overseer           | [repos/overseer.md](repos/overseer.md)                     |
| skyview            | [repos/skyview.md](repos/skyview.md)                       |
| agent-board        | [repos/agent-board.md](repos/agent-board.md)               |
| kryptos            | [repos/kryptos.md](repos/kryptos.md)                       |
| gcp                | [repos/gcp.md](repos/gcp.md)                               |
| osrs               | [repos/osrs.md](repos/osrs.md)                             |
| games              | [repos/games.md](repos/games.md)                           |
| auto-apply-plugin  | [repos/auto-apply-plugin.md](repos/auto-apply-plugin.md)   |
| avatar             | [repos/avatar.md](repos/avatar.md)                         |
| farm-3j            | [repos/farm-3j.md](repos/farm-3j.md)                       |
| fire               | [repos/fire.md](repos/fire.md)                             |
| opencut            | [repos/opencut.md](repos/opencut.md)                       |
| opencut-controller | [repos/opencut-controller.md](repos/opencut-controller.md) |
| vhs                | [repos/vhs.md](repos/vhs.md)                               |

---

## Scripts

| Script | File | Purpose |
| ------ | ---- | ------- |
| sync-repos | [scripts/sync-repos.ps1](scripts/sync-repos.ps1) | Sync repo docs from live repos, update Last Validated, report new HANDOFFs |

---

## Docs

| Doc | File |
| --- | ---- |
| Enhancement roadmap | [docs/ENHANCEMENT_ROADMAP.md](ENHANCEMENT_ROADMAP.md) |
| Gaps & improvement plan | [docs/GAPS_AND_IMPROVEMENT_PLAN.md](GAPS_AND_IMPROVEMENT_PLAN.md) |
| Security checklist | [docs/SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) |
| Mass feedback | [docs/MASS-FEEDBACK.md](MASS-FEEDBACK.md) |
| Q2 2026 planning | [docs/2026Q2.md](2026Q2.md) |
| Productization & Tiering | [docs/PRODUCTIZATION.md](PRODUCTIZATION.md) |

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

## Tool & Model Setup (per device)

> These settings are **not git-tracked** — configure once per machine after cloning.
> `.obsidian/` and `.nexus/` are intentionally excluded from version control (contain certs, device IDs, and secrets).

### 1. Start 9router

9router is a local Docker container that proxies all AI requests — enables provider fallback, token savings (RTK), and multi-account pooling.

```bash
cd ~/code/9router
docker compose up -d   # auto-restarts with Docker Desktop
```

Dashboard: http://localhost:20128 — add at least one provider, copy your API key.

### 2. Claude Code

In `~/.claude/settings.json` env block:
```json
"ANTHROPIC_BASE_URL": "http://localhost:20128/v1",
"ANTHROPIC_API_KEY": "<your-9router-api-key>"
```

Recommended model: `cc/claude-sonnet-4-6` (routes through Claude Code subscription via 9router).

### 3. Obsidian / Nexus plugin

This folder is the Obsidian vault. Nexus must be configured per device:

1. Open Obsidian with this vault
2. Settings → Community Plugins → Nexus → enable **openai** provider:
   - Base URL: `http://localhost:20128/v1`
   - API Key: `<your-9router-api-key>`
   - Default model: `cc/claude-sonnet-4-6`
3. Confirm Local REST API plugin is active with insecure port **27123** enabled

### 4. Claude Code → Obsidian MCP

`~/.claude/mcp.json` obsidian entry must use **HTTP** port 27123 (not HTTPS 27124):
```json
"obsidian": {
  "type": "http",
  "url": "http://127.0.0.1:27123/mcp/",
  "headers": { "Authorization": "Bearer <OBSIDIAN_API_KEY>" }
}
```

`OBSIDIAN_API_KEY` is found in Obsidian → Settings → Local REST API.
**Obsidian must be open** for the MCP to be reachable — it is not a background service.

---

## File Structure

```text
agent/
├── AGENT-MAIN.md          # Autonomous delivery flow + run-order checklist
├── README.md
├── docs/                  # Planning docs, roadmaps, feedback archives
├── projects/              # Personal agent definitions (Finance, Career, Builder, Intake)
├── prompts/               # Delivery pipeline agent prompts + reusable modules
├── scripts/               # Maintenance scripts (sync-repos, etc.)
└── repos/                 # Per-repo context files (summary + synced subdirs)
```

## Related
- [[AGENT-MAIN]] — autonomous delivery flow and run-order checklist
- [[prompts/PMO|PMO]] — planning authority and audit workflow
- [[2026Q2]] — current quarter planning
- [[OVERSEER-COMPLIANCE|Overseer Compliance]] — documentation standards
- [[repos/stash|stash runbook]] — vault root runbook and index
