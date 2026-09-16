# Tasks

## Todo

- [ ] Basic CLI interface for the deployer (P3, M) — split out of the old "Improve GitHub Actions CI workflow" scope; not started.
- [ ] Design the contract upgradeability mechanism — **implementation** (P2, M). Design is written up in ROADMAP.md's new "2027" section; deferred there rather than shipped as untested proxy/initializer logic (see rationale in that section).
- [ ] Apply gas-optimization findings from the 2026-09 research pass below (P3, S) — no contract code changed this cycle; findings are documented, not yet implemented.
- [ ] Get Slither producing real findings in this sandboxed dev environment (P3, S) — configured (`config/slither.config.json`, `npm run security:slither`, CI `slither` job using `crytic/slither-action`) but this dev sandbox blocks solc's native binary download (both `solc-select` and Hardhat's own solc fetch hit it; Hardhat has a WASM fallback, `solc-select`/crytic-compile do not), so no local run completed. The CI job runs on a normal-network GitHub Actions runner and should work there — check its first run's summary/annotations and record a findings baseline once it does.
- [ ] Deferred: `npm audit` (post fast-uri fix) still flags js-yaml (high, non-major fix available but transitive via a dep that hasn't republished against it), adm-zip (moderate, fix requires downgrading hardhat to 3.11.1), and hardhat/@nomicfoundation/hardhat-mocha (moderate, fix requires a semver-major hardhat downgrade/change). None of these are among the 4 Dependabot alerts fixed in the fast-uri patch; not forcing a Hardhat major-version change without verifying compatibility first (P2, M)

## In Progress

(none)

## Done — 2026-09 cycle

- [x] Implement basic deployment functionality (P1, M) — `deploy/deploy.ts` deploys RegisterPortal, Domains, and LabNFT via Hardhat v3's `network.connect()` + ethers v6, with constructor-argument handling (`DOMAIN_TLD`, `REGISTER_PORTAL_FUNDING` env vars), pre-flight error handling (refuses to spend on a non-local network with a zero-balance deployer), and per-deployment console logging (address, tx hash, gas used). Verified against the local Hardhat network only, per this cycle's ground rules.
- [x] Set up a local development environment with Hardhat (P1, S) — `docker-compose up hardhat-node` and `npx hardhat node --config hardhat.config.mjs` both verified working; documented in README.md.
- [x] Refactoring deployment script for clarity (P2, S) — the four legacy `scripts/*.js` files used ethers v5 syntax (`.deployed()`, `.address`, `ethers.utils.parseEther`) that throws under this repo's actual ethers v6 dependency; they were unused by any script/doc and have been removed in favor of `deploy/deploy.ts`.
- [x] Create deployment scripts for different networks (P2, M) — `deploy/deploy.ts` is network-agnostic (driven by Hardhat's `--network` flag); `npm run deploy`, `deploy:sepolia`, `deploy:mumbai` all point at it.
- [x] Add event logging for important deployment actions (P2, S) — see `deploy/deploy.ts`'s per-contract console logging and final `console.table` summary.
- [x] Implement access control for deployment functions (P2, S) — interpreted as: (1) `deploy/deploy.ts` validates the deployer account before spending anything on a non-local network, and (2) `Domains.withdraw` (the one existing fund-moving admin function) now uses OpenZeppelin's audited `Ownable` instead of a bespoke `owner`/`onlyOwner` pair. RegisterPortal and LabNFT were **not** given a new owner-gated withdraw function — neither contract had an owner concept before, and inventing one now (i.e. a way for a single key to drain RegisterPortal's prize pool) is a new centralization/rug-pull vector this docs-and-roadmap cycle isn't the place to introduce without a dedicated design + audit pass.
- [x] Fix pre-existing RegisterPortal balance depletion test (P3, S) — the test was a 50/50 coin-flip (`register()`'s prize payout depends on a pseudo-random `seed`) wrapped in a try/catch that treated both outcomes as passing, so it frequently never exercised the revert path at all. Rewritten to be fully deterministic: `networkHelpers.setPrevRandao` pins `block.prevrandao` at both deploy time and register time, the exact `seed` the contract will compute is replicated in the test, and the next block's timestamp is chosen so the on-chain formula is guaranteed to land on a "win" against a zero-funded contract — guaranteeing the balance-depletion revert fires every run instead of ~50% of the time.
- [x] Improve GitHub Actions CI workflow (P2, M) — see METRICS.md's CI investigation writeup for what "0%" actually meant. Changes: (1) `coverage` now runs Hardhat v3's native `--coverage` flag instead of an `echo` stub (solidity-coverage, the previous tool, has no Hardhat v3 support); (2) removed the "Check contract sizes" step, which called `hardhat size-contracts` from `hardhat-contract-sizer` — a Hardhat-^2.x-only plugin that isn't installed, so the step has silently failed every run since the Hardhat v3 migration, masked by `continue-on-error: true`; (3) added a `slither` job (see the Slither item above).
- [x] Configure Slither security analysis (P3, M) — `config/slither.config.json`, `npm run security:slither`, and a CI `slither` job added. See the "Todo" item above for why no findings could be gathered from this sandbox and where to look for the first real result.
- [x] Research gas optimization techniques for deployment (P3, S) — findings from reading `contracts/*.sol`, no code changed:
  - `Domains.svgPartOne` / `svgPartTwo` are mutable `string` state variables that never change after deployment; they should be `constant` so they're inlined into bytecode instead of costing an `SLOAD` on every `register()` call.
  - `LabNFT`'s eight trait `string[]` arrays (`skybox`, `location`, ... `blockmod`) and `randomColor` are storage arrays populated at construction, which is why `LabNFT` is by far the most expensive of the three contracts to deploy. Solidity doesn't support `constant`/`immutable` for dynamic array types, so the real fix is architectural (e.g. move trait data off-chain into `tokenURI` metadata generation, or pack traits into a `bytes32` lookup table) rather than a one-line change — flagged for a future cycle, not attempted here.
  - `RegisterPortal.getAllRegisters()` and `Domains.getAllNames()` both copy an unbounded array to memory in a `view` call; fine today at this scale, but both are O(n) and will eventually hit the block gas limit for `eth_call` on public RPC providers as the arrays grow. Consider paginated getters if either contract sees real usage.
  - `LabNFT.mintNFT`'s minting loop (`for(uint256 i; i < num; i++)`) could use an `unchecked` increment since `num < 11` is already enforced by an earlier `require`, making overflow impossible — minor savings, not applied here to avoid touching minting logic in a docs-focused cycle.

## Done — earlier cycles

- [x] Created initial project structure using Hardhat (P1, S)
- [x] Fix all vulnerabilities - 0 vulnerabilities via npm overrides (P1, L)
- [x] Patch 4 high-severity Dependabot alerts (fast-uri < 3.1.6, GHSA-jqff-g426-hqxp / GHSA-f65p-4m7j-42xc / GHSA-fph4-wmhf-6fwf / GHSA-5jgf-p345-68v8) via `fast-uri` npm override to ^3.1.6; verified with 63/63 tests passing (P1, S)
- [x] Write unit tests for the core contract logic - 63 passing tests (P1, L)
- [x] Docker containerization for development environment (P2, M)
- [x] Solhint integration for Solidity linting (P2, S)
- [x] Pre-commit hooks for automated code quality checks (P2, M)
- [x] Dependabot configuration for automated dependency updates (P2, S)
- [x] Docker Compose multi-service orchestration (P2, M)
- [x] Updated documentation with testing and Docker examples (P2, M)
