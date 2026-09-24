# Tasks

## Todo

- [ ] Basic CLI interface for the deployer (P3, M) — split out of the old "Improve GitHub Actions CI workflow" scope; not started.
- [ ] Design the contract upgradeability mechanism — **implementation** (P2, M). Design is written up in ROADMAP.md's new "2027" section; deferred there rather than shipped as untested proxy/initializer logic (see rationale in that section).
- [ ] Apply gas-optimization findings from the 2026-09 research pass below (P3, S) — no contract code changed this cycle; findings are documented, not yet implemented.
- [ ] Get Slither producing real findings in this sandboxed dev environment (P3, S) — configured (`config/slither.config.json`, `npm run security:slither`, CI `slither` job using `crytic/slither-action`) but this dev sandbox blocks solc's native binary download (both `solc-select` and Hardhat's own solc fetch hit it; Hardhat has a WASM fallback, `solc-select`/crytic-compile do not), so no local run completed. The CI job runs on a normal-network GitHub Actions runner and should work there — check its first run's summary/annotations and record a findings baseline once it does.
- [ ] Deferred: `npm audit` (post fast-uri fix) still flags js-yaml (high, non-major fix available but transitive via a dep that hasn't republished against it), adm-zip (moderate, fix requires downgrading hardhat to 3.11.1), and hardhat/@nomicfoundation/hardhat-mocha (moderate, fix requires a semver-major hardhat downgrade/change). None of these are among the 4 Dependabot alerts fixed in the fast-uri patch; not forcing a Hardhat major-version change without verifying compatibility first (P2, M)

## In Progress

(none)

## Done

Condensed into `docs/ROADMAP.md` (milestones), `docs/FEATURES.md` (shipped
capabilities), and `CHANGELOG.md` (change-by-change history, including the
2026-09 cycle's deployment script, CI/Slither, and Ownable migration work) —
see those files rather than a duplicated narrative here.
