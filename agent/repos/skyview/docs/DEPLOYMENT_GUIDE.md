# 🚀 Production Deployment Guide

Complete step-by-step guide to deploy SkyView to production.

---

## 📋 Pre-Deployment Checklist

### 1. Optimize Assets ⚡

```bash
# Install optimization tools
npm install sharp

# Convert images to WebP
npm run optimize:images

# Verify WebP files created
ls assets/gallery/*.webp
```

**Expected Output:**

```
✅ Converted: sunset-marina.jpg → sunset-marina.webp (800 KB saved)
✅ Converted: aerial-waterfront.jpg → aerial-waterfront.webp (1.1 MB saved)
```

### 2. Update Configuration 🔧

#### A. Feature Flags (config.js)

Enable features you want live:

```javascript
features: {
    testimonials: true,     // ✅ Enable when you have real reviews
    contactForm: true,      // ✅ Enable after Netlify Forms setup
    calendly: true,         // ✅ Update URL below
    clientPortal: false,    // ⏳ Keep disabled until production ready
    adminCMS: true,         // ✅ Enable for content management
    preview3D: false,       // ⏳ Future feature
    analytics: true,        // ✅ Enable after adding tracking ID
    platform: false         // ⏳ Marketplace mode — see ROADMAP.md before enabling
},

calendly: {
    url: 'https://calendly.com/YOUR-USERNAME/consultation'  // 🔴 UPDATE THIS!
}
```

#### B. Analytics (index.html)
Uncomment and add your tracking ID:
```html
<!-- Plausible Analytics -->
<script defer data-domain="your-domain.com" src="https://plausible.io/js/script.js"></script>
```

#### C. Contact Information
Update the `contact` block in `config.js` — it's the single place to enter this data, and it propagates to the visible contact info, meta tags, and schema.org structured data automatically:
- `email`, `phone` / `phoneE164`
- `social.facebook` / `.twitter` / `.instagram` / `.youtube`
- `address.locality` / `.region` / `.country` (and `.street` / `.postalCode` if applicable)
- `geo.latitude` / `.longitude` (approximate service-area coordinates)

### 3. Run Tests 🧪
```bash
# Run Playwright E2E tests
npm test

# Run unit tests with coverage
npm run test:unit

# Start local static server for manual testing
npx http-server . -p 8080

# Test in browser at http://localhost:8080
```

### 4. Quality Checks ✅
- [ ] All images load correctly
- [ ] Contact form submits successfully
- [ ] Calendly widget loads
- [ ] Mobile menu works on small screens
- [ ] Gallery lightbox opens
- [ ] Video background plays
- [ ] No console errors

---

## 🌐 Deploy to Netlify

### Method 1: Deploy from GitHub (Recommended)

#### Step 1: Push to GitHub
```bash
# Add all changes
git add .

# Commit with descriptive message
git commit -m "feat: Production ready with WebP optimization"

# Push to GitHub
git push origin main
```

#### Step 2: Connect to Netlify
1. Go to https://app.netlify.com/
2. Click "Add new site" → "Import an existing project"
3. Choose "Deploy with GitHub"
4. Authorize Netlify to access your repo
5. Select your `skyview` repository

#### Step 3: Configure Build Settings
```
Build command: node scripts/build.js
Publish directory: dist
```

#### Step 4: Deploy!
- Click "Deploy site"
- Wait 1-2 minutes for initial deployment
- You'll get a URL like: `https://random-name-123.netlify.app`

### Method 2: Drag & Drop Deploy

#### Step 1: Build Locally
```bash
# Ensure all assets are optimized
npm run optimize:images
```

#### Step 2: Deploy
1. Go to https://app.netlify.com/drop
2. Drag your entire project folder
3. Drop it on the upload area
4. Wait for deployment to complete

---

## ⚙️ Post-Deployment Configuration

### 1. Custom Domain (Optional)
#### Add Your Domain
1. Go to "Domain settings" in Netlify
2. Click "Add custom domain"
3. Enter your domain (e.g., `skyviewdrones.com`)
4. Follow DNS configuration instructions

#### Update DNS Records
Add these records with your domain registrar:
```
Type: CNAME
Name: www
Value: [your-site].netlify.app

Type: A (if using apex domain)
Name: @
Value: 75.2.60.5
```

### 2. Enable Netlify Forms
#### Auto-Setup (Recommended)
Netlify detects forms automatically! Just verify:
1. Go to "Forms" in Netlify dashboard
2. You should see "Contact Form"
3. Set email notification address

