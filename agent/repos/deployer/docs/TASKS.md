---
up: "[[repos/deployer]]"
source: https://github.com/Nitsuah-Labs/deployer/blob/main/docs/TASKS.md
kind: repo-doc
repo: deployer
---

# Tasks

> 🧭 [deployer](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · **Tasks** · [Changelog](./CHANGELOG.md) · [Metrics](./METRICS.md) <!-- nav -->

Last Updated: 2026-09-24

## Todo

- [ ] Basic CLI interface for the deployer (P3, M) — split out of the old "Improve GitHub Actions CI workflow" scope; not started.
- [ ] Design the contract upgradeability mechanism — **implementation** (P2, M). Design is written up in ROADMAP.md's "Design Notes: Contract Upgradeability" (2027 Q1); deferred there rather than shipped as untested proxy/initializer logic (see rationale in that section).
- [ ] Apply gas-optimization findings from the 2026-09 research pass below (P3, S) — no contract code changed this cycle; findings are documented, not yet implemented.
- [ ] **[2027-Q1]** Triage the Slither baseline, then gate CI on High findings (P2, S · Type: Security · Confidence: High). The 2026-09-24 run reported **2 High**, both `weak-prng`: `RegisterPortal` seeds from `block.prevrandao + block.timestamp` at `RegisterPortal.sol#28` and `#49`. Acceptable if the seed only picks cosmetic traits; not acceptable if it decides anything of value. It also reported **2 Medium**: `locked-ether`, and `divide-before-multiply` in `libs/Base64.sol`, which is usually intentional in Base64 encoders. Acceptance criteria: each finding is fixed or explicitly suppressed with a `// slither-disable-next-line` and a rationale, then `scripts/slither-check.py` exits non-zero on any High.
- [ ] Deferred: `npm audit` (post fast-uri fix) still flags js-yaml (high, non-major fix available but transitive via a dep that hasn't republished against it), adm-zip (moderate, fix requires downgrading hardhat to 3.11.1), and hardhat/@nomicfoundation/hardhat-mocha (moderate, fix requires a semver-major hardhat downgrade/change). None of these are among the 4 Dependabot alerts fixed in the fast-uri patch; not forcing a Hardhat major-version change without verifying compatibility first (P2, M). Partly addressed since: js-yaml 4.3.2 (#153) and adm-zip override 0.6.1 (#158) — re-run `npm audit` in Docker to confirm what's left before closing.

## In Progress

(none)

## Done

Condensed into `docs/ROADMAP.md` (milestones), `docs/FEATURES.md` (shipped
capabilities), and `CHANGELOG.md` (change-by-change history, including the
2026-09 cycle's deployment script, CI/Slither, and Ownable migration work) —
see those files rather than a duplicated narrative here.
