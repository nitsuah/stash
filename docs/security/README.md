# Security review

Tracking: nitsuah/stash#302. Never put secrets or tokens in issues, PRs, or these files.

## Tiers

- **P0**: auth bypass, exposed secret, or unauthenticated write; fix first.
- **P1**: over-broad OAuth scopes, a shared admin key, or a missing rate limit.
- **P2**: hygiene and docs.

## Safe validation

- Test accounts only; read-only probes; no production writes.
- No secrets in issues or PRs.
- Report a P0 privately to the owner before filing anything public.

## Scope

CodeRabbit is out of scope.

## Index

- [OAUTH-INVENTORY.md](OAUTH-INVENTORY.md)
- [ENDPOINT-ACL.md](ENDPOINT-ACL.md)
- nitsuah/gcp#78
- nitsuah/ats-fill#176
- nitsuah/skyview#213
- nitsuah/fire#279
- nitsuah/vhs#102
- nitsuah/vigil#345
- nitsuah/stash#303
