---
description: 根据专利ID自动创建专利介绍的Markdown文件
---

这个workflow用于根据一个或多个专利ID自动化生成旅行博客或专利介绍页面：
1. 从Google Patents抓取专利详情（标题、摘要、事件、PDF链接）
2. 自动判断授权/待授权状态
3. 生成正确命名的Markdown文件
4. 自动处理版本更新（如从A版升级到B版时删除旧文件）

## 前置条件

确保已安装Python依赖：
```bash
pip3 install requests beautifulsoup4
```

## 步骤

### 1. 自动同步 (推荐方式)

该方式会自动从 Google Patents 下载最新的 CSV 文件，并与本地 `blogs/patent/` 目录进行比对。如果发现新专利或已授权的专利，会自动抓取信息并生成/替换 Markdown 文件。

// turbo
```bash
python3 scripts/sync_patents.py
```

该脚本的工作流程：
1. **自动下载**: 访问 Google Patents 抓取最新的专利列表 CSV。
2. **差量比对**: 识别本地尚未创建的专利，或已从“申请”变为“授权”的专利。
3. **批量抓取**: 自动调用 `patent_generator.py` 获取详情。

### 2. 手动处理特定 ID

如果你只需要处理某个特定的专利，可以带参数运行：

// turbo
```bash
python3 scripts/sync_patents.py <PATENT_ID1> <PATENT_ID2> ...
```

**示例**：
```bash
python3 scripts/sync_patents.py CN111399709B
```

### 3. 检查生成的文件

文件将按照格式 `yyyy-mm-dd-{授权/待授权专利}-{ID}.md` 生成。

```bash
ls -lt blogs/patent/ | head -n 5
```

### 4. 上传相关图片 (可选)

如果该专利有证书图片，将其放置在 `images/in-post/patent/` 目录下，并命名为 `<ID>.jpg`。

### 5. 提交更改

```bash
git add blogs/patent/*.md
git commit -m "Sync patents from Google Patents"
git push origin
```

## 脚本说明

- **`scripts/patent_generator.py`**: 核心抓取和生成逻辑。
- **`scripts/sync_patents.py`**: 基于 CSV 的批量同步封装。

## 常见问题

### Q: 抓取失败或日期不对怎么办？
A: 有时 Google Patents 的页面结构会有所不同。如果脚本无法提取日期，会报错。在这种情况下，你可以手动修改生成的 Markdown 文件。

### Q: 如何添加更多自动标签？
A: 编辑 `patent_generator.py` 中的 `keywords` 列表，加入你常用的关键词。
