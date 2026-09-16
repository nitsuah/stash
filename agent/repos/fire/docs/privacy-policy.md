# FIRE Tracker — Privacy Policy & Terms of Use

**Effective Date:** August 2026  
**Application:** FIRE Tracker (`lifefire.netlify.app` / self-hosted)  
**Repository:** [github.com/nitsuah/fire](https://github.com/nitsuah/fire)

---

## 1. Overview

FIRE Tracker is a **local-first, privacy-by-design** personal finance tool. It is not a financial product, bank, or registered investment advisor. No financial data you enter is ever transmitted to any remote server operated by this application.

---

## 2. Data Storage

### 2a. Browser-Only Mode (lifefire.netlify.app)

When you use the hosted Netlify deployment:

- **All data lives exclusively in your browser's `localStorage`**, keyed to `fire_tracker_state`.
- Data never leaves your device through this application. It is not sent to Netlify servers, cloud databases, or any third party by this app.
- Clearing your browser data, switching browsers, or using a private/incognito session **will erase your data**. Use the Export JSON Backup feature regularly.
- The Netlify platform itself may log standard HTTP access metadata (IP address, timestamp, URL path) as part of normal CDN operation — this is governed by [Netlify's Privacy Policy](https://www.netlify.com/privacy/), not this document.

### 2b. Self-Hosted / Local Docker Mode

When you run the application locally via Docker:

- Data is stored in a **local `data/db.json` file** on your machine.
- The Express server (`localhost:3001`) is bound to `127.0.0.1` (loopback), so it's reachable only from your machine, not other devices on your network. `FIRE_API_KEY` is required by default (set `FIRE_AUTH_DISABLED=true` to explicitly opt out for local-only use) — see [security-hardening.md](security-hardening.md).
- The browser app syncs with this local server; `localStorage` serves as a fallback if the server is unreachable.

---

## 3. Data Never Collected or Transmitted by This App

The following data is explicitly **never collected, stored remotely, or shared** by this application:

- Account balances, net worth, or investment values
- Portfolio positions or CSV import contents
- Expense figures or income data
- Names, email addresses, or any personally identifiable information
- IP addresses or device identifiers (by this app — see Section 2a regarding Netlify)

---

## 4. External Services & Third-Party Requests

The following **external CDN requests** are made when loading the application. These load UI libraries only — no financial data is included in these requests:

| Service | Purpose | What is sent |
|---|---|---|
| `fonts.googleapis.com` | Inter & Outfit typefaces | Browser/font request only |
| `fonts.gstatic.com` | Font file delivery | Browser/font request only |
| `cdn.jsdelivr.net` | Chart.js & annotation plugin | Browser/script request only |
| `cdn.jsdelivr.net` | Marked.js (markdown renderer) | Browser/script request only |

No financial data, account information, or personal data is included in any of these requests.

---

## 5. CSV File Imports

When you import a CSV file (Fidelity, Chase, Capital One, or other):

- The file is **parsed entirely in your browser using JavaScript**. It is never uploaded to any server.
- Parsed data is written to `localStorage` (browser mode) or `data/db.json` (local server mode) only.
- Imported file names and record counts are logged locally for your reference; the raw file content is not retained after parsing.

---

## 6. MCP Server (Claude / LLM Integration)

FIRE Tracker includes an optional **MCP (Model Context Protocol) server** (`app/mcp-server.mjs`) for integration with AI assistants such as Claude Code and Claude Desktop.

**What the MCP server does:**

- Exposes **8 read-only tools** that allow an AI assistant to query your FIRE data (net worth, accounts, CDs, expenses, projections, portfolio positions, and side gig income).
- Runs as a **local stdio process** spawned by your AI assistant client. It does not bind to a network port or expose any HTTP endpoint.
- Reads from `data/db.json` only — it has no write access by design (no write tools are registered).

**What the MCP server does NOT do:**

- It does not transmit your financial data to Anthropic, Claude, or any remote server on its own. Data sent to an AI assistant through tool calls is subject to that assistant's privacy policy (e.g., [Anthropic's Privacy Policy](https://www.anthropic.com/privacy)).
- It does not run unless explicitly configured and started.
- It cannot modify your data.

**Important:** When you invoke an AI assistant with the MCP server enabled, the tool responses (your financial data) are sent to the AI provider's API. Only enable this integration if you are comfortable with this and have reviewed your AI provider's data handling policies.

---

## 7. Webhook Integration (Optional)

The optional webhook feature allows external services to push data updates into your local FIRE Tracker instance:

- Webhook endpoints are **user-configured** and run on your local server only.
- Webhook secrets (HMAC keys) are stored in `data/db.json` on your machine.
- You are responsible for the security of any external service you connect via webhook.
- No webhook data is relayed to any third party by this application.

---

## 8. Data Backup & Deletion

- **Export:** Use "Export JSON Backup" in the sidebar to download a complete copy of your data at any time.
- **Delete (browser mode):** Clear `localStorage` in your browser (DevTools → Application → Storage → Clear Site Data).
- **Delete (local server mode):** Delete `data/db.json` from your machine.
- No data is held remotely by this application, so there is no account to close or remote data to request deletion of.

---

## 9. No Financial Advice

FIRE Tracker is a **personal calculation and tracking tool**. Nothing in this application constitutes financial, investment, tax, or legal advice.

- Projections are mathematical estimates based on inputs you provide. Actual investment returns, inflation, and tax obligations will differ.
- Safe Withdrawal Rate (SWR) figures are educational references (e.g., the Bengen 4% Rule) and are not personalized recommendations.
- Consult a qualified financial advisor, CPA, or attorney for decisions affecting your actual financial situation.

---

## 10. Terms of Use

By using FIRE Tracker you agree to the following:

1. **Personal use only.** This application is intended for individual personal finance tracking. Do not use it to store financial data for other people without their explicit consent.
2. **No warranty.** This software is provided "as is," without warranty of any kind, express or implied, including but not limited to fitness for a particular purpose or accuracy of financial calculations.
3. **User responsibility.** You are solely responsible for the accuracy of the data you enter, the security of your device and browser, and any financial decisions made using this tool.
4. **Open source license.** This application is released under the [MIT License](https://github.com/nitsuah/fire/blob/main/LICENSE). You may inspect, fork, and self-host it freely.
5. **No liability.** The author(s) of FIRE Tracker shall not be liable for any financial loss, data loss, or damages of any kind arising from use of this application.

---

## 11. Changes to This Policy

This document may be updated to reflect changes in application features (e.g., new integrations). The effective date at the top of this document reflects the most recent revision. Continued use of the application after a policy update constitutes acceptance of the revised terms.

---

*FIRE Tracker is an open-source project. Questions or concerns? Open an issue at [github.com/nitsuah/fire](https://github.com/nitsuah/fire).*
