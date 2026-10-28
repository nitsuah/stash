# Uptime Webhook Monitor
Checks your URLs and posts to a Discord or Slack webhook when one is down or returns an error.
1. Edit `targets.json`: your URLs and webhook URL.
2. Test: `node monitor.mjs --dry`
3. Schedule it (cron, Task Scheduler, or a CI schedule) every 5 to 15 minutes.
No dependencies; Node 18 or newer. It alerts on every run while a site is down, so pick a sensible schedule.

Personal and commercial use. Do not resell or redistribute the files themselves.
