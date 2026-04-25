---
layout: default
subtitle: 社交媒体资料聚合页
---

<!-- Critical CSS - Inject immediately to prevent FOUC -->
<style>
/* Hide default layout elements immediately */
.social-page .navigation-wrapper,
.social-page .article-author-top,
.social-page .headline-wrap { display: none !important; }
.social-page #main { margin-top: 0 !important; max-width: none !important; width: 100% !important; padding: 0 !important; }
.social-page .article-wrap { max-width: none !important; width: 100% !important; padding: 0 !important; margin: 0 !important; }
.social-page article { max-width: none !important; width: 100% !important; }

/* Mobile horizontal padding - must use !important to override */
@media (max-width: 768px) {
    .social-page .social-layout { padding: 0 16px !important; }
}

/* Skeleton loading for images */
.lazy-img:not(.loaded) { background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%); background-size: 200% 100%; animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* Pre-define avatar/cover sizes to prevent layout shift */
.profile-avatar img { width: 100px; height: 100px; }
.post-avatar img { width: 40px; height: 40px; }
.profile-cover { height: 200px; }
</style>

<script>
// Add social-page class immediately (before DOMContentLoaded)
document.documentElement.classList.add('social-page');
document.body && document.body.classList.add('social-page');
</script>

<script>
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.includes('social')) {
        document.body.classList.add('social-page');
        // Hide default header elements
        var nav = document.querySelector('.navigation-wrapper');
        var authorTop = document.querySelector('.article-author-top');
        var headline = document.querySelector('.headline-wrap');
        if (nav) nav.style.display = 'none';
        if (authorTop) authorTop.style.display = 'none';
        if (headline) headline.style.display = 'none';
        
        // CRITICAL: Remove width constraints from parent containers
        // This fixes the middle column being squeezed issue
        var main = document.querySelector('#main');
        var articleWrap = document.querySelector('.article-wrap');
        var article = document.querySelector('article');
        
        if (main) {
            main.style.marginTop = '0';
            main.style.maxWidth = 'none';
            main.style.width = '100%';
            main.style.padding = '0';
        }
        if (articleWrap) {
            articleWrap.style.maxWidth = 'none';
            articleWrap.style.width = '100%';
            articleWrap.style.padding = '0';
            articleWrap.style.margin = '0';
        }
        if (article) {
            article.style.maxWidth = 'none';
            article.style.width = '100%';
        }
    }
});
</script>

<div class="social-layout">
    <!-- Left Sidebar - Fixed -->
    <aside class="social-left-sidebar">
        <div class="left-sidebar-inner">
            <a href="/" class="sidebar-logo-text">
                STUART LAU
            </a>
            <nav class="sidebar-nav">
                <a href="/" class="nav-item">
                    <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
                    <span>Home</span>
                </a>
                <a href="/publications/" class="nav-item">
                    <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                    <span>Patents</span>
                </a>
                <a href="/travel/" class="nav-item">
                    <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/></svg>
                    <span>Travel</span>
                </a>
            </nav>
        </div>
    </aside>

    <!-- Main Content - Scrollable -->
    <main class="social-main">
        {% assign posts_count = 0 %}
        {% assign years = "2026,2025,2024,2023,2022,2021" | split: "," %}
        {% for yr in years %}
            {% if site.data.douban[yr] %}
                {% assign posts_count = posts_count | plus: site.data.douban[yr].size %}
            {% endif %}
        {% endfor %}
        
        {% assign blogs_count = site.posts | concat: site.pages | where_exp: "p", "p.path contains 'blogs/tech/'" | size %}
        {% assign patents_count = site.pages | where: "layout", "post" | where_exp: "p", "p.path contains 'blogs/patent'" | size %}
        {% assign books_count = site.data.books.all | size %}
        {% assign movies_count = site.data.douban_movies | size | default: 0 %}
        {% assign games_count = site.data.douban_games | size | default: 0 %}
        {% assign travel_count = site.data['travel-points'].points.size | default: 99 %}

        <!-- Profile Header -->
        <div class="profile-header">
            <!-- Cover Image -->
            <div class="profile-cover">
                <img src="" alt="Cover" id="cover-img">
            </div>
            
            <!-- Profile Info Container -->
            <div class="profile-info-container">
                <!-- Avatar overlapping cover -->
                <div class="profile-avatar">
                    <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau">
                </div>
                
                <!-- Profile Details -->
                <div class="profile-details">
                    <h1 class="profile-name">Stuart Lau</h1>
                    <p class="profile-handle">@stuartlau</p>
                    <!-- Profile Bio - Category labels removed as requested -->
                    <div class="profile-meta">
                        <span><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/></svg> Shanghai, China</span>
                        <span><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg> <a href="{{ site.url }}" target="_blank">stuartlau.github.io</a></span>
                    </div>
                    <div class="profile-stats">
                        <a href="/publications/"><span class="stat-value">120+</span> Patents</a>
                        <a href="/travel/"><span class="stat-value">14</span> Countries</a>
                        <a href="/blogs/"><span class="stat-value">180+</span> Articles</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab Navigation -->
        <div class="content-tabs">
            <a href="#posts" class="tab-item active" data-tab="posts">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M4 11h5V5H4v6zm0 7h5v-6H4v6zm6 0h5v-6h-5v6zm6 0h5v-6h-5v6zm-6-7h5V5h-5v6zm6-6v6h5V5h-5z"/></svg>
                <span class="tab-text">Posts</span>
            </a>
            <a href="#blogs" class="tab-item" data-tab="blogs">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z"/></svg>
                <span class="tab-text">Articles</span>
            </a>
            <a href="#patents" class="tab-item" data-tab="patents">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                <span class="tab-text">Patents</span>
            </a>
            <a href="#douban" class="tab-item" data-tab="douban">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-5-9h10v2H7z"/></svg>
                <span class="tab-text">Collections</span>
            </a>
            <a href="#travel" class="tab-item" data-tab="travel">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zM7 9c0-2.76 2.24-5 5-5s5 2.24 5 5c0 2.88-2.88 7.19-5 9.88C9.08 16.19 7 11.88 7 9z"/><circle cx="12" cy="9" r="2.5"/></svg>
                <span class="tab-text">Travel</span>
            </a>
            <a href="#history" class="tab-item" data-tab="history" style="display:none;">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" class="tab-icon-mobile"><path d="M13 3a9 9 0 0 0-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42A8.954 8.954 0 0 0 13 21a9 9 0 0 0 0-18zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z"/></svg>
                <span class="tab-text" id="otd-tab-label">04/23</span>
            </a>
        </div>

        <!-- Content Panels -->
        <div class="content-panels">
            <!-- Posts Tab (Broadcast) -->
            <div class="content-panel active" id="posts-panel">
                <!-- Integrated OTD Section -->
                <div id="posts-otd-list" style="display:none;"></div>
                
                <div class="feed-list" id="posts-list">
                    {% assign years = "2026,2025,2024,2023,2022,2021" | split: "," %}
                    {% assign all_posts = "" | split: "," %}
                    {% for yr in years %}
                        {% if site.data.douban[yr] %}
                            {% assign all_posts = all_posts | concat: site.data.douban[yr] %}
                        {% endif %}
                    {% endfor %}
                    {% assign sorted_posts = all_posts | sort: "time" | reverse %}
                    {% for item in sorted_posts %}
                    {% assign post_id = item.time | replace: " ", "-" | replace: ":", "-" %}
                    <div class="feed-item douban-item expandable-item" data-post-id="douban-{{ post_id }}" {% if forloop.index > 10 %}style="display:none"{% endif %}>
                        <div class="post-avatar">
                            <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau" class="lazy-avatar" loading="lazy">
                        </div>
                        <div class="post-author-line">
                            <span class="feed-meta">{{ item.time }}</span>
                        </div>
                        <div class="feed-content">
                            <p class="feed-text">{{ item.content | strip_html | strip_newlines }}</p>
                            {% if item.images and item.images.size > 0 %}
                            <div class="social-image-grid">
                                {% for img in item.images %}
                                <div class="grid-img-wrap" onclick="openLightbox('{{ img }}', {{ item.images | jsonify | escape }})">
                                    <div class="img-placeholder">
                                        <div class="img-loading-spinner"></div>
                                    </div>
                                    <img data-src="{{ img }}" alt="Douban" class="social-img lazy-img no-zoom">
                                </div>
                                {% endfor %}
                            </div>
                            {% endif %}
                            
                            <!-- Interaction Buttons -->
                            <div class="post-actions">
                                <button class="action-btn comment-btn" onclick="togglePostComments(this)" data-post-id="douban-{{ post_id }}">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
                                    </svg>
                                    <span class="action-count" id="comment-count-{{ post_id }}">评论</span>
                                </button>
                                <button class="action-btn like-btn" onclick="togglePostComments(this)" data-post-id="douban-{{ post_id }}">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
                                    </svg>
                                    <span class="action-count" id="like-count-{{ post_id }}">点赞</span>
                                </button>
                                <button class="action-btn share-btn" onclick="openShareModal('douban-{{ post_id }}')">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/>
                                    </svg>
                                    <span class="action-count">分享</span>
                                </button>
                            </div>
                            
                            <!-- Giscus Comments Container (hidden by default) -->
                            <div class="post-giscus-wrapper" id="giscus-{{ post_id }}" data-term="douban-{{ post_id }}" style="display:none;">
                                <div class="giscus-loading">
                                    <div class="giscus-loading-spinner"></div>
                                    <span>加载评论中...</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                <div class="scroll-sentinel" id="posts-sentinel"></div>
            </div>

            <!-- Blogs Tab -->
            <div class="content-panel" id="blogs-panel">
                <div class="tag-cloud-wrap" style="margin: 16px; background: #fff; border: 1px solid #eff3f4; border-radius: 16px; padding: 20px;">
                    <div class="tag-cloud-head" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div class="tag-cloud-title" style="font-weight: 700; color: #0f1419; font-size: 18px;">Article Topics</div>
                        <button id="blog-tag-cloud-clear" type="button" class="tag-cloud-clear" style="background:none; border:none; color:#1d9bf0; cursor:pointer; font-size:14px;" hidden>Clear Filter</button>
                    </div>
                    <div id="blog-tag-cloud" class="tag-cloud" style="width: 100%; height: 260px; overflow: hidden;"></div>
                </div>

                <div class="blogs-column" id="blogs-list">
                    {% assign posts = site.posts | concat: site.pages | where_exp: "p", "p.path contains 'blogs/tech/'" | sort: "date" | reverse %}
                    <script>
                    window.__BLOG_POST_TAGS__ = [{% for p in posts %}{{ p.tags | jsonify }}{% unless forloop.last %},{% endunless %}{% endfor %}];
                    </script>
                    {% for post in posts %}
                    <div class="feed-item expandable-item" data-tags="{{ post.tags | jsonify | escape }}" {% if forloop.index > 10 %}style="display:none"{% endif %}>
                        <div class="post-avatar">
                            <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau" class="lazy-avatar" loading="lazy">
                        </div>
                        <div class="post-author-line">
                            <span class="feed-meta">{{ post.date | date: "%Y-%m-%d" }}</span>
                        </div>
                        <div class="feed-content">
                            <a href="{{ post.url }}" class="blog-preview-card">
                                <div class="blog-preview-body">
                                    <div class="blog-preview-title">{{ post.title }}</div>
                                    <div class="blog-preview-excerpt">
                                        {% assign plain_content = post.content | strip_html | strip_newlines %}
                                        {{ post.subtitle | default: post.description | default: plain_content | truncate: 160 }}
                                    </div>
                                    <div class="blog-preview-footer">
                                        <svg viewBox="0 0 24 24" width="12" height="12" fill="currentColor" style="margin-right:4px; vertical-align:middle;"><path d="M11.96 14.945c-.067 0-.136-.01-.203-.027-1.13-.318-2.097-.986-2.795-1.932-.832-1.125-1.176-2.508-.968-3.893s.933-2.605 2.04-3.438c.114-.083.27-.06.353.055.082.115.06.27-.055.353-1.007.756-1.635 1.83-1.808 3.033-.19 1.258.122 2.515.877 3.535.634.86 1.513 1.468 2.474 1.74a.25.25 0 0 1-.063.494z"/><path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm0 18c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8-3.589 8-8 8z"/></svg>
                                        stuartlau.github.io
                                    </div>
                                </div>
                            </a>
                            </a>
                            <div class="post-actions" style="border-top:none; margin-top:0; padding-top:4px;">
                                <button class="action-btn share-btn" onclick="openShareModal(this.closest('.feed-item'))">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/>
                                    </svg>
                                    <span class="action-count">生成海报</span>
                                </button>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                <div class="scroll-sentinel" id="blogs-sentinel"></div>
            </div>

            <!-- Travel Tab -->
            <div class="content-panel" id="travel-panel">
                <div id="life-travel-wrap" class="life-travel-wrap" style="padding: 16px;">
                    <div class="tag-cloud-wrap" style="margin-bottom: 24px; background: #f8f9fa; border: 1px solid #eff3f4; border-radius: 16px; padding: 20px;">
                        <div class="tag-cloud-head" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                            <div class="tag-cloud-title" style="font-weight: 700; color: #0f1419; font-size: 18px;">Footprints</div>
                            <button id="life-tag-cloud-clear" type="button" class="tag-cloud-clear" style="background:none; border:none; color:#1d9bf0; cursor:pointer; font-size:14px;" hidden>Clear Filter</button>
                        </div>
                        <div id="life-tag-cloud-active" class="tag-cloud-active" style="margin-bottom: 8px; font-size: 14px; color: #536471;" hidden></div>
                        <div id="life-tag-cloud" class="tag-cloud" style="width: 100%; height: 260px; overflow: hidden;"></div>
                    </div>
                    <div id="life-travel-map" class="life-travel-map" style="width: 100%; height: 500px; border-radius: 16px; border: 1px solid #eff3f4; z-index: 1;"></div>
                </div>
            </div>

            <!-- Patents Tab -->
            <div class="content-panel" id="patents-panel">
                <div class="tag-cloud-wrap" style="margin: 16px; background: #fff; border: 1px solid #eff3f4; border-radius: 16px; padding: 20px;">
                    <div class="tag-cloud-head" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div class="tag-cloud-title" style="font-weight: 700; color: #0f1419; font-size: 18px;">Patent Topics</div>
                        <button id="patent-tag-cloud-clear" type="button" class="tag-cloud-clear" style="background:none; border:none; color:#1d9bf0; cursor:pointer; font-size:14px;" hidden>Clear Filter</button>
                    </div>
                    <div id="patent-tag-cloud-active" class="tag-cloud-active" style="margin-bottom: 8px; font-size: 14px; color: #536471;" hidden></div>
                    <div id="patent-tag-cloud" class="tag-cloud" style="width: 100%; height: 260px; overflow: hidden;"></div>
                </div>

                <div class="feed-list" id="patents-list">
                    {% assign patents = site.posts | concat: site.pages | where_exp: "p", "p.path contains 'blogs/patent/'" | sort: "date" | reverse %}
                    <script>
                    window.__PATENT_POST_TAGS__ = [{% for p in patents %}{{ p.tags | jsonify }}{% unless forloop.last %},{% endunless %}{% endfor %}];
                    </script>
                    {% for patent in patents %}
                    <div class="feed-item expandable-item" data-tags="{{ patent.tags | jsonify | escape }}" {% if forloop.index > 10 %}style="display:none"{% endif %}>
                        <div class="post-avatar">
                            <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau" class="lazy-avatar" loading="lazy">
                        </div>
                        <div class="post-owner-column" style="display: flex; flex-direction: column; gap: 4px;">
                            <span class="feed-meta js-no-relative" style="margin-left: 0; font-size: 13px; color: #536471; display: block; line-height: 1.4;">
                                {% assign p_date = patent.date | date: '%Y-%m-%d' %}
                                {% if p_date == blank %}
                                    {% assign p_path_parts = patent.path | split: '/' %}
                                    {% assign p_filename = p_path_parts | last %}
                                    {% assign p_date = p_filename | slice: 0, 10 %}
                                {% endif %}
                                {% if patent.tags contains '已授权' %}
                                    Application granted on {{ p_date }}
                                {% else %}
                                    Application filed on {{ p_date }}
                                {% endif %}
                            </span>
                        </div>
                        <div class="feed-content">
                            <a href="{{ patent.url }}" class="blog-preview-card">
                                <div class="blog-preview-body">
                                    <div class="blog-preview-title">{{ patent.title | remove: "授权专利-" | remove: "待授权专利-" | remove: "Granted Patent-" | remove: "Patent Application-" | split: "-" | last }}</div>
                                    <div class="blog-preview-excerpt">
                                        {{ patent.title | remove: "授权专利-" | remove: "待授权专利-" | remove: "Granted Patent-" | remove: "Patent Application-" | split: "-" | first }}
                                    </div>
                                    <div class="blog-preview-footer">
                                        Google Patents / WIPO Reference
                                    </div>
                                </div>
                            </a>
                            </a>
                            <div class="post-actions" style="border-top:none; margin-top:0; padding-top:4px;">
                                <button class="action-btn share-btn" onclick="openShareModal(this.closest('.feed-item'))">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                        <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/>
                                    </svg>
                                    <span class="action-count">生成海报</span>
                                </button>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            <div class="content-panel" id="douban-panel">
                <div class="tag-cloud-wrap" style="margin-bottom: 24px; background: #f8f9fa; border: 1px solid #eff3f4; border-radius: 16px; padding: 20px;">
                    <div class="tag-cloud-head" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <div class="tag-cloud-title" style="font-weight: 700; color: #0f1419; font-size: 18px;">Collection Themes</div>
                        <button id="collection-tag-cloud-clear" type="button" class="tag-cloud-clear" style="background:none; border:none; color:#1d9bf0; cursor:pointer; font-size:14px;" hidden>Clear Filter</button>
                    </div>
                    <div id="collection-tag-cloud-active" class="tag-cloud-active" style="margin-bottom: 8px; font-size: 14px; color: #536471;" hidden></div>
                    <div id="collection-tag-cloud" class="tag-cloud-container" style="min-height: 120px; position: relative;">
                        <!-- Word cloud will be rendered here via JS -->
                    </div>
                </div>

                <div class="feed-list" id="douban-list">
                    <div style="padding: 24px; text-align: center; color: #536471;">Loading media journey...</div>
                </div>
                <div class="scroll-sentinel" id="douban-sentinel"></div>
                
                {% assign douban_books = site.data.books.all | jsonify %}
                {% assign douban_movies = site.data.movies.all | jsonify %}
                {% assign douban_games = site.data.games.all | jsonify %}
                <script id="douban-data-books" type="application/json">{{ douban_books }}</script>
                <script id="douban-data-movies" type="application/json">{{ douban_movies }}</script>
                <script id="douban-data-games" type="application/json">{{ douban_games }}</script>
            </div>

            <!-- On This Day Tab -->
            <div class="content-panel" id="history-panel">
                <div class="feed-list" id="history-feed-list">
                    <div class="feed-item" style="justify-content:center; color:#536471; font-size:14px; padding:24px;">Loading...</div>
                </div>
            </div>
        </div>
    </main>

    <!-- Right Sidebar - Fixed -->
    <aside class="social-right-sidebar">
        <div class="right-sidebar-inner">
            <!-- Search Box -->
            <div class="search-widget">
                <div class="widget-title">Search</div>
                <div class="search-box">
                    <input type="text" id="sidebar-search" placeholder="Search posts...">
                </div>
            </div>
            
            <!-- On This Day -->
            <div class="history-widget">
                <div class="widget-title">On This Day</div>
                <div class="history-list" id="history-today">
                    <div class="history-item">Loading...</div>
                </div>
            </div>
            
            <!-- Social Links -->
            <div class="social-links-widget">
                <a href="https://github.com/stuartlau" target="_blank" class="social-link-item">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                    <span>GitHub</span>
                </a>
                <a href="https://www.linkedin.com/in/stuartlau" target="_blank" class="social-link-item">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                    <span>LinkedIn</span>
                </a>
                <a href="mailto:stuart8@126.com" class="social-link-item">
                    <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
                    <span>Email</span>
                </a>
            </div>
        </div>
    </aside>
