# Tasks

## Done

_See [docs/ROADMAP.md](ROADMAP.md) Q1/Q2 for the condensed shipped-milestone record and
[docs/CHANGELOG.md](CHANGELOG.md) for the change-by-change history._

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
