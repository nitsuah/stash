# Metrics

> 🧭 [auto-apply-plugin](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · **Metrics** <!-- nav -->

## Core Metrics

| Metric        | Value |
| ------------- | ----- |
| Code Coverage | 83.48% lines |
| Build Time    | 3.44s |
| Bundle Size   | 619.78KB |
| Test Files    | 13 (9 unit + 4 Playwright e2e) |
| Test Cases    | 125 (111 unit + 14 Playwright e2e) |
| Other coverage | 83.48% lines / 65.99% branches / 82.11% functions |

## Health

| Metric        | Value  |
| ------------- | ------ |
| Open Issues   | 0 (gh issue list, 2026-09-02) |
| PR Turnaround | ~11h avg, last 5 merged PRs (#56–#60, gh pr list, 2026-09-02) |
| Skipped Tests | 0      |
| Lint Status   | pass (Docker Node 22 Alpine, `npm run lint`, 2026-09-02) |
| Latest Validation | Native (no Docker in this cloud automation environment): `npm install && npm run test:coverage` — 111 pass / 0 fail, 83.48% lines / 65.99% branches / 82.11% functions; `npm run lint` clean (2026-09-18) |
| Lockfile Sync | pass (`npm ci` succeeds in clean container, 2026-09-02) |
| Health Score  | 92/100 |


## How to Update

All commands run inside Docker — no local Node required.

### Build test image
```bash
docker build --target test -t ats-fill:test .
```

### Lint
```bash
docker run --rm ats-fill:test npm run lint
```

### Tests
```bash
docker run --rm ats-fill:test npm test
```

### Coverage
```bash
docker run --rm ats-fill:test npm run test:coverage
```

### Playwright e2e
```bash
docker build --target e2e -t ats-fill:e2e .
docker run --rm ats-fill:e2e npm run test:e2e
```

### docker-compose shortcuts
```bash
docker compose run --rm lint
docker compose run --rm test
docker compose run --rm coverage
docker compose run --rm e2e
```
