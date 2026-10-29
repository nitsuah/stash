# eng-loc · bb-mcp · 2026-10-29
HEAD: 58c2085da73e2b1d26832bcb3ab86701eb121dac

kind: eng-loc · repo: bb-mcp · tier: T2 (vigil snapshot 2026-10-21) · mode: --report · last commit: 2026-10-28 23:24 -0400

Method: `git ls-files` + per-file `wc -l` on a `--depth 1` clone. Same exclusions as fire. Churn/author history **not available** (shallow clone), marked "assumed: not confirmed". Per-file coverage not measured.

## Inventory Summary
- Code LOC (ts/js, excl. tests/promo/JSON): 9,130
- Test LOC: 6,414 across 30 files. Largest `tests/tools-grade-writeback.test.ts` at 603 LOC, under the threshold.
- Container: `Dockerfile` present.

## Top 10 LOC Files

| # | File | LOC | Lang | Role |
|---|------|-----|------|------|
| 1 | `src/index.ts` | 1,237 | TS | Server bootstrap, OIDC callback, tool invocation, identity checks |
| 2 | `src/tools/admin.ts` | 728 | TS | Admin tool definitions |
| 3 | `src/tools/grade-writeback.ts` | 613 | TS | Grade write-back tools |
| 4 | `src/tools/parent.ts` | 605 | TS | Parent tools |
| 5 | `src/tools/instructor.ts` | 589 | TS | Instructor tools |
| 6 | `src/tools/student.ts` | 515 | TS | Student tools |
| 7 | `src/tools/webhook-tools.ts` | 514 | TS | Webhook tools |
| 8 | `src/schemas.ts` | 427 | TS | Schemas |
| 9 | `src/bb-client.ts` | 410 | TS | Blackboard API client |
| 10 | `src/oidc-auth.ts` | 392 | TS | OIDC auth |

## Risk Rank

- **High — `src/index.ts`**: 1,237 LOC mixing server bootstrap (mTLS/OIDC config check ≈L678), the OIDC callback handler (≈L837, ~48 lines), a tool invocation wrapper (≈L952, ~53 lines), and identity verification (≈L1104, ~62 lines). Mixed concerns in the entry file, so the rationale is structural. Block lengths are approximate.
- **Medium — `src/tools/admin.ts`**: 728 LOC of tool definitions with inline enrollment mapping and an update-payload branch (≈L456). Already split by role, which is a good sign.
- **Medium — `src/tools/grade-writeback.ts`**: 613 LOC with repeated `attemptId` branches (≈L315, ≈L429, ≈L500). `toIsoOrNull` (L18) is a generic helper living in a tool module, a low-risk extraction.
- Others (parent, instructor, student, webhook-tools, schemas, bb-client, oidc-auth): no structural signal recorded this run. Role-split layout is already in place.

## Refactor Opportunities by Phase (suggested, not executed)

- **Phase 1, index.ts**: move the OIDC callback and identity verification into the existing `oidc-auth.ts` boundary, and the invocation wrapper into a helper module. Keep `index.ts` as the entry point. Risk: medium. Validate with the existing tool tests and a server smoke test.
- **Phase 2, grade-writeback.ts**: move `toIsoOrNull` to a shared util. Risk: low.

## Validation Plan
Per LOC.md Phase 3: run the test suite in the repo's Docker setup, start the server, and check the OIDC login path before each PR. Not run in report mode.

## Repo Summary

| Repo | Top concern | Priority | Notes |
|---|---|---|---|
| bb-mcp (T2) | `src/index.ts` mixed entry point | High (T2, ranks after T1 items) | Tool files already split by role |

Canaries: not applicable to this repo.