</div>

<div id="lightbox">
    <div class="lightbox-backdrop" id="lb-backdrop"></div>
    <button class="lightbox-close" id="lb-close">×</button>
    <button id="lightbox-prev" class="lightbox-nav">‹</button>
    <div class="lightbox-content">
        <img id="lightbox-img" src="" alt="Zoomed view">
    </div>
    <button id="lightbox-next" class="lightbox-nav">›</button>
</div>

</div>

<!-- Share Card Modal -->
<div id="share-modal" class="share-modal">
    <div class="share-modal-container">
        <img id="share-image-preview" src="" alt="Share Preview">
        <div class="share-modal-btns">
            <button class="share-action-btn close-share-btn" onclick="closeShareModal()">取消</button>
            <button class="share-action-btn save-btn" onclick="saveShareImage()">保存海报</button>
        </div>
    </div>
</div>

<!-- Hidden Card Template for Generation -->
<div id="share-card-template">
    <div class="card-header">
        <img src="/images/douban_avatar.jpg" class="card-avatar">
        <div class="card-user-info">
            <span class="card-name">Stuart Lau</span>
            <span class="card-handle">@stuartlau</span>
        </div>
    </div>
    <div class="card-body">
        <p class="card-text"></p>
        <div class="card-media"></div>
        <div class="card-quote-wrap">
            <img src="" class="card-quote-img">
            <div class="card-quote-details">
                <div class="card-quote-title"></div>
                <div class="card-quote-subtitle"></div>
            </div>
        </div>
    </div>
    <div class="card-footer">
        <div class="card-meta">
            <span class="card-date"></span>
            <span class="card-brand">stuartlau.github.io</span>
        </div>
        <div class="card-qr-wrap">
            <div id="card-qr-canvas"></div>
        </div>
    </div>
</div>
<button id="back-to-top" class="back-to-top" onclick="scrollToTop()" aria-label="Back to top">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"></polyline>
    </svg>
</button>

<style>
/* Twitter-style Layout */
* {
    box-sizing: border-box;
}

.social-layout {
    position: relative;
    display: flex;
    justify-content: center;
    min-height: 100vh;
    background: #fff;
}

/* Left Sidebar - Fixed to left */
.social-left-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 275px;
    height: 100vh;
    padding: 12px 24px;
    background: #fff;
    z-index: 1000;
    border-right: 1px solid #eff3f4;
    overflow-y: auto;
}

.left-sidebar-inner {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.sidebar-logo-text {
    display: block;
    margin-bottom: 20px;
    padding: 12px;
    font-size: 20px;
    font-weight: 900;
    color: #0f1419;
    text-decoration: none;
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.sidebar-nav .nav-item {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 12px 16px;
    border-radius: 30px;
    color: #0f1419;
    text-decoration: none;
    font-size: 18px;
    font-weight: 400;
    transition: background 0.2s;
}

.sidebar-nav .nav-item:hover {
    background: #f7f9f9;
}

.sidebar-nav .nav-item span {
    font-weight: 500;
}

/* Main Content - Centered */
.social-main {
    flex: 1;
    width: calc(100% - 275px - 350px);
    min-width: 0;
    max-width: 680px;
    margin-left: 275px;
    margin-right: 350px;
    background: #fff;
    border-right: 1px solid #eff3f4;
    border-left: 1px solid #eff3f4;
}

/* Left Sidebar - Fixed */
.social-left-sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: 275px;
    height: 100vh;
    padding: 12px 24px;
    background: #fff;
    z-index: 1000;
    border-right: 1px solid #eff3f4;
    overflow-y: auto;
}

/* Right Sidebar - Fixed */
.social-right-sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: 350px;
    height: 100vh;
    padding: 12px 24px;
    background: #fff;
    overflow-y: auto;
    border-left: 1px solid #eff3f4;
    z-index: 1000;
}

/* Responsive */
@media (max-width: 1400px) {
    .social-right-sidebar {
        width: 300px;
    }

    .social-main {
        width: calc(100% - 275px - 300px);
        margin-right: 300px;
    }
}

@media (max-width: 1200px) {
    .social-right-sidebar {
        display: none;
    }

    .social-main {
        width: calc(100% - 275px);
        margin-right: 0;
        max-width: none;
    }
}

@media (max-width: 900px) {
    .social-left-sidebar {
        width: 80px;
        padding: 12px 8px;
    }

    .sidebar-logo-text {
        display: none;
    }

    .sidebar-nav .nav-item {
        justify-content: center;
        padding: 12px;
    }

    .sidebar-nav .nav-item span {
        display: none;
    }

    .social-main {
        width: calc(100% - 80px);
        margin-left: 80px;
    }
}

@media (max-width: 768px) {
    .social-left-sidebar, .social-right-sidebar {
        display: none !important;
    }

    .social-layout {
        display: block;
        padding: 0 8px;
    }

    .social-main {
        width: 100%;
        margin-left: 0;
        min-width: 0;
        border: none;
    }
    
    .profile-header {
        margin: 0 -8px;
        width: calc(100% + 16px);
    }
    
    /* Ensure content tabs and feed items respect the padding */
    .content-tabs {
        margin-left: 0;
        margin-right: 0;
    }
    
    .feed-item {
        padding-left: 0;
        padding-right: 0;
    }
}

/* Profile Header - Twitter Style */
.profile-header {
    position: relative;
    border-bottom: 1px solid #eff3f4;
}

/* Cover Image - Dynamic background from Unsplash */
.profile-cover {
    width: 100%;
    height: 200px;
    overflow: hidden;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-image: url('https://source.unsplash.com/featured/1200x400/?nature,landscape,travel');
    background-size: cover;
    background-position: center;
}

.profile-cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* Profile Info Container - Block layout (text below avatar) */
.profile-info-container {
    padding: 0 16px 16px;
    position: relative;
    min-height: 70px;
}

/* Avatar - Overlapping Cover */
.profile-avatar {
    position: absolute;
    top: -50px; /* Position so half shows in cover, half in content area */
    left: 16px;
}

.profile-avatar img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    border: 4px solid #fff;
    background: #fff;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Profile Details - Positioned below avatar */
.profile-details {
    padding-top: 76px; /* Use padding instead of margin to prevent CSS margin collapse */
    margin-top: 0;
    padding-left: 0;
    text-align: left;
}

.profile-name {
    font-size: 20px;
    font-weight: 800;
    color: #0f1419;
    margin: 0 0 2px 0;
}

.profile-handle {
    color: #536471;
    font-size: 15px;
    margin: 0 0 10px 0;
}

