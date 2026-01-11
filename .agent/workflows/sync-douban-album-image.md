---
description: 从豆瓣相册下载图片并为旅行博客添加header-img
---

# 从豆瓣相册同步图片并添加Header Image

这个workflow用于自动化处理旅行博客的header图片。

## 前置条件

```bash
pip3 install requests beautifulsoup4
echo "your_douban_cookie" > ~/.douban.cookie
```

## 快速开始

// turbo
```bash
# 1. 抓取相册列表并匹配城市
python3 scripts/sync-douban-album-image/auto_match_albums.py --fetch-albums

# 2. 下载封面图片
./download_matched.sh

# 3. 查看结果
ls -la images/in-post/
```

## 详细步骤

### 方法一：自动匹配相册（推荐）

使用 `auto_match_albums.py` 自动从豆瓣相册列表匹配城市。

#### 1. 抓取并缓存相册列表

// turbo
```bash
python3 scripts/sync-douban-album-image/auto_match_albums.py --fetch-albums --dry-run
```

这会：
- 从 `https://www.douban.com/people/shuoleo/photos` 爬取所有相册
- 解析相册标题（格式：`yyyy年yy月·在XXX`）
- 匹配到对应的 md 文件
- 结果缓存到 `douban_albums_cache.json`

#### 2. 下载封面图片

// turbo
```bash
python3 scripts/sync-douban-album-image/auto_match_albums.py
./download_matched.sh
```

#### 3. 更新 markdown 文件

手动更新 md 文件：
- 添加 `header-img: img/in-post/{City}-0.jpg` 到 front matter
- 添加相册卡片 HTML（参考下面的模板）

**相册卡片 HTML 模板**：
```html
<div class="album-grid">
  <a href="https://www.douban.com/photos/album/{album_id}/" class="album-card" target="_blank">
    <div class="album-image">
      <img src="{{ site.url }}/images/in-post/{City}-0.jpg" alt="{City}" class="no-zoom">
    </div>
    <div class="album-info">
      <span class="album-title">{City} Album</span>
      <span class="album-desc">2024-01</span>
    </div>
  </a>
</div>
```

### 方法二：扫描已有相册链接

如果 md 文件中已经有豆瓣相册链接：

// turbo
```bash
python3 scripts/sync-douban-album-image/generate_image_report.py
./download_missing.sh
python3 scripts/sync-douban-album-image/update_header_images.py
```

#### 可用选项：
```bash
# 校验现有图片的 URL 是否变化
python3 scripts/sync-douban-album-image/generate_image_report.py --verify

# 列出没有相册链接的文件
python3 scripts/sync-douban-album-image/generate_image_report.py --list-no-album
```

## 技术细节

### 豆瓣页面 HTML 选择器
- 相册容器：`div.albumlst`
- 相册封面链接：`a.album_photo`
- 相册标题：容器内另一个 `<a>` 标签
- 封面图片：`span.rec[data-image]` 属性

### 封面图片 URL
封面图片需要从相册页面获取，URL 格式：
```
https://img{n}.doubanio.com/view/photo/l/public/p{photo_id}.jpg
```
注意：`photo_id` 和 `album_id` 不同，必须访问相册页面获取。

### 城市名称映射
在 `auto_match_albums.py` 中的 `CITY_NAME_MAP` 字典：
```python
CITY_NAME_MAP = {
    '北京': 'Beijing',
    '上海': 'Shanghai',
    '成都': 'Chengdu',
    # ...
}
```
新增城市需要手动添加到此映射。

### 图片命名规则
格式：`{英文城市名}-{序号}.jpg`
- 例如：`Beijing-0.jpg`, `Chengdu-1.jpg`

## 文件位置

- 脚本目录：`scripts/sync-douban-album-image/`
  - `auto_match_albums.py` - 自动匹配相册
  - `generate_image_report.py` - 扫描已有链接
  - `update_header_images.py` - 更新 front matter
- 图片输出：`images/in-post/*-{n}.jpg`
- 缓存文件：`douban_albums_cache.json`
- 旅行博客：`blogs/travelling/` (递归扫描)

## 常见问题

### Q: 403 错误？
A: 需要配置 Cookie。从浏览器复制完整 Cookie 到 `~/.douban.cookie`。

### Q: 新城市没有匹配？
A: 在 `CITY_NAME_MAP` 中添加中英文映射。

### Q: 图片下载失败？
A: 手动用 curl 下载：
```bash
curl -L -H 'Referer: https://www.douban.com/' \
     -H 'User-Agent: Mozilla/5.0' \
     '{image_url}' -o 'images/in-post/{City}-0.jpg'
```
