# Image Optimization Guide - WebP Format

## Why WebP?

WebP images are 25-35% smaller than JPEG/PNG while maintaining the same quality. This means:

- ✅ Faster page loads
- ✅ Better SEO rankings
- ✅ Lower bandwidth costs
- ✅ Improved user experience

## Quick Start

### Option 1: Online Converter (Easiest)
1. Go to https://cloudconvert.com/jpg-to-webp
2. Upload your JPG/PNG images
3. Download the WebP versions
4. Save them in `assets/gallery/` with `.webp` extension

### Option 2: Command Line (Batch Processing)

**Install cwebp:**
- **Windows**: Download from https://developers.google.com/speed/webp/download
- **Mac**: `brew install webp`
- **Linux**: `sudo apt install webp`

**Convert single image:**
```bash
cwebp -q 85 input.jpg -o output.webp
```

**Convert all images in folder:**
```bash
# Windows PowerShell
Get-ChildItem -Path assets/gallery -Filter *.jpg | ForEach-Object { cwebp -q 85 $_.FullName -o ($_.FullName -replace '.jpg','.webp') }

# Mac/Linux
for file in assets/gallery/*.jpg; do cwebp -q 85 "$file" -o "${file%.jpg}.webp"; done
```

### Option 3: Using Node.js Script

Create `scripts/convert-to-webp.js`:

```javascript
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const inputDir = 'assets/gallery';
const files = fs.readdirSync(inputDir);

files.forEach(file => {
    if (file.match(/\.(jpg|jpeg|png)$/i)) {
        const inputPath = path.join(inputDir, file);
        const outputPath = inputPath.replace(/\.(jpg|jpeg|png)$/i, '.webp');
        
        sharp(inputPath)
            .webp({ quality: 85 })
            .toFile(outputPath)
            .then(() => console.log(`✅ Converted: ${file} → ${path.basename(outputPath)}`))
            .catch(err => console.error(`❌ Error: ${file}`, err));
    }
});
```

**Run it:**
```bash
npm install sharp
node scripts/convert-to-webp.js
```

---

## Implementation

### Gallery System (Automatic Fallback)

The site now supports WebP with automatic fallbacks! Just add both formats:

**File structure:**
```
assets/gallery/
  ├── sunset-marina.jpg      ← Fallback
  ├── sunset-marina.webp     ← Preferred
  ├── aerial-waterfront.jpg  ← Fallback
  └── aerial-waterfront.webp ← Preferred
```

**Gallery JSON:**
```json
{
    "items": [
        {
            "src": "assets/gallery/sunset-marina",
            "alt": "Sunset marina view",
            "category": "landscape"
        }
    ]
}
```

Notice: No file extension! The system automatically tries `.webp` first, falls back to `.jpg`.

---

## Optimized Settings

### For Photos (Aerial Shots)
- **Quality**: 85 (sweet spot)
- **Method**: 6 (best compression)
```bash
cwebp -q 85 -m 6 input.jpg -o output.webp
```

### For Graphics/Text
- **Quality**: 95 (higher for clarity)
```bash
cwebp -q 95 input.png -o output.webp
```

### For Thumbnails
- **Quality**: 75 (smaller size OK)
- **Resize**: 400px width
```bash
cwebp -q 75 -resize 400 0 input.jpg -o thumb.webp
```

---

## Browser Support

WebP is supported by:
- ✅ Chrome (all versions)
- ✅ Firefox 65+
- ✅ Safari 14+ (2020+)
- ✅ Edge (all versions)
- ⚠️ IE11: No support (uses fallback)

**Coverage: ~95% of users** (with fallback for the rest)

---

## Performance Gains

**Example savings:**
- `sunset-marina.jpg`: 2.4 MB → `sunset-marina.webp`: 1.6 MB (33% smaller!)
- `aerial-waterfront.jpg`: 3.1 MB → `aerial-waterfront.webp`: 2.0 MB (35% smaller!)

**For 10 gallery images:**
- Before: ~25 MB total
- After: ~16 MB total
- **Savings: 9 MB (36% reduction!)**

---

## Conversion Checklist

- [ ] Convert all gallery images to WebP
- [ ] Keep original JPG/PNG as fallbacks
- [ ] Update `gallery.json` (remove file extensions)
- [ ] Test on different browsers
- [ ] Verify images load correctly
- [ ] Check mobile performance
- [ ] Monitor Lighthouse scores

---

## Current Status

**Images to convert:**
1. `sunset-marina.jpg` → `sunset-marina.webp`
2. `aerial-waterfront.jpg` → `aerial-waterfront.webp`
3. `image1.jpg` → `image1.webp`
4. `image2.jpg` → `image2.webp`
5. `image3.jpg` → `image3.webp`
6. `image4.jpg` → `image4.webp`
7. `image5.jpg` → `image5.webp`
8. `image6.jpg` → `image6.webp`
9. `hero-bg.jpg` → `hero-bg.webp` (if exists)

---

## Advanced: Responsive Images

For even better performance, create multiple sizes:

```html
<picture>
  <source 
    srcset="assets/gallery/sunset-marina-800.webp 800w,
            assets/gallery/sunset-marina-1200.webp 1200w,
            assets/gallery/sunset-marina-1600.webp 1600w"
    type="image/webp"
    sizes="(max-width: 768px) 100vw, 50vw">
  <source 
    srcset="assets/gallery/sunset-marina-800.jpg 800w,
            assets/gallery/sunset-marina-1200.jpg 1200w,
            assets/gallery/sunset-marina-1600.jpg 1600w"
    sizes="(max-width: 768px) 100vw, 50vw">
  <img src="assets/gallery/sunset-marina.jpg" alt="Sunset marina">
</picture>
```

---

## Monitoring

### Lighthouse Score (Before/After)
Run in Chrome DevTools:
1. Open DevTools (F12)
2. Go to "Lighthouse" tab
3. Click "Generate report"

**Target scores:**
- Performance: 90+ (currently ~70-80)
- Best Practices: 95+
- SEO: 95+

### Page Speed Insights
- Test at: https://pagespeed.web.dev/
- Enter your site URL after deployment

---

## Resources

- **WebP Guide**: https://developers.google.com/speed/webp
- **Image Optimization**: https://web.dev/fast/#optimize-your-images
- **Online Tools**: https://squoosh.app/ (Google's image optimizer)
- **Bulk Converter**: https://cloudconvert.com/

---

## Need Help?

Run into issues? Common fixes:
- **Images not loading?** Check file paths and extensions
- **Quality too low?** Increase quality setting (85-95)
- **Files too large?** Decrease quality or resize
- **Safari issues?** Ensure fallback JPG exists
