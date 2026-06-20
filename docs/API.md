# API Decision Record

## Decision: No External API

This repository contains scripts, examples, and automation tools. It does not expose any hosted API, webhook endpoint, or external service contract.

All code in this repository acts as a **client** to third-party APIs:

| Directory | APIs Called |
|-----------|------------|
| `atlassian/` | Atlassian Cloud REST APIs |
| `SAAS/pagerduty/` | PagerDuty REST API + Events API v2 |
| `SAAS/slack/` | Slack Web API |
| `SAAS/github/` | GitHub REST API v3 |
| `SAAS/datadog/` | Datadog API v1/v2 |
| `cloud/aws/` | AWS APIs via boto3 |

## If an API Is Added

If a hosted endpoint is introduced in the future, document it here with:
- Base URL and auth scheme
- Endpoint list with request/response shapes
- Rate limits and SLA expectations
- Versioning policy
