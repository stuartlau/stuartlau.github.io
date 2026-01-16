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

    <!-- Tab Navigation -->
    <div class="social-tabs">
        <button class="social-tab active" data-tab="posts">
            <span class="tab-label">Posts</span>
            <span class="tab-highlight"></span>
        </button>
        <button class="social-tab" data-tab="replies">
            <span class="tab-label">Replies</span>
            <span class="tab-highlight"></span>
        </button>
        <button class="social-tab" data-tab="media">
            <span class="tab-label">Media</span>
            <span class="tab-highlight"></span>
        </button>
        <button class="social-tab" data-tab="likes">
            <span class="tab-label">Likes</span>
            <span class="tab-highlight"></span>
        </button>
    </div>

    <!-- Tab Content -->
    <div class="social-content">
        <!-- Posts Tab -->
        <div class="social-panel active" id="posts-panel">
            <!-- Featured Post (Patent Highlight) -->
            <div class="social-pinned">
                <div class="pinned-badge">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                        <path d="M17 3H7c-1.1 0-2 .9-2 2v16l7-3 7 3V5c0-1.1-.9-2-2-2z"/>
                    </svg>
                    Pinned Patent
                </div>
                <div class="pinned-content">
                    <div class="pinned-header">
                        <img src="{{ site.url }}/images/linkedin_avatar.jpg" class="pinned-avatar" alt="Stuart">
                        <div class="pinned-user-info">
                            <span class="pinned-name">Stuart Lau</span>
                            <span class="pinned-handle">@stuartlau</span>
                            <span class="pinned-time">· Jan 15, 2026</span>
                        </div>
                    </div>
                    <div class="pinned-text">
                        Just received grant for my latest patent on distributed session management. This is one of 120+ patents I've filed across IM, video streaming, and distributed systems.
                    </div>
                    <div class="pinned-tags">
                        <a href="/publications/#distributed" class="pinned-tag">#DistributedSystems</a>
                        <a href="/publications/#im" class="pinned-tag">#IM</a>
                        <a href="/publications/#patent" class="pinned-tag">#Patent</a>
                    </div>
                    <div class="pinned-stats">
                        <span class="pinned-stat">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                            </svg>
                            42
                        </span>
                        <span class="pinned-stat">
                            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                <path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/>
                            </svg>
                            12
                        </span>
                    </div>
                </div>
            </div>

            <!-- Recent Posts Feed -->
            <div class="social-feed">
                <!-- Blog Post 1 -->
                <div class="social-post">
                    <img src="{{ site.url }}/images/linkedin_avatar.jpg" class="post-avatar" alt="Stuart">
                    <div class="post-content">
                        <div class="post-header">
                            <span class="post-name">Stuart Lau</span>
                            <span class="post-handle">@stuartlau</span>
                            <span class="post-time">· Jan 12, 2026</span>
                        </div>
                        <div class="post-text">
                            Exploring Claude Code and Windsurf for AI-assisted development. The productivity boost is real! Working on some exciting patent applications for conversation state management at scale.
                        </div>
                        <div class="post-tags">
                            <a href="/blogs/tech/2026/2026-01-12-douban-movie-game-book-architecture" class="post-tag">#AIDev</a>
                            <a href="/publications/#architecture" class="post-tag">#Architecture</a>
                        </div>
                        <div class="post-actions">
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18z"/>
                                </svg>
                                <span>2</span>
                            </button>
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/>
                                </svg>
                                <span>5</span>
                            </button>
                            <button class="post-action like">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                                </svg>
                                <span>28</span>
                            </button>
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Blog Post 2 -->
                <div class="social-post">
                    <img src="{{ site.url }}/images/linkedin_avatar.jpg" class="post-avatar" alt="Stuart">
                    <div class="post-content">
                        <div class="post-header">
                            <span class="post-name">Stuart Lau</span>
                            <span class="post-handle">@stuartlau</span>
                            <span class="post-time">· Jan 10, 2026</span>
                        </div>
                        <div class="post-text">
                            Great insights from "Designing Data-Intensive Applications". Highly recommend this book for anyone building distributed systems. Now reading the Chinese translation and taking notes.
                        </div>
                        <div class="post-book-ref">
                            <div class="book-cover" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                                <svg viewBox="0 0 24 24" width="32" height="32" fill="white">
                                    <path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 4h5v8l-2.5-1.5L6 12V4z"/>
                                </svg>
                            </div>
                            <div class="book-info">
                                <span class="book-title">Designing Data-Intensive Applications</span>
                                <span class="book-author">Martin Kleppmann</span>
                            </div>
                        </div>
                        <div class="post-actions">
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18z"/>
                                </svg>
                                <span>1</span>
                            </button>
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/>
                                </svg>
                                <span>3</span>
                            </button>
                            <button class="post-action like">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                                </svg>
                                <span>15</span>
                            </button>
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Blog Post 3 -->
                <div class="social-post">
                    <img src="{{ site.url }}/images/linkedin_avatar.jpg" class="post-avatar" alt="Stuart">
                    <div class="post-content">
                        <div class="post-header">
                            <span class="post-name">Stuart Lau</span>
                            <span class="post-handle">@stuartlau</span>
                            <span class="post-time">· Jan 5, 2026</span>
                        </div>
                        <div class="post-text">
                            New blog post: "Architecting Conversation State at Scale" - Lessons learned from handling millions of concurrent IM sessions.
                        </div>
                        <a href="/blogs/tech/2026/2026-01-05-Architecting_Conversation_State_at_Scale" class="post-link">
                            <div class="post-link-content">
                                <span class="post-link-title">Architecting Conversation State at Scale</span>
                                <span class="post-link-desc">How to design distributed systems for real-time messaging with billions of daily messages...</span>
                            </div>
                        </a>
                        <div class="post-actions">
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18z"/>
                                </svg>
                                <span>3</span>
                            </button>
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/>
                                </svg>
                                <span>8</span>
                            </button>
                            <button class="post-action like">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                                </svg>
                                <span>52</span>
                            </button>
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Travel Post -->
                <div class="social-post">
                    <img src="{{ site.url }}/images/linkedin_avatar.jpg" class="post-avatar" alt="Stuart">
                    <div class="post-content">
                        <div class="post-header">
                            <span class="post-name">Stuart Lau</span>
                            <span class="post-handle">@stuartlau</span>
                            <span class="post-time">· Dec 2025</span>
                        </div>
                        <div class="post-text">
                            Seoul trip with family! Amazing food, friendly people, and great memories. Can't wait to explore more of Asia next year.
                        </div>
                        <div class="post-images">
                            <div class="post-image" style="background: linear-gradient(135deg, #ff6b6b 0%, #ffa502 100%);">
                                <svg viewBox="0 0 24 24" width="48" height="48" fill="white" opacity="0.9">
                                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                                </svg>
                            </div>
                            <div class="post-image" style="background: linear-gradient(135deg, #5352ed 0%, #70a1ff 100%);">
                                <svg viewBox="0 0 24 24" width="48" height="48" fill="white" opacity="0.9">
                                    <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                                </svg>
                            </div>
                        </div>
                        <div class="post-tags">
                            <a href="/blogs/travelling/Asia/SouthKorea/首尔_Seoul" class="post-tag">#Seoul</a>
                            <a href="/life/" class="post-tag">#Travel</a>
                        </div>
                        <div class="post-actions">
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18z"/>
                                </svg>
                                <span>5</span>
                            </button>
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z"/>
                                </svg>
                                <span>12</span>
                            </button>
                            <button class="post-action like">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
                                </svg>
                                <span>89</span>
                            </button>
                            <button class="post-action">
                                <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                                    <path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92-1.31-2.92-2.92-2.92z"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Replies Tab -->
        <div class="social-panel" id="replies-panel">
            <div class="social-panel-empty">
                <p class="empty-title">No replies yet</p>
                <p class="empty-desc">When you reply to posts, they'll show up here.</p>
            </div>
        </div>

        <!-- Media Tab -->
        <div class="social-panel" id="media-panel">
            <div class="social-media-grid">
                <a href="/movies/all.html" class="media-item" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <svg viewBox="0 0 24 24" width="32" height="32" fill="white">
                        <path d="M18 4l2 4h-3l-2-4h-2l2 4h-3l-2-4H8l2 4H7L5 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4h-4z"/>
                    </svg>
                    <span>Movies</span>
                </a>
                <a href="/books/" class="media-item" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
                    <svg viewBox="0 0 24 24" width="32" height="32" fill="white">
                        <path d="M18 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 4h5v8l-2.5-1.5L6 12V4z"/>
                    </svg>
                    <span>Books</span>
                </a>
                <a href="/games/all.html" class="media-item" style="background: linear-gradient(135deg, #ee0979 0%, #ff6a00 100%);">
                    <svg viewBox="0 0 24 24" width="32" height="32" fill="white">
                        <path d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-10 7H8v3H6v-3H3v-2h3V8h2v3h3v2zm4.5 2c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4-3c-.83 0-1.5-.67-1.5-1.5S18.67 9 19.5 9s1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/>
                    </svg>
                    <span>Games</span>
                </a>
                <a href="/blogs/travelling/" class="media-item" style="background: linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%);">
                    <svg viewBox="0 0 24 24" width="32" height="32" fill="white">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/>
                    </svg>
                    <span>Travel</span>
                </a>
            </div>
        </div>

        <!-- Likes Tab -->
        <div class="social-panel" id="likes-panel">
            <div class="social-panel-empty">
                <p class="empty-title">No likes yet</p>
                <p class="empty-desc">When you like posts, they'll show up here.</p>
            </div>
        </div>
    </div>
