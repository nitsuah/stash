# Roadmap

## Near Term (0-3 months)

- [x] Project setup and architecture
- [x] Fix all vulnerabilities or refactor (0 vulnerabilities via npm overrides)
- [x] Docker containerization for development
- [x] Solhint integration for code quality
- [x] Pre-commit hooks implementation
- [x] Automated dependency management with Dependabot
- [x] **Core Contract Development:** Implement basic deployment functionality for simple Solidity contracts. Rationale: Provides initial deployer capability. Scope: Handling constructor arguments, basic error handling. Success: Contracts deploy successfully to a test network. Risks: Solidity version incompatibilities. **Shipped 2026-09:** `deploy/deploy.ts` deploys RegisterPortal, Domains, and LabNFT with per-contract constructor args, deployer-balance validation, and per-network behavior (see TASKS.md).
- [ ] **Basic CLI Interface:** Develop a command-line interface for interacting with the deployer. Rationale: Simplifies deployment process. Scope: Deploy command, network configuration. Success: Users can deploy contracts via the CLI. Risks: CLI usability issues.
- [x] **Test Network Integration:** Integrate with a local test network (e.g., Ganache, Hardhat). Rationale: Facilitates testing and development. Scope: Network configuration, deployment scripts. Success: Contracts deploy seamlessly to the test network. Risks: Test network instability. **Shipped 2026-09:** documented in README.md's "Local Development" section; `docker-compose up hardhat-node` and `npx hardhat node` both verified working.

## Mid Term (3-6 months)

- [ ] **Advanced Deployment Options:** Add support for more complex deployment scenarios (e.g., proxy contracts, upgradeable contracts). Rationale: Expands deployer capabilities. Scope: Proxy pattern implementation, upgradeability logic. Success: Complex contracts deploy correctly. Risks: Security vulnerabilities in proxy implementation. **See the "2027" section below** — retrofitting upgradeability onto contracts that were never designed for it (no storage-gap planning, value-holding constructors) is a genuinely novel, high-risk change deferred to a dedicated security-review cycle rather than shipped here.
- [ ] **Configuration Management:** Implement a configuration system for managing deployment settings. Rationale: Improves flexibility and reusability. Scope: Configuration files, environment variables. Success: Users can easily configure deployment parameters. Risks: Configuration complexity.
- [ ] **Gas Optimization:** Implement gas optimization techniques in the deployment process. Rationale: Reduces deployment costs. Scope: Bytecode optimization, gas estimation. Success: Deployment gas costs are reduced. Risks: Potential for breaking changes. **Research completed 2026-09** (see TASKS.md); no contract code changed this cycle — findings are documented, not yet implemented.
- [x] **Security Audits:** Conduct initial security audits of the core contract and CLI. Rationale: Identifies and mitigates potential vulnerabilities. Scope: Static analysis, manual review. Success: Security vulnerabilities are identified and addressed. Risks: Audit findings require significant rework.
- [x] **Access Control:** Standardize admin-only contract functions on OpenZeppelin's audited `Ownable`. **Shipped 2026-09:** `Domains.withdraw` now uses OZ `Ownable` instead of a bespoke owner mapping (see CHANGELOG.md). RegisterPortal and LabNFT intentionally left without an owner-gated withdraw path — see TASKS.md for why adding one was judged out of scope.

## Long Term (6-12 months)

- [x] **Multi-Network Support:** Expand support to multiple blockchain networks (e.g., Ethereum mainnet, Polygon). Rationale: Increases deployer adoption. Scope: Network-specific configurations, cross-chain compatibility. Success: Contracts deploy seamlessly to multiple networks. Risks: Network-specific issues.
- [x] **Automated Testing:** Implement a comprehensive suite of automated tests (63 tests). Rationale: Ensures code quality and stability. Scope: Unit tests, integration tests. Success: Code changes are automatically tested. Risks: Test coverage gaps.
- [ ] **UI/UX Improvements:** Develop a more user-friendly interface (e.g., web UI). Rationale: Improves user experience. Scope: Web interface design, deployment workflows. Success: Users find the deployer easy to use. Risks: UI development delays.
- [ ] **Community Contributions:** Encourage and support community contributions. Rationale: Fosters wider adoption and innovation. Scope: Contribution guidelines, issue tracking. Success: Community members actively contribute to the project. Risks: Lack of community engagement.

## 2027

### Contract upgradeability — design (implementation deferred)

TASKS.md carried "Design the contract upgradeability mechanism (P2, M)" into
this cycle. After reviewing the three existing contracts, implementation is
deferred to 2027 rather than shipped now: none of RegisterPortal, Domains, or
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
   introduced this cycle for `Domains` (see "Mid Term" above), extended to
   RegisterPortal and LabNFT if they adopt upgradeability.
5. Require a passing Slither run (see TASKS.md) plus a manual review of the
   storage-layout diff as a merge gate for every upgrade, not just the
   initial rollout.
6. Ship behind a new contract file (e.g. `RegisterPortalUpgradeable.sol`)
   rather than modifying the existing contracts in place, so the
   non-upgradeable versions remain available and this is an additive,
   revertible change.

## Completed Milestones

- [x] Project setup and architecture
- [x] Comprehensive test suite (63 passing tests)
- [x] Security vulnerability fixes (0 vulnerabilities)
- [x] Docker containerization
- [x] Code quality tooling (Solhint, pre-commit hooks)
- [x] Automated dependency management (Dependabot)
- [x] Multi-network support (Ethereum, Polygon, Sepolia, Mumbai)
- [x] Modern toolchain migration (Solidity 0.8.28, OpenZeppelin v5, Ethers v6)