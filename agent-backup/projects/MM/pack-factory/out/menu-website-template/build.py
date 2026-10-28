"""Build an accessible one-page menu site: python build.py  (reads menu.json, writes index.html)"""
import json, html
d = json.load(open("menu.json", encoding="utf-8"))
e = html.escape
secs = "".join(
    f"<section aria-labelledby='s{i}'><h2 id='s{i}'>{e(s['title'])}</h2><ul>"
    + "".join(f"<li><span class='p'>${e(it['price'])}</span><span class='n'>{e(it['name'])}</span>" + (f"<br><span class='d'>{e(it['note'])}</span>" if it['note'] else "") + "</li>" for it in s["items"])
    + "</ul></section>" for i, s in enumerate(d["sections"]))
hours = "".join(f"<li>{e(h)}</li>" for h in d["hours"])
CSS = ":root{--bg:#fffdf8;--fg:#1d1b18;--accent:#7a2e0e}body{margin:0;background:var(--bg);color:var(--fg);font:18px/1.6 system-ui,sans-serif}header,main,footer{max-width:42rem;margin:auto;padding:1.5rem}a{color:var(--accent)}h1,h2{color:var(--accent)}ul{list-style:none;padding:0}li{margin:.6rem 0}.p{float:right;font-weight:600}.d{color:#4a4640;font-size:.9em}.skip{position:absolute;left:-999px}.skip:focus{left:1rem;top:1rem;background:#fff;padding:.5rem}"
page = (
    "<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
    f"<title>{e(d['name'])} menu</title><meta name='description' content='{e(d['name'])}: menu, hours and location.'><style>{CSS}</style></head><body>"
    "<a class='skip' href='#main'>Skip to menu</a>"
    f"<header><h1>{e(d['name'])}</h1><p>{e(d['tagline'])}</p></header>"
    f"<main id='main'>{secs}</main>"
    f"<footer><h2>Visit us</h2><p>{e(d['address'])}<br><a href='tel:{e(d['phone'])}'>{e(d['phone'])}</a></p><ul>{hours}</ul></footer></body></html>"
)
open("index.html", "w", encoding="utf-8").write(page)
print("wrote index.html")