/* Bio items - grid layout with icons */
.profile-bio-items {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 12px;
    margin-bottom: 10px;
}

.bio-item {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    color: #536471;
    padding: 3px 8px;
    background: rgba(0, 0, 0, 0.04);
    border-radius: 12px;
}

.bio-item svg {
    flex-shrink: 0;
    opacity: 0.7;
}

[data-theme="dark"] .bio-item {
    background: rgba(255, 255, 255, 0.08);
    color: #8b98a5;
}

.profile-bio {
    color: #0f1419;
    font-size: 15px;
    line-height: 1.5;
    margin: 0 0 12px 0;
}

.profile-meta {
    display: flex;
    gap: 20px;
    color: #536471;
    font-size: 14px;
    margin-bottom: 12px;
}

.profile-meta span {
    display: flex;
    align-items: center;
    gap: 6px;
}

.profile-stats {
    display: flex;
    gap: 24px;
}

.profile-stats a {
    color: #536471;
    font-size: 15px;
    text-decoration: none;
}

.profile-stats a:hover .stat-value {
    text-decoration: underline;
}

.profile-stats .stat-value {
    font-weight: 700;
    color: #0f1419;
}

/* Content Tabs */
.tab-icon-mobile {
    display: none; /* Hidden by default on PC */
}

.content-tabs {
    display: flex;
    background: #fff;
    border-bottom: 1px solid #eff3f4;
    position: sticky;
    top: 0;
    z-index: 50;
    width: 100%;
    flex-shrink: 0;
}

@media (max-width: 768px) {
    .content-tabs {
        overflow-x: auto;
        white-space: nowrap;
        justify-content: flex-start;
        -webkit-overflow-scrolling: touch;
        padding-bottom: 2px;
        scrollbar-width: none; /* Firefox */
    }
    .content-tabs::-webkit-scrollbar {
        display: none; /* Chrome/Safari */
    }

    .tab-item {
        flex: 0 0 auto;
        min-width: 70px;
        padding: 12px 16px;
    }

    /* Keep using text on mobile, just horizontal scroll */
    .tab-text {
        display: inline !important;
    }

    .tab-icon-mobile {
        display: none !important;
    }
}

.tab-item {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 10px 5px;
    text-decoration: none;
    color: #536471;
    font-size: 15px;
    transition: background 0.2s;
    position: relative;
}

.tab-item:hover {
    background: #f7f9f9;
}

.tab-item.active {
    color: #1d9bf0;
    font-weight: 700;
}

.tab-item.active svg {
    stroke: #1d9bf0;
    fill: rgba(29, 155, 240, 0.1);
}

.tab-item.active::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 60px;
    height: 4px;
    background: #1d9bf0;
    border-radius: 2px;
}

.tab-label {
    display: block;
    font-size: 10px;
    margin-top: 2px;
}

/* Content Panels */
.content-panel {
    display: none;
}

.content-panel.active {
    display: block;
}

/* Feed Items - Grid layout: avatar + author row, content below */
.feed-item {
    display: grid;
    grid-template-columns: 40px 1fr;
    grid-template-rows: auto auto;
    gap: 0 12px;
    padding: 12px 24px; /* Roomy padding for desktop */
    border-bottom: 1px solid #eff3f4;
    text-decoration: none;
    transition: background 0.2s;
}

.feed-item:hover {
    background: #f7f9f9;
}

/* Post Avatar - row 1 & 2, vertically top aligned */
.post-avatar {
    grid-column: 1;
    grid-row: 1 / span 2; /* Span both text rows */
    align-self: start;
}

.post-avatar img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

/* Author line - row 1, column 2 */
.post-author-line {
    grid-column: 2;
    grid-row: 1;
    display: flex;
    align-items: center;
    gap: 6px;
    /* Removed align-self: center to stay at the top */
}

.post-author {
    font-size: 15px;
    font-weight: 700;
    color: #0f1419;
}

.feed-meta {
    font-size: 13px;
    color: #536471;
}

/* Feed Content - row 2, strictly right column (Twitter/X style) */
.feed-content {
    grid-column: 2;
    grid-row: 2;
    min-width: 0;
    margin: 0;
    padding: 0;
}

.feed-text {
    font-size: 15px;
    line-height: 1.5;
    color: #0f1419;
    margin: 0;
    padding: 0;
    word-break: break-all;
}

.feed-text.collapsed {
    display: -webkit-box;
    -webkit-line-clamp: 6;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.expand-btn {
    color: #8b98a5; /* Subtle gray */
    background: none;
    border: none;
    padding: 0;
    font-size: 14px;
    cursor: pointer;
    margin-top: 4px;
    font-weight: 500;
}

.feed-content a {
    color: #536471;
    text-decoration: none;
}

.feed-content a:hover {
    text-decoration: underline;
}

.expand-btn:hover {
    text-decoration: underline;
}

.feed-title {
    font-size: 15px;
    font-weight: 700;
    color: #0f1419;
    margin: 0 0 4px 0;
}

/* X-Style Blog Preview Card */
.blog-preview-card {
    display: block;
    text-decoration: none;
    margin-top: 4px;
    border: 1px solid #eff3f4;
    border-radius: 12px;
    overflow: hidden;
    transition: background 0.2s;
    background: #fff;
}

.blog-preview-card:hover {
    background: #f7f9f9;
}

.blog-preview-body {
    padding: 12px;
}

.blog-preview-title {
    font-size: 15px;
    font-weight: 700;
    color: #0f1419;
    margin-bottom: 2px;
    line-height: 1.3;
}

.blog-preview-excerpt {
    font-size: 14px;
    color: #536471;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 4px;
}

.blog-preview-footer {
    font-size: 13px;
    color: #536471;
    display: flex;
    align-items: center;
}

.feed-excerpt {
    font-size: 14px;
    color: #536471;
    margin: 0 0 4px 0;
    line-height: 1.4;
}

.feed-comment {
    font-size: 13px;
    color: #536471;
    margin: 4px 0 0 0;
    font-style: italic;
}

.feed-cover {
    width: 60px;
    height: 85px;
    object-fit: cover;
    border-radius: 6px;
    flex-shrink: 0;
    opacity: 0;
    transition: opacity 0.3s ease;
}

.feed-cover.loaded {
    opacity: 1;
}

.feed-cover-placeholder {
    width: 60px;
    height: 85px;
    background: linear-gradient(135deg, #f0f0f0 0%, #e0e0e0 100%);
    border-radius: 6px;
    flex-shrink: 0;
    display: flex;
    justify-content: center;
    align-items: center;
}

.cover-loading-spinner {
    width: 20px;
    height: 20px;
    border: 2px solid #e0e0e0;
    border-top-color: #1d9bf0;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

/* Post Actions */
/* Post Actions */
.post-actions {
    display: flex;
    gap: 16px;
    margin-top: 6px;
    padding-top: 0;
}

.action-btn {
    display: flex;
    align-items: center;
    gap: 5px;
    background: none;
    border: none;
    color: #536471;
    cursor: pointer;
    padding: 4px 8px;
    margin-left: -8px; /* Align slightly left to match text logic */
    border-radius: 16px;
    font-size: 12px;
    transition: all 0.2s;
}

.action-btn:hover {
    background: rgba(29, 155, 240, 0.1);
    color: #1d9bf0;
}

.action-btn:hover svg {
    stroke: #1d9bf0;
}

.action-btn.active {
    color: #1d9bf0;
}

.action-btn.active svg {
    stroke: #1d9bf0;
    fill: rgba(29, 155, 240, 0.2);
}

.like-btn:hover {
    background: rgba(249, 24, 128, 0.1);
    color: #f91880;
}

.like-btn:hover svg {
    stroke: #f91880;
}

.like-btn.active {
    color: #f91880;
}

.like-btn.active svg {
    stroke: #f91880;
    fill: rgba(249, 24, 128, 0.3);
}

.action-count {
    font-weight: 500;
}

/* Giscus Wrapper for Posts */
.post-giscus-wrapper {
    margin-top: 12px;
    padding: 16px;
    background: #f7f9f9;
    border-radius: 12px;
    border: 1px solid #eff3f4;
}

.giscus-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    padding: 20px;
    color: #536471;
    font-size: 14px;
}

.giscus-loading-spinner {
    width: 20px;
    height: 20px;
    border: 2px solid #e0e0e0;
    border-top-color: #1d9bf0;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

/* Buttons with data show count prominently */
.action-btn.has-data {
    color: #0f1419;
    font-weight: 600;
}

.action-btn.has-data .action-count {
    background: rgba(29, 155, 240, 0.1);
    padding: 2px 8px;
    border-radius: 10px;
    color: #1d9bf0;
}

.like-btn.has-data .action-count {
    background: rgba(249, 24, 128, 0.1);
    color: #f91880;
}

/* Blog Cards */
.blog-card-wide {
    text-decoration: none;
    background: #fff;
    border-bottom: 1px solid #eff3f4;
    transition: background 0.2s;
    display: block;
}

.blog-card-wide:hover {
    background: #f7f9f9;
}

.blog-card-content {
    padding: 16px 20px;
}

.blog-card-title {
    font-size: 16px;
    font-weight: 700;
    color: #0f1419;
    margin-bottom: 8px;
}

.blog-card-excerpt {
    font-size: 14px;
    color: #536471;
    line-height: 1.5;
    margin-bottom: 8px;
}

.blog-card-date {
    font-size: 13px;
    color: #8b98a5;
}

/* Media Grid */
.media-section {
    padding: 16px 20px;
    border-bottom: 1px solid #eff3f4;
}

.media-section h3 {
    font-size: 16px;
    font-weight: 700;
    color: #0f1419;
    margin: 0 0 12px 0;
}

.media-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
}

.media-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none;
    width: 80px;
}

.media-item img {
    width: 70px;
    height: 100px;
    object-fit: cover;
    border-radius: 6px;
    margin-bottom: 6px;
}

.media-item span {
    font-size: 11px;
    color: #536471;
    text-align: center;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    width: 100%;
}

/* Scroll Sentinel for Infinite Scroll */
.scroll-sentinel {
    width: 100%;
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: linear-gradient(to bottom, transparent, #f7f9f9 20%);
}

.scroll-sentinel.loading::after {
    content: '';
    width: 24px;
    height: 24px;
    border: 3px solid #e0e0e0;
    border-top-color: #1d9bf0;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

.scroll-sentinel.end::after {
    content: 'No more content';
    color: #536471;
    font-size: 13px;
}

/* Social Image Grid */
.social-image-grid {
    display: flex !important;
    gap: 8px;
    margin-top: 8px;
    overflow-x: auto;
    padding-bottom: 8px;
    scrollbar-width: thin; /* Firefox */
}

/* Custom Scrollbar for Chrome/Safari/Webkit */
.social-image-grid::-webkit-scrollbar {
    height: 6px;
}

.social-image-grid::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
}

.social-image-grid::-webkit-scrollbar-thumb {
    background: #ccc;
    border-radius: 3px;
}

.social-image-grid::-webkit-scrollbar-thumb:hover {
    background: #bbb;
}

.grid-img-wrap {
    width: 120px;
    height: 120px;
    border-radius: 8px;
    overflow: hidden;
    cursor: zoom-in;
    position: relative;
    flex-shrink: 0; /* Prevent shrinking in flex container */
}

.social-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    transition: transform 0.2s, opacity 0.3s ease;
    opacity: 0;
}

.social-img.loaded {
    opacity: 1;
}

.grid-img-wrap:hover .social-img {
    transform: scale(1.05);
}

/* Image Lazy Loading Styles */
.img-placeholder {
    width: 100%;
    height: 100%;
    min-height: 120px;
    background: linear-gradient(135deg, #f0f0f0 0%, #e0e0e0 100%);
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 8px;
}

.img-loading-spinner {
    width: 30px;
    height: 30px;
    border: 3px solid #e0e0e0;
    border-top-color: #1d9bf0;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.lazy-avatar {
    opacity: 0;
    transition: opacity 0.3s ease;
}

.lazy-avatar.loaded {
    opacity: 1;
}

/* Fade in animation for loaded images */
@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

.social-img.loaded {
    animation: fadeIn 0.3s ease;
}

.more-images-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 18px;
    font-weight: 700;
    pointer-events: none;
}

/* Right Sidebar - Fixed */
.social-right-sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: 350px;
    height: 100vh;
    padding: 12px 24px;
    background: #fff;
    overflow-y: auto;
    border-left: 1px solid #eff3f4;
    z-index: 1000;
}

.right-sidebar-inner {
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding-top: 12px;
}

/* Widget Styles */
.widget-title {
    font-size: 20px;
    font-weight: 800;
    color: #0f1419;
    margin-bottom: 12px;
}

/* Search Widget */
.search-widget {
    background: #f7f9f9;
    border-radius: 16px;
    padding: 16px;
}

.search-box {
    position: relative;
    width: 100%;
}

.search-box input {
    width: 100%;
    padding: 12px 20px;
    background: #eff3f4;
    border: 1px solid transparent;
    border-radius: 30px;
    font-size: 15px;
    outline: none;
    transition: all 0.2s;
}
input:focus {
    border-color: #1d9bf0;
}

.search-box button {
    padding: 12px 16px;
    background: #1d9bf0;
    color: #fff;
    border: none;
    border-radius: 20px;
    cursor: pointer;
    transition: background 0.2s;
}

