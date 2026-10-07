---
up: "[[repos/fire]]"
title: "fire · README"
source: https://github.com/nitsuah/fire/blob/main/skills/README.md
kind: repo-doc
repo: fire
---

# Claude skills

> 🧭 [fire](../README.md) · [Features](../docs/FEATURES.md) · [Roadmap](../docs/ROADMAP.md) · [Tasks](../docs/TASKS.md) · [Changelog](../docs/CHANGELOG.md) · [Metrics](../docs/METRICS.md) <!-- nav -->

## `fire-coach`

A [Claude skill](https://docs.claude.com/en/docs/claude-code/skills) that turns
Claude into a FIRE coach for this app. It combines:

- your live numbers from the read-only [MCP server](../README.md#mcp-server-claude-integration),
- a FIRE playbook covering the 4% rule, savings rate, order of operations,
  taxes, sequence risk, CDs and what to do when income stops
  ([references/financial-playbook.md](fire-coach/references/financial-playbook.md)),
- a guide to every tab, Chaos mode and layout customization
  ([references/app-guide.md](fire-coach/references/app-guide.md)).

### Install

Claude Code (personal, all projects):

```bash
mkdir -p ~/.claude/skills && cp -r skills/fire-coach ~/.claude/skills/
```

Just this project:

```bash
mkdir -p .claude/skills && cp -r skills/fire-coach .claude/skills/
```

Claude.ai / Claude Desktop: zip the `fire-coach` folder and upload it under
**Settings → Capabilities → Skills**.

Then ask things like *"How am I tracking toward FIRE?"*, *"What happens if I
lose my job?"*, *"Is a 4% withdrawal rate safe for me?"* or *"How do I pin the
CD Ladder to my dashboard?"*. Connect the `fire-tracker` MCP server
(`.mcp.json`) so the answers use your real data.

The skill is educational, not personalized investment advice.
