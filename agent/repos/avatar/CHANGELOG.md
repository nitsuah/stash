# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added batch generation mode and seed interpolation roadmap items (#16).
- Added a dataset validation cell ("Step 6.5") to `notebooks/DreamBooth_Stable_Diffusion.ipynb` that raises a clear error before training if any concept has fewer than 3 or more than 10 images.

### Changed

- Documentation audit: corrected inaccuracies in README, FEATURES.md, ROADMAP.md, and TASKS.md to accurately reflect the DreamBooth/Stable Diffusion pipeline.
- Aligned the Python version matrix to 3.11 across CI (`.github/workflows/ci.yml`), the Dockerfile base image, and `pyproject.toml` ruff/black targets; updated the README's Python version note accordingly.
- Pinned exact versions in `config/requirements.txt` (previously unpinned), resolved against the `python:3.11-slim-bookworm` base image.
- Expanded the vague "User feedback integration" roadmap item into a proper scoping note with open questions, rather than guessing at an implementation.
- Bumped `actions/checkout` from v6 to v7 in CI (#17).
- Bumped `actions/setup-python` from v6 to v7 in CI (#18).

### Fixed

- Added explicit `contents: read` permission to CI build job to resolve GITHUB_TOKEN scope warning (#19).

### Security

## [0.1.0] - 2024-06-01

### Added
- Project initialization

[Unreleased]: https://github.com/nitsuah/avatar/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nitsuah/avatar/releases/tag/v0.1.0