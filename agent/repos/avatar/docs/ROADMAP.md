---
up: "[[repos/avatar]]"
source: https://github.com/nitsuah/avatar/blob/main/docs/ROADMAP.md
kind: repo-doc
repo: avatar
---

# Roadmap

> 🧭 [avatar](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

> 2027 planning reset (2026-09-24): completed 2026 milestones (DreamBooth pipeline, v0.1.0, utils extraction with
> 100% coverage, Docker dev, pre-commit, CI, Python 3.12 alignment, notebook dataset validation) were removed from this
> file — see [FEATURES](./FEATURES.md) and [CHANGELOG](./CHANGELOG.md). Every open 2026 item was carried into 2027 Q1
> for triage at planning; vague placeholders ("Performance improvements", "Advanced features", "Enterprise features")
> were dropped because they had no defined scope.

## 2027 Q1 - Quality & Usability (Planned)

- [ ] Add model evaluation metrics to notebook (FID score, CLIP similarity) so output quality can be measured objectively *(carried from 2026 Q2)*
- [ ] **User feedback integration — needs scoping, not yet actionable** *(carried from 2026 Q2)*. The original bullet had no defined mechanism, data model, or trigger; scheduling it requires answering:
  - *Feedback on what?* Generated sample images (thumbs up/down per sample), overall model quality after training, or the notebook/workflow experience itself?
  - *Collection mechanism?* A widget cell in the notebook (e.g. `ipywidgets` buttons), a GitHub issue template, or an external form?
  - *Storage/consumption?* Where does feedback land, and who/what acts on it (retraining trigger, roadmap input, nothing automated)?
  - *Owner?* Single-contributor project — confirm this is worth building vs. simply inviting feedback via GitHub Discussions/Issues.
- [ ] Web UI for non-technical users (Gradio or Streamlit interface wrapping the notebook workflow) *(carried from 2026 Q3)*
- [ ] **Batch generation mode** — accept a list of seed values (names, usernames, IDs) and export all generated avatars as a zip archive *(carried from 2026 Q3)*
- [ ] **Seed interpolation / morph frames** — given two seeds, generate an N-frame interpolation sequence and export as GIF or PNG strip *(carried from 2026 Q3)*
- [ ] Support for alternative base models (Stable Diffusion XL, SDXL-Turbo) *(carried from 2026 Q3)*
- [ ] Multi-user training job queue *(carried from 2026 Q4)*
- [ ] API endpoint for programmatic avatar generation from trained models *(carried from 2026 Q4)*

<!--
AGENT INSTRUCTIONS:
This file tracks the project's high-level goals.
1. Organize items by year + quarter (e.g. "2027 Q1").
2. When an item ships, remove it here and condense it into FEATURES.md / CHANGELOG.md.
3. Add new strategic goals as they emerge.
4. Ensure items are high-level features or milestones, not individual bug fixes.
-->
