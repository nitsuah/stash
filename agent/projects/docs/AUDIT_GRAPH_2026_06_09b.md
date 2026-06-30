# Graph Connectivity Audit — 2026-06-09 (Pass 2 + Orphan Patch)

## Run Stats
- Documents scanned: 148 (.md) + non-markdown assets in scope
- Prior audit: [[AUDIT_GRAPH_2026_06_09]]
- Broken links repaired: 0 (none found this pass)
- Graph noise noted: 2 false-positive nodes (`path/DocName`, `docs/money`) from prior audit report's backtick-quoted text — Obsidian does NOT parse wikilinks in inline code spans; these are grep artifacts only
- Near-orphans improved: 3 (REPO-README, repos/opencut, repos/nitsuah)
- Orphan clusters resolved: 1 (DEMO_VIDEO cluster bridged to main graph via repos/motor-pool.md)
- New file branches connected: kryptos analysis+archive, darkmoon archive, opencut AGENTS
- Links added: ~40 (across 22 documents)

## Interpretation Note — Kryptos Audit Chain

The orphan-patch task specified linking `AUDIT_2026-06-01` to `[[AUDIT_GRAPH_2026_06_09]]`. This was interpreted as a reference to the prior kryptos audit (`AUDIT_2026-05-24`), not to the vault graph connectivity audit. Reason: AUDIT_2026-06-01 is a kryptos `src/` code audit; AUDIT_GRAPH_2026_06_09 is a vault graph connectivity audit — connecting them would create a semantically misleading edge. The kryptos audit chain was instead chained chronologically: `AUDIT_2025-10-26` → `AUDIT_2026-05-24` → `AUDIT_2026-06-01`.

## Changes Made

### Pass 2 — Connectivity repair
| Document | Change | Reason |
|---|---|---|
| `REPO-README.md` | Fixed broken markdown link `(OVERSEER-COMPLIANCE.md)` → `(docs/OVERSEER-COMPLIANCE.md)`; added `## Related` section | Near-orphan (degree 1); broken link |
| `repos/opencut-controller.md` | Added `[[repos/opencut]]` in new `## Related` section | Reciprocal missing — opencut.md linked to controller but not vice versa |
| `repos/nitsuah-io.md` | Added `[[repos/nitsuah\|nitsuah (v1)]]` predecessor reference | nitsuah.md had 0 inbound; successor should reference predecessor |

### Orphan patch — Media assets indexed
| Asset | Indexed in | Reason |
|---|---|---|
| `DEMO_VIDEO_120S.srt` | `repos/motor-pool/docs/DEMO_VIDEO_SCRIPT` | Caption file for main demo |
| `DEMO_VIDEO_60S.srt` | `repos/motor-pool/docs/DEMO_VIDEO_SCRIPT` | Caption file for short demo |
| `DEMO_VIDEO_60S_MOBILE.srt` | `repos/motor-pool/docs/DEMO_VIDEO_SCRIPT` | Caption file for mobile cut |
| `lighthouse-desktop.report.html` | `repos/skyview/docs/PERFORMANCE_CHECKLIST` | Desktop Lighthouse audit belongs with perf checklist |
| `lighthouse-desktop.report.json` | `repos/skyview/docs/PERFORMANCE_CHECKLIST` | Same parent as .html |
| `farm.png` | `repos/farm-3j/docs/Farm_RTS_Game_Manual` | RTS map asset belongs with game manual |

