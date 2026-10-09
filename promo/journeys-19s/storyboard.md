# journeys-19s

Feature spot for the journeys QA loop. Wordmark on screen from frame 0; no shared intro; outro 2.5 s. 120 BPM, cuts on beats.

| t (s) | Scene | On screen |
|---|---|---|
| 0–3 | title | "QA before you have users." / AI once, bot every night (poster at 2.4) |
| 3–7.5 | review | fire Insights screenshot being scanned; four real review-pass issues land (#169, #167, #175, #178); "11 issues" |
| 7.5–12 | nightly | `npm run test:journeys` with fire's 7 real journey names; "7 passed · 19 visual baselines · 0 tokens"; phone journey screenshot |
| 12–16.5 | lifecycle | fail → issue opened → same fingerprint → fix PR `Refs #N` → 3 green nights → auto-closed |
| 16.5–19 | outro | `/journeys`, "AI writes it once. Code runs it every night.", the page URL |

Data: fire's fictional demo seed only (screenshots are fire's `docs/screenshots/`, copied to `pages/assets/journeys-*.png`).