</div>

<style>
/* Social Profile Container */
.social-profile-container {
    max-width: 600px;
    margin: 0 auto;
    background: #fff;
    min-height: 100vh;
}

/* Cover Image */
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

/* Profile Header */
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

/* Tab Navigation */
.social-tabs {
    display: flex;
    border-bottom: 1px solid #eff3f4;
    margin-top: 8px;
}

.social-tab {
    flex: 1;
    padding: 16px 0;
    background: none;
    border: none;
    position: relative;
    cursor: pointer;
    transition: background 0.2s;
}

.social-tab:hover {
    background: #f7f9f9;
}

.social-tab.active .tab-label {
    font-weight: 600;
}

.social-tab.active .tab-highlight {
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 56px;
    height: 4px;
    background: #1d9bf0;
    border-radius: 2px;
}

.tab-label {
    color: #536471;
    font-size: 15px;
}

/* Tab Content */
.social-content {
    padding-bottom: 60px;
}

.social-panel {
    display: none;
}

.social-panel.active {
    display: block;
}

/* Pinned Post */
.social-pinned {
    padding: 12px 16px;
    border-bottom: 1px solid #eff3f4;
}

.pinned-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #536471;
    font-size: 13px;
    margin-bottom: 8px;
}

.pinned-content {
    padding-left: 48px;
}

