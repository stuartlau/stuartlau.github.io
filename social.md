---
layout: default
---

<div class="social-profile-container">
    <!-- Cover Image -->
    <div class="social-cover" style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);">
        <div class="cover-particles">
            {% for i in (1..15) %}
            <div class="cover-particle" style="left: {{ i | times: 6 | plus: 5 }}%; animation-delay: {{ i | times: 0.3 }}s;"></div>
            {% endfor %}
        </div>
    </div>

    <!-- Profile Header -->
    <div class="social-header">
        <div class="profile-avatar">
            <img src="{{ site.url }}/images/linkedin_avatar.jpg" alt="Stuart Lau">
        </div>
        <div class="profile-actions">
            <a href="https://github.com/stuartlau" target="_blank" class="profile-btn follow">Follow</a>
            <a href="mailto:stuart8@126.com" class="profile-btn message">Message</a>
        </div>
    </div>

    <!-- Profile Info -->
    <div class="social-profile-info">
        <div class="profile-name-row">
            <h1 class="profile-name">Stuart Lau</h1>
            <svg class="verified-badge" viewBox="0 0 24 24" width="20" height="20" fill="#1d9bf0">
                <path d="M22.5 12.5c0-1.58-.875-2.95-2.148-3.6.154-.435.238-.905.238-1.4 0-2.21-1.71-3.998-3.818-3.998-.47 0-.92.084-1.336.25C14.818 2.415 13.51 1.5 12 1.5s-2.816.917-3.437 2.25c-.415-.165-.866-.25-1.336-.25-2.11 0-3.818 1.79-3.818 4 0 .495.083.965.238 1.4-1.272.65-2.147 2.02-2.147 3.6 0 1.435.716 2.69 1.77 3.46-.133.382-.206.783-.206 1.21 0 2.21 1.71 3.998 3.818 3.998.47 0 .92-.084 1.336-.25.62 1.333 1.926 2.25 3.437 2.25 1.512 0 2.818-.917 3.437-2.25.415.165.866.25 1.336.25 2.11 0 3.818-1.79 3.818-4 0-.427-.073-.828-.206-1.21 1.054-.77 1.77-2.025 1.77-3.46zM12 16.5c-.83 0-1.6-.39-2.083-1.058-.32.47-.865.942-1.532 1.02-.82.096-1.473-.5-1.82-.972-.47-.64-.635-1.43-.14-2.2.17-.264.37-.532.595-.803.17-.205.34-.415.505-.63-.37-.55-.585-1.23-.585-1.97 0-1.66 1.35-3 3-3 .42 0 .82.1 1.17.27.35-.55.885-1.05 1.58-1.3.46-.165.97-.18 1.45-.03.32.1.62.24.89.42.27-.33.65-.65 1.12-.85.37-.16.78-.23 1.18-.18.62.07 1.16.39 1.53.88.25-.1.52-.18.8-.23.82-.14 1.58.12 2.07.67.17.2.3.42.38.65.08.23.1.48.05.73-.04.25-.14.49-.28.71.36.42.55.95.55 1.5v3.2c0 .42-.13.82-.37 1.17-.24.35-.58.63-.99.82-.41.19-.87.28-1.34.26-.47-.02-.92-.14-1.33-.35-.41-.21-.76-.5-1.03-.86-.27-.36-.47-.77-.58-1.21-.11-.44-.13-.9-.05-1.35.08-.45.27-.87.54-1.24.27-.37.62-.68 1.02-.92.4-.24.85-.4 1.32-.47v-.42c0-.55-.22-1.07-.62-1.45-.4-.38-.93-.6-1.5-.6z"></path>
                <path d="M10.5 13.5l-2.5-2.5-.7.7 3 3 6-6-.7-.7z"></path>
            </svg>
        </div>
        <p class="profile-handle">@stuartlau</p>
        <p class="profile-bio">Full Stack Engineer & Patent Inventor | 120+ Patents | Building systems at scale</p>
        
        <div class="profile-meta">
            <span class="meta-item">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                </svg>
                Shanghai, China
            </span>
            <span class="meta-item">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                </svg>
                Joined January 2025
            </span>
        </div>

        <div class="profile-stats">
            <a href="/publications/" class="stat-link">
                <span class="stat-value">120+</span>
                <span class="stat-label">Patents</span>
            </a>
            <a href="/life/" class="stat-link">
                <span class="stat-value">14</span>
                <span class="stat-label">Countries</span>
            </a>
            <a href="/blogs/" class="stat-link">
                <span class="stat-value">50+</span>
                <span class="stat-label">Posts</span>
            </a>
        </div>
    </div>

    <!-- Two Column Layout -->
    <div class="social-columns">
        <!-- Left Navigation -->
        <div class="social-nav">
            <a href="#blogs" class="nav-item active" data-tab="blogs">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                </svg>
                <span>Blogs</span>
            </a>
            <a href="#posts" class="nav-item" data-tab="posts">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                </svg>
                <span>Broadcast</span>
            </a>
            <a href="#patents" class="nav-item" data-tab="patents">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                <span>Patents</span>
            </a>
            <a href="#books" class="nav-item" data-tab="books">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 4h5v8l-2.5-1.5L6 12V4z"/>
                </svg>
                <span>Books</span>
            </a>
            <a href="#games" class="nav-item" data-tab="games">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-10 7H8v3H6v-3H3v-2h3V8h2v3h3v2zm4.5 2c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4-3c-.83 0-1.5-.67-1.5-1.5S18.67 9 19.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/>
                </svg>
                <span>Games</span>
            </a>
            <a href="#movies" class="nav-item" data-tab="movies">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M18 4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4h-4z"/>
                </svg>
                <span>Movies</span>
            </a>
            <a href="#travel" class="nav-item" data-tab="travel">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                </svg>
                <span>Travel</span>
            </a>
        </div>

        <!-- Right Content -->
        <div class="social-content">
            <!-- Blogs Tab -->
            <div class="content-panel active" id="blogs-panel">
                <h2 class="panel-title">Blogs</h2>
                <div class="feed-list">
                    {% assign posts = site.pages | where: "layout", "post" | where_exp: "p", "p.url contains '/blogs/tech'" | sort: "date" | reverse %}
                    {% for post in posts limit: 20 %}
                    <a href="{{ post.url }}" class="feed-item">
                        <div class="feed-tags">
                            {% for tag in post.tags %}
                            {% if tag != "Post" %}
                            <span class="feed-tag">{{ tag }}</span>
                            {% endif %}
                            {% endfor %}
                        </div>
                        <div class="feed-content">
                            <h3 class="feed-title">{{ post.title }}</h3>
                            <p class="feed-excerpt">{{ post.excerpt | strip_html | truncate: 120 }}</p>
                            <span class="feed-date">{{ post.date | date: "%Y-%m-%d" }}</span>
                        </div>
                    </a>
                    {% endfor %}
                    <a href="/blogs/" class="view-all-link">View all blogs →</a>
                </div>
            </div>

            <!-- Posts Tab (Broadcast/Douban) -->
            <div class="content-panel" id="posts-panel">
                <h2 class="panel-title">Broadcast</h2>
                <div class="feed-list">
                    {% assign year_str = "2026" %}
                    {% assign posts_data = site.data.douban[year_str] | reverse %}
                    {% for item in posts_data limit: 30 %}
                    <div class="feed-item douban-item">
                        <div class="feed-tags">
                            <span class="feed-tag">Broadcast</span>
                            {% if item.images and item.images.size > 0 %}
                            <span class="feed-tag photo">Photo</span>
                            {% endif %}
                        </div>
                        <div class="feed-content">
                            <p class="feed-text">{{ item.content | strip_html | truncate: 150 }}</p>
                            {% if item.images and item.images.size > 0 %}
                            <div class="feed-images">
                                <img src="{{ item.images[0] }}" alt="Image" class="feed-image">
                            </div>
                            {% endif %}
                            <span class="feed-date">{{ item.time }}</span>
                        </div>
                    </div>
                    {% endfor %}
                    <a href="/douban/2026.html" class="view-all-link">View all broadcasts →</a>
                </div>
            </div>

            <!-- Patents Tab -->
            <div class="content-panel" id="patents-panel">
                <h2 class="panel-title">Patents</h2>
                <div class="feed-list">
                    {% assign patents = site.pages | where: "layout", "post" | where_exp: "p", "p.url contains '/blogs/patent'" | sort: "date" | reverse %}
                    {% for patent in patents limit: 40 %}
                    <a href="{{ patent.url }}" class="feed-item">
                        <div class="feed-tags">
                            {% for tag in patent.tags %}
                            {% if tag != "Patent" and tag != "已授权" and tag != "待授权" and tag != "China" and tag != "US" and tag != "Japan" %}
                            <span class="feed-tag">{{ tag }}</span>
                            {% endif %}
                            {% endfor %}
                        </div>
                        <div class="feed-content">
                            <h3 class="feed-title">{{ patent.title | remove: "授权专利-" | remove: "待授权专利-" | remove: "Granted Patent-" | remove: "Patent Application-" | split: "-" | last }}</h3>
                            <p class="feed-excerpt">Patent registration document - {{ patent.title | remove: "授权专利-" | remove: "待授权专利-" | remove: "Granted Patent-" | remove: "Patent Application-" | split: "-" | first }}</p>
                            <span class="feed-date">{{ patent.date | date: "%Y-%m-%d" }}</span>
                        </div>
                    </a>
                    {% endfor %}
                    <a href="/publications/" class="view-all-link">View all patents →</a>
                </div>
            </div>

            <!-- Books Tab -->
            <div class="content-panel" id="books-panel">
                <h2 class="panel-title">Books</h2>
                <div class="feed-list">
                    {% assign books = site.data.books.all | reverse %}
                    {% for book in books limit: 30 %}
                    <a href="https://book.douban.com/subject/{{ book.id }}/" target="_blank" class="feed-item">
                        <div class="feed-tags">
                            <span class="feed-tag">{{ book.rating }}</span>
                            <span class="feed-tag">{{ book.date_read | slice: 0, 4 }}</span>
                        </div>
                        <div class="feed-content">
                            <h3 class="feed-title">{{ book.title }}</h3>
                            <p class="feed-excerpt">{{ book.author }} · {{ book.publisher }}</p>
                            {% if book.comment %}
                            <p class="feed-comment">"{{ book.comment | strip_html | truncate: 100 }}"</p>
                            {% endif %}
                        </div>
                        {% if book.cover %}
                        <img src="{{ book.cover }}" alt="{{ book.title }}" class="feed-cover">
                        {% endif %}
                    </a>
                    {% endfor %}
                    <a href="/books/" class="view-all-link">View all books →</a>
                </div>
            </div>

            <!-- Games Tab -->
            <div class="content-panel" id="games-panel">
                <h2 class="panel-title">Games</h2>
                <div class="feed-list">
                    {% assign games = site.data.games.all | reverse %}
                    {% for game in games limit: 30 %}
                    <a href="https://www.douban.com/game/{{ game.id }}/" target="_blank" class="feed-item">
                        <div class="feed-tags">
                            <span class="feed-tag">{{ game.rating }}</span>
                            <span class="feed-tag">{{ game.date | slice: 0, 4 }}</span>
                        </div>
                        <div class="feed-content">
                            <h3 class="feed-title">{{ game.title }}</h3>
                            <p class="feed-excerpt">{{ game.platform }} · {{ game.genre }}</p>
                        </div>
                        {% if game.cover %}
                        <img src="{{ game.cover }}" alt="{{ game.title }}" class="feed-cover">
                        {% endif %}
                    </a>
                    {% endfor %}
                    <a href="/games/all" class="view-all-link">View all games →</a>
                </div>
            </div>

            <!-- Movies Tab -->
            <div class="content-panel" id="movies-panel">
                <h2 class="panel-title">Movies</h2>
                <div class="feed-list">
                    {% assign movies = site.data.movies.all | reverse %}
                    {% for movie in movies limit: 30 %}
                    <a href="https://movie.douban.com/subject/{{ movie.id }}/" target="_blank" class="feed-item">
                        <div class="feed-tags">
                            <span class="feed-tag">{{ movie.rating }}</span>
                            <span class="feed-tag">{{ movie.year }}</span>
                        </div>
                        <div class="feed-content">
                            <h3 class="feed-title">{{ movie.title }}</h3>
                            <p class="feed-excerpt">{{ movie.director }} · {{ movie.genre }}</p>
                        </div>
                        {% if movie.cover %}
                        <img src="{{ movie.cover }}" alt="{{ movie.title }}" class="feed-cover">
                        {% endif %}
                    </a>
                    {% endfor %}
                    <a href="/movies/all.html" class="view-all-link">View all movies →</a>
                </div>
            </div>

            <!-- Travel Tab -->
            <div class="content-panel" id="travel-panel">
                <h2 class="panel-title">Travel</h2>
                <div class="feed-list">
                    {% assign travels = site.pages | where: "layout", "post" | where_exp: "p", "p.url contains '/blogs/travelling'" | sort: "date" | reverse %}
                    {% for travel in travels limit: 30 %}
                    <a href="{{ travel.url }}" class="feed-item">
                        <div class="feed-tags">
                            {% assign region = travel.url | split: '/' | last %}
                            <span class="feed-tag">{{ region | replace: '_', ' ' }}</span>
                        </div>
                        <div class="feed-content">
                            <h3 class="feed-title">{{ travel.title }}</h3>
                            <p class="feed-excerpt">{{ travel.excerpt | strip_html | truncate: 120 }}</p>
                            <span class="feed-date">{{ travel.date | date: "%Y-%m-%d" }}</span>
                        </div>
                        {% if travel.cover %}
                        <img src="{{ travel.cover }}" alt="{{ travel.title }}" class="feed-cover">
                        {% endif %}
                    </a>
                    {% endfor %}
                    <a href="/life/" class="view-all-link">View all travel journals →</a>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
