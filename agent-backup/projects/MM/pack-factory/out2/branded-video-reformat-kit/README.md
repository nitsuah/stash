# Branded Video Reformat Kit
Turn one finished video into vertical (1080x1920), square (1080x1080) and landscape (1920x1080) versions with a title bar and a brand footer.
Needs Docker only (ffmpeg runs in a container). Edit `brand.json` for colors and names; add variants to A/B test.

    sh run.sh my-video.mp4 my-brand A "Short title"

Outputs land in `out/`. The default footer shows your brand name and URL. Change the fonts or layout in `render.py`.

Personal and commercial use. Do not resell or redistribute the files themselves.
