# Metrics

## Core Metrics

| Metric        | Value |
| ------------- | ----- |
| Code Coverage | 89.66% lines |
| Build Time    | 3.44s |
| Bundle Size   | 619.78KB |
| Test Files    | 13 (9 unit + 4 Playwright e2e) |
| Test Cases    | 120 (106 unit + 14 Playwright e2e) |
| Other coverage | 89.66% lines / 66.89% branches / 86.24% functions |

## Health

| Metric        | Value  |
| ------------- | ------ |
| Open Issues   | 0 (gh issue list, 2026-09-02) |
| PR Turnaround | ~11h avg, last 5 merged PRs (#56–#60, gh pr list, 2026-09-02) |
| Skipped Tests | 0      |
| Lint Status   | pass (Docker Node 22 Alpine, `npm run lint`, 2026-09-02) |
| Latest Validation | Docker Node 22 Alpine + Playwright Noble image: lint pass, `npm test` 106 pass / 0 fail, Playwright 14 pass / 0 fail (incl. a11y audits), `npm run test:coverage` 89.66% lines / 66.89% branches / 86.24% functions (2026-09-02) |
| Lockfile Sync | pass (`npm ci` succeeds in clean container, 2026-09-02) |
| Health Score  | 92/100 |


## How to Update

All commands run inside Docker — no local Node required.

### Build test image
```bash
docker build --target test -t auto-apply-plugin:test .
```

### Lint
```bash
docker run --rm auto-apply-plugin:test npm run lint
```

### Tests
```bash
docker run --rm auto-apply-plugin:test npm test
```

### Coverage
```bash
docker run --rm auto-apply-plugin:test npm run test:coverage
```

### Playwright e2e
```bash
docker build --target e2e -t auto-apply-plugin:e2e .
docker run --rm auto-apply-plugin:e2e npm run test:e2e
```

### docker-compose shortcuts
```bash
docker compose run --rm lint
docker compose run --rm test
docker compose run --rm coverage
docker compose run --rm e2e
```
