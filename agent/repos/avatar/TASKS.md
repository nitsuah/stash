# Tasks

## Done

- [x] Identify repo purpose — DreamBooth fine-tuning on Stable Diffusion v1-5 via Jupyter notebook on Google Colab.
- [x] Add `requirements.txt` — available at `config/requirements.txt`.
- [x] Add README with "how to run the notebook" and expected outputs.
- [x] Extract testable utilities to `avatar/utils.py` (concepts list, image validation, training command builder).
- [x] Create `tests/test_utils.py` — 24 tests covering all utility functions.
- [x] Achieve 100% coverage of `avatar/utils.py`.
- [x] Set up Docker for local development (test + notebook stages).
- [x] Configure pre-commit hooks (ruff, black, flake8, isort, pytest-on-push).
- [x] Set up GitHub Actions CI (lint + test on push/PR to main).
- [x] Clarify Python version matrix — aligned CI, Dockerfile, and `pyproject.toml` (ruff/black targets) to Python 3.11.
- [x] Add dataset validation cell to notebook — new "Step 6.5" cell surfaces a clear error when any concept's image count is outside the 3–10 recommended range before Step 7 (training) runs; mirrors the tested `avatar/utils.py::validate_image_count` logic.
- [x] Pin exact versions in `config/requirements.txt` — resolved and pinned against the `python:3.11-slim-bookworm` Docker base (jupyter==1.1.1, notebook==7.6.2, ipykernel==7.3.0, matplotlib==3.11.1, pandas==3.0.5, numpy==2.4.6, pytest==9.1.1, pytest-cov==7.1.0, flake8==7.3.0).
- [x] Pin `actions/setup-python` to a commit SHA in CI (CWE-494) — `.github/workflows/ci.yml` now references `actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7`; SHA independently verified against the tag via the GitHub API before applying.
- [x] Align Step 6.5's `_count_images` with `DreamBoothDataset`'s actual accept-any-Pillow-openable-file contract — the notebook cell previously undercounted concept directories that used image extensions outside `('.jpg', '.jpeg', '.png')`, producing a false "not enough images" error even though real training would have accepted those files. Now opens+verifies each regular file with Pillow instead of filtering by suffix.

## In Progress

## Todo

- [ ] Bring `avatar/utils.py::count_images_in_directory` (and `validate_image_count`) in line with the notebook's Pillow-based counting (see the "Align Step 6.5" item above — the notebook and `utils.py` now diverge). Deferred separately because `tests/test_utils.py::test_count_images_with_files` creates fixture images via `.touch()` (empty files Pillow cannot open); a content-based rewrite needs new fixtures (real minimal images, e.g. via `PIL.Image.new(...).save(...)`) before the function itself can change.
- [ ] Commit a hashed lock file (`pip-compile --generate-hashes` or equivalent) for the full Python dependency graph used by `config/requirements.txt` / `Dockerfile` (CWE-829) — flagged as a "heavy lift" by CodeRabbit; needs `pip-tools` added, a generated lock file, and a CI step to install from it.

- [ ] Add model evaluation step to notebook — compute CLIP similarity score between generated samples and training images to quantify output quality.
- [ ] Add `nbconvert` step to CI — execute the notebook headlessly to catch broken cells (guard with `@pytest.mark.notebook` or a separate workflow job).
- [ ] Export notebook to `examples/DreamBooth_Stable_Diffusion.html` so users can preview the workflow without running Colab.
- [ ] Document the `build_training_command` utility in README — show how to use it to reproduce the training command locally.
- [ ] Add Gradio or Streamlit inference UI — wrap the trained model in a simple web form for non-technical users.
- [ ] Add a `CONTRIBUTING.md` entry (or link to `nitsuah/.github`) to the local repo root for discoverability.
- [ ] Scope "user feedback integration" (see `ROADMAP.md` Q2) — needs a concrete mechanism, data model, and trigger defined before it's actionable; not implemented here per explicit instruction not to guess at scope.
- [ ] Create `run_notebook.sh` helper script:

```bash
#!/usr/bin/env bash
python -m pip install -r config/requirements.txt
NOTEBOOK="${1:-notebooks/DreamBooth_Stable_Diffusion.ipynb}"
jupyter nbconvert --to html "$NOTEBOOK" --ExecutePreprocessor.timeout=600 --execute
```

<!--
AGENT INSTRUCTIONS:
This file tracks specific actionable tasks.
1. Categorize tasks into "Todo", "In Progress", and "Done".
2. Add new tasks identified during code analysis or planning.
3. Mark tasks as [x] when verified as complete.
4. Keep task descriptions concise but actionable.
-->
