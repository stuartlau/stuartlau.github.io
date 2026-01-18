---
layout: page
permalink: /blogs/index.html
title: Blogs
subtitle: 技术博客，记录学习与成长
---

<div class="tag-cloud-wrap">
  <div class="tag-cloud-head">
    <div class="tag-cloud-title">Tags</div>
  </div>
  <div id="tag-cloud" class="tag-cloud">
    {% assign all_tags = "" | split: "" %}
    {% for post in site.pages %}
      {% if post.url contains '/blogs/tech/' and post.layout == 'post' %}
        {% for tag in post.tags %}
          {% unless tag == "Post" or tag == "Jekyll" or tag == "featured" or tag == nil %}
            {% assign all_tags = all_tags | push: tag %}
          {% endunless %}
        {% endfor %}
      {% endif %}
    {% endfor %}
    {% assign unique_tags = all_tags | uniq | sort %}
    {% for tag in unique_tags %}
      <a href="#tag-{{ tag | slugify }}" class="tag" data-tag="{{ tag }}">{{ tag }}</a>
    {% endfor %}
  </div>
</div>

<div id="blog-list" class="blog-list">
  {% assign sorted_posts = "" | split: "" %}
  {% for post in site.pages %}
    {% if post.url contains '/blogs/tech/' and post.layout == 'post' and post.date %}
      {% assign sorted_posts = sorted_posts | push: post %}
    {% endif %}
  {% endfor %}
  {% assign sorted_posts = sorted_posts | sort: "date" | reverse %}
  {% for post in sorted_posts limit: 20 %}
  <a href="{{ post.url }}" class="blog-item">
    <div class="blog-item-header">
      <span class="blog-date">{{ post.date | date: "%Y-%m-%d" }}</span>
      <span class="blog-tags">
        {% for tag in post.tags limit: 2 %}
          {% unless tag == "Post" or tag == "Jekyll" or tag == "featured" %}
            <span class="blog-tag">{{ tag }}</span>
          {% endunless %}
        {% endfor %}
      </span>
    </div>
    <h3 class="blog-title">{{ post.title }}</h3>
    {% if post.subtitle %}
    <p class="blog-subtitle">{{ post.subtitle }}</p>
    {% endif %}
  </a>
  {% endfor %}
</div>

<style>
.blog-list { max-width: 800px; margin: 0 auto; }
.blog-item {
    display: block;
    padding: 20px 24px;
    margin-bottom: 12px;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    text-decoration: none;
    transition: all 0.2s ease;
}
.blog-item:hover {
    border-color: #ec4899;
    box-shadow: 0 4px 12px rgba(236, 72, 153, 0.1);
    transform: translateY(-2px);
}
.blog-item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.blog-date { font-size: 0.85rem; color: #9ca3af; }
.blog-tags { display: flex; gap: 8px; }
.blog-tag {
    font-size: 0.75rem;
    padding: 2px 8px;
    background: rgba(236, 72, 153, 0.1);
    color: #ec4899;
    border-radius: 4px;
}
.blog-title { margin: 0 0 4px 0; font-size: 1.1rem; font-weight: 600; color: #1f2937; }
.blog-subtitle { margin: 0; font-size: 0.9rem; color: #6b7280; }
.tag-cloud { display: flex; flex-wrap: wrap; gap: 8px; padding: 16px 0; }
.tag {
    padding: 6px 14px;
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    border-radius: 20px;
    font-size: 0.85rem;
    text-decoration: none;
    transition: all 0.2s;
}
.tag:hover { background: rgba(16, 185, 129, 0.2); }
</style>
