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

  // --- Animal Icons Logic ---
  var animalIcons = [
    { name: 'Cat', svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#555" d="M226.5 92.9c14.3 42.9-.3 86.2-32.6 96.8s-70.1-15.6-84.4-58.5s.3-86.2 32.6-96.8s70.1 15.6 84.4 58.5zM100.4 198.6c18.9 32.4 14.3 70.1-10.2 84.1s-59.1-.9-78-33.3S-2.2 179.3 22.3 165.3s59.1 .9 78 33.3zM69.2 401.2C121.6 259.9 214.7 224 456 224c13.2 0 24-10.8 24-24V128c0-13.2-10.8-24-24-24S432 114.8 432 128v48c0 17.7-14.3 32-32 32H176c-17.7 0-32-14.3-32-32V64c0-17.7 14.3-32 32-32h60.8c12.2 0 23.2 8.3 26.2 19.3l8 29.5c5.4 19.9 25.7 31.8 45.4 26.5s31.8-25.7 26.5-45.4l-8.2-30.2C324 16.2 301.7 0 277 0H176C123 0 80 43 80 96v83.6c-4 1.3-8.2 2.6-12.8 4.2C33.7 195 9.2 225.9 2 262.3C-6.5 305.6 15.7 347.1 52.3 371l6.4 4.1c-9.1 17.8-8.1 42.6 9.8 68.7c17.6 25.6 44.4 44.9 76.9 44.9c25.4 0 51.5-12.1 72.8-26.4c2.8-1.9 5.5-3.8 8.1-5.7c37.7-27.4 69.8-67.4 86.8-111c5.2-13.4-1.5-28.5-14.9-33.7s-28.5 1.5-33.7 14.9c-12.8 32.7-37 62.8-65.4 83.5c-2.3 1.7-4.7 3.4-7.2 5.1c-17.6 11.8-37.1 19.3-51.2 19.3c-14.9 0-25.1-9.9-32.9-21.2c-5.8-8.4-9.8-16.7-12-23.7c31-15.3 49.3-38.3 49.3-64c0-23.7-15.6-45.6-42.5-59.5zM176 368c-17.7 0-32-14.3-32-32s14.3-32 32-32s32 14.3 32 32s-14.3 32-32 32z"/></svg>' },
    { name: 'Dog', svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#8B4513" d="M329.6 24c-18.4-5.3-37.8 .5-53.2 12L251 46.8c-18.1 13.5-42.3 16.4-62.8 7.5L144 38.4C119.5 27.8 91.2 31.9 69.7 48.3l-1.3 1C48.2 65.1 36.3 89.2 39.4 114.8c4.3 36-24.6 66.8-60.8 64.4C-23.5 177.6-32 203.4-25.8 226.5l19 71.3C5.6 343.9 48 377.9 96.6 377.9H296c56.4 0 106.8-29.6 134-78.6l38.2-71.2c6.2-11.5 5.2-25.6-2.5-36.1L450.4 171l28.9-20.6c13.2-9.4 19.3-25.8 15.3-41.5L484 72.8c-6.8-26.6-33.3-43.5-60.4-38.6L412.3 36c-13.8 2.5-27.9-1.3-38.3-10.3l-20.3-17.6c-5.8-5-16.2-7.3-24.1-4.1zm115.1 44.5c4.5 .8 9 4.1 10.1 8.5l10.6 36.1c.8 2.7-.2 5.5-2.6 7.1L428.2 145c-4 2.8-9.4 1.9-12.4-2.1l-25-33.1c-1.3-1.7-1.8-4-.9-6L410.8 73c1.7-3.9 7.6-5.8 11.5-3s22.4 20.6 22.4-1.5zM122.9 83c3.8-2.6 8.7-3.1 12.9-1.3L159.2 92c4.3 1.9 7.3 6 7.7 10.7l.6 5.8c.4 4.3 3.6 7.8 7.9 8.6c4.5 .8 8.7-2.3 9.4-6.8l2-13.1c1.2-8.3-3.6-16.3-11.4-18.7l-35.3-11c-6.9-2.1-14.3-.9-20.2 3.5l-2.8 2.1c-5.8 4.3-6.9 12.6-2.2 18.2C118.3 95.8 122.9 83 122.9 83zM320 320c0 17.7-14.3 32-32 32H192c-17.7 0-32-14.3-32-32s14.3-32 32-32h96c17.7 0 32 14.3 32 32z"/></svg>' },
    { name: 'Rabbit', svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#aaa" d="M112 112c0-35.3 14.3-64 32-64s32 28.7 32 64l0 13c32.7 6.1 63.3 15.6 91.5 28.1c14.7-22.3 24.5-48.4 24.5-77.1c0-35.3 14.3-64 32-64s32 28.7 32 64c0 35.8-15.5 68.3-39.7 91.3c21.2 13.5 40.5 29.3 57.2 47c23.6-6.6 48.7-10.3 74.6-10.3c15.2 0 29.9 1.4 44 3.9V48c0-26.5 21.5-48 48-48s48 21.5 48 48v240c0 88.4-71.6 160-160 160c-26.4 0-51.2-6.4-73.4-17.8l-5.3-2.7c-9.1-4.7-18.4-9.9-28.1-15.3c-23.3-13.1-44.5-27-61.1-40.4c-9.5-7.7-18.1-15.3-25.5-22.8c-23.1-23.7-38.6-54.7-41.5-89.8L96 112zM320 224a32 32 0 1 0 0 64 32 32 0 1 0 0-64z"/></svg>' },
    { name: 'Bird', svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#3498db" d="M124.9 83.1C65.5 141.6 15.7 217.3 1.1 230c-5.7 5.3-1.7 15.1 6 14.9c56.7-1.1 113.8-3.1 127 1.8c21.4 7.9 44.5 35.8 45.1 76.5c.3 22 17.6 40.7 39.5 42l161.7-.6c8.5 0 16.7 3.4 22.7 9.4l45.4 45.1c9 8.9 23.3 10.1 33.8 2.8l38.2-26.6c17.5-12.2 41.5-7.9 53.6 9.6l23.1 33.3c10.8 15.6 33.7 14.8 43.4-1.5l26-43.8c6.9-11.6 4.9-26.3-4.8-35.6l-50.1-48.4c-8.9-8.6-13.9-20.7-13.9-33.1V102.7c0-23.8-27-37.5-45.9-23.4l-31 23.2c-7.9 5.9-17.7 9.1-27.6 9.1l-24.8 .1c-11.5 0-22.8 3.5-32.3 10.1L272 232h-43.5c-35 0-59.7-34.9-49.3-68.5C189.6 130 208.5 73.1 224 32c5.2-13.9-6.3-28.3-20.9-26.1l-78.2 11.6z"/></svg>' },
    { name: 'Fish', svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#e67e22" d="M479.1 386.5c-11.1-39.7-44.1-70-84.3-77.9c-15.5-3-31.5-4.4-47.5-4.2c-54.8 .6-107.2 26.6-141.7 70.4C221.7 355 244 336 268 320c24-16 48-16 72-16c20.2 0 40 4.1 60 12c-20-20-40-20-60-20c-24 0-44.5 12-64.6 28.1c-18.6 14.9-39.8 35.6-66.3 54.4c.5 30.6 8.3 61.1 23.1 89.4l4.9 0c26.5 0 51.9-10.5 70.7-29.3L479.1 386.5zM292.1 498.4c-13.1-26.9-20-56.3-20.4-85.8C202 368.6 122.1 349.5 49.6 364L7.8 372.4c-11 2.2-18.7-10.7-13.2-20.3C18.4 310.8 61.3 247.9 166.7 206c-13.8 24.3-37.5 41.5-64.8 47.9c-9.3 .3-16.7-7.2-16.7-16.5c0-6 3.4-11.5 8.8-14.3c35.6-18.8 64.9-52 79.2-94.8c1.3-4 5-6.6 9.3-6.6s8 2.7 9.3 6.6c14.2 42.8 43.6 75.9 79.2 94.8c5.4 2.9 8.8 8.4 8.8 14.3c0 9.3-7.4 16.8-16.7 16.5c-27.4-6.4-51-23.6-64.8-47.9c105.4 41.8 148.4 104.7 172.1 146.1c-3.8 1.5-7.6 3-11.4 4.4C333.6 365 311 378.8 290.3 392.4c17.5 25.1 40 45.4 66.2 59.8c9.6 5.3 10.3 19 1.2 25.2l-10.9 7.5c-18.8 12.9-42.8 18.2-65.4 14.3l-5.6-1zM501.9 33.6l-50.6 63.3C407.7 82.5 357 76.2 305 77.7c-9 5.3-17.7 11.1-26 17.5c51.7-8.8 105.5-3.3 155.1 16.9l46.7-58.4c8.5-10.6 24.8-10.6 33.3 0l46.7 58.4c49.6-20.3 103.5-25.7 155.1-16.9c-8.3-6.4-17-12.2-26-17.5c-51.5-1.5-102.1 4.7-145.5 19.1l-50.6-63.3c-11.8-14.8-33.8-14.8-45.6 0z"/></svg>' },
    { name: 'Frog', svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#2ecc71" d="M104 160a24 24 0 1 0 0-48 24 24 0 1 0 0 48zm224 72a24 24 0 1 0 0-48 24 24 0 1 0 0 48zm208-72a24 24 0 1 0 0-48 24 24 0 1 0 0 48zM104 296a24 24 0 1 0 0-48 24 24 0 1 0 0 48zm432 0a24 24 0 1 0 0-48 24 24 0 1 0 0 48zM248 104a24 24 0 1 0 -48 0 24 24 0 1 0 48 0zM416 80a24 24 0 1 0 0 48 24 24 0 1 0 0-48zM32 512C14.3 512 0 497.7 0 480c0-12.6 7.4-23.4 18-28.7c26.7-13.3 54.4-44.2 60.1-50.7c3.9-4.5 6-10.3 6-16.3v-53.7c-9.2-8.5-15.6-19.8-18-32.9c-5.7-30.9-1.5-62.9 14.6-89.2l12.8-21c2.1-3.5 4.8-6.5 8-8.9C115 168.3 128 153.2 128 136c0-13.3 10.7-24 24-24s24 10.7 24 24c0 14.9 10.2 27.5 24.1 30.5c39.6 8.5 80.2 8.5 119.8 0c13.9-3 24.1-15.6 24.1-30.5c0-13.3 10.7-24 24-24s24 10.7 24 24c0 17.2 13 32.3 26.5 42.6c3.2 2.4 5.9 5.5 8 8.9l12.8 21c16.1 26.3 20.3 58.3 14.6 89.2c-2.4 13.1-8.7 24.4-18 32.9v53.7c0 6 2.1 11.8 6 16.3c5.7 6.5 33.4 37.4 60.1 50.7C504.6 456.6 512 467.4 512 480c0 17.7-14.3 32-32 32H352c-17.7 0-32-14.3-32-32V384c0-17.7-14.3-32-32-32s-32 14.3-32 32v96c0 17.7-14.3 32-32 32H32z"/></svg>' },
    { name: 'Spider', svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#333" d="M256 0c35.3 0 64 28.7 64 64V98.2c28.9 9.8 52.8 30.7 66.8 59.5c1 .9 2.1 1.9 3.2 2.8l20.1 20.1c16.1 16.1 41.6 17.5 59.3 3.4l1.3-1c17-13.6 42-12.3 57.6 3.2s16.9 40.7 3.2 57.6l-1.3 1c-3.1 2.5-12.3 7.1-17.1 11.9l-20.1 20.1c-16.7 16.7-40.4 49-23.4 96.6c4.5 12.6 1.4 26.6-7.8 35.8s-23.2 12.2-35.8 7.8c-32.9-11.6-45.9-42.3-51.4-58.5c-37.1-4.8-69.6-19.8-93.5-49.3c-2.8 1.4-5.9 2.1-9 2.1H236.4c-3.6 0-7-1-10.1-2.9C215 329.2 196.4 336 176 336H160c-26.5 0-48-21.5-48-48s21.5-48 48-48h16c19.3 0 36.3-10.9 44.5-27H208c-8.8 0-16-7.2-16-16v-8.6c-27.6-6-49.3-25.7-58.1-51.4H120c-13.3 0-24 10.7-24 24v24c0 13.3 10.7 24 24 24h16c13.3 0 24 10.7 24 24s-10.7 24-24 24H120c-39.8 0-72-32.2-72-72V144c0-39.8 32.2-72 72-72h13.9c8.8 25.7 30.5 45.4 58.1 51.4V112c0 8.8 7.2 16 16 16h32c8.8 0 16-7.2 16-16V64c0-35.3 28.7-64 64-64zM96 448H64c-17.7 0-32 14.3-32 32s14.3 32 32 32H96c17.7 0 32-14.3 32-32s-14.3-32-32-32zm32-64h24c13.3 0 24 10.7 24 24s-10.7 24-24 24H128c-13.3 0-24-10.7-24-24s10.7-24 24-24zm320 64h-32c-17.7 0-32 14.3-32 32s14.3 32 32 32h32c17.7 0 32-14.3 32-32s-14.3-32-32-32zm64 0c-17.7 0-32 14.3-32 32s14.3 32 32 32h32c17.7 0 32-14.3 32-32s-14.3-32-32-32H480z"/></svg>' },
    { name: 'Horse', svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 576 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#795548" d="M309.6 142.6c13.5-8.4 20-25.1 15.6-40.3L288 16 250.7 66.2C240.2 80.3 241 100.1 252.8 113.3l56.8 29.3zM161.4 397.7l-9.5-38c-8.6-34.6-32.5-62.8-64.8-76.3C40.6 268 0 286.1 0 318.9c0 40 25.1 77.2 62.6 92.6l23.5 9.7L54.6 461c-4.4 17.5 6 35.2 23.5 39.5s35.2-6 39.5-23.5L161.4 397.7zM343.3 64H504c39.8 0 72 32.2 72 72V392c0 13.3-10.7 24-24 24s-24-10.7-24-24V320H448v96c0 13.3-10.7 24-24 24s-24-10.7-24-24V320H320v96c0 13.3-10.7 24-24 24s-24-10.7-24-24V304c0-39.8 32.2-72 72-72H510c5-16.7-7.8-33.7-25.2-33.7c-9.6 0-18.7 5.2-23.8 13.6c-18.2 29.8-50.5 48.1-85.3 48.1H324.7L312 208.6l7.8 2.6c10.4 3.5 15.9 14.6 12.4 25s-14.6 15.9-25 12.4l-7.8-2.6-5.5 16.4c-9.2 27.6-39 42.6-66.6 33.4s-42.6-39-33.4-66.6l32.2-96.5c10.4 3.5 21.6 4.3 32.4 2.4l84.7-11.4z"/></svg>' },
    { name: 'Dragon', svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#c0392b" d="M194.4 227.1c-15.6-25-39.7-44.4-67.6-54.6L125 152c-15-5.5-22.7-22-17.2-37s22-22.7 37-17.2l8.8 3.2c12.2 4.5 25.6 1.7 34.6-7.8s12-23.3 7-35.3c-.5-1.1-1-2.2-1.6-3.3-3.1-5.7-9.3-9.1-15.8-9.1c-6 0-11.8 3-15.5 8.1l-24 32.9c-8.8 12.1-25.8 14.6-37.9 5.8s-14.6-25.8-5.8-37.9l24-32.9C133.5 30.6 157.9 18 183.9 22.8c12.1 2.2 23.3 9.4 30.7 19.3l17.7 23.6C263 32 301.2 16 341.2 16H472c13.3 0 24 10.7 24 24s-10.7 24-24 24H353.6C291 64 240 115 240 177.6c0 10.1 1.3 19.9 3.8 29.4l41.6 155.8 45.4-81.7c8.8-15.9 29-21.7 44.9-12.8s21.7 29 12.8 44.9L326.6 424.1c-12.2 21.9-35.1 35.9-60.2 36.8L120.5 464H121c-19.4 33-54.6 48-87.3 48H12c-6.6 0-12-5.4-12-12V428c0-26.5 21.5-48 48-48s48 21.5 48 48v26.7l126.3-4.5-30.7-114.9c-10.4-38.8 5.3-79.6 38.6-101.9L222 233l-27.6-5.8zM416 192c17.7 0 32-14.3 32-32s-14.3-32-32-32-32 14.3-32 32 14.3 32 32 32zm80 32c17.7 0 32-14.3 32-32s-14.3-32-32-32-32 14.3-32 32 14.3 32 32 32zM280 96c13.3 0 24-10.7 24-24s-10.7-24-24-24s-24 10.7-24 24s10.7 24 24 24z"/></svg>' },
    { name: 'Kiwi', svg: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><!--!Font Awesome Free 6.5.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2023 Fonticons, Inc.--><path fill="#8d6e63" d="M191.4 125.1c-12-6.9-20.9-18.4-23.7-32.6l-5.6-27.9c-3.1-15.4-16.7-26.6-32.4-26.6H72c-17.7 0-32 14.3-32 32s14.3 32 32 32h31L114.2 153l-64.1 64.1c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L176.6 181.3l21 6.5C230.7 198 256 228.8 256 264c0 13.3 10.7 24 24 24s24-10.7 24-24c0-38.4-16-72.9-41.5-97.1l-14.5-14 36-9L308.8 84l-20.1-20.1-59.9 14.9-37.3 46.4zM400 32c-79.5 0-144 64.5-144 144v8.5l26-6.5c39.9-10 82.2 13.5 94.6 52.6l10.9 34.3 22.1-13.8c12.2-7.6 27.6-8.7 40.8-2.9l69.7 30.5V176c0-79.5-64.5-144-144-144zm0 448c51.9 0 96.5-27.7 121.2-69.6L443.9 376.5 431 384.6c-27.4 17.1-61.9 19.6-91.7 6.6L310.6 379c-12.5-5.5-26.9-1.9-35.3 8.9L242.7 430c-15.6 20.1-43.1 27.2-66.2 17.1L126.6 425.2c-16.3-7.1-23.6-26.1-16.5-42.3s26.1-23.6 42.3-16.5l49.9 21.8c2.8 1.2 5.9 .5 8-1.9l26.6-30.8c3.2-3.7 3.5-9.1 1-13.1c-32.9-52.5-20.6-121.3 29.6-159.9l12-9.2c4.4-3.4 10.7-3.1 14.7 1l24.3 24.3c3.4 3.4 3.8 8.7 1.1 12.7L250 252.1c-6.2 9.4-6.2 21.6 0 31c6 9.1 18.2 11.8 27.4 6.1l43.2-27.1c6.2-3.9 13.9-3.9 20.2 0l42.6 26.6 22.8-14.2c3.7-2.3 8.1-3.1 12.4-2.1L492.3 289c4.2 1 8.8-.4 11.5-3.8l5.4-6.8C506.7 434.5 458.2 480 400 480z"/></svg>' }
  ];

  function getRandomIcon() {
