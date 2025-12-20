---
layout: page
permalink: /blogs/index.html
title: Blogs
---

<div class="tag-cloud-wrap">
  <div class="tag-cloud-head">
    <div class="tag-cloud-title">Tags</div>
    <button id="tag-cloud-clear" type="button" class="tag-cloud-clear" hidden>Clear</button>
    <div id="tag-cloud-active" class="tag-cloud-active" hidden></div>
  </div>
  <div id="tag-cloud" class="tag-cloud"></div>
</div>

<div id="blog-list" class="blog-list"></div>

{% assign docs = site.pages | where: "layout", "post" %}
{% assign docs = docs | where_exp: "p", "p.url contains '/blogs/'" %}
{% assign docs = docs | sort: "date" | reverse %}

<script>
  window.__BLOG_POSTS__ = [
    {% for p in docs %}
      {
        title: {{ p.title | default: p.url | jsonify }},
        url: {{ p.url | relative_url | jsonify }},
        date: {{ p.date | date_to_xmlschema | jsonify }},
        tags: {{ p.tags | default: empty | jsonify }}
      }{% unless forloop.last %},{% endunless %}
    {% endfor %}
  ];
</script>
