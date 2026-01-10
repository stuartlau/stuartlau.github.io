/* ============================================
   Homepage Interactive Features
   ============================================ */

// Global language state
window.CURRENT_LANG = 'cn';

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    initCountUp();
    loadLatestBlog();
    loadLatestDouban();
    initObservers();
});

// Counter Animation
function initCountUp() {
    const counters = document.querySelectorAll('.stat-number');

    const animateCount = (element) => {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000;
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target + (target === 120 ? '+' : target === 10 ? '+' : '');
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    };

    // Intersection Observer for counter animation
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && entry.target.textContent === '0') {
                animateCount(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

// Toggle timeline card expansion
function toggleCard(card) {
    const isExpanded = card.classList.contains('expanded');

    // Close all other cards
    document.querySelectorAll('.timeline-card').forEach(c => {
        if (c !== card) {
            c.classList.remove('expanded');
        }
    });

    // Toggle current card
    if (isExpanded) {
        card.classList.remove('expanded');
    } else {
        card.classList.add('expanded');
    }
}

// Switch activity tabs
function switchTab(tabName) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.closest('.tab-btn').classList.add('active');

    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabName + '-content').classList.add('active');

    // Load content if not loaded
    if (tabName === 'blog' && !window.blogLoaded) {
        loadLatestBlog();
    } else if (tabName === 'douban' && !window.doubanLoaded) {
        loadLatestDouban();
    }
}

// Load latest blog posts
function loadLatestBlog() {
    fetch('/search.json')
        .then(res => res.json())
        .then(data => {
            const tech Posts = data.filter(post =>
                post.categories && post.categories.includes('技术') &&
                !post.title.includes('专利')
            ).slice(0, 3);

            const html = techPosts.map(post => `
                <div class="blog-item">
                    <h3><a href="${post.url}">${post.title}</a></h3>
                    <div class="blog-meta">
                        <span class="blog-date">${new Date(post.date).toLocaleDateString(window.CURRENT_LANG === 'cn' ? 'zh-CN' : 'en-US')}</span>
                        ${post.tags ? post.tags.map(tag => `<span class="blog-tag">${tag}</span>`).join('') : ''}
                    </div>
                    ${post.description ? `<p class="blog-excerpt">${post.description}</p>` : ''}
                </div>
            `).join('');

            document.getElementById('blog-content').innerHTML = html || '<p class="empty-state">No recent posts</p>';
            window.blogLoaded = true;
        })
        .catch(err => {
            console.error('Failed to load blog posts:', err);
            document.getElementById('blog-content').innerHTML = '<p class="error-state">Failed to load posts</p>';
        });
}

// Load latest Douban feed
function loadLatestDouban() {
    // Get current year
    const year = new Date().getFullYear();

    fetch(`/_data/douban/${year}.json`)
        .then(res => res.json())
        .then(data => {
            const latest = data.slice(0, 3);

            const html = latest.map(status => `
                <div class="douban-item">
                    <div class="douban-content">${status.content}</div>
                    ${status.images && status.images.length > 0 ? `
                        <div class="douban-images">
                            ${status.images.slice(0, 3).map(img => `
                                <img src="${img}" alt="Douban image">
                            `).join('')}
                        </div>
                    ` : ''}
                    <div class="douban-time">${status.time}</div>
                </div>
            `).join('');

            document.getElementById('douban-content').innerHTML = html || '<p class="empty-state">No recent updates</p>';
            window.doubanLoaded = true;
        })
        .catch(err => {
            console.error('Failed to load Douban feed:', err);
            // Try fallback year
            fetch(`/_data/douban/${year - 1}.json`)
                .then(res => res.json())
                .then(data => {
                    const latest = data.slice(0, 3);
                    const html = latest.map(status => `
                        <div class="douban-item">
                            <div class="douban-content">${status.content}</div>
                            <div class="douban-time">${status.time}</div>
                        </div>
                    `).join('');
                    document.getElementById('douban-content').innerHTML = html;
                })
                .catch(() => {
                    document.getElementById('douban-content').innerHTML = '<p class="error-state">Failed to load feed</p>';
                });
        });
}

// Language switching
function switchLang(lang) {
    window.CURRENT_LANG = lang;

    // Update button states
    document.getElementById('lang-btn-cn').classList.toggle('active', lang === 'cn');
    document.getElementById('lang-btn-en').classList.toggle('active', lang === 'en');

    // Toggle all language-specific elements
    document.querySelectorAll('[id$="-cn"]').forEach(el => {
        el.style.display = lang === 'cn' ? '' : 'none';
    });
    document.querySelectorAll('[id$="-en"]').forEach(el => {
        el.style.display = lang === 'en' ? '' : 'none';
    });

    // Refresh patent list if exists
    if (window.refreshPatentList) {
        window.refreshPatentList();
    }

    // Reload blog if already loaded (for date format)
    if (window.blogLoaded) {
        loadLatestBlog();
    }
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Intersection Observer for scroll animations
function initObservers() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.timeline-item, .activity-section').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s, transform 0.6s';
        observer.observe(el);
    });
}

// Add styles for blog and douban items dynamically
const style = document.createElement('style');
style.textContent = `
.blog-item {
    background: #fff;
    padding: 20px;
    margin-bottom: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: all 0.3s;
}

[data-theme="dark"] .blog-item {
    background: #1e1e1e;
}

.blog-item:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    transform: translateY(-2px);
}

.blog-item h3 {
    margin: 0 0 8px 0;
    font-size: 1.3rem;
}

.blog-item h3 a {
    color: #2e963d;
    text-decoration: none;
}

[data-theme="dark"] .blog-item h3 a {
    color: #66bb6a;
}

.blog-item h3 a:hover {
    text-decoration: underline;
}

.blog-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
    font-size: 0.9rem;
}

.blog-date {
    color: #666;
}

[data-theme="dark"] .blog-date {
    color: #9ca3af;
}

.blog-tag {
    display: inline-block;
    padding: 2px 8px;
    background: rgba(46, 150, 61, 0.1);
    color: #2e963d;
    border-radius: 4px;
    font-size: 0.85rem;
}

[data-theme="dark"] .blog-tag {
    background: rgba(102, 187, 106, 0.2);
    color: #66bb6a;
}

.blog-excerpt {
    color: #666;
    line-height: 1.6;
    margin: 0;
}

[data-theme="dark"] .blog-excerpt {
    color: #c9d1d9;
}

.douban-item {
    background: #fff;
    padding: 20px;
    margin-bottom: 16px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

[data-theme="dark"] .douban-item {
    background: #1e1e1e;
}

.douban-content {
    color: #222;
    line-height: 1.8;
    margin-bottom: 12px;
}

[data-theme="dark"] .douban-content {
    color: #e6edf3;
}

.douban-images {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 8px;
    margin-bottom: 12px;
}

.douban-images img {
    width: 100%;
    height: 100px;
    object-fit: cover;
    border-radius: 6px;
}

.douban-time {
    color: #999;
    font-size: 0.9rem;
}

.empty-state, .error-state {
    text-align: center;
    padding: 40px 20px;
    color: #999;
}
`;
document.head.appendChild(style);
