# Release process

> 🧭 [auto-apply-plugin](../../README.md) · [Features](../FEATURES.md) · [Roadmap](../ROADMAP.md) · [Tasks](../TASKS.md) · [Changelog](../CHANGELOG.md) · [Metrics](../METRICS.md) <!-- nav -->

## Normal development

Pull requests and pushes continue to use the existing CI workflow for lint, unit tests, coverage, E2E, and the security audit.

Chrome Web Store publishing is deliberately not tied to merges into `main`.

## Production release

Use an explicit semantic-version tag:

```text
vMAJOR.MINOR.PATCH
```

The tag must exactly match `manifest.json` without the leading `v`.

Example:

```text
manifest.json -> 1.1.0
git tag v1.1.0
git push origin v1.1.0
```

The tag triggers `.github/workflows/chrome-release.yml`.

## Human control

The `production` GitHub environment is the final release gate. Configure required reviewers so a maintainer explicitly approves the Store submission.

This keeps routine CI automatic while preventing an accidental merge or arbitrary branch push from publishing an extension.

## Artifacts

Every release produces:

- a versioned extension ZIP
- a SHA-256 checksum file
- generated GitHub Release notes

The exact tag is used as the source for both packaging and publishing.
