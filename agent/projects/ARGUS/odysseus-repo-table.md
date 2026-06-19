# Odysseus Integration Table — All Repos

> Odysseus sits at the center as the brain and orchestrator. It doesn't need to do the coding itself — it reads workspaces, schedules tasks, kicks off agents, monitors containers, and routes work to the right tool. The shared drive mount means every repo is just a file path away. The Docker socket means it can restart containers, trigger builds, and eventually kick off autonomous Claude/agent loops.

---

## Repo Table

| Repo                  | Type                                      | Status                            | Odysseus Role                                                                                                                                                                                                                                              | Connection Method                                                                                                                                                        | Priority                              |
| --------------------- | ----------------------------------------- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------- |
| **odysseus**          | Core workspace / self                     | 🟢 Running                        | Self-aware brain. Writes its own skills, docs, and config. Restarts itself via Docker socket. Knows its own API.                                                                                                                                           | Self-referential via `/api/codex/*` + Docker socket + shared drive                                                                                                       | 🔴 Ongoing                            |
| **agent-board**       | Multi-service AI ops platform             | 🟢 Active — multi-container stack | Sister platform. Shares Ollama. Odysseus monitors its containers, receives outputs from its tools, and can delegate heavy agent tasks to it. Potential: Odysseus kicks off agent-board tool runs for autonomous coding/content loops.                      | Docker socket (container health, restart); shared Ollama at `8081`; tool output webhooks → Odysseus notes                                                                | 🔴 High                               |
| **stash**             | Personal knowledge vault + Obsidian vault | 🟢 Active — always growing        | Odysseus primary external brain. Reads Obsidian notes, enterprise scripts, all MD. Writes back session summaries, research outputs, decisions, generated skills. Git-tracked, Obsidian-readable, permanent.                                                | Shared drive mount (read + write); session-dump task; weekly index cron                                                                                                  | 🔴 High                               |
| **overseer**          | Meta-repo intelligence layer              | 🟡 Active — building out          | Aggregates "what needs to happen next" across all repos. Stalled PRs, vuln fixes, missing docs, ROADMAP/TASKS/FEATURES health. Odysseus reads these MD files directly from workspace and takes or delegates action — commits, PR creation, build triggers. | Shared drive: `workspace/<repo>/ROADMAP.md` etc. direct read; GitHub MCP for PR/issue actions; Docker socket to kick off builds/tests; overseer webhook → Odysseus todos | 🔴 High                               |
| **fire**              | FIRE tracker + API server                 | 🟡 Active                         | Financial context grouped elsewhere. Odysseus polls periodically and surfaces numbers in morning briefing. Circle back later.                                                                                                                              | Scheduled API poll → Odysseus note; milestone webhook → todo                                                                                                             | 🟡 Eventually                         |
| **vhs**               | VHS collection index (active dev)         | 🟡 WIP — active for GF            | Odysseus can help curate entries, research valuations, write back to JSON via shell. NeonDB is the interesting asset — one of only 3 repos with one.                                                                                                       | Shared drive + shell tool; NeonDB direct query potential                                                                                                                 | 🟡 Low-Medium (loop back when active) |
| **kryptos**           | K4 cipher toolkit                         | 🔵 Side project                   | Cool autonomous sub-agent pattern. NeonDB. Low priority but fun. Loop back.                                                                                                                                                                                | Shell tool; NeonDB                                                                                                                                                       | 🟢 Low                                |
| **bb-mcp**            | Blackboard MCP server                     | 🟡 WIP — part of agent-board      | Deprioritize for now. Will eventually be a good example of a semi-complex MCP layered on top of a local/remote LLM inside agent-board. Pull from image registry or GitHub when ready.                                                                      | TBD — agent-board integration first                                                                                                                                      | 🟢 Deprioritized                      |
| **avatar**            | Generative AI model trainer               | 🔵 Deprioritized                  | Interesting as a future agent-board experience concept (user uploads images → agent-board runs fine-tune pipeline). Not now.                                                                                                                               | Concept only for now                                                                                                                                                     | 🟢 Low                                |
| **auto-apply-plugin** | Chrome job application autofill           | 🔵 Low priority                   | Lower than previously listed. Drop it for now.                                                                                                                                                                                                             | —                                                                                                                                                                        | 🟢 Low                                |
| **gcp**               | Google Drive audit/copy CLI               | 🔵 Utility                        | Role TBD. Basic Gemini is enough for now. Revisit if skills fall flat or a clear automation need emerges.                                                                                                                                                  | Shell tool when needed                                                                                                                                                   | 🟢 Low                                |
| **opencut-classic**   | Forked video editor                       | 🔵 Exploring                      | Want to play with it first. Potentially becomes an agent-board experience — its own SLM/container that helps edit AI-generated content from agent-board tools. One to watch.                                                                               | TBD — evaluate first                                                                                                                                                     | 🟢 Low (watch)                        |
| **darkmoon**          | Multiplayer 3D game (live)                | 🔵 Proof of concept               | Downtime loops only. CI failure alerts are the one useful hook.                                                                                                                                                                                            | GitHub Actions webhook → todo if broken                                                                                                                                  | 🟢 Very Low                           |
| **games**             | Browser arcade (live)                     | 🔵 Proof of concept               | Same as darkmoon.                                                                                                                                                                                                                                          | GitHub Actions webhook → todo                                                                                                                                            | 🟢 Very Low                           |
| **farm-3j**           | Client farm site                          | 🔵 Client PoC                     | Loop on downtime.                                                                                                                                                                                                                                          | Deploy webhook → log                                                                                                                                                     | 🟢 Very Low                           |
| **skyview**           | Client drone services site                | 🔵 Hands-off client               | Ignore. They'll ask if they need updates.                                                                                                                                                                                                                  | None                                                                                                                                                                     | ⬛ Ignore                              |
| **osrs**              | OSRS bot                                  | 🔵 Ignore                         | Ignore.                                                                                                                                                                                                                                                    | None                                                                                                                                                                     | ⬛ Ignore                              |

