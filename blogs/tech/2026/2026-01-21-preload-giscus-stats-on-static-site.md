---
layout: post
title: "静态博客实战：如何在列表页预加载 Giscus 评论数与避坑指南"
date: 2026-01-21
categories: Tech
tags: [Giscus, Jekyll, GraphQL, CORS, Frontend]
description: "详细记录了在静态博客（Jekyll）的动态流页面中集成 Giscus 评论系统的全过程。面对浏览器 CORS 跨域限制，从尝试直连 API 到使用 corsproxy.io 失败，最终通过 allorigins.win 成功解决问题的排坑实录。"
header-img: "https://user-gold-cdn.xitu.io/2019/3/22/169a4d626f362741?imageView2/0/w/1280/h/960/format/webp/ignore-error/1"
---

在上一篇文章中，我提到为博客的 Social 页面添加了点赞和评论功能。其中最核心的挑战在于：**如何在用户不点开评论框的情况下，就在列表中直接显示每条动态的"评论数"和"点赞数"？**

Giscus 本身是一个基于 GitHub Discussions 的评论系统，它的核心逻辑是加载一个 `iframe`。但如果我们想在列表页展示 50 条动态的统计数据，总不能预加载 50 个 iframe 吧？那浏览器直接就炸了。

本文将详细复盘如何利用 Giscus 的 API 实现数据预加载，以及在实现过程中遇到的严重的 CORS（跨域）问题及其终极解决方案。

## 1. 方案设计：利用 API 预取数据

Giscus 官方虽然主要提供组件接入，但它背后的数据完全存储在 GitHub Discussions 中。Giscus 也提供了一个未公开但在社区中广为人知的 API 端点，用于获取 Discussion 的元数据。

端点地址：`https://giscus.app/api/discussions`

我们只需要传入配置好的参数（repo, term, category 等），它就会返回如下 JSON 结构：

```json
{
  "discussion": {
    "totalCommentCount": 5,
    "reactionCount": 12,
    "reactions": { ... }
  }
}
```

这看起来太完美了！我迅速写好了前端代码：

```javascript
const params = new URLSearchParams({
    repo: 'stuartlau/stuartlau.github.io',
    term: 'douban-2026-01-20-12-00',
    category: 'Announcements',
    // ...
});

const response = await fetch(`https://giscus.app/api/discussions?${params}`);
const data = await response.json();
updateUI(data.discussion.totalCommentCount);
```

## 2. 第一道坎：浏览器 CORS 拦截

代码在本地用 `curl` 测试完美通过，数据返回正常。然而，一部署到网页上，控制台直接飘红：

```
Access to fetch at 'https://giscus.app/api/...' from origin 'https://stuartlau.github.io' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**原因分析**：
Giscus 的这个 API 并没有配置允许跨域（`Access-Control-Allow-Origin: *`）。这意味着它不希望被前端页面直接 Ajax 调用，可能是为了防止滥用。

对于纯静态博客，我们没有后端服务器来做"中转代理"，这下麻烦了。

## 3. 尝试一：使用 corsproxy.io

在前端解决 CORS 问题的标准做法是使用 **CORS Proxy**。这类服务的作用是：
1.  你请求代理服务器。
2.  代理服务器去请求目标地址（服务器端请求不受 CORS 限制）。
3.  代理服务器把结果返回给你，并加上允许跨域的 Header。

我首先尝试了业界知名的 `corsproxy.io`：

```javascript
const targetUrl = `https://giscus.app/api/discussions?${params}`;
const proxyUrl = `https://corsproxy.io/?${encodeURIComponent(targetUrl)}`;
await fetch(proxyUrl);
```

**结果：失败 (403 Forbidden)**
在本地测试时（localhost），请求成功了。但当我部署到线上或者多刷新几次后，请求变成了 `403 Forbidden`。
查看响应内容，发现是 **Cloudflare 的盾**拦截了请求。因为 `corsproxy.io` 是公共服务，很容易被 CDN 厂商标记为"机器人流量"或"滥用行为"而进行屏蔽。依赖它不够稳定。

## 4. 终极方案：使用 AllOrigins

在几乎要放弃、准备改为"点击后才加载"的时候，我想到了另一个更老牌、机制稍微不同的代理服务：**AllOrigins** (`api.allorigins.win`)。

与直接透传响应不同，AllOrigins 会将目标内容包装在一个 JSON 对象的 `contents` 字段中返回。这种"包裹"的方式，似乎更容易绕过一些简单的反爬策略，且该服务的稳定性在社区口碑中一直不错。

**代码实现**：

```javascript
// 1. 构造原始 Giscus API 地址
const apiUrl = `https://giscus.app/api/discussions?` + new URLSearchParams({
    repo: 'stuartlau/stuartlau.github.io',
    term: 'douban-2026-01-20-12-00',
    category: 'Announcements',
    strict: '0',
    reactionsEnabled: 'true',
    emitMetadata: 'false'
});

// 2. 使用 allorigins.win 作为代理
const searchUrl = 'https://api.allorigins.win/get?url=' + encodeURIComponent(apiUrl);

try {
    const response = await fetch(searchUrl);
    if (!response.ok) throw new Error('Proxy error');
    
    // 3. 关键步骤：解析包装好的数据
    const proxyData = await response.json();
    // 目标数据在 contents 字段里，且是字符串格式，需要二次解析
    const data = JSON.parse(proxyData.contents); 
    
    // 4. 更新 UI
    if (data && data.discussion) {
        renderStats(data.discussion.totalCommentCount, data.discussion.reactionCount);
    }
} catch (e) {
    console.warn('预加载失败，降级为不显示数字');
}
```

**结果：成功！**
部署后，页面能够稳定地加载每个 Post 的评论数和点赞数。虽然多了一次网络跳转，但由于传输的数据量极小（JSON 文本），延迟几乎不可感知。

## 5. 性能优化技巧

虽然解决了跨域问题，但如果在列表页一次性发出 50 个请求，依然会对客户端和 Giscus 服务器造成压力。

为此我做了几个优化：
1.  **分批加载**：只加载当前视口内可见（Visible）的 Post 的数据。
2.  **请求节流**：在循环请求时，每个请求之间人为 `await setTimeout(200)`，避免瞬间并发过高触发速率限制（Rate Limiting）。
3.  **懒加载机制**：配合 Infinite Scroll，只有当用户滚动加载更多内容时，才去请求新内容的统计数据。

## 总结

在静态网站上通过 API 集成动态功能，CORS 往往是最大的拦路虎。在没有后端支持的情况下，合理利用 CORS Proxy 服务是一个有效的解法。

-   **corsproxy.io**：直接透传，使用方便，但容易被 Cloudflare 拦截。
-   **allorigins.win**：JSON 包裹返回，解析稍繁琐，但穿透性更好，更稳定。

希望这个避坑指南能帮助到同样想在静态博客里玩出花样的你。
