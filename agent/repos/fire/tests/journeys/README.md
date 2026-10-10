---
up: "[[repos/fire]]"
title: "fire · README"
source: https://github.com/nitsuah/fire/blob/main/tests/journeys/README.md
kind: repo-doc
repo: fire
---

# Journeys

Nightly happy paths a real user takes, one visual baseline per step. Contract and issue lifecycle: [nitsuah/.github journeys/STANDARD.md](https://github.com/nitsuah/.github/blob/main/journeys/STANDARD.md).

- `journey.js`: the shared `step()` helper, vendored from nitsuah/.github. Don't edit it here.
- `fire.js`: the fire fixture: demo seed (`promo/demo-seed.js`), mocked prices (`promo/demo-mocks.js`), frozen clock, Chart.js animation off, settle waits.
- `*.spec.js`: one journey per thing a user wants done, tagged `@feature:<promo/spots.json id>`.
- `__screenshots__/`: Linux baselines. **Generate them only in Docker.**

```bash
docker build -f config/Dockerfile.playwright -t fire-playwright-e2e .
# run, as CI does
docker run --rm -e CI=true fire-playwright-e2e npm run test:journeys
# write new/changed baselines back into the repo (Git Bash: prefix MSYS_NO_PATHCONV=1)
docker run --rm -v "$PWD/tests/journeys:/work/tests/journeys" fire-playwright-e2e npm run test:journeys -- --update-snapshots
# soak before opening a PR: 3 runs, 0 failures
docker run --rm -e CI=true -v "$PWD/tests/journeys:/work/tests/journeys" fire-playwright-e2e npm run test:journeys -- --retries 0 --repeat-each 3
```

A UI fix fails its journey's visual step until the PR updates the baseline. That's intended: the PNG diff in the PR is the before/after.
