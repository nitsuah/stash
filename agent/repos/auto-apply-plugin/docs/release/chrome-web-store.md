# Chrome Web Store release setup

> 🧭 [auto-apply-plugin](../../README.md) · [Features](../FEATURES.md) · [Roadmap](../ROADMAP.md) · [Tasks](../TASKS.md) · [Changelog](../CHANGELOG.md) · [Metrics](../METRICS.md) <!-- nav -->

ats-fill uses the Chrome Web Store API v2 with the documented OAuth 2.0 credential flow for subsequent releases. The first Store listing remains a manual setup step; after that, a protected GitHub Actions environment can publish tagged releases.

## One-time Google setup

1. Create/select a Google Cloud project.
2. Enable the **Chrome Web Store API**.
3. Configure the OAuth consent screen.
4. Create an OAuth client ID using **Web application** as the application type.
5. Add `https://developers.google.com/oauthplayground` as an authorized redirect URI.
6. Use OAuth 2.0 Playground with the Chrome Web Store scope `https://www.googleapis.com/auth/chromewebstore` to authorize the Google account that owns the Chrome Web Store item and obtain a refresh token.
7. Copy the publisher ID from the Chrome Web Store Developer Dashboard.
8. Record the extension ID after the first Store item exists.

Google requires 2-step verification for developers publishing/updating extensions.

## One-time Chrome Web Store setup

Before the first automated publish:

1. Register the extension manually in the Chrome Web Store Developer Dashboard.
2. Complete the Store listing and Privacy tabs.
3. Upload the first package manually.
4. Complete any required developer verification/payment steps.
5. Publish the initial item manually and confirm its extension ID.
6. Confirm the listing's visibility settings are compatible with API publishing.

The first listing cannot be created by this repository workflow; the workflow assumes an existing Store item.

## GitHub setup

Create a GitHub Actions environment named `production`. Configure required reviewers if you want a human approval before a Store submission.

Add these secrets to the `production` environment:

| Secret | Value |
| --- | --- |
| `CWS_CLIENT_ID` | Google OAuth client ID |
| `CWS_CLIENT_SECRET` | Google OAuth client secret |
| `CWS_REFRESH_TOKEN` | OAuth refresh token for the authorized Chrome Web Store account |
| `CWS_PUBLISHER_ID` | Chrome Web Store publisher ID |
| `CWS_EXTENSION_ID` | Published extension ID |

Do not put OAuth credentials, refresh tokens, or any other secret in the repository, workflow YAML, release notes, or GitHub Actions logs.

## Release flow

1. Update `manifest.json` to the next semantic version.
2. Merge the change to `main`.
3. From GitHub Actions, run **Create Chrome Web Store Release Tag**. It reads `manifest.json`, validates the version, and creates/pushes the matching `vX.Y.Z` tag. The tag then triggers the release workflow.
4. The workflow checks that the tag and manifest version match.
5. It builds the extension and produces a ZIP containing the contents of `dist/`.
6. It verifies the ZIP and records a SHA-256 checksum.
7. A GitHub Release is created with the ZIP and checksum.
8. The `production` environment approval gate runs.
9. The workflow refreshes an OAuth access token and uploads the ZIP using Chrome Web Store API v2.
10. If the upload is asynchronous, the workflow polls `fetchStatus` for up to two minutes.
11. The workflow calls `publish`, submitting the release for Chrome Web Store review.

A Store submission may remain under review after the workflow succeeds. A successful API publish call means the package was submitted; it does not guarantee immediate public availability.

## Rollback

Do not reuse a published version number. Fix the issue, increment the manifest version, create a new tag, and release the new version.

## Local validation

```bash
node scripts/validate-manifest.mjs
node scripts/validate-release-version.mjs v1.0.0
node scripts/package-extension.mjs
```
