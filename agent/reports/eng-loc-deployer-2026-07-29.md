# ENG LOC Report — deployer (2026-07-29)

> 🧭 [[repos/deployer|deployer]] <!-- nav -->

**Thresholds**: `max_lines=500`, `min_lines=30`
**Extensions**: `.ts`, `.tsx`, `.js`, `.jsx`, `.py`, `.go`, `.rs`, `.java`, `.cs`, `.php`, `.rb`, `.swift`, `.kt`, `.scala`, `.vue`, `.svelte`
**Excluded**: `node_modules/`, `.git/`, `dist/`, `build/`, `.next/`, `.claude/worktrees/`, `.playwright-mcp/`, `.venv/`, `venv/`, `env/`

---

## 🔴 Too Large (> 500 lines) — Refactor Candidates

| Lines | File | Secondary Scan Notes |
|-------|------|---------------------|
| 811 | deployer/types/ethers-contracts/factories/LabNFT__factory.ts | Generated factory - check if generated |
| 781 | deployer/types/ethers-contracts/factories/Domains__factory.ts | Generated factory |
| 700 | deployer/types/ethers-contracts/factories/emojis.sol/MyToken__factory.ts | Generated factory |
| 549 | deployer/types/ethers-contracts/LabNFT.ts | Contract type - check if generated |
| 547 | deployer/types/ethers-contracts/Domains.ts | Contract type |

---

## 🟢 Too Small (< 30 lines) — Merge Candidates

| Lines | File | Suggested Merge Target |
|-------|------|------------------------|
| 1 | deployer/config/hardhat.config.js | Check if config |
| 4 | deployer/types/ethers-contracts/factories/emojis.sol/index.ts | Merge with factories barrel |
| 4 | deployer/types/ethers-contracts/emojis.sol/index.ts | Merge with emojis barrel |
| 7 | deployer/types/ethers-contracts/factories/RegisterPortal__factory.ts | Merge with factories |
| 14 | deployer/types/ethers-contracts/factories/index.ts | Merge with factories barrel |
| 14 | deployer/examples/getBal/deploy/001_deploy_greeter.ts | Check if deploy script |
| 14 | deployer/examples/getBal/test/Greeter.test.ts | Merge with tests |
| 14 | deployer/examples/getBal/deploy/002_deploy_balance-read.ts | Check if deploy script |
| 15 | deployer/examples/getBal/test/BalanceReadTest.test.ts | Merge with tests |
| 23 | deployer/scripts/registDeploy.js | Check if script |
| 23 | deployer/scripts/nftDeploy.js | Check if script |
| 29 | deployer/scripts/registRun.js | Check if script |

---

*Generated: 2026-07-29*
