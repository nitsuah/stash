# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added (Q3 2026)

- **Selective copy filters by file type** (`--include-mime`, `--exclude-mime`): copy only docs,
  PDFs, images, or any MIME type pattern; aliases like `docs`, `sheets`, `pdf`, `images` expand
  to full MIME strings; prefix patterns (e.g. `image/`) match all subtypes.
- **Exponential backoff with rate-limit awareness**: retry loop now backs off exponentially
  (starting at 1 s, capped at `--max-backoff`, default 60 s) with jitter; 429/503 responses
  are logged at WARNING rather than ERROR to distinguish rate-limiting from hard failures.
- **Parallel file copy** (`--workers N`): ThreadPoolExecutor-based parallel copy of files
  within each folder level; folder creation remains sequential to preserve parent IDs.
- **`--max-retries` CLI arg**: configures per-file retry attempts (previously hardcoded to 1).
- **`--max-backoff` CLI arg**: caps the exponential backoff delay in seconds.
- **`skipped_files` counter** added to progress telemetry and final summary when MIME filters
  are active.
- **Incremental / skip-existing copy** (`--skip-existing`): files already present in the
  destination are skipped rather than duplicated; existing subfolders are reused rather than
  recreated — enables safe re-runs after partial failures.
- **`tests/test_q3_features.py`**: 35 new tests covering MIME filter helpers,
  filtered counts, filtered copy, exponential backoff, parallel copy, skip-existing, and CLI args.

### Added

- Documentation compliance updates for Overseer standards
- FEATURES.md with comprehensive feature documentation
- CHANGELOG.md to track version history
- CONTRIBUTING.md with contribution guidelines

### Changed

- Updated ROADMAP.md to quarterly format with completion status
- Updated TASKS.md with proper section structure (Done, In Progress, Todo)
- Updated METRICS.md with accurate project metrics

## [1.0.0] - 2023-11-01

### Added

- Initial release of Google Drive API script
- OAuth2 authentication and authorization flow
- Assessment 1: Root folder file and folder counting
- Assessment 2: Recursive child object counting with detailed CSV reports
- Assessment 3: Folder copying with validation
- Recursive folder copying with structure preservation
- Retry mechanism for file copy failures
- Comprehensive error handling and logging system
- CSV-based validation comparing source and destination
- Environment variable configuration for folder IDs and client credentials
- CI/CD workflows: Pylint, Bandit, CodeQL, Dependency Review
- README.md with setup instructions and badges
- ABOUT.md with detailed implementation documentation
- Support for trashed file filtering

### Fixed

- Error handling for failed file copy operations with parent folder URL retrieval
