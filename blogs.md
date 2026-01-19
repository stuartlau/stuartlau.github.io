---
layout: page
permalink: /blogs/index.html
title: Blogs
subtitle: 技术博客，记录学习与成长
---

<div class="tag-cloud-wrap">
  <div class="tag-cloud-head">
    <div class="tag-cloud-title">Tags</div>
    <button id="tag-cloud-clear" class="tag-cloud-clear" hidden>Clear</button>
    <div id="tag-cloud-active" class="tag-cloud-active" hidden></div>
  </div>
  <div id="tag-cloud" class="tag-cloud"></div>
</div>

<div id="blog-list" class="blog-list">
  {% assign sorted_posts = "" | split: "" %}
  {% for post in site.pages %}
    {% if post.url contains '/blogs/tech/' and post.layout == 'post' and post.date %}
      {% assign sorted_posts = sorted_posts | push: post %}
    {% endif %}
  {% endfor %}
  {% assign sorted_posts = sorted_posts | sort: "date" | reverse %}
  {% for post in sorted_posts limit: 10 %}
  <a href="{{ post.url }}" class="blog-item" data-tags="{{ post.tags | join: ',' }}">
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

{% if sorted_posts.size > 10 %}
<button id="load-more-blogs" class="load-more-btn" onclick="loadMoreBlogs()">Load more blogs ↓</button>
{% endif %}