.search-box button:hover {
    background: #1a8cd8;
}

/* History Widget */
.history-widget {
    background: #f7f9f9;
    border-radius: 16px;
    padding: 16px;
}

.history-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.history-item {
    padding: 12px;
    background: #fff;
    border-radius: 8px;
    font-size: 14px;
    line-height: 1.5;
    color: #0f1419;
}

.history-item a {
    color: #1d9bf0;
    text-decoration: none;
}

.history-item a:hover {
    text-decoration: underline;
}

/* Social Links Widget */
.social-links-widget {
    background: #f7f9f9;
    border-radius: 16px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.social-link-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: #fff;
    border-radius: 8px;
    color: #0f1419;
    text-decoration: none;
    font-size: 15px;
    font-weight: 500;
    transition: background 0.2s;
}

.social-link-item:hover {
    background: #eff3f4;
}

/* Prevent scroll when lightbox open on mobile/iOS */
body.lightbox-open {
    overflow: hidden !important;
}

/* Lightbox - Non-fullscreen popup style */
#lightbox {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 10000;
    -webkit-tap-highlight-color: transparent;
}

.lightbox-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    cursor: zoom-out;
}

#lightbox.loading::after {
    content: '';
    position: absolute;
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.lightbox-content {
    position: relative;
    max-width: 85%;
    max-height: 85%;
    cursor: zoom-out; /* iOS click fix */
}

#lightbox-img {
    max-width: 100%;
    max-height: 80vh;
    border-radius: 8px;
    object-fit: contain;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    cursor: zoom-out;
    opacity: 0;
    transform: scale(0.98);
    transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

#lightbox-img.loaded {
    opacity: 1;
    transform: scale(1);
}

.lightbox-switching #lightbox-img {
    opacity: 0;
    transform: scale(0.96);
}

.lightbox-close {
    position: fixed;
    top: 20px;
    right: 20px;
    background: rgba(255,255,255,0.9);
    color: #333;
    border: none;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 20px;
    font-weight: bold;
    display: flex;
    justify-content: center;
    align-items: center;
    transition: background 0.2s;
    z-index: 10002;
}

.lightbox-close:hover, .lightbox-close:active {
    background: #fff;
    color: #333;
}

.lightbox-nav {
    position: fixed;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255,255,255,0.9);
    color: #333;
    border: none;
    padding: 12px;
    cursor: pointer;
    font-size: 20px;
    border-radius: 50%;
    transition: background 0.2s;
    width: 44px;
    height: 44px;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 10002;
}

.lightbox-nav:hover, .lightbox-nav:active {
    background: #fff;
    color: #333;
}

#lightbox-prev {
    left: 16px;
}

#lightbox-next {
    right: 16px;
}

.lightbox-counter {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    color: #fff;
    background: rgba(0, 0, 0, 0.6);
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 500;
    z-index: 10002;
}

@media (max-width: 768px) {
    .lightbox-content {
        max-width: 95%;
        max-height: 90%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    #lightbox-img {
        max-width: 100%;
        max-height: 85vh;
        width: auto;
        height: auto;
        border-radius: 0;
        object-fit: contain;
    }
    
    .lightbox-nav {
        width: 40px;
        height: 40px;
        background: rgba(0,0,0,0.4);
        color: #fff;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    @media (hover: none) {
        .lightbox-nav:hover {
            background: rgba(0,0,0,0.4);
            color: #fff;
        }
    }
    .lightbox-nav:active, .lightbox-close:active {
        background: rgba(255,255,255,0.8);
        color: #333;
    }
    
    #lightbox-prev {
        left: 8px;
    }
    
    #lightbox-next {
        right: 8px;
    }
    
    .lightbox-close {
        top: 16px;
        right: 16px;
        background: rgba(0,0,0,0.5);
        color: #fff;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .lightbox-counter {
        bottom: 20px;
        background: rgba(0,0,0,0.5);
    }
}

/* Post Header (Twitter-like) */
.post-author-line {
    display: flex;
    align-items: baseline;
    gap: 6px;
    margin-bottom: 4px;
}

.post-author {
    font-weight: 700;
    font-size: 15px;
    color: var(--text-color);
}

/* Quote Card Style (Twitter-like) */
.quote-card {
    display: flex;
    border: 1px solid #cfd9de; /* Twitter border color */
    border-radius: 12px;
    overflow: hidden;
    margin-top: 8px;
    text-decoration: none;
    transition: background-color 0.2s, border-color 0.2s;
    background-color: #fff;
}

.quote-card:hover {
    background-color: rgba(0, 0, 0, 0.03);
    border-color: #bbcdd6;
}

[data-theme="dark"] .quote-card {
    border-color: #2f3336;
    background-color: transparent;
}

[data-theme="dark"] .quote-card:hover {
    background-color: rgba(255, 255, 255, 0.03);
    border-color: #3e4448;
}

.quote-media {
    width: 72px;
    min-width: 72px;
    position: relative;
    border-right: 1px solid #cfd9de;
    background-color: #f7f9f9;
}

[data-theme="dark"] .quote-media {
    border-right-color: #2f3336;
    background-color: #1a1a1a;
}

.quote-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.quote-details {
    padding: 10px;
    flex: 1;
    min-width: 0; /* Prevent flex overflow */
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.quote-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--text-color);
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.quote-subtitle {
    font-size: 13px;
    color: #536471;
    margin-bottom: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

[data-theme="dark"] .quote-subtitle {
    color: #71767b;
}

.quote-rating-row {
    display: flex;
    align-items: center;
    gap: 6px;
}

.quote-score {
    font-size: 13px;
    color: #ff9800; /* Douban orange equivalent */
    font-weight: 500;
}

/* Mobile adjustments for quote card - Show full info like PC */
@media (max-width: 480px) {
    .quote-card {
        flex-direction: row;
        padding: 10px;
    }

    .quote-media {
        width: 70px;
        height: 100px;
        min-width: 70px;
        border-right: none;
        border-bottom: none;
        border-radius: 6px;
        overflow: hidden;
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
    
    .quote-author {
        font-size: 12px;
    }
    
    .quote-rating {
        margin-top: 4px;
    }
    
    .quote-score {
        font-size: 12px;
    }
    
    [data-theme="dark"] .quote-media {
        border-color: #2f3336;
    }
    
    .quote-img {
        object-fit: cover;
        object-position: center;
    }
}


/* Back to Top Button - Mobile Only */
.back-to-top {
    display: none;
    position: fixed;
    bottom: 24px;
    left: 24px;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
    border: none;
    cursor: pointer;
    z-index: 9999;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    transition: all 0.3s ease;
    opacity: 0;
    transform: translateY(20px);
    align-items: center;
    justify-content: center;
}

.back-to-top.visible {
    opacity: 1;
    transform: translateY(0);
}

.back-to-top:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(102, 126, 234, 0.5);
}

.back-to-top:active {
    transform: translateY(0);
}

@media (max-width: 768px) {
    .back-to-top {
        display: flex;
    }
}

/* Responsive */
@media (max-width: 1280px) {
    .social-right-sidebar {
        display: none;
    }
    
    .social-main {
        margin-right: 0;
    }
}

@media (max-width: 1080px) {
    .social-left-sidebar {
        width: 80px;
        padding: 12px 8px;
    }
    
    .sidebar-logo-text {
        display: none;
    }
    
    .sidebar-nav .nav-item {
        justify-content: center;
        padding: 12px;
    }
    
    .sidebar-nav .nav-item span {
        display: none;
    }
    
    .social-main {
        margin-left: 80px;
        margin-right: 0;
    }
}

@media (max-width: 768px) {
    /* Mobile layout adjustments */
    html, body {
        width: 100% !important;
        max-width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Reset Jekyll default containers */
    #main, .article-wrap, article {
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .social-left-sidebar, .social-right-sidebar {
        display: none !important;
    }
    
    .social-layout {
        display: block;
        width: 100%;
        max-width: 100vw;
        overflow: visible; /* Allow sticky to work */
        margin: 0 !important;
        padding: 0 !important;
    }

    .social-main {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        overflow: visible; /* Allow sticky to work */
    }

    /* Profile cover should span full width */
    .profile-header, .profile-cover {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .profile-cover img {
        width: 100% !important;
    }

    /* Hide search box on mobile to save space */
    .search-widget {
        display: none !important;
    }

    .tab-text {
        display: inline !important; 
    }

    /* Show icons on mobile too */
    .tab-icon-mobile {
        display: inline-block !important;
        margin-bottom: 2px;
        vertical-align: middle;
    }
    
    #search-toggle {
        display: none !important;
    }

    .tab-item {
        padding: 12px 0;
    }
    
    .profile-header {
        /* Remove flex column center logic to keep left alignment like Twitter */
        padding: 0 !important;
    }

    .profile-info-container {
        padding: 0 8px 16px;
        display: block; 
        text-align: left;
        min-height: 70px;
    }
    
    .feed-item {
        padding: 12px 8px !important; /* Half padding for mobile */
        gap: 0 10px;
    }

    .profile-avatar {
        position: absolute;
        top: -50px;
        left: 8px;
        margin: 0;
    }

    .profile-details {
        padding-top: 76px;
        margin-top: 0;
        width: 100%;
        text-align: left;
        padding-left: 0;
    }
    
    .content-tabs {
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        z-index: 100;
        background: #fff;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        border-bottom: 1px solid #eff3f4;
    }
    
    .tab-item {
        padding: 12px 20px;
        white-space: nowrap;
    }
}

/* Share Card Modal Styles */
.share-modal {
    position: fixed;
    top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.85);
    z-index: 11000;
    display: none;
    justify-content: center;
    align-items: center;
    backdrop-filter: blur(8px);
}

.share-modal.active { display: flex; }

.share-modal-container {
    width: 90%;
    max-width: 480px;
    background: transparent;
    display: flex;
    flex-direction: column;
    align-items: center;
    animation: modalSlideUp 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}

@keyframes modalSlideUp {
    from { transform: translateY(40px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

#share-image-preview {
    width: 100%;
    border-radius: 20px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    background: #fff;
    margin-bottom: 24px;
}

.share-modal-btns {
    display: flex;
    gap: 16px;
    width: 100%;
}

.share-action-btn {
    flex: 1;
    padding: 14px;
    border-radius: 50px;
    border: none;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.save-btn { background: #1d9bf0; color: #fff; }
.save-btn:hover { background: #1a8cd8; }
.close-share-btn { background: rgba(255,255,255,0.1); color: #fff; border: 1px solid rgba(255,255,255,0.2); }
.close-share-btn:hover { background: rgba(255,255,255,0.2); }

/* Hidden Card Template */
#share-card-template {
    position: fixed;
    left: -9999px;
    top: 0;
    width: 600px;
    background: #fff;
    padding: 40px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    color: #1a1a1a;
    font-family: 'Inter', system-ui, sans-serif;
}

.card-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 30px;
}

.card-avatar { width: 64px; height: 64px; border-radius: 50%; border: 2px solid #eff3f4; }
.card-user-info { display: flex; flex-direction: column; }
.card-name { font-size: 20px; font-weight: 800; }
.card-handle { font-size: 15px; color: #536471; }

.card-body { flex: 1; margin-bottom: 40px; }
.card-text { font-size: 24px; line-height: 1.5; font-weight: 400; margin-bottom: 24px; word-break: break-word; }
.card-media { margin-bottom: 24px; border-radius: 16px; overflow: hidden; max-height: 400px; border: 1px solid #eff3f4; }
.card-media img { width: 100%; height: auto; display: block; }

.card-quote-wrap {
    border: 1px solid #eff3f4;
    border-radius: 16px;
    padding: 16px;
    display: flex;
    gap: 16px;
    background: #f7f9f9;
}
.card-quote-img { width: 80px; height: 110px; border-radius: 8px; object-fit: cover; }
.card-quote-details { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.card-quote-title { font-size: 18px; font-weight: 700; margin-bottom: 6px; }
.card-quote-subtitle { font-size: 14px; color: #536471; }

.card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 30px;
    border-top: 1px solid #eff3f4;
}
.card-meta { display: flex; flex-direction: column; gap: 4px; }
.card-date { font-size: 14px; color: #536471; }
.card-brand { font-size: 16px; font-weight: 700; color: #1d9bf0; }
.card-qr-wrap { text-align: center; }
#card-qr-canvas { width: 80px; height: 80px; }
</style>

<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const tabItems = document.querySelectorAll('.tab-item');
    const panels = document.querySelectorAll('.content-panel');

    tabItems.forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            var targetTab = this.getAttribute('data-tab');
            tabItems.forEach(function(tab) { tab.classList.remove('active'); });
            this.classList.add('active');
            panels.forEach(function(panel) {
                panel.classList.remove('active');
            });
            const activePanel = document.getElementById(targetTab + '-panel');
            if (activePanel) activePanel.classList.add('active');
            history.pushState(null, null, '#' + targetTab);
            
            // Handle Travel & Patent Tab specific logic
            if (targetTab === 'travel') {
                if (window._travelMap && window._travelMap.invalidateSize) {
                    setTimeout(() => window._travelMap.invalidateSize(), 150);
                } else if (typeof initTravelComponent === 'function') {
                    initTravelComponent();
                }
            } else if (targetTab === 'patents') {
                setTimeout(initPatentCloud, 100);
            } else if (targetTab === 'blogs') {
                setTimeout(initBlogCloud, 100);
            } else if (targetTab === 'douban') {
                setTimeout(initCollectionCloud, 100);
            }
            
            // Check text overflow for the newly active tab
            setTimeout(checkTextOverflow, 50);
            
            // Trigger lazy loading for images in the newly active panel
            setTimeout(function() {
                if (typeof reobserveLazyImages === 'function') {
                    reobserveLazyImages();
                }
            }, 50);
        });
    });

    // Hourly Persisted Cover Image
    const coverImgEl = document.getElementById('cover-img');
    if (coverImgEl) {
        const now = new Date();
        const hourlySeed = now.getFullYear() + '-' + now.getMonth() + '-' + now.getDate() + '-' + now.getHours();
        coverImgEl.src = `https://picsum.photos/seed/social-${hourlySeed}/1200/400`;
        coverImgEl.style.cursor = 'pointer';
        coverImgEl.addEventListener('load', function() {
            this.dataset.finalSrc = this.src;
        });
        coverImgEl.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const src = this.dataset.finalSrc || this.src;
            if (src && src !== window.location.href) openLightbox(src);
        });
        coverImgEl.onerror = function() {
            this.style.display = 'none';
        };
    }

    if (window.location.hash) {
        var hash = window.location.hash.slice(1);
        var activeTab = document.querySelector('.tab-item[data-tab="' + hash + '"]');
        if (activeTab) activeTab.click();
    }
    
    // Load "On This Day" content
    loadHistoryToday();
    
    // Back to Top Button - show/hide on scroll
    const backToTopBtn = document.getElementById('back-to-top');
    if (backToTopBtn) {
        let lastScrollY = 0;
        window.addEventListener('scroll', function() {
            const scrollY = window.scrollY || window.pageYOffset;
            if (scrollY > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
            lastScrollY = scrollY;
        }, { passive: true });
    }
});

// Scroll to top function
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Search functionality - use existing search modal
function performSearch() {
    const searchModal = document.getElementById('search-modal');
    const searchToggle = document.getElementById('search-toggle');
    if (searchModal && searchToggle) {
        // Only trigger modal if hidden
        if (searchModal.hasAttribute('hidden')) {
            searchToggle.click();
        }
        
        const query = document.getElementById('sidebar-search').value.trim();
        if (query) {
            setTimeout(() => {
                const searchInput = document.getElementById('search-input');
                if (searchInput) {
                    searchInput.value = query;
                    searchInput.dispatchEvent(new Event('input'));
                    searchInput.focus();
                }
            }, 200);
        }
    }
}

// Allow Enter key in search box
document.addEventListener('DOMContentLoaded', function() {
    const sidebarSearch = document.getElementById('sidebar-search');
    if (sidebarSearch) {
        sidebarSearch.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
});

// Convert absolute time to relative time (e.g., "2026-01-16 14:30" -> "1 day" or "23h")
function getRelativeTime(timeStr) {
    if (!timeStr) return timeStr;
    
    const postTime = new Date(timeStr);
    const now = new Date();
    const diffMs = now - postTime;
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
    
    if (diffMinutes < 60) {
        return diffMinutes + 'm';
    } else if (diffHours < 24) {
        return diffHours + 'h';
    } else if (diffDays <= 7) {
        return diffDays + ' day' + (diffDays > 1 ? 's' : '');
    } else {
        // Return original format for posts older than 7 days
        return timeStr.split(' ')[0]; // Just the date part
    }
}

// Apply relative time to all feed meta elements after page load
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        document.querySelectorAll('.feed-meta:not(.js-no-relative)').forEach(el => {
            const originalTime = el.textContent.trim();
            if (originalTime.match(/\d{4}-\d{2}-\d{2}/)) {
                const relativeTime = getRelativeTime(originalTime);
                if (relativeTime !== originalTime) {
                    el.setAttribute('title', originalTime); // Keep original as tooltip
                    el.textContent = relativeTime;
                }
            }
        });
    }, 500);

    // Initialize true lazy loading for images using data-src
    initImageLazyLoading();

    // Initialize avatar lazy loading
    initAvatarLazyLoading();

    // Initialize infinite scroll
    initInfiniteScroll();

    // Load Douban content
    loadDoubanContent();

    // Check text overflow on initial load
    setTimeout(checkTextOverflow, 800);
});

// Global image lazy loading observer
let imageLazyObserver = null;

// True Image Lazy Loading - only loads images when visible
function initImageLazyLoading() {
    if (!('IntersectionObserver' in window)) {
        // Fallback: load all images immediately for older browsers
        loadAllImages();
        return;
    }

    imageLazyObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                
                // Check if we're observing a wrapper (.grid-img-wrap or .quote-media) or an image directly
                if (target.classList.contains('grid-img-wrap') || target.classList.contains('quote-media')) {
                    // It's a wrapper, load the image stored in _lazyImg
                    const img = target._lazyImg;
                    if (img && img.dataset.src) {
                        loadLazyImage(img);
                    }
                } else {
                    // It's a direct image (feed-cover)
                    loadLazyImage(target);
                }
                
                imageLazyObserver.unobserve(target);
            }
        });
    }, { 
        rootMargin: '200px 0px', // Start loading 200px before visible
        threshold: 0 
    });

    // Only observe images that are currently visible (not display:none)
    observeVisibleLazyImages();
}

