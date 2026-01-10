/* ==========================================
   Homepage V2 - Interactive Features
   ========================================== */

// Global state
window.CURRENT_LANG = 'cn';
let blogLoaded = false;
let doubanLoaded = false;

// Initialize on load
document.addEventListener('DOMContentLoaded', function () {
    console.log('Initializing homepage...');
    loadLatestContent();
    initTimelineDots();
});

// Language switching function
function switchLanguage(lang) {
    console.log('Switching to:', lang);
    window.CURRENT_LANG = lang;

    // Update button states
    document.getElementById('lang-btn-cn').classList.toggle('active', lang === 'cn');
    document.getElementById('lang-btn-en').classList.toggle('active', lang === 'en');

    // Toggle all cn/en elements
    document.querySelectorAll('[id$="-cn"]').forEach(el => {
        el.style.display = lang === 'cn' ? '' : 'none';
    });
    document.querySelectorAll('[id$="-en"]').forEach(el => {
        el.style.display = lang === 'en' ? '' : 'none';
    });

    // Refresh patent list if loaded
    if (window.refreshPatentList) {
        window.refreshPatentList();
    }
}

// Content tab switching
function switchContentTab(tabName) {
    console.log('Switching tab to:', tabName);

    // Update tab buttons
    document.querySelectorAll('.content-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    event.target.closest('.content-tab').classList.add('active');

    // Update panels
    document.querySelectorAll('.content-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.getElementById(tabName + '-panel').classList.add('active');

    // Load content if needed
    if (tabName === 'blog' && !blogLoaded) {
        loadFullBlogList();
    }
}

// Load latest content for homepage
function loadLatestContent() {
    console.log('Loading latest content...');
    loadLatestBlog();
    loadLatestDouban();
}

// Load latest 3 blog posts
function loadLatestBlog() {
    fetch('/search.json')
        .then(res => res.json())
        .then(data => {
            console.log('Loaded search.json:', data.length, 'posts');

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

            console.log('Filtered tech posts:', techPosts.length);

            if (techPosts.length === 0) {
                document.getElementById('latest-blog-list').innerHTML = '<p class="empty-msg">No recent posts</p>';
                return;
            }

            const html = techPosts.map(post => `
                <div class="blog-item">
                    <h4><a href="${post.url}">${post.title}</a></h4>
                    <div class="blog-meta">${new Date(post.date).toLocaleDateString(window.CURRENT_LANG === 'cn' ? 'zh-CN' : 'en-US')}</div>
                </div>
            `).join('');

            document.getElementById('latest-blog-list').innerHTML = html;
        })
        .catch(err => {
            console.error('Failed to load blog posts:', err);
            document.getElementById('latest-blog-list').innerHTML = '<p class="error-msg">Failed to load</p>';
        });
}

// Load latest 3 Douban posts
function loadLatestDouban() {
    const year = new Date().getFullYear();
    const dataUrl = `/_data/douban/${year}.json`;

    console.log('Loading Douban from:', dataUrl);

    fetch(dataUrl)
        .then(res => {
            if (!res.ok) throw new Error('Not found');
            return res.json();
        })
        .then(data => {
            console.log('Loaded Douban data:', data.length, 'items');

            const latest = data.slice(0, 3);

            const html = latest.map(status => `
                <div class="douban-item">
                    <div class="douban-content">${status.content.length > 100 ? status.content.substring(0, 100) + '...' : status.content}</div>
                    <div class="douban-time">${status.time}</div>
                </div>
            `).join('');

            document.getElementById('latest-douban-list').innerHTML = html;
        })
        .catch(err => {
            console.warn('Failed to load current year, trying previous year:', err);
            // Fallback to previous year
            fetch(`/_data/douban/${year - 1}.json`)
                .then(res => res.json())
                .then(data => {
                    const latest = data.slice(0, 3);
                    const html = latest.map(status => `
                        <div class="douban-item">
                            <div class="douban-content">${status.content.length > 100 ? status.content.substring(0, 100) + '...' : status.content}</div>
                            <div class="douban-time">${status.time}</div>
                        </div>
                    `).join('');
                    document.getElementById('latest-douban-list').innerHTML = html;
                })
                .catch(() => {
                    document.getElementById('latest-douban-list').innerHTML = '<p class="error-msg">Failed to load</p>';
                });
        });
}

// Load full blog list for blog tab
function loadFullBlogList() {
    fetch('/search.json')
        .then(res => res.json())
        .then(data => {
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
                .slice(0, 10);

            const html = techPosts.map(post => `
                <div class="blog-item">
                    <h4><a href="${post.url}">${post.title}</a></h4>
                    <div class="blog-meta">
                        ${new Date(post.date).toLocaleDateString(window.CURRENT_LANG === 'cn' ? 'zh-CN' : 'en-US')}
                        ${post.tags ? ' · ' + post.tags.slice(0, 3).join(', ') : ''}
                    </div>
                    ${post.description ? `<p style="color:#666;margin:8px 0 0 0;font-size:0.9rem;">${post.description}</p>` : ''}
                </div>
            `).join('');

            document.getElementById('blog-list-full').innerHTML = html;
            blogLoaded = true;
        })
        .catch(err => {
            console.error('Failed to load full blog list:', err);
            document.getElementById('blog-list-full').innerHTML = '<p class="error-msg">Failed to load</p>';
        });
}

// Initialize timeline dots interaction
function initTimelineDots() {
    const dots = document.querySelectorAll('.timeline-dot');
    dots.forEach(dot => {
        dot.addEventListener('click', function () {
            const company = this.getAttribute('data-company');
            const year = this.getAttribute('data-year');
            const lang = window.CURRENT_LANG;

            // You can add a modal or tooltip here to show company details
            alert(`${company} (${year})`);
        });
    });
}

// Add CSS for empty/error states
const style = document.createElement('style');
style.textContent = `
.empty-msg, .error-msg {
    text-align: center;
    padding: 20px;
    color: #999;
    font-size: 0.9rem;
}

.error-msg {
    color: #e74c3c;
}
`;
document.head.appendChild(style);

console.log('Homepage script loaded successfully');
