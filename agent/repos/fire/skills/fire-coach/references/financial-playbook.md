---
up: "[[repos/fire]]"
title: "fire · financial-playbook"
source: https://github.com/nitsuah/fire/blob/main/skills/fire-coach/references/financial-playbook.md
kind: repo-doc
repo: fire
---

# FIRE financial playbook

General, widely accepted principles for reaching financial independence.
Dollar limits (IRA/401(k)/HSA caps, tax brackets, ACA thresholds) change
every year: look up the current figures instead of quoting from memory.

## 1. The core math

- **FIRE number** = annual spending ÷ safe withdrawal rate (SWR). At 4%
  that's **25× annual spending**; at 3.5%, about 28.6×; at 3.25%, about 30.8×.
  fire computes it as annual expenses (including insurance and tax drag) ÷ SWR.
- **The 4% rule** (Bengen, 1994; the Trinity study) held up over historical
  **30-year** retirements. Early retirees facing 40–50+ years usually plan on
  **3.25–3.5%**, or a flexible withdrawal rule (spend less after bad years).
- **Savings rate drives the timeline more than returns.** Starting from
  zero, with a 5% real return and a 4% SWR:

  | Savings rate | Years to FI |
  | --- | --- |
  | 10% | ~52 |
  | 20% | ~37 |
  | 30% | ~28 |
  | 40% | ~22 |
  | 50% | ~17 |
  | 60% | ~13 |
  | 70% | ~9 |

  Spending cuts count twice: you save more *and* need a smaller FIRE number.
- **Flavors** (as the app draws them): **Lean FIRE** = 75% of the target,
  **Fat FIRE** = 125%, **Coast FIRE** = enough today that growth alone reaches
  the FIRE number by the retirement age (FIRE number ÷ (1 + real return)^years),
  **Barista FIRE** = part-time income covers the gap while the portfolio grows.
- **Think in real (inflation-adjusted) returns.** A 7–8% nominal stock return
  is roughly 4.5–5.5% real. fire's projection chart is already in real terms.

## 2. Order of operations (where the next dollar goes)

1. **Starter emergency fund**: about one month of expenses in cash.
2. **Employer 401(k)/403(b) match**: an instant 50–100% return.
3. **High-interest debt** (credit cards, anything above ~8%): pay it off.
4. **Full emergency fund**: 3–6 months of expenses; 6–12 if income is
   variable, single-earner or self-employed. Keep it in a HYSA, money market,
   T-bills or a short CD ladder.
5. **HSA** if on an HSA-eligible high-deductible plan. It's triple
   tax-advantaged; invest it and keep receipts for later reimbursement.
6. **IRA** (Roth or traditional; see §4).
7. **Max the workplace plan**.
8. **Taxable brokerage**, plus extra payments on moderate-rate debt if that
   lets them sleep better.

## 3. Investing

- **Own the market cheaply.** Broad, low-cost index funds (total US,
  total international, total bond), with expense ratios ideally under 0.10–0.20%.
  Fees compound against you.
- **Allocation matches the time horizon and nerves.** More equities while
  accumulating. Add bonds/cash as retirement nears. An allocation you can
  hold through a 40% drawdown beats a "better" one you abandon.
- **Limit concentration.** Keep any single stock (including employer stock)
  to roughly ≤10% of the portfolio; fire flags concentration and scores
  diversification.
- **Rebalance** once a year or when a class drifts more than ~5 percentage
  points (or 25% relative) from target. Rebalance inside tax-advantaged accounts
  first, or by directing new contributions, to avoid realizing gains.
- **Don't time the market.** Automate contributions on payday and keep
  investing through downturns.
- **Asset location:** tax-inefficient assets (bonds, REITs) in tax-advantaged
  accounts; broad equity index funds are fine in taxable.

## 4. Taxes

- **Roth vs. traditional:** pay tax at whichever rate is lower, now or in
  retirement. High earners pursuing FIRE often favor traditional
  contributions now and convert to Roth in low-income early-retirement years.
