# Website Tech Stack Detector (CMS, frameworks, CDN)

Give this Actor a list of websites and it tells you what each one runs on: the CMS, JavaScript frameworks and libraries, analytics and tag managers, web server, CDN and hosting, and e-commerce and payment tools. Use it to qualify leads, research competitors, or audit the sites you manage.

## How it works
Each URL is fetched once. The response headers, cookies, meta tags, script and link URLs and the HTML are matched against a fingerprint list kept in the `fingerprints` folder. Every detection comes with the evidence that triggered it (for example `header:server` or `script:/wp-includes/`). Technologies that follow from another (WordPress implies PHP) are added and marked `implied`.

## Output
One row per URL: url, finalUrl after redirects, status, `technologies` (name, category, website, evidence) and `technologyCount`. A URL that cannot be fetched returns a row with an error and is not charged. A site where nothing is recognized returns an empty list, not an error.

## Limits
Detection uses only what the server returns for one request. Technologies that appear only after JavaScript runs, or only on other pages, are not seen. Fingerprints are matched case-insensitively and a match shows presence, not a version number. The list covers common technologies and grows over time. Only analyze sites you are allowed to analyze.

Pricing is per analyzed site (pay per event).
