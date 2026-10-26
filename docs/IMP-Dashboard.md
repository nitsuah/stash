# IMP Dashboard (auto‑generated)

## Summary (last 24 h)
- **26** IMP runs across 5 repos
- **16** passed gate → open PRs
- **10** failed gate (diff too large, missing trailer, no commits, permission denials)

## Details
| Repo | Passed | Failed | Notes |
|------|--------|--------|-------|
| fire | 5 | 2 | diff > 15 lines on issue 171; missing trailer on repeat runs |
| vhs  | 2 | 3 | no commits on issues 77/79; permission denials |
| vigil| 4 | 3 | missing trailer (issues 276/313); no commits (issue 276) |
| stash| 3 | 2 | missing trailer (issues 285/287); no commits (issues 287/289) |
| other| 2 | 0 | — |

## Recommendations
- Split large diffs ≤ 15 lines.
- Add IMP trailer automatically (see wrapper).
- Ensure `git add/commit` before gate.
- Run via Docker (config enforces this).
- Clean old worktrees > 48 h.
- Review open PRs nightly.
