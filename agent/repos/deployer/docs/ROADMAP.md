# Roadmap

> 🧭 [deployer](../README.md) · [Features](./FEATURES.md) · **Roadmap** · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

> 2027 planning reset (2026-09-24): the old Near/Mid/Long-Term horizons and the "Completed Milestones" list were
> replaced with quarter sections. Shipped items (project setup, 0-vuln overrides, Docker, Solhint, pre-commit,
> Dependabot, core deployment script, Hardhat test-network integration, security audit, OZ `Ownable` access control,
> multi-network support, 63-test suite, Solidity 0.8.28/OZ v5/ethers v6 migration, CI Slither that actually analyzes
> the contracts) are condensed in [FEATURES](./FEATURES.md) / [CHANGELOG](./CHANGELOG.md). Every open item was carried
> into 2027 Q1 below.

## 2027 Q1 - Security Gate & Upgradeability (Planned)

### Committed

- [ ] **Slither High findings gate** — triage the 2026-09-24 baseline (2 High `weak-prng` in `RegisterPortal`, 2 Medium), fix or suppress each with rationale, then fail CI on any High. Prerequisite for any upgradeability work.
- [ ] **Contract upgradeability — implementation** *(carried from Mid Term "Advanced Deployment Options")* — UUPS retrofit per the design below, shipped as additive `*Upgradeable.sol` contracts behind a dedicated security review.
- [ ] **Apply gas-optimization findings** *(carried from Mid Term; research done 2026-09, see TASKS.md)*.
- [ ] **Basic CLI interface** *(carried from Near Term)* — deploy command + network configuration on top of `deploy/deploy.ts`.
- [ ] **Configuration management** *(carried from Mid Term)* — config files/env for deployment parameters, reusable across networks.

### Exploratory

- [ ] **Web UI for deployments** *(carried from Long Term "UI/UX Improvements")*.
- [ ] **Community contributions** *(carried from Long Term)* — contribution guidelines + issue tracking; low priority while the repo is private.

## Design Notes: Contract Upgradeability (for the 2027 Q1 item above)

TASKS.md carried "Design the contract upgradeability mechanism (P2, M)" into
this cycle. After reviewing the three existing contracts, implementation is
deferred to 2027 rather than shipped in 2026-09: none of RegisterPortal, Domains, or
LabNFT were built with upgradeability in mind, and retrofitting it safely is
a bigger, riskier change than a docs-and-roadmap cycle should ship without a
dedicated security-review pass. The design below is the plan for that pass.

**Why not now:**
- All three constructors are `payable` and/or take constructor args that
  would need to move to an `initialize()` function — a mechanical but
  error-prone change (initializer front-running, double-init guards).
- None of the contracts reserve storage gaps, so inserting new state in a
  future version risks corrupting storage laid out by proxies deployed
  against today's layout.
- RegisterPortal and Domains both hold user funds (prize pool / registration
  fees). An upgradeable proxy is a strictly larger attack surface for
  contracts that already move value — it deserves its own audit, not a
  drive-by conversion.

**Proposed approach when this is picked up:**
1. Use OpenZeppelin's UUPS pattern (`UUPSUpgradeable` + `Initializable`) over
   the Transparent Proxy pattern — lower runtime gas overhead and the
   upgrade authorization lives in the implementation, which is easier to
   reason about for a small team.
2. Convert each `constructor` to an `initialize()` function guarded by
   `initializer`; deploy via `@openzeppelin/hardhat-upgrades`'s
   `deployProxy`, which also validates storage-layout compatibility on
   every subsequent `upgradeProxy` call.
3. Add explicit `uint256[50] private __gap;` storage gaps to each contract
   before this ships, so future additions don't shift inherited storage
   slots.
4. Gate `_authorizeUpgrade` behind the same `Ownable` access control
   introduced in 2026-09 for `Domains`, extended to
   RegisterPortal and LabNFT if they adopt upgradeability.
5. Require a passing Slither run (see TASKS.md) plus a manual review of the
   storage-layout diff as a merge gate for every upgrade, not just the
   initial rollout.
6. Ship behind a new contract file (e.g. `RegisterPortalUpgradeable.sol`)
   rather than modifying the existing contracts in place, so the
   non-upgradeable versions remain available and this is an additive,
   revertible change.
