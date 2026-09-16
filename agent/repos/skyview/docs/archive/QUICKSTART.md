# ⚡ Quick Start Guide for Your Friend

**Welcome to your new website!** Here's everything you need to know in 5 minutes.

---

## 🎯 Your Website Has:

✅ Beautiful homepage with services  
✅ Dynamic photo/video gallery  
✅ Contact form (captures leads)  
✅ Booking calendar integration  
✅ Testimonials from "clients"  
✅ Admin panel to manage photos  
✅ Client portal (prototype)  
✅ Privacy policy  
✅ Mobile-friendly design  

---

## 🔧 What YOU Need to Do:

### Prerequisite: Enable/Disable Features (2 min) ⚡
**This controls what shows on your site!**

1. Open `config.js` in your code editor
2. Look at the `features:` section
3. Current settings (good defaults!):
   ```javascript
   testimonials: false,    // Hidden (you don't have reviews yet)
   contactForm: false,     // Hidden (form not set up yet)
   calendly: true,         // Visible (ready to use!)
   ```
4. Keep these for now - we'll enable more later!

### 1. Deploy the Website (10 min)
1. Go to **netlify.com** and sign up (free)
2. Click "Add new site" → "Import from Git"
3. Connect your GitHub repo
4. Click "Deploy" (that's it!)
5. You'll get a URL like: `random-name-123.netlify.app`

### 2. Set Up Admin Access (5 min)
1. In Netlify dashboard: **Identity** → "Enable Identity"
2. **Settings** → "Registration" → "Invite only"
3. **Identity tab** → "Invite users" → Enter YOUR email
4. Check your email and accept invite
5. Visit: `your-site.netlify.app/admin`
6. Log in with your email
7. Now you can add/edit gallery photos! 🎉

### 3. Connect Your Calendly (3 min)
1. Go to **calendly.com** and create account (free)
2. Create a meeting type (e.g., "15-min Consultation")
3. Copy your Calendly URL (looks like: `calendly.com/yourname`)
4. **Open `config.js` file**
5. Find the `calendly:` section
6. Replace `skyviewdynamics` with YOUR Calendly username:
   ```javascript
   calendly: {
       url: 'https://calendly.com/YOUR-NAME/consultation',
   }
   ```
7. Push change to GitHub (Netlify auto-deploys)

### 4. Get Email Notifications (2 min)
1. Netlify dashboard → **Forms**
2. Click "Form notifications"
3. "Add notification" → "Email notification"
4. Enter your email address
5. **Open `config.js` and enable form:**
   ```javascript
   contactForm: true
   ```
6. Push to GitHub
7. Done! Form is now live and you'll get email notifications!

---

## 📱 How to Use the Admin Panel

After step 2 above:

1. Go to: `your-site.netlify.app/admin`
2. Log in
3. Click "Gallery Assets"
4. Click "New Gallery Asset"
5. Upload a photo/video
6. Fill in title, type, tags
7. Click "Publish"
8. Photo appears on your website immediately! ✨

---

## 📝 Optional Setup (Do Later):

### Custom Domain (Instead of netlify.app URL)
1. Buy domain (Google Domains, Namecheap, etc.)
2. Netlify: "Domain settings" → "Add custom domain"
3. Follow instructions to point DNS
4. Free SSL certificate included!

### Analytics (See who visits)
- **Option 1:** Netlify Analytics ($9/mo) - Turn on in dashboard
- **Option 2:** Plausible ($9/mo) - Sign up, then in `config.js` set `analytics: true`
- **Option 3:** Free tracking with GoatCounter

### Social Media Links
- Update footer in `index.html` with your real Instagram/YouTube links

---

## 🎨 How to Update Content

### Change Text
- Edit `index.html` in VS Code or GitHub
- Push changes → Auto-deploys in ~1 minute

### Add/Remove Photos
- Use the `/admin` panel (easiest!)
- Or edit `assets/gallery.json` manually

### Update Pricing
- Edit "Services" section in `index.html`

### Change Colors/Styling
- Edit `styles/style.css`

---

## 📁 Important Files

| File | What It Does |
|------|--------------|
| `config.js` | **🎯 FEATURE FLAGS - Controls what's visible!** |
| `index.html` | Main website page |
| `styles/style.css` | All the styling |
| `assets/gallery.json` | Your photos/videos data |
| `/admin` | Content management system |
| `MANUAL_SETUP.md` | Detailed setup instructions |

---

## 🆘 Something Broken?

### Contact form not working?
- Make sure you deployed to Netlify (works automatically there)
- Check spam folder for test emails

### Admin login not working?
- Make sure you enabled Netlify Identity
- Check that you accepted the invite email

### Gallery not showing photos?
- Check `assets/gallery.json` formatting
- Make sure image files are in `assets/gallery/` folder

### Calendly not showing?
- Make sure you replaced the placeholder URL
- Check that your Calendly event type is active

---

## 💰 Cost Breakdown

**Free:**
- Netlify hosting (free tier is plenty)
- Netlify Identity (100 users free)
- Netlify Forms (100 submissions/month free)
- Calendly (free plan works great)

**Optional Paid:**
- Custom domain: ~$12/year
- Analytics: $0-9/month
- More form submissions: $19/month
- Calendly Pro: $10/month (for more features)

**Total to start: $0** 🎉

---

## 🚀 Launch Checklist

Before sharing with clients:

- [ ] Deployed to Netlify
- [ ] Admin access working
- [ ] Calendly URL updated
- [ ] Email notifications set up
- [ ] Tested contact form
- [ ] Added at least 5-10 real photos to gallery
- [ ] Updated contact info in footer (email, phone)
- [ ] Changed example testimonials to real ones (or remove)
- [ ] Test on phone to make sure mobile works

---

## 📞 Need Help?

1. **Check the docs folder** - Detailed guides for everything
2. **Read MANUAL_SETUP.md** - Step-by-step instructions
3. **Google/YouTube** - Tons of Netlify tutorials
4. **Netlify Support** - Great documentation
5. **Ask me!** - I'm here to help

---

## 🎉 You're Almost There!

Just do the 4 setup steps above and you'll have a **professional website live in 20 minutes!**

Your new online presence will:
- Impress potential clients
- Capture leads automatically
- Let people book consultations
- Showcase your best work
- Run 24/7 with no effort

**Time to launch! 🚀**

---

**P.S.** - Update your email signature, business cards, and social media with your new website URL once it's live!
