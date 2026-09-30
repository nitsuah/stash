# obn-import — 2026-09-30

First run of this checker: eng-loc reporting is overdue (14d, cadence 9d) and cloud/week-vuln has never been produced; everything else is within cadence.

## 1. Stale notes
- Non-dated notes: `agent/notes/eng-loc-notes.md` — last changed 2026-09-24 (6 days). Not stale (30d threshold).
- Newest daily note: `2026-09-27.md` (3 days old). Not flagged (threshold is >3 days).

## 2. Missing reports (by cadence)
- **cloud/daily-brief** (4d): last 2026-09-30 (today). OK.
- **cloud/week-vuln** (9d): no directory/files found anywhere in the repo. Never produced — flag for setup or retirement.
- **eng-loc** (9d): newest report is `eng-loc-skyview-2026-09-16.md` / `eng-loc-darkmoon-2026-09-16.md`, 14 days old. **OVERDUE.**
- **eng-mini** (9d): newest `eng-mini-fire-2026-09-24.md` / `eng-mini-games-2026-09-24.md` / `eng-mini-stash-2026-09-24.md`, 6 days old. OK.
- **sotu-data** (9d): `agent/reports/sotu/sotu-data.json` + `sotu-2026-W39.md`, last touched 2026-09-28, 2 days old. OK.
- **tire-kick** (35d): `tire-kick-2026-09-24.md`, 6 days old. OK.
- **pmo-audit** (35d): `pmo-audit-2026-09-24.md`, 6 days old. OK.
- **usage-report** (35d): `usage-report-2026-09.md`, created 2026-09-24, 6 days old. OK.
- **rsi-report** (35d): `rsi-report-2026-09.md`, created 2026-09-24, 6 days old. OK.

## 3. Placeholder prompts
None. All `agent/prompts/*.md` files are 25+ lines (smallest: AUTO.md and Growth.md at 25 lines).

## 4. Untracked repos (60+ days with no report)
None. All 17 repos in `scope.md`'s Tracked table appear in a report within the last 6 days — `avatar` and `osrs` have no eng-loc/eng-mini reports but are both covered in `pmo-audit-2026-09-24.md` and `tire-kick-2026-09-24.md`.

## 5. Follow-ups
`agent/jobs/` does not exist — skipped.

## 6. Vault graph (`find-orphans.py --check`)
```
vault: /home/user/stash/agent
notes: 479  orphans (no links in or out): 1  unreferenced (links out, none in): 2
reachable from VAULT-MAP: 475  unreachable: 4  by hops: 0:1, 1:64, 2:213, 3:170, 4+:27
star hubs (40+ out-links): VAULT-MAP.md (80)
unresolved links (ghost nodes): 0 in 0 notes
attachments: 25  unlinked (loose dots in the graph): 3  -> reports/sotu/priorities.json, reports/sotu/sotu-data.json, scripts/sotu-page.html

orphans by folder:
     1  reports

FAIL: 1 note(s) outside the repo mirrors have no path from the vault home:
  reports/cloud/daily-brief/daily-brief-2026-09-30.md
```
