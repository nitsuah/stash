# API / MCP endpoint authorization matrix

No keys, tokens, or secrets in this file. Tracking: nitsuah/stash#302.

| Repo | Surface | AuthN | AuthZ / principal | Rate limit | Deny behaviour | Tracking | Status |
|---|---|---|---|---|---|---|---|
| ats-fill | TBD | TBD | TBD | TBD | TBD | nitsuah/ats-fill#176 | unverified |
| gcp | TBD | TBD | TBD | TBD | TBD | nitsuah/gcp#78 | unverified |
| vigil | MCP server | shared admin key | TBD | 60 req/min (docs/MCP.md) | TBD | nitsuah/vigil#345 | unverified |
| vhs | TBD | TBD | TBD | TBD | TBD | nitsuah/vhs#102 | unverified |
| fire | TBD | TBD | TBD | TBD | TBD | nitsuah/fire#279 | unverified |
| skyview | TBD | TBD | TBD | TBD | TBD | nitsuah/skyview#213 | unverified |
| bb-mcp | TBD | OIDC | TBD | TBD | TBD | TBD | unverified |
| stash | sso/ SAML example | TBD | TBD | TBD | TBD | nitsuah/stash#303 | unverified |
