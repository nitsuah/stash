# Feature Flags & Configuration Guide

> 🧭 [skyview](../README.md) · [Features](./FEATURES.md) · [Roadmap](./ROADMAP.md) · [Tasks](./TASKS.md) · [Changelog](./CHANGELOG.md) · [Metrics](../METRICS.md) <!-- nav -->
>
> **Outdated as of 2026-09-19:** the `contactForm`, `calendly`, `platform` and `analyticsDebugPanel` flags no longer exist. The contact form and Calendly were removed from the marketing site (people are sent to the platform at `/app`; the contact email/phone live only on `pages/privacy.html`), and the conversion dashboard is admin-only. Sections below that mention those flags are historical; see `config.js` for the current flags.

## Overview

The Skyview website uses a simple configuration file (`config.js`) to control which features are visible. This allows you to easily enable/disable sections as they become ready for production.

## Quick Start

**To enable/disable features, edit `config.js`:**

```javascript
window.SKYVIEW_CONFIG = {
    features: {
        testimonials: false,       // ← Change to true when you have reviews
        calendly: true,            // ← Already enabled (ready to use!)
        clientPortal: false,       // ← Enable when ready to deliver files
        adminCMS: true,            // ← Enable when Netlify Identity is set up
        analytics: false,          // ← Enable when analytics is configured
        platform: false            // ← Marketplace mode; see ROADMAP.md before enabling
    }
}
```

Current live defaults are always in `config.js` itself — treat the snippet above as illustrative, not authoritative.

**That's it!** Change `false` to `true` to enable, `true` to `false` to disable.

---

## Feature Flags Explained

### 1. Testimonials (`testimonials`)

**Default:** `false` (hidden)

**What it does:**
- Shows/hides the "Client Testimonials" section
- Shows/hides "REVIEWS" link in navigation menu

**When to enable:**
- After you collect real client testimonials
- Replace the example testimonials in `index.html` first
- Should have at least 3-5 real reviews

**To enable:**
```javascript
testimonials: true
```

---

### 2. Contact Form (`contactForm`)

**Default:** `false` (hidden)

**What it does:**
- Shows/hides the **entire Contact section**
- When disabled, hides "CONTACT" link in navigation
- When disabled, no contact information is shown on the site

**When to enable:**
- After setting up Netlify Forms email notifications
- When you're ready to receive form submissions
- After testing the form works correctly

**Setup required:**
1. Deploy to Netlify
2. Set up form notifications in Netlify dashboard
3. Test submission
4. Enable flag

**To enable:**
```javascript
contactForm: true
```

---

### 3. Calendly Booking (`calendly`)

**Default:** `true` (enabled)

**What it does:**
- Shows/hides the entire Booking section
- Shows/hides "BOOKING" link in navigation
- Controls where the hero "BOOK A CONSULTATION" button links to
  - If enabled: Links to #booking
  - If disabled: Links to #contact instead

**When to disable:**
- If Calendly account isn't set up yet
- During maintenance

**Configuration:**
Update the Calendly URL in `config.js`:
```javascript
calendly: {
    url: 'https://calendly.com/YOUR-USERNAME/consultation',
    primaryColor: '00d4ff',
    hideGdprBanner: true
}
```

**Hero CTA Behavior:**
The "BOOK A CONSULTATION" button automatically updates based on what's enabled:
- Calendly enabled → Links to #booking
- Calendly disabled, Contact enabled → Links to #contact  
- Both disabled → Links to #gallery and changes text to "VIEW OUR WORK"

**To disable:**
```javascript
calendly: false
```

---

### 4. Client Portal (`clientPortal`)

**Default:** `false` (hidden)

**What it does:**
- Currently just a console log (placeholder)
- In future: Could add footer link to `/client-portal.html`

**When to enable:**
- After choosing client portal implementation
- When ready to deliver files to clients
- See `docs/CLIENT_PORTAL.md` for options

**To enable:**
```javascript
clientPortal: true
```

---

### 5. Admin CMS (`adminCMS`)

**Default:** `true` (enabled)