/* Container */
.social-profile-container {
    max-width: 1200px;
    margin: 0 auto;
    background: #fff;
    min-height: 100vh;
}

/* Cover */
.social-cover {
    height: 200px;
    position: relative;
    overflow: hidden;
}

.cover-particles {
    position: absolute;
    width: 100%;
    height: 100%;
}

.cover-particle {
    position: absolute;
    width: 4px;
    height: 4px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    animation: float-up 8s infinite ease-in-out;
}

@keyframes float-up {
    0%, 100% { transform: translateY(100px); opacity: 0; }
    50% { transform: translateY(0); opacity: 0.6; }
}

/* Header */
.social-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding: 0 16px;
    margin-top: -50px;
    position: relative;
}

.profile-avatar {
    width: 134px;
    height: 134px;
    border-radius: 50%;
    border: 4px solid #fff;
    overflow: hidden;
    background: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.profile-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.profile-actions {
    display: flex;
    gap: 8px;
    margin-bottom: 12px;
}

.profile-btn {
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s;
}

.profile-btn.follow {
    background: #1d9bf0;
    color: #fff;
}

.profile-btn.follow:hover {
    background: #1a8cd8;
}

.profile-btn.message {
    background: #fff;
    color: #0f1419;
    border: 1px solid #cfd9de;
}

.profile-btn.message:hover {
    background: #f7f9f9;
}

/* Profile Info */
.social-profile-info {
    padding: 12px 16px;
}

.profile-name-row {
    display: flex;
    align-items: center;
    gap: 4px;
}

.profile-name {
    font-size: 20px;
    font-weight: 700;
    color: #0f1419;
    margin: 0;
}

.verified-badge {
    flex-shrink: 0;
}

.profile-handle {
    color: #536471;
    font-size: 15px;
    margin: 2px 0;
}

.profile-bio {
    color: #0f1419;
    font-size: 15px;
    line-height: 1.4;
    margin: 12px 0;
}

.profile-meta {
    display: flex;
    gap: 16px;
    margin-bottom: 12px;
}

.meta-item {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #536471;
    font-size: 14px;
}

.profile-stats {
    display: flex;
    gap: 20px;
}

.stat-link {
    display: flex;
    gap: 4px;
    text-decoration: none;
}

.stat-link:hover .stat-value {
    text-decoration: underline;
}

.stat-value {
    font-weight: 600;
    color: #0f1419;
    font-size: 14px;
}

.stat-label {
    color: #536471;
    font-size: 14px;
}

/* Two Column Layout */
.social-columns {
    display: flex;
    border-top: 1px solid #eff3f4;
}

/* Left Navigation */
.social-nav {
    width: 200px;
    flex-shrink: 0;
    padding: 12px 0;
    border-right: 1px solid #eff3f4;
    position: sticky;
    top: 0;
    height: fit-content;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    color: #536471;
    text-decoration: none;
    border-radius: 24px;
    font-size: 15px;
    font-weight: 400;
    transition: all 0.2s;
}

.nav-item:hover {
    background: #f7f9f9;
    color: #0f1419;
}

.nav-item.active {
    color: #0f1419;
    font-weight: 600;
    background: #e8f5fe;
}

.nav-item svg {
    flex-shrink: 0;
}

/* Content Column */
.social-content {
    flex: 1;
    padding: 0;
}

.content-panel {
    display: none;
}

.content-panel.active {
    display: block;
}

.panel-title {
    padding: 16px;
    margin: 0;
    font-size: 20px;
    font-weight: 700;
    color: #0f1419;
    border-bottom: 1px solid #eff3f4;
}

/* Feed List */
.feed-list {
    padding: 0;
}

.feed-item {
    display: block;
    padding: 16px;
    border-bottom: 1px solid #eff3f4;
    text-decoration: none;
    transition: background 0.2s;
}

.feed-item:hover {
    background: #f7f9f9;
}

.feed-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 8px;
}

