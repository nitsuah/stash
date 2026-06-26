# Metrics

## Core Metrics

| Metric            | Value | Notes                                                    |
| ----------------- | ----- | -------------------------------------------------------- |
| Code Coverage     | 98%+  | Comprehensive test coverage across all features. Only a few unreachable dead-code lines excluded. |
| Lines of Code     | ~750  | `gcp/copy_folder.py`                                     |
| Python Files      | 1     | Single implementation file                               |
| Test Files        | 5     | `test_copy_folder.py`, `test_copy_folder_extended.py`, `test_main.py`, `test_q3_features.py`, `test_rca_import.py` |
| Test Cases        | 80    | Auth, file ops, recursive counting, copying with retry, MIME filters, exponential backoff, parallel copy, skip-existing, CLI args |
| Functions         | ~18   | Core ops + helpers: backoff, MIME filter, skip-existing, progress tracking |
| Dependencies      | 4     | pandas, google-api-python-client, auth libraries         |
| CI/CD Workflows   | 5     | Pylint, Bandit, CodeQL, Dependency Review, Docker Smoke  |
| Assessment Files  | 3     | CSV reports for validation                               |

## Health

| Metric           | Value      | Notes                                         |
| ---------------- | ---------- | --------------------------------------------- |
| Open Issues      | 0          | No open issues                                |
| Last Updated     | 2026-06-03 | Q3 feature set complete (dev-q3)              |
| License          | GPL-3.0    | GNU General Public License v3                 |
| Python Version   | 3.12       | Tested on Python 3.12                         |
| Security Scans   | 3          | Bandit, CodeQL, Dependency Review             |
