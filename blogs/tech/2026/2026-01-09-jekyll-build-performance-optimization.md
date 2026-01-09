---
layout: post
title: "记一次 Jekyll 构建时间从 1 分钟激增到 10 分钟的排查与优化"
subtitle: "从 O(N²) 的 Liquid 循环到前端异步加载的架构演进"
date: 2026-01-09
author: StuartLau
header-img: img/post-bg-debug.png
catalog: true
tags:
    - Jekyll
    - Configuration
    - Performance
    - Debugging
---

## 背景：突如其来的构建变慢

最近在对博客进行功能迭代时，突然发现 GitHub Actions 的构建时间出现了异常的激增。

- **正常情况**：构建部署通常在 **1 分钟** 左右完成。
- **异常情况**：突然飙升至 **10 分钟** 以上，甚至偶尔超时。

起初，通过 Git 提交历史排查，我怀疑是最近引入的 **豆瓣广播同步功能** 导致的。因为该功能将数千张图片（约 600MB）提交到了 Git 仓库中。直觉告诉我，Git 拉取和 Jekyll 复制大量静态文件的 IO 开销是罪魁祸首。

然而，经过对比测试和详细的 Log 分析，事实并非如此。

## 根本原因：算法复杂度陷阱

虽然图片增多确实会增加 IO 时间，但真正的瓶颈在于 CPU 计算。

在排查中，我发现引入了一个新的功能模块：**相关文章推荐 (Related Posts)**。这个功能被实现在 `_includes/related-posts.html` 中，完全使用了 Jekyll 的模板语言 **Liquid** 编写。

### 问题代码分析

```liquid
{% comment %} 伪代码逻辑 {% endcomment %}
{% for post in site.posts %}             <!-- 外层循环：遍历所有文章 (N) -->
  {% for other_post in site.posts %}     <!-- 内层循环：再次遍历所有文章 (N) -->
     <!-- 计算标签交集和排序逻辑 -->
  {% endfor %}
{% endfor %}
```

这就构成了一个经典的 **$O(N^2)$** 算法复杂度问题。

- **Liquid 的低效**：Liquid 是一个为了安全和简单设计的模板语言，并不适合进行复杂的逻辑运算。
- **指数级爆炸**：随着博客文章数量增长到几百篇，计算量呈指数级上升。对于每一篇文章生成页面时，Jekyll 都要遍历全站其他所有文章计算相关度。

### 流程对比图

我们可以用 Mermaid图表来直观地看清这个问题：

<div class="mermaid">
graph TD
    subgraph "Before: Liquid Implementation (Server Side)"
    A[Jekyll Build Start] --> B{Iterate All Posts}
    B -->|Post 1...N| C[Calculate Related Posts]
    C --> D{Iterate All Other Posts}
    D --> E[Compare Tags]
    E --> F[Sort by Relevance]
    F --> G[Render HTML]
    G --> H[Next Post]
    end
    
    style C fill:#f96,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    style D fill:#f96,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    
    subgraph "Bottleneck Analysis"
    I[Complexity O N*N]
    J[Build Time: ~10 mins]
    end

    C -.-> I
    G -.-> J
</div>

## 解决方案：架构迁移至前端

为了解决这个问题，我决定将计算压力从 **构建时 (Build Time)** 转移到 **运行时 (Runtime)**，并利用客户端浏览器的计算能力。

### 1. 数据层改造

首先，我们需要让前端能够获取到所有文章的元数据（特别是标签）。利用现有的 `search.json`，在其中追加 `tags` 字段。

```json
{
  "title": "...",
  "url": "...",
  "tags": ["Tech", "Optimization", ...]  // 新增字段
}
```

### 2. 前端实现 (JavaScript)

编写一段轻量级的 JavaScript 代码 (`assets/js/related-posts.js`)，在页面加载完成后异步执行：

1.  读取当前页面的标签。
2.  获取 `search.json` 数据。
3.  在浏览器内存中过滤出有共同标签的文章。
4.  按相关度排序并提取前 3 篇。
5.  动态插入 DOM 到页面中。

### 优化后的架构

<div class="mermaid">
sequenceDiagram
    participant B as Jekyll Build
    participant C as Client Browser
    participant S as Server (GitHub Pages)

    Note over B: Optimization Phase
    B->>B: Generate search.json (O(N))
    B->>S: Deploy Static Files
    Note right of B: Build Time: ~1 min
    
    Note over C: Runtime Phase
    C->>S: Request Page HTML
    S-->>C: Return HTML (Clean)
    C->>S: Async Fetch search.json
    S-->>C: Return JSON Data
    
    rect rgb(240, 248, 255)
    Note right of C: JavaScript Logic
    C->>C: Filter Related Posts
    C->>C: Render to DOM
    end
</div>

## 总结

通过这次优化，我们将一个计算密集型的任务从原本不擅长计算的 Liquid 模板引擎中剥离，交给了擅长处理数据的 JavaScript 引擎。

**成效显著：**
*   **构建时间**：从 10 分钟回落至 **1 分钟**。
*   **用户体验**：页面首屏加载不受影响，相关推荐异步加载，顺滑流畅。
*   **可维护性**：JS 代码比复杂的 Liquid 模板更易读、易调试。

这也再次印证了在静态网站生成器中，**"Data as API, Logic as Client-side"** 往往是处理复杂动态逻辑的最佳实践。
