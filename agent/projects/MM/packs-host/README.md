# Pack-host staging

`map.txt` is the expected release manifest; it is not proof that ZIPs are currently staged. Before deployment, stage the exact release ZIPs in this directory's `site/` folder and run:

```sh
python reconcile_map.py
```

The check fails on missing, extra, duplicate, unsafe, or incorrectly named archives. To rebuild the manifest from a non-empty staged archive directory after reviewing the filenames, run `python reconcile_map.py --archive-dir site --refresh`. It refuses to replace the manifest when no ZIPs are staged. Do not deploy until the check succeeds.
