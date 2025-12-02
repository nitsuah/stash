# Contributing to stash

Thank you for your interest in contributing! We welcome contributions from everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)
- [Issues](#issues)
- [Pull Requests](#pull-requests)
- [Branching](#branching)
- [Commit Messages](#commit-messages)
- [Testing](#testing)
- [Linting](#linting)
- [Releases](#releases)

## 🤝 Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [maintainer@email.com].  See the full [Code of Conduct](CODE_OF_CONDUCT.md).

## 🚀 Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/stash.git
   cd stash
   ```
3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/nitsuah/stash.git
   ```
4. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💡 How to Contribute

### Types of Contributions

- **Bug fixes**: Fix issues or problems in the codebase
- **New features**: Add new functionality or capabilities
- **Documentation**: Improve or add to project documentation

### Before You Start

- Check existing [issues](../../issues) and [pull requests](../../pulls) to avoid duplicate work.
- For major changes, please open an issue first to discuss what you would like to change.
- Make sure your code follows the project's coding standards.

## 🛠️ Development Setup

### Prerequisites

- Visual Studio (latest recommended version)
- .NET Framework 4.7.2 or later

### Installation

1.  Clone the repository.
2.  Open the solution file (`*.sln`) in Visual Studio.
3.  Restore NuGet packages.
4.  Build the solution.

## 🔄 Pull Request Process

1. **Update your branch** with the latest upstream changes:

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Make your changes** following the coding standards.

3. **Test your changes** thoroughly.

4. **Commit your changes** with clear, descriptive messages.

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes

5. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** on GitHub:
   - Provide a clear title and description.
   - Reference any related issues.
   - Ensure CI checks pass.

7. **Respond to feedback** from maintainers and update as needed.

## 📝 Coding Standards

### General Guidelines

- Write clean, readable, and maintainable code.
- Follow the existing code style and conventions.
- Add comments for complex logic.
- Use meaningful variable and function names.

### Language-Specific Standards (.NET/Visual Basic)

- Use `Option Strict On` and `Option Explicit On`.
- Follow Microsoft's .NET coding guidelines.
- Handle exceptions appropriately.

## 🐛 Reporting Bugs

When reporting bugs, please include:

- **Clear title and description**
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Screenshots or error messages** if applicable
- **Environment details**: OS, Visual Studio version, .NET version.

Use the [bug report template](../../issues/new?template=bug_report.md) if available.

## 💡 Suggesting Features

When suggesting features, please include:

- **Clear title and description**
- **Use case**: Why is this feature needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches you've thought about

Use the [feature request template](../../issues/new?template=feature_request.md) if available.

## Issues

- Use GitHub issues to report bugs, suggest features, or ask questions.
- Before creating a new issue, please search existing issues to avoid duplicates.
- Provide as much detail as possible in your issue description.

## Pull Requests

- All code changes should be submitted via pull requests.
- Each pull request should address a single issue or feature.
- Ensure your pull request passes all CI checks.
- Be prepared to address feedback and make revisions to your pull request.

## Branching

- Use descriptive branch names, such as `feature/new-feature` or `fix/bug-description`.
- Base your branches off the `main` branch.
- Keep your branches up-to-date with `main` by rebasing frequently.

## Commit Messages

- Use clear and concise commit messages.
- Follow the Conventional Commits specification (e.g., `feat: add new feature`, `fix: resolve bug`).
- Provide context for your changes in the commit message body.

## Testing

- Write unit tests for all new code.
- Ensure existing tests pass before submitting a pull request.
- Aim for high test coverage.
- Tests are located in the `TODO: TEST_PROJECT_NAME` project.
- Use `TODO: TEST_FRAMEWORK` for testing.

## Linting

- The project uses `TODO: LINTING_TOOL` for linting.
- Run the linter before submitting a pull request.
- Fix any linting errors.
- Linting configuration is located in `TODO: LINTING_CONFIG_FILE`.

## Releases

- Releases are managed by the maintainers.
- New releases are created based on semantic versioning.
- Release notes are generated automatically from commit messages.

## 🙏 Recognition

Contributors will be recognized in:

- The project README
- Release notes for significant contributions
- The [CONTRIBUTORS](CONTRIBUTORS.md) file (if applicable)

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## 📧 Questions?

If you have questions, feel free to:

- Open an issue with the `question` label
- Contact the maintainers at [contact@email.com]

Thank you for contributing! 🎉