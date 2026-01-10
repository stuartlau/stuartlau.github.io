// Patent Section Toggle - Elegant Link Style (Both CN & EN)
document.addEventListener('DOMContentLoaded', function () {
    var cloudWrap = document.querySelector('.tag-cloud-wrap');
    var blogList = document.getElementById('blog-list');

    if (cloudWrap) {
        // Hide by default
        cloudWrap.style.display = 'none';
        if (blogList) blogList.style.display = 'none';

        // Function to create and attach toggle link
        function addToggleLink(statsP, textCnId, textEnId) {
            if (!statsP) return;

            var toggleLink = document.createElement('a');
            toggleLink.className = 'patent-toggle-link';
            toggleLink.href = 'javascript:void(0)';
            toggleLink.innerHTML = '<span id="' + textCnId + '">查看详情 ›</span><span id="' + textEnId + '" style="display:none;">View Details ›</span>';
            toggleLink.style.cssText = 'margin-left:12px;color:#2e963d;text-decoration:none;font-size:0.95rem;font-weight:500;border-bottom:1px dashed #2e963d;transition:all 0.2s;';

            toggleLink.onmouseover = function () {
                this.style.color = '#267a31';
                this.style.borderBottomColor = '#267a31';
            };
            toggleLink.onmouseout = function () {
                this.style.color = '#2e963d';
                this.style.borderBottomColor = '#2e963d';
            };

            toggleLink.onclick = function () {
                if (cloudWrap.style.display === 'none') {
                    cloudWrap.style.display = 'block';
                    if (blogList) blogList.style.display = 'block';
                    // Update all toggle texts
                    document.querySelectorAll('[id^="toggle-text-cn-"]').forEach(function (el) {
                        el.innerHTML = '收起 ‹';
                    });
                    document.querySelectorAll('[id^="toggle-text-en-"]').forEach(function (el) {
                        el.innerHTML = 'Hide ‹';
                    });
                } else {
                    cloudWrap.style.display = 'none';
                    if (blogList) blogList.style.display = 'none';
                    // Update all toggle texts
                    document.querySelectorAll('[id^="toggle-text-cn-"]').forEach(function (el) {
                        el.innerHTML = '查看详情 ›';
                    });
                    document.querySelectorAll('[id^="toggle-text-en-"]').forEach(function (el) {
                        el.innerHTML = 'View Details ›';
                    });
                }
            };

            statsP.appendChild(document.createTextNode(' '));
            statsP.appendChild(toggleLink);
        }

        // Add to both CN and EN versions
        addToggleLink(document.getElementById('patent-stats-cn'), 'toggle-text-cn-1', 'toggle-text-en-1');
        addToggleLink(document.getElementById('patent-stats-en'), 'toggle-text-cn-2', 'toggle-text-en-2');
    }
});