#### Manual Setup (If Needed)
Add to your form in [index.html](index.html):
```html
<form name="contact" method="POST" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="contact">
  <!-- rest of form -->
</form>
```

#### Configure Notifications
1. Go to "Forms" → "Form notifications"
2. Click "Add notification" → "Email notification"
3. Enter your email
4. Select "Contact Form"
5. Save

**Test it:** Submit form on live site → Check email

### 3. Enable Netlify Identity (for CMS)
#### Setup Identity
1. Go to "Identity" in Netlify dashboard
2. Click "Enable Identity"
3. Go to "Settings and usage"
4. Click "Registration" → Set to "Invite only"

#### Create Admin User
1. Go to "Identity" tab
2. Click "Invite users"
3. Enter your email
4. Check email for invitation link
5. Set password

#### Configure Git Gateway
1. Go to "Settings" → "Identity" → "Services"
2. Enable "Git Gateway"
3. Click "Generate access token"

**Test it:** Visit `https://your-site.netlify.app/admin` → Log in

### 4. Enable Analytics

#### Plausible Analytics (Recommended - Privacy-Friendly)
1. Sign up at https://plausible.io/ ($9/month)
2. Add your site domain
3. Copy tracking code
4. Already added to index.html! Just uncomment and update domain
5. Enable in config.js: `analytics: true`

#### Netlify Analytics (Built-in)
1. Go to "Analytics" in Netlify dashboard
2. Click "Enable Analytics" ($9/month)
3. Instant server-side tracking (no code changes!)

#### Google Analytics (Free)
1. Create property at https://analytics.google.com/
2. Copy Measurement ID (G-XXXXXXXXXX)
3. Add to index.html:
```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### 5. Configure Environment Variables (If Needed)
1. Go to "Site settings" → "Environment variables"
2. Add any API keys or secrets
3. Never commit these to Git!

---

## 🔒 Security Hardening

### 1. Security Headers

Security headers (CSP, X-Frame-Options, Permissions-Policy, Referrer-Policy, and X-Robots-Tag on admin/portal routes) are **already defined in netlify.toml**. No manual step required. Review or extend the `[[headers]]` blocks in `netlify.toml` if you need to customise them.

### 2. Enable HTTPS
- Automatic on Netlify! ✅
- Certificate auto-renews
- HTTP redirects to HTTPS automatically

### 3. Configure CORS (If Using APIs)
Add to netlify.toml:
```toml
[[headers]]
  for = "/api/*"
  [headers.values]
    Access-Control-Allow-Origin = "https://your-domain.com"
```

---

## 📊 Performance Verification

### 1. Run Lighthouse
1. Open deployed site in Chrome
2. Press F12 → Lighthouse tab
3. Click "Generate report"

**Target Scores:**
- ✅ Performance: 90+
- ✅ Accessibility: 95+
- ✅ Best Practices: 95+
- ✅ SEO: 95+

### 2. Test PageSpeed Insights
1. Visit https://pagespeed.web.dev/
2. Enter your site URL
3. Check mobile + desktop scores

**Target:**
- ✅ Mobile: 90+ (Good)
- ✅ Desktop: 95+ (Good)

### 3. Verify WebP Usage
1. Open site in Chrome
2. Press F12 → Network tab
3. Filter by "Img"
4. Check files being loaded

**Expected:** Should see `.webp` files loading (not `.jpg`)

### 4. Check Core Web Vitals
In browser console, you should see:
```
📊 Performance Metrics:
   ⏱️  Time to First Byte: 45ms
   📄 DOM Ready: 320ms
   ✅ Page Load Complete: 1250ms

🎯 Largest Contentful Paint: 1800ms
⚡ First Input Delay: 50ms
📐 Cumulative Layout Shift: 0.05
```

---

## 🎯 Go-Live Checklist

### Critical (Must Complete)
- [ ] WebP images converted and deployed
- [ ] config.js updated with real Calendly URL
- [ ] Contact form tested and receiving emails
- [ ] Real contact info added (email, phone)
- [ ] All placeholder text replaced
- [ ] Mobile testing completed
- [ ] Lighthouse score 90+
- [ ] HTTPS enabled (automatic)

### Important (Recommended)
- [ ] Custom domain configured
- [ ] Analytics enabled and tracking
- [ ] Netlify Identity configured (for /admin)
- [ ] Security headers added to netlify.toml
- [ ] Sitemap created and submitted to Google
- [ ] Favicon displays correctly
- [ ] Social media preview images set

### Optional (Nice to Have)
- [ ] Real testimonials added (or section disabled)
- [ ] Additional gallery images uploaded
- [ ] Blog/news section added
- [ ] Client portal production implementation
- [ ] 3D preview feature implemented
- [ ] Performance monitoring dashboard

---

## 🔄 Continuous Deployment

### Automatic Deploys
Once connected to GitHub, Netlify automatically deploys when you push:

```bash
# Make changes
git add .
git commit -m "Update gallery images"
git push origin main

