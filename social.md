---
layout: default
subtitle: 社交媒体资料聚合页
---

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
        <!-- Profile Header -->
        <div class="profile-header">
            <!-- Cover Image -->
            <div class="profile-cover">
                <img src="{{ site.url }}/images/home-bg-art.jpg" alt="Cover">
            </div>
            
            <!-- Profile Info Container -->
            <div class="profile-info-container">
                <!-- Avatar overlapping cover -->
                <div class="profile-avatar">
                    <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau">
                </div>
                
                <!-- Profile Details -->
                <div class="profile-details">
                    <h1 class="profile-name">刘硕</h1>
                    <p class="profile-handle">@stuartlau</p>
                    <p class="profile-bio">Full Stack Engineer & Patent Inventor | Former Kuaishou, Amazon, Xiaomi | 120+ Patents | Building systems at scale | Traveling the world</p>
                    <div class="profile-meta">
                        <span><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/></svg> Shanghai, China</span>
                        <span><svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg> <a href="{{ site.url }}" target="_blank">stuartlau.github.io</a></span>
                    </div>
                    <div class="profile-stats">
                        <a href="/publications/"><span class="stat-value">120+</span> Patents</a>
                        <a href="/travel/"><span class="stat-value">14</span> Countries</a>
                        <a href="/blogs/"><span class="stat-value">180+</span> Blogs</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tab Navigation -->
        <div class="content-tabs">
            <a href="#posts" class="tab-item active" data-tab="posts">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" class="tab-icon-mobile"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
                <span class="tab-text">Posts</span>
            </a>
            <a href="#blogs" class="tab-item" data-tab="blogs">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" class="tab-icon-mobile"><path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25z"/></svg>
                <span class="tab-text">Blogs</span>
            </a>
            <a href="#patents" class="tab-item" data-tab="patents">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" class="tab-icon-mobile"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                <span class="tab-text">Patents</span>
            </a>
            <a href="#books" class="tab-item" data-tab="books">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" class="tab-icon-mobile"><path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>
                <span class="tab-text">Books</span>
            </a>
            <a href="#movies" class="tab-item" data-tab="movies">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" class="tab-icon-mobile"><path d="M18 4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4h-4z"/></svg>
                <span class="tab-text">Movies</span>
            </a>
            <a href="#games" class="tab-item" data-tab="games">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" class="tab-icon-mobile"><path d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2z"/></svg>
                <span class="tab-text">Games</span>
            </a>
        </div>

        <!-- Content Panels -->
        <div class="content-panels">
            <!-- Posts Tab (Broadcast) -->
            <div class="content-panel active" id="posts-panel">
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
                    <div class="feed-item douban-item expandable-item" {% if forloop.index > 10 %}style="display:none"{% endif %}>
                        <div class="post-avatar">
                            <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau" class="lazy-avatar" loading="lazy">
                        </div>
                        <div class="feed-content">
                            <div class="post-author-line">
                                <span class="post-author">@stuartlau</span>
                                <span class="feed-meta">{{ item.time }}</span>
                            </div>
                            <p class="feed-text">{{ item.content | strip_html | strip_newlines }}</p>
                            {% if item.images and item.images.size > 0 %}
                            <div class="social-image-grid">
                                {% for img in item.images %}
                                <div class="grid-img-wrap" onclick="openLightbox('{{ img }}', {{ item.images | jsonify | escape }})">
                                    <div class="img-placeholder">
                                        <div class="img-loading-spinner"></div>
                                    </div>
                                    <img data-src="{{ img }}" alt="Douban" class="social-img lazy-img">
                                </div>
                                {% endfor %}
                            </div>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
                <div class="scroll-sentinel" id="posts-sentinel"></div>
            </div>

            <!-- Blogs Tab -->
            <div class="content-panel" id="blogs-panel">
                <div class="blogs-column" id="blogs-list">
                    {% assign posts = site.posts | concat: site.pages | where_exp: "p", "p.path contains 'blogs/tech/'" | sort: "date" | reverse %}
                    {% for post in posts %}
                    <a href="{{ post.url }}" class="feed-item expandable-item" {% if forloop.index > 10 %}style="display:none"{% endif %}>
                        <div class="post-avatar">
                            <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau">
                        </div>
                        <div class="feed-content">
                            <div class="blog-card-title">{{ post.title }}</div>
                            <div class="blog-card-excerpt">
                                {% assign plain_content = post.content | strip_html | strip_newlines %}
                                {{ post.subtitle | default: post.description | default: plain_content | truncate: 200 }}
                            </div>
                            <span class="blog-card-date">{{ post.date | date: "%Y-%m-%d" }}</span>
                        </div>
                    </a>
                    {% endfor %}
                </div>
                <div class="scroll-sentinel" id="blogs-sentinel"></div>
            </div>

            <!-- Patents Tab -->
            <div class="content-panel" id="patents-panel">
                <div class="feed-list" id="patents-list">
                    {% assign patents = site.pages | where: "layout", "post" | where_exp: "p", "p.path contains 'blogs/patent'" | sort: "date" | reverse %}
                    {% for patent in patents %}
                    <a href="{{ patent.url }}" class="feed-item expandable-item" {% if forloop.index > 10 %}style="display:none"{% endif %}>
                        <div class="post-avatar">
                            <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau">
                        </div>
                        <div class="feed-content">
                            <div class="blog-card-title">{{ patent.title | remove: "授权专利-" | remove: "待授权专利-" | remove: "Granted Patent-" | remove: "Patent Application-" | split: "-" | last }}</div>
                            <div class="blog-card-excerpt">
                                {{ patent.title | remove: "授权专利-" | remove: "待授权专利-" | remove: "Granted Patent-" | remove: "Patent Application-" | split: "-" | first }}
                            </div>
                            <span class="blog-card-date">{{ patent.date | date: "%Y-%m-%d" }}</span>
                        </div>
                    </a>
                    {% endfor %}
                </div>
                <div class="scroll-sentinel" id="patents-sentinel"></div>
            </div>

            <!-- Books Tab -->
            <div class="content-panel" id="books-panel">
                <div class="feed-list" id="books-list">
                    {% assign books = site.data.books.all | sort: "date_read" | reverse %}
                    {% for book in books %}
                    <a href="https://book.douban.com/subject/{{ book.book_id }}/" target="_blank" class="feed-item expandable-item" {% if forloop.index > 10 %}style="display:none"{% endif %}>
                        <div class="post-avatar">
                            <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau">
                        </div>
                        <div class="feed-content">
                            <span class="feed-meta">{{ book.date_read | slice: 0, 4 }} · <span class="rating-stars" data-score="{% if book.my_rating %}{{ book.my_rating | times: 2 }}{% else %}{{ book.douban_rating }}{% endif %}"></span> {{ book.my_rating | default: '-' }}/{{ book.douban_rating }}</span>
                            <h5 class="feed-title">{{ book.title }}</h5>
                            <p class="feed-excerpt">{{ book.author }} · {{ book.publisher }}</p>
                            {% if book.my_comment %}
                            <p class="feed-comment">📖 {{ book.my_comment | truncate: 60 }}</p>
                            {% endif %}
                        </div>
                        {% if book.cover %}
                        <div class="feed-cover-placeholder">
                            <div class="cover-loading-spinner"></div>
                        </div>
                        <img data-src="{{ book.cover }}" alt="{{ book.title }}" class="feed-cover lazy-img">
                        {% endif %}
                    </a>
                    {% endfor %}
                </div>
                <div class="scroll-sentinel" id="books-sentinel"></div>
            </div>

            <!-- Movies Tab -->
            <div class="content-panel" id="movies-panel">
                <div class="feed-list" id="movies-list">
                    {% assign movies = site.data.movies.all | sort: "watched_date" | reverse %}
                    {% for movie in movies %}
                    <a href="https://movie.douban.com/subject/{{ movie.movie_id }}/" target="_blank" class="feed-item expandable-item" {% if forloop.index > 10 %}style="display:none"{% endif %}>
                        <div class="post-avatar">
                            <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau">
                        </div>
                        <div class="feed-content">
                            <span class="feed-meta">{{ movie.watched_date | slice: 0, 4 }} · <span class="rating-stars" data-score="{% if movie.my_rating %}{{ movie.my_rating | times: 2 }}{% else %}{{ movie.douban_rating }}{% endif %}"></span> {{ movie.my_rating | default: '-' }}/{{ movie.douban_rating }}</span>
                            <h5 class="feed-title">{{ movie.title }}</h5>
                            <p class="feed-excerpt">{{ movie.directors | join: ", " }} · {{ movie.genres | join: "/" }}</p>
                            {% if movie.my_comment %}
                            <p class="feed-comment">💬 {{ movie.my_comment | truncate: 60 }}</p>
                            {% endif %}
                        </div>
                        {% if movie.poster %}
                        <div class="feed-cover-placeholder">
                            <div class="cover-loading-spinner"></div>
                        </div>
                        <img data-src="{{ movie.poster }}" alt="{{ movie.title }}" class="feed-cover lazy-img">
                        {% endif %}
                    </a>
                    {% endfor %}
                </div>
                <div class="scroll-sentinel" id="movies-sentinel"></div>
            </div>

            <!-- Games Tab -->
            <div class="content-panel" id="games-panel">
                <div class="feed-list" id="games-list">
                    {% assign games = site.data.games.all | sort: "played_date" | reverse %}
                    {% for game in games %}
                    <a href="{{ game.douban_url }}" target="_blank" class="feed-item expandable-item" {% if forloop.index > 10 %}style="display:none"{% endif %}>
                        <div class="post-avatar">
                            <img src="{{ site.url }}/images/douban_avatar.jpg" alt="Stuart Lau">
                        </div>
                        <div class="feed-content">
                            <span class="feed-meta">{{ game.played_date | slice: 0, 4 }} · <span class="rating-stars" data-score="{% if game.my_rating %}{{ game.my_rating | times: 2 }}{% else %}{{ game.douban_rating }}{% endif %}"></span> {{ game.my_rating | default: '-' }}/{{ game.douban_rating }}</span>
                            <h5 class="feed-title">{{ game.title }}</h5>
                            <p class="feed-excerpt">{{ game.platforms | join: "/" }} · {{ game.genres | join: "/" }}</p>
                            {% if game.developer %}
                            <p class="feed-comment">🎮 {{ game.developer }}</p>
                            {% endif %}
                        </div>
                        {% if game.cover %}
                        <div class="feed-cover-placeholder">
                            <div class="cover-loading-spinner"></div>
                        </div>
                        <img data-src="{{ game.cover }}" alt="{{ game.title }}" class="feed-cover lazy-img">
                        {% endif %}
                    </a>
                    {% endfor %}
                </div>
                <div class="scroll-sentinel" id="games-sentinel"></div>
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

