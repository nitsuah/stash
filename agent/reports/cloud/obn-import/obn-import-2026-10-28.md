---
kind: cloud/obn-import
date: 2026-10-28
---

# obn-import — 2026-10-28

> 🧭 ← [[reports/cloud/obn-import/obn-import-2026-10-21|2026-10-21]] <!-- nav -->

One cadence miss: cloud/daily-brief is 5 days old (limit 4). The newest daily note is current, and the vault graph now has 109 broken links plus 4 unreachable notes.

## 1. Stale notes
- Non-dated notes: only `agent/notes/eng-loc-notes.md`, last changed 2026-10-08 (20 days). Not stale.
- Newest daily note: `2026-10-26.md`, 2 days old. OK.

## 2. Missing reports (by cadence)
- **cloud/daily-brief** (4d): newest `daily-brief-2026-10-23.md`, **5 days — OVERDUE**.
- **cloud/week-vuln** (9d): 2026-10-22 (6 days). OK.
- **eng-loc** (9d): 2026-10-22 (6 days). OK.
- **eng-mini** (9d): 2026-10-21 (7 days). OK.
- **sotu-data** (9d): `sotu-2026-W43.md`, 2026-10-24 (4 days). OK.
- **tire-kick** (35d): 2026-09-30 (28 days). OK.
- **pmo-audit** (35d): 2026-10-01 (27 days). OK.
- **usage-report** (35d): 2026-09, committed 2026-10-22 (6 days). OK.
- **rsi-report** (35d): 2026-10, committed 2026-10-22 (6 days). OK.

## 3. Placeholder prompts
None. All `agent/prompts/*.md` files are 10+ lines.

## 4. Untracked repos (60+ days with no report)
None. `deployer`'s newest eng-loc report is 2026-07-29 (91 days), but it is still named in tire-kick (2026-09-30) and SOTU W43, so it is not report-less.

## 5. Follow-ups
`agent/jobs/` does not exist — skipped.

## 6. Vault graph (`find-orphans.py --check`)
```
notes: 675  orphans (no links in or out): 3  unreferenced (links out, none in): 30
reachable from VAULT-MAP: 615  unreachable: 60  by hops: 0:1, 1:70, 2:247, 3:224, 4+:73
star hubs (40+ out-links): VAULT-MAP.md (90)
unresolved links (ghost nodes): 109 in 1 notes
attachments: 94  unlinked (loose dots in the graph): 70

FAIL: 109 broken link(s) in notes outside repo mirrors and MM source tree (fix with scripts/fix-doc-links.py --vault):
  projects/MM-hub.md: (109 links under projects/MM/ — audit-scanner node_modules/reports, pack-factory out*/, skill-pack/dist, template-pack/dist)

FAIL: 4 note(s) outside repo mirrors and MM source tree have no path from the vault home:
  notes/2026-10-26.md
  projects/ISSUE-QUEUE-PLAN.md
  projects/MM-hub.md
  reports/cloud/daily-brief/daily-brief-2026-10-23.md
```
(The 109-link FAIL list is abbreviated here; all are in `projects/MM-hub.md`.)
