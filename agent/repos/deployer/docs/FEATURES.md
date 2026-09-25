---
up: "[[repos/deployer]]"
source: https://github.com/Nitsuah-Labs/deployer/blob/main/docs/FEATURES.md
---

# Features

> 🧭 [deployer](../README.md) · **Features** · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

## Core Functionality

- **Smart Contract Deployment** - Deploys smart contracts to Ethereum and Polygon networks.
- **Network Selection** - Supports Mainnet (Ethereum, Polygon) and Testnets (Sepolia, Mumbai).
- **Multiple Contract Types**:
  - **RegisterPortal**: Wave registration with prize distribution
  - **Domains**: On-chain domain name service with NFT integration
  - **LabNFT**: Generative NFT collection with dynamic attributes
- **Deployment Scripts** - `deploy/deploy.ts` handles constructor args, error handling, and per-network deployment for all three contract types (see TASKS.md).
- **Contract Verification** - Etherscan/Polygonscan verification is wired into `hardhat.config.mjs`'s `etherscan` block but the `verify:*` npm scripts are currently disabled (`hardhat-verify` is not registered as an active plugin) — treat this as configured-but-not-yet-enabled, not shipped.

## Technology Stack

- **Solidity 0.8.28** - Latest Solidity with enhanced security features
- **Hardhat 3.15.0** - Modern development environment, ESM-only, native ethers v6 network connections
- **OpenZeppelin 5.6.1** - Secure, audited contract libraries
- **Ethers.js v6** - Latest Web3 interaction library
- **TypeScript 7.0** - Type-safe development

## Integrations

- **Ethers.js v6** - Modern contract deployment and interaction, via Hardhat v3's native `network.connect()`.
- **OpenZeppelin Contracts** - Battle-tested contract standards (ERC721, Ownable, etc.).
- **Gas Reporter** - Detailed gas usage analytics (`REPORT_GAS=true npm test`).
- **Hardhat's built-in coverage** - `--coverage` flag; the `solidity-coverage` plugin previously referenced here has no Hardhat v3 support and isn't installed.

Not currently integrated, despite being listed as a devDependency: **`hardhat-deploy`** — its Hardhat v3 support (v2.x) is built on a separate "rocketh" toolchain with additional peer dependencies this repo doesn't install, and it isn't registered as a plugin in `hardhat.config.mjs`. `deploy/deploy.ts` uses Hardhat's native ethers integration instead, deliberately avoiding that dependency. **TypeChain** was also removed at some point (see comments in `test/*.test.ts`); tests use plain `ethers.Contract` typing instead.

## UI/UX

None — this is a Solidity contract + Hardhat tooling repo with no web interface. (A previous version of this file described a "Deployment Dashboard"; no such UI exists in this codebase, so the claim was removed rather than left as aspirational.)

## Testing & Quality

- **Comprehensive Test Suite** - 63 passing tests covering all major contracts (verified in Docker as part of the 2026-09 roadmap cycle).
- **Test Categories**:
  - RegisterPortal: 15+ tests (registration, cooldowns, prizes, edge cases)
  - Domains: 20+ tests (DNS operations, pricing, withdrawals, access control)
  - LabNFT: 28+ tests (minting, attributes, transfers, SVG generation)
- **Gas Usage Reporting** - Detailed gas consumption analysis.
- **Coverage** - Hardhat v3's native `--coverage` flag (`npm run coverage`); see METRICS.md for the most recently measured numbers.
- **viaIR Compilation** - Advanced optimization for complex contracts.
- **Solhint Linting** - Automated code quality and best practices enforcement.
- **Pre-commit Hooks** - Catch issues before commit (linting, formatting, security).
- **Docker Testing** - Run tests in containerized environment.
- **Slither Static Analysis** - `npm run security:slither` / CI `slither` job analyzes `contracts/` with solc 0.8.28 (47 contracts, 21 findings baseline on 2026-09-24) and fails if it ever analyzes 0 contracts; High-finding gate tracked in TASKS.md.

## Security

- **OpenZeppelin v5** - Latest audited security libraries.
- **Modern Solidity** - 0.8.28 with built-in overflow protection.
- **Access Control** - Ownable contracts for admin functions.
- **Custom Errors** - Gas-efficient error handling (Unauthorized, InvalidName, etc.).
- **Reentrancy Protection** - Safe external calls using `call{value: amount}("")` pattern.
- **Input Validation** - Comprehensive validation on all user inputs.
- **Environment Security** - `.env` files excluded from version control.
- **Random Number Generation** - Uses `block.prevrandao` instead of deprecated `block.difficulty`.

## Infrastructure

- **Docker Support** - Containerized Hardhat development environment.
- **Docker Compose** - Multi-service orchestration (node, test, coverage).
- **Pre-commit Hooks** - Automated quality checks before commits.
- **Dependabot** - Automated security updates and dependency management.
- **Solhint** - Solidity-specific linting with best practices rules.
- **CI-Ready** - Infrastructure ready for GitHub Actions integration.

## Developer Experience

- **Well-Documented Codebase** - Comprehensive documentation and code comments.
- **Example Deployment Scripts** - Provides example scripts for common deployment scenarios.
- **Clear Error Messages** - Returns informative error messages to assist with debugging.
- **Reproducible Environment** - Docker ensures consistent development setup.
- **Automated Code Quality** - Linting and formatting enforced via pre-commit hooks.
- **Testing Documentation** - See README.md's "Testing" section (a previously-referenced `TESTING.md` was never created; the dead link has been removed).