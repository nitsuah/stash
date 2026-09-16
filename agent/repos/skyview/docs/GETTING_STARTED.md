# Getting Started with SkyView Website

Welcome! This guide will help you get the SkyView drone services website up and running. Everything is set up and ready - you just need to configure a few things.

## 🎯 What's Already Done

Your website includes:
- ✅ Professional design with animations
- ✅ Services showcase with pricing
- ✅ Dynamic photo & video gallery
- ✅ Contact form ready for Netlify
- ✅ Calendly booking integration
- ✅ Client portal system (password-protected file delivery)
- ✅ Testimonials section
- ✅ Privacy policy page
- ✅ WebP image optimization (30-40% smaller files!)
- ✅ Video support (MP4/MOV files)
- ✅ Performance monitoring

## 🚀 Quick Launch (30 Minutes)

### 🐳 Docker Workflow

If Node.js is not installed locally, use Docker for the main validation path:

```bash
# Serve the production container locally
docker compose -f config/docker-compose.yml up --build web

# Run the unit suite with coverage in Docker
docker compose -f config/docker-compose.yml run --rm unit
```

The recommended dev command is `npm run dev` (runs `netlify dev` on port 8888 with Netlify Functions and Identity active). A static fallback is `npx http-server . -p 3000` for quick previews without Functions.

### Step 1: Deploy to Netlify (10 min)
```bash
# If not already deployed
1. Push code to GitHub
2. Go to https://netlify.com
3. Click "Add new site" → "Import an existing project"
4. Connect GitHub and select the skyview repository
5. Click "Deploy site"
```

**Detailed Guide:** See `docs/DEPLOYMENT_GUIDE.md`

### Step 2: Configure Features (5 min)

Open `config.js` in the root folder and customize:

```javascript
// Update these first!
calendly: {
    url: 'https://calendly.com/YOUR-USERNAME/consultation',
}

// Enable features you want visible
features: {
    testimonials: true,   // Show testimonials section
    contactForm: true,    // Show contact form (after Netlify setup)
    calendly: true,       // Show booking section
    clientPortal: true,   // Show client login link
    analytics: true,      // Enable analytics (after setup)
}
```

**Full Options:** See `docs/CONFIG.md`

### Step 3: Set Up Admin Access (10 min)

1. Go to Netlify Dashboard → Identity
2. Enable Netlify Identity
3. Settings → Registration → "Invite only"
4. Invite yourself via email
5. Visit `https://yoursite.netlify.app/admin`
6. Log in with your credentials

Now you can manage gallery content without touching code!

### Step 4: Configure Notifications (5 min)

1. Submit a test form on your site
2. Netlify Dashboard → Forms → "Form notifications"
3. Add your email to receive submissions

**Detailed Guide:** See `docs/EMAIL_NOTIFICATIONS.md`

## 📸 Managing Your Gallery

### Adding Images

1. **Drop JPG/PNG files** into `assets/gallery/` folder
2. **Convert to WebP** (smaller file size):
   ```bash
   npm run optimize:images
   ```
3. **Add to gallery.json:**
   ```json
   {
     "src": "assets/gallery/your-photo.jpg",
     "alt": "Description for SEO",
     "category": "real_estate",
     "featured": true
   }
   ```
4. Push to GitHub - auto-deploys!

### Adding Videos

1. **Drop MP4/MOV files** into `assets/gallery/` folder
2. **Add to gallery.json** with `type: "video"`:
   ```json
   {
     "src": "assets/gallery/your-video.mp4",
     "alt": "Video description",
     "category": "landscape",
     "type": "video"
   }
   ```
3. Gallery automatically shows videos with controls!

**Full Guide:** See `docs/WEBP_OPTIMIZATION.md`

## 🎨 Customization

### Colors & Branding
Edit `styles/style.css`:
```css
:root {
    --color-primary: #0a0e27;      /* Dark blue background */
    --color-secondary: #00d4ff;    /* Cyan accent */
    --color-accent: #ff4444;       /* Red CTA buttons */
}
```

### Text Content
Edit `index.html` - all sections clearly labeled:
- Hero section (lines 75-95)
- Services section (lines 100-200)
- Gallery section (lines 170-185)
- Testimonials section (lines 300-350)

### Calendly Settings
Update `config.js`:
```javascript
calendly: {
    url: 'your-calendly-link',
    height: 700,
    text: 'Schedule a Free Consultation',
    primaryColor: '00d4ff'
}
```

## 📊 Analytics Setup (Optional)

### Option A: Plausible (Privacy-Friendly)
1. Sign up at https://plausible.io
2. Add your domain
3. Update `config.js`:
   ```javascript
   analytics: {
       provider: 'plausible',
       domain: 'yourdomain.com'
   }
   ```

### Option B: Netlify Analytics
1. Netlify Dashboard → Analytics
2. Enable ($9/month)
3. No code changes needed!

**Full Guide:** See `docs/ANALYTICS_SETUP.md`

## 🔒 Client Portal Setup

Already built and ready! Clients can:
- Log in with access codes you provide
- View their project files
- Download photos/videos individually or in bulk

**Usage Guide:** See `docs/CLIENT_PORTAL.md`

## 📱 Testing Checklist

Before going live:
- [ ] Test contact form submission
- [ ] Test Calendly booking flow
- [ ] Check gallery loads images AND videos
- [ ] Test on mobile device
- [ ] Test client portal login
- [ ] Verify email notifications work
- [ ] Check all links in navigation

## 🆘 Common Issues

### Gallery shows broken images
- Run `npm run optimize:images` to create WebP versions
- Check `assets/gallery.json` paths match actual files
- Hard refresh browser (Ctrl+Shift+R)

### Calendly not showing
- Check `config.js` has correct Calendly URL
- Verify `features.calendly: true` in config
- Check browser console for errors

### Contact form not working
- Deploy to Netlify first (forms don't work locally)
- Enable Netlify Identity
- Configure email notifications in Netlify dashboard

### Videos not playing
- Make sure files are MP4 or MOV format
- Add `"type": "video"` to gallery.json entry
- Check file path is correct

## 📚 Documentation Index

- `DEPLOYMENT_GUIDE.md` - Detailed Netlify deployment
- `CONFIG.md` - config.js reference
- `WEBP_OPTIMIZATION.md` - Image optimization details
- `EMAIL_NOTIFICATIONS.md` - Form notification setup
- `CLIENT_PORTAL.md` - Client delivery system
- `ANALYTICS_SETUP.md` - Analytics options
- `PERFORMANCE_CHECKLIST.md` - Performance tips

## 🎉 You're Ready!

Your site is production-ready. Just:
1. Deploy to Netlify
2. Update config.js
3. Add your photos/videos
4. Set up email notifications

Questions? Check the docs/ folder or the inline comments in the code.

**Last Updated:** 2026-08-22
