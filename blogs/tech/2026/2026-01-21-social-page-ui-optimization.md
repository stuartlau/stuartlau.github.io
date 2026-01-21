---
layout: post
title: "社交页面UI优化与性能提升实录"
date: 2026-01-21
categories: Tech
tags: [Frontend, Performance, CSS, JavaScript, UI]
description: "记录一次针对个人网站社交页面的全面UI优化和性能提升过程，包括移动端适配、动态背景图、Lightbox优化、FOUC防治等多项改进。"
---

今晚对个人网站的Social页面进行了一系列UI优化和性能提升，涉及移动端体验、视觉效果、加载性能等多个方面。本文记录这些优化的技术细节和踩坑经验。

## 1. 移动端书影音展示优化

### 问题描述
移动端的书籍、电影、游戏卡片采用了全宽大图展示，只显示封面图片，没有标题、作者、评分等信息，用户体验差。

### 解决方案
将移动端的 `.quote-card` 布局从纵向改为横向，保持与PC端一致的信息密度：

```css
@media (max-width: 480px) {
    .quote-card {
        flex-direction: row;
        padding: 10px;
    }

    .quote-media {
        width: 70px;
        height: 100px;
        min-width: 70px;
        border-radius: 6px;
    }
    
    .quote-info {
        padding: 0 0 0 10px;
        flex: 1;
        min-width: 0;
    }
    
    .quote-title {
        font-size: 14px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
}
```

**效果**：移动端现在显示70x100px的小封面 + 完整的标题、作者、评分信息。

## 2. 动态背景图

### 需求
希望每次访问页面时，头部背景图能动态随机展示高质量图片，而不是固定的本地图片。

### 方案演进

**方案一：Unsplash Source API（失败）**
```javascript
coverImgEl.src = 'https://source.unsplash.com/1200x400/?nature';
```
问题：Unsplash于2025年后逐渐关闭了免费的Source API，返回503错误。

**方案二：Lorem Picsum（成功）**
```javascript
const randomSeed = Math.floor(Math.random() * 1000);
coverImgEl.src = 'https://picsum.photos/seed/' + randomSeed + '/1200/400';
```
Picsum是更稳定的替代方案，通过seed参数实现每次刷新显示不同图片。

### 兜底处理
```javascript
coverImgEl.onerror = function() {
    this.style.display = 'none';
    // 父容器的CSS渐变背景作为fallback
};
```

## 3. 移动端Lightbox性能问题

### 问题描述
用户在移动端点击图片放大后，页面卡死，滑动时下方一片白色，无法响应其他操作。

### 根因分析
1. 大图加载阻塞主线程
2. `body.style.overflow = 'hidden'` 在iOS上导致滚动穿透
3. 图片加载时没有loading状态反馈

### 临时解决方案
考虑到移动端性能限制，直接禁用移动端的Lightbox功能：

```javascript
function openLightbox(src, imagesArr) {
    const isMobile = window.innerWidth <= 768 || 
        /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    if (isMobile) {
        return; // 移动端不触发放大
    }
    // ... PC端正常处理
}
```

### 其他优化（供未来参考）
- 添加loading旋转动画
- 使用`position: fixed`防止iOS滚动穿透
- 图片加载完成后淡入显示
- 5秒超时保护

## 4. /blogs页面词云优化

### 问题描述
词云标签都是同一种绿色，视觉单调，标签尺寸过大，不够紧凑。

### 解决方案
参考travel页面的设计，使用彩色调色板：

```javascript
const colors = [
    '#2563eb', '#dc2626', '#16a34a', '#ca8a04', '#9333ea',
    '#ea580c', '#0891b2', '#be185d', '#059669', '#7c3aed',
    // ...
];

tags.forEach(({ tag, count }, index) => {
    const a = document.createElement('a');
    a.style.backgroundColor = colors[index % colors.length];
    a.style.color = '#fff';
    // ...
});
```

CSS调整为更紧凑的样式：
```css
.tag {
    padding: 4px 10px;
    border-radius: 16px;
    font-size: 13px;
    font-weight: 500;
}
```

## 5. 页面加载性能优化（FOUC防治）

### 问题描述
每次打开Social页面都有一段时间的排版错乱，元素闪烁后才恢复正常。

### 根因分析
这是典型的FOUC（Flash of Unstyled Content）问题：
1. 关键CSS写在页面底部的`<style>`标签里
2. 隐藏元素的JS在`DOMContentLoaded`后才执行
3. 图片没有预设尺寸，加载时导致布局跳动

### 解决方案

**1. 关键CSS前置**
将最关键的布局CSS放在页面最开头：

```html
<!-- Critical CSS - Inject immediately to prevent FOUC -->
<style>
.social-page .navigation-wrapper,
.social-page .article-author-top,
.social-page .headline-wrap { display: none !important; }
.social-page #main { margin-top: 0 !important; max-width: none !important; }
</style>
```

**2. 立即注入class**
在`DOMContentLoaded`之前就添加标识class：

```html
<script>
document.documentElement.classList.add('social-page');
document.body && document.body.classList.add('social-page');
</script>
```

**3. 图片骨架屏**
```css
.lazy-img:not(.loaded) { 
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%); 
    background-size: 200% 100%; 
    animation: shimmer 1.5s infinite; 
}
@keyframes shimmer { 
    0% { background-position: 200% 0; } 
    100% { background-position: -200% 0; } 
}
```

**4. 预定义尺寸防止CLS**
```css
.profile-avatar img { width: 100px; height: 100px; }
.post-avatar img { width: 40px; height: 40px; }
.profile-cover { height: 200px; }
```

## 6. 其他优化

### 6.1 移动端回到顶部按钮
在左下角添加悬浮按钮，滚动超过300px时显示：

```css
.back-to-top {
    position: fixed;
    bottom: 24px;
    left: 24px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* 只在移动端显示 */
}

@media (max-width: 768px) {
    .back-to-top { display: flex; }
}
```

### 6.2 Patents Tab UI统一
将专利列表的UI改为与Blogs Tab一致，包含@作者名和日期。

### 6.3 Album竖图显示修复
城市相册页面的竖图封面被裁切，文字遮挡图片底部：

```css
.album-image {
    height: 200px; /* 固定高度替代aspect-ratio */
    display: flex;
    align-items: center;
    justify-content: center;
}

.album-image img {
    object-fit: contain; /* 完整显示，不裁切 */
}
```

### 6.4 Blog文章头像统一
将`_layouts/post.html`中的作者头像从`site.owner.avatar`改为固定的`douban_avatar.jpg`。

## 总结

| 优化项 | 优化前问题 | 解决方案 |
|--------|-----------|----------|
| 移动端书影音 | 只显示大图，无信息 | 横向布局，完整信息 |
| 背景图 | 本地静态图 | Picsum动态随机图 |
| 移动端Lightbox | 页面卡死 | 暂时禁用 |
| /blogs词云 | 单调绿色 | 彩色标签，紧凑样式 |
| 页面加载 | FOUC闪烁 | 关键CSS前置+骨架屏 |
| 回到顶部 | 无 | 移动端悬浮按钮 |

本次优化主要聚焦于用户体验和视觉效果，后续还可以考虑：
- Service Worker缓存策略
- 图片WebP格式转换
- CSS/JS代码分割和压缩
- 首屏关键路径渲染优化
