"""python make_jsonld.py business.json > snippet.html  : paste the output into your page <head>."""
import json, sys
b = json.load(open(sys.argv[1], encoding="utf-8"))
missing = [k for k in ("name", "url", "telephone") if not b.get(k)]
if missing:
    sys.exit("missing: " + ", ".join(missing))
a = b["address"]
data = {"@context": "https://schema.org", "@type": b.get("type", "LocalBusiness"), "name": b["name"], "url": b["url"], "telephone": b["telephone"],
        "address": {"@type": "PostalAddress", "streetAddress": a["street"], "addressLocality": a["city"], "addressRegion": a["state"], "postalCode": a["zip"], "addressCountry": a["country"]},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"], "opens": h["opens"], "closes": h["closes"]} for h in b["hours"]]}
for k in ("priceRange", "sameAs"):
    if b.get(k):
        data[k] = b[k]
print('<script type="application/ld+json">')
print(json.dumps(data, indent=2))
print("</script>")