// Load a single lazy image
function loadLazyImage(img) {
    const src = img.dataset.src;
    if (!src) return;
    
    // Set loading state
    img.onload = function() {
        this.classList.add('loaded');
        // Hide the placeholder (check for various placeholder types)
        const placeholder = this.previousElementSibling;
        if (placeholder && (
            placeholder.classList.contains('img-placeholder') || 
            placeholder.classList.contains('feed-cover-placeholder')
        )) {
            placeholder.style.display = 'none';
        }
    };
    
    img.onerror = function() {
        // Hide placeholder on error too
        const placeholder = this.previousElementSibling;
        if (placeholder) placeholder.style.display = 'none';
        // Hide the broken image
        this.style.display = 'none';
    };
    
    // Start loading
    img.src = src;
    img.removeAttribute('data-src');
}

// Load all images (fallback for older browsers)
function loadAllImages() {
    document.querySelectorAll('.lazy-img[data-src]').forEach(img => {
        loadLazyImage(img);
    });
}

// Observe only visible lazy images (not display:none items, and in active panel)
function observeVisibleLazyImages() {
    if (!imageLazyObserver) return;
    
    // For images inside .grid-img-wrap (Posts), observe the wrapper instead
    // because the img itself has tiny dimensions before loading
    document.querySelectorAll('.grid-img-wrap').forEach(wrap => {
        const img = wrap.querySelector('.lazy-img[data-src]');
        if (!img) return;
        
        // Check if in active panel
        const panel = wrap.closest('.content-panel');
        if (panel && !panel.classList.contains('active')) return;
        
        // Check if parent item is visible
        const feedItem = wrap.closest('.expandable-item') || wrap.closest('.feed-item');
        if (feedItem && feedItem.style.display === 'none') return;
        
        // Store reference to the image on the wrapper
        wrap._lazyImg = img;
        imageLazyObserver.observe(wrap);
    });
    
    // For Quote Cards (Books, Movies, Games), observe the media wrapper
    document.querySelectorAll('.quote-media').forEach(wrap => {
        const img = wrap.querySelector('.lazy-img[data-src]');
        if (!img) return;

        // Check if in active panel
        const panel = wrap.closest('.content-panel');
        if (panel && !panel.classList.contains('active')) return;

        // Check if parent item is visible
        const feedItem = wrap.closest('.expandable-item') || wrap.closest('.feed-item');
        if (feedItem && feedItem.style.display === 'none') return;
        
        // Ensure no-zoom is added
        if (!img.classList.contains('no-zoom')) {
            img.classList.add('no-zoom');
        }

        // Store reference
        wrap._lazyImg = img;
        imageLazyObserver.observe(wrap);
    });
}

// Re-observe newly visible images (called after loadMore or tab switch)
function reobserveLazyImages() {
    if (!imageLazyObserver) {
        loadAllImages();
        return;
    }
    observeVisibleLazyImages();
}

// Avatar Lazy Loading
function initAvatarLazyLoading() {
    const avatarObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.classList.add('loaded');
                avatarObserver.unobserve(img);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.lazy-avatar').forEach(img => {
        avatarObserver.observe(img);
    });
}

// Prevent avatar images from being zoomable
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.post-avatar img, .profile-avatar img, .sidebar-logo img').forEach(img => {
        img.style.cursor = 'default';
        img.addEventListener('click', function(e) {
            e.stopPropagation();
            e.preventDefault();
        });
    });
});

// Check for text overflow and add Expand/Collapse button
function checkTextOverflow() {
    document.querySelectorAll('.feed-text:not([data-expand-init])').forEach(el => {
        // Check character length first (threshold: 150)
        const charCount = el.textContent.trim().length;
        if (charCount < 150) {
             el.dataset.expandInit = 'true';
             return;
        }

        // Clone to calculate actual height
        const clone = el.cloneNode(true);
        clone.style.visibility = 'hidden';
        clone.style.position = 'absolute';
        clone.style.width = el.offsetWidth + 'px';
        clone.style.lineHeight = '1.5';
        clone.style.webkitLineClamp = 'none';
        clone.style.display = 'block';
        document.body.appendChild(clone);
        
        const fullHeight = clone.offsetHeight;
        const lineHeight = parseFloat(getComputedStyle(el).lineHeight);
        const maxHeight = lineHeight * 6.5; 
        
        document.body.removeChild(clone);

        if (fullHeight > maxHeight) {
            el.classList.add('collapsed');
            const btn = document.createElement('button');
            btn.className = 'expand-btn';
            btn.textContent = '...全文';
            btn.onclick = (e) => {
                e.preventDefault();
                e.stopPropagation();
                el.classList.remove('collapsed');
                btn.remove();
            };
            el.parentNode.insertBefore(btn, el.nextSibling);
        }
        el.dataset.expandInit = 'true';
    });
}

// --- Share Card Logic ---
function openShareModal(target) {
    const modal = document.getElementById('share-modal');
    const preview = document.getElementById('share-image-preview');
    const container = document.getElementById('share-card-template');
    
    // Clear previous
    preview.src = '';
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Extract content
    let feedItem = (typeof target === 'string') 
        ? document.querySelector(`[data-post-id="${target}"]`)
        : target;
    
    if (!feedItem) return;

    const name = "Stuart Lau";
    const handle = "@stuartlau";
    const date = feedItem.querySelector('.feed-meta').getAttribute('title') || feedItem.querySelector('.feed-meta').textContent;
    const text = feedItem.querySelector('.feed-text') ? feedItem.querySelector('.feed-text').textContent : '';
    
    // Handle Images
    const imgGrid = feedItem.querySelector('.social-image-grid');
    let firstImg = '';
    if (imgGrid) {
        const firstImgEl = imgGrid.querySelector('img');
        if (firstImgEl) firstImg = firstImgEl.dataset.src || firstImgEl.src;
    }

    // Handle Quote (Book/Movie)
    const quoteCard = feedItem.querySelector('.quote-card');
    let quoteData = null;
    if (quoteCard) {
        quoteData = {
            title: quoteCard.querySelector('.quote-title') ? quoteCard.querySelector('.quote-title').textContent : '',
            subtitle: quoteCard.querySelector('.quote-subtitle') ? quoteCard.querySelector('.quote-subtitle').textContent : '',
            img: quoteCard.querySelector('.quote-img') ? (quoteCard.querySelector('.quote-img').dataset.src || quoteCard.querySelector('.quote-img').src) : ''
        };
    } else {
        // Blog/Patent Preview Card
        const blogCard = feedItem.querySelector('.blog-preview-card');
        if (blogCard) {
            quoteData = {
                title: blogCard.querySelector('.blog-preview-title').textContent,
                subtitle: blogCard.querySelector('.blog-preview-excerpt').textContent,
                img: ''
            };
        }
    }

    // Populate Template
    container.querySelector('.card-date').textContent = date;
    container.querySelector('.card-text').textContent = text;
    
    const mediaContainer = container.querySelector('.card-media');
    if (firstImg) {
        mediaContainer.style.display = 'block';
        mediaContainer.innerHTML = `<img src="${firstImg}" crossorigin="anonymous">`;
    } else {
        mediaContainer.style.display = 'none';
    }

    const quoteWrap = container.querySelector('.card-quote-wrap');
    if (quoteData) {
        quoteWrap.style.display = 'flex';
        quoteWrap.querySelector('.card-quote-title').textContent = quoteData.title;
        quoteWrap.querySelector('.card-quote-subtitle').textContent = quoteData.subtitle;
        if (quoteData.img) {
            quoteWrap.querySelector('.card-quote-img').style.display = 'block';
            quoteWrap.querySelector('.card-quote-img').src = quoteData.img;
        } else {
            quoteWrap.querySelector('.card-quote-img').style.display = 'none';
        }
    } else {
        quoteWrap.style.display = 'none';
    }

    // Generate QR Code
    const qrWrap = document.getElementById('card-qr-canvas');
    qrWrap.innerHTML = '';
    new QRCode(qrWrap, {
        text: window.location.origin + window.location.pathname + "#" + (feedItem.dataset.postId || ""),
        width: 80,
        height: 80,
        colorDark: "#1a1a1a",
        colorLight: "#ffffff"
    });

    // Capture (wait for layout & image load)
    setTimeout(() => {
        html2canvas(container, {
            useCORS: true,
            scale: 2, // Retina quality
            backgroundColor: '#ffffff'
        }).then(canvas => {
            preview.src = canvas.toDataURL('image/png');
        });
    }, 500);
}

