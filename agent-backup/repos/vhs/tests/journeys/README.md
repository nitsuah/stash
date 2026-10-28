---
up: "[[repos/vhs]]"
title: "vhs · README"
source: https://github.com/nitsuah/vhs/blob/main/tests/journeys/README.md
kind: repo-doc
repo: vhs
---

# Journeys

Nightly happy paths a real user takes, one visual baseline per step. Contract and issue lifecycle: [nitsuah/.github journeys/STANDARD.md](https://github.com/nitsuah/.github/blob/main/journeys/STANDARD.md).

- `journey.js`: the shared `step()` helper, vendored from nitsuah/.github. Don't edit it here.
- `vhs.js`: the vhs fixture: the fictional demo collection (`promo/demo-seed.js`, the launch video's tapes), every `/api` and `/auth` call answered in the browser (`promo/demo-mocks.js`), a frozen clock, a seeded `Math.random` (the 1-in-50 "Be Kind, Rewind!" toast otherwise lands in a baseline now and then), sounds off.
- `serve.js`: serves `public/` as static files, so no Postgres or Ollama runs.
- `*.spec.js`: one journey per thing a user wants done, tagged `@feature:<promo/spots.json id>`. Steps tagged `{ docs: '<feature id>' }` also write `docs/screenshots/<id>.png` (`npm run capture:screenshots`, run by `.github/workflows/visual-docs.yml`).
- `__screenshots__/`: Linux baselines. **Generate them only in Docker.**

```bash
docker build -f config/Dockerfile.playwright -t vhs-journeys .
# run, as CI does
docker run --rm -e CI=true vhs-journeys
# write new/changed baselines back into the repo (Git Bash: prefix MSYS_NO_PATHCONV=1 and use $(pwd -W))
docker run --rm -v "$PWD/tests/journeys:/work/tests/journeys" vhs-journeys npm run test:journeys -- --update-snapshots
# soak before opening a PR: 3 runs, 0 failures
docker run --rm -e CI=true -v "$PWD/tests/journeys:/work/tests/journeys" vhs-journeys npm run test:journeys -- --retries 0 --repeat-each 3
# regenerate the docs screenshots locally
docker run --rm -e CI=true -v "$PWD/tests/journeys:/work/tests/journeys" -v "$PWD/docs/screenshots:/work/docs/screenshots" vhs-journeys npm run capture:screenshots
```

Tolerance is `maxDiffPixels: 20`: the soak measured 0 px of noise over 36 runs, and one changed letter in a button is 137 px.

A UI fix fails its journey's visual step until the PR updates the baseline. That's intended: the PNG diff in the PR is the before/after.

Known gap: `review.spec.js` stops short of checking that confirmed tapes appear in the Collection, because they don't until the view re-renders ([#79](https://github.com/nitsuah/vhs/issues/79)). The fix PR adds that check back.
