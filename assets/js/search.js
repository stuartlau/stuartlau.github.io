(function () {
  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function escHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function normalizeUrl(u) {
    if (!u) return '/';
    try {
      return new URL(u, window.location.origin).toString();
    } catch (e) {
      return u;
    }
  }

  var modal;
  var input;
  var results;
  var toggleBtn;

  var fuse;
  var indexLoaded = false;
  var indexLoading = false;
  var pendingQuery = '';

  function openModal() {
    if (!modal) return;
    modal.removeAttribute('hidden');
    document.documentElement.classList.add('search-open');
    if (input) input.focus();
    loadIndex();
  }

  function closeModal() {
    if (!modal) return;
    modal.setAttribute('hidden', '');
    document.documentElement.classList.remove('search-open');
    if (input) input.value = '';
    results.innerHTML = '';
  }

  function renderResults(items) {
    if (!results) return;

    if (!items || !items.length) {
      results.innerHTML = '<div class="search-empty">No results</div>';
      return;
    }

    results.innerHTML = items
      .slice(0, 20)
      .map(function (item, index) {
        var doc = item.item || item;
        var title = escHtml(doc.title || 'Untitled');
        var url = escHtml(normalizeUrl(doc.url));
        var dateStart = doc.date ? doc.date.substring(0, 10) : ''; // Extract YYYY-MM-DD

        return (
          '<a class="search-result" href="' + url + '">' +
          '<span class="search-result-index">' + (index + 1) + '.</span>' +
          '<div class="search-result-title">' + title + '</div>' +
          (dateStart ? '<div class="search-result-date">' + dateStart + '</div>' : '') +
          '</a>'
        );
      })
      .join('');
  }

  function doSearch(query) {
    if (!query || !query.trim()) {
      results.innerHTML = '';
      return;
    }
    if (!fuse) {
      pendingQuery = query;
      results.innerHTML = '<div class="search-empty">Loading...</div>';
      loadIndex();
      return;
    }
    var q = query.trim();
    var out = fuse.search(q);

    var qLower = q.toLowerCase();
    var isAscii = /^[\x00-\x7F]+$/.test(q);
    var scoreCutoff = isAscii ? 0.2 : 0.35;
    out = (out || []).filter(function (r) {
      if (!r) return false;
      if (typeof r.score === 'number' && r.score > scoreCutoff) return false;
      var doc = r.item || r;
      var hay = String(doc.title || '').toLowerCase();
      if (!isAscii) return true;
      if (qLower.length < 4) return true;
      return hay.indexOf(qLower) !== -1;
    });
    renderResults(out);
  }

  function loadIndex() {
    if (indexLoaded || indexLoading) return;
    if (typeof window.Fuse !== 'function') return;

    indexLoading = true;

    var indexUrl = modal && modal.getAttribute('data-index-url') ? modal.getAttribute('data-index-url') : '/search.json';

    fetch(indexUrl, { cache: 'no-store' })
      .then(function (r) {
        if (!r.ok) throw new Error('Failed to load search index');
        return r.json();
      })
      .then(function (docs) {
        fuse = new window.Fuse(docs || [], {
          includeScore: true,
          includeMatches: true,
          threshold: 0.25,
          ignoreLocation: true,
          minMatchCharLength: 2,
          keys: [
            { name: 'title', weight: 1.0 }
          ]
        });
        indexLoaded = true;

        if (pendingQuery && input) {
          var q = pendingQuery;
          pendingQuery = '';
          doSearch(q);
        }
      })
      .catch(function () {
        indexLoaded = false;
      })
      .finally(function () {
        indexLoading = false;
      });
  }

  // --- Cute Animal Icons (High Quality, Color Flat Style) ---
  var animalIcons = [
    {
      name: 'Cat',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M54 26c-2.3-4.1-11.4-5-11.4-5-4.1-3.6-7.8-5-10.6-5s-6.5 1.4-10.6 5c0 0-9.1.9-11.4 5-2.5 4.5.3 16.1 6.8 20.3 4.6 2.9 10 4.7 15.2 4.7 5.3 0 10.7-1.8 15.2-4.7 6.6-4.2 9.4-15.8 6.8-20.3z" fill="#FFB74D"/><path d="M19 28a3 3 0 1 0 0 6 3 3 0 0 0 0-6m26 0a3 3 0 1 0 0 6 3 3 0 0 0 0-6" fill="#3E2723"/><path d="M32 38c-4 0-6-1.5-6-1.5v-2s2 1.5 6 1.5 6-1.5 6-1.5v2s-2 1.5-6 1.5z" fill="#3E2723"/><path d="M13.5 12.5L20 22H11l2.5-9.5zM50.5 12.5L44 22h9l-2.5-9.5z" fill="#FFB74D"/></svg>'
    },
    {
      name: 'Dog',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M32 58c-9.9 0-19-4-24-11-2-12 5-24 12-28 6-3 7-6 7-6V9h10v4s1 3 7 6c7 4 14 16 12 28-5 7-14.1 11-24 11z" fill="#A1887F"/><path d="M12 24C8 28 2 34 2 40s6 10 10 10h4c0-6 2-16 6-22-4-4-8-4-10-4zm40 0c4 4 10 10 10 16s-6 10-10 10h-4c0-6-2-16-6-22 4-4 8-4 10-4z" fill="#5D4037"/><circle cx="23" cy="30" r="3" fill="#3E2723"/><circle cx="41" cy="30" r="3" fill="#3E2723"/><path d="M32 44c-4 0-6-3-6-3s2 5 6 5 6-5 6-5-2 3-6 3z" fill="#3E2723"/><circle cx="32" cy="38" r="4" fill="#3E2723"/></svg>'
    },
    {
      name: 'Rabbit',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M42 20c-3 0-6-5-7-10V2h-6v8c-1 5-4 10-7 10-4.6 3-8 10-8 18 0 12.1 7.9 22 18 22s18-9.9 18-22c0-8-3.4-15-8-18z" fill="#FCE4EC"/><circle cx="24" cy="34" r="3" fill="#F48FB1"/><circle cx="40" cy="34" r="3" fill="#F48FB1"/><path d="M32 46c-2 0-4-3-4-3s2 1 4 1 4-1 4-1-2 3-4 3z" fill="#F06292"/><circle cx="32" cy="40" r="2" fill="#F06292"/></svg>'
    },
    {
      name: 'Panda',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><circle cx="16" cy="18" r="8" fill="#37474F"/><circle cx="48" cy="18" r="8" fill="#37474F"/><path d="M54 26C51.7 21.9 45 20 32 20S12.3 21.9 10 26c-2.5 4.5.3 16.1 6.8 20.3 4.6 2.9 10 4.7 15.2 4.7 5.3 0 10.7-1.8 15.2-4.7 6.6-4.2 9.4-15.8 6.8-20.3z" fill="#fff"/><ellipse cx="21" cy="30" rx="5" ry="4" fill="#37474F"/><ellipse cx="43" cy="30" rx="5" ry="4" fill="#37474F"/><circle cx="21" cy="30" r="1.5" fill="#fff"/><circle cx="43" cy="30" r="1.5" fill="#fff"/><circle cx="32" cy="38" r="3" fill="#37474F"/><path d="M32 44c-3 0-5-2-5-2s2 2 5 2 5-2 5-2-2 2-5 2z" fill="#37474F"/></svg>'
    },
    {
      name: 'Fox',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M54 22c-2.3-4.1-11.4-5-11.4-5-4.1-3.6-7.8-5-10.6-5s-6.5 1.4-10.6 5c0 0-9.1.9-11.4 5-2.5 4.5.3 16.1 6.8 20.3 4.6 2.9 10 4.7 15.2 4.7 5.3 0 10.7-1.8 15.2-4.7 6.6-4.2 9.4-15.8 6.8-20.3z" fill="#FF7043"/><path d="M12 24c4 8 12 16 20 16s16-8 20-16v18c-4 5-11 8-20 8s-16-3-20-8V24z" fill="#fff"/><circle cx="22" cy="32" r="3" fill="#3E2723"/><circle cx="42" cy="32" r="3" fill="#3E2723"/><circle cx="32" cy="44" r="3" fill="#3E2723"/><path d="M8 8l8 12h-8L8 8zm48 0l-8 12h8l8-12z" fill="#FF7043"/></svg>'
    },
    {
      name: 'Koala',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><circle cx="14" cy="20" r="8" fill="#90A4AE"/><circle cx="50" cy="20" r="8" fill="#90A4AE"/><path d="M54 30c0-12-9.9-22-22-22S10 18 10 30c0 9 5 17 12 20v6c0 2 2 4 4 4h12c2 0 4-2 4-4v-6c7-3 12-11 12-20z" fill="#B0BEC5"/><circle cx="24" cy="28" r="3" fill="#37474F"/><circle cx="40" cy="28" r="3" fill="#37474F"/><ellipse cx="32" cy="36" rx="6" ry="8" fill="#37474F"/></svg>'
    },
    {
      name: 'Lion',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><circle cx="32" cy="32" r="26" fill="#FFB74D"/><circle cx="32" cy="32" r="20" fill="#FFECB3"/><circle cx="24" cy="28" r="3" fill="#3E2723"/><circle cx="40" cy="28" r="3" fill="#3E2723"/><path d="M32 40c-3 0-5 2-5 2s2 2 5 2 5-2 5-2-2-2-5-2z" fill="#3E2723"/><line x1="16" y1="36" x2="26" y2="38" stroke="#3E2723" stroke-width="2"/><line x1="16" y1="40" x2="26" y2="40" stroke="#3E2723" stroke-width="2"/><line x1="48" y1="36" x2="38" y2="38" stroke="#3E2723" stroke-width="2"/><line x1="48" y1="40" x2="38" y2="40" stroke="#3E2723" stroke-width="2"/></svg>'
    },
    {
      name: 'Penguin',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M32 2C18 2 10 14 10 30c0 10 0 20 6 28h32c6-8 6-18 6-28 0-16-8-28-22-28z" fill="#37474F"/><path d="M32 8c-8 0-14 8-14 20 0 16 6 26 14 26s14-10 14-26c0-12-6-20-14-20z" fill="#ECEFF1"/><circle cx="25" cy="22" r="3" fill="#37474F"/><circle cx="39" cy="22" r="3" fill="#37474F"/><path d="M32 30l-4 4h8z" fill="#FF9800"/><path d="M16 58c-4 0-6-3-6-3s0 5 6 5 8-2 8-2-4 0-8 0zm4 0c0 0 0 0 0 0zm28 0c4 0 6-3 6-3s0 5-6 5-8-2-8-2 4 0 8 0z" fill="#FF9800"/></svg>'
    },
    {
      name: 'Owl',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M52 20c-3-4-8-6-8-6s-4 4-12 4-12-4-12-4-5 2-8 6c-4 5-1 16 3 20 5 4 10 5 17 5s12-1 17-5c4-4 7-15 3-20z" fill="#795548"/><circle cx="21" cy="26" r="8" fill="#FFF"/><circle cx="43" cy="26" r="8" fill="#FFF"/><circle cx="21" cy="26" r="3" fill="#3E2723"/><circle cx="43" cy="26" r="3" fill="#3E2723"/><path d="M32 36l-3-4h6z" fill="#FFC107"/></svg>'
    },
    {
      name: 'Pig',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M54 26c-2-4-6-6-6-6 4-6 6-12 6-12-4 0-10 4-14 8-3-1-6-1-8-1s-5 0-8 1c-4-4-10-8-14-8 0 0 2 6 6 12 0 0-4 2-6 6-6 7 1 18 6 22 5 3 10 4 16 4s11-1 16-4c5-4 11-15 6-22z" fill="#F48FB1"/><path d="M32 34c-6 0-10 2-10 6s4 6 10 6 10-2 10-6-4-6-10-6z" fill="#F06292"/><circle cx="29" cy="38" r="2" fill="#880E4F"/><circle cx="35" cy="38" r="2" fill="#880E4F"/><circle cx="22" cy="28" r="2" fill="#880E4F"/><circle cx="42" cy="28" r="2" fill="#880E4F"/></svg>'
    },
    {
      name: 'Tiger',
      svg: '<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><path d="M54 26c-2-4-6-6-6-6 3-5 3-10 3-10-4-1-8 2-10 4-3-1-6-2-9-2s-6 1-9 2c-2-2-6-5-10-4 0 0 0 5 3 10 0 0-4 2-6 6-5 7 1 18 6 22 5 3 10 4 16 4s11-1 16-4c5-4 11-15 6-22z" fill="#FFB74D"/><path d="M32 50c-4 0-8-2-8-6s3-4 8-4 8 0 8 4-4 6-8 6z" fill="#FFF9C4"/><path d="M32 40c-3 0-4 2-4 2s1 2 4 2 4-2 4-2-1-2-4-2z" fill="#3E2723"/><circle cx="22" cy="30" r="2" fill="#3E2723"/><circle cx="42" cy="30" r="2" fill="#3E2723"/><path d="M32 16l-2 6h4z" fill="#3E2723"/><path d="M22 18l-4 4 6 2z" fill="#3E2723"/><path d="M42 18l4 4-6 2z" fill="#3E2723"/></svg>'
    }
  ];

  function getRandomIcon() {
    return animalIcons[Math.floor(Math.random() * animalIcons.length)];
  }

  function setRandomIcons() {
    // 1. Search Modal Icon
    var searchIconObj = getRandomIcon();
    var searchHeader = document.querySelector('.search-modal .search-header');
    if (searchHeader) {
      var oldIcon = searchHeader.querySelector('.search-animal-icon');
      if (oldIcon) oldIcon.remove();

      var iconContainer = document.createElement('div');
      iconContainer.className = 'search-animal-icon';
      iconContainer.innerHTML = searchIconObj.svg;
      iconContainer.style.width = '42px';
      iconContainer.style.height = '42px';
      iconContainer.style.marginRight = '12px';
      iconContainer.style.marginBottom = '2px';
      iconContainer.style.alignSelf = 'flex-end'; // Keep roughly aligned

      var style = document.createElement('style');
      style.innerHTML = '.search-modal .search-header::before { display: none !important; }';
      document.head.appendChild(style);

      searchHeader.insertBefore(iconContainer, searchHeader.firstChild);
    }

    // 2. Homepage Home Icon (Multiple elements support)
    var homeIcons = document.querySelectorAll('.title-animal-icon');
    if (homeIcons.length > 0) {
      homeIcons.forEach(function (homeIcon) {
        var updateHomeIcon = function () {
          var iconObj = getRandomIcon();
          homeIcon.innerHTML = iconObj.svg;
          homeIcon.title = iconObj.name + ': Oops, you found me!';
        };

        updateHomeIcon();
        homeIcon.onclick = updateHomeIcon;
      });
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    setRandomIcons();

    modal = qs('#search-modal');
    input = qs('#search-input');
    results = qs('#search-results');
    toggleBtn = qs('#search-toggle');

    if (!modal || !input || !results || !toggleBtn) return;

    toggleBtn.addEventListener('click', function () {
      openModal();
    });

    modal.addEventListener('click', function (e) {
      if (e.target === modal) closeModal();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeModal();
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openModal();
      }
    });

    input.addEventListener('input', function () {
      doSearch(input.value);
    });
  });
})();