function closeShareModal() {
    const modal = document.getElementById('share-modal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

function saveShareImage() {
    const preview = document.getElementById('share-image-preview');
    if (!preview.src) return;
    
    const link = document.createElement('a');
    link.download = `stuartlau-share-${Date.now()}.png`;
    link.href = preview.src;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}


// Load history on this day from Douban posts
function loadHistoryToday() {
    const today = new Date();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const todayStr = `${month}-${day}`;
    
    // Get all posts from the page (including hidden ones)
    const allPosts = Array.from(document.querySelectorAll('.douban-item'));
    const todayPosts = allPosts.filter(item => {
        const metaEl = item.querySelector('.feed-meta');
        if (metaEl) {
            const dateStr = metaEl.textContent.trim();
            return dateStr.includes(todayStr);
        }
        return false;
    });
    
    // --- Populate sidebar widget (desktop, limit to 3) ---
    const historyList = document.getElementById('history-today');
    if (historyList) {
        const sidebarPosts = todayPosts.slice(0, 3);
        if (sidebarPosts.length > 0) {
            historyList.innerHTML = sidebarPosts.map(post => {
                const textEl = post.querySelector('.feed-text');
                const text = textEl ? textEl.innerHTML : '';
                let imgHtml = '';
                const gridImgs = post.querySelector('.grid-images');
                if (gridImgs) {
                     const imgs = Array.from(gridImgs.querySelectorAll('img')).slice(0, 3);
                     if (imgs.length) {
                         imgHtml = `<div style="display:flex; gap:4px; margin-top:8px;">` + 
                             imgs.map(img => `<div style="width:60px; height:60px; border-radius:4px; overflow:hidden;"><img src="${img.dataset.src||img.src}" style="width:100%; height:100%; object-fit:cover;"></div>`).join('') +
                             `</div>`;
                     }
                } else {
                    const coverImg = post.querySelector('.quote-img');
                    if (coverImg) {
                        const src = coverImg.dataset.src || coverImg.src;
                        imgHtml = `<div style="margin-top:8px;"><img src="${src}" style="height:80px; width:auto; border-radius:4px;"></div>`;
                    }
                }
                const meta = post.querySelector('.feed-meta').textContent.trim();
                const yearMatch = meta.match(/\d{4}/);
                const year = yearMatch ? yearMatch[0] : meta;
                return `<div class="history-item" style="padding-bottom:12px; margin-bottom:12px; border-bottom:1px solid #eff3f4;">
                    <div style="font-size:13px; color:#536471; margin-bottom:4px; font-weight:600;">${year}</div>
                    <div style="font-size:14px; line-height:1.5;">${text}</div>
                    ${imgHtml}
                </div>`;
            }).join('');
        } else {
            historyList.innerHTML = '<div class="history-item" style="color:#536471; font-size:14px;">No memories found for today in history.</div>';
        }
    }
    
    // --- Populate Posts Tab Integrated Section ---
    const postsOtdList = document.getElementById('posts-otd-list');
    
    if (postsOtdList) {
        if (todayPosts.length > 0) {
            postsOtdList.style.display = 'block';
            postsOtdList.innerHTML = todayPosts.map(post => {
                const textEl = post.querySelector('.feed-text');
                const text = textEl ? textEl.innerHTML : '';
                const meta = post.querySelector('.feed-meta').textContent.trim();
                const yearMatch = meta.match(/\d{4}-\d{2}-\d{2}/) || meta.match(/\d{4}/);
                const dateStr = yearMatch ? yearMatch[0] : meta;
                
                // Reconstruct images/quotes
                let extraHtml = '';
                const imgGrid = post.querySelector('.social-image-grid');
                if (imgGrid) extraHtml += imgGrid.outerHTML;
                const quoteCard = post.querySelector('.quote-card');
                if (quoteCard) extraHtml += quoteCard.outerHTML;
                const blogCard = post.querySelector('.blog-preview-card');
                if (blogCard) extraHtml += blogCard.outerHTML;
                
                return `<div class="feed-item">
                    <div class="post-avatar">
                        <img src="/images/douban_avatar.jpg" alt="Stuart Lau" loading="lazy">
                    </div>
                    <div class="post-author-line">
                        <div style="font-weight:600; color:#536471; font-size:13px;">${dateStr}</div>
                    </div>
                    <div class="feed-content">
                        <p class="feed-text">${text}</p>
                        ${extraHtml}
                    </div>
                </div>`;
            }).join('');
        } else {
            postsOtdList.style.display = 'none';
        }
    }

    // --- Populate history tab panel (mobile, show all, feed-item format) ---
    const historyFeedList = document.getElementById('history-feed-list');
    if (historyFeedList) {
        if (todayPosts.length > 0) {
            historyFeedList.innerHTML = todayPosts.map(post => {
                const textEl = post.querySelector('.feed-text');
                const text = textEl ? textEl.textContent : '';
                const meta = post.querySelector('.feed-meta').textContent.trim();
                
                // Reconstruct images
                let imagesHtml = '';
                const imgGrid = post.querySelector('.social-image-grid');
                if (imgGrid) {
                    imagesHtml = imgGrid.outerHTML;
                }
                // Quote card (books/movies/games)
                const quoteCard = post.querySelector('.quote-card');
                let quoteHtml = quoteCard ? quoteCard.outerHTML : '';
                
                return `<div class="feed-item">
                    <div class="post-avatar">
                        <img src="/images/douban_avatar.jpg" alt="Stuart Lau" loading="lazy">
                    </div>
                    <div class="post-author-line">
                        <span class="post-author">@stuartlau</span>
                        <span class="feed-meta">${meta}</span>
                    </div>
                    <div class="feed-content">
                        <p class="feed-text">${text}</p>
                        ${imagesHtml}
                        ${quoteHtml}
                    </div>
                </div>`;
            }).join('');
        } else {
            historyFeedList.innerHTML = '<div class="feed-item" style="justify-content:center; color:#536471; font-size:14px; padding:24px;">今天暂无历史记录 📅</div>';
        }
    }
}

function loadDoubanContent() {
    const list = document.getElementById('douban-list');
    if (!list) return;

    try {
        const booksData = document.getElementById('douban-data-books');
        const moviesData = document.getElementById('douban-data-movies');
        const gamesData = document.getElementById('douban-data-games');

        if (!booksData || !moviesData || !gamesData) return;

        const books = JSON.parse(booksData.textContent || '[]');
        const movies = JSON.parse(moviesData.textContent || '[]');
        const games = JSON.parse(gamesData.textContent || '[]');

        let items = [];
        books.forEach(b => items.push({ date: b.read_date, type: 'Book', data: b }));
        movies.forEach(m => items.push({ date: m.watched_date, type: 'Movie', data: m }));
        games.forEach(g => items.push({ date: g.played_date, type: 'Game', data: g }));

        items.sort((a, b) => (b.date || '').localeCompare(a.date || ''));

        if (items.length === 0) {
            list.innerHTML = '<div style="padding:40px; text-align:center; color:#536471;">No media records found.</div>';
            return;
        }

        list.innerHTML = items.map((item, idx) => {
            const d = item.data;
            let quoteHtml = '';
            
            if (item.type === 'Book') {
                quoteHtml = `
                    <a href="https://book.douban.com/subject/${d.book_id}/" target="_blank" class="quote-card">
                        ${d.cover ? `<div class="quote-media"><img data-src="${d.cover}" class="quote-img lazy-img no-zoom"></div>` : ''}
                        <div class="quote-details">
                            <div class="quote-title">${d.title}</div>
                            <div class="quote-subtitle">${d.author || ''}</div>
                            <div class="quote-rating-row"><span class="rating-stars" data-score="${(d.my_rating || d.douban_rating || 0) * 2}"></span></div>
                        </div>
                    </a>`;
            } else if (item.type === 'Movie') {
                quoteHtml = `
                    <a href="https://movie.douban.com/subject/${d.movie_id}/" target="_blank" class="quote-card">
                        ${d.poster ? `<div class="quote-media"><img data-src="${d.poster}" class="quote-img lazy-img no-zoom"></div>` : ''}
                        <div class="quote-details">
                            <div class="quote-title">${d.title}</div>
                            <div class="quote-subtitle">${(d.directors || []).join(', ')}</div>
                            <div class="quote-rating-row"><span class="rating-stars" data-score="${(d.my_rating || d.douban_rating || 0) * 2}"></span></div>
                        </div>
                    </a>`;
            } else {
                quoteHtml = `
                    <a href="${d.douban_url}" target="_blank" class="quote-card">
                        ${d.cover ? `<div class="quote-media"><img data-src="${d.cover}" class="quote-img lazy-img no-zoom"></div>` : ''}
                        <div class="quote-details">
                            <div class="quote-title">${d.title}</div>
                            <div class="quote-subtitle">${(d.platforms || []).join('/')}</div>
                            <div class="quote-rating-row"><span class="rating-stars" data-score="${(d.my_rating || d.douban_rating || 0) * 2}"></span></div>
                        </div>
                    </a>`;
            }

            const itemTags = (item.type === 'Book' ? (d.tags && d.tags.length > 0 ? d.tags : [d.author, d.publisher].filter(Boolean)) : (d.genres || [])) || [];
            return `
                <div class="feed-item expandable-item" style="${idx >= 10 ? 'display:none' : ''}" data-tags='${JSON.stringify(itemTags).replace(/'/g, "&#39;")}'>
                    <div class="post-avatar">
                        <img src="/images/douban_avatar.jpg" alt="Stuart Lau" loading="lazy">
                    </div>
                    <div class="post-author-line">
                        <span class="post-author">@stuartlau</span>
                        <span class="feed-meta">${item.date || ''} · ${item.type}</span>
                    </div>
                    <div class="feed-content">
                        ${d.my_comment ? `<p class="feed-text" style="margin-bottom:12px;">${d.my_comment}</p>` : '<div style="height:4px;"></div>'}
                        ${quoteHtml}
                    </div>
                    <div class="post-actions" style="padding-left:50px;">
                        <button class="action-btn share-btn" onclick="openShareModal(this.closest('.feed-item'))">
                            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/>
                            </svg>
                            <span class="action-count">生成海报</span>
                        </button>
                    </div>
                </div>`;
        }).join('');

        list.querySelectorAll('.rating-stars').forEach(el => {
            el.innerHTML = renderStars(el.dataset.score);
        });
        
        // Generate Word Cloud Data
        const tagCounts = {};
        items.forEach(item => {
            const d = item.data;
            // Use genres for movies/games, and author/publisher as fallback for books if no tags
            const tags = (item.type === 'Book' ? (d.tags && d.tags.length > 0 ? d.tags : [d.author, d.publisher].filter(Boolean)) : (d.genres || [])) || [];
            tags.forEach(t => {
                if (t && typeof t === 'string' && t.trim()) {
                    tagCounts[t] = (tagCounts[t] || 0) + 1;
                }
            });
        });
        
        const cloudDataArr = Object.keys(tagCounts).map(name => ({
            text: name,
            size: tagCounts[name]
        })).sort((a, b) => b.size - a.size);
        
        window.__COLLECTION_POST_TAGS__ = items.map(item => {
            const d = item.data;
            return (item.type === 'Book' ? (d.tags && d.tags.length > 0 ? d.tags : [d.author, d.publisher].filter(Boolean)) : (d.genres || []));
        });
        
        initCollectionCloud(cloudDataArr);
        reobserveLazyImages();
    } catch (e) {
        console.error('Error loading Douban data', e);
        list.innerHTML = '<div style="padding:40px; text-align:center; color:red;">Failed to load media journey.</div>';
    }
}


let loadMoreState = {};

function loadMore(listId) {
    const list = document.getElementById(listId);
    if (!list) return;

    if (!loadMoreState[listId]) {
        loadMoreState[listId] = { loaded: 10, loading: false, ended: false };
    }
    const state = loadMoreState[listId];
    if (state.loading || state.ended) return;

    const sentinel = document.getElementById(listId.replace('list', 'sentinel'));
    if (sentinel) sentinel.classList.add('loading');

    state.loading = true;

    setTimeout(() => {
        const hiddenItems = Array.from(list.querySelectorAll('.expandable-item')).filter(el => el.style.display === 'none');
        
        // Find active tags for filtering
        const panelType = listId === 'patents-list' ? 'patents' : (listId === 'blogs-list' ? 'blogs' : 'collections');
        const activeTag = panelType === 'patents' ? window._activePatentTag : (panelType === 'blogs' ? window._activeBlogTag : window._activeCollectionTag);

        let shownCount = 0;
        let processedCount = 0;
        const batchSize = 10;
        
        // Always process at least N items, only showing those that match the tag
        for (let i = 0; i < hiddenItems.length && shownCount < batchSize; i++) {
            const item = hiddenItems[i];
            processedCount++;
            
            if (activeTag) {
                try {
                    const tagsStr = item.dataset.tags || '[]';
                    const tags = JSON.parse(tagsStr.replace(/&quot;/g, '"').replace(/&#39;/g, "'"));
                    if (tags.includes(activeTag)) {
                        item.style.display = '';
                        shownCount++;
                    }
                } catch(e) {
                    // Fallback for parsing errors
                }
            } else {
                item.style.display = '';
                shownCount++;
            }
        }

        state.loaded += processedCount;
        state.loading = false;
        state.ended = (processedCount >= hiddenItems.length);
        
        if (sentinel) {
            sentinel.classList.remove('loading');
            if (state.ended) sentinel.classList.add('end');
        }

        // Re-check text overflow and lazy images for newly shown items
        setTimeout(() => {
            checkTextOverflow();
            reobserveLazyImages();
        }, 100);
        
        // Trigger text overflow check
        setTimeout(checkTextOverflow, 100);
        
        // Preload stats for newly visible posts (if it's the posts list)
        if (listId === 'posts-list' && typeof preloadPostStats === 'function') {
            setTimeout(preloadPostStats, 500);
        }
    }, 300);
}

// Initialize Infinite Scroll with Intersection Observer
function initInfiniteScroll() {
    if (!('IntersectionObserver' in window)) {
        return;
    }

    const panels = ['posts', 'blogs', 'patents', 'douban'];

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const sentinel = entry.target;
                const listId = sentinel.id.replace('sentinel', 'list');
                loadMore(listId);
            }
        });
    }, {
        rootMargin: '200px 0px',
        threshold: 0
    });

    panels.forEach(panel => {
        const sentinel = document.getElementById(panel + '-sentinel');
        if (sentinel) {
            observer.observe(sentinel);
        }
    });
}
let currentImageIndex = 0;

