# MM operating loop (state lives in Neon; this file is the rulebook)
Weekly (agent): run audit-scanner on new `leads`, run monitor/monitor.mjs on `monitor_targets`, log to `scans`/`monitor_checks`, update `projects.next_action`, review `experiments` whose review_date passed and write `result`/`learning`, kill per kill_rule.
Human gates: publish clicks, outreach approval/sending, payouts, accounts, tax, pricing.
Cost rule: zero-LLM scripts for repeatable work; LLM only for copy/summaries; log estimated cost in `money_events`.
Offload demos and one-off sites to Base44 + Netlify free tiers.
Assets built: audit-scanner, template-pack, icon-pack, monitor. Trials: org / saas / local lead groups compared in `experiments`.