.feed-tag {
    padding: 2px 8px;
    background: #eff3f4;
    border-radius: 12px;
    font-size: 12px;
    color: #536471;
}

.feed-tag.photo {
    background: #e8f5fe;
    color: #1d9bf0;
}

.feed-content {
    flex: 1;
}

.feed-title {
    margin: 0 0 4px 0;
    font-size: 15px;
    font-weight: 600;
    color: #0f1419;
}

.feed-excerpt {
    margin: 0 0 4px 0;
    font-size: 14px;
    color: #536471;
    line-height: 1.4;
}

.feed-comment {
    margin: 4px 0;
    font-size: 14px;
    color: #0f1419;
    font-style: italic;
    line-height: 1.4;
}

.feed-text {
    margin: 0 0 8px 0;
    font-size: 14px;
    color: #0f1419;
    line-height: 1.5;
}

.feed-date {
    font-size: 13px;
    color: #536471;
}

.feed-images {
    margin: 8px 0;
}

.feed-image {
    max-width: 200px;
    max-height: 150px;
    border-radius: 12px;
    object-fit: cover;
}

.feed-cover {
    width: 60px;
    height: 80px;
    object-fit: cover;
    border-radius: 6px;
    flex-shrink: 0;
}

.douban-item {
    display: flex;
    flex-direction: column;
}

