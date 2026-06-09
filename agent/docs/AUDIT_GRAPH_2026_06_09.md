# Graph Connectivity Audit — 2026-06-09

## Run Stats
- Documents scanned: 148
- Broken links repaired: 3
- True orphans found: 4 → resolved: 4, flagged: 0
- Near-orphans improved: 1 (HANDOFF.md — 0 outbound → 3 outbound)
- Orphaned assets found: 0
- Links added: 14 (across 8 documents)
- Compared against prior audit: none

## Phase 0: Convention Summary

Sampled `AGENT-MAIN.md`, `prompts/PMO.md`, `repos/agent-board.md`, `repos/stash.md`.

- **Link style**: `[[path/DocName|Alias]]` inline prose; `[[path/DocName]]` for bare refs. Paths relative to vault root, no `.md` extension.
- **Naming**: UPPER_SNAKE_CASE for docs/prompts; Title Case for projects; kebab-case for repo subdoc files.
- **Link placement**: Inline in prose where a natural anchor exists; `## Related` section appended when no prose anchor exists.
- **No YAML front matter** used for links.
- **README.md** uses standard markdown links `[text](path)` — not wikilinks. This is an index/navigation file, kept as-is.

## Changes Made

| Document | Links Added | Reason |
|---|---|---|
| `prompts/Growth.md` | Fixed `[[docs/money]]` → `[[docs/MONEY-MAKERS]]` | Broken link — `docs/money.md` deleted, renamed to `MONEY-MAKERS.md` |
| `repos/stash.md` | Fixed `[[docs/money]]` → `[[docs/MONEY-MAKERS]]`; added `[[projects/Builder]]`, `[[projects/Career]]`, `[[projects/Finance]]` | Broken link repair + anchored personal agent orphans in Vault Index |
| `prompts/QA.md` | Fixed `[[prompts/OVERSEER-COMPLIANCE]]` → `[[docs/OVERSEER-COMPLIANCE]]` | Ghost link — `prompts/OVERSEER-COMPLIANCE.md` does not exist; file lives at `docs/` |
| `projects/Builder.md` | `[[projects/Career]]`, `[[projects/Finance]]`, `[[docs/MONEY-MAKERS]]` | True orphan — 0 in/out wikilinks; connected to sibling personal agents |
| `projects/Career.md` | `[[projects/Finance]]`, `[[projects/Builder]]` | True orphan — 0 in/out wikilinks; connected to sibling personal agents |
| `projects/Finance.md` | `[[projects/Career]]`, `[[projects/Builder]]` | True orphan — 0 in/out wikilinks; connected to sibling personal agents |
| `docs/MONEY-MAKERS.md` | `[[prompts/Growth]]`, `[[docs/GAPS_AND_IMPROVEMENT_PLAN]]`, `[[projects/Builder]]` | True orphan (inbound broken refs all pointed to deleted `docs/money`); now anchored |
| `prompts/HANDOFF.md` | `[[prompts/PMO]]`, `[[projects/Intake]]`, `[[prompts/OPS]]`, `[[prompts/QA]]` | 12 inbound / 0 outbound — template with no graph edges out; added Pipeline Context section |

## Flagged for Human Review
None — all candidates had clear, confident connection targets.

## Stub Candidates
None identified in this pass.

## Orphaned Assets
None — no `.png`, `.html`, or other non-markdown assets present in the vault root or docs.

## Skipped (Intentionally Isolated)

| Document | Reason |
|---|---|
| `repos/*/CHANGELOG.md`, `FEATURES.md`, `METRICS.md`, `README.md`, `ROADMAP.md`, `TASKS.md` | Synced mirrors from external repos. Each is linked-to by its parent runbook (`repos/<name>.md`). Adding wikilinks to synced files would create noise and drift on re-sync. |
| `repos/.github/CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `PULL_REQUEST_TEMPLATE.md`, `SECURITY.md`, `SUPPORT.md` | GitHub community standard templates. Intentionally isolated by design. |
| `Nexus/data/` | Contains `conversations/`, `tasks/`, `workspaces/` — runtime data directories with no `.md` files; not part of the knowledge graph. |

## Tenuously Connected Clusters
- `repos/nitsuah.md` connects to the main graph only via its single outbound link `[[repos/nitsuah-io]]` and 1 inbound from `repos/stash.md` Vault Index. Degree = 2. Acceptable — it's a legacy repo with an explicit "superseded by" note.
- `opencut` / `opencut-controller` pair: both have internal cross-links and connect to the main graph via PMO references. Degree adequate.

## Related
- [[repos/stash]] — vault root runbook; Vault Index updated in this pass
- [[docs/GAPS_AND_IMPROVEMENT_PLAN]] — related planning document
