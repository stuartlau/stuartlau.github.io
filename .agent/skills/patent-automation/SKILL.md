---
description: 自动化专利文档管理，包括从 Google Patents 抓取详情、生成 Markdown、同步授权状态、以及自动关联专利设计图片。
name: Patent Automation
---

# Patent Automation Skill

当你处理专利相关任务（如创建新专利介绍、同步专利状态、处理专利图片）时，请使用此技能。

## 核心功能

1. **自动同步与抓取**: 
   - 优先使用脚本 `scripts/patent-md-create/sync_patents.py`。
   - 逻辑：自动从 Google Patents 下载最新 CSV，识别新专利或状态变更（如“申请”变“授权”），自动生成/替换 Markdown 文件。
   - 文件命名规范：`yyyy-mm-dd-{授权/待授权专利}-{ID}.md`。

2. **图片关联与管理**:
   - 脚本：`scripts/insert_patent_design_images.py`。
   - 逻辑：扫描 `images/in-post/patent/design` 下的 PNG，根据 ID 自动插入到 `blogs/patent` 对应的 MD 文件顶部。
   - 证书图片：若存在证书图片，应放在 `images/in-post/patent/` 下，命名为 `<ID>.jpg`。

3. **版本控制**:
   - 当专利从申请阶段（待授权）转为授权阶段时，应自动删除旧的待授权 MD 文件，生成新的授权 MD。

## 使用场景

- 当用户要求“同步专利”或“我有新专利了”。
- 当用户上传或移动了专利相关的图片。
- 当你需要参考现有专利的格式进行编辑时。
