---
layout: page
permalink: /blogs/index.html
title: Blogs
subtitle: 技术博客，记录学习与成长
---

<div class="tag-cloud-wrap">
  <div class="tag-cloud-head">
    <div class="tag-cloud-title">Tags</div>
    <button id="tag-cloud-clear" type="button" class="tag-cloud-clear" hidden>Clear</button>
    <div id="tag-cloud-active" class="tag-cloud-active" hidden></div>
  </div>
  <div id="tag-cloud" class="tag-cloud"></div>
</div>

<div id="blog-list" class="blog-list" data-api-base="/api/blogs"></div>

<div class="infinite-loading" id="blog-loading" style="display: none; text-align: center; padding: 20px;">
  <div class="infinite-spinner">
    <div class="spinner"></div>
    <span>加载中...</span>
  </div>
</div>

<div class="infinite-end" id="blog-end" style="display: none; text-align: center; padding: 30px; color: #999;">
  <span>— 已经到底啦 —</span>
</div>

<script>
  window.__BLOG_POSTS__ = [];
</script>
