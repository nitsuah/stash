"""python build.py -> index.html (reads links.json). Upload anywhere."""
import json, html
d = json.load(open("links.json", encoding="utf-8"))
e = html.escape
links = "".join(f"<li><a href='{e(l['url'])}'>{e(l['label'])}</a></li>" for l in d["links"])
css = f"body{{margin:0;background:{d['bg']};color:{d['fg']};font:20px/1.5 system-ui,sans-serif;text-align:center}}main{{max-width:30rem;margin:auto;padding:2rem 1rem}}ul{{list-style:none;padding:0}}li{{margin:1rem 0}}a{{display:block;padding:1rem;border:2px solid {d['accent']};border-radius:10px;color:{d['fg']};text-decoration:none;font-weight:600}}a:hover,a:focus{{background:{d['accent']};color:{d['bg']}}}"
page = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{e(d['name'])}</title><meta name='description' content='{e(d['bio'])}'><style>{css}</style></head><body><main><h1>{e(d['name'])}</h1><p>{e(d['bio'])}</p><nav aria-label='Links'><ul>{links}</ul></nav></main></body></html>"
open("index.html", "w", encoding="utf-8").write(page)
print("wrote index.html")
