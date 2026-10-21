---
kind: cloud/obn-import
date: 2026-10-21
---

# obn-import — 2026-10-21

> 🧭 ← [[reports/cloud/obn-import/obn-import-2026-10-15|2026-10-15]] <!-- nav -->

The newest daily note is 6 days old (2026-10-15) and the vault graph FAIL count is back up (4 → 9 unreachable reports); report cadences are otherwise on time.

## 1. Stale notes
- Non-dated notes: `agent/notes/eng-loc-notes.md`, last changed 2026-10-08 (13 days). Not stale.
- Newest daily note: `2026-10-15.md`, **6 days old, over the 3-day threshold**. The 10-16 and 10-21 notes exist only on open PRs #253 and #255.

## 2. Missing reports (by cadence)
- **cloud/daily-brief** (4d): `daily-brief-2026-10-21.md`, today. OK.
- **cloud/week-vuln** (9d): `week-vuln-2026-10-15.md`, 6 days. OK.
- **eng-loc** (9d): newest 2026-10-15 (6 days). OK at type level. Per repo, `deployer` (07-29), `darkmoon`, `fire` and `skyview` (09-16) and `avatar` (never) have the oldest or no eng-loc report.
- **eng-mini** (9d): newest 2026-10-14 (7 days). OK.
- **sotu-data** (9d): `sotu-2026-W43.md`, 2026-10-21. OK.
- **tire-kick** (35d): 2026-09-30 (21 days). OK.
- **pmo-audit** (35d): 2026-10-01 (20 days). OK.
- **usage-report** (35d): 2026-09 (about 21 days). OK.
- **rsi-report** (35d): 2026-10. OK.

## 3. Placeholder prompts
None. All `agent/prompts/*.md` files are 10+ lines.

## 4. Untracked repos (60+ days with no report)
None. `deployer`'s only eng-loc report is 84 days old, but it is named in tire-kick (2026-09-30) and SOTU W43, so it is not report-less.

## 5. Follow-ups
`agent/jobs/` does not exist — skipped.

## 6. Vault graph (`find-orphans.py --check`)
```
vault: /home/user/stash/agent
notes: 613  orphans (no links in or out): 8  unreferenced (links out, none in): 16
reachable from VAULT-MAP: 589  unreachable: 24  by hops: 0:1, 1:68, 2:245, 3:221, 4+:54
star hubs (40+ out-links): VAULT-MAP.md (88)
unresolved links (ghost nodes): 0 in 0 notes
attachments: 29  unlinked (loose dots in the graph): 5  -> reports/sotu/priorities.json, reports/sotu/sotu-data.json, scripts/sotu-page.html, scripts/vault-graph-gif.js, scripts/visual-board-page.html

orphans by folder:
     8  reports

FAIL: 9 note(s) outside the repo mirrors have no path from the vault home:
  reports/cloud/daily-brief/daily-brief-2026-10-15.md
  reports/cloud/daily-brief/daily-brief-2026-10-16.md
  reports/cloud/daily-brief/daily-brief-2026-10-21.md
  reports/cloud/week-vuln/week-vuln-2026-10-15.md
  reports/eng-loc-kryptos-2026-10-15.md
  reports/eng-loc-vhs-2026-10-15.md
  reports/eng-loc-vigil-2026-10-15.md
  reports/sotu/sotu-2026-W42.md
  reports/sotu/sotu-2026-W43.md
```
