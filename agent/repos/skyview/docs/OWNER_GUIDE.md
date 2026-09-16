# SkyView Website - Owner's Guide

**Welcome!** This is your complete, production-ready drone services website. Everything works - you just need to plug in your accounts and content.

## 🎉 What You Have

Your website is **fully built** with:

### Visitor Features
- Professional hero section with video background
- Services showcase with pricing
- Photo & video gallery (automatic optimization)
- Contact form (email notifications)
- Calendly booking integration
- Testimonials section
- Privacy policy page
- Mobile-responsive design

### Behind the Scenes
- Admin dashboard for managing gallery
- Client portal for delivering files
- Automatic WebP image conversion (30-40% smaller files)
- Video support (MP4/MOV)
- Performance monitoring
- Feature flags (turn sections on/off easily)

## 🚦 Launch Checklist (30 Minutes Total)

### Before You Start
✅ Website code is complete  
✅ All features tested and working  
✅ Documentation ready  

### Your 4 Steps

#### 1. Deploy (10 min) 🚀
```
Push to GitHub → Connect to Netlify → Auto-deploys!
```
**Guide:** `docs/DEPLOYMENT_GUIDE.md`

#### 2. Configure (10 min) ⚙️
Edit `config.js` file:
- Add your Calendly booking URL
- Turn on features you want visible
- Set your business info

**Guide:** `docs/CONFIG.md`

#### 3. Add Content (5 min) 📸
- Drop photos/videos in `assets/gallery/` folder
- Run `npm run optimize:images`
- Update `assets/gallery.json`

**Guide:** `docs/WEBP_OPTIMIZATION.md`

#### 4. Setup Notifications (5 min) 📧
- Enable Netlify Identity
- Configure email notifications
- Test contact form

**Guide:** `docs/EMAIL_NOTIFICATIONS.md`

## 📖 Documentation Map

**START HERE:**
- 📘 **[Getting Started](docs/GETTING_STARTED.md)** ← **Read this first!**

**Setup & Configuration:**
- [Configuration Reference](docs/CONFIG.md) - What each setting does
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Publishing to web

**Adding Content:**
- [WebP Optimization](docs/WEBP_OPTIMIZATION.md) - Images & videos
- [Asset Management](docs/ASSET_MANAGEMENT.md) - Organizing files

**Advanced Features:**
- [Client Portal](docs/CLIENT_PORTAL.md) - Delivering files to clients
- [Email Notifications](docs/EMAIL_NOTIFICATIONS.md) - Form alerts
- [Analytics Setup](docs/ANALYTICS_SETUP.md) - Tracking visitors

**Performance:**
- [Performance Checklist](docs/PERFORMANCE_CHECKLIST.md) - Speed tips
- [Optimization Flow](docs/OPTIMIZATION_FLOW.md) - Technical details

## 🎯 Common Tasks

### "I want to add a new photo"
1. Put JPG in `assets/gallery/` folder
2. Run `npm run optimize:images`
3. Add entry to `assets/gallery.json`
4. Push to GitHub (auto-deploys)

### "I want to add a video"
1. Put MP4/MOV in `assets/gallery/` folder
2. Add to `assets/gallery.json` with `"type": "video"`
3. Push to GitHub

### "I want to turn off testimonials"
1. Open `config.js`
2. Change `testimonials: false`
3. Push to GitHub

### "I want to update my booking link"
1. Open `config.js`
2. Update `calendly.url`
3. Push to GitHub

### "I want to get form submissions by email"
1. Netlify Dashboard → Forms
2. Form notifications → Add email
3. Done!

## 🆘 Troubleshooting

### "Gallery images look broken"
→ Run `npm run optimize:images` to create WebP versions

### "Videos won't play"
→ Make sure you added `"type": "video"` to gallery.json

### "Contact form doesn't work locally"
→ Forms only work on Netlify (after deployment)

### "Calendly widget shows 404"
→ Update the URL in `config.js` to your actual Calendly link

### "Changes don't show up"
→ Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

## 💡 Pro Tips

1. **Test in preview first**: Netlify creates preview URLs for each commit
2. **Keep backups**: Your GitHub repo is your backup
3. **Document your changes**: Use commit messages
4. **Check mobile**: Test on your phone before announcing
5. **Monitor forms**: Check Netlify dashboard weekly for submissions

## 🔐 Important Info to Save

Write these down somewhere safe:

- **Netlify Account**: [Your email]
- **Netlify Site URL**: [Will get after deploy]
- **GitHub Repo**: https://github.com/nitsuah/skyview
- **Calendly URL**: [Your Calendly link]
- **Admin Email**: [Email for form notifications]
- **Client Portal Codes**: [Create as needed]

## 📊 What's Next?

Your site is **production-ready**. After launch:

### Optional Improvements
- Set up analytics (Plausible or Netlify Analytics)
- Add your custom domain
- Create client portal codes for your first projects
- Add more testimonials as you get them
- Keep adding new drone footage to gallery

### Future Features (Not Urgent)
- SEO optimization (Schema.org markup)
- Blog section
- Advanced 3D previews
- Email newsletter signup

## 🎓 Learning Resources

- **Netlify**: https://docs.netlify.com
- **Calendly**: https://help.calendly.com
- **HTML/CSS Basics**: https://www.w3schools.com
- **This Project**: All docs in `docs/` folder

## ✅ Final Checklist

Before announcing your site:

- [ ] Deployed to Netlify
- [ ] Custom domain connected (optional)
- [ ] Calendly URL updated
- [ ] Real photos/videos in gallery
- [ ] Contact form tested (received email)
- [ ] Booking flow tested
- [ ] Checked on mobile phone
- [ ] Privacy policy reviewed
- [ ] All links work
- [ ] Feature flags set correctly

## 🎊 You're Ready to Launch!

Your professional drone services website is complete and ready to attract clients. Just follow the 30-minute launch checklist above.

**Questions?** Check `docs/GETTING_STARTED.md` or review the specific guides for each feature.

Good luck! 🚁

---

**Last updated:** 2026-09-02
**Status:** Production Ready ✅