# Netlify automatically:
# 1. Detects push
# 2. Builds site
# 3. Deploys to production
# 4. ~30 seconds total
```

### Deploy Previews
For pull requests:
1. Create branch: `git checkout -b new-feature`
2. Make changes and push
3. Create PR on GitHub
4. Netlify creates preview URL
5. Test before merging
6. Merge → Auto-deploys to production

### Rollback (If Needed)
1. Go to "Deploys" in Netlify dashboard
2. Find previous working deploy
3. Click "..." → "Publish deploy"
4. Site instantly reverts

---

## 📈 Monitoring & Maintenance

### Weekly Tasks
- [ ] Check analytics for traffic trends
- [ ] Monitor form submissions
- [ ] Review Lighthouse scores
- [ ] Check for broken links
- [ ] Update gallery with new projects

### Monthly Tasks
- [ ] Review and respond to testimonials
- [ ] Update blog/news (if applicable)
- [ ] Check for dependency updates
- [ ] Review security headers
- [ ] Backup gallery images

### Quarterly Tasks
- [ ] Run comprehensive SEO audit
- [ ] Review and optimize underperforming pages
- [ ] Update content and offerings
- [ ] Refresh testimonials and portfolio
- [ ] Review analytics and set new goals

---

## 🆘 Troubleshooting

### Site Not Loading
- Check Netlify deploy logs for errors
- Verify DNS records (if using custom domain)
- Check for syntax errors in HTML/CSS/JS

### Form Not Working
- Verify `data-netlify="true"` attribute
- Check form name matches notification settings
- Test with valid email address
- Check spam folder

### Images Not Loading
- Verify file paths are correct
- Check Network tab for 404 errors
- Ensure WebP and JPG versions both exist
- Clear cache and hard refresh (Ctrl+Shift+R)

### CMS Not Accessible
- Verify Netlify Identity is enabled
- Check you're logged in
- Ensure Git Gateway is configured
- Try incognito mode (clear cache)

### Performance Issues
- Run Lighthouse to identify bottlenecks
- Check image file sizes (should be < 500 KB each)
- Verify WebP images are being used
- Check for console errors

---

## 🎉 Launch Announcement

### Social Media
Share on:
- [ ] LinkedIn
- [ ] Facebook
- [ ] Instagram
- [ ] Twitter

**Sample Post:**
```
🚁✨ Excited to announce the launch of our new website!

Experience cutting-edge drone services with:
• Stunning aerial photography
• Real-time 3D previews
• Easy online booking
• Professional portfolio gallery

Visit us: [your-site-url]

#DronePhotography #AerialView #NewWebsite
```

### Email Campaign
Send to:
- [ ] Existing clients
- [ ] Email subscribers
- [ ] Business partners

### Google My Business
- [ ] Update website URL
- [ ] Add new photos
- [ ] Post announcement

---

## 📞 Support

### Documentation
- 📖 README.md - Project overview
- 📖 docs/CONFIG.md - Feature flags guide
- 📖 docs/WEBP_OPTIMIZATION.md - Image optimization
- 📖 docs/PERFORMANCE_CHECKLIST.md - Performance guide

### Resources
- **Netlify Docs**: https://docs.netlify.com/
- **Decap CMS Docs**: https://decapcms.org/docs/
- **Calendly Integration**: https://help.calendly.com/

### Getting Help
1. Check documentation first
2. Review deploy logs in Netlify
3. Search Netlify community forums
4. Contact support (paid plans)

---

## ✅ Deployment Complete!

**Congratulations! 🎉** Your site is now live!

### Next Steps:
1. Share your site URL
2. Monitor analytics
3. Gather user feedback
4. Iterate and improve

### Success Metrics to Track:
- Traffic (visitors per month)
- Conversion rate (form submissions / visitors)
- Booking rate (Calendly appointments / visitors)
- Bounce rate (should be < 60%)
- Average session duration (target: 2+ minutes)
- Page load time (target: < 3 seconds)

---

**Need help?** Check the docs folder or review Netlify deploy logs.

**Ready to scale?** See ROADMAP.md for planned Q4 2026 and 2027 features.
