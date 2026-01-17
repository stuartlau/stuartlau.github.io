---
layout: page
permalink: /publications/index.html
title: Publications
subtitle: 专利与学术著作展示
---
## Patent

{% assign all_posts = site.pages | where: "layout", "post" %}
{% assign granted_count = 0 %}
{% assign pending_count = 0 %}
{% for p in all_posts %}
  {% if p.url contains '/blogs/' %}
    {% if p.title contains '待授权专利' %}
      {% assign pending_count = pending_count | plus: 1 %}
    {% elsif p.title contains '授权专利' %}
      {% assign granted_count = granted_count | plus: 1 %}
    {% endif %}
  {% endif %}
{% endfor %}

<p style="font-size: 1.1em; font-weight: 500; margin-bottom: 1.5rem;">
  已授权（{{ granted_count }}个）、待授权（{{ pending_count }}个）
</p>

<div class="tag-cloud-wrap">
  <div class="tag-cloud-head">
    <div class="tag-cloud-title">Patent Tags Cloud</div>
    <button id="tag-cloud-clear" type="button" class="tag-cloud-clear" hidden>Clear</button>
    <div id="tag-cloud-active" class="tag-cloud-active" hidden></div>
  </div>
  <div id="tag-cloud" class="tag-cloud"></div>
</div>

<!-- Container for filtered results when a tag is clicked -->
<div id="blog-list" class="blog-list"></div>

{%- assign patent_posts = site.pages | where: "layout", "post" | where_exp: "p", "p.url contains '/blogs/'" | where_exp: "p", "p.tags contains 'Patent'" -%}

<script>
  window.__BLOG_POSTS__ = [
    {%- for p in patent_posts -%}
      {
        title: {{ p.title | default: p.url | jsonify }},
        url: {{ p.url | relative_url | jsonify }},
        date: {{ p.date | date_to_xmlschema | jsonify }},
        tags: {{ p.tags | default: empty | jsonify }}
      }{%- unless forloop.last -%},{%- endunless -%}
    {%- endfor -%}
  ];
</script>

<script src="https://cdn.jsdelivr.net/npm/d3@3.5.17/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3-cloud@1/build/d3.layout.cloud.js"></script>
<script src="{{ site.url }}/assets/js/tag-cloud.js"></script>

<br>

---
## Conference Paper
- Shuo Liu, Qiaoyan Wen, <a href="https://ieeexplore.ieee.org/abstract/document/6155893/">Distributed cluster
  authentication model based on CAS</a>
  <em>2011 4th IEEE International Conference on Broadband Network and Multimedia
  Technology(<strong>IEEE</strong>)</em>, 2012
<br>

---
## Community Contribution
- <a href="https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=180194">OpenDNSSEC 1.4.1 Bugfixes, 2013</a>