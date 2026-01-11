/**
 * Table of Contents (TOC) Generator
 * Automatically generates a table of contents from article headings
 */
(function () {
    'use strict';

    function generateTOC() {
        const tocContent = document.getElementById('toc-content');
        const tocWrapper = document.getElementById('toc-wrapper');

        if (!tocContent || !tocWrapper) return;

        // Find article content
        const article = document.querySelector('.article-wrap');
        if (!article) {
            tocWrapper.style.display = 'none';
            return;
        }

        // Get all headings (h3, h4, h5, h6 - since max is h3)
        const headings = article.querySelectorAll('h3, h4, h5, h6');

        if (headings.length === 0) {
            tocWrapper.style.display = 'none';
            return;
        }

        // Build TOC HTML
        const ul = document.createElement('ul');
        let hasValidHeadings = false;

        headings.forEach(function (heading, index) {
            // Skip if heading is inside toc-wrapper
            if (heading.closest('.toc-wrapper')) return;

            hasValidHeadings = true;

            // Create ID if not exists
            if (!heading.id) {
                heading.id = 'heading-' + index;
            }

            const li = document.createElement('li');
            const a = document.createElement('a');

            a.href = '#' + heading.id;
            a.textContent = heading.textContent;
            a.className = 'toc-' + heading.tagName.toLowerCase();
            a.dataset.headingId = heading.id;

            li.appendChild(a);
            ul.appendChild(li);
        });

        if (!hasValidHeadings) {
            tocWrapper.style.display = 'none';
            return;
        }

        tocContent.appendChild(ul);

        // Toggle functionality
        const toggleBtn = document.querySelector('.toc-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', function () {
                const isExpanded = this.getAttribute('aria-expanded') === 'true';
                this.setAttribute('aria-expanded', !isExpanded);
                tocContent.classList.toggle('collapsed', isExpanded);
            });
        }

        // Scroll spy - highlight current section
        const tocLinks = tocContent.querySelectorAll('a');

        function updateActiveLink() {
            let current = null;
            const scrollTop = window.scrollY || document.documentElement.scrollTop;

            headings.forEach(function (heading) {
                if (heading.closest('.toc-wrapper')) return;
                const rect = heading.getBoundingClientRect();
                const top = rect.top + scrollTop;

                if (top <= scrollTop + 100) {
                    current = heading.id;
                }
            });

            tocLinks.forEach(function (link) {
                if (link.dataset.headingId === current) {
                    link.classList.add('active');
                } else {
                    link.classList.remove('active');
                }
            });
        }

        // Throttle scroll events
        let ticking = false;
        window.addEventListener('scroll', function () {
            if (!ticking) {
                requestAnimationFrame(function () {
                    updateActiveLink();
                    ticking = false;
                });
                ticking = true;
            }
        });

        // Smooth scroll
        tocLinks.forEach(function (link) {
            link.addEventListener('click', function (e) {
                e.preventDefault();
                const targetId = this.getAttribute('href').slice(1);
                const target = document.getElementById(targetId);
                if (target) {
                    const top = target.getBoundingClientRect().top + window.scrollY - 80;
                    window.scrollTo({ top: top, behavior: 'smooth' });
                }
            });
        });

        // Initial update
        updateActiveLink();
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', generateTOC);
    } else {
        generateTOC();
    }
})();
