---
description: 同步豆瓣看过的电影数据
---

# 同步豆瓣电影数据

此workflow用于从豆瓣抓取和同步您看过的电影数据。

## 使用步骤

1. 确保豆瓣Cookie已配置在 `~/.douban.cookie` 文件中
   - 如果没有，请从浏览器登录豆瓣后复制Cookie字符串到该文件

2. 运行同步脚本（全量抓取所有电影）
// turbo
3. 执行命令：`python3 scripts/sync-douban-movies/sync_douban_movies.py`

4. 检查生成的数据文件
   - 数据文件：`_data/movies/all.json`
   - 电影海报：`images/movies/`

5. 本地预览网站
   - 执行命令：`open http://localhost:4000/movies/all.html`
   - （确保 Jekyll 服务已启动）

6. 如果满意结果，提交并推送到 GitHub
   - 脚本会自动执行 git add、commit 和 push
   - 或手动执行：`git add . && git commit -m "sync movies" && git push`

## 参数说明

- `--max-pages N`：限制最多抓取N页（可选，默认100页）
- `--cookie "cookie字符串"`：直接指定Cookie（可选，会覆盖文件中的Cookie）

## 示例

```bash
# 全量抓取所有电影
python3 scripts/sync-douban-movies/sync_douban_movies.py

# 只抓取前10页（150部电影）
python3 scripts/sync-douban-movies/sync_douban_movies.py --max-pages 10

# 使用自定义Cookie
python3 scripts/sync-douban-movies/sync_douban_movies.py --cookie "your_cookie_here"
```