function updateLightboxImage() {
    const lbImg = document.getElementById('lightbox-img');
    const lb = document.getElementById('lightbox');
    
    if (!lbImg) return;
    
    // Show loading state
    lbImg.classList.remove('loaded');
    lb.classList.add('loading');
    lb.classList.add('lightbox-switching');
    
    // Set up load handlers
    lbImg.onload = function() {
        // Clear any leftover inline styles so CSS classes work properly
        lbImg.style.cssText = '';
        lbImg.classList.add('loaded');
        lb.classList.remove('loading');
        lb.classList.remove('lightbox-switching');
    };
    
    lbImg.onerror = function() {
        lb.classList.remove('loading');
        lb.classList.remove('lightbox-switching');
        closeLightbox(); 
    };
    
    // Set src after a tiny delay to ensure opacity transition starts
    setTimeout(() => {
        lbImg.src = currentImages[currentImageIndex];
    }, 50);
    
    const prevBtn = document.getElementById('lightbox-prev');
    const nextBtn = document.getElementById('lightbox-next');
    if (prevBtn) prevBtn.style.display = currentImages.length > 1 ? 'flex' : 'none';
    if (nextBtn) nextBtn.style.display = currentImages.length > 1 ? 'flex' : 'none';

    // Update Counter
    let counter = document.getElementById('lightbox-counter');
    const contentWrapper = document.querySelector('.lightbox-content');
    if (!counter && contentWrapper) {
        counter = document.createElement('div');
        counter.id = 'lightbox-counter';
        counter.className = 'lightbox-counter';
        contentWrapper.appendChild(counter);
    }
    
    if (counter) {
        if (currentImages.length > 1) {
            counter.textContent = `${currentImageIndex + 1} / ${currentImages.length}`;
            counter.style.display = 'block';
        } else {
            counter.style.display = 'none';
        }
    }
}

function nextLightboxImage(e) {
    if (e) e.stopPropagation();
    currentImageIndex = (currentImageIndex + 1) % currentImages.length;
    updateLightboxImage();
}

function prevLightboxImage(e) {
    if (e) e.stopPropagation();
    currentImageIndex = (currentImageIndex - 1 + currentImages.length) % currentImages.length;
    updateLightboxImage();
}

var _lightboxClosing = false;

function closeLightbox(e) {
    if (e) {
        e.stopPropagation();
        e.preventDefault();
    }
    
    const lb = document.getElementById('lightbox');
    if (!lb) return;
    
    // Force-hide immediately
    lb.style.display = 'none';
    lb.classList.remove('loading', 'lightbox-switching');
    
    const lbImg = document.getElementById('lightbox-img');
    if (lbImg) {
        lbImg.onload = lbImg.onerror = null;
        lbImg.classList.remove('loaded');
        // Clear inline styles — let CSS base state (opacity:0) take over naturally
        lbImg.style.cssText = '';
        lbImg.src = '';
    }
    
    currentImages = [];
    
    // Force-restore body scroll
    document.body.classList.remove('lightbox-open');
    document.body.style.overflow = '';
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.width = '';
    document.documentElement.style.overflow = '';
    
    _lightboxClosing = false;
}

function openLightbox(src, galleryImages) {
    const lb = document.getElementById('lightbox');
    const lbImg = document.getElementById('lightbox-img');
    if (!lb || !lbImg) return;
    
    // If already open with same image, close (toggle)
    if (lb.style.display === 'flex' && currentImages.length === 1 && currentImages[0] === src) {
        closeLightbox();
        return;
    }
    
    _lightboxClosing = false;
    
    if (src) {
        if (galleryImages && galleryImages.length > 0) {
            currentImages = galleryImages;
            currentImageIndex = currentImages.indexOf(src);
            if (currentImageIndex === -1) {
                currentImages = [src];
                currentImageIndex = 0;
            }
        } else {
            currentImages = [src];
            currentImageIndex = 0;
        }
        
        updateLightboxImage();
        lb.style.display = 'flex';
        document.body.classList.add('lightbox-open');
    }
}

function handleLightboxInteraction(e) {
    // Nav buttons and close button have stopPropagation in their own handlers,
    // so clicks on them never reach here. Everything else closes the lightbox.
    closeLightbox(e);
}

document.addEventListener('DOMContentLoaded', function() {
    // Update OTD Tab Date
    try {
        const now = new Date();
        const mm = String(now.getMonth() + 1).padStart(2, '0');
        const dd = String(now.getDate()).padStart(2, '0');
        const label = document.getElementById('otd-tab-label');
        if (label) label.textContent = mm + '/' + dd;
    } catch(e) {}

    // --- Lightbox: Direct event handlers (no bubbling) ---
    const lb = document.getElementById('lightbox');
    const backdrop = document.getElementById('lb-backdrop');
    const lbImg = document.getElementById('lightbox-img');
    const prevBtn = document.getElementById('lightbox-prev');
    const nextBtn = document.getElementById('lightbox-next');
    const closeBtn = document.getElementById('lb-close');
    
    // Click backdrop → close
    if (backdrop) backdrop.addEventListener('click', function(e) { e.stopPropagation(); closeLightbox(); });
    
    // Click image → close
    if (lbImg) lbImg.addEventListener('click', function(e) { e.stopPropagation(); closeLightbox(); });
    
    // Click close button → close
    if (closeBtn) closeBtn.addEventListener('click', function(e) { e.stopPropagation(); closeLightbox(); });
    
    // Click content area (black strips around image) → close
    const lbContent = document.querySelector('.lightbox-content');
    if (lbContent) lbContent.addEventListener('click', function(e) {
        // Only close if not clicking a button inside
        if (e.target === lbContent) closeLightbox();
    });
    
    // Click prev/next → navigate (stopPropagation to prevent close)
    if (prevBtn) prevBtn.addEventListener('click', function(e) { e.stopPropagation(); prevLightboxImage(); });
    if (nextBtn) nextBtn.addEventListener('click', function(e) { e.stopPropagation(); nextLightboxImage(); });
    
    // Click anywhere else on lightbox container → close
    if (lb) lb.addEventListener('click', function() { closeLightbox(); });
    
    // Touch swipe support for mobile
    let touchStartX = 0;
    if (lb) {
        lb.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, {passive: true});
        lb.addEventListener('touchend', function(e) {
            const touchEndX = e.changedTouches[0].screenX;
            const diff = touchEndX - touchStartX;
            if (diff < -50) nextLightboxImage();
            else if (diff > 50) prevLightboxImage();
        }, {passive: true});
    }
});

document.addEventListener('keydown', function(e) {
    const lb = document.getElementById('lightbox');
    if (lb && lb.style.display === 'flex') {
        if (e.key === 'ArrowRight') nextLightboxImage();
        if (e.key === 'ArrowLeft') prevLightboxImage();
        if (e.key === 'Escape') closeLightbox();
    }
});

// Render Stars
function renderStars(score) {
    if (!score) return '';
    const num = parseFloat(score);
    const stars = Math.round((num / 2) * 2) / 2;
    const full = Math.floor(stars);
    const half = stars % 1 !== 0;
    const empty = 5 - Math.ceil(stars);
    
    // SVG Styling: Align middle to match text and other stars properly
    const svgAttr = 'viewBox="0 0 24 24" width="14" height="14" style="display:inline-block; vertical-align:middle; margin-top:-2px;"';
    const starPath = "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z";
    
    let html = '';
    
    // Full Stars
    for(let i=0; i<full; i++) {
        html += `<svg ${svgAttr} fill="#ffa500"><path d="${starPath}"/></svg>`;
    }
    
    // Half Star
    if(half) {
        // Use inline-flex and middle alignment for the container
        html += `<span style="position:relative; display:inline-block; width:14px; height:14px; vertical-align:middle; margin-top:-2px;">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="#e0e0e0" style="position:absolute; left:0; top:0;"><path d="${starPath}"/></svg>
            <svg viewBox="0 0 24 24" width="14" height="14" fill="#ffa500" style="position:absolute; left:0; top:0; clip-path: inset(0 50% 0 0);"><path d="${starPath}"/></svg>
        </span>`;
    }
    
    // Empty Stars
    for(let i=0; i<empty; i++) {
        html += `<svg ${svgAttr} fill="#e0e0e0"><path d="${starPath}"/></svg>`;
    }
    
    return html;
}

// Initialize Stars
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.rating-stars').forEach(el => {
        el.innerHTML = renderStars(el.dataset.score);
    });
});
// ============================================
// Post Comments & Reactions (Giscus Integration)
// ============================================

var activePostGiscus = null;
var postGiscusIframe = null;
var currentPostTerm = null;

// Preload discussion stats for visible posts
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit for the page to stabilize
    setTimeout(function() {
        preloadPostStats();
    }, 1000);
});

// Preload stats for visible posts using GitHub GraphQL API via proxy
async function preloadPostStats() {
    const visiblePosts = document.querySelectorAll('.douban-item:not([style*="display:none"])');
    
    for (const post of visiblePosts) {
        const postId = post.getAttribute('data-post-id');
        if (!postId) continue;
        
        try {
            await fetchPostStats(postId);
        } catch (e) {
            console.warn('Failed to fetch stats for:', postId, e);
        }
        
        // Small delay between requests to avoid rate limiting
        await new Promise(r => setTimeout(r, 200));
    }
}

// Fetch stats for a single post from giscus API
async function fetchPostStats(term) {
    const repo = 'stuartlau/stuartlau.github.io';
    const repoId = 'R_kgDOOf5c7g';
    const category = 'Announcements';
    const categoryId = 'DIC_kwDOOf5c7s4Cz_Oz';
    
    // Use giscus's internal API to search for discussions
    // Note: We specificly use a CORS proxy to bypass browser restrictions
    // because giscus.app does not allow direct cross-origin requests from client-side
    const apiUrl = `https://giscus.app/api/discussions?` + new URLSearchParams({
        repo: repo,
        term: term,
        category: category,
        strict: '0',
        reactionsEnabled: 'true',
        emitMetadata: 'false'
    });
    
    // Use allorigins.win as a more lenient CORS proxy
    const searchUrl = 'https://api.allorigins.win/get?url=' + encodeURIComponent(apiUrl);
    
    try {
        const response = await fetch(searchUrl, {
            method: 'GET'
            // No headers needed for this proxy
        });
        
        if (!response.ok) {
            throw new Error('Proxy request failed: ' + response.status);
        }
        
        const proxyData = await response.json();
        const data = JSON.parse(proxyData.contents); // allorigins wraps the response in 'contents'
        
        if (data && data.discussion) {
            updatePostStatsUI(term, {
                commentCount: data.discussion.totalCommentCount || 0,
                reactionCount: data.discussion.reactionCount || 0,
                reactions: data.discussion.reactions || {}
            });
        }
    } catch (e) {
        // Fallback: just show the buttons without counts or debug log
        // console.warn('Stats fetch failed for', term);
    }
}

// Update the UI with fetched stats
function updatePostStatsUI(term, stats) {
    const postId = term.replace('douban-', '');
    
    // Update comment count
    const commentEl = document.getElementById('comment-count-' + postId);
    if (commentEl && stats.commentCount > 0) {
        commentEl.textContent = stats.commentCount;
        commentEl.closest('.action-btn').classList.add('has-data');
    }
    
    // Update like count (reactions)
    const likeEl = document.getElementById('like-count-' + postId);
    if (likeEl && stats.reactionCount > 0) {
        likeEl.textContent = stats.reactionCount;
        likeEl.closest('.action-btn').classList.add('has-data');
    }
}