/* View All Link */
.view-all-link {
    display: block;
    padding: 16px;
    text-align: center;
    color: #1d9bf0;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    border-top: 1px solid #eff3f4;
}

.view-all-link:hover {
    text-decoration: underline;
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .social-nav {
        width: 100%;
        display: flex;
        overflow-x: auto;
        border-right: none;
        border-bottom: 1px solid #eff3f4;
        padding: 8px 0;
        position: relative;
        -webkit-overflow-scrolling: touch;
    }
    
    .nav-item {
        padding: 8px 12px;
        white-space: nowrap;
        font-size: 14px;
    }
    
    .nav-item span {
        display: none;
    }
    
    .nav-item {
        gap: 6px;
    }
    
    .social-columns {
        flex-direction: column;
    }
    
    .feed-cover {
        width: 50px;
        height: 70px;
    }
}

@media (max-width: 500px) {
    .social-cover {
        height: 150px;
    }
    
    .social-header {
        padding: 0 12px;
    }
    
    .profile-avatar {
        width: 100px;
        height: 100px;
    }
    
    .profile-btn {
        padding: 8px 12px;
        font-size: 13px;
    }
    
    .profile-actions {
        margin-bottom: 8px;
    }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const navItems = document.querySelectorAll('.nav-item');
    const panels = document.querySelectorAll('.content-panel');
    
    navItems.forEach(function(item) {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            var targetTab = this.getAttribute('data-tab');
            
            navItems.forEach(function(nav) { nav.classList.remove('active'); });
            this.classList.add('active');
            
            panels.forEach(function(panel) {
                panel.classList.remove('active');
                if (panel.id === targetTab + '-panel') {
                    panel.classList.add('active');
                }
            });
            
            history.pushState(null, null, '#' + targetTab);
        });
    });
    
    if (window.location.hash) {
        var hash = window.location.hash.slice(1);
        var activeNav = document.querySelector('.nav-item[data-tab="' + hash + '"]');
        if (activeNav) {
            activeNav.click();
        }
    }
    
    window.addEventListener('hashchange', function() {
        if (window.location.hash) {
            var hash = window.location.hash.slice(1);
            var activeNav = document.querySelector('.nav-item[data-tab="' + hash + '"]');
            if (activeNav) {
                navItems.forEach(function(nav) { nav.classList.remove('active'); });
                activeNav.classList.add('active');
                panels.forEach(function(panel) {
                    panel.classList.remove('active');
                    if (panel.id === hash + '-panel') {
                        panel.classList.add('active');
                    }
                });
            }
        }
    });
});
</script>
