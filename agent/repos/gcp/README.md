# gcp

<!-- Status -->
[![Linting](https://github.com/nitsuah/gcp/actions/workflows/pylint.yml/badge.svg)](https://github.com/nitsuah/gcp/actions)
<!-- CI is TBD [![CI](https://github.com/nitsuah/gcp/actions/workflows/pylint.yml/badge.svg)](https://github.com/nitsuah/gcp/actions) -->

**TL;DR:** Google Drive assessment and copy tooling packaged as the `drive-copy` CLI.

## Objectives

- Assessment #1 - Write a script to generate a report that shows the total number of files and folders in the root of the source folder.
- Assessment #2 - Write a script to recursively count the number of child objects (all sub-files & folders) for each top-level folder under the source folder.
- Assessment #3 - Write a script to copy content (nested files/folders) of the source folder to destination folder.

## Setup GCP environment

- [Login to GCP & Create project](https://console.cloud.google.com/getting-started?organizationId=0)
- [Create Google OAuth 2.0 Client IDs](https://console.cloud.google.com/apis/credentials/consent?project=project-id)

## Installation

### Prerequisites
- Python 3.10 or higher
- Google Cloud Platform account with Drive API enabled
- OAuth 2.0 Client ID credentials ([setup guide](https://console.cloud.google.com/apis/credentials))

### Install from source

```bash
# Clone the repository
git clone https://github.com/nitsuah/gcp.git
cd gcp

# Install in development mode
pip install -e ".[dev]"

# Verify installation
drive-copy --help
```

### Required API Scopes
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/drive.metadata.readonly`

## Configuration

Set the following environment variables:

```bash
export GOOGLE_DRIVE_CLIENT_ID_FILE='/path/to/client_id.json'
export GOOGLE_DRIVE_SOURCE_FOLDER_ID='your-source-folder-id'
export GOOGLE_DRIVE_DESTINATION_FOLDER_ID='your-destination-folder-id'
```

Or create a `.env` file (see `.env.example`):

```bash
GOOGLE_DRIVE_CLIENT_ID_FILE=/path/to/credentials.json
GOOGLE_DRIVE_SOURCE_FOLDER_ID=abc123xyz
GOOGLE_DRIVE_DESTINATION_FOLDER_ID=xyz456abc
```

## Usage

### CLI Command

```bash
# Canonical packaged entrypoint
drive-copy

# Print required environment variable names
drive-copy --help-env

# Preview copy scope without writing outputs or copying files
drive-copy --dry-run

# Copy only Google Docs and PDFs (aliases: docs, sheets, slides, pdf, images, text, video, audio, zip)
drive-copy --include-mime docs,pdf

# Copy everything except images and videos (prefix 'image/' matches all image subtypes)
drive-copy --exclude-mime images,video

# Combine filters with dry-run to preview what would be copied
drive-copy --dry-run --include-mime docs,sheets

# Parallel copy with 4 workers (files within each folder level are copied concurrently)
drive-copy --workers 4

# Retry up to 5 times with exponential backoff capped at 120 s (rate-limit friendly)
drive-copy --max-retries 5 --max-backoff 120

# Re-run safely after a partial failure — already-copied files and folders are skipped
drive-copy --skip-existing

# Copy mode logs periodic COPY PROGRESS updates and a final COPY PROGRESS SUMMARY
drive-copy

# Alternate valid path (module execution)
python -m gcp.copy_folder
```

`drive-report` appears in older notes, but the packaged console script in `pyproject.toml` is `drive-copy`.

### Python Module

```python
from gcp.copy_folder import count_files_and_folders, copy_child_objects

# Count files in a folder
num_files, num_folders = count_files_and_folders('folder_id')

# Copy folder contents
copy_child_objects('source_id', 'destination_id')
```

## Output Schema

### CSV Format
```csv
Folder Name,File Count,Folder Count
Design,15,3
Documentation,28,5
TOTAL,43,8
```

### JSON Format
See `examples/report-sample.json` for complete structure.

## Outputs

- [![Assessment-1](https://badgen.net/badge/assessment-1/VALIDATED/green?icon=github)](https://github.com/nitsuah/gcp/blob/main/outputs/assessment-1.csv)
- [![Assessment-2](https://badgen.net/badge/assessment-2/VALIDATED/green?icon=github)](https://github.com/nitsuah/gcp/blob/main/outputs/assessment-2.csv)
- [![Assessment-3](https://badgen.net/badge/assessment-3/VALIDATED/green?icon=github)](https://github.com/nitsuah/gcp/blob/main/outputs/assessment-3.csv)

## Workflows

- [![pylint](https://github.com/nitsuah/gcp/actions/workflows/pylint.yml/badge.svg)](https://github.com/nitsuah/gcp/actions/workflows/pylint.yml)
- [![Bandit](https://github.com/nitsuah/gcp/actions/workflows/bandit.yml/badge.svg)](https://github.com/nitsuah/gcp/actions/workflows/bandit.yml)
- [![CodeQL](https://github.com/nitsuah/gcp/actions/workflows/codeql.yml/badge.svg)](https://github.com/nitsuah/gcp/actions/workflows/codeql.yml)
- [![Dependency Review](https://github.com/nitsuah/gcp/actions/workflows/dependency-review.yml/badge.svg)](https://github.com/nitsuah/gcp/actions/workflows/dependency-review.yml)
## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md

## Repository Index

### Root Files
- [[repos/gcp/CHANGELOG.md|CHANGELOG.md]]
- [[repos/gcp/FEATURES.md|FEATURES.md]]
- [[repos/gcp/METRICS.md|METRICS.md]]
- [[repos/gcp/ROADMAP.md|ROADMAP.md]]
- [[repos/gcp/TASKS.md|TASKS.md]]