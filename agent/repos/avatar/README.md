# avatar

[![CI](https://github.com/nitsuah/avatar/actions/workflows/ci.yml/badge.svg)](https://github.com/nitsuah/avatar/actions)

Uses Google Colab & Jupyter notebook to create an AI Avatar project using Dreambooth and Stable Diffusion.

## Development

All checks run via Docker — no local Python required.

**Run tests (25 unit tests):**
```bash
docker compose -f config/docker-compose.yml --profile test run --rm test
```

**Start the Jupyter notebook server:**
```bash
docker compose -f config/docker-compose.yml up notebook
```
Open `http://localhost:8888/`. Set `JUPYTER_TOKEN` in `.env` for auth, or leave empty to disable locally.

**Pre-commit hooks** (lint/format on commit, tests on push):
```bash
pip install pre-commit && pre-commit install && pre-commit install --hook-type pre-push
```

### Notes

- The notebook container runs as a non-root user and does not use `--allow-root`.
- A healthcheck is configured to ensure the notebook endpoint is responsive.

## Prerequisites

- 4-5 GB/s of free space on Google Drive
- [Copy Colab file to your Google Drive](https://colab.research.google.com/github/buildspace/diffusers/blob/main/examples/dreambooth/DreamBooth_Stable_Diffusion.ipynb?utm_source=buildspace.so&utm_medium=buildspace_project#scrollTo=XU7NuMAA2drw)
- [Register or Login at Huggingface.co](https://huggingface.co/login)

## Procedures

- Step 0: Connect to a virtual machine and Google Drive
- Step 1: Install Requirements
- Step 2:[Create Hugginface.co access token](https://huggingface.co/settings/tokens)
- Step 3: Install xformers from precompiled wheels, use the following if you have issues (ETA:~40mins) // FIXME: `pip install git+https://github.com/facebookresearch/xformers@4c06c79#egg=xformers`
- Step 4: Configure your model
- Step 5: Configure the training resources
- Step 5.5 - Tell Stable Diffusion what you're turning for
- Step 6: Upload your images
- Step 7.1: Change `max_train_steps` (MAX: 2000)
- Step 7.2: Update `save_sample_prompt`, more than just "Photo of xyz person", ex: `Photo of NITSUAH MAN, highly detailed, 8k, uhd, studio lighting, beautiful`
- Step 7.2 - Set weights (run without changes first time)
- Step 7.3 - Generate test images!
- Step 8 - Convert weights to CKPT
- Step 9 - Inference
- Step 10 - Generate images!
- Step 11 - Upload your custom trained model to HuggingFace
## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md

## Repository Index

### Root Files
- [[repos/avatar/CHANGELOG.md|CHANGELOG.md]]
- [[repos/avatar/FEATURES.md|FEATURES.md]]
- [[repos/avatar/METRICS.md|METRICS.md]]
- [[repos/avatar/ROADMAP.md|ROADMAP.md]]
- [[repos/avatar/TASKS.md|TASKS.md]]