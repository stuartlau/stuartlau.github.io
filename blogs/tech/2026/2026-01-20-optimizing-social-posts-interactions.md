---
layout: post
title: "优化 Social Posts 页面的交互与性能：懒加载、CDN 与 Giscus 集成"
date: 2026-01-20
categories: Tech
tags: [Jekyll, Image Optimization, Lazy Loading, Giscus, CDN, Frontend]
description: "记录一次对 Jekyll 博客 Social 页面（Posts 流）的深度优化过程，包括实现基于 IntersectionObserver 的智能图片懒加载、CDN 自动替换、移动端体验优化，以及如何为动态内容集成 Giscus 评论系统并实现点赞和评论数的预加载。"
header-img: "https://user-gold-cdn.xitu.io/2019/3/22/169a4d626f362741?imageView2/0/w/1280/h/960/format/webp/ignore-error/1"
---

最近，我对博客的 [Social 页面](/social.html)（主要用于同步展示我的豆瓣广播、书影音记录）进行了一系列的优化。这个页面的特点是内容流很长，包含大量图片，且不仅仅是静态的文章展示，更像是一个社交媒体的时间线。

这次优化的主要目标是：提升加载性能（图片懒加载、CDN），增强互动性（点赞、评论），以及优化移动端体验。以下是这次折腾的技术总结。

## 1. 智能图片懒加载的"坑"与解

### 问题初现

最初，Posts 页面使用了浏览器原生的 `loading="lazy"` 属性。但在实际测试中发现，对于长列表和大量图片，这种方式并不总是可靠，且无法精确控制加载时机。于是我决定引入 `IntersectionObserver` 来手动控制。

然而，第一版实现上线后，发现了一个严重问题：**图片一直处于 loading 状态，无法加载。**

### 排查过程

通过浏览器调试，我发现虽然 IntersectionObserver 已经初始化，但回调函数始终没有触发 `isIntersecting: true`。

经过一番排查（甚至用上了浏览器自动化做了一次深度体检），终于找到了原因：

Posts 页面的图片被包裹在 `.social-image-grid` 容器中，而这个容器设置了 `overflow: auto`。当 IntersectionObserver 的 `root` 默认为 `null`（即视口）时，如果观察的目标元素位于一个有滚动条的父容器内，且该父容器本身没有被滚动，那么观察者可能无法正确计算交叉区域，导致检测失效。

此外，由于图片在加载前没有设置 `src`，其尺寸可能坍缩为 0 或极小（如 20px），这在复杂的布局嵌套中容易导致可见性检测异常。

### 解决方案

1.  **观察包装器而非图片**：不直接观察 `img` 标签，而是观察其父容器 `.grid-img-wrap`。这个容器有固定的 CSS 尺寸（如 120x120px），这保证了无论图片加载状态如何，观察目标始终占据稳定的空间。
2.  **调整 Overflow**：移除了不必要的局部滚动限制，让页面滚动更加自然。

```javascript
// 优化后的观察逻辑
document.querySelectorAll('.grid-img-wrap').forEach(wrap => {
    const img = wrap.querySelector('.lazy-img[data-src]');
    if (!img) return;
    
    // 只在当前激活的 Tab 中观察
    const panel = wrap.closest('.content-panel');
    if (panel && !panel.classList.contains('active')) return;
    
    // 省略部分代码...
    
    // 将图片引用挂在 wrapper 上方便回调时调用
    wrap._lazyImg = img;
    imageLazyObserver.observe(wrap);
});
```

同时，我们还处理了 Tab 切换和 Infinite Scroll 加载更多时的逻辑，确保新出现的内容能被及时纳入观察。

## 2. 自动化 CDN 图片加速

为了提升国内访问速度，我使用 jsDelivr 加速 GitHub 仓库中的图片。

之前我写了一个 `cdn-images.js` 脚本，它会自动将页面内的相对路径图片 (`/images/...`) 替换为 CDN 链接。

### 遇到的问题

脚本只处理了 `src` 属性。当我们切换到懒加载模式后，图片 URL 存储在 `data-src` 属性中，原脚本就失效了。这意味着图片在懒加载触发时，仍然请求的是原始路径（或者因为生产环境路径问题导致 404）。

### 改进

