---
kind: cloud/obn-import
date: 2026-10-07
---

# obn-import — 2026-10-07

All report cadences are now within schedule (previous run's week-vuln/eng-loc overdue flags are resolved), but the newest daily note is 6 days old and the vault graph's unreachable-report count has grown sharply (1 → 24 FAILs) since the last check.

## 1. Stale notes
- Non-dated notes: `agent/notes/eng-loc-notes.md` — last changed 2026-09-25 (12 days). Not stale (30d threshold).
- Newest daily note: `2026-10-01.md` (6 days old). **Flagged** — exceeds the 3-day threshold.

## 2. Missing reports (by cadence)
- **cloud/daily-brief** (4d): last `daily-brief-2026-10-06.md`, 1 day old. OK.
- **cloud/week-vuln** (9d): last `week-vuln-2026-10-01.md`, 6 days old. OK (was overdue last run; now current).
- **eng-loc** (9d): newest `eng-loc-bb-mcp-2026-10-01.md` / `eng-loc-games-2026-10-01.md` / `eng-loc-osrs-2026-10-01.md`, 6 days old. OK (was overdue last run; now current).
- **eng-mini** (9d): newest batch dated 2026-10-02 (e.g. `eng-mini-games-2026-10-02.md`), 6 days old. OK.
- **sotu-data** (9d): `sotu-2026-W40.md` / `sotu-data.json`, last touched 2026-09-30, 7 days old. OK.
- **tire-kick** (35d): `tire-kick-2026-09-24.md`, 13 days old. OK.
- **pmo-audit** (35d): `pmo-audit-2026-10-01.md`, 6 days old. OK.
- **usage-report** (35d): `usage-report-2026-09.md`, last touched 2026-09-25, 12 days old. OK.
- **rsi-report** (35d): `rsi-report-2026-09.md`, last touched 2026-09-25, 12 days old. OK.

## 3. Placeholder prompts
None. All `agent/prompts/*.md` files are 25+ lines (smallest: `AUTO.md` and `Growth.md` at 25 lines).

## 4. Untracked repos (60+ days with no report)
None. All 17 repos in `scope.md`'s Tracked table appear in a report within the last 12 days — `deployer` is the oldest at 2026-09-25 (`pmo-audit`/`tire-kick`/`usage-report`/`rsi-report` era), still well under the 60-day threshold.

## 5. Follow-ups
`agent/jobs/` does not exist — skipped.

## 6. Vault graph (`find-orphans.py --check`)
```
vault: /home/user/stash/agent
notes: 538  orphans (no links in or out): 8  unreferenced (links out, none in): 20
reachable from VAULT-MAP: 509  unreachable: 29  by hops: 0:1, 1:67, 2:222, 3:191, 4+:28
star hubs (40+ out-links): VAULT-MAP.md (86)
unresolved links (ghost nodes): 4 in 1 notes
attachments: 27  unlinked (loose dots in the graph): 4  -> reports/sotu/priorities.json, reports/sotu/sotu-data.json, scripts/sotu-page.html, scripts/vault-graph-gif.js

orphans by folder:
     8  reports

unresolved links by folder:
     4  repos/fire

FAIL: 24 note(s) outside the repo mirrors have no path from the vault home:
  reports/cloud/daily-brief/daily-brief-2026-10-01.md
  reports/cloud/daily-brief/daily-brief-2026-10-02.md
  reports/cloud/daily-brief/daily-brief-2026-10-05.md
  reports/cloud/daily-brief/daily-brief-2026-10-06.md
  reports/cloud/week-vuln/week-vuln-2026-10-01.md
  reports/eng-loc-bb-mcp-2026-10-01.md
  reports/eng-loc-games-2026-10-01.md
  reports/eng-loc-osrs-2026-10-01.md
  reports/eng-mini-agent-board-2026-10-02.md
  reports/eng-mini-ats-fill-2026-10-02.md
  reports/eng-mini-avatar-2026-10-02.md
  reports/eng-mini-bb-mcp-2026-10-02.md
  reports/eng-mini-darkmoon-2026-10-02.md
  reports/eng-mini-farm-3j-2026-10-02.md
  reports/eng-mini-fire-2026-10-01.md
  reports/eng-mini-games-2026-10-02.md
  reports/eng-mini-gcp-2026-10-02.md
  reports/eng-mini-kryptos-2026-10-01.md
  reports/eng-mini-nitsuah-io-2026-10-02.md
  reports/eng-mini-osrs-2026-10-02.md
  reports/eng-mini-skyview-2026-10-02.md
  reports/eng-mini-stash-2026-10-01.md
  reports/eng-mini-vhs-2026-10-02.md
  reports/eng-mini-vigil-2026-10-02.md
```
