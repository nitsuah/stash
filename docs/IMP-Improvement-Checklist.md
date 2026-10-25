# IMP Improvements Checklist

- [x] Add `.imps/` to `.gitignore` (already done).
- [x] Create central config `imps-config.yml` (done).
- [x] Add wrapper script `scripts/imp-run.ps1` (done).
- [x] Document IMP dashboard & timeline (done).
- [x] Add pointer file `.github/imps-path.txt` (done).
- [ ] Update brief‑generation scripts to automatically append the required IMP trailer.
- [ ] Add lint to ensure diffs ≤ 15 lines before committing.
- [ ] Schedule nightly clean‑up of worktrees older than 48 h (could be a cron task).
- [ ] Ensure future IMP runs use Docker (`docker compose run …`) as per config.

*All items marked with [x] are completed; unchecked items remain pending.*