// Toggle giscus comments for a post
function togglePostComments(btn) {
    var postId = btn.getAttribute('data-post-id');
    var wrapper = document.getElementById('giscus-' + postId.replace('douban-', ''));
    
    if (!wrapper) {
        console.error('Giscus wrapper not found for:', postId);
        return;
    }
    
    var term = wrapper.getAttribute('data-term');
    
    // If clicking the same one that's already open, just hide it
    if (wrapper.style.display !== 'none' && wrapper.querySelector('.giscus-container')) {
        wrapper.style.display = 'none';
        btn.classList.remove('active');
        return;
    }
    
    // Hide all other giscus wrappers
    document.querySelectorAll('.post-giscus-wrapper').forEach(function(w) {
        if (w !== wrapper) {
            w.style.display = 'none';
        }
    });
    
    // Remove active state from all buttons
    document.querySelectorAll('.action-btn.active').forEach(function(b) {
        b.classList.remove('active');
    });
    
    // Show this wrapper and set button active
    wrapper.style.display = 'block';
    btn.classList.add('active');
    
    // Initialize or reuse giscus
    if (!activePostGiscus) {
        initPostGiscus(wrapper, term);
    } else {
        movePostGiscus(wrapper, term);
    }
}

function initPostGiscus(wrapper, term) {
    // Remove loading indicator
    var loading = wrapper.querySelector('.giscus-loading');
    if (loading) loading.style.display = 'none';
    
    // Create container
    activePostGiscus = document.createElement('div');
    activePostGiscus.className = 'giscus-container';
    wrapper.appendChild(activePostGiscus);
    
    currentPostTerm = term;
    
    // Create giscus script
    var script = document.createElement('script');
    script.src = "https://giscus.app/client.js";
    script.setAttribute("data-repo", "stuartlau/stuartlau.github.io");
    script.setAttribute("data-repo-id", "R_kgDOOf5c7g");
    script.setAttribute("data-category", "Announcements");
    script.setAttribute("data-category-id", "DIC_kwDOOf5c7s4Cz_Oz");
    script.setAttribute("data-mapping", "specific");
    script.setAttribute("data-term", term);
    script.setAttribute("data-strict", "0");
    script.setAttribute("data-reactions-enabled", "1");
    script.setAttribute("data-emit-metadata", "0");
    script.setAttribute("data-input-position", "top");
    script.setAttribute("data-theme", document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light');
    script.setAttribute("data-lang", "zh-CN");
    script.setAttribute("crossorigin", "anonymous");
    script.setAttribute("async", "");
    
    script.onload = function() {
        console.log('✓ Post Giscus loaded for:', term);
        setTimeout(function() {
            postGiscusIframe = activePostGiscus.querySelector('iframe.giscus-frame');
            if (postGiscusIframe) {
                console.log('✓ Post Giscus iframe found');
            }
        }, 1000);
    };
    
    activePostGiscus.appendChild(script);
}

function movePostGiscus(wrapper, term) {
    if (!activePostGiscus) return;
    
    // Remove loading indicator from new wrapper
    var loading = wrapper.querySelector('.giscus-loading');
    if (loading) loading.style.display = 'none';
    
    // Move container to new wrapper
    wrapper.appendChild(activePostGiscus);
    
    // Update term if different
    if (currentPostTerm !== term) {
        updatePostGiscusTerm(term);
    }
}

function updatePostGiscusTerm(newTerm) {
    if (!postGiscusIframe) {
        console.error('No post giscus iframe to update');
        return;
    }
    
    var currentSrc = postGiscusIframe.src;
    var newSrc = currentSrc.replace(
        /term=[^&]*/,
        'term=' + encodeURIComponent(newTerm)
    );
    
    console.log('Updating post giscus term to:', newTerm);
    postGiscusIframe.src = newSrc;
    currentPostTerm = newTerm;
}
</script>

<!-- Travel Dependencies -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3@3.5.17/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3-cloud@1/build/d3.layout.cloud.js"></script>

<script>
// Adapted Travel Init for Social Page
function initTravelComponent() {
    if (window._travelInitialized) {
        if (window._travelMap) window._travelMap.invalidateSize();
        return;
    }
    
    const wrap = document.getElementById('life-travel-wrap');
    if (!wrap) return;

    window._travelInitialized = true;
    
    // Lazy load the travel logic
    const script = document.createElement('script');
    script.src = '/assets/js/life-travel.js';
    script.onload = () => {
        console.log('✓ Travel logic loaded');
        // The script initialized itself, but we might need to invalidateSize 
        // after a delay to ensure it catches the visible container
        setTimeout(() => {
            if (window._travelMap) window._travelMap.invalidateSize();
        }, 500);
    };
    document.head.appendChild(script);
}

function initPatentCloud() {
    const cloudEl = document.getElementById('patent-tag-cloud');
    if (!cloudEl || !window.d3) return;
    
    const clearBtn = document.getElementById('patent-tag-cloud-clear');
    if (clearBtn) {
        clearBtn.onclick = () => applyFeedFilter('patents', null);
    }

    const counts = {};
    (window.__PATENT_POST_TAGS__ || []).forEach(tags => {
        (tags || []).forEach(t => {
            if (t === 'Patent') return;
            counts[t] = (counts[t] || 0) + 1;
        });
    });

    const data = Object.keys(counts).map(t => ({ text: t, size: counts[t] }));
    const width = cloudEl.clientWidth || 600;
    const height = 260;

    const sizeScale = d3.scale.linear()
        .domain([d3.min(data, d => d.size) || 1, d3.max(data, d => d.size) || 1])
        .range([12, 52]);

    const activeTag = window._activePatentTag;

    d3.layout.cloud()
        .size([width, height])
        .words(data.map(d => ({ text: d.text, size: sizeScale(d.size) })))
        .padding(5)
        .rotate(0)
        .font("Inter, system-ui, sans-serif")
        .fontSize(d => d.size)
        .on("end", words => {
            const container = d3.select("#patent-tag-cloud");
            container.selectAll("svg").remove();
            
            container.append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", `translate(${width/2},${height/2})`)
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", d => d.size + "px")
                .style("font-family", "Inter")
                .style("font-weight", d => d.text === activeTag ? "700" : "400")
                .style("fill", (d, i) => {
                    if (d.text === activeTag) return "#1d9bf0";
                    const colors = ['#1d9bf0', '#16a34a', '#dc2626', '#ca8a04', '#9333ea', '#ea580c', '#0891b2', '#be185d', '#059669', '#7c3aed'];
                    return colors[i % colors.length];
                })
                .style("cursor", "pointer")
                .attr("text-anchor", "middle")
                .attr("transform", d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
                .text(d => d.text)
                .on("click", (d) => {
                    applyFeedFilter('patents', d.text);
                });
        })
        .start();
}

function initBlogCloud() {
    const cloudEl = document.getElementById('blog-tag-cloud');
    if (!cloudEl || !window.d3) return;
    
    const clearBtn = document.getElementById('blog-tag-cloud-clear');
    if (clearBtn) {
        clearBtn.onclick = () => applyFeedFilter('blogs', null);
    }

    const counts = {};
    (window.__BLOG_POST_TAGS__ || []).forEach(tags => {
        (tags || []).forEach(t => {
            if (!t) return;
            counts[t] = (counts[t] || 0) + 1;
        });
    });

    const data = Object.keys(counts).map(t => ({ text: t, size: counts[t] }));
    const width = cloudEl.clientWidth || 600;
    const height = 260;

    const sizeScale = d3.scale.linear()
        .domain([d3.min(data, d => d.size) || 1, d3.max(data, d => d.size) || 1])
        .range([12, 52]);

    const activeTag = window._activeBlogTag;

    d3.layout.cloud()
        .size([width, height])
        .words(data.map(d => ({ text: d.text, size: sizeScale(d.size) })))
        .padding(5)
        .rotate(0)
        .font("Inter, system-ui, sans-serif")
        .fontSize(d => d.size)
        .on("end", words => {
            const container = d3.select("#blog-tag-cloud");
            container.selectAll("svg").remove();

            container.append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", `translate(${width/2},${height/2})`)
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", d => d.size + "px")
                .style("font-family", "Inter")
                .style("font-weight", d => d.text === activeTag ? "700" : "400")
                .style("fill", (d, i) => {
                    if (d.text === activeTag) return "#1d9bf0";
                    const colors = ['#1d9bf0', '#16a34a', '#dc2626', '#ca8a04', '#9333ea', '#ea580c', '#0891b2', '#be185d', '#059669', '#7c3aed'];
                    return colors[i % colors.length];
                })
                .style("cursor", "pointer")
                .attr("text-anchor", "middle")
                .attr("transform", d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
                .text(d => d.text)
                .on("click", (d) => {
                    applyFeedFilter('blogs', d.text);
                });
        })
        .start();
}

function initCollectionCloud(externalData) {
    const cloudEl = document.getElementById('collection-tag-cloud');
    if (!cloudEl || !window.d3) return;
    
    const clearBtn = document.getElementById('collection-tag-cloud-clear');
    if (clearBtn) {
        clearBtn.onclick = () => applyFeedFilter('collections', null);
    }

    let data = [];
    if (externalData) {
        data = externalData;
    } else {
        const counts = {};
        (window.__COLLECTION_POST_TAGS__ || []).forEach(tags => {
            (tags || []).forEach(t => {
                if (!t) return;
                counts[t] = (counts[t] || 0) + 1;
            });
        });
        data = Object.keys(counts).map(t => ({ text: t, size: counts[t] }));
    }

    if (data.length === 0) return;

    const width = cloudEl.clientWidth || 600;
    const height = 160;

    const sizeScale = d3.scale.linear()
        .domain([d3.min(data, d => d.size) || 1, d3.max(data, d => d.size) || 1])
        .range([10, 28]);

    const activeTag = window._activeCollectionTag;

    d3.layout.cloud()
        .size([width, height])
        .words(data.map(d => ({ text: d.text, size: sizeScale(d.size) })))
        .padding(5)
        .rotate(0)
        .font("Inter, system-ui, sans-serif")
        .fontSize(d => d.size)
        .on("end", words => {
            const container = d3.select("#collection-tag-cloud");
            container.selectAll("svg").remove();

            container.append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", `translate(${width/2},${height/2})`)
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", d => d.size + "px")
                .style("font-family", "Inter")
                .style("font-weight", d => d.text === activeTag ? "700" : "400")
                .style("fill", (d, i) => {
                    if (d.text === activeTag) return "#1d9bf0";
                    const colors = ['#1d9bf0', '#16a34a', '#dc2626', '#ca8a04', '#9333ea', '#ea580c', '#0891b2', '#be185d', '#059669', '#7c3aed'];
                    return colors[i % colors.length];
                })
                .style("cursor", "pointer")
                .attr("text-anchor", "middle")
                .attr("transform", d => `translate(${d.x},${d.y})rotate(${d.rotate})`)
                .text(d => d.text)
                .on("click", (d) => {
                    applyFeedFilter('collections', d.text);
                });
        })
        .start();
}

function applyFeedFilter(panelType, tag) {
    let listId = '';
    if (panelType === 'patents') listId = 'patents-list';
    else if (panelType === 'blogs') listId = 'blogs-list';
    else if (panelType === 'collections') listId = 'douban-list';

    const list = document.getElementById(listId);
    const prefix = panelType === 'patents' ? 'patent' : (panelType === 'blogs' ? 'blog' : 'collection');
    const sentinel = document.getElementById(panelType + '-sentinel');
    const cloudActive = document.getElementById(prefix + '-tag-cloud-active');
    const cloudClear = document.getElementById(prefix + '-tag-cloud-clear');
    
    // Toggle logic: if clicking the active tag, treat it as null (clear)
    const currentActive = panelType === 'patents' ? window._activePatentTag : (panelType === 'blogs' ? window._activeBlogTag : window._activeCollectionTag);
    if (tag === currentActive) tag = null;

    if (panelType === 'patents') window._activePatentTag = tag;
    else if (panelType === 'blogs') window._activeBlogTag = tag;
    else if (panelType === 'collections') window._activeCollectionTag = tag;

    if (!list) return;

    const items = list.querySelectorAll('.feed-item');
    
    if (!tag) {
        // Reset everything
        items.forEach((item, idx) => {
            if (idx < 10) item.style.display = ''; // Revert to CSS default (grid)
            else item.style.display = 'none';
        });
        if (sentinel) sentinel.style.display = 'block';
        if (cloudActive) cloudActive.hidden = true;
        if (cloudClear) cloudClear.hidden = true;
        
        // Reset infinite scroll state for this list
        // Reset infinite scroll state for this list
        if (loadMoreState && loadMoreState[listId]) {
            loadMoreState[listId].loaded = 10;
            loadMoreState[listId].ended = false;
        }
    } else {
        // Apply filter
        let count = 0;
        items.forEach(item => {
            try {
                const tagsStr = item.dataset.tags || '[]';
                const tags = JSON.parse(tagsStr.replace(/&quot;/g, '"').replace(/&#39;/g, "'"));
                if (tags.includes(tag)) {
                    item.style.display = ''; // Revert to CSS default (grid)
                    count++;
                } else {
                    item.style.display = 'none';
                }
            } catch (e) {
                console.error('Error parsing tags', e);
            }
        });
        if (sentinel) sentinel.style.display = 'none';
        if (cloudActive) {
            cloudActive.hidden = false;
            cloudActive.textContent = `Showing: ${tag} (${count})`;
        }
        if (cloudClear) cloudClear.hidden = false;
    }
    
    // Refresh the cloud to show active state
    if (panelType === 'patents') {
        initPatentCloud();
    } else if (panelType === 'blogs') {
        initBlogCloud();
    } else if (panelType === 'collections') {
        initCollectionCloud();
    }
    
    // Re-check text overflow for filtered items
    setTimeout(checkTextOverflow, 100);
}
</script>
