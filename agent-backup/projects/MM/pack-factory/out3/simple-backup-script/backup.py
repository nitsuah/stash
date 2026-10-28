"""python backup.py --src ~/Documents --src ~/Projects --dest /mnt/backup --keep 7
Creates a timestamped .tar.gz of each source, verifies it can be read, and deletes the oldest beyond --keep. Stdlib only."""
import os, sys, tarfile, time
from pathlib import Path

def opts(name):
    return [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == name and i + 1 < len(sys.argv)]

srcs, dest, keep = [Path(os.path.expanduser(s)) for s in opts("--src")], Path(os.path.expanduser((opts("--dest") or ["."])[0])), int((opts("--keep") or ["7"])[0])
if not srcs:
    sys.exit("usage: backup.py --src DIR [--src DIR ...] --dest DIR [--keep N]")
dest.mkdir(parents=True, exist_ok=True)
stamp = time.strftime("%Y%m%d-%H%M%S")
for s in srcs:
    name = s.name or "root"
    out = dest / f"{name}-{stamp}.tar.gz"
    with tarfile.open(out, "w:gz") as t:
        t.add(s, arcname=name)
    with tarfile.open(out) as t:
        n = len(t.getmembers())
    print(f"wrote {out} ({out.stat().st_size} bytes, {n} entries, verified)")
    olds = sorted(dest.glob(f"{name}-*.tar.gz"))
    for o in olds[:-keep]:
        o.unlink()
        print("removed old", o.name)
