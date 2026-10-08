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

Ask: *"How am I tracking toward FIRE?"*, *"What happens if I lose my job?"*,
*"Is a 4% withdrawal rate safe for me?"* or *"How do I pin the CD Ladder to my
dashboard?"*

## `reseller-autopilot`

A low-touch reselling workflow built around the **Side Hustle Hub**. It prices
items from sold comps, compares the net after fees on eBay, Etsy, Mercari,
Poshmark and FB Marketplace, drafts platform-specific listings for you to post
and cross-list yourself, triages a pile of
stuff into sell, bundle and donate, and sets up a weekly "list and forget" routine.
It reads `get_side_gig_income` / `get_side_gig_tax_summary` for profit and tax
checks.

- [references/platform-fees.md](reseller-autopilot/references/platform-fees.md):
  fees, fit, and the net formula for each platform.
- [references/listing-playbook.md](reseller-autopilot/references/listing-playbook.md):
  titles, descriptions, photos, price drops and the weekly routine.

Ask: *"What's this worth and where should I sell it?"*, *"Turn these 12 items into
listings"*, *"Is this flip worth it?"*

## `passive-income-lab`

Finds and sizes low-touch ("AFK") income streams such as cash yield and CD ladders,
digital downloads on Etsy, print-on-demand, renting out gear and reselling. It
checks the user's runway first (no capital at risk when runway is short), shows
how much each stream moves the FIRE date, and writes a 30-day launch plan.

- [references/streams.md](passive-income-lab/references/streams.md): eight
  streams with hours, capital, realistic year-one ranges, risks and red flags.
- [references/fire-math.md](passive-income-lab/references/fire-math.md): converts
  monthly income into a lower FIRE number, and covers taxes.

Ask: *"How can I make $300 a month without much time?"*, *"How much sooner could
I retire with an Etsy shop?"*, *"Give me a 30-day plan to start."*

### Install

Claude Code (personal, all projects):

```bash
mkdir -p ~/.claude/skills && cp -r skills/fire-coach skills/reseller-autopilot skills/passive-income-lab ~/.claude/skills/
```

Just this project:

```bash
mkdir -p .claude/skills && cp -r skills/fire-coach skills/reseller-autopilot skills/passive-income-lab .claude/skills/
```

Claude.ai / Claude Desktop: zip each skill folder and upload it under
**Settings → Capabilities → Skills**.

**Live data (the `fire-tracker` MCP server)** depends on the client:

- **Claude Code:** `.mcp.json` at the repo root connects it automatically when
  you start Claude Code in this directory.
- **Claude Desktop:** add a local server to `claude_desktop_config.json` that runs
  `node app/mcp-server.mjs` from your fire checkout (see
  [MCP Server](../README.md#mcp-server-claude-integration)).
- **claude.ai:** the server runs locally over stdio, so claude.ai can't reach it.
  The skills still work there and ask you for the numbers they need.

The skills are educational, not personalized investment or tax advice.
