# auto-apply-plugin

> Reviewed: 2026-06-25

## Overview

"Apply Workspace" — Chrome MV3 extension for local-first AI-assisted job applications. Stores profile locally, detects ATS forms, reads JDs from the page, generates tailored answers via user's own Gemini API key, and requires review before form fill. Zero server, zero subscription.

## Current Goals / Roadmap Focus

**Q2 2026 (in progress):**
- Polish popup into a true job-workspace view (tracker lanes, bubble cards, DnD, pay controls, verdict dropdown)
- `apply-bot` → "Apply Workspace" rebrand pass (copy, icons, docs)
- Picker-style job detail capture from current page or pasted JD

**Q3 2026 (in progress):**
- Expand job search to additional sources, on-ATS-page parsing depth, OAuth job source

**Q4 2026 (exploratory):**
- LinkedIn + Indeed multi-site scraping and alerting
- Identity-provider imports (Google, ID.me) for profile bootstrapping
- Interview prep mode (local, Gemini-backed behavioral/technical Q&A)
- Application analytics panel (response rate by source, salary effectiveness)

## Open P0/P1 Tasks

- [/] P1 — Polish popup workspace view (in progress; remaining: refresh screenshots gallery, monitor FE feedback)
- [/] P1 — Keep local-first autofill and privacy controls trustworthy (ongoing monitoring)
- [/] P2 — `apply-bot` rebrand pass (partial; copy done, icons/docs pending)
- [/] P1 — Multi-source job search aggregation (shipped 9 keyless + 4 keyed sources; remaining: on-ATS parsing depth, tracker indexing, OAuth job source)

**Deferred/blocked (FE-pass follow-ups):**
- [ ] UX Audit batch 2 (medium priority): expanded card modal, popup/standalone sync, narrative card overflow, memory delete confirm
- [ ] Wire `axe-core` into Playwright e2e — **BLOCKED**: needs `npm install` to update lock file; npm not available in dev environment
- [ ] a11y burndown: keyboard DnD alternative, color-contrast verification, focus-ring audit

## Blockers

- `axe-core` Playwright integration blocked by no npm in dev environment (requires Docker workaround)
- OAuth job sources (LinkedIn partner API is partner-gated; scraping is the current path)

## Recent Changes (Unreleased)

- Tracker module split into focused files under `popup/tracker/`
- CSV import support for tracker history
- ATS receiver auto-recovery path (retries content-script injection)
- Memory controls: edit, ignore, restore, remove
- Popup workspace UX polished: wider layout, tighter controls, grouped editor sections
- Job search shipped: 9 keyless sources (Remotive, Arbeitnow, The Muse, Remote OK, Jobicy, Working Nomads, HN Who's Hiring, We Work Remotely, remote.co) + 4 keyed (Adzuna, USAJOBS, Reed, Jooble) + LinkedIn session source
- LinkedIn OIDC profile import (BYO OAuth — user supplies client ID/secret)
- AI Summarize/Clean Up buttons on JD field, tracker cards, job search results, preview answers
- Pay filter with annual/hourly toggle, dual slider; "hide unknown-salary" toggle
- Per-source filter chips; source selection + pay filter persist to `chrome.storage.local`
