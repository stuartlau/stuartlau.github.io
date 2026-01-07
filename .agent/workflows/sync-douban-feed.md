---
description: Sync Douban broadcast feed for a specific year
---

1. Execute the sync script with the provided year and cookie.
   - You MUST ask the user for the `cookie` if it is not provided in the input context.
   - You MUST ask for the `year` if it is not clear.
   - Run the following command (replace `<YEAR>` and `<COOKIE>` with actual values):
   
```bash
python3 scripts/sync-douban-feed/sync_douban.py --year <YEAR> --cookie "<COOKIE>"
```

2. Verify the output file `_data/douban/<YEAR>.json` was created or updated.
3. (Optional) Run `jekyll build` or just let the incremental server pick it up to see changes.
