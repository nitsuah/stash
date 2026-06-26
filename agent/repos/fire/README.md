# 🔥 FIRE Calculator & Tracker

[![CI](https://github.com/nitsuah/fire/actions/workflows/ci.yml/badge.svg)](https://github.com/nitsuah/fire/actions/workflows/ci.yml)
![Dashboard Preview](docs/assets/dashboard_preview.png)
repo: [[darkmoon]]
*(Placeholder for visual reference)*

> A lightweight, secure, and privacy-preserving Financial Independence, Retire Early (FIRE) calculator and tracker. Built as a 100% client-side static web application with a premium dark-mode user interface, it runs locally via Docker and stores all data inside your browser's `localStorage`—ensuring complete data privacy with zero external server dependencies.

---

## 🚀 Core Features

### 1. Unified Net Worth Analytics & Projections

- Real-time tracking of current assets and liabilities.
- Rich interactive projection graphs using **Chart.js** detailing retirement horizons.
- Toggleable withdrawal rates (3.0%, 3.5%, 4.0% SWR) and inflation-adjusted compound growth projections.

### 2. Safe, Read-Only CSV Imports

- Import investment portfolios directly from Fidelity exports (automatically maps Account Name, Symbol, Description, Quantity, Cost Basis, and Current Value).
- Import credit card/banking statements from Chase and Capital One to track recent spending and balances.
- All file processing happens locally in JavaScript; no financial data is ever transmitted over the network.

### 3. CD & Fixed Income Tracker

- Track Certificate of Deposits (CDs) with individual principal, yield, and maturity dates.
- Interactive CD Ladder visualizer showing interest payouts over time and upcoming maturities.

### 4. Side Gig & eBay Hub

- Track side income streams dynamically (e.g. eBay, side gigs, freelancing).
- Built-in **eBay Profit Calculator** (input sale price, item cost, shipping, and automatically compute eBay fees, margins, and ROI).
- Log custom accounts and side income check-ins.

### 5. Local Data Management

- Persistent storage across sessions via `localStorage`.
- Simple Backup utility allowing one-click export (JSON download) and restore (JSON upload) of your entire configuration.

---

## 🛠️ Tech Stack & Setup

- **Front-end**: HTML5, Vanilla JavaScript, CSS3 (Vanilla custom styling with HSL color tokens & Glassmorphic components)
- **Charts**: [Chart.js](https://www.chartjs.org/) via CDN
- **Environment**: Docker (Nginx Alpine)

### Running with Docker

Run the container using a simple volume mount so modifications to your files are reflected instantly in the browser:

```bash
# Build the docker image
docker build -t fire-calculator .

# Run the container (binds to port 8080)
docker run -d -p 8080:80 -v ${PWD}:/usr/share/nginx/html --name fire-app fire-calculator
```

Once running, visit **`http://localhost:8080`** in your browser.

To stop the container:

```bash
docker stop fire-app
docker rm fire-app
```

---

## 📁 Directory Structure

```bash
fire/
├── index.html                           # Core layout & HTML structure
├── styles.css                           # Premium glassmorphism design tokens & styles
├── app.js                               # CSV parsing, state sync, and calculator engines
├── Dockerfile                           # Alpine Nginx container setup
├── README.md                            # Project overview (this file)
├── ROADMAP.md                           # Q2-Q4 feature milestones
├── TASKS.md                             # Detailed project task checklist
└── Portfolio_Positions_Jun-02-2026.csv  # Sample Fidelity investment data
```

---

## 🗺️ Roadmap & Tasks
## Repository Index

### Root Files
- [[repos/fire/CHANGELOG.md|CHANGELOG.md]]
- [[repos/fire/FEATURES.md|FEATURES.md]]
- [[repos/fire/METRICS.md|METRICS.md]]
- [[repos/fire/ROADMAP.md|ROADMAP.md]]
- [[repos/fire/TASKS.md|TASKS.md]]

### Documentation
- [[repos/fire/docs/fire-feedback.md|fire-feedback.md]]
- [[repos/fire/docs/fire-plan.md|fire-plan.md]]

- View milestones in [ROADMAP.md](ROADMAP.md)
- View active implementation checklist in [TASKS.md](TASKS.md)
