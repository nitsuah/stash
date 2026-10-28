# Cover factory

Run `bash run.sh` from this directory. The runner builds the pack-factory and icon-pack visual inputs, installs the Playwright package required by the renderer, checks that referenced assets exist, then writes cover and thumbnail PNG/HTML files under `out/`.

The script intentionally fails before rendering if a referenced generated asset is missing. It does not publish or upload the images.
