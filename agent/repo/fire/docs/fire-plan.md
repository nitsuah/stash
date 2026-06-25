Implementation Plan - Lightweight FIRE Tracker & Calculator
A lightweight, secure, and privacy-preserving FIRE (Financial Independence, Retire Early) calculator and tracker. The app operates 100% client-side, storing data in localStorage and allowing users to import positions/statements (like Fidelity CSVs) to track net worth, CDs, expenses, side-income (e.g., eBay), and run projections.

User Review Required
IMPORTANT

Data Privacy & Security: No credentials or live API integrations are used. Integration is achieved via safe, read-only local parsing of CSV exports from Fidelity, Chase, and Capital One. Storage Strategy: All user inputs and imported data will be saved to the browser's localStorage. We will provide a simple Import/Export backup utility (JSON format) so the user never loses their data.

TIP

Design Philosophy: We are going to build a premium, glassmorphism-inspired dark mode dashboard with interactive Chart.js visualizations, responsive tables, micro-animations, and dynamic feedback.

Open Questions
Chart Library: I plan to pull in Chart.js via CDN (e.g., cdnjs/jsdelivr) for drawing the interactive net worth projections and asset allocation charts. Do you approve using Chart.js via CDN?
Fidelity CSV Parsing: Should the Fidelity parser support multi-account aggregation if the CSV contains multiple accounts (like CB, FXAIX, Health Savings Account seen in Portfolio_Positions_Jun-02-2026.csv)? (I will assume yes, grouping by Account Name).
Proposed Changes
Documentation Set
[NEW] 
README.md
Contains the project overview, core pillars, visual previews, setup guidelines, and directory layouts.

[NEW] 
ROADMAP.md
Outlines the phase breakouts for 2026 (Q2 Foundation & Core Calculators, Q3 Extended Integrations & Side Hustles, Q4 Portfolio Analytics & Advanced Scenarios).

[NEW] 
TASKS.md
Tracks detailed implementation tasks, priority states, contexts, and acceptance criteria in the style of the overseer repository.

Core Web Application
[NEW] 
index.html
The main entry point. Multi-tab layout featuring:

Dashboard: Net Worth summary, asset allocation chart, and retirement status indicators.
Data Imports: Drag-and-drop file upload for Fidelity CSVs, Chase statement CSVs, Capital One CSVs, plus manual transaction entry.
CD & Fixed Income Tracker: Track interest rates, maturity dates, yields, and calculate ladder payouts.
Expenses & Taxes Manager: Input basic living costs, recurring expenses, and estimate tax drag.
Side Gig Tracker: Log manual sales, flip calculations (eBay fee & shipping calculator), and side-income suggestions.
Projections: Detailed interactive chart displaying retirement horizons based on SWR (3%, 3.5%, 4% withdrawal rates), inflation-adjusted compound growth, and custom return rates.
[NEW] 
styles.css
The design system stylesheet:

CSS custom properties (variables) for theme tokens.
Curated dark palette (e.g., Deep Space Blue #0b0f19, Emerald Green #10b981 for gains, Sunset Coral #f43f5e for expenses).
Glassmorphism effects (semi-transparent backdrops, blur filters, subtle borders).
Smooth hover animations, responsive grid layouts, and modern typography (Outfit / Inter).
[NEW] 
app.js
The logic controller:

State management linked with localStorage sync.
CSV parsers for:
Fidelity Positions (parsing Symbol, Quantity, Last Price, Current Value, and Account Name).
Chase/Capital One transaction statements (parsing credits/debits).
Projection engine using standard compound growth and SWR rules.
Sidebar or tab-switching controller.
CSV import handlers, manual CD/expense/side-income handlers, and backup import/export.
Verification Plan
Automated Tests
We will construct browser verification steps to validate file loading, chart drawing, and CSV parser correctness.
We can run a lightweight HTTP dev server (e.g., python -m http.server or npx live-server) to run the page locally and interact with it.
Manual Verification
Upload the existing Portfolio_Positions_Jun-02-2026.csv file using the UI's drag-and-drop zone.
Verify that the Net Worth summary updates to show the aggregate value of all accounts (~$450,000+ based on the CSV data).
Check that the asset allocation chart accurately parses different symbols (COIN, SPAXX, etc.).
Input a sample manual CD (e.g., $10,000 at 5% for 1 year) and verify that yield payouts are correctly calculated and included in the asset list.
Run projections with 3.5% and 4% withdrawal rates and confirm that the FIRE target and target retirement age shift dynamically.