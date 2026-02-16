# Tasks

## Todo

### High Priority - Repository Organization & Documentation

#### A. Top-level README
- [ ] Add one-paragraph description of repository purpose
- [ ] Include license note
- [ ] Create directory listing with one-line descriptions:
  - `atlassian/` - Atlassian automation scripts
  - `git/` - Git utilities and helpers
  - `ias/` - Infrastructure automation scripts
  - `projects/` - Project-specific tooling
  - `saas/` - SaaS integration tools
  - `windows/` - Windows PowerShell/VBA utilities

#### B. Per-subproject READMEs
- [ ] `atlassian/README.md` with WHAT, WHY, HOW, SAFETY, EXAMPLE_OUTPUT
- [ ] `git/README.md` with WHAT, WHY, HOW, SAFETY, EXAMPLE_OUTPUT
- [ ] `ias/README.md` with WHAT, WHY, HOW, SAFETY, EXAMPLE_OUTPUT
- [ ] `projects/README.md` with WHAT, WHY, HOW, SAFETY, EXAMPLE_OUTPUT
- [ ] `saas/README.md` with WHAT, WHY, HOW, SAFETY, EXAMPLE_OUTPUT
- [ ] `windows/README.md` with WHAT, WHY, HOW, SAFETY, EXAMPLE_OUTPUT

#### C. Security & Sanitization
- [ ] Search for sensitive data patterns:
  - `token`, `password`, `secret`, `.pem`, `.p12`, `credentials`
- [ ] Replace any real credentials with placeholders
- [ ] Add commit message with `REDACTED` tag
- [ ] Update `.gitignore` for local artifacts:
  - `*.pem`, `*.p12`, `*.key`, `*credentials*.json`
  - Local config files
  - Test outputs
- [ ] Audit all scripts for hardcoded hostnames/IPs
- [ ] Replace internal hostnames with `example.com` placeholders

#### D. Usability Improvements (Pick 2)
- [ ] Convert most-used PowerShell script to use `Param()` blocks
- [ ] Add comprehensive help comments to PowerShell scripts
- [ ] Create sample CSV for VBA/Access tools
- [ ] Add example output files for each major script
- [ ] Document required permissions for each script

#### E. Contributing & Issue Templates
- [ ] Update `CONTRIBUTING.md` with:
  - How to propose changes
  - Security reminder: "Don't commit secrets"
  - Testing guidelines for scripts
  - Documentation requirements
- [ ] Add issue template for script requests
- [ ] Add PR template with security checklist

### Medium Priority - Code Quality

- [ ] Implement settings persistence to XML using .NET serialization (P1, M)
- [ ] Add robust error handling for all file I/O operations (P1, S)
- [ ] Implement a simple TreeView-based UI for snippet management (P2, L)
- [ ] Add unit tests for the Snippet and Folder classes (P2, M)
- [ ] Implement basic substring search in snippet titles and content (P2, M)
- [ ] Refactor the main form's event handlers to separate methods (P3, L)
- [ ] Add support for exporting snippets as individual text files (P3, S)
- [ ] Create a basic MSI installer using Visual Studio Installer Projects (P3, S)

### Files to Create
- [ ] Top-level `README.md` (enhanced)
- [ ] Subproject `README.md` files (6 total)
- [ ] `SECURITY.md` with sensitive data removal procedures
- [ ] `.gitignore` updates for credentials

### Commands to Run
- [ ] `git ls-files | Select-Object -First 50 | ForEach-Object { Get-Content $_ -TotalCount 2 }`
- [ ] `rg "token|password|secret|KEY|CRED" -n` (search for secrets)
- [ ] Test sample scripts to verify they work with placeholders

## In Progress

- [ ] Implementing syntax highlighting in the snippet editor using ScintillaNET (P1, L)
- [ ] Adding support for multiple snippet folders, allowing nested organization (P2, M)

## Done

- [x] Set up CI/CD pipeline
- [x] Created initial project structure

## References
- See `AGENT_INSTRUCTIONS.md` for detailed implementation guide
- See `CONTRIBUTING.md` → PR Security Checklist for submission requirements
- See `SECURITY.md` → IT Scripts & Automation Security for specific warnings