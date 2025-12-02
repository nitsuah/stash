# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** Stash
**Description:** A personal folder of miscellaneous code and designs over the years. Predominantly Visual Basic .NET projects, solutions, and snippets.
**Tech Stack:** Visual Basic .NET

## Code Style & Conventions

### General Guidelines

- Follow existing code patterns and file structure.
- Maintain consistent naming conventions across the codebase.
- Write self-documenting code with clear variable and function names.
- Add comments only when the code's intent is not immediately clear.
- Prefer explicit variable declarations.

### Language-Specific Guidelines

- **Visual Basic .NET**:
    - Use `Option Strict On` and `Option Explicit On` for all projects.
    - Follow Microsoft's .NET coding conventions.
    - Use `Try...Catch` blocks for error handling.
    - Prefer `String.Format` or string interpolation for string formatting.
    - Use meaningful variable names (e.g., `customerName` instead of `cn`).
    - Use properties for accessing and modifying class members.

### File Organization

- Organize projects into meaningful solutions.
- Group related classes into namespaces.
- Use separate files for each class or module.
- Place resource files (e.g., images, icons) in a `Resources` folder.

## Architecture Patterns

- N/A (Due to the miscellaneous nature of the repository, specific architectural patterns may not be consistently applied.)

## Testing Strategy

- Unit tests are encouraged where applicable.
- Use a testing framework like NUnit or MSTest.
- Write tests to cover edge cases and error conditions.
- Aim for high test coverage for critical components.

## Security Considerations

- Never commit secrets, API keys, or credentials.
- Validate all user inputs to prevent injection attacks.
- Use parameterized queries when interacting with databases.
- Implement proper error handling to prevent information leakage.

## Performance Guidelines

- Optimize database queries (use indexes, avoid full table scans).
- Avoid unnecessary object creation.
- Use efficient data structures and algorithms.
- Profile code to identify performance bottlenecks.

## Documentation Requirements

- Update README.md when adding new projects or making significant changes.
- Document complex algorithms or business logic.
- Add comments to code to explain its purpose and functionality.

## Common Pitfalls to Avoid

- Don't ignore exceptions.
- Don't hardcode configuration values.
- Don't use magic numbers.
- Don't write overly complex or convoluted code.
- Don't commit commented-out code.

## Preferred Libraries & Tools

- Visual Studio: The primary IDE for development.
- .NET Framework/.NET: The target framework for applications.
- NUnit/MSTest: Testing frameworks.

## Additional Context

- This repository contains a variety of projects and snippets, so consistency may vary.
- Focus on improving code quality and maintainability where possible.

---

**Note:** These instructions help GitHub Copilot provide more relevant and consistent suggestions. Update this file as project conventions evolve.