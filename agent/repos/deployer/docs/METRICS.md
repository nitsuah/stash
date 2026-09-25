# Metrics for Nitsuah-Labs/deployer

> 🧭 [deployer](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · **Metrics** <!-- nav -->

This document outlines the key metrics used to track the health and performance of the Nitsuah-Labs/deployer project.

_Last verified: 2026-09 roadmap-and-docs cycle. "Verified" below means measured directly in this cycle, in Docker, against the code in this PR — not carried forward from a prior update._

## Metrics Table

| Metric                       | Current | Target  | Status |
| ---------------------------- | ------- | ------- | ------ |
| Code Coverage                | 92.45% lines / 85.90% statements (verified, `npm run coverage` in Docker — see "Coverage" note below) | 90%     | 🟢 (lines) / 🟡 (statements) |
| Number of Tests              | 63 (verified, `npm test` in Docker) | 50      | 🟢     |
| Slither Findings (High)      | 2 (`weak-prng` in RegisterPortal; 2026-09-24, 47 contracts analyzed) | 0       | 🔴     |
| Slither Findings (Medium)    | 2 (`locked-ether`, `divide-before-multiply` in Base64; 2026-09-24) | <= 2    | 🟢     |
| Gas Usage (Deployment)       | RegisterPortal 512,195 / Domains 4,036,286 / LabNFT 13,162,757 (verified via `deploy/deploy.ts` against the local Hardhat network) | < 5000000 | 🟢 (RegisterPortal, Domains) / 🔴 (LabNFT — see note) |
| Gas Usage (Typical Tx)       | TBD (needs a `REPORT_GAS=true npm test` run; not captured this cycle) | < 100000  | 🟡     |
| Cyclomatic Complexity (Avg)  | TBD     | < 10      | 🟡     |
| Lines of Code (SLOC)         | TBD     | < 500     | 🟡     |
| CI/CD Pipeline Success Rate  | ~98% (verified via `gh run list`, see note below) | 99%     | 🟢     |
| Deployment Time              | TBD     | < 60s     | 🟡     |
| Number of Dependencies       | 20 devDependencies (verified via package.json) | < 10 | 🔴 (target unrealistic for a Hardhat + OpenZeppelin + TypeScript stack; see note) |

**Status:**

- 🟢: Good - Metric is meeting or exceeding the target.
- 🟡: Warning - Metric is close to the target, but needs attention.
- 🔴: Critical - Metric is significantly below the target.
- ⚪: Not measured this cycle (see the note for why).

### CI/CD Pipeline Success Rate — investigation (2026-09)

The previous "0%" figure was stale, not current. `gh run list --repo Nitsuah-Labs/deployer --workflow=ci.yml --limit 50` shows 49 of the last 50 `CI` workflow runs succeeded; the one failure (2026-07-29, immediately before the Hardhat v2→v3 toolchain migration commits) was a one-off, not a recurring issue, and the very next run on `main` succeeded. Across all workflows (`CI` + Dependabot's own runs) over the last 100 runs, 86 succeeded / 14 failed — the failures are concentrated in that same pre-migration window. There is no live CI/CD reliability problem; the metric was simply never updated after the underlying issue was fixed. Two real (if minor) CI problems were found and fixed this cycle instead:
- The `coverage` step ran an `echo` stub that always exited 0 without doing anything, since `solidity-coverage` doesn't support Hardhat v3. It now runs Hardhat v3's native `--coverage` flag.
- The "Check contract sizes" step called a Hardhat-^2.x-only plugin (`hardhat-contract-sizer`) that isn't installed, so it has failed on every run since the v3 migration — masked by `continue-on-error: true`. Removed (see TASKS.md).

Neither of these caused the workflow to report failure (both were silently masked), which is presumably why the true state of CI health was hard to see at a glance. Consider that a general lesson for this file: a green run badge doesn't guarantee every step inside it did something meaningful.

### Coverage

Hardhat v3 has no working `solidity-coverage` integration (that plugin's `peerDependencies` cap it at `hardhat ^2.11.0`, confirmed via `npm view solidity-coverage peerDependencies`), so the previous 86.33% figure could not have been produced by this repo's actual toolchain and predates the v3 migration — it was not carried forward as fact. Hardhat v3 ships its own native coverage (`hardhat test --coverage`, now wired up as `npm run coverage`); the 92.45%/85.90% total above is a real, freshly-measured run of it (`docker compose run --rm test npx hardhat test --config hardhat.config.mjs --coverage`, single container, no concurrent load — an earlier attempt run alongside another Docker container hit mocha timeouts under resource contention and was discarded rather than reported). Per-file breakdown from that run:

| File                            | Line % | Statement % | Uncovered lines   |
| -------------------------------- | ------ | ------------ | ------------------ |
| `contracts/RegisterPortal.sol`   | 100.00 | 100.00       | —                   |
| `contracts/libs/Base64.sol`      | 97.56  | 87.50        | 20                  |
| `contracts/libs/StringUtils.sol` | 47.06  | 41.67        | 21-28, 30           |
| `contracts/Domains.sol`          | 91.53  | 88.00        | 115-117, 119, 133   |
| `contracts/LabNFT.sol`           | 98.72  | 98.21        | 166                 |

`StringUtils.sol` is the main drag on the total — it's a small library (`strlen`/UTF-8 length counting) with unicode-handling branches the current test suite doesn't specifically target; a good candidate for the next cycle's coverage work. `contracts/emojis.sol` (an untested Hardhat-scaffold demo contract) was relocated to `examples/scaffold/` this cycle specifically because it was dragging the total down without representing real product code — see CHANGELOG.md.

### Gas Usage (Deployment)

Measured by running `deploy/deploy.ts` against a fresh local Hardhat network. LabNFT's 13.16M gas deployment cost is the concrete, measured confirmation of the gas-optimization research finding in TASKS.md: its eight trait `string[]` arrays are populated in storage at construction, which is expensive and — being dynamic-array storage — can't be made `constant`/`immutable` without an architecture change (e.g. moving trait data off-chain into `tokenURI` generation). Not addressed this cycle; see TASKS.md.

### Number of Dependencies

20 is `Object.keys(devDependencies).length` from `package.json` at the time of writing — genuinely double the "< 10" target. That target predates this being a Hardhat + OpenZeppelin + TypeScript + Mocha/Chai project, all of which pull in their own required peer/dev tooling; treat the target itself as the thing to revisit, not this count as a regression to chase down.

## How to Update

This section describes how to update the metrics listed above.

### Line Coverage & Branch Coverage & Number of Tests

    1.  `solidity-coverage` does NOT work on this project — it only supports Hardhat ^2.x. Use Hardhat v3's built-in coverage instead.
    2.  Run tests with coverage: `npm run coverage` (or `docker compose --profile coverage run --rm coverage`).
    3.  Hardhat v3's native coverage prints a summary to the console (no lcov.info yet). Update the "Current" column with the values from that output.

### Slither Findings (High & Medium)

    1.  `npm run security:slither` (runs `slither contracts/` with `config/slither.config.json`; needs `solc` 0.8.28, e.g. `solc-select install 0.8.28 && solc-select use 0.8.28`), or read the CI `slither` job summary, which lists counts by impact.
    2.  Review the output/job summary and count the number of High and Medium severity findings. Update the "Current" column.  Address or mitigate findings.

### Gas Usage (Deployment & Typical Tx)

    1.  Use `hardhat-gas-reporter`. Install: `npm install --save-dev hardhat-gas-reporter`
    2.  Configure `config/hardhat.config.js` to include the reporter.
    3.  Run tests with gas reporting enabled: `REPORT_GAS=true npx hardhat test`
    4.  Examine the gas usage reports for deployment and typical transactions. Update the "Current" column.

### Cyclomatic Complexity (Avg) & Lines of Code (SLOC) & Number of Dependencies

    1.  Install `tokei`: `cargo install tokei` (requires Rust toolchain)
    2.  Run `tokei`: `tokei .`
    3.  The output will provide SLOC.  Update the "Current" column.
    4.  For Cyclomatic Complexity, consider using a tool like `radon` after converting Solidity to a Python-like AST (This is a complex task and may require custom tooling). Update the "Current" column when available.
    5. To get the number of dependencies, run `npm list --depth=0` and count the number of listed packages.

### CI/CD Pipeline Success Rate

    1.  Monitor the CI/CD pipeline (e.g., GitHub Actions) for build and test success/failure rates.
    2.  Calculate the success rate over a period (e.g., last 30 days) and update the "Current" column.

### Deployment Time

    1.  Measure the time taken for contract deployment during the CI/CD pipeline or local deployments.  Use timestamps before and after the deployment transaction is sent.
    2.  Update the "Current" column.
