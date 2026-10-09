---
up: "[[repos/fire]]"
title: "fire · platform-fees"
source: https://github.com/nitsuah/fire/blob/main/skills/reseller-autopilot/references/platform-fees.md
kind: repo-doc
repo: fire
---

# Platform fees and fit (US, checked October 2026)

Fees change, so treat these as estimates and confirm on each platform's fee page
before quoting exact nets. The fire app's **Platform Fee Calculator** has a tab
for each platform below and uses these rules (Mercari's processing fee is an
opt-in checkbox there, at 2.9% + $0.50).

| Platform | Seller fees | Best for | Watch out for |
| --- | --- | --- | --- |
| **eBay** | Final value fee about 13–15% of item + shipping in most categories, plus a $0.30–$0.40 per-order fee. Promoted Listings adds whatever ad rate you set (2–5% is typical). | Electronics, collectibles, parts, media, brand-name anything, and buyers who search by model number | Category rates vary (some are lower, for example sneakers over $150). Returns policies. Managed-payments holds for new sellers. |
| **Etsy** | $0.20 listing (renews every 4 months or after a sale) + 6.5% transaction fee on item + shipping + 3% + $0.25 processing. Offsite Ads take 12–15% of attributed sales, capped at $100. | Handmade, **vintage (20+ years old)**, craft supplies, **digital downloads** | Only those categories are allowed. Offsite Ads can be mandatory once you pass $10k a year. |
| **Mercari** | 10% of item + buyer-paid shipping. Sources disagree on whether a separate ~2.9% + $0.30–0.50 processing fee still applies, so check the seller dashboard. Standard direct-deposit payout is free. | Fast, casual sales: toys, games, home goods, small electronics | The fee also applies to shipping. Build cheap labels into the price instead of charging high shipping. |
| **Poshmark** | $2.95 under $15, and 20% at $15 and up. Poshmark's prepaid label is paid by the buyer. | Clothing, shoes, bags, beauty | 20% hurts on cheap items. Bundle under $15. |
| **FB Marketplace** | Local pickup is free. Shipped orders through checkout pay about 5% (min $0.40). | Furniture, bulky and local items, anything that's a pain to ship | No-shows and scams. Cash or in-app payment only; never accept "overpay and refund" or a code sent to your phone. |

## Net formula

```
net = list price + buyer shipping − platform fees − label cost − item cost
fees (eBay)    ≈ (price + shipping) × (category rate + ad rate) + $0.30–$0.40
fees (Etsy)    = $0.20 + (price + shipping) × 9.5% + $0.25 (+ offsite ads if attributed)
fees (Mercari) ≈ (price + shipping) × 10% (+ 2.9% + $0.50 processing if your dashboard shows it)
fees (Poshmark) = price < $15 ? $2.95 : price × 20%
fees (FB)      = local ? 0 : max(price × 5%, $0.40)
```

## Picking a platform

1. Bulky or heavy item → **FB Marketplace** (local).
2. Clothing → **Poshmark** if $15 or more, otherwise **Mercari** or a bundle.
3. Handmade, vintage or digital → **Etsy**.
4. Searched by exact model, collectible or high value → **eBay** (deepest sold comps).
5. Anything else under ~$40 → **Mercari** first, then cross-list to eBay after 14 days.

## Shipping rules of thumb

- Under 1 lb: USPS Ground Advantage is usually cheapest. Weigh it, don't guess.
- Use the platform's discounted labels; they beat retail-counter prices.
- Free shipping converts better. Fold the label into the price, but remember
  Etsy and Mercari charge their percentage on the total either way.
