#!/bin/sh
# Run inside the playwright container: installs deps, serves sample-site, scans it.
npm install --no-audit --no-fund --silent || exit 1
node serve.cjs &
sleep 1
node scan.mjs http://localhost:8080 /,/menu.html sample-bakery