<div id="all-posts-data" data-posts='[
  {% for post in sorted_posts %}
  {
    "url": "{{ post.url }}",
    "title": "{{ post.title | escape }}",
    "date": "{{ post.date | date: "%Y-%m-%d" }}",
    "subtitle": "{{ post.subtitle | default: post.description | default: "" | escape }}",
    "tags": [{% for tag in post.tags %}"{{ tag }}"{% unless forloop.last %},{% endunless %}{% endfor %}]
  }{% unless forloop.last %},{% endunless %}
  {% endfor %}
]'></div>

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
.blog-item.hidden { display: none; }
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
.tag-cloud-clear {
    padding: 4px 12px;
    background: #f3f4f6;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    font-size: 0.8rem;
    cursor: pointer;
}
.tag-cloud-clear:hover { background: #e5e7eb; }
.tag-cloud-active {
    padding: 4px 12px;
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    border-radius: 20px;
    font-size: 0.8rem;
}
.tag {
    padding: 6px 14px;
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    border-radius: 20px;
    font-size: 0.85rem;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s;
}
.tag:hover, .tag.active { background: rgba(16, 185, 129, 0.2); }
.load-more-btn {
    display: block;
    width: 100%;
    max-width: 800px;
    margin: 20px auto;
    padding: 12px 24px;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    color: #6b7280;
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
}
.load-more-btn:hover { background: #f3f4f6; color: #374151; }
.load-more-btn.hidden { display: none; }
</style>

<script>
// Tag cloud and blog filtering
document.addEventListener('DOMContentLoaded', function() {
    // Collect all tags from posts
    const tagCounts = {};
    const blogItems = document.querySelectorAll('.blog-item');
    
    blogItems.forEach(item => {
        const tags = (item.dataset.tags || '').split(',').filter(t => t && t !== 'Post' && t !== 'Jekyll' && t !== 'featured');
        tags.forEach(tag => {
            tagCounts[tag] = (tagCounts[tag] || 0) + 1;
        });
    });
    
    // Create tag cloud
    const cloudEl = document.getElementById('tag-cloud');
    if (cloudEl && Object.keys(tagCounts).length > 0) {
        const tags = Object.keys(tagCounts).map(tag => ({ tag, count: tagCounts[tag] }));
        const minCount = Math.min(...tags.map(t => t.count));
        const maxCount = Math.max(...tags.map(t => t.count));
        const sizeScale = d3.scale.linear().domain([minCount, maxCount]).range([12, 28]);
        
        tags.sort((a, b) => a.tag.localeCompare(b.tag));
        
        tags.forEach(({ tag, count }) => {
            const a = document.createElement('a');
            a.className = 'tag';
            a.dataset.tag = tag;
            a.textContent = tag;
            a.style.fontSize = sizeScale(count) + 'px';
            a.title = count + ' posts';
            a.addEventListener('click', () => toggleTag(tag));
            cloudEl.appendChild(a);
        });
    }
    
    // Setup load more
    window.blogsData = JSON.parse(document.getElementById('all-posts-data').dataset.posts);
    window.blogsVisible = 10;
    
    const loadMoreBtn = document.getElementById('load-more-blogs');
    if (loadMoreBtn && window.blogsData.length <= 10) {
        loadMoreBtn.classList.add('hidden');
    }
});

let activeTag = '';

function toggleTag(tag) {
    const cloudEl = document.getElementById('tag-cloud');
    const clearBtn = document.getElementById('tag-cloud-clear');
    const activeEl = document.getElementById('tag-cloud-active');
    const blogItems = document.querySelectorAll('.blog-item');
    const loadMoreBtn = document.getElementById('load-more-blogs');
    
    if (activeTag === tag) {
        activeTag = '';
        cloudEl.querySelectorAll('.tag').forEach(t => t.classList.remove('active'));
        clearBtn.hidden = true;
        activeEl.hidden = true;
        
        // Show first 10 items
        blogItems.forEach((item, index) => {
            item.classList.toggle('hidden', index >= 10);
        });
        
        if (window.blogsData && window.blogsData.length > 10) {
            loadMoreBtn.classList.remove('hidden');
        }
        window.blogsVisible = 10;
    } else {
        activeTag = tag;
        cloudEl.querySelectorAll('.tag').forEach(t => t.classList.remove('active'));
        cloudEl.querySelector(`[data-tag="${tag}"]`).classList.add('active');
        clearBtn.hidden = false;
        activeEl.textContent = 'Filter: ' + tag;
        activeEl.hidden = false;
        
        // Filter items
        let visibleCount = 0;
        blogItems.forEach(item => {
            const tags = (item.dataset.tags || '').split(',');
            const matches = tags.includes(tag) && tags.includes(tag); // Already filtered above
            item.classList.toggle('hidden', !tags.includes(tag));
            if (!tags.includes(tag)) visibleCount++;
        });
        
        loadMoreBtn.classList.add('hidden');
        window.blogsVisible = visibleCount;
    }
}

function loadMoreBlogs() {
    const blogList = document.getElementById('blog-list');
    const loadMoreBtn = document.getElementById('load-more-blogs');
    
    if (!window.blogsData) return;
    
    const fragment = document.createDocumentFragment();
    const start = window.blogsVisible;
    const end = Math.min(start + 10, window.blogsData.length);
    
    for (let i = start; i < end; i++) {
        const post = window.blogsData[i];
        const a = document.createElement('a');
        a.href = post.url;
        a.className = 'blog-item' + (activeTag && !post.tags.includes(activeTag) ? ' hidden' : '');
        a.dataset.tags = post.tags.join(',');
        
        const tagsHtml = post.tags
            .filter(t => t !== 'Post' && t !== 'Jekyll' && t !== 'featured')
            .slice(0, 2)
            .map(t => `<span class="blog-tag">${t}</span>`)
            .join('');
        
        a.innerHTML = `
            <div class="blog-item-header">
                <span class="blog-date">${post.date}</span>
                <span class="blog-tags">${tagsHtml}</span>
            </div>
            <h3 class="blog-title">${post.title}</h3>
            ${post.subtitle ? `<p class="blog-subtitle">${post.subtitle}</p>` : ''}
        `;
        fragment.appendChild(a);
    }
    
    blogList.appendChild(fragment);
    window.blogsVisible = end;
    
    if (end >= window.blogsData.length) {
        loadMoreBtn.classList.add('hidden');
    }
}

document.getElementById('tag-cloud-clear')?.addEventListener('click', () => toggleTag(activeTag));
</script>
