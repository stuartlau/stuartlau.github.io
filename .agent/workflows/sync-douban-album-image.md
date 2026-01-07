---
description: 从豆瓣相册下载图片并为旅行博客添加header-img
---

# 从豆瓣相册同步图片并添加Header Image

这个workflow用于自动化处理旅行博客的header图片：
1. 从豆瓣相册提取图片URL
2. 下载图片到本地
3. 自动更新markdown文件的front matter

## 前置条件

确保已安装Python依赖：
```bash
pip3 install requests beautifulsoup4
```

## 步骤

### 1. 生成图片下载报告和脚本

运行脚本来扫描所有需要header-img的旅行博客文件：

```bash
python3 scripts/sync-douban-album-image/generate_image_report.py
```

这个脚本会：
- 扫描 `blogs/travelling/` 目录中的所有markdown文件
- 检查哪些文件缺少 `header-img`
- 从文件内容中提取豆瓣相册URL
- 访问豆瓣相册页面获取第一张图片的URL
- 生成两个文件：
  - `douban_images_report.txt` - 详细报告，包含所有图片URL和需要添加的front matter
  - `download_images.sh` - 可执行的下载脚本

### 2. 下载图片

运行生成的shell脚本来下载所有图片：

```bash
./download_images.sh
```

这个脚本会：
- 使用curl命令下载图片（带有Referer header绕过豆瓣的反爬虫保护）
- 将图片保存到 `images/in-post/` 目录
- 使用格式 `{城市名}-0.jpg` 命名文件

**注意**：如果某些图片下载失败（豆瓣可能会限制），可以：
- 手动在浏览器中打开图片URL并保存
- 或者稍后重试下载脚本

### 3. 更新markdown文件

下载完图片后，运行脚本自动更新所有markdown文件：

```bash
python3 scripts/sync-douban-album-image/update_header_images.py
```

这个脚本会：
- 扫描所有旅行博客markdown文件
- 检查对应的图片文件是否存在于 `images/in-post/` 目录
- 在YAML front matter中添加 `header-img: img/in-post/{城市名}-0.jpg`
- 插入位置在 `author:` 行之后

### 4. 验证结果

检查更新后的文件：

```bash
# 查看某个更新后的文件
cat blogs/travelling/2019-05-02-Suzhou.md

# 查看下载的图片
ls -lh images/in-post/ | grep "-0.jpg"
```

### 5. 提交更改

如果一切正常，提交更改到Git：

```bash
git add blogs/travelling/*.md
git add images/in-post/*-0.jpg
git commit -m "Add header images for travel blog posts from Douban albums"
git push
```

## 脚本说明

### generate_image_report.py

主要功能：
- 提取豆瓣相册URL
- 解析相册页面获取图片URL
- 生成下载脚本和报告

关键逻辑：
- 优先选择相册封面图片
- 如果没有封面，选择第一张照片
- 将图片URL从中等尺寸(/m/)转换为大尺寸(/l/)

### download_images.sh

自动生成的shell脚本，包含所有curl下载命令。

关键参数：
- `-H 'Referer: https://www.douban.com/'` - 绕过豆瓣的Referer检查
- `-H 'User-Agent: Mozilla/5.0'` - 模拟浏览器请求
- `-o 'images/in-post/{filename}'` - 指定输出文件路径

### update_header_images.py

主要功能：
- 读取markdown文件的front matter
- 检查是否已有header-img
- 验证对应图片文件是否存在
- 在正确位置插入header-img行

## 常见问题

### Q: 豆瓣返回418错误怎么办？

A: 豆瓣有反爬虫保护，如果直接用Python下载会被阻止。解决方案：
1. 使用生成的shell脚本（带Referer header）
2. 或者手动在浏览器中下载图片

### Q: 某些文件没有豆瓣相册链接怎么办？

A: 这些文件会被跳过。你需要：
1. 手动添加豆瓣相册链接到文件内容
2. 或者手动下载图片并添加header-img

### Q: 如何为单个文件添加header-img？

A: 手动编辑markdown文件的front matter：

```yaml
---
layout:     post
permalink:  /blogs/2019-05-02-Suzhou/index.html
title:      "Suzhou"
date:       2019-05-02
author:     StuartLau
header-img: img/in-post/Suzhou-0.jpg  # 添加这一行
header-style: text
---
```

### Q: 图片命名规则是什么？

A: 格式为 `{城市名}-0.jpg`，其中城市名从文件名中提取。
例如：`2019-05-02-Suzhou.md` → `Suzhou-0.jpg`

## 文件位置

- 脚本文件：项目根目录
  - `scripts/sync-douban-album-image/generate_image_report.py`
  - `scripts/sync-douban-album-image/update_header_images.py`
  - `download_images.sh` (自动生成)
  
- 输入文件：`blogs/travelling/*.md`
- 输出图片：`images/in-post/*-0.jpg`
- 报告文件：`douban_images_report.txt` (自动生成)

## 示例

完整流程示例：

```bash
# 1. 生成报告和下载脚本
python3 scripts/sync-douban-album-image/generate_image_report.py

# 2. 下载图片
./download_images.sh

# 3. 更新markdown文件
python3 scripts/sync-douban-album-image/update_header_images.py

# 4. 查看结果
git status

# 5. 提交更改
git add blogs/travelling/*.md images/in-post/*-0.jpg
git commit -m "Add header images from Douban albums"
git push
```
