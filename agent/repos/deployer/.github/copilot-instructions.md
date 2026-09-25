# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** Wave Portal Contract
**Description:** Wave portal contract. Allows users to send "waves" and messages, recorded on the blockchain.
**Tech Stack:** Solidity

## Code Style & Conventions

### General Guidelines

- Follow existing code patterns and file structure.
- Use Solidity best practices for security and gas efficiency.
- Write NatSpec comments for all functions and events.
- Keep functions short and focused on a single responsibility.

### Solidity-Specific Guidelines

- Use Solidity version ^0.8.0.
- Use `SPDX-License-Identifier` at the top of each file.
- Prefer `require` statements for input validation.
- Use `emit` to generate events.
- Follow the style guide from the Solidity documentation.

### File Organization

- Contract files should be named with `.sol` extension.
- Interfaces should be defined in separate files.
- Place tests in a `test/` directory.

## Architecture Patterns

- This is a simple contract, so keep the architecture straightforward.
- Focus on gas optimization and security.
- Use modifiers to enforce access control.

## Testing Strategy

- Write unit tests for all functions.
- Aim for 100% test coverage.
- Use Hardhat for testing.
- Test all edge cases and potential vulnerabilities.

## Security Considerations

- Prevent reentrancy attacks.
- Protect against integer overflows and underflows (Solidity 0.8+ handles this by default).
- Validate all inputs to prevent unexpected behavior.
- Follow security best practices from Consensys and OpenZeppelin.

## Performance Guidelines

- Optimize gas usage.
- Avoid unnecessary state changes.
- Use efficient data structures.

## Documentation Requirements

- Update NatSpec comments when adding new functions or changing existing ones.
- Update README.md with any important changes.

## Common Pitfalls to Avoid

- Avoid using `transfer` or `send` for sending Ether (use `call` instead).
- Don't use `assert` for input validation (use `require` instead).
- Don't store sensitive data on the blockchain.
- Don't assume that `block.timestamp` is accurate (it can be manipulated by miners).

## Preferred Libraries & Tools

- Hardhat: For development, testing, and deployment.
- OpenZeppelin Contracts: For secure and reusable smart contract components (use sparingly, only when necessary).
- Ethers.js or Web3.js: For interacting with the contract from client-side applications.

## Additional Context

- This contract is deployed on [TODO: SPECIFY_NETWORK].
- The contract address is [TODO: SPECIFY_CONTRACT_ADDRESS].
- Use `npx hardhat compile` to compile the contract.
- Use `npx hardhat test` to run the tests.

## Commit Conventions

- Use conventional commits: `feat: add new wave function`, `fix: prevent reentrancy attack`, `docs: update README.md`.

## Examples

**Good:**

```solidity
/**
 * @dev Sends a wave to the contract.
 * @param _message The message to send with the wave.
 */
function wave(string memory _message) public {
    require(bytes(_message).length > 0, "Message cannot be empty");
    totalWaves++;
    emit NewWave(msg.sender, _message, block.timestamp);
}
```

**Bad:**

```solidity
function wave(string message) public { // Missing NatSpec
    totalWaves++;
    emit NewWave(msg.sender, message); // Missing timestamp
}
```

---

**Note:** These instructions help GitHub Copilot provide more relevant and consistent suggestions. Update this file as project conventions evolve.