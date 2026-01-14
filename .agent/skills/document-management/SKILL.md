---
description: 自动管理资产目录中的文件（如 PDF），将其转换为带有嵌入查看器的博客文章。
name: Document Management
---

# Document Management Skill

当你发现 `assets/files` 目录下有新的静态文件，或者用户询问如何发布这些文件时，请使用此技能。

## 核心流程

1. **自动扫描**: 
   - 检查 `assets/files` 目录中的文件（如 PDF）。
2. **博客转换**:
   - 运行脚本 `python3 scripts/generate-doc-md/generate_doc.py`。
   - 脚本将：
     1. 验证 `blogs/tech/YYYY/` 下是否存在对应的 Markdown。
     2. 若不存在，生成一个新的 Markdown 文件，通过 iframe 或专用组件嵌入该文件。

## 注意事项
- 生成的文件应包含正确的 Frontmatter（如标题、日期、类别）。
- 确保文件的路径在 Markdown 中是正确的相对路径或 URL。
