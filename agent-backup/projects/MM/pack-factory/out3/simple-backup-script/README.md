# Simple Backup Script
    python backup.py --src ~/Documents --src ~/Projects --dest /mnt/backup --keep 7
Makes a timestamped compressed archive of each folder, checks the archive can be read back, and keeps only the newest N per folder.
Schedule it with cron (Linux/macOS) or Task Scheduler (Windows). Keep a copy off-site, and test a restore now and then.
It does not encrypt; store archives somewhere you trust or encrypt the destination. Plain Python 3.

Personal and commercial use. Do not resell or redistribute the files themselves.