<div id="lightbox" onclick="handleLightboxClick(event)">
    <div class="lightbox-content" onclick="event.stopPropagation()">
        <button class="lightbox-close" onclick="closeLightbox()">×</button>
        <button id="lightbox-prev" class="lightbox-nav" onclick="prevLightboxImage(event)">‹</button>
        <img id="lightbox-img" src="" alt="Zoomed view">
        <button id="lightbox-next" class="lightbox-nav" onclick="nextLightboxImage(event)">›</button>
    </div>
</div>

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
    }

    .social-main {
        width: 100%;
        margin-left: 0;
        min-width: 0;
        border: none;
    }
}

/* Profile Header - Twitter Style */
.profile-header {
    position: relative;
    border-bottom: 1px solid #eff3f4;
}

/* Cover Image */
.profile-cover {
    width: 100%;
    height: 200px;
    overflow: hidden;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.profile-cover img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

/* Profile Info Container */
.profile-info-container {
    padding: 0 16px 16px;
    position: relative;
}

/* Avatar - Overlapping Cover */
.profile-avatar {
    position: absolute;
    top: 50px; /* Position so half shows in cover, half in content area */
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
    margin-top: 60px;
    padding-left: 16px;
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
    margin: 0 0 12px 0;
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
    }

    .tab-item {
        flex: 0 0 auto;
        min-width: 70px;
        padding: 12px 16px;
    }

    .tab-text {
        display: none;
    }

    .tab-icon-mobile {
        display: block !important;
        margin: 0;
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
    border-bottom: 4px solid transparent;
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

/* Feed Items */
.feed-item {
    display: flex;
    justify-content: flex-start; /* Compact layout */
    gap: 10px; /* Tight distance between text and image */
    padding: 12px 0; /* Remove horizontal padding per request */
    border-bottom: 1px solid #eff3f4;
    text-decoration: none;
    transition: background 0.2s;
}

.feed-item:hover {
    background: #f7f9f9;
}

.feed-content {
    flex: 1;
    min-width: 0;
}

/* Post Avatar */
.post-avatar {
    flex-shrink: 0;
}

.post-avatar img {
    width: 48px; /* Doubled size per request */
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
}

/* Post Author Line */
.post-author-line {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}

.post-author {
    font-size: 15px;
    font-weight: 700;
    color: #0f1419;
    margin-left: 2px; /* Ensure space from avatar */
}

.feed-meta {
    font-size: 13px;
    color: #536471;
}

.feed-text {
    font-size: 15px;
    line-height: 1.5;
    color: #0f1419;
    margin: 0;
}

.feed-title {
    font-size: 15px;
    font-weight: 700;
    color: #0f1419;
    margin: 0 0 4px 0;
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
    height: 100px;
    flex-shrink: 0;
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    cursor: pointer;
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

/* Lightbox - Non-fullscreen popup style */
#lightbox {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.7);
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 10000;
    cursor: pointer; /* Click anywhere to close */
}

.lightbox-content {
    position: relative;
    max-width: 85%;
    max-height: 85%;
    cursor: default; /* Prevent close when clicking content */
}

#lightbox-img {
    max-width: 100%;
    max-height: 80vh;
    border-radius: 8px;
    object-fit: contain;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5);
    cursor: default;
}