---

## Agent-Board Container Map

Since Odysseus has Docker socket access, here's what it can see and interact with:

| Container | Image | Port | Odysseus Interaction |
|---|---|---|---|
| `agent-board` | `agent-board` | `6, 11, 7, 23` | Main app — webhook target for tool outputs; health monitor |
| `agent-dashboard` | `agent-board-agent-dashboard` | `3000` | UI layer — Odysseus can check if it's up; pull session data |
| `agent-db` | `postgres:16-alpine` | `5432` | Postgres backing store — Odysseus could query for session logs if needed |
| `nemoclaw` | `nemoclaw:latest` | `9000→8080` | Unknown role — investigate; likely a specialized model or tool runner |
| `ollama` | `ollama/ollama:latest` | `8081→8080` | Shared with Odysseus. Both platforms use the same models |
| `tool-content-gen` | `agent-board-tool-content-gen` | `3200` | Content generation tool — Odysseus can trigger and receive output |
| `tool-website` | `agent-board-tool-website` | `3201` | Website tool — similar, Odysseus can orchestrate |

**What Odysseus can do with Docker socket:**
- `docker ps` → health check all containers, alert if any down
- `docker restart <container>` → recover crashed services
- `docker logs <container> --tail 50` → pull logs for debugging or summaries
- `docker compose up -d` → spin up new services from workspace
- Kick off a build in another repo: `cd /workspace/overseer && docker compose build && docker compose up -d`
- Eventually: start a Claude Code loop or codex agent container as a sub-task

---

## Stash Deep Dive

Stash is the most underrated piece of the whole setup. It's not a side repo — it's the permanent knowledge layer.

### What lives there
- Full Obsidian vault (config + all your notes)
- 15 years of enterprise automation (VBA, PowerShell, Atlassian templates)
- Tons of MD files — runbooks, notes, decisions, configs

### Read flows (stash → Odysseus)
- Agent reads any file directly: `cat /workspace/stash/notes/topic.md`
- Weekly index cron: scan all `.md` → generate searchable TOC doc in Odysseus
- Obsidian notes become live RAG context in agent chat
- Scripts become callable: "find the PowerShell script that does AD user detection" → agent greps, reads, summarizes

### Write flows (Odysseus → stash)
- **Session dump task**: at end of significant chats → write `stash/odysseus/YYYY-MM-DD-topic.md`
- **Research outputs**: deep research results → `stash/research/`
- **Decisions**: when agent helps decide something → append to `stash/decisions/`
- **Generated skills**: new skills Odysseus creates → `stash/skills/` + load into Odysseus
- **Cross-repo analysis**: overseer findings + ROADMAP reviews → `stash/ops/`

Result: stash becomes a permanent, git-tracked, Obsidian-readable record of everything the workspace does. Your second brain gets auto-fed.

**The task:**
```
Trigger: session_end event (or nightly cron)
Action: Summarize session outputs, decisions, learnings
        Write to /workspace/stash/odysseus/[date]-[topic].md
        git add + git commit -m "odysseus: session dump [date]"
```

---

## Overseer Deep Dive

Overseer enforces ROADMAP, TASKS, FEATURES, METRICS as MD files in every repo. Since the whole workspace is mounted, Odysseus can:

1. Read `workspace/<repo>/ROADMAP.md` directly — no API needed
2. Identify stalled PRs, blocked tasks, missing files
3. Write missing docs via shell tool, commit, push
4. Trigger builds/tests via Docker socket or shell
5. Eventually: spawn a Claude Code loop to handle a specific task autonomously

**The weekly ops loop:**
```
Sunday 9am cron:
→ For each repo in workspace:
   → Read ROADMAP.md, TASKS.md, FEATURES.md
   → Check GitHub via MCP: open PRs, failing CI, vuln alerts
   → Score health
   → Create Odysseus todos for anything needing action
   → Write summary to stash/ops/YYYY-MM-DD-weekly.md
→ Synthesize cross-repo priorities into one "this week" doc
```

This is the async ops day you're describing — except Odysseus runs it automatically, surfaces the prioritized list, and you just approve and execute (or let it execute).

---

## The Three NeonDBs

Only 3 repos have NeonDB instances: **overseer**, **vhs**, **kryptos**. Worth noting because:
- Odysseus can query them directly via shell tool (psql or Python)
- Overseer's Neon has repo health scores — queryable without the UI
- VHS Neon has the collection data — Odysseus can read/write records
- Kryptos Neon has cipher analysis state — feed into research tasks

When you're ready to hook these up, the pattern is the same: store connection strings in Odysseus memory (encrypted), agent queries via shell when needed.

---

## Priority Connection Order (Revised)

| # | What | Why |
|---|---|---|
| 1 | **Stash session-dump task** | Immediate, zero setup, every chat becomes permanent knowledge |
| 2 | **GitHub MCP server** | All repos' PRs, CI, issues in Odysseus agent chat — fuels the overseer loop |
| 3 | **Overseer workspace read + weekly ops cron** | Agent reads ROADMAP/TASKS/FEATURES directly, creates prioritized task list |
| 4 | **Docker socket health monitor** | Agent-board containers + Odysseus itself; health checks, auto-restart |
| 5 | **Agent-board tool webhooks** | tool-content-gen and tool-website output → Odysseus notes |
| 6 | **fire API polling** | Eventually — financial briefing context |
| 7 | **VHS + NeonDB** | When active dev loop resumes |
| 8 | **opencut-classic evaluation** | When you've had time to play with it |

