# Metrics

> 🧭 [gcp](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · **Metrics** <!-- nav -->

## Core Metrics

| Metric            | Value | Notes                                                    |
| ----------------- | ----- | -------------------------------------------------------- |
| Code Coverage | 99% total | Docker run 2026-09-24 (`python:3.12-slim`, `pip install -r requirements-dev.txt -e .`): `copy_folder.py` 98% (419 stmts, 7 miss), `gcp_setup.py` 99% (181 stmts, 1 miss: the `__main__` guard; was 0% before `tests/test_gcp_setup.py`), `retry.py` 96% (27 stmts, 1 miss). Total 628 stmts, 9 miss (was 70%). 178 tests pass in ~7s. Command: `pytest tests/ --cov=gcp --cov-report=term-missing`. Use an editable install (`-e .`) so pytest measures the checked-out `gcp/`. With a plain `pip install .`, tests can import the site-packages copy instead, and `--cov=gcp` may then miss it (the first 2026-09-24 container run reported 0% this way). |
| Lines of Code | 1491 | `wc -l gcp/*.py` (2026-09-24): `copy_folder.py` 1079, `gcp_setup.py` 334, `retry.py` 75, `__init__.py` 3 |
| Python Files | 4 | `gcp/__init__.py`, `copy_folder.py`, `gcp_setup.py`, `retry.py`. No longer a single implementation file. |
| Test Files | 8 | `test_copy_folder.py`, `test_copy_folder_extended.py`, `test_gcp_setup.py`, `test_main.py`, `test_pr59_review_fixes.py`, `test_q3_features.py`, `test_rca_import.py`, `test_roadmap_2026.py` (+ `conftest.py`) |
| Test Cases | 178 | All passing in Docker (2026-09-24) |
| Functions         | ~22   | Core ops + helpers: backoff, MIME filter, skip-existing, permission mirroring, duplicate detection, progress tracking |
| Dependencies      | 5     | pandas, google-api-python-client, auth libraries, pyasn1 |
| CI/CD Workflows   | 6     | Pylint, Bandit, CodeQL, Dependency Review, Docker Smoke, Python CI |
| Assessment Files  | 3     | CSV reports for validation                               |
| Report Files      | 1     | `duplicate-report.csv` (`--duplicate-report`)             |

## Health

| Metric           | Value      | Notes                                         |
| ---------------- | ---------- | --------------------------------------------- |
| Open Issues | 0 | `gh issue list` (2026-09-24) |
| Last Updated | 2026-09-24 | gcp_setup.py tests added; Docker coverage re-run |
| License          | GPL-3.0    | GNU General Public License v3                 |
| Python Version   | 3.10+      | CI matrix: 3.10, 3.11, 3.12                   |
| Security Scans   | 3          | Bandit, CodeQL, Dependency Review             |
