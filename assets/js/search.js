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

  function snippetFromMatch(result) {
    var doc = result && (result.item || result) ? (result.item || result) : null;
    if (!doc) return '';

    var matches = result && result.matches ? result.matches : null;
    if (!matches || !matches.length) return doc.excerpt || '';

    var best = null;
    for (var i = 0; i < matches.length; i++) {
      var m = matches[i];
      if (!m || !m.key || !m.indices || !m.indices.length) continue;
      if (m.key !== 'content' && m.key !== 'excerpt' && m.key !== 'title') continue;
      best = m;
      if (m.key === 'content') break;
    }
    if (!best) return doc.excerpt || '';

    var text = doc[best.key] || '';
    if (!text) return doc.excerpt || '';

    var idx = best.indices[0];
    if (!idx || idx.length < 2) return doc.excerpt || '';

    var start = Math.max(0, idx[0] - 45);
    var end = Math.min(text.length, idx[1] + 90);
    var head = start > 0 ? '...' : '';
    var tail = end < text.length ? '...' : '';

    return head + text.slice(start, end).trim() + tail;
  }

  function renderResults(items) {
    if (!results) return;

    if (!items || !items.length) {
      results.innerHTML = '<div class="search-empty">No results</div>';
      return;
    }

    results.innerHTML = items
      .slice(0, 20)
      .map(function (item) {
        var doc = item.item || item;
        var title = escHtml(doc.title || 'Untitled');
        var url = escHtml(normalizeUrl(doc.url));
        var excerpt = escHtml(snippetFromMatch(item) || '');
        return (
          '<a class="search-result" href="' +
          url +
          '">' +
          '<div class="search-result-title">' +
          title +
          '</div>' +
          (excerpt ? '<div class="search-result-excerpt">' + excerpt + '</div>' : '') +
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
    var scoreCutoff = isAscii ? 0.35 : 0.55;
    out = (out || []).filter(function (r) {
      if (!r) return false;
      if (typeof r.score === 'number' && r.score > scoreCutoff) return false;
      if (!isAscii) return true;
      if (qLower.length < 4) return true;
      var doc = r.item || r;
      var hay = ((doc.title || '') + ' ' + (doc.excerpt || '') + ' ' + (doc.content || '')).toLowerCase();
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
            { name: 'title', weight: 0.6 },
            { name: 'excerpt', weight: 0.25 },
            { name: 'content', weight: 0.15 }
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

  document.addEventListener('DOMContentLoaded', function () {
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