.pinned-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;
}

.pinned-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    object-fit: cover;
}

.pinned-user-info {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 2px;
}

.pinned-name {
    font-weight: 600;
    color: #0f1419;
    font-size: 14px;
}

.pinned-handle {
    color: #536471;
    font-size: 14px;
}

.pinned-time {
    color: #536471;
    font-size: 14px;
}

.pinned-text {
    color: #0f1419;
    font-size: 15px;
    line-height: 1.4;
    margin-bottom: 12px;
}

.pinned-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 12px;
}

.pinned-tag {
    color: #1d9bf0;
    font-size: 14px;
    text-decoration: none;
}

.pinned-tag:hover {
    text-decoration: underline;
}

.pinned-stats {
    display: flex;
    gap: 24px;
}

.pinned-stat {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #536471;
    font-size: 14px;
}

/* Social Feed */
.social-feed {
    padding-bottom: 60px;
}

.social-post {
    display: flex;
    padding: 12px 16px;
    border-bottom: 1px solid #eff3f4;
    cursor: pointer;
    transition: background 0.2s;
}

.social-post:hover {
    background: #f7f9f9;
}

.post-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
    flex-shrink: 0;
}

.post-content {
    flex: 1;
    min-width: 0;
    margin-left: 12px;
}

.post-header {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 2px;
    margin-bottom: 4px;
}

.post-name {
    font-weight: 600;
    color: #0f1419;
    font-size: 15px;
}

.post-handle {
    color: #536471;
    font-size: 15px;
}

.post-time {
    color: #536471;
    font-size: 15px;
}