- **Tax-loss harvesting:** realized losses offset realized gains, then up to
  $3,000/yr of ordinary income ($1,500 if married filing separately); the rest carries forward. **Wash-sale rule:**
  buying a substantially identical security within 30 days before or after the
  sale (in *any* account, including IRAs) disallows the loss. fire's Insights tab
  lists harvesting candidates.
- **Low-income years are an opportunity:** gap years, sabbaticals and early
  retirement are good times for Roth conversions and for realizing long-term
  gains in the 0% bracket.
- **Getting money out before 59½:** Roth IRA *contributions* (not earnings)
  can be withdrawn anytime. A **Roth conversion ladder** makes each conversion
  penalty-free after 5 years. The **Rule of 55** applies to a 401(k) from an
  employer you leave in or after the year you turn 55. **72(t)/SEPP** allows
  substantially equal periodic payments. HSA receipts can be reimbursed any time.
- **Side-hustle income:** self-employment tax is ~15.3% on 92.35% of net
  earnings, on top of income tax. A return is generally required once net
  self-employment earnings reach $400. Pay **quarterly estimates**; the
  safe-harbor rule is 100% of last year's tax, or 110% above the high-income
  threshold, or 90% of the current year's tax in four equal payments. The 90%
  current-year alternative avoids overpayment when income drops but requires a
  reasonable projection. Deduct real costs: cost of goods, platform fees, shipping,
  supplies and business mileage. fire tags ledger rows for this.

## 5. Protecting the plan

- **Sequence-of-returns risk:** a crash early in retirement does far more
  damage than the same crash later. Mitigations: a 1–2 year cash/CD buffer,
  a "bond tent" (more bonds just before and after the retirement date), and
  flexible spending in down years. fire models **cash-first withdrawals** after
  the retirement age.
- **Life happens.** Surgery, a pet emergency, a roof, a job loss and a new
  baby all hit eventually. The emergency fund and insurance exist for these.
  fire's **🌪️ Chaos mode** shows how a realistic mix of them bends the
  projection.
- **Insurance:** health (pre-Medicare: ACA marketplace subsidies depend on
  MAGI, so plan withdrawals and conversions around them; COBRA is a bridge);
  term life if anyone depends on your income; long-term disability while
  working; umbrella liability once net worth grows; deductibles sized to the
  emergency fund.
- **Estate basics:** beneficiary designations on every account (they override
  a will), a will, durable power of attorney, healthcare directive.

## 6. Cash & CDs

- Emergency fund and near-term money (< ~3 years) belong in cash
  equivalents, not stocks.
- **CD ladders** stagger maturities (e.g. 3/6/12/18/24 months) so something
  always matures soon. Before renewing, compare the rate with current HYSA,
  money-market and T-bill yields, and note the early-withdrawal penalty.
  fire's CD Ladder card and `get_cds` show maturities.

## 7. When income stops (job loss, gap year, health)

1. Compute **runway** = liquid assets ÷ monthly spending (`get_emergency_runway`).
2. Cut discretionary spending immediately; renegotiate or pause
   subscriptions; review insurance (ACA special enrollment vs. COBRA).
3. File for unemployment benefits if eligible.
4. Avoid early 401(k)/IRA withdrawals (taxes + 10% penalty) while cash and
   taxable accounts last; don't sell investments in a panic.
5. Use the low-income year: Roth conversions and 0%-bracket gain harvesting
   may be cheap now.
6. Setting savings to $0 (Projections → Growth Settings) only models
   *stopped contributions*. Before the retirement age the projection does
   not subtract living expenses, so it understates a job loss. Use
   `get_emergency_runway` (months until $0 when spending comes out of the
   portfolio) for the real depletion picture, or 🌪️ Chaos's job-loss events,
   which do charge lost savings plus spending. Set a date to revisit.

## 8. Habits that compound

- Pay yourself first and automate it.
- Optimize the big three: **housing, transportation, food**, which usually
  make up 60%+ of spending. Small subscriptions matter less than a cheaper car.
- Avoid lifestyle creep: bank at least half of every raise.
- Track net worth monthly, not daily; review the plan yearly.
- Side income accelerates FI: while working, every extra dollar is saved; and
  income you'd keep earning in retirement (Barista FIRE) shrinks the FIRE
  number by $25,000 per $1,000/yr it covers, at a 4% SWR.
