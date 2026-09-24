# GCP Google Drive Tools Roadmap

Last Updated: 2026-09-02

The `drive-copy` CLI is in maintenance mode: the core assessment/copy feature set (Q1-Q3 2026)
and both concrete Q4 exploratory items below have shipped. The only open idea is the 2027 web
UI evaluation; barring a new concrete request, future work here is expected to be bugfixes and
dependency upkeep rather than new CLI surface area.

## 2026 Q1–Q3 ✅

> Completed. All shipped features documented in FEATURES.md and CHANGELOG.md.

## 2026 Q4 ✅

> Completed. Both concrete Q4 items shipped; see FEATURES.md and CHANGELOG.md for details.

- [x] **Duplicate detection report** (`--duplicate-report`) — before or after a copy run, generate a CSV of files with identical names and sizes across source and destination; helps identify redundant copies and cleanup candidates alongside the existing assessment reports.
- [x] **Permission mirroring** (`--mirror-permissions`) — copy ACL/sharing settings from source files and folders to their destination counterparts so migrated content retains its original access controls instead of defaulting to destination-owner-only access.

## 2027 (Exploratory)

- [ ] **Lightweight web UI for credential and folder configuration** — evaluated during the 2026
  Q4 pass and deferred. `drive-copy` is a single-user local CLI configured via three environment
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
