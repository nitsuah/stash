# Personal Agent System

Three focused Claude agents for your three operational domains.
Each has its own system prompt and purpose-built skills.

---

## Agents

| Agent | File | Purpose | Cadence |
|-------|------|---------|---------|
| 💼 CFO | `agents/cfo/Finance.md` | Track finances, runway, CDs | Weekly or on-demand |
| 🧑‍💻 Career | `agents/career/Career.md` | Evaluate jobs, draft outreach | When job-hunting |
| 🔧 Builder | `agents/builder/Builder.md` | Find leads, close web design clients | When building |

---

## Skills

| Skill | Used By | What It Does |
|-------|---------|-------------|
| `financial-summary` | CFO | Structured financial snapshots + runway calc |
| `job-evaluator` | Career | Scores roles on stress / pay / fit |
| `lead-finder` | Builder | Finds local biz leads with weak web presence |
| `outreach-writer` | Career + Builder | Drafts cold emails, DMs, follow-ups |

---

## Usage

### Option A: Claude.ai (simplest)
1. Open 3 separate Claude chats
2. Paste the contents of each `.md` file as the system prompt
3. Chat normally

### Option B: Run locally with Python
```bash
pip install anthropic python-dotenv
export ANTHROPIC_API_KEY=sk-...
AGENT=cfo python run_agent.py
```

### Option C: Docker
```bash
# Build
docker build -t personal-agents .

# Run CFO agent
docker run -it -e ANTHROPIC_API_KEY=sk-... -e AGENT=cfo personal-agents

# Run Career agent
docker run -it -e ANTHROPIC_API_KEY=sk-... -e AGENT=career personal-agents

# Run Builder agent
docker run -it -e ANTHROPIC_API_KEY=sk-... -e AGENT=builder personal-agents
```

### Option D: Docker Compose
```bash
# Create .env file first
echo "ANTHROPIC_API_KEY=sk-..." > .env

# Run any agent
docker compose run cfo
docker compose run career
docker compose run builder
```

### Push to Docker Hub
```bash
docker tag personal-agents yourusername/personal-agents:latest
docker push yourusername/personal-agents:latest
```

---

## File Structure

```
.
├── agents/
│   ├── cfo/Finance.md          # CFO system prompt
│   ├── career/Career.md        # Career system prompt
│   └── builder/Builder.md      # Builder system prompt
├── skills/
│   ├── financial-summary/SKILL.md
│   ├── job-evaluator/SKILL.md
│   ├── lead-finder/SKILL.md
│   └── outreach-writer/SKILL.md
├── run_agent.py                # CLI runner
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Suggested Routine

| When | Agent | Action |
|------|-------|--------|
| Monday morning | CFO | "Give me my weekly summary" |
| Job opportunity appears | Career | Paste job description, get scored |
| Want to work on clients | Builder | "Find me 5 leads in [city]" |
| Recruiter messages you | Career | "Help me reply to this recruiter" |
| Ready to send outreach | Builder/Career | "Write me a message for [target]" |

---

## Notes

- All agents are in LOW EFFORT / calm mode by default
- No agent will push you to grind or overwhelm you
- Docker containerization is ready but defer to Claude.ai pasting until you have 2–3 paying clients

---

## Product Delivery Pipeline Agents

The repository now also includes a Product Delivery Pipeline agent set for product planning and execution governance.

| Agent | File | Purpose |
|-------|------|---------|
| PMO | PMO.md | Audit products, maintain ROADMAP/TASKS from evidence, enforce branch + PR governance |
| Intake | Intake.md | Convert findings/requests into prioritized, acceptance-ready tasks |
| Delivery/DevOps | DevOps.md | Implement approved tasks, validate changes, ship via branch + PR |
| QA | QA.md | Verify quality, prevent regressions, and feed improvements back into planning |

Recommended flow:

1. PMO audit identifies reality gaps and planning updates.
2. Intake shapes those into clear, prioritized implementation briefs.
3. Delivery/DevOps executes on branches and opens evidence-backed PRs.
4. QA validates behavior and routes defects/improvements back to TASKS/ROADMAP.
