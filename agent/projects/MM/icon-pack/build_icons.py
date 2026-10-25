"""Generates a 40-icon line-style SVG pack from primitives. Zero LLM. Output: dist/ + minimal-line-icons.zip"""
import pathlib
import shutil
import zipfile

# each icon: svg body in a 24x24 box, stroke-based
ICONS = {
    "home": '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="M16 16l5 5"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><circle cx="17" cy="9" r="2.5"/><path d="M2 20c0-3.5 3-5.5 7-5.5s7 2 7 5.5"/><path d="M16 14.5c3 0 6 1.5 6 4.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "phone": '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
    "bell": '<path d="M6 17V11a6 6 0 0112 0v6l2 2H4z"/><path d="M10 21h4"/>',
    "heart": '<path d="M12 20S3 14 3 8.5A4.5 4.5 0 0112 7a4.5 4.5 0 019 1.5C21 14 12 20 12 20z"/>',
    "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
    "check": '<path d="M4 12l5 5L20 6"/>',
    "close": '<path d="M5 5l14 14M19 5L5 19"/>',
    "plus": '<path d="M12 4v16M4 12h16"/>',
    "minus": '<path d="M4 12h16"/>',
    "arrow-right": '<path d="M4 12h16M14 6l6 6-6 6"/>',
    "arrow-left": '<path d="M20 12H4M10 6l-6 6 6 6"/>',
    "arrow-up": '<path d="M12 20V4M6 10l6-6 6 6"/>',
    "arrow-down": '<path d="M12 4v16M6 14l6 6 6-6"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "download": '<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',
    "upload": '<path d="M12 15V3M7 8l5-5 5 5M4 20h16"/>',
    "trash": '<path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"/>',
    "edit": '<path d="M4 20l1-5L16 4l4 4L9 19z"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>',
    "unlock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 017-2.6"/>',
    "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "link": '<path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M3 18l6-5 4 3 3-2 5 4"/>',
    "file": '<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5"/>',
    "folder": '<path d="M3 6h7l2 2h9v11H3z"/>',
    "chat": '<path d="M4 5h16v11H9l-5 4z"/>',
    "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="18" cy="20" r="1.5"/><path d="M2 3h3l3 12h11l2-8H6"/>',
    "tag": '<path d="M3 12V3h9l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    "map-pin": '<path d="M12 21s7-6 7-11a7 7 0 00-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
    "moon": '<path d="M20 14A8 8 0 019.5 3.5 8 8 0 1020 14z"/>',
    "bolt": '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
    "chart": '<path d="M4 20V4M4 20h16"/><path d="M8 16v-5M12 16V8M16 16v-8"/>',
}


def svg(body, stroke="currentColor", w=2):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'



def main():
    root = pathlib.Path(__file__).parent
    dist = root / "dist" / "minimal-line-icons"
    shutil.rmtree(root / "dist", ignore_errors=True)
    (dist / "svg").mkdir(parents=True)
    for n, b in ICONS.items():
        (dist / "svg" / f"{n}.svg").write_text(svg(b))

    cells = "".join(f'<div class="c">{svg(b, "#222")}<span>{n}</span></div>' for n, b in ICONS.items())
    (dist / "preview.html").write_text(
        f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Minimal Line Icons</title>"
        f"<style>body{{font-family:Arial;margin:24px}}.g{{display:grid;grid-template-columns:repeat(auto-fill,100px);gap:12px}}"
        f".c{{text-align:center;font-size:11px;color:#555}}.c svg{{width:48px;height:48px;display:block;margin:0 auto 4px}}</style></head>"
        f"<body><h1>Minimal Line Icons ({len(ICONS)})</h1><div class='g'>{cells}</div></body></html>"
    )
    (dist / "LICENSE.txt").write_text(
        "Minimal Line Icons. Use in personal and commercial projects, unlimited. "
        "Do not resell or redistribute the icon files themselves as a pack.\n"
    )
    (dist / "README.txt").write_text(
        f"{len(ICONS)} line icons, 24x24 grid, 2px stroke, currentColor (inherits your text color).\n"
        "svg/ folder: one file per icon. Open preview.html to browse.\n"
        "Tip: change stroke-width or stroke in the SVG to restyle.\n"
    )
    zp = root / "minimal-line-icons.zip"
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(dist.rglob("*")):
            if p.is_file():
                z.write(p, f"minimal-line-icons/{p.relative_to(dist).as_posix()}")

    print(len(ICONS), "icons", zp.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
