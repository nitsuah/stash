# Features

`nitsuah/fire` is a lightweight FIRE (Financial Independence, Retire Early) Tracker and API Server, built with JavaScript, designed for efficient financial management and programmatic access.

## Core Functionality

- **Net Worth Tracking** — Monitor assets and liabilities to calculate overall net worth in real time.
- **Asset & Liability Management** — Record and manage custom accounts, CDs, real estate, and vehicles.
- **Fidelity CSV Import** — Parses Fidelity brokerage position exports; aggregates symbols, quantities, and cash; dedupes settled cash from P&L.
- **Chase / Capital One CSV Import** — Parses credit card statement debits and auto-categorizes spending into monthly cash flow.
- **Local Storage Sync** — All data persists in browser localStorage with Import/Export JSON backup utility.
- **Docker Environment** — Node/Alpine container on port 8080 with volume-mounted data/ for consistent local dev.

## Investments Dashboard

- **P&L Table** — Red-green color scale, sortable faceted columns with inline totals, pie-chart filter that greys non-selected slices.
- **Risk Concentration Badges** — ⚡ for positions ≥15% of portfolio, ⚠ for ≥20%; market return comparison badges per position.
- **Diversification Suggestion Block** — Allocation-aware tips surfaced inline with the investments view.
- **Collapse-All Toggle** — Collapses investment rows; cost basis included in facet totals.

## Retirement Projections

- **Net Worth Projections Engine** — SWR curves (3%, 3.5%, 4%) with retirement age predictions and milestone forecasts.
- **Time-Period Filters** — 1M / 1Y / 5Y / 10Y / 15Y+ buttons on both retirement growth charts.
- **Chart Line Toggles** — Toggle NW, 75%/100%/125% FIRE goals, Coast FIRE, and US Median benchmark independently.
- **Bull/Bear Scenario Bands** — Clickable +2%/−2% offset buttons update the growth path in real time.
- **CD Maturity Markers** — Overlaid on the dashboard retirement growth chart to show liquidity events.
- **Multi-Scenario FIRE Comparison** — Side-by-side comparison of FIRE dates across varying salary bumps, market downturns, and inflation spikes.

## Asset Trackers

- **Real Estate Tracker** — Manual entry with property name, value, equity, and mortgage details.
- **Vehicle Tracker** — Make/model/year, current value, loan balance, and depreciation estimate; fleet summary view.
- **CD Tracker** — Annual yield badge on the CDs Maturing Soon dashboard card.
- **CD Ladder Visualizer** — Timeline view of upcoming CD maturities with aggregate yield overlays.
- **Side Hustle Tracker** — Manual income logs for Etsy, FB Marketplace, Craigslist, and eBay; includes a built-in fee and shipping margin calculator to track net sales income per platform.

## Dashboard & UX

- **Glassmorphic Dark Theme** — High-end HTML5 layout with CSS glassmorphism.
- **Header Summary Bar** — Mini allocation bars, Annual Income metric, and FIRE Progress bar with percentage displayed inside.
- **Financial Overview Tab** — Unified Accounts + CDs & Fixed Income tab with Monthly Cash Flow section (income vs. expenses, savings rate, annual surplus/deficit).
- **Dashboard Layout** — Growth + investments left column; allocation + stats + CDs right column.
- **Metric Tooltips** — Inline explanation indicators for financial terms (SWR, FIRE number, Coast FIRE, etc.) surfaced directly on each metric.
- **Mobile-Responsive Layout** — Adaptive layout for tablet and phone viewports without loss of core dashboard functionality.

## Planned

- **Tax Drag Estimation Engine** — Custom federal/state bracket support with capital gains configuration.
- **PWA Packaging** — Offline access and lightweight installable app.
- **Webhook / Local Sync Templates** — Self-hosted data sync templates for automated balance imports without manual CSV uploads.
