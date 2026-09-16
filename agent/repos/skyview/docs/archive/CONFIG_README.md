# 🎯 Quick Config Guide

**Want to show/hide features on your site? Edit `config.js`!**

## Current Settings

```javascript
features: {
    testimonials: false,     // ❌ Hidden (add reviews first)
    contactForm: false,      // ❌ Hidden (set up Netlify Forms first)
    calendly: true,          // ✅ Visible (ready to use!)
    clientPortal: false,     // ❌ Hidden (not needed yet)
    adminCMS: true,          // ✅ Ready (configure Netlify Identity)
    preview3D: false,        // ❌ Hidden (future feature)
    analytics: false         // ❌ Hidden (add later)
}
```

## How to Enable Features

1. Open `config.js`
2. Change `false` to `true` for the feature you want
3. Save the file
4. Push to GitHub (Netlify auto-deploys)
5. Done! ✨

## Examples

**Enable contact form:**
```javascript
contactForm: true  // ← Change this line
```

**Enable testimonials:**
```javascript
testimonials: true  // ← Change this line
```

**Update Calendly URL:**
```javascript
calendly: {
    url: 'https://calendly.com/YOUR-USERNAME/consultation',  // ← Update this
}
```

## Full Documentation

- **Detailed guide:** [docs/CONFIG.md](docs/CONFIG.md)
- **Setup checklist:** [MANUAL_SETUP.md](MANUAL_SETUP.md)
- **Quick start:** [QUICKSTART.md](QUICKSTART.md)

---

**That's it!** One file controls your entire site. 🚀
