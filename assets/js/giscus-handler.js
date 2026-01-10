// Global Giscus instance management
var globalGiscusContainer = null;
var giscusIframe = null;
var currentTerm = null;

// Toggle Giscus - uses single global instance
function toggleGiscus(el) {
    var bubble = el.closest('.status-bubble');
    if (!bubble) return;

    var wrapper = bubble.querySelector('.giscus-wrapper');
    if (!wrapper) return;

    var term = wrapper.getAttribute('data-term');
    var wrapperId = wrapper.getAttribute('id');

    console.log('Toggle requested for:', wrapperId, 'term:', term);

    // If clicking the same one that's already open, just hide it
    if (wrapper.querySelector('.giscus-active-container')) {
        console.log('Hiding current Giscus');
        var container = wrapper.querySelector('.giscus-active-container');
        container.remove();
        wrapper.style.display = 'none';
        return;
    }

    // Hide all other wrappers and remove the active container from them
    document.querySelectorAll('.giscus-wrapper').forEach(function (w) {
        w.style.display = 'none';
        var activeContainer = w.querySelector('.giscus-active-container');
        if (activeContainer) {
            activeContainer.remove();
        }
    });

    // Show this wrapper
    wrapper.style.display = 'block';

    // Initialize global Giscus if not done yet
    if (!globalGiscusContainer) {
        console.log('Initializing global Giscus instance');
        initGlobalGiscus(wrapper, term);
    } else {
        console.log('Reusing global Giscus, updating term from', currentTerm, 'to', term);
        moveGiscusToWrapper(wrapper);
        updateGiscusTerm(term);
    }
}

function initGlobalGiscus(wrapper, term) {
    globalGiscusContainer = document.createElement('div');
    globalGiscusContainer.className = 'giscus-active-container';
    globalGiscusContainer.style.cssText = 'margin-top: 15px;';
    wrapper.appendChild(globalGiscusContainer);

    currentTerm = term;

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

    script.onload = function () {
        console.log('✓ Global Giscus loaded for term:', term);
        // Find and store the iframe reference
        setTimeout(function () {
            giscusIframe = globalGiscusContainer.querySelector('iframe.giscus-frame');
            if (giscusIframe) {
                console.log('✓ Iframe found and stored');
                // Inject custom CSS to hide negative reactions
                injectReactionFilter();
            } else {
                console.error('✗ Iframe not found after load');
            }
        }, 1000);
    };

    globalGiscusContainer.appendChild(script);
}

function injectReactionFilter() {
    if (!giscusIframe) return;

    try {
        var iframeDoc = giscusIframe.contentDocument || giscusIframe.contentWindow.document;
        var style = iframeDoc.createElement('style');
        style.textContent = `
            /* Hide negative/neutral reactions, keep only positive ones */
            /* Hide: thumbs down (-1), confused, eyes */
            button[value="-1"],
            button[value="confused"],
            button[value="eyes"] {
                display: none !important;
            }
            
            /* Keep visible: thumbs up (+1), heart, hooray, rocket, laugh */
        `;
        iframeDoc.head.appendChild(style);
        console.log('✓ Reaction filter injected');
    } catch (e) {
        console.warn('Cannot inject CSS into Giscus iframe (CORS):', e);
        // Fallback: will need to use Giscus's built-in方法
    }
}

function moveGiscusToWrapper(wrapper) {
    if (!globalGiscusContainer) return;

    // Move the container to the new wrapper
    wrapper.appendChild(globalGiscusContainer);
    console.log('Moved Giscus container to:', wrapper.getAttribute('id'));
}

function updateGiscusTerm(newTerm) {
    if (currentTerm === newTerm) {
        console.log('Term unchanged, skipping update');
        return;
    }

    console.log('Updating term from', currentTerm, 'to', newTerm);

    if (!giscusIframe) {
        console.error('No iframe to update');
        return;
    }

    // Get current iframe src and parse it
    var currentSrc = giscusIframe.src;

    // Replace the term parameter in the URL
    var newSrc = currentSrc.replace(
        /term=[^&]*/,
        'term=' + encodeURIComponent(newTerm)
    );

    console.log('Reloading iframe with new term:', newTerm);
    console.log('New src:', newSrc.substring(0, 150) + '...');

    // Reload iframe with new src
    giscusIframe.src = newSrc;
    currentTerm = newTerm;
}