**What it does:**
- Currently just tracks status
- Admin panel is available at `/admin` regardless
- Requires Netlify Identity to be configured

**Setup required:**
1. Deploy to Netlify
2. Enable Netlify Identity
3. Invite yourself as user
4. Visit `/admin` to manage gallery

**To disable:**
```javascript
adminCMS: false
```

---

### 6. 3D Preview (`preview3D`)

**Default:** `false` (hidden)

**What it does:**
- Shows/hides the "INTERACTIVE 3D PREVIEW" card in the gallery section
- This is a placeholder for future 3D viewer functionality

**When to enable:**
- When you implement a 3D viewer/model viewer
- When you have 3D scans or models to showcase
- Currently just a "Coming Soon" placeholder

**To enable:**
```javascript
preview3D: true
```

---

### 7. Analytics (`analytics`)

**Default:** `false` (disabled)

**What it does:**
- Automatically loads analytics script when enabled
- No need to manually add script tags
- Supports multiple providers

**Configuration:**
```javascript
analytics: {
    provider: 'plausible',  // or 'netlify', 'goatcounter', 'none'
    domain: 'yourdomain.com'
}
```

**To enable:**
```javascript
analytics: true
```

Then set up your chosen provider account and update the domain.

---

## Configuration Options

### Contact Information

This is the **single place** to enter real business identity data. It
propagates to the visible contact info (`[data-contact-email]` /
`[data-contact-phone]` elements), meta tags, and the schema.org
`LocalBusiness` structured data automatically (`applyContactIdentity()` and
`updateStructuredData()` in `config.js`) — no other file needs to change.

```javascript
contact: {
    email: 'your@email.com',
    phone: '+1 (555) 123-4567',
    phoneE164: '+15551234567',
    social: {
        facebook: 'https://facebook.com/yourpage',
        twitter: 'https://twitter.com/yourusername',
        instagram: 'https://instagram.com/yourusername',
        youtube: 'https://youtube.com/yourchannel'
    },
    address: {
        locality: 'Your City',
        region: 'State',
        country: 'US'
        // street / postalCode optional — a service-area business doesn't need a full street address
    },
    geo: {
        latitude: '0.0',   // approximate service-area coordinates, not pinpoint navigation
        longitude: '0.0'
    }
}
```

As of the 2026-09 cycle, every value above is still a placeholder on the
live site — see TASKS.md "Complete the launch checklist with verified
production identity data" for exactly what's needed from the business owner.
`contact.phone` and `contact.phoneE164` serve different purposes: `phone` is
the human-readable string shown in visible contact elements
(`[data-contact-phone]`), while `phoneE164` feeds `telephone` in the
schema.org structured data, which requires E.164 format. Both fields fall
back to the other if only one is set, so a config with just one filled in
still populates both surfaces — but for correct display formatting, set
`phone` explicitly rather than relying on the raw E.164 fallback.
`contact.geo`'s placeholder `'0.0'` values are deliberately **not**
published to the JSON-LD `geo` block — `updateStructuredData()` omits `geo`
entirely until both `latitude` and `longitude` are set to real, non-`'0.0'`
values, since publishing `(0, 0)` (a real ocean location) would be worse than
omitting the optional field.

---

## Typical Launch Progression

### Week 1: Initial Launch
```javascript
features: {
    testimonials: false,     // Don't have reviews yet
    contactForm: false,      // Still testing
    calendly: true,          // Ready! ✅
    clientPortal: false,     // Not needed yet
    adminCMS: true,          // Set up for managing gallery
    preview3D: false,        // Not implemented yet
    analytics: false         // Will add later
}
```

### Week 2-4: Full Launch
```javascript
features: {
    testimonials: false,     // Still collecting
    contactForm: true,       // Now accepting leads! ✅
    calendly: true,          // ✅
    clientPortal: false,     // Working on it
    adminCMS: true,          // ✅
    preview3D: false,        // Future feature
    analytics: true          // Now tracking! ✅
}
```

