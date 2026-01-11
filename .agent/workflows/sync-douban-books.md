---
description: 同步豆瓣读书数据和封面图片
---

# 同步豆瓣读书数据

同步豆瓣"已读"、"在读"、"想读"书籍到网站 Books 页面。

## 前置条件

```bash
pip3 install requests beautifulsoup4
echo "your_douban_cookie" > ~/.douban.cookie
```

## 步骤

### 1. 同步书籍数据

// turbo
```bash
python3 scripts/sync-douban-books/sync_douban_books.py
```

这会：
- 抓取三个列表：collect（已读）、do（在读）、wish（想读）
- 每本书添加 `status` 字段标识来源
- 按 `publish_date` 降序排列
- 保存到 `_data/books/all.json`

### 2. 下载书籍封面

// turbo
```bash
python3 scripts/sync-douban-books/download_book_covers.py
```

这会：
- 并发访问每本书的豆瓣页面
- 提取封面 URL 并下载到 `images/books/`
- 跳过已存在的图片

### 3. 更新 JSON 添加封面路径

// turbo
```bash
python3 -c "
import json, os
with open('_data/books/all.json', 'r') as f:
    books = json.load(f)
for book in books:
    bid = book.get('book_id')
    if os.path.exists(f'images/books/{bid}.jpg'):
        book['cover'] = f'/images/books/{bid}.jpg'
with open('_data/books/all.json', 'w') as f:
    json.dump(books, f, indent=2, ensure_ascii=False)
print('Done!')
"
```

### 4. 验证结果

```bash
# 检查封面数量
ls images/books/*.jpg | wc -l

# 预览页面
open http://localhost:4000/books/index.html
```

## 文件位置

- 同步脚本：`scripts/sync-douban-books/sync_douban_books.py`
- 封面下载：`scripts/sync-douban-books/download_book_covers.py`
- 数据文件：`_data/books/all.json`
- 封面目录：`images/books/`
- 页面入口：`books/index.md`

## 数据结构

```json
{
  "book_id": "12345",
  "title": "书名",
  "author": "作者",
  "cover": "/images/books/12345.jpg",
  "status": "collect",  // collect=已读, do=在读, wish=想读
  "publish_date": "2024-1-1",
  "douban_rating": "8.5"
}
```
