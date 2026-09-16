# Metrics

## Core Metrics

| Metric            | Value | Notes                                                    |
| ----------------- | ----- | -------------------------------------------------------- |
| Code Coverage     | 98% (`copy_folder.py`) / 67% total | Docker run 2026-09-02: `copy_folder.py` 98% (391 stmts, 7 miss); `gcp_setup.py` 0% (not yet tested, 181 stmts); 108 tests pass in ~14s. Command: `pytest tests/ --cov=gcp --cov-report=term-missing` |
| Lines of Code     | ~1010 | `gcp/copy_folder.py`                                     |
| Python Files      | 1     | Single implementation file                               |
| Test Files        | 6     | `test_copy_folder.py`, `test_copy_folder_extended.py`, `test_main.py`, `test_q3_features.py`, `test_rca_import.py`, `test_roadmap_2026.py` |
| Test Cases        | 108   | Auth, file ops, recursive counting, copying with retry, MIME filters, exponential backoff, parallel copy, skip-existing, permission mirroring, duplicate detection, CLI args |
| Functions         | ~22   | Core ops + helpers: backoff, MIME filter, skip-existing, permission mirroring, duplicate detection, progress tracking |
| Dependencies      | 5     | pandas, google-api-python-client, auth libraries, pyasn1 |
| CI/CD Workflows   | 6     | Pylint, Bandit, CodeQL, Dependency Review, Docker Smoke, Python CI |
| Assessment Files  | 3     | CSV reports for validation                               |
| Report Files      | 1     | `duplicate-report.csv` (`--duplicate-report`)             |

## Health

| Metric           | Value      | Notes                                         |
| ---------------- | ---------- | --------------------------------------------- |
| Open Issues      | 0          | No open issues                                |
| Last Updated     | 2026-09-02 | Docker coverage run (pytest --cov=gcp)        |
| License          | GPL-3.0    | GNU General Public License v3                 |
| Python Version   | 3.10+      | CI matrix: 3.10, 3.11, 3.12                   |
| Security Scans   | 3          | Bandit, CodeQL, Dependency Review             |
