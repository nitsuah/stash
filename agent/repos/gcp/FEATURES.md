# GCP Google Drive API Script Features

## Core Capabilities

### Authentication & Authorization

- OAuth2 authentication flow using Google OAuth 2.0 with local server callback
- Environment variable-based client ID JSON file configuration
- Drive full access and metadata read-only API scopes

### Reporting & Analysis

- `[shipped]` **Assessment 1 — Root Count**: CSV report of files and folders in source folder root
- `[shipped]` **Assessment 2 — Recursive Count**: CSV report with recursive child object counts for all top-level folders
- `[shipped]` **Assessment 3 — Copy Validation**: CSV report of destination folder contents after copy
- `[shipped]` **CSV Export**: Structured CSV output with folder name, file count, folder count

### Folder Operations

- `[shipped]` **Recursive Copy**: Copies all files and folders from source to destination, preserving directory structure
- `[shipped]` **Dry-run Mode** (`--dry-run`): Previews source counts and planned copy target without writing any files or issuing copy API calls
- `[shipped]` **MIME Filters** (`--include-mime`, `--exclude-mime`): Copy only matching file types; short aliases (`docs`, `sheets`, `slides`, `forms`, `drawings`, `pdf`, `images`, `text`, `video`, `audio`, `zip`) expand to full MIME strings; prefix patterns (e.g. `image/`) match all subtypes
- `[shipped]` **Parallel Copy** (`--workers N`): ThreadPoolExecutor-based concurrent file copy within each folder level; folder creation stays sequential to preserve parent IDs
- `[shipped]` **Incremental / Skip-Existing** (`--skip-existing`): Skips files and subfolders already present in the destination — safe for re-runs after partial failures

### Reliability & Retries

- `[shipped]` **Exponential Backoff** (`--max-retries`, `--max-backoff`): Per-file retry loop with exponential delay (base 1 s, jitter, configurable cap); HTTP 429/503 logged at WARNING to distinguish rate-limiting from hard failures
- `[shipped]` **Copy Validation**: Automatic comparison of Assessment 2 and Assessment 3 CSV reports after copy completes
- Graceful error handling with parent folder URL retrieval for failed copy operations

### Progress Telemetry

- `[shipped]` **Periodic Progress Logs**: `COPY PROGRESS` log lines every N items (configurable) with file, folder, failed, and skipped counts plus elapsed time
- `[shipped]` **Final Summary**: `COPY PROGRESS SUMMARY` at completion with total elapsed duration
- `[shipped]` **Skipped Counter**: Tracks files skipped by MIME filters or `--skip-existing`

## Configuration

### Environment Variables

| Variable | Description |
| --- | --- |
| `GOOGLE_DRIVE_CLIENT_ID_FILE` | Path to OAuth2 client ID JSON file |
| `GOOGLE_DRIVE_SOURCE_FOLDER_ID` | Google Drive folder ID to copy from |
| `GOOGLE_DRIVE_DESTINATION_FOLDER_ID` | Google Drive folder ID to copy to |

### CLI Flags

| Flag | Default | Description |
| --- | --- | --- |
| `--dry-run` | off | Preview scope without copying |
| `--include-mime MIME` | (none) | Allowlist of MIME patterns (comma-separated) |
| `--exclude-mime MIME` | (none) | Denylist of MIME patterns (comma-separated) |
| `--workers N` | 1 | Parallel copy workers |
| `--max-retries N` | 1 | Retry attempts per file |
| `--max-backoff SECONDS` | 60 | Cap on exponential backoff delay |
| `--skip-existing` | off | Skip files/folders already in destination |
| `--help-env` | — | Print required environment variable names and exit |

## Output Artifacts

| File | Description |
| --- | --- |
| `outputs/assessment-1.csv` | Root folder file and folder counts |
| `outputs/assessment-2.csv` | Recursive counts for all child folders |
| `outputs/assessment-3.csv` | Destination folder validation report |
| `outputs/gcp-<timestamp>.log` | Timestamped log with operation details and errors |