.post-text {
    color: #0f1419;
    font-size: 15px;
    line-height: 1.4;
    margin-bottom: 12px;
}

.post-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 12px;
}

.post-tag {
    color: #1d9bf0;
    font-size: 14px;
    text-decoration: none;
}

.post-tag:hover {
    text-decoration: underline;
}

.post-book-ref {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px;
    background: #f7f9f9;
    border-radius: 12px;
    margin-bottom: 12px;
    text-decoration: none;
}

.book-cover {
    width: 48px;
    height: 48px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.book-info {
    display: flex;
    flex-direction: column;
}

.book-title {
    font-weight: 600;
    color: #0f1419;
    font-size: 14px;
}

.book-author {
    color: #536471;
    font-size: 13px;
}

.post-link {
    display: block;
    text-decoration: none;
    margin-bottom: 12px;
}

.post-link-content {
    padding: 12px;
    background: #f7f9f9;
    border-radius: 12px;
    border: 1px solid #eff3f4;
}

.post-link-title {
    display: block;
    font-weight: 600;
    color: #0f1419;
    font-size: 14px;
    margin-bottom: 4px;
}

.post-link-desc {
    color: #536471;
    font-size: 13px;
    line-height: 1.4;
}

.post-images {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin-bottom: 12px;
}

.post-image {
    aspect-ratio: 1;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: transform 0.2s;
}

.post-image:hover {
    transform: scale(1.02);
}

.post-actions {
    display: flex;
    justify-content: space-between;
    max-width: 425px;
}

.post-action {
    display: flex;
    align-items: center;
    gap: 6px;
    background: none;
    border: none;
    color: #536471;
    font-size: 13px;
    padding: 8px;
    margin: -8px;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.2s;
}

.post-action:hover {
    background: rgba(29, 155, 240, 0.1);
    color: #1d9bf0;
}

.post-action.like:hover {
    background: rgba(249, 24, 128, 0.1);
    color: #f91880;
}

.post-action span {
    font-size: 13px;
}

/* Empty Panel */
.social-panel-empty {
    padding: 48px 16px;
    text-align: center;
}

.empty-title {
    font-size: 20px;
    font-weight: 700;
    color: #0f1419;
    margin-bottom: 8px;
}

.empty-desc {
    color: #536471;
    font-size: 15px;
}

/* Media Grid */
.social-media-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    padding: 8px;
}

.media-item {
    aspect-ratio: 1;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    text-decoration: none;
    color: #fff;
    font-size: 14px;
    font-weight: 600;
    transition: transform 0.2s;
}

.media-item:hover {
    transform: scale(1.02);
}

/* Mobile Responsive */
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
    
    .social-profile-info {
        padding: 8px 12px;
    }
    
    .profile-actions {
        margin-bottom: 8px;
    }
    
    .social-tab {
        padding: 12px 0;
    }
    
    .social-tab.active .tab-highlight {
        width: 40px;
    }
    
    .tab-label {
        font-size: 14px;
    }
    
    .social-post {
        padding: 8px 12px;
    }
    
    .post-content {
        margin-left: 8px;
    }
    
    .post-actions {
        max-width: 100%;
    }
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabs = document.querySelectorAll('.social-tab');
    const panels = document.querySelectorAll('.social-panel');
    
    tabs.forEach(function(tab) {
        tab.addEventListener('click', function() {
            var targetTab = this.getAttribute('data-tab');
            
            // Update tab states
            tabs.forEach(function(t) { t.classList.remove('active'); });
            this.classList.add('active');
            
            // Update panel states
            panels.forEach(function(p) {
                p.classList.remove('active');
                if (p.id === targetTab + '-panel') {
                    p.classList.add('active');
                }
            });
        });
    });
    
    // Like button toggle
    var likeButtons = document.querySelectorAll('.post-action.like');
    likeButtons.forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('liked');
            var svg = this.querySelector('svg');
            if (this.classList.contains('liked')) {
                svg.style.fill = '#f91880';
                var span = this.querySelector('span');
                span.textContent = parseInt(span.textContent) + 1;
            } else {
                svg.style.fill = '';
                var span = this.querySelector('span');
                span.textContent = parseInt(span.textContent) - 1;
            }
        });
    });
});
</script>
