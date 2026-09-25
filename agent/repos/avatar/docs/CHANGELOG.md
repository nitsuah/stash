---
up: "[[repos/avatar]]"
source: https://github.com/nitsuah/avatar/blob/main/docs/CHANGELOG.md
---

# Changelog

> 🧭 [avatar](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Added batch generation mode and seed interpolation roadmap items (#16).
- Added a dataset validation cell ("Step 6.5") to `notebooks/DreamBooth_Stable_Diffusion.ipynb` that raises a clear error before training if any concept has fewer than 3 or more than 10 images.

### Changed

- Raised the Python floor to 3.12 (previously aligned to 3.11) across CI (`.github/workflows/ci.yml`), the Dockerfile base image, and `pyproject.toml` ruff/black targets; updated the README's Python version note accordingly. This unblocks Dependabot PR #23 (numpy 2.4.6 -> 2.5.3), which requires Python >=3.12.
- Documentation audit: corrected inaccuracies in README, FEATURES.md, ROADMAP.md, and TASKS.md to accurately reflect the DreamBooth/Stable Diffusion pipeline.
- Pinned exact versions in `config/requirements.txt` (previously unpinned), resolved against the Python 3.12 base image.
- Expanded the vague "User feedback integration" roadmap item into a proper scoping note with open questions, rather than guessing at an implementation.
- Bumped `actions/checkout` from v6 to v7 in CI (#17).
- Bumped `actions/setup-python` from v6 to v7 in CI (#18).
- Dependency bumps: numpy 2.5.3 (#23), pandas 3.0.6 (#26), matplotlib 3.11.2 (#27).
- README "Copy Colab file" link now opens this repo's own notebook instead of the archived buildspace `diffusers` fork.
- Planning docs reset for 2027 (`pmo-ff`): completed roadmap items condensed into FEATURES, open 2026 items carried into 2027 Q1, breadcrumb navigation + README docs index added.

### Fixed

- Added explicit `contents: read` permission to CI build job to resolve GITHUB_TOKEN scope warning (#19).
- Step 6.5's dataset-count check now opens+verifies each file with Pillow instead
  of filtering by `.jpg`/`.jpeg`/`.png` suffix, matching `DreamBoothDataset`'s
  actual accept-any-Pillow-openable-file contract — previously undercounted
  concept directories using other image extensions, producing a false
  "not enough images" error.

### Security

- Pinned `actions/setup-python` to a commit SHA in CI (CWE-494), verified
  against the tag via the GitHub API before applying.

## [0.1.0] - 2024-06-01

### Added
- Project initialization

[Unreleased]: https://github.com/nitsuah/avatar/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/nitsuah/avatar/releases/tag/v0.1.0