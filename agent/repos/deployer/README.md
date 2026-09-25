---
up: "[[repos/deployer]]"
source: https://github.com/Nitsuah-Labs/deployer/blob/main/README.md
kind: repo-doc
repo: deployer
---

# Contract Safe

> 🧭 **deployer** · [Features](./docs/FEATURES.md) · [Roadmap](./docs/ROADMAP.md) · [Tasks](./docs/TASKS.md) · [Changelog](./docs/CHANGELOG.md) · [Metrics](./docs/METRICS.md) <!-- nav -->

[![CI](https://github.com/Nitsuah-Labs/deployer/actions/workflows/ci.yml/badge.svg)](https://github.com/Nitsuah-Labs/deployer/actions)

Nitsuah Labs Contract Safe - A collection of Solidity smart contracts including Wave Portal, Domain Name Service, and NFT collections.

## 🚀 Tech Stack

- **Solidity**: ^0.8.28
- **Hardhat**: ^3.15.0
- **OpenZeppelin Contracts**: ^5.6.1
- **Ethers.js**: ^6.17.0
- **TypeScript**: ^7.0.2

## 📦 Installation

```bash
npm install
```

## 🔨 Commands

```bash
# Compile contracts
npm run compile

# Run tests
npm test

# Run tests with coverage (Hardhat v3's built-in --coverage flag;
# solidity-coverage doesn't support Hardhat v3, so it isn't used here)
npm run coverage

# Lint Solidity contracts
npm run lint

# Clean artifacts
npm run clean

# Deploy (defaults to the local Hardhat network — see "Local Development" below)
npm run deploy
npm run deploy:sepolia
npm run deploy:mumbai

# Verify contracts
npm run verify:sepolia
npm run verify:mumbai

# Static analysis (see "Security" below)
npm run security:slither

# Other Hardhat commands
npx hardhat accounts --config hardhat.config.mjs
npx hardhat node --config hardhat.config.mjs
npx hardhat help
```

## 🖥️ Local Development

This repo's `hardhat` network (used by `npm test` and by default for
`npm run deploy`) is an in-process, ephemeral chain — nothing to start. For a
persistent local node you can point external tools (e.g. MetaMask) at:

```bash
npx hardhat node --config hardhat.config.mjs
# or, via Docker:
docker compose up hardhat-node
```

Then, in a second terminal, deploy against it:

```bash
npx hardhat run deploy/deploy.ts --config hardhat.config.mjs --network localhost
```

`deploy/deploy.ts` deploys RegisterPortal, Domains, and LabNFT with sensible
local defaults (see its header comment and `.env.template` for the env vars
that override them). It refuses to send funds on any non-local network
without a funded `PRIVATE_KEY`.

### 🐳 Docker Commands

```bash
# Start local Hardhat node
docker compose up hardhat-node

# Run tests in Docker
docker compose run --rm test

# Run coverage in Docker
docker compose --profile coverage run --rm coverage

# Build Docker image
docker compose build
```

## 🧪 Testing

Comprehensive test suite with 63 passing tests covering:

- **RegisterPortal**: Wave registration, cooldown periods, prize distribution
- **Domains**: Domain registration, pricing, records management, withdrawals
- **LabNFT**: NFT minting, attributes, enumeration, transfers, approvals

Run them with `npm test` (or `docker compose run --rm test`). All tests run
against the local, in-process `hardhat` network — nothing is ever sent to a
real network as part of testing.

## 🛡️ Security

- **Solhint** (`npm run lint`) enforces Solidity style and common
  best-practice rules on every commit and in CI.
- **Slither** (`npm run security:slither`, or the `slither` CI job) runs
  static analysis with Trail of Bits' detector suite. Configuration lives in
  `config/slither.config.json`.

## 📝 Smart Contracts

### RegisterPortal

Wave portal contract allowing users to send "waves" and messages recorded on the blockchain with random prize distribution.

### Domains

Domain name service (DNS) contract with dynamic pricing based on name length, SVG-based NFTs, and on-chain metadata.

### LabNFT

Generative NFT collection with randomized attributes and animated SVG visuals.

## 🌐 Networks

- **Ethereum Mainnet**
- **Sepolia Testnet** (replaces deprecated Rinkeby)
- **Polygon Mainnet**
- **Mumbai Testnet**

## 🔐 Environment Variables

Create a `.env` file with:

```env
PRIVATE_KEY=your_private_key
SEPOLIA_RPC_URL=your_sepolia_rpc_url
MUMBAI_RPC_URL=your_mumbai_rpc_url
ETH_RPC_URL=your_ethereum_rpc_url
POLYGON_RPC_URL=your_polygon_rpc_url
ETHERSCAN_API_KEY=your_etherscan_api_key
POLYGONSCAN_API_KEY=your_polygonscan_api_key
```

## 📚 Learning Resources

- [Buildspace - Wave Portal](https://buildspace.so/p/CO02cf0f1c-f996-4f50-9669-cf945ca3fb0b/lessons/LE8f43618f-ffae-44ef-892b-2600adb2eba7)
- [Buildspace - NFT Collection](https://buildspace.so/p/mint-nft-collection/lessons/LE8ed42760-6bec-415a-b2bc-4987858c99ad)

## 🔧 Development Tools

- **Solhint**: Solidity linting with best practices
- **Hardhat's built-in coverage**: `--coverage` flag, no external plugin needed under Hardhat v3
- **Slither**: static analysis (`npm run security:slither`)
- **Docker**: Containerized development environment
- **Pre-commit Hooks**: Automated code quality checks
- **Dependabot**: Automated dependency updates

## 🔄 Recent Updates (September 2026)

- ✅ Migrated to Hardhat v3 (`hardhat.config.mjs`, ESM-only, native ethers v6 network connections)
- ✅ Added `deploy/deploy.ts`: basic deployment functionality for RegisterPortal, Domains, and LabNFT, network-agnostic via `--network`
- ✅ `Domains` access control migrated from a bespoke owner pattern to OpenZeppelin's `Ownable`
- ✅ Switched test/CI coverage to Hardhat v3's native `--coverage` flag (solidity-coverage has no Hardhat v3 support)
- ✅ Configured Slither static analysis (local script + CI job)
- ✅ Fixed a flaky, non-deterministic RegisterPortal test
- ✅ Removed dead/broken legacy deployment scripts and an unused Hardhat v2-only config file
- ✅ Fixed a Docker build regression (`Dockerfile` required a host `.env` file that isn't guaranteed to exist)

<details>
<summary>December 2025</summary>

- ✅ Updated to Solidity 0.8.28
- ✅ Migrated to OpenZeppelin v5.1.0
- ✅ Updated to Ethers.js v6.13.0
- ✅ Replaced deprecated packages with @nomicfoundation/hardhat-toolbox
- ✅ Added comprehensive test suite (63 tests)
- ✅ Updated to modern TypeScript 5.6
- ✅ Migrated from Rinkeby to Sepolia testnet
- ✅ Added Docker support for development
- ✅ Integrated Solhint for code quality
- ✅ Fixed all security vulnerabilities

</details>

## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:
- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md

<!-- docs-index:start -->

## Docs Index

Every doc at the repo root (other than this README) and under `docs/` (the files mirrored into the Obsidian vault), so none of them is orphaned.

- [Changelog](./docs/CHANGELOG.md) — `docs/CHANGELOG.md`
- [Features](./docs/FEATURES.md) — `docs/FEATURES.md`
- [Metrics for Nitsuah-Labs/deployer](./docs/METRICS.md) — `docs/METRICS.md`
- [Roadmap](./docs/ROADMAP.md) — `docs/ROADMAP.md`
- [Tasks](./docs/TASKS.md) — `docs/TASKS.md`

<!-- docs-index:end -->
