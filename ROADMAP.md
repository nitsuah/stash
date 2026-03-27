# Roadmap

Last Updated: 2026-03-27

## Near Term (0-3 Months)

- [ ] **Codebase Review & Refactor:** Review existing code for clarity, consistency, and adherence to .NET best practices. Rationale: Improve maintainability and reduce technical debt. Scope: Focus on core modules. Success: Codebase follows consistent style and has improved documentation. Risks: Time constraints may limit scope.
- [ ] **Project Documentation:** Create a basic README file and initial project documentation. Rationale: Onboarding and future development. Scope: Project overview, setup instructions, and contribution guidelines. Success: Comprehensive README and initial documentation. Risks: Documentation may become outdated quickly.
- [ ] **Dependency Management:** Review and update NuGet package dependencies. Rationale: Security and stability. Scope: Identify outdated packages and update to latest stable versions. Success: All dependencies are up-to-date and compatible. Risks: Potential breaking changes in updated packages.
- [ ] **Architecture Baseline:** Create `ARCHITECTURE.md` documenting module boundaries, execution context, and dependency map for `atlassian/`, `git/`, `ias/`, `projects/`, and `windows/` (P1)
- [ ] **Script Runbook:** Add safety matrix and runbook in `README.md` — prerequisites, parameters, dry-run paths, and risk notes per script family (P1)
- [ ] **Security Hygiene Pass:** Run and record a sensitive-data and hardcoded-hostname scan; remediate findings and harden `.gitignore` where needed (P0)

## Mid Term (3-6 Months)

- [ ] **GUI Enhancement:** Improve the user interface of existing Visual Basic .NET applications within the stash. Rationale: Enhance usability and visual appeal. Scope: Focus on frequently used applications. Success: Improved user experience and visual design. Risks: Subjective user preferences may be difficult to satisfy.
- [ ] **Basic Testing Framework:** Implement a basic unit testing framework for core components. Rationale: Improve code quality and prevent regressions. Scope: Focus on key algorithms and data structures. Success: Unit tests cover critical functionality. Risks: Difficulty in writing effective unit tests for legacy code.
- [ ] **Configuration Management:** Implement a configuration management system (e.g., using app.config or settings files). Rationale: Improve flexibility and maintainability. Scope: Allow users to customize application behavior without modifying code. Success: Configuration settings are easily managed and updated. Risks: Complexity in managing configuration settings across multiple applications.
- [ ] **Naming and Consistency Cleanup:** Normalize anomalous filenames (e.g. `ias/Windows-userdata..yml`) and tighten cross-reference accuracy across docs/scripts (P2)
- [ ] **Lightweight Validation Harness:** Define repeatable smoke checks for high-impact scripts (dry-run where possible); produce decision record on feasibility (P2)

## Long Term (6-12 Months)

- [ ] **Modularization:** Break down large applications into smaller, more manageable modules. Rationale: Improve code organization and reusability. Scope: Focus on applications with complex functionality. Success: Code is organized into well-defined modules with clear interfaces. Risks: Requires significant refactoring effort.
- [ ] **Data Persistence:** Implement data persistence mechanisms (e.g., using SQL Server or XML files). Rationale: Allow applications to store and retrieve data. Scope: Focus on applications that require data storage. Success: Data is stored and retrieved reliably. Risks: Data corruption or loss.
- [ ] **Error Handling & Logging:** Implement robust error handling and logging mechanisms. Rationale: Improve debugging and troubleshooting capabilities. Scope: Capture and log errors, warnings, and informational messages. Success: Errors are logged and can be easily analyzed. Risks: Overly verbose logging can impact performance.
- [ ] **Cross-Repo Automation Catalog:** Publish a discoverable catalog of script capabilities and ownership metadata; pilot with one script family (P3)
- [ ] **Operational Metrics Maturity:** Define measurable quality metrics grounded in executable checks with collection method and feasibility assessment (P3)

## Completed Milestones

- [x] Project setup and architecture
- [x] Initial repository bootstrap and governance baseline (`LICENSE`, `SECURITY.md`, `.github` templates present)
- [x] PMO audit and planning alignment — repository structure validated, docs re-aligned to actual repo scope