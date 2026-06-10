# avatar — AI Avatar Generation (DreamBooth + Stable Diffusion)

**Last Validated:** 2026-06-10 | Initial vault entry
**Repo:** https://github.com/nitsuah/avatar
**Branch convention:** `pmo/avatar/planning-alignment-YYYY-MM-DD`

---

## Runtime Status

| Check | Status | Notes |
|---|---|---|
| Docker build | PASS | Jupyter notebook container runs as non-root with healthcheck |
| Test suite | PASS | 25 unit tests (Docker Compose) |
| Notebook server | Available | `http://localhost:8888/` via `docker compose up notebook` |
| Docs baseline | PASS | README, ROADMAP, TASKS, FEATURES, METRICS present |

---

## Stack

- **Training:** DreamBooth + Stable Diffusion on Google Colab
- **Runtime:** Jupyter notebook server (Docker, non-root)
- **Language:** Python
- **CI:** GitHub Actions
- **Prerequisites:** Google Drive (4-5 GB free), HuggingFace account

---

## PMO Findings

- Training pipeline runs on Google Colab (external cloud dependency — not local).
- `xformers` install step has a known workaround comment in the notebook (`FIXME`).
- Docker container provides local inference/notebook server; Colab handles the heavy training.

---

## Priority Focus

1. Resolve `xformers` install FIXME — document current working install path.
2. Document inference workflow (Steps 9–10) with example prompts.
3. Validate test coverage reflects current notebook state.

---

## Key Commands

```bash
# Run unit tests (25 tests)
docker compose -f config/docker-compose.yml --profile test run --rm test

# Start Jupyter notebook server
docker compose -f config/docker-compose.yml up notebook
# → http://localhost:8888/  (set JUPYTER_TOKEN in .env for auth)
```

---

## Active PMO

See TASKS.md and ROADMAP.md for current priorities.

---

## Vault Index

*Copied from repo — do not edit these files, overwritten on sync. Edit only this `.md`.*

**Core:** [[repos/avatar/ROADMAP|ROADMAP]] · [[repos/avatar/TASKS|TASKS]] · [[repos/avatar/FEATURES|FEATURES]] · [[repos/avatar/METRICS|METRICS]] · [[repos/avatar/CHANGELOG|CHANGELOG]] · [[repos/avatar/README|README]]
