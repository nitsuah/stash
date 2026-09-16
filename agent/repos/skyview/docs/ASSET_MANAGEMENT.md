# Asset Management & Admin Guide

Skyview uses a decentralized asset management system powered by **Decap CMS** (formerly Netlify CMS). This allows you to manage gallery images without touching code.

## Accessing the Admin Panel

Once deployed to Netlify:

1. Navigate to `yoursite.com/admin/`.
2. Login with your **Netlify Identity** credentials (you will need to invite yourself from the Netlify Dashboard > Identity tab).

## Managing Gallery Images

Inside the Admin Panel:

1. Click on **Gallery** in the left sidebar.
2. You will see a list of current images.
3. **Add New**: Click "Add Items" to upload a new photo.
    * **Image**: Upload directly from your computer. Note: Large files will be stored in the repository.
    * **Alt Text**: Describe the image for accessibility.
    * **Category**: Select the appropriate category for future filtering.
    * **Season**: Optionally tag the image with a season (spring, summer, fall, winter, all).
    * **Display Order**: Set the sort priority (1–999; lower numbers appear first).
    * **Active**: Uncheck to hide the item without deleting it.
    * **Featured**: Check to mark the item for spotlight use.
4. **Publish**: Click "Publish" to save changes. This will automatically trigger a site deployment.

## Using External Assets (Cloudinary/S3)

If you have large video files or want to host images externally:

### Option A: Manual JSON Edit

1. Open `assets/gallery.json` in the codebase.
2. Change the `src` field of an item to the full URL (e.g., `https://res.cloudinary.com/...`).

### Option B: Cloudinary Integration with Decap CMS

To enable direct Cloudinary uploads from the Admin panel:

1. Open `admin/config.yml`.
2. Add your Cloudinary configuration:

    ```yaml
    media_library:
      name: cloudinary
      config:
        cloud_name: your_cloud_name
        api_key: your_api_key
    ```

3. This prevents bloating the git repository with large media files.

## 4. Video Assets

Video is **natively supported**. The gallery renders `<video>` elements with playback controls for any entry that has `"type": "video"` in `assets/gallery.json`. No external hosting (YouTube/Vimeo) is required for MP4/MOV files.

Add a video entry to `assets/gallery.json`:

```json
{
  "src": "assets/gallery/your-clip.mp4",
  "alt": "Aerial flyover of the marina",
  "category": "landscape",
  "type": "video",
  "active": true
}
```

Place the file in `assets/gallery/` and push — the gallery loads it automatically.

## 5. Gallery JSON Fields

All fields supported in `assets/gallery.json` (editable via the Decap CMS admin panel or directly):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| src | string | yes | Path or URL to the image/video file |
| alt | string | yes | Alt text (accessibility and SEO) |
| category | string | yes | One of: events, real_estate, landscape, commercial |
| season | string | no | One of: all, spring, summer, fall, winter (default: all) |
| displayOrder | number | no | Sort priority 1–999; lower = appears first |
| active | boolean | no | false hides the item without deleting it (default: true) |
| featured | boolean | no | Marks entry for spotlight use (default: false) |
| type | string | no | Set to `"video"` for MP4/MOV files; omit or leave blank for images |