我更新了 `cdn-images.js`，使其：
1.  同时扫描 `src` 和 `data-src` 属性。
2.  监听 `MutationObserver`，当新内容（如"加载更多"加载的 Posts）被插入 DOM 时，也能自动处理其中的图片。
3.  保持本地开发环境（`localhost`）不走 CDN，方便调试。

```javascript
// 同时处理 src 和 data-src
const dataSrc = img.getAttribute('data-src');
if (dataSrc) {
    const newDataSrc = toCdnUrl(dataSrc);
    if (newDataSrc !== dataSrc) {
        img.setAttribute('data-src', newDataSrc);
    }
}
```

## 3. 为动态内容集成 Giscus 评论

这是最有趣的部分。Giscus 通常用于博客文章页，一一对应。但我想在 Posts 流中的**每一条广播**下都添加评论功能。

### 挑战 1：唯一 ID 的生成

Posts 并非独立的 Jekyll Post 文件，而是从 JSON 数据中读取生成的。它们没有天然的 `page.url` 或 `page.id`。

**解决方案**：既然广播不会频繁修改发布时间，我决定使用**时间戳**作为唯一标识。
格式：`douban-{YYYY}-{MM}-{DD}-{HH}-{MM}`。

前端渲染时：
```liquid
{% assign post_id = item.time | replace: " ", "-" | replace: ":", "-" %}
<div class="feed-item" data-post-id="douban-{{ post_id }}">
    ...
```

这个 `douban-2026-01-18-19-10` 就成为了 Giscus 配置中的 `term` 参数。

### 挑战 2：单实例复用与性能

如果给列表里成百上千条 Post 都预先加载 Giscus iframe，浏览器肯定会崩溃。

**解决方案**：
1.  **按需加载**：只有用户点击"评论"按钮时，才初始化 Giscus。
2.  **单实例模式**：整个页面只维护**一个** Giscus 容器和 iframe。当用户点击另一条 Post 的评论时，我们将这个容器移动（`appendChild`）到新的父节点下，并通 `postMessage` (或者重新设置 `src`) 更新 `term`。

### 挑战 3：数据预加载

如果用户必须点开才能看到有没有评论，体验不够好。我希望直接在按钮上显示"3条评论"、"5个赞"。

**解决方案**：利用 Giscus 的 API（通过 GitHub GraphQL）。
在页面加载（以及加载更多）时，我会批量获取当前可见 Post 的统计数据。

```javascript
// 获取统计数据
const searchUrl = `https://giscus.app/api/discussions?` + new URLSearchParams({
    repo: repo,
    term: term,
    // ...
});

const data = await response.json();
if (data.discussion) {
    updatePostStatsUI(term, {
        commentCount: data.discussion.totalCommentCount,
        reactionCount: data.discussion.reactionCount
    });
}
```

为了避免触发 API 速率限制，我在请求之间加入了 200ms 的延时。

## 4. 移动端体验优化与冲突解决

### Sticky Tabs

在移动端，我希望 Tabs 栏在用户向下滚动查看内容时能吸顶，方便切换。
最初使用了 `position: sticky`，但在 iOS Safari 上经常失效。原因通常是父级元素设置了 `overflow: hidden` 或 `overflow: auto`。

通过排查 CSS 层级，我将相关父容器（`html`, `body`, `.social-main` 等）的 `overflow` 属性调整为 `visible` 或 `clip`，最终让 Sticky 效果稳定工作。

### 图片放大镜冲突

我使用了 `medium-zoom` 插件来实现文章图片的点击放大。同时，我在 Posts 页面实现了一个自定义的 Lightbox（支持相册切换）。

结果导致：点击 Post 图片时，同时触发了 `medium-zoom` 的放大和我的 Lightbox 弹窗，体验非常割裂。

**修复**：给 Posts 页面的图片添加 `no-zoom` 类。`medium-zoom` 初始化时会忽略带此类名的图片。

```html
<img data-src="..." class="social-img lazy-img no-zoom">
```

## 总结

经过这一晚的优化，Social 页面的体验有了质的飞跃：
- **快**：图片按需加载，CDN 加速。
- **稳**：布局交互更丝滑，移动端适配更好。
- **活**：每一条动态都可以被点赞和评论，让这个静态页面"活"了起来。

这种在静态站点（SSG）上通过 "Micro-Interactions"（微交互）和动态 API 增强功能的实践，既保留了静态站点的低成本和高性能，又弥补了其交互性的短板，是一个非常值得推荐的模式。
