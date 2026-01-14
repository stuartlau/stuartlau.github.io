---
description: 同步社交媒体（如豆瓣）的广播、书籍、电影和相册数据到本地仓库。
name: Social Media Sync
---

# Social Media Sync Skill

当用户要求更新读书进度、同步电影清单或同步豆瓣广播时，请激活此技能并选择相应的辅助脚本。

## 核心工具集

1. **豆瓣广播 (Feed)**:
   - 脚本：`scripts/sync-douban-feed/sync_douban.py`
   - 参数：可选 `--year 2025`。

2. **读书 (Books)**:
   - 脚本：对应 `scripts/sync_douban_books.py`（通常由 workflow `sync-douban-books.md` 定义）。

3. **电影 (Movies)**:
   - 脚本：对应 `scripts/sync_douban_movies.py`。

4. **相册 (Album)**:
   - 脚本：`scripts/sync_douban_album_image.py`。

## 操作指南
- 运行这些脚本前，通常需要确保 `~/.douban.cookie` 文件存在且有效。
- 同步完成后，检查 `_data/douban/` 目录下的 JSON 文件更新情况。
- 如果涉及图片，确保图片路径已正确更新到 Markdown 或 JSON 中。
