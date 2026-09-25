---
up: "[[repos/deployer]]"
source: https://github.com/Nitsuah-Labs/deployer/blob/main/docs/CHANGELOG.md
kind: repo-doc
repo: deployer
---

# Changelog

> 🧭 [deployer](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · **Changelog** · [Metrics](./METRICS.md) <!-- nav -->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `deploy/deploy.ts`: basic deployment functionality for RegisterPortal, Domains, and LabNFT — constructor-argument handling, deployer-balance validation before spending on a non-local network, per-deployment console logging, and network selection via Hardhat's `--network` flag. Replaces the four legacy `scripts/*.js` files, which used ethers v5 syntax (`.deployed()`, `.address`, `ethers.utils.parseEther`) incompatible with this project's actual ethers v6 dependency and were unused by any script or doc.
- Slither static analysis: `config/slither.config.json`, `npm run security:slither`, and a CI `slither` job.
- Hardhat v3's native `--coverage` flag wired up as `npm run coverage` (solidity-coverage, the previous intended tool, has no Hardhat v3 support — its `peerDependencies` cap it at `hardhat ^2.11.0`).
- ROADMAP.md "2027" section: a written design for retrofitting UUPS upgradeability onto the existing contracts, deferred rather than implemented this cycle (see ROADMAP.md for the full rationale).

### Changed
- **BREAKING**: `Domains` now inherits OpenZeppelin's `Ownable` instead of a bespoke `owner` state variable + `onlyOwner` modifier. `Domains.withdraw()` now reverts with `OwnableUnauthorizedAccount(address)` instead of the custom `Unauthorized()` error when called by a non-owner. `Domains.owner()` and `Domains.isOwner()` keep the same external signatures.
- CI (`ci.yml`): `coverage` step now runs real Hardhat v3 coverage instead of a no-op `echo` stub; removed the "Check contract sizes" step (called `hardhat-contract-sizer`, a Hardhat-^2.x-only plugin that isn't installed — the step has silently failed every run since the Hardhat v3 migration, masked by `continue-on-error`); added a `slither` job.
- `Dockerfile` no longer does `COPY .env ./.env` — that line required a host `.env` file to exist at build time, which isn't guaranteed (`.env` is gitignored), so `docker compose build` failed on a fresh clone with no local `.env`. Runtime secrets are supplied via `docker-compose.yml`'s existing `.env` volume mount on the services that need them instead.
- `docker-compose.yml`: replaced the now-removed `./scripts` bind mounts with `./deploy`; fixed the `coverage` service's command (`npx hardhat coverage` isn't a real task under Hardhat v3 — coverage is a flag on `test`).
- `package.json`: `deploy:sepolia` / `deploy:mumbai` now run `deploy/deploy.ts` via `hardhat run` — they previously invoked the `hardhat deploy` task from `hardhat-deploy`, which was never registered as a plugin in the active `hardhat.config.mjs` and so did not exist as a runnable task.

### Removed
- `scripts/nftDeploy.js`, `scripts/nftRun.js`, `scripts/registDeploy.js`, `scripts/registRun.js` — broken under ethers v6 (ethers v5 syntax), unreferenced by any other file, superseded by `deploy/deploy.ts`.
- `hardhat.config.cjs` — an unused, dead Hardhat v2-style config (`require("hardhat-deploy")`, CommonJS) incompatible with the installed Hardhat v3; nothing referenced it (the active config is `hardhat.config.mjs`, used via every `--config` flag in `package.json`).

### Fixed
- RegisterPortal's "contract balance depletion" test was a 50/50 coin-flip wrapped in a try/catch that treated both outcomes as passing, so it often never exercised the revert path it was meant to test. Rewritten to be fully deterministic using `networkHelpers.setPrevRandao` (see `test/RegisterPortal.test.ts` for the full explanation) — it now reliably exercises and asserts the low-balance revert on every run.

### Security
- CI Slither job now actually analyzes the contracts (47 contracts, 21 findings incl. 2 High `weak-prng`) and fails if it analyzes 0 — it had been green while checking nothing (#164, #165).
- Patched high-severity Dependabot alerts (#152); `adm-zip` override bumped to 0.6.1 (#158); `js-yaml` 4.3.2 (#153).

### Docs
- Planning docs reset for 2027 (`pmo-ff`): Near/Mid/Long-Term horizons replaced with 2027 Q1, completed items condensed into FEATURES/CHANGELOG, breadcrumb navigation + README docs index added.
- METRICS.md: corrected the "CI/CD Pipeline Success Rate: 0%" figure, which was stale (recent runs are ~98% green — see METRICS.md's investigation note for the `gh run list` evidence); documented that the previous 86.33% coverage figure predates a toolchain change that makes it unverifiable, rather than carrying it forward as current.
- README.md, FEATURES.md: corrected Hardhat version references (were still showing Hardhat 2.x fields despite `package.json` depending on Hardhat 3.x), added Local Development and Security sections, removed a dead link to a `TESTING.md` that was never created.
- `.env.template`: replaced generic, unrelated boilerplate (`DATABASE_URL`, `PORT`, ...) with the environment variables this project's `hardhat.config.mjs` and `deploy/deploy.ts` actually read.

## [1.0.0] - 2025-12

### Added
- Comprehensive test suite with 63 passing tests
- Tests for RegisterPortal, Domains, and LabNFT contracts
- Modern Hardhat toolbox integration
- Gas reporter and solidity coverage support
- TypeScript 5.6 support
- Docker support for containerized development
- Solhint integration for Solidity linting
- Pre-commit hooks for code quality
- Dependabot for automated dependency updates
- Docker Compose for multi-service orchestration

### Changed
- **BREAKING**: Updated to Solidity 0.8.28 from 0.8.4
- **BREAKING**: Migrated to OpenZeppelin Contracts v5.1.0 from v4.9.6
- **BREAKING**: Updated to Ethers.js v6.13.0 from v5.6.5
- Updated Hardhat to v2.22.0 from v2.9.3
- Replaced `Counters` library with simple uint256 counters
- Replaced `block.difficulty` with `block.prevrandao` for randomness
- Updated contract overrides for OpenZeppelin v5 compatibility
- Migrated from deprecated Rinkeby to Sepolia testnet
- Enabled viaIR compiler option for complex contracts

### Deprecated
- Rinkeby network configuration (use Sepolia instead)

### Removed
- Deprecated hardhat-waffle and ethereum-waffle packages
- Old Counters library usage
- Outdated network configurations

### Fixed
- OpenZeppelin v5 compatibility issues
- TypeScript compilation errors
- Contract override function signatures
- Stack too deep errors with viaIR compiler

### Security
- Updated all dependencies to latest stable versions
- Removed vulnerable package versions

## [0.1.0] - 2024-06-10

### Added
- Project initialization with Hardhat.
- Initial smart contract deployment script.

[Unreleased]: https://github.com/Nitsuah-Labs/deployer/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Nitsuah-Labs/deployer/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/Nitsuah-Labs/deployer/releases/tag/v0.1.0