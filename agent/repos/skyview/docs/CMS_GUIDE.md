# CMS Editing Guide

**Last Updated:** 2026-08-22

SkyView uses [Decap CMS](https://decapcms.org/) (formerly Netlify CMS) with a Git Gateway backend. Content changes made in the CMS editor result in commits to the `main` branch, which triggers an automatic Netlify deploy.

---

## Prerequisites

- The site must be deployed to Netlify.
- **Netlify Identity** must be enabled and you must have accepted an invitation.
- **Git Gateway** must be enabled under Netlify → Site settings → Identity → Services.

If you have not completed these steps, follow [GETTING_STARTED.md](GETTING_STARTED.md) (Step 3) first.

---

## Accessing the CMS

1. Navigate to `https://your-site.netlify.app/admin/` (or your custom domain + `/admin/`).
2. Click **Login with Netlify Identity**.
3. Sign in with the email address you were invited with.

---

## Managing the Gallery

The gallery is the primary content collection managed through the CMS.

### Viewing gallery items

Click **Gallery** in the left sidebar, then **Gallery Items**. You will see the full list of items from `assets/gallery.json`.

### Adding a new item

1. Click **Gallery → Gallery Items → Edit**.
2. Scroll to the bottom of the item list and click **Add item**.
3. Fill in the fields:

| Field | What to enter |
|-------|---------------|
| Image | Upload a JPG, PNG, or WebP file from your computer, or paste an external URL |
| Alt Text | A short description of the shot (used for accessibility and SEO) |
| Category | events / real_estate / landscape / commercial |
| Season | The season when the shot was taken, or "all" if evergreen |
| Display Order | 1–999; lower numbers appear first in the gallery |
| Active | Leave checked to show the item; uncheck to hide it without deleting |
| Featured | Check to flag the item for spotlight or hero use |

4. Click **Save** (top right). Do **not** publish yet — save first to review.
5. Click **Publish** to commit the change and trigger a deploy.

> **Tip:** Deploys take 30–60 seconds. You can queue multiple edits before publishing.

### Editing an existing item

Click the item in the list, edit any field, then click **Save** and **Publish**.

### Hiding an item without deleting it

Uncheck the **Active** toggle, then Save and Publish. The item stays in the JSON but is filtered out of the rendered gallery.

### Deleting an item

Click the item, scroll to the bottom of the form, and click **Delete**. This removes the entry from `assets/gallery.json` but does **not** delete the image file from the repository — remove the file from `assets/gallery/` manually if you no longer need it.

---

## Uploading Media

When you click the **Image** field and choose to upload a file, Decap CMS commits the file directly to `assets/gallery/` in the repository. Large files (>5 MB) will bloat the git history — for video files or high-resolution source files, consider hosting on an external CDN and entering the URL instead of uploading.

### Recommended workflow for images

1. Optimise images locally before uploading:
   ```bash
   npm run optimize:images
   ```
   This converts JPG/PNG files in `assets/gallery/` to WebP (30–40% smaller).
2. Upload the WebP file through the CMS, or commit it directly and add the entry to `assets/gallery.json`.

### Video files

Video is natively supported — no YouTube or Vimeo embed required. Add videos to `assets/gallery/` and set the **type** field to `video` in the gallery JSON (via direct edit of `assets/gallery.json`; the CMS list widget does not yet expose a type selector).

---

## What the CMS Can and Cannot Do

| Can do | Cannot do |
|--------|-----------|
| Add, edit, hide, reorder, and delete gallery items | Edit site copy (hero text, service descriptions) — edit `index.html` directly |
| Upload images to `assets/gallery/` | Manage the platform React app at `/app/` |
| Change gallery categories, seasons, and display order | Change feature flags — edit `config.js` directly |
| Trigger deploys by publishing | Manage Netlify Forms submissions |

---

## Troubleshooting

**"Not authorized" or blank login screen**
- Make sure Netlify Identity is enabled for the site.
- Check that Git Gateway is enabled under Identity → Services.
- Try an incognito window to rule out a cached session.

**Changes not appearing after Publish**
- Check the Deploys tab in the Netlify dashboard for build errors.
- A publish always commits to `main` — verify the commit appears in the GitHub repo.

**Image not loading after upload**
- The file path in `gallery.json` must exactly match the filename (case-sensitive on Linux/Netlify).
- Run `npm run optimize:images` locally if you uploaded a JPG/PNG and need a WebP version.

---

## Further Reading

- [Decap CMS Documentation](https://decapcms.org/docs/intro/)
- [Asset Management Guide](ASSET_MANAGEMENT.md) — full gallery JSON field reference
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) — Netlify deployment reference (includes Identity + Git Gateway setup)
