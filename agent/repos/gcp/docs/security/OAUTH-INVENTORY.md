---
up: "[[repos/gcp]]"
title: "gcp · OAUTH-INVENTORY"
source: https://github.com/nitsuah/gcp/blob/main/docs/security/OAUTH-INVENTORY.md
kind: repo-doc
repo: gcp
---

# OAuth Client Inventory

## Google OAuth Clients

| Repo      | Provider       | Client Purpose               | Scopes               | Redirect URIs       | Consent/Verification | Rotation Owner | Status      |
|-----------|----------------|-----------------------------|---------------------|---------------------|----------------------|----------------|-------------|
| gcp       | Google OAuth   | Google OAuth integration     | gmail.modify        | https://gcp.example.com/auth/callback | Google OAuth consent screen | TBD            | unverified |
| ats-fill  | Chrome Web Store | Chrome Web Store publish     | webstore.publish     | https://ats-fill.example.com/auth/callback | Chrome Web Store verification | TBD            | unverified |
| bb-mcp    | OIDC Provider | OIDC provider integration    | openid, profile, email | https://bb-mcp.example.com/auth/callback | OIDC provider consent screen | TBD            | unverified |

## Other Repos

| Repo      | Provider       | Client Purpose               | Scopes               | Redirect URIs       | Consent/Verification | Rotation Owner | Status      |
|-----------|----------------|-----------------------------|---------------------|---------------------|----------------------|----------------|-------------|
| vigil    | TBD            | TBD                         | TBD                 | TBD                 | TBD                  | TBD            | unverified |
| vhs       | TBD            | TBD                         | TBD                 | TBD                 | TBD                  | TBD            | unverified |
| fire      | TBD            | TBD                         | TBD                 | TBD                 | TBD                  | TBD            | unverified |
| skyview   | TBD            | TBD                         | TBD                 | TBD                 | TBD                  | TBD            | unverified |
| stash     | TBD            | TBD                         | TBD                 | TBD                 | TBD                  | TBD            | unverified |
