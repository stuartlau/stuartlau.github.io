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
  <div class="loading-state">Loading posts...</div>
</div>

<button id="load-more-blogs" class="load-more-btn hidden" onclick="loadMoreBlogs()">Load more blogs ↓</button>

<style>
.blog-list { max-width: 800px; margin: 0 auto; min-height: 200px; }
.loading-state { text-align: center; padding: 40px; color: #9ca3af; font-size: 1.1rem; }
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
    outline: none;
    border: none;
}
.load-more-btn:hover { background: #f3f4f6; color: #374151; }
.load-more-btn.hidden { display: none; }
</style>

<script>
// State
let allPosts = [];
let filteredPosts = [];
let visibleCount = 0;
let activeTag = '';
const PAGE_SIZE = 10;

document.addEventListener('DOMContentLoaded', async function() {
    try {
        const response = await fetch('/api/blogs.json');
        if (!response.ok) throw new Error('Failed to load data');
        
        allPosts = await response.json();
        // Initial setup
        initTagCloud();
        applyFilter(); 
        
    } catch (e) {
        console.error(e);
        document.getElementById('blog-list').innerHTML = 
            '<div class="loading-state">Failed to load posts. Please try again later.</div>';
    }
});

function initTagCloud() {
    const tagCounts = {};
    allPosts.forEach(post => {
        if (post.tags) {
            post.tags.forEach(tag => {
                if (tag && tag !== 'Post' && tag !== 'Jekyll' && tag !== 'featured') {
                    tagCounts[tag] = (tagCounts[tag] || 0) + 1;
                }
            });
        }
    });

    const cloudEl = document.getElementById('tag-cloud');
    if (!cloudEl || Object.keys(tagCounts).length === 0) return;

    const tags = Object.keys(tagCounts).map(tag => ({ tag, count: tagCounts[tag] }));
    const minCount = Math.min(...tags.map(t => t.count));
    const maxCount = Math.max(...tags.map(t => t.count));

    // Manual scale function
    const sizeScale = (count) => {
        if (maxCount === minCount) return 16;
        return 12 + ((count - minCount) / (maxCount - minCount)) * (16); // 12px to 28px
    };

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
    
    // Setup clear button
    const clearBtn = document.getElementById('tag-cloud-clear');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => toggleTag(activeTag));
    }
}

function toggleTag(tag) {
    const cloudEl = document.getElementById('tag-cloud');
    const clearBtn = document.getElementById('tag-cloud-clear');
    const activeEl = document.getElementById('tag-cloud-active');
    
    if (activeTag === tag) {
        // Deactivate
        activeTag = '';
        cloudEl.querySelectorAll('.tag').forEach(t => t.classList.remove('active'));
        clearBtn.hidden = true;
        activeEl.hidden = true;
    } else {
        // Activate
        activeTag = tag;
        cloudEl.querySelectorAll('.tag').forEach(t => t.classList.remove('active'));
        const tagEl = cloudEl.querySelector(`[data-tag="${tag}"]`);
        if (tagEl) tagEl.classList.add('active');
        
        clearBtn.hidden = false;
        activeEl.textContent = 'Filter: ' + tag;
        activeEl.hidden = false;
    }
    
    applyFilter();
}

function applyFilter() {
    if (activeTag) {
        filteredPosts = allPosts.filter(p => p.tags && p.tags.includes(activeTag));
    } else {
        filteredPosts = [...allPosts];
    }
    
    // Reset list
    const list = document.getElementById('blog-list');
    list.innerHTML = '';
    visibleCount = 0;
    
    if (filteredPosts.length === 0) {
        list.innerHTML = '<div class="loading-state">No posts found for this tag.</div>';
        document.getElementById('load-more-blogs').classList.add('hidden');
    } else {
        loadMoreBlogs();
    }
}

function loadMoreBlogs() {
    const list = document.getElementById('blog-list');
    const start = visibleCount;
    const end = Math.min(start + PAGE_SIZE, filteredPosts.length);
    
    if (start >= end) return;
    
    const fragment = document.createDocumentFragment();
    
    for (let i = start; i < end; i++) {
        const post = filteredPosts[i];
        const a = document.createElement('a');
        a.href = post.url;
        a.className = 'blog-item';
        
        // Tags to display
        const displayTags = (post.tags || [])
            .filter(t => t !== 'Post' && t !== 'Jekyll' && t !== 'featured')
            .slice(0, 2)
            .map(t => `<span class="blog-tag">${t}</span>`)
            .join('');
            
        a.innerHTML = `
            <div class="blog-item-author" style="display:flex; align-items:flex-start; margin-bottom:8px;">
                <div class="post-avatar" style="width:40px; height:40px; margin-right:12px; flex-shrink:0;">
                    <img src="/images/douban_avatar.jpg" alt="Stuart Lau" style="width:100%; height:100%; border-radius:50%; object-fit:cover;">
                </div>
                <div style="flex:1;">
                    <div class="post-info" style="display:flex; align-items:center; flex-wrap:wrap;">
                        <span style="font-weight:700; color:#0f1419; margin-right:4px;">@stuartlau</span>
                        <span style="color:#536471; font-size:15px; margin-right:8px;">· ${post.date || ''}</span>
                        <div class="blog-tags" style="margin-left:auto;">${displayTags}</div>
                    </div>
                </div>
            </div>
            <div style="padding-left:52px;">
                <h3 class="blog-title" style="margin:0 0 6px 0;">${post.title}</h3>
                ${post.subtitle ? `<p class="blog-subtitle">${post.subtitle}</p>` : ''}
            </div>
        `;
        fragment.appendChild(a);
    }
    
    list.appendChild(fragment);
    visibleCount = end;
    
    // Button visibility
    const loadMoreBtn = document.getElementById('load-more-blogs');
    if (visibleCount >= filteredPosts.length) {
        loadMoreBtn.classList.add('hidden');
    } else {
        loadMoreBtn.classList.remove('hidden');
    }
}
</script>
