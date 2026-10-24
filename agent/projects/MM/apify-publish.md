# Publishing an Apify Actor with the CLI (no browser)

The CLI is logged in on the host (`npx -y apify-cli@latest info` shows `nitsuahlabs`). Use host Node, not Docker, for these commands. Run them from a stash worktree, not the shared checkout.

1. Build and upload: `cd projects/products/<actor> && npx -y apify-cli@latest push` (needs `.actor/output_schema.json`, and the default input must give a non-empty dataset or Apify's daily self-test marks the Actor "under maintenance").
2. Pricing, categories (one call; example for a pay-per-event Actor):
   `npx -y apify-cli@latest api PUT v2/actors/<id> -d '{"categories":["DEVELOPER_TOOLS"],"pricingInfos":[{"pricingModel":"PAY_PER_EVENT","minimalMaxTotalChargeUsd":null,"pricingPerEvent":{"actorChargeEvents":{"apify-actor-start":{"eventTitle":"Actor Start","eventDescription":"Charged when the Actor starts running. Number of events charged depends on Actor memory (one event per GB, minimum one event).","isOneTimeEvent":true,"eventPriceUsd":0.00005},"<event>":{"eventTitle":"...","eventDescription":"...","isOneTimeEvent":false,"eventPriceUsd":0.01,"isPrimaryEvent":true}}}}]}'`
   Valid categories seen: DEVELOPER_TOOLS, SEO_TOOLS, SOCIAL_MEDIA, VIDEOS (more exist).
3. Test on the platform: `npx -y apify-cli@latest api POST "v2/actors/<id>/runs?waitForFinish=90" -d '{"startUrls":[{"url":"https://example.com/"}]}'`.
4. Publish: `npx -y apify-cli@latest api PUT v2/actors/<id> -d '{"isPublic":true}'`.
5. Icon: not covered by the API calls; upload it in the console Publication tab (cover-factory/icons.mjs makes the PNGs), accept the crop, then CLICK SAVE on the "You have unsaved changes" banner. The upload alone does not persist. Verify with `api GET v2/actors/<id>` and check `pictureUrl` is present.

Reading a published Actor (`api GET v2/actors/<id>`) shows the exact pricing structure to copy.