### Month 2+: Mature Site
```javascript
features: {
    testimonials: true,      // Got 5+ reviews! ✅
    contactForm: true,       // ✅
    calendly: true,          // ✅
    clientPortal: true,      // Delivering files! ✅
    adminCMS: true,          // ✅
    preview3D: true,         // 3D viewer implemented! ✅
    analytics: true          // ✅
}
```

---

## How It Works (Technical)

The `config.js` file:
1. Defines a global `window.SKYVIEW_CONFIG` object
2. Runs on `DOMContentLoaded` event
3. Checks each feature flag
4. Shows/hides sections using `display: none`
5. Adds "Coming Soon" messages where appropriate

**Benefits:**
- ✅ One file to control everything
- ✅ No code changes needed to enable features
- ✅ Easy to test features before public launch
- ✅ Graceful handling of disabled sections
- ✅ No broken links or empty pages

---

## Testing Feature Flags

**To test different configurations:**

1. Edit `config.js`
2. Save the file
3. Refresh your browser (hard refresh: Ctrl+F5)
4. Check that sections appear/disappear correctly

**Things to verify:**
- [ ] Navigation links hide when sections are disabled
- [ ] Disabled sections don't show in page
- [ ] "Coming Soon" message appears for contact form
- [ ] Hero CTA button points to correct section
- [ ] No console errors

---

## Pro Tips

### Gradual Rollout
Enable features one at a time to test thoroughly:
```javascript
// Day 1: Just calendly
calendly: true

// Day 3: Add contact form
contactForm: true

// Week 2: Add analytics
analytics: true

// Month 2: Add testimonials
testimonials: true
```

### Staging vs Production
Use different configs for testing vs live:

**Local/Staging:**
```javascript
testimonials: true  // Test with example data
```

**Production:**
```javascript
testimonials: false  // Hide until real reviews
```

### Maintenance Mode
Quickly disable features during maintenance:
```javascript
features: {
    testimonials: false,
    contactForm: false,  // Temporarily disable while fixing
    calendly: false,     // Temporarily disable during update
    // ...
}
```

---

## Common Scenarios

### "I'm not ready for any leads yet"
```javascript
contactForm: false
calendly: false
```
Visitors can see your work but can't book/contact yet.
- Hero button changes to "VIEW OUR WORK" → links to gallery
- No contact or booking sections visible
- Perfect for portfolio-only mode

---

### "I want bookings but not form submissions"
```javascript
contactForm: false
calendly: true
```
People can book consultations via Calendly only.

---

### "I'm launching today!"
```javascript
contactForm: true
calendly: true
analytics: true
```
Full lead generation mode! 🚀

---

### "Testing the site before going live"
```javascript
// Enable everything to test
testimonials: true
contactForm: true
calendly: true
clientPortal: true
analytics: false  // Don't track test traffic
```

---

## Troubleshooting

### Feature not hiding/showing?
1. Check `config.js` syntax (commas, quotes)
2. Hard refresh browser (Ctrl+F5)
3. Check browser console for errors (F12)
4. Verify section IDs match (`#testimonials`, `#booking`, etc.)

### "Coming Soon" message not showing?
- Only shows for contact form when disabled
- Make sure `contactForm: false` is set

### Calendly URL not updating?
- Check format: `https://calendly.com/username/event`
- Refresh page after changing config
- Make sure Calendly script is loaded

---

## Advanced: Custom Feature Flags

You can add your own feature flags:

```javascript
features: {
    // ... existing flags ...
    promotionalBanner: true,
    specialOffer: false,
    holidayTheme: false
}
```

Then add logic in your HTML/JS:
```javascript
if (window.SKYVIEW_CONFIG.features.promotionalBanner) {
    // Show banner
}
```

---

## File Reference

- **config.js** - Main configuration file (edit this!)
- **index.html** - Loads config.js in `<head>`
- **docs/CONFIG.md** - This documentation

---

## Summary

**Config file location:** `config.js`

**To enable a feature:** Change `false` → `true`

**To disable a feature:** Change `true` → `false`

**When to use:**
- ✅ Gradually rolling out features
- ✅ Testing before launch
- ✅ Maintenance/downtime
- ✅ A/B testing (advanced)

**No coding required** - just edit one file! 🎉