.lightbox-close {
    position: absolute;
    top: -40px;
    right: 0;
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
}

.lightbox-close:hover {
    background: #fff;
}

.lightbox-nav {
    position: absolute;
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
}

.lightbox-nav:hover {
    background: #fff;
}

#lightbox-prev {
    left: -60px;
}

#lightbox-next {
    right: -60px;
}

.lightbox-counter {
    position: absolute;
    bottom: -30px;
    left: 50%;
    transform: translateX(-50%);
    color: #fff;
    background: rgba(0, 0, 0, 0.6);
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 500;
}

@media (max-width: 768px) {
    .lightbox-content {
        max-width: 95%;
    }
    
    .lightbox-nav {
        width: 36px;
        height: 36px;
        padding: 8px;
        font-size: 16px;
    }
    
    #lightbox-prev {
        left: 10px;
    }
    
    #lightbox-next {
        right: 10px;
    }
    
    .lightbox-close {
        top: -35px;
        right: 5px;
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
        display: none; 
    }

    .tab-icon-mobile {
        display: block !important;
        margin: 0 auto;
    }
    
    #search-toggle {
        display: none !important;
    }

    .tab-item {
        padding: 12px 0;
    }
    
    .profile-header {
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 0 !important;
        min-height: 180px !important;
    }

    .profile-info-container {
        padding: 0 20px 20px;
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .profile-avatar {
        position: relative;
        top: -40px;
        left: 0;
        margin: 0 auto;
    }
    
    .profile-details {
        margin-top: -30px;
        width: 100%;
        text-align: center;
        padding-left: 0; /* Clear PC alignment */
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
</style>

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
            
            // Trigger lazy loading for images in the newly active panel
            setTimeout(function() {
                if (typeof reobserveLazyImages === 'function') {
                    reobserveLazyImages();
                }
            }, 50);
        });
    });

    // Random Cover Image
    const coverImgs = [
        'bg1.jpg', 'bg2.jpg', 'bg3.jpg'
    ];
    const randomBg = coverImgs[Math.floor(Math.random() * coverImgs.length)];
    const coverImgEl = document.querySelector('.profile-cover img');
    if (coverImgEl) {
        // Correct path to background image - removing redundant '/' if any
        let baseUrl = '{{ site.url }}';
        if (baseUrl.endsWith('/')) baseUrl = baseUrl.slice(0, -1);
        coverImgEl.src = baseUrl + '/images/background/' + randomBg;
    }

    if (window.location.hash) {
        var hash = window.location.hash.slice(1);
        var activeTab = document.querySelector('.tab-item[data-tab="' + hash + '"]');
        if (activeTab) activeTab.click();
    }
    
    // Load "On This Day" content
    loadHistoryToday();
});

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
        document.querySelectorAll('.feed-meta').forEach(el => {
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
                
                // Check if we're observing a wrapper (.grid-img-wrap) or an image directly
                if (target.classList.contains('grid-img-wrap')) {
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
    
    // For other lazy images (Books, Movies, Games covers), observe directly
    document.querySelectorAll('.feed-cover.lazy-img[data-src]').forEach(img => {
        // Check if in active panel
        const panel = img.closest('.content-panel');
        if (panel && !panel.classList.contains('active')) return;
        
        // Check if parent item is visible
        const feedItem = img.closest('.expandable-item') || img.closest('.feed-item');
        if (feedItem && feedItem.style.display === 'none') return;
        
        imageLazyObserver.observe(img);
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

// Load history on this day from Douban posts
function loadHistoryToday() {
    const today = new Date();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const todayStr = `${month}-${day}`;
    
    const historyList = document.getElementById('history-today');
    if (!historyList) return;
    
    // Get all posts from the page
    const allPosts = Array.from(document.querySelectorAll('.douban-item'));
    const todayPosts = allPosts.filter(item => {
        const metaEl = item.querySelector('.feed-meta');
        if (metaEl) {
            const dateStr = metaEl.textContent.trim();
            return dateStr.includes(todayStr);
        }
        return false;
    }).slice(0, 3); // Limit to 3 items
    
    if (todayPosts.length > 0) {
        historyList.innerHTML = todayPosts.map(post => {
            const text = post.querySelector('.feed-text').textContent.trim();
            const meta = post.querySelector('.feed-meta').textContent.trim();
            return `<div class="history-item"><strong>${meta.split(' ')[0]}</strong><br>${text.substring(0, 100)}${text.length > 100 ? '...' : ''}</div>`;
        }).join('');
    } else {
        historyList.innerHTML = '<div class="history-item">No posts on this day in previous years.</div>';
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
        const toLoad = Math.min(hiddenItems.length, 10);

        if (toLoad === 0) {
            state.ended = true;
            if (sentinel) {
                sentinel.classList.remove('loading');
                sentinel.classList.add('end');
            }
            return;
        }

        for (let i = 0; i < toLoad; i++) {
            hiddenItems[i].style.display = '';
        }

        state.loaded += toLoad;
        state.loading = false;
        state.ended = hiddenItems.length <= 10;

        if (sentinel) {
            sentinel.classList.remove('loading');
            if (state.ended) {
                sentinel.classList.add('end');
            }
        }

        // Trigger lazy loading for newly visible images
        reobserveLazyImages();
    }, 300);
}

// Initialize Infinite Scroll with Intersection Observer
function initInfiniteScroll() {
    if (!('IntersectionObserver' in window)) {
        return;
    }

    const panels = ['posts', 'blogs', 'patents', 'books', 'movies', 'games'];

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

function openLightbox(src, imagesArr) {
    const lb = document.getElementById('lightbox');
    
    // If the image is already open, close it (toggle effect)
    if (lb.style.display === 'flex' && currentImages.length === 1 && currentImages[0] === src) {
        closeLightbox();
        return;
    }

    currentImages = imagesArr || [src];
    currentImageIndex = currentImages.indexOf(src);
    if (currentImageIndex === -1) currentImageIndex = 0;

    updateLightboxImage();
    lb.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function updateLightboxImage() {
    const lbImg = document.getElementById('lightbox-img');
    if (lbImg) lbImg.src = currentImages[currentImageIndex];
    
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

function closeLightbox() {
    const lb = document.getElementById('lightbox');
    if (lb) lb.style.display = 'none';
    document.body.style.overflow = 'auto';
    currentImages = []; // Reset current images
}

// Handle click on lightbox background (close when clicking outside content)
function handleLightboxClick(e) {
    // Only close if clicking directly on the lightbox backdrop
    if (e.target.id === 'lightbox') {
        closeLightbox();
    }
}

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
    
    const starPath = "M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z";
    
    let html = '';
    
    // Full Stars
    for(let i=0; i<full; i++) {
        html += `<svg viewBox="0 0 24 24" width="14" height="14" fill="#ffa500"><path d="${starPath}"/></svg>`;
    }
    
    // Half Star
    if(half) {
        html += `<span style="position:relative; display:inline-block; width:14px; height:14px;">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="#e0e0e0"><path d="${starPath}"/></svg>
            <svg viewBox="0 0 24 24" width="14" height="14" fill="#ffa500" style="position:absolute; left:0; top:0; clip-path: inset(0 50% 0 0);"><path d="${starPath}"/></svg>
        </span>`;
    }
    
    // Empty Stars
    for(let i=0; i<empty; i++) {
        html += `<svg viewBox="0 0 24 24" width="14" height="14" fill="#e0e0e0"><path d="${starPath}"/></svg>`;
    }
    
    return html;
}

// Initialize Stars
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.rating-stars').forEach(el => {
        el.innerHTML = renderStars(el.dataset.score);
    });
});
</script>
