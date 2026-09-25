# GCP Google Drive Tools Roadmap

> 🧭 [gcp](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

The `drive-copy` CLI is in maintenance mode: the core assessment/copy feature set (2026 Q1–Q3), both
2026 Q4 items (duplicate-detection report, permission mirroring), and `gcp_setup.py` test coverage (99%)
have shipped — see [FEATURES](./FEATURES.md) and [CHANGELOG](./CHANGELOG.md). Completed 2026 sections were
removed in the 2027 planning reset (2026-09-24). Barring a new concrete request, future work is bugfixes and
dependency upkeep rather than new CLI surface area.

## 2027 Q1 (Exploratory)

- [ ] **Lightweight web UI for credential and folder configuration** — evaluated during the 2026
  Q4 pass and deferred to 2027. `drive-copy` is a single-user local CLI configured via three environment
  variables (`GOOGLE_DRIVE_CLIENT_ID_FILE`, `GOOGLE_DRIVE_SOURCE_FOLDER_ID`,
  `GOOGLE_DRIVE_DESTINATION_FOLDER_ID`) and an `InstalledAppFlow` OAuth flow that already opens a
  local browser tab to authorize; there's no persistent server process or account/session model
  for a UI to attach to. A "thin wrapper" is not actually thin here: it would need its own process
  lifecycle, a way to resolve folder IDs to human-readable paths for a picker (recursive Drive
  API traversal, since v3 has no native "browse by path"), and secure local handling of the OAuth
  token instead of the CLI's current run-once-and-exit flow — closer to a new small application
  than a view over the existing architecture.
  - Note: `apps/` in this repo already contains an unrelated Node/Express "Workspace OAuth Engine"
    (multi-account Gmail/Calendar/Drive-logging dashboard) from earlier boilerplate work. It does
    not implement drive-copy credential/folder configuration and was not extended for this
    purpose — evaluate on its own merits separately if it's still wanted.
  - If revisited: scope as a small standalone FastAPI (or Flask) app in `gcp/` that shells out to
    the existing `copy_folder` functions, with a folder picker backed by `files.list` and
    server-held OAuth tokens (not stored in the browser). Should not block on or reuse `apps/`.
