(function () {
    const container = document.getElementById('related-posts');
    if (!container) return;

    const currentTags = (container.getAttribute('data-tags') || '').split(',').filter(Boolean);
    const minCommonTags = parseInt(container.getAttribute('data-min-tags') || '1', 10);
    const maxPosts = parseInt(container.getAttribute('data-max') || '3', 10);
    const currentUrl = window.location.pathname;

    if (currentTags.length === 0) {
        container.style.display = 'none';
        return;
    }

    fetch('/search.json')
        .then(response => response.json())
        .then(posts => {
            if (!posts || posts.length === 0) return;

            const related = [];

            posts.forEach(post => {
                // Skip current post
                // Helper to check if URLs match (handling trailing slashes etc)
                if (post.url === currentUrl || post.url.includes(currentUrl) || currentUrl.includes(post.url)) {
                    // Basic check, might need refinement if urls are very different
                    // Ideally compare canonical paths.
                    // For now, simple strict check + substring check to be safe
                    if (post.url === currentUrl) return;
                }

                const otherTags = post.tags || [];
                let commonCount = 0;

                otherTags.forEach(tag => {
                    if (currentTags.includes(tag)) {
                        commonCount++;
                    }
                });

                if (commonCount >= minCommonTags) {
                    related.push({
                        post: post,
                        common: commonCount
                    });
                }
            });

            // Sort by common tags (descending)
            related.sort((a, b) => b.common - a.common);

            // Take top N
            const topPosts = related.slice(0, maxPosts).map(item => item.post);

            if (topPosts.length > 0) {
                renderRelatedPosts(topPosts);
            } else {
                container.style.display = 'none';
            }
        })
        .catch(err => {
            console.error('Failed to load related posts:', err);
            container.style.display = 'none';
        });

    function renderRelatedPosts(posts) {
        const title = container.getAttribute('data-title') || 'You might also enjoy';
        const viewAllText = 'View all articles'; // Could be parameterized too
        const viewAllUrl = '/blogs/';

        let html = `
      <div class="related-articles">
        <h4>
          ${title}
          <small class="pull-right">
            <a href="${viewAllUrl}">${viewAllText}</a>
          </small>
        </h4>
        <ul>
    `;

        posts.forEach(post => {
            html += `
        <li>
          <a href="${post.url}" title="${post.title}">${post.title}</a>
        </li>
      `;
        });

        html += `
        </ul>
        <hr />
      </div>
    `;

        container.innerHTML = html;
    }
})();
