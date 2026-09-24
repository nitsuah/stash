## FEATURES.md

## Core Functionality

- **DreamBooth Fine-Tuning** — Fine-tunes Stable Diffusion v1-5 on 3–10 user-provided photos to create a personalized avatar model tied to a unique text token.
- **Prior Preservation** — Trains with 50 class-prior images to prevent the model from forgetting general class knowledge (e.g., "man" or "person") while learning the specific subject.
- **Text Encoder Training** — Trains both the UNet and text encoder for stronger subject binding.
- **Mixed Precision (fp16) Training** — Reduces GPU memory usage by half, enabling training on consumer-grade GPUs and Colab instances.
- **8-bit Adam Optimizer** — Further reduces GPU memory footprint (via `bitsandbytes`) without meaningful loss in training quality.
- **Configurable Training Steps** — `max_train_steps` is user-adjustable up to 2000; the utility module auto-recommends 100 steps per image + 100 base.
- **Image Count Validation** — Utility function enforces the 3–10 image recommendation and surfaces clear messages when the count is out of range.
- **Concepts List (JSON)** — Multi-concept training is supported via a structured `concepts_list.json` file, configurable per subject and class.
- **Sample Image Generation During Training** — `save_sample_prompt` generates preview images at checkpoint intervals so progress can be monitored without a separate inference step.
- **CKPT Weight Export** — Trained weights can be converted to the standard `.ckpt` format compatible with community tooling (Automatic1111, ComfyUI, etc.).
- **HuggingFace Model Upload** — Trained model can be pushed directly to a HuggingFace Hub repository for sharing or reuse.

## Developer Utilities (`avatar/utils.py`)

- **`create_concepts_list`** — Generates a list of concept dictionaries from an instance name and class name.
- **`save_concepts_json` / `load_concepts_json`** — Serializes and deserializes the concepts list to/from a JSON file.
- **`create_instance_directories`** — Creates on-disk data directories for all concept entries.
- **`validate_concept_structure`** — Validates that a concept dict contains all required fields before training.
- **`calculate_recommended_training_steps`** — Returns a recommended step count given a number of training images.
- **`count_images_in_directory`** — Counts `.jpg`, `.jpeg`, and `.png` files in a given directory.
- **`validate_image_count`** — Validates that image count is within the 3–10 recommended range and returns a human-readable status message.
- **`build_training_command`** — Assembles the full `accelerate launch train_dreambooth.py ...` command string from structured parameters. Note: the default `--save_interval=10000` steps exceeds the typical 2000-step training run, so intermediate saves may not occur; the final model is saved after training completes.

## Infrastructure

- **Dockerized Development** — Two-stage Dockerfile: `test` target for CI, `notebook` target for the local Jupyter server.
- **Non-root Notebook Container** — The notebook service runs as `appuser` for improved container security.
- **Container Healthcheck** — Docker Compose and the Dockerfile both configure a curl-based healthcheck on the Jupyter port.
- **25 Unit Tests, 100% Coverage** — All utility functions in `avatar/utils.py` are covered by pytest with 25 tests across 7 test classes.
- **Pre-commit Hooks** — Lint (ruff, flake8), format (black, isort), and test-on-push hooks enforced via `.pre-commit-config.yaml`.
- **GitHub Actions CI** — Runs linting and the full test suite on every push and pull request to `main`.
- **Environment Variable Template** — `.env.example` documents `JUPYTER_TOKEN` and other runtime variables.
