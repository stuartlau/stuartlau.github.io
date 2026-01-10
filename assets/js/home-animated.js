/**
 * Main JavaScript for Animated Homepage
 * Handles interactions, scroll animations, and content loading
 */

// Global state
window.CURRENT_LANG = 'cn';

// Initialize everything
document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 Animated homepage initializing...');
    initScrollAnimations();
    init3DCards();
    loadContent();
});

// Language switching
function switchLanguage(lang) {
    window.CURRENT_LANG = lang;

    // Update buttons
    document.querySelectorAll('.lang-switch span').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Toggle language-specific elements
    document.querySelectorAll('[id$="-cn"]').forEach(el => {
        el.style.display = lang === 'cn' ? '' : 'none';
    });
    document.querySelectorAll('[id$="-en"]').forEach(el => {
        el.style.display = lang === 'en' ? '' : 'none';
    });

    // Restart typewriter with new language
    if (window.typewriter) {
        const texts = lang === 'cn'
            ? ['软件架构师 · 技术极客', '120+ 专利持有者', '10年+ 互联网经验']
            : ['Software Architect', '120+ Patent Holder', '10+ Years Experience'];
        window.typewriter.texts = texts;
    }

    // Refresh patent cloud if exists
    if (window.refreshPatentList) {
        window.refreshPatentList();
    }
}

// Scroll-triggered animations
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('.content-section, .timeline-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(40px)';
        el.style.transition = 'opacity 0.6s, transform 0.6s';
        observer.observe(el);
    });
}

// 3D Card Effect
function init3DCards() {
    document.querySelectorAll('.card-3d').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
}

// Flip card toggle
function toggleFlipCard(element) {
    const card = element.closest('.flip-card');
    card.classList.toggle('flipped');
}

// Content tab switching
function switchContentTab(tabName) {
    // Update buttons
    document.querySelectorAll('.content-tab').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.closest('.content-tab').classList.add('active');

    // Update panels
    document.querySelectorAll('.content-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.getElementById(tabName + '-panel').classList.add('active');
}

// Load content
async function loadContent() {
    await loadLatestBlog();
    await loadLatestDouban();
}

async function loadLatestBlog() {
    try {
        const res = await fetch('/search.json');
        const data = await res.json();

        const techPosts = data
            .filter(post => {
                const isTech = post.categories && (
                    post.categories.includes('技术') ||
                    post.categories.includes('Tech')
                );
                const notPatent = !post.title.includes('专利') && !post.title.includes('Patent');
                return isTech && notPatent;
            })
            .sort((a, b) => new Date(b.date) - new Date(a.date))
            .slice(0, 3);

        const html = techPosts.map(post => `
            <div class="blog-item card-3d">
                <h3><a href="${post.url}">${post.title}</a></h3>
                <div class="meta">${new Date(post.date).toLocaleDateString(window.CURRENT_LANG === 'cn' ? 'zh-CN' : 'en-US')}</div>
                ${post.description ? `<p>${post.description.substring(0, 100)}...</p>` : ''}
            </div>
        `).join('');

        const container = document.getElementById('blog-list');
        if (container) {
            container.innerHTML = html;
            // Re-init 3D effect for new cards
            init3DCards();
        }
    } catch (err) {
        console.error('Failed to load blog:', err);
    }
}

async function loadLatestDouban() {
    try {
        const year = new Date().getFullYear();
        const res = await fetch(`/_data/douban/${year}.json`);
        const data = await res.json();

        const latest = data.slice(0, 3);
        const html = latest.map(status => `
            <div class="douban-item card-3d">
                <div class="content">${status.content.substring(0, 120)}${status.content.length > 120 ? '...' : ''}</div>
                <div class="time">${status.time}</div>
            </div>
        `).join('');

        const container = document.getElementById('douban-list');
        if (container) {
            container.innerHTML = html;
            init3DCards();
        }
    } catch (err) {
        console.warn('Failed to load Douban:', err);
    }
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});

// Add dynamic styles for content items
const style = document.createElement('style');
style.textContent = `
.blog-item, .douban-item {
    background: #fff;
    padding: 24px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}

[data-theme="dark"] .blog-item,
[data-theme="dark"] .douban-item {
    background: #1e1e1e;
}

.blog-item h3 {
    margin: 0 0 10px 0;
    font-size: 1.2rem;
}

.blog-item h3 a {
    color: var(--primary-green);
    text-decoration: none;
}

[data-theme="dark"] .blog-item h3 a {
    color: var(--primary-green-light);
}

.blog-item .meta,
.douban-item .time {
    color: #999;
    font-size: 0.85rem;
    margin-bottom: 12px;
}

.blog-item p,
.douban-item .content {
    color: #666;
    line-height: 1.6;
    margin: 0;
}

[data-theme="dark"] .blog-item p,
[data-theme="dark"] .douban-item .content {
    color: #c9d1d9;
}
`;
document.head.appendChild(style);

console.log('✅ Animated homepage initialized');
