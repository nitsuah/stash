---
kind: cloud/obn-import
date: 2026-10-15
---

# obn-import — 2026-10-15

> 🧭 ← [[reports/cloud/obn-import/obn-import-2026-10-07|2026-10-07]] · [[reports/cloud/obn-import/obn-import-2026-10-21|2026-10-21]] → <!-- nav -->

Seven tracked repos (darkmoon, deployer, fire, kryptos, vigil, skyview, vhs) are overdue on eng-loc (stuck on 2026-10-01 runs, 14 days old), `avatar` has never had an eng-loc report and `deployer` has never had an eng-mini report, and the vault graph's unreachable-report FAIL count has dropped sharply (24 → 4) since the last check.

## 1. Stale notes
- Non-dated notes: `agent/notes/eng-loc-notes.md` — last changed 2026-10-01 (14 days). Not stale (30d threshold).
- Newest daily note: `2026-10-14.md` (1 day old). OK — well under the 3-day threshold.

## 2. Missing reports (by cadence)
- **cloud/daily-brief** (4d): last `daily-brief-2026-10-14.md`, 1 day old. OK.
- **cloud/week-vuln** (9d): last `week-vuln-2026-10-08.md`, 6 days old. OK.
- **eng-loc** (9d): **OVERDUE** for 7 of 17 tracked repos — all stuck on the 2026-10-01 batch, 14 days old: `darkmoon`, `deployer`, `fire`, `kryptos`, `vigil` (still filed under old name `overseer`), `skyview`, `vhs`. Also **`avatar` has no eng-loc report at all** (never run for this repo). Current (≤8 days): `motor-pool`, `ats-fill`, `bb-mcp`, `farm-3j`, `games`, `gcp`, `nitsuah-io`, `osrs`, `stash`.
- **eng-mini** (9d): all 17 tracked repos current (≤8 days) **except `deployer`, which has no eng-mini report at all** (never run for this repo).
- **sotu-data** (9d): `sotu-2026-W41.md` / `sotu-data.json`, last touched 2026-10-14, 1 day old. OK.
- **tire-kick** (35d): `tire-kick-2026-09-30.md`, 8 days old. OK.
- **pmo-audit** (35d): `pmo-audit-2026-10-01.md`, 14 days old. OK.
- **usage-report** (35d): `usage-report-2026-09.md`, 8 days old. OK.
- **rsi-report** (35d): `rsi-report-2026-10.md`, 8 days old. OK.

## 3. Placeholder prompts
None. All `agent/prompts/*.md` files are 10+ lines.

## 4. Untracked repos (60+ days with no report)
None. All 17 repos in `scope.md`'s Tracked table appear in a report within the last 14 days — `deployer` is the oldest (eng-loc only, via `eng-loc-deployer-2026-07-29.md`), still well under the 60-day threshold.

## 5. Follow-ups
`agent/jobs/` does not exist — skipped.

## 6. Vault graph (`find-orphans.py --check`)
```
vault: /home/user/stash/agent
notes: 593  orphans (no links in or out): 1  unreferenced (links out, none in): 13
reachable from VAULT-MAP: 579  unreachable: 14  by hops: 0:1, 1:68, 2:243, 3:217, 4+:50
star hubs (40+ out-links): VAULT-MAP.md (88)
unresolved links (ghost nodes): 0 in 0 notes
attachments: 29  unlinked (loose dots in the graph): 5  -> reports/sotu/priorities.json, reports/sotu/sotu-data.json, scripts/sotu-page.html, scripts/vault-graph-gif.js, scripts/visual-board-page.html

orphans by folder:
     1  reports

FAIL: 4 note(s) outside the repo mirrors have no path from the vault home:
  reports/cloud/daily-brief/daily-brief-2026-10-14.md
  reports/eng-mini-fire-2026-10-14.md
  reports/eng-mini-kryptos-2026-10-14.md
  reports/eng-mini-vigil-2026-10-14.md
```
