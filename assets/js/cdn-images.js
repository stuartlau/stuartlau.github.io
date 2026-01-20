/**
 * CDN Image Loader
 * Automatically converts local image URLs to jsDelivr CDN URLs for faster loading
 */
(function () {
    // CDN configuration
    const CDN_BASE = 'https://cdn.jsdelivr.net/gh/stuartlau/stuartlau.github.io@main';
    const LOCAL_PATTERNS = [
        '/images/',
        '/img/',
        '/assets/images/'
    ];

    // Skip CDN conversion for localhost/development
    const isLocalhost = window.location.hostname === 'localhost' ||
        window.location.hostname === '127.0.0.1' ||
        window.location.hostname.includes('.local');

    if (isLocalhost) {
        console.log('[CDN] Skipping CDN conversion in development mode');
        return;
    }

    /**
     * Convert a local image URL to CDN URL
     */
    function toCdnUrl(src) {
        if (!src) return src;

        // Skip if already a CDN URL or external URL
        if (src.includes('cdn.jsdelivr.net') ||
            src.includes('//') && !src.startsWith('/')) {
            return src;
        }

        // Check if it's a local image path
        const isLocalImage = LOCAL_PATTERNS.some(pattern => src.includes(pattern));

        if (isLocalImage) {
            // Remove any leading domain if present
            let path = src;
            if (src.includes('stuartlau.github.io')) {
                path = src.split('stuartlau.github.io')[1];
            }

            // Ensure path starts with /
            if (!path.startsWith('/')) {
                path = '/' + path;
            }

            return CDN_BASE + path;
        }

        return src;
    }

    /**
     * Process all images on the page
     */
    function processImages() {
        const images = document.querySelectorAll('img');
        let converted = 0;

        images.forEach(img => {
            const originalSrc = img.getAttribute('src');
            const newSrc = toCdnUrl(originalSrc);

            if (newSrc !== originalSrc) {
                img.setAttribute('src', newSrc);
                converted++;
            }

            // Also handle srcset if present
            const srcset = img.getAttribute('srcset');
            if (srcset) {
                const newSrcset = srcset.split(',').map(entry => {
                    const parts = entry.trim().split(' ');
                    parts[0] = toCdnUrl(parts[0]);
                    return parts.join(' ');
                }).join(', ');

                if (newSrcset !== srcset) {
                    img.setAttribute('srcset', newSrcset);
                }
            }
        });

        // Also process background images in style attributes
        const elementsWithBg = document.querySelectorAll('[style*="background"]');
        elementsWithBg.forEach(el => {
            const style = el.getAttribute('style');
            if (style && style.includes('url(')) {
                const newStyle = style.replace(/url\(['"]?([^'")\s]+)['"]?\)/g, (match, url) => {
                    const newUrl = toCdnUrl(url);
                    return `url('${newUrl}')`;
                });

                if (newStyle !== style) {
                    el.setAttribute('style', newStyle);
                }
            }
        });

        if (converted > 0) {
            console.log(`[CDN] Converted ${converted} images to CDN URLs`);
        }
    }

    // Run when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', processImages);
    } else {
        processImages();
    }

    // Also observe for dynamically added images
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            mutation.addedNodes.forEach(node => {
                if (node.nodeType === 1) { // Element node
                    if (node.tagName === 'IMG') {
                        const newSrc = toCdnUrl(node.getAttribute('src'));
                        if (newSrc !== node.getAttribute('src')) {
                            node.setAttribute('src', newSrc);
                        }
                    }
                    // Also check for images within the added node
                    const images = node.querySelectorAll && node.querySelectorAll('img');
                    if (images) {
                        images.forEach(img => {
                            const newSrc = toCdnUrl(img.getAttribute('src'));
                            if (newSrc !== img.getAttribute('src')) {
                                img.setAttribute('src', newSrc);
                            }
                        });
                    }
                }
            });
        });
    });

    observer.observe(document.body || document.documentElement, {
        childList: true,
        subtree: true
    });
})();
