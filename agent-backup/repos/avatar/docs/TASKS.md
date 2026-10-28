---
up: "[[repos/avatar]]"
title: "avatar · TASKS"
source: https://github.com/nitsuah/avatar/blob/main/docs/TASKS.md
kind: repo-doc
repo: avatar
---

# Tasks

> 🧭 [avatar](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-30

## Done

_Shipped work lives in [FEATURES](./FEATURES.md) (capabilities) and [CHANGELOG](./CHANGELOG.md) (change-by-change history)._

## In Progress

## Todo

- [ ] Commit a hashed lock file (`pip-compile --generate-hashes` or equivalent) for the full Python dependency graph used by `config/requirements.txt` / `Dockerfile` (CWE-829) — flagged as a "heavy lift" by CodeRabbit; needs `pip-tools` added, a generated lock file, and a CI step to install from it.
  - Priority: P2
  - Type: CI

- [ ] Add model evaluation step to notebook — compute CLIP similarity (and FID, per ROADMAP 2027 Q1) score between generated samples and training images to quantify output quality.
  - Priority: P2
  - Type: Feature
- [ ] Add `nbconvert` step to CI — execute the notebook headlessly to catch broken cells (guard with `@pytest.mark.notebook` or a separate workflow job).
  - Priority: P2
  - Type: CI
- [ ] Export notebook to `examples/DreamBooth_Stable_Diffusion.html` so users can preview the workflow without running Colab.
  - Priority: P3
  - Type: Docs
- [ ] Document the `build_training_command` utility in README — show how to use it to reproduce the training command locally.
  - Priority: P3
  - Type: Docs
- [ ] Add Gradio or Streamlit inference UI — wrap the trained model in a simple web form for non-technical users.
  - Priority: P2
  - Type: Feature
- [ ] Add a `CONTRIBUTING.md` entry (or link to `nitsuah/.github`) to the local repo root for discoverability. GitHub already serves the org defaults: as of the 2026-09-24 PMO audit, `gh api repos/nitsuah/avatar/community/profile` resolves `contributing`, `code_of_conduct` and `pull_request_template` from `nitsuah/.github`. This item is only about in-repo discoverability, so P3.
  - Priority: P3
  - Type: Docs
- [ ] Scope "user feedback integration" (see `ROADMAP.md` 2027 Q1) — needs a concrete mechanism, data model, and trigger defined before it's actionable; not implemented here per explicit instruction not to guess at scope.
  - Priority: P3
  - Type: Docs
- [ ] Create `run_notebook.sh` helper script:
  - Priority: P3
  - Type: Tech debt

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
