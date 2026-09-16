# avatar

[![CI](https://github.com/nitsuah/avatar/actions/workflows/ci.yml/badge.svg)](https://github.com/nitsuah/avatar/actions)

Uses Google Colab & Jupyter notebook to create a personalized AI avatar by fine-tuning Stable Diffusion v1-5 with DreamBooth on a small set of user-provided photos. The trained model produces new images of the subject in arbitrary styles and settings.

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

**Install dependencies (for local development outside Docker):**

```bash
pip install -r config/requirements.txt
```

> **Python version note:** Python 3.11 is used consistently across the Docker image, CI pipeline, and `pyproject.toml` lint/format targets. Use Python 3.11 for local development outside Docker.

### Notes

- The notebook container runs as a non-root user and does not use `--allow-root`.
- A healthcheck is configured to ensure the notebook endpoint is responsive.

## Prerequisites

- **GPU required** for DreamBooth training. Google Colab may provide a free GPU runtime; GPU type and quota vary — use the Colab link below.
- 4-5 GB of free space on Google Drive
- [Copy Colab file to your Google Drive](https://colab.research.google.com/github/buildspace/diffusers/blob/main/examples/dreambooth/DreamBooth_Stable_Diffusion.ipynb?utm_source=buildspace.so&utm_medium=buildspace_project#scrollTo=XU7NuMAA2drw)
- [Register or Login at HuggingFace.co](https://huggingface.co/login)
- A HuggingFace account is only needed for uploads or gated models; `runwayml/stable-diffusion-v1-5` is public and ungated

## How It Works

This project uses **DreamBooth**, a few-shot fine-tuning technique that personalizes a pre-trained text-to-image diffusion model. You supply 3–10 photos; DreamBooth trains the model to associate a unique identifier and class name with your appearance (e.g., instance identifier `nitsuah` and class name `man`, passed as separate parameters). After training you can generate the subject in any style described by a text prompt.

Key training settings:
- Base model: `runwayml/stable-diffusion-v1-5`
- VAE: `stabilityai/sd-vae-ft-mse`
- Mixed precision: `fp16`
- Optimizer: 8-bit Adam (memory-efficient)
- Text encoder training: enabled
- Prior preservation: enabled (50 class images)
- Recommended training steps: 100 per image + 100 base (e.g., 700 steps for 6 images)

## Procedures

- Step 0: Connect to a virtual machine and Google Drive
- Step 1: Install Requirements
- Step 2: [Create HuggingFace access token](https://huggingface.co/settings/tokens)
- Step 3: Install xformers for memory-efficient attention. If the precompiled wheels fail, build from source (ETA: ~40 min): `pip install git+https://github.com/facebookresearch/xformers@4c06c79#egg=xformers`
- Step 4: Configure your model (set `MODEL_NAME` to `runwayml/stable-diffusion-v1-5`)
- Step 5: Configure the training resources
- Step 5.5: Tell Stable Diffusion what you're training for (set your unique token and class name)
- Step 6: Upload your photos (3–10 images recommended)
- Step 7.1: Change `max_train_steps` (MAX: 2000; recommended: 100 × number of images + 100)
- Step 7.2: Update `save_sample_prompt` — use a descriptive prompt such as `Photo of NITSUAH MAN, highly detailed, 8k, uhd, studio lighting, beautiful`
- Step 7.3: Set prior preservation weights (run without changes on first pass)
- Step 7.4: Generate test images to preview results
- Step 8: Convert weights to CKPT format
- Step 9: Inference — generate images from the trained model
- Step 10: Generate images with custom prompts
- Step 11: Upload your trained model to HuggingFace

## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md
