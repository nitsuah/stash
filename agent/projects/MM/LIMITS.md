# Limits and when to retry

Source of truth is the Neon `limits` table (project `moneymakers`). This is a readable copy (2026-10-23).

| System | Limit seen | Retry when | Queued |
|---|---|---|---|
| Apify Store publishing | `daily-publication-limit` after 5 Actors published in a day | Next UTC day; publish up to 5 | sitemap-url-checker (`IvLomTuUb0jvJyETF`), then tech-stack detector |
| Gumroad | 10 new products per day | Next day; create up to 10 | 26 built packs; each needs a cover and thumbnail first |
| Imps dispatcher | 5 per cycle, 2 per repo, 8 open imp PRs, 15 runs per 24h, 24h cooldown after 2 gate fails; turn caps imp 40 / fix 25 / review 25 | Hourly at :07, or run `dispatch.mjs --max N` by hand under the cap | stash issues 287-290 |
| 9router | Host port 20128 hangs if a stale `wslrelay` holds it; dispatcher logs "did not answer a MAX probe" | Whenever that skip appears | none |
| stash pushes | Imps runner sets `origin` push URL to `no_push` | Always | none |
| Etsy | Shop needs the user's card, bank and ID | When the user finishes setup | 9 drafted listings plus factory packs |

Retry guidance is summarized in the `Retry when` column above. Apify publication steps are in `apify-publish.md`; the remaining scripts' invocation commands are documented in their project READMEs or source usage text.
