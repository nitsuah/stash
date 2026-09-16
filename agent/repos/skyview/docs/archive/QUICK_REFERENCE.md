# 🚀 Quick Reference Card

**One-page reference for common tasks**

---

## 🎯 Common Commands

```bash
# Development
npm run dev                      # Start Netlify dev server (port 8888)
npm run optimize:images          # Convert images to WebP

# Testing
npm test                         # Run E2E tests
npm run test:unit                # Run unit tests
npm run test:unit -- --coverage  # Run with coverage

# Lighthouse Score
# F12 → Lighthouse tab → Generate report
```

---

## ⚙️ Feature Toggles (config.js)

```javascript
features: {
    testimonials: false,    // Show/hide testimonials
    contactForm: false,     // Show/hide contact form
    calendly: true,         // Show/hide booking
    clientPortal: false,    // Show/hide client portal
    adminCMS: true,         // Enable /admin access
    preview3D: false,       // 3D preview (future)
    analytics: false        // Analytics tracking
}
```

**Quick toggle**: Edit `config.js` → refresh page

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `config.js` | Feature flags & settings |
| `index.html` | Main website page |
| `styles/style.css` | All styling |
| `scripts/main.js` | JavaScript entry point |
| `assets/gallery.json` | Gallery content |
| `netlify.toml` | Netlify configuration |

---

## 🖼️ Image Workflow

### Adding New Images

1. **Add to folder**:
   ```
   assets/gallery/new-image.jpg
   ```

2. **Convert to WebP**:
   ```bash
   npm run optimize:images
   ```

3. **Update gallery**:
   ```json
   {
     "src": "assets/gallery/new-image.jpg",
     "alt": "Description",
     "category": "landscape"
   }
   ```

4. **Verify**: Both `.jpg` and `.webp` files should exist

---

## 🔍 Troubleshooting

### Images not loading?
```bash
# Check file paths
ls assets/gallery/

# Re-optimize
npm run optimize:images
```

### Form not working?
1. Check Netlify Forms is enabled
2. Verify `data-netlify="true"` in HTML
3. Test on deployed site (not localhost)

### CMS not accessible?
1. Enable Netlify Identity in dashboard
2. Visit `/admin` on deployed site
3. Create user invitation

### Performance issues?
1. Run Lighthouse (F12 → Lighthouse)
2. Check console for errors
3. Verify WebP images loading

---

## 📊 Performance Targets

| Metric | Target | How to Check |
|--------|--------|--------------|
| Lighthouse Score | 90+ | F12 → Lighthouse |
| Page Size | < 3.5 MB | F12 → Network |
| Load Time (3G) | < 10s | DevTools → Throttling |
| WebP Usage | 90%+ | Console logs |

---

## 🚀 Deploy Checklist

### Before Deploy
- [ ] `npm run optimize:images`
- [ ] Update config.js (Calendly URL)
- [ ] Test locally (`npm run serve`)
- [ ] Run Lighthouse (score 90+)

### Deploy to Netlify
1. Push to GitHub
2. Connect repo to Netlify
3. Deploy (automatic)
4. Configure Netlify Forms
5. Enable Netlify Identity
6. Test live site

---

## 📚 Documentation Quick Links

- [Quick Start](../QUICKSTART.md) - 5-min setup
- [Deployment](DEPLOYMENT_GUIDE.md) - Production deploy
- [Performance](PERFORMANCE_CHECKLIST.md) - Optimization
- [WebP Guide](WEBP_OPTIMIZATION.md) - Image optimization
- [Manual Setup](MANUAL_SETUP.md) - Configuration

---

## 🛠️ Useful Tools

### Online
- [Squoosh](https://squoosh.app/) - Image optimizer
- [PageSpeed](https://pagespeed.web.dev/) - Performance test
- [WebPageTest](https://webpagetest.org/) - Advanced testing
- [TinyJPG](https://tinyjpg.com/) - Image compression

### CLI
```bash
# Install tools
npm install -g http-server       # Local server
npm install sharp                # Image processing

# Quick tests
npx lighthouse https://your-site.com --view
```

---

## 💡 Pro Tips

1. **Always test locally first**: `npm run serve`
2. **Check console logs**: Look for performance metrics
3. **Keep originals**: Never delete JPG files (they're fallbacks)
4. **Quality 85**: Best balance for WebP conversion
5. **Test on mobile**: Real devices, not just simulators
6. **Monitor metrics**: Check Lighthouse regularly
7. **Use feature flags**: Easy enable/disable without code changes
8. **Commit often**: Small commits are easier to debug

---

## 🔑 Environment Variables

### For Future Use

```bash
# Netlify Environment Variables
CALENDLY_API_KEY=your-key-here
ANALYTICS_ID=your-id-here
CONTACT_EMAIL=your-email@example.com
```

Set in: Netlify Dashboard → Site settings → Environment variables

---

## 📞 Quick Help

### Can't find something?
```bash
# Search for text in files
grep -r "search term" .

# Find files
find . -name "filename"

# Check file structure
tree -L 2
```

### Need to revert?
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all changes
git restore .
```

### Server issues?
```bash
# Kill process on port
# Windows PowerShell:
Get-Process -Id (Get-NetTCPConnection -LocalPort 8080).OwningProcess | Stop-Process

# Mac/Linux:
lsof -ti:8080 | xargs kill
```

---

## 🎯 Success Checklist

### Development Ready
- [x] WebP optimization implemented
- [x] Performance monitoring active
- [x] Feature flags working
- [x] Documentation complete

### Production Ready
- [ ] Images converted to WebP
- [ ] Config.js updated (real URLs)
- [ ] Lighthouse score 90+
- [ ] All features tested
- [ ] Deployed to Netlify
- [ ] Forms configured
- [ ] Analytics enabled

---

**Last Updated**: December 13, 2025
**Status**: ✅ Development Complete - Ready for Production!

---

Need more help? Check the [docs/](.) folder for comprehensive guides!
