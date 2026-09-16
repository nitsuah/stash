# Analytics Setup Guide

This document outlines options for adding privacy-friendly analytics to track visitor interest and site performance.

## Recommended: Plausible Analytics

**Why Plausible?**
- ✅ Privacy-friendly (no cookies, GDPR compliant)
- ✅ Lightweight (< 1KB script)
- ✅ Simple dashboard with key metrics
- ✅ No personal data collection
- ✅ No consent banner needed

### Setup Instructions:

1. **Sign up for Plausible:**
   - Visit: https://plausible.io
   - Create an account (paid service, ~$9/month)
   - Add your domain (e.g., skyview.com)

2. **Add Tracking Script:**
   - Plausible will provide a script tag like:
   ```html
   <script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
   ```
   - Add this to the `<head>` section of `index.html` (already configured below)

3. **View Analytics:**
   - Access dashboard at: https://plausible.io/yourdomain.com
   - Share public dashboard if desired (optional)

### Metrics Tracked:
- Page views
- Unique visitors
- Top pages
- Referral sources
- Geographic data (country-level only)
- Device types (desktop/mobile)

---

## Alternative 1: Netlify Analytics

**Built into Netlify hosting - No setup required!**

- ✅ Server-side tracking (no JavaScript needed)
- ✅ Cannot be blocked by ad blockers
- ✅ Privacy-friendly
- ✅ $9/month add-on to Netlify

### How to Enable:
1. Go to Netlify dashboard
2. Navigate to: **Site Settings → Analytics**
3. Enable Netlify Analytics
4. View reports directly in Netlify dashboard

### Metrics Tracked:
- Page views
- Unique visitors
- Top pages
- Bandwidth usage
- 404 errors

---

## Alternative 2: GoatCounter

**Free & Open Source**

- ✅ 100% free
- ✅ Privacy-friendly
- ✅ Open source
- ✅ Simple setup

### Setup:
1. Visit: https://www.goatcounter.com
2. Create free account
3. Add script to `<head>`:
```html
<script data-goatcounter="https://yoursite.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
```

---

## Alternative 3: Cloudflare Web Analytics

**Free tier available**

- ✅ Free
- ✅ Privacy-first
- ✅ No cookies
- ✅ Integrated with Cloudflare

### Setup:
1. Add your site to Cloudflare (if not already)
2. Enable Web Analytics in dashboard
3. Add provided script tag to `<head>`

---

## Implementation Status

A **built-in privacy-first conversion baseline** is now shipped in `scripts/conversion-tracking.js`.
It records four launch events without storing PII:
- `landing_view`
- `booking_cta_click`
- `contact_submit`
- `gallery_engagement`

Metrics are persisted locally in `localStorage` under `skyview:conversion-metrics:v1` so launch readiness can be verified before choosing an external analytics provider.

Currently configured for **Plausible Analytics** (optional external forwarding):
- Script is ready and the domain is set to `skyviewdynamics.com`
- Keep `features.analytics` disabled until the Plausible property is confirmed
- Local baseline tracking continues to work even while the external script remains off

### To Activate:
1. Choose your analytics provider (Plausible recommended)
2. Update the `data-domain` attribute with your actual domain
3. Uncomment the script tag in `index.html`
4. Deploy the changes

---

## Comparison Table

| Feature | Plausible | Netlify Analytics | GoatCounter | Cloudflare |
|---------|-----------|-------------------|-------------|------------|
| Cost | $9/mo | $9/mo | Free | Free |
| Privacy | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Setup | Easy | Easiest | Easy | Medium |
| Ad-blocker proof | ❌ | ✅ | ❌ | ❌ |
| Real-time | ✅ | ✅ | ✅ | ✅ |
| Custom events | ✅ | ❌ | Limited | ✅ |

## Recommendation

**For Skyview:** Start with **Plausible Analytics**
- Best balance of features, privacy, and ease of use
- Clean, modern dashboard
- No technical complexity
- Can track custom events (e.g., form submissions, button clicks)

**Budget Option:** Use **Netlify Analytics** if already on Netlify Pro plan

**Free Option:** Try **GoatCounter** first to test analytics before committing to paid

---

## Privacy Policy Note

Even with privacy-friendly analytics, consider adding a simple privacy statement:
- Location: Footer or dedicated page
- Mention: "We use privacy-friendly analytics to understand visitor interest"
- No cookie consent needed for these tools (they don't use cookies)

## Testing

After implementing:
1. Visit your site
2. Wait 5-10 minutes
3. Check analytics dashboard
4. Verify events are being tracked