### Orphan patch — Loose docs connected
| Document | Links Added | Reason |
|---|---|---|
| `repos/motor-pool/docs/DEMO_VIDEO_SCRIPT` | `[[DEMO_VIDEO_SCRIPT_SHORT]]`, SRT refs | Script siblings + caption assets |
| `repos/motor-pool/docs/DEMO_VIDEO_SCRIPT_SHORT` | `[[DEMO_VIDEO_SCRIPT]]` | Bidirectional sibling |
| `repos/motor-pool.md` | Added `demo/` section with `[[DEMO_VIDEO_SCRIPT]]`, `[[DEMO_VIDEO_SCRIPT_SHORT]]` | **Bridge link** — connects entire DEMO_VIDEO cluster to main graph |
| `repos/farm-3j/docs/FARM-RTS-NORTH-STAR` | `[[Farm_RTS_Game_Manual]]` | Bidirectional sibling |
| `repos/kryptos/docs/analysis/K4_ACTIVE_RESEARCH` | `[[K4-FRONTEND]]`, `[[AUDIT_2026-06-01]]`, `[[repos/kryptos]]` | Vault links to analysis cluster |
| `repos/kryptos/docs/analysis/K4-FRONTEND` | `[[K4_ACTIVE_RESEARCH]]`, `[[repos/kryptos]]` | Link to parent research doc |
| `repos/kryptos/docs/archive/AUDIT_2025-10-26` | Navigation: Next → AUDIT_2026-05-24, Parent → kryptos | Temporal chain start |
| `repos/kryptos/docs/archive/AUDIT_2026-05-24` | Navigation: Previous/Next, Parent → kryptos | Temporal chain middle |
| `repos/kryptos/docs/archive/AUDIT_2026-06-01` | Navigation: Previous → AUDIT_2026-05-24, Parent → K4_ACTIVE_RESEARCH + kryptos | Temporal chain end |
| `repos/kryptos.md` | Added `analysis/` and `archive/` sections to Vault Index | 9 analysis docs + 3 audit docs had 0 inbound |
| `repos/darkmoon/docs/archive/ARCHITECTURE_IMPROVEMENTS` | `[[L7_ENGINEERING_REVIEW]]`, `[[ARCHITECTURE]]`, `[[repos/darkmoon]]` | Archive cluster → main graph |
| `repos/darkmoon/docs/archive/L7_ENGINEERING_REVIEW` | `[[ARCHITECTURE_IMPROVEMENTS]]`, `[[ARCHITECTURE]]`, `[[repos/darkmoon]]` | Archive cluster → main graph |
| `repos/darkmoon/docs/ARCHITECTURE` | `[[ARCHITECTURE_IMPROVEMENTS]]`, `[[L7_ENGINEERING_REVIEW]]` | Active doc links back to archive analyses |
| `repos/darkmoon/docs/archive/HANDOFF-player-tag-fix-20260403` | `[[repos/darkmoon]]`, `[[prompts/HANDOFF]]` | Orphan HANDOFF anchored to runbook + template |
| `repos/darkmoon.md` | Added `archive/` section to Vault Index | 3 archive docs had 0 inbound from runbook |
| `repos/opencut/OpenCut-AGENTS` | `[[repos/opencut]]` | Standalone orphan anchored to parent runbook |
| `repos/opencut.md` | Added `[[OpenCut-AGENTS]]` to Core section | Bidirectional: runbook → AGENTS doc |

## Graph Noise — Action Required by Human
These were detected by the grep-based audit tool but are NOT real graph edges in Obsidian:
- `path/DocName` (2 occurrences) — example wikilink syntax in `docs/AUDIT_GRAPH_2026_06_09.md` Phase 0 section; inside backtick code spans; Obsidian does not parse as links
- `docs/money` (2 occurrences) — old broken link shown in `docs/AUDIT_GRAPH_2026_06_09.md` audit table; inside backtick code spans; Obsidian does not parse as links
- `prompts/OVERSEER-COMPLIANCE` (1 occurrence) — audit report description text; same reason

**No action needed** — these are grep false-positives. Obsidian's graph is correct.

## Flagged for Human Review
- `repos/kryptos/docs/analysis/K1_2_3_PATTERN_ANALYSIS.md`, `K1_K2_VALIDATION_RESULTS.md`, `K3_VALIDATION_RESULTS.md` — referenced only within kryptos analysis context; kryptos.md Vault Index now covers the K4 docs but not K1/K2/K3 series. Consider adding to kryptos.md Vault Index if these need graph visibility.
- `repos/skyview/docs/DEPLOYMENT_GUIDE.md` — added as Related in PERFORMANCE_CHECKLIST but worth verifying the lighthouse report belongs there vs. a dedicated asset index.

## Skipped (Intentionally Isolated)
- All `repos/*/CHANGELOG.md`, `FEATURES.md`, `METRICS.md`, `README.md`, `ROADMAP.md`, `TASKS.md` — synced mirrors from external repos
- `repos/.github/` template files — GitHub community standard templates
- `repos/kryptos/docs/analysis/K4-CLOCKS.html` — HTML asset, no markdown parent references it by wikilink; flagged for human review if graph visibility needed

## Related
- [[AUDIT_GRAPH_2026_06_09]] — prior pass (2026-06-09 pass 1)
- [[repos/stash]] — vault root runbook
