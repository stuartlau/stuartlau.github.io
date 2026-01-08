---
description: Sync Douban broadcast feed for a specific year
---

1. Run the sync command. The script will automatically read the cookie from `~/.douban.cookie` and default to the current year. It will also automatically commit and push changes to git if any.
   
```bash
python3 scripts/sync-douban-feed/sync_douban.py
```

- Optional: Specify a year or override cookie
```bash
python3 scripts/sync-douban-feed/sync_douban.py --year 2025 --cookie "..."
```

2. Verify the output in git log or GitHub repo.
