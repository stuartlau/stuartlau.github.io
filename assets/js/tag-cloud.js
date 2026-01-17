(function () {
  // Ensure default language
  if (typeof window.CURRENT_LANG === 'undefined') {
    window.CURRENT_LANG = 'cn';
  }

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

  function normalizeTag(t) {
    return String(t || '').trim();
  }

  function buildTagStats(posts) {
    var map = Object.create(null);
    posts.forEach(function (p) {
      var tags = Array.isArray(p.tags) ? p.tags : [];
      tags.forEach(function (t) {
        var tag = normalizeTag(t);
        if (!tag || tag === 'null' || tag === 'undefined') return;
        map[tag] = (map[tag] || 0) + 1;
      });
    });

    var out = [];
    Object.keys(map).forEach(function (k) {
      out.push({ tag: k, count: map[k] });
    });

    return out.sort(function (a, b) {
      return b.count - a.count;
    });
  }

  function setCloudStatus(msg) {
    var cloudEl = qs('#tag-cloud');
    if (!cloudEl) return;
    cloudEl.innerHTML = '<div class="tag-cloud-status">' + escHtml(msg) + '</div>';
  }

  function renderPostCard(p, idx, isEn) {
    var bgColors = [
      'rgba(37, 99, 235, 0.08)',
      'rgba(22, 163, 74, 0.08)',
      'rgba(202, 138, 4, 0.08)',
      'rgba(147, 51, 234, 0.08)',
      'rgba(234, 88, 12, 0.08)',
      'rgba(8, 145, 178, 0.08)',
      'rgba(190, 24, 93, 0.08)',
      'rgba(5, 150, 105, 0.08)',
    ];

    var title = escHtml(p.title || 'Untitled');
    var url = escHtml(p.url || '#');
    var date = p.date ? new Date(p.date).toLocaleDateString('zh-CN') : '';
    var tags = Array.isArray(p.tags) ? p.tags : [];
    var bgColor = bgColors[idx % bgColors.length];

    if (isEn && (title.indexOf('专利') !== -1 || (p.tags && p.tags.indexOf('Patent') !== -1))) {
      var idMatch = title.match(/([A-Z]{2}\d+[A-Z]?)/);
      if (idMatch) {
        var id = idMatch[1];
        var type = title.indexOf('待授权') !== -1 ? 'Pending Patent' : 'Granted Patent';
        title = type + ' ' + id;
        url = 'https://patents.google.com/patent/' + id + '/en';
      }
    }

    var tagsHtml = tags.length > 0
      ? '<span class="blog-card-tags">' + tags.slice(0, 3).map(function (t) { return escHtml(t); }).join(' · ') + '</span>'
      : '';

    var excerpt = escHtml(p.excerpt || '');

    // Store date for sorting
    var postDate = p.date ? new Date(p.date).getTime() : 0;

    return '<a href="' + url + '" class="blog-card" data-date="' + postDate + '"' + (isEn ? ' target="_blank"' : '') + ' style="background-color:' + bgColor + '; height: auto; min-height: 100px;">' +
      '<h4 class="blog-card-title">' + title + '</h4>' +
      '<div class="blog-card-meta">' +
      (date ? '<span class="blog-card-date">' + date + '</span>' : '') +
      tagsHtml +
      '</div>' +
      '<div class="blog-card-tooltip">' +
      (excerpt ? '<p class="blog-card-excerpt">' + excerpt + '</p>' : '') +
      (tags.length > 0 ? '<p><strong>标签：</strong>' + tags.join(' / ') + '</p>' : '') +
      '</div>' +
      '</a>';
  }

  function renderList(posts, filterTag) {
    var listEl = qs('#blog-list');
    if (!listEl) return;

    var shown = posts;
    if (filterTag) {
      shown = posts.filter(function (p) {
        return Array.isArray(p.tags) && p.tags.indexOf(filterTag) !== -1;
      });
    }

    // Sort by date descending (newest first)
    shown.sort(function (a, b) {
      var dateA = a.date ? new Date(a.date).getTime() : 0;
      var dateB = b.date ? new Date(b.date).getTime() : 0;
      return dateB - dateA;
    });

    if (!shown.length) {
      listEl.innerHTML = '<div class="blog-list-empty">No posts</div>';
      return;
    }

    var isEn = window.CURRENT_LANG === 'en';

    // Wrap cards in a grid container
    listEl.innerHTML =
      '<div class="blog-card-grid">' +
      shown
        .map(function (p, idx) {
          return renderPostCard(p, idx, isEn);
        })
        .join('') +
      '</div>';
  }

  var allLoadedPosts = [];
  var currentFilter = '';
  var currentPage = 1;
  var isLoading = false;
  var hasMore = true;
  var apiBase = '';
  var tagsCache = [];

  async function loadPosts() {
    if (isLoading || !hasMore) return;

    var listEl = qs('#blog-list');
    var loadingEl = qs('#blog-loading');
    if (!listEl) return;

    isLoading = true;
    if (loadingEl) loadingEl.style.display = 'block';

    try {
      var response = await fetch(apiBase + '/page-' + currentPage + '.json');
      if (!response.ok) throw new Error('Failed to fetch');

      var data = await response.json();

      if (data.data && data.data.length > 0) {
        // Add new posts to allLoadedPosts, then sort by date
        data.data.forEach(function (p) {
          allLoadedPosts.push(p);
        });

        // Sort all posts by date descending (newest first)
        allLoadedPosts.sort(function (a, b) {
          var dateA = a.date ? new Date(a.date).getTime() : 0;
          var dateB = b.date ? new Date(b.date).getTime() : 0;
          return dateB - dateA;
        });

        // Re-render the list with sorted posts
        var isEn = window.CURRENT_LANG === 'en';
        var gridContainer = listEl.querySelector('.blog-card-grid') || document.createElement('div');
        gridContainer.className = 'blog-card-grid';

        // Clear existing cards and re-render all
        var existingCards = listEl.querySelectorAll('.blog-card');
        existingCards.forEach(function (card) { card.remove(); });

        allLoadedPosts.forEach(function (p, idx) {
          var cardHtml = renderPostCard(p, idx, isEn);
          var tempDiv = document.createElement('div');
          tempDiv.innerHTML = cardHtml;
          var card = tempDiv.firstElementChild;
          card.style.opacity = '0';
          card.style.transform = 'translateY(10px)';
          gridContainer.appendChild(card);

          requestAnimationFrame(function () {
            card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          });
        });

        if (!listEl.querySelector('.blog-card-grid')) {
          listEl.appendChild(gridContainer);
        }

        currentPage++;
        hasMore = data.page < data.total_pages;
      } else {
        hasMore = false;
      }

      if (!hasMore) {
        var endEl = qs('#blog-end');
        if (endEl) endEl.style.display = 'block';
      }
    } catch (error) {
      console.error('Failed to load posts:', error);
      if (loadingEl) {
        loadingEl.querySelector('span').textContent = '加载失败，点击重试';
        loadingEl.style.cursor = 'pointer';
        loadingEl.onclick = loadPosts;
      }
    } finally {
      isLoading = false;
      if (hasMore && loadingEl) {
        loadingEl.style.display = 'none';
      }
    }
  }

  function applyFilter(posts, filterTag) {
    currentFilter = filterTag;
    allLoadedPosts = [];
    currentPage = 1;
    hasMore = true;

    var listEl = qs('#blog-list');
    var endEl = qs('#blog-end');
    if (listEl) listEl.innerHTML = '';
    if (endEl) endEl.style.display = 'none';

    loadPosts();
  }

  function renderCloud(tags, activeTag, onPick) {
    var cloudEl = qs('#tag-cloud');
    if (!cloudEl) return;
    if (!tags || !tags.length) {
      setCloudStatus('No tags');
      return;
    }
    if (!window.d3) {
      setCloudStatus('d3 not loaded');
      return;
    }
    if (!window.d3.layout || !window.d3.layout.cloud) {
      setCloudStatus('d3-cloud not loaded');
      return;
    }

    cloudEl.innerHTML = '';

    var width = Math.min(920, cloudEl.clientWidth || 920);
    var height = 260;

    var counts = tags.map(function (t) { return t.count; });
    var min = Math.min.apply(Math, counts);
    var max = Math.max.apply(Math, counts);

    var size = window.d3.scale
      .sqrt()
      .domain([min || 1, max || 1])
      .range([12, 52]);

    var colors = [
      '#2563eb', '#dc2626', '#16a34a', '#ca8a04', '#9333ea',
      '#ea580c', '#0891b2', '#be185d', '#059669', '#7c3aed',
      '#c2410c', '#1e40af', '#166534', '#991b1b', '#581c87'
    ];

    var colorMap = Object.create(null);
    var colorIndex = 0;

    var color = function (t) {
      if (activeTag && t === activeTag) return 'var(--link-color)';
      if (!colorMap[t]) {
        colorMap[t] = colors[colorIndex % colors.length];
        colorIndex++;
      }
      return colorMap[t];
    };

    var layout = window.d3.layout
      .cloud()
      .size([width, height])
      .words(
        tags.map(function (d) {
          return { text: d.tag, size: size(d.count), count: d.count };
        })
      )
      .padding(2)
      .rotate(function () {
        return 0;
      })
      .font('Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif')
      .fontSize(function (d) {
        return d.size;
      })
      .on('end', function (words) {
        draw(words, onPick);
      });

    layout.start();

    function draw(words, onPickCallback) {
      var svg = window.d3
        .select(cloudEl)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

      var g = svg
        .append('g')
        .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');

      var texts = g
        .selectAll('text')
        .data(words)
        .enter()
        .append('text')
        .attr('data-original-size', function (d) {
          return d.size;
        })
        .style('font-size', function (d) {
          return d.size + 'px';
        })
        .style('font-family', 'Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif')
        .style('fill', function (d) {
          return color(d.text);
        })
        .attr('text-anchor', 'middle')
        .attr('transform', function (d) {
          return 'translate(' + [d.x, d.y] + ')rotate(' + d.rotate + ')';
        })
        .style('cursor', 'pointer')
        .text(function (d) {
          return d.text;
        });

      texts.append('title')
        .text(function (d) {
          return d.text + ' (' + d.count + ')';
        });

      texts.on('mouseenter', function (d) {
        var self = window.d3.select(this);
        var originalSize = parseFloat(self.attr('data-original-size'));
        self.transition()
          .duration(200)
          .style('font-size', (originalSize * 1.3) + 'px');
      });

      texts.on('mouseleave', function (d) {
        var self = window.d3.select(this);
        var originalSize = parseFloat(self.attr('data-original-size'));
        self.transition()
          .duration(200)
          .style('font-size', originalSize + 'px');
      });

      texts.on('click', function (d) {
        if (!d || !d.text) return;
        window.d3.select(this).interrupt();
        if (onPickCallback && typeof onPickCallback === 'function') {
          onPickCallback(d.text);
        }
      });
    }
  }

  async function init() {
    var cloudEl = qs('#tag-cloud');
    var listEl = qs('#blog-list');
    if (!cloudEl || !listEl) return;

    apiBase = listEl.dataset.apiBase || '/api/blogs';

    var posts = Array.isArray(window.__BLOG_POSTS__) ? window.__BLOG_POSTS__ : [];
    var tags = buildTagStats(posts);
    tagsCache = tags;

    if (!posts.length) {
      setCloudStatus('No posts data');
    }

    var active = '';
    var clearBtn = qs('#tag-cloud-clear');
    var activeEl = qs('#tag-cloud-active');

    function setActive(tag) {
      active = active === tag ? '' : tag;
      if (clearBtn) clearBtn.hidden = !active;
      if (activeEl) {
        activeEl.hidden = !active;
        activeEl.textContent = active ? 'Filter: ' + active : '';
      }

      var filteredPosts = posts;
      if (active) {
        filteredPosts = posts.filter(function (p) {
          return Array.isArray(p.tags) && p.tags.indexOf(active) !== -1;
        });
      }

      renderList(filteredPosts, active);

      if (tags.length > 0) {
        renderCloud(tags, active, setActive);
      }
    }

    window.refreshPatentList = function () {
      var filteredPosts = posts;
      if (active) {
        filteredPosts = posts.filter(function (p) {
          return Array.isArray(p.tags) && p.tags.indexOf(active) !== -1;
        });
      }
      renderList(filteredPosts, active);
    };

    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        setActive(active);
      });
    }

    if (tags.length > 0) {
      renderCloud(tags, '', setActive);
    }

    window.addEventListener('resize', function () {
      if (tags.length > 0) {
        renderCloud(tags, active, setActive);
      }
    });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting && hasMore && !isLoading) {
          loadPosts();
        }
      });
    }, { rootMargin: '200px' });

    var endEl = qs('#blog-end');
    if (endEl) {
      observer.observe(endEl);
    }

    loadPosts();

    return true;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      try {
        init();
      } catch (e) {
        setCloudStatus('Tag cloud error: ' + (e && e.message ? e.message : String(e)));
      }
    });
  } else {
    try {
      init();
    } catch (e) {
      setCloudStatus('Tag cloud error: ' + (e && e.message ? e.message : String(e)));
    }
  }
})();
