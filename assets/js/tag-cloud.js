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

  function renderList(posts, filterTag) {
    var listEl = qs('#blog-list');
    if (!listEl) return;

    var shown = posts;
    if (filterTag) {
      shown = posts.filter(function (p) {
        return Array.isArray(p.tags) && p.tags.indexOf(filterTag) !== -1;
      });
    }

    if (!shown.length) {
      listEl.innerHTML = '<div class="blog-list-empty">No posts</div>';
      return;
    }

    // Check language
    var isEn = window.CURRENT_LANG === 'en';

    listEl.innerHTML =
      '<ul class="blog-list-ul">' +
      shown
        .map(function (p) {
          var title = escHtml(p.title || 'Untitled');
          var url = escHtml(p.url || '#');

          // Translation logic for Patents in English mode
          if (isEn && (title.indexOf('专利') !== -1 || (p.tags && p.tags.indexOf('Patent') !== -1))) {
            var idMatch = title.match(/([A-Z]{2}\d+[A-Z]?)/);
            if (idMatch) {
              var id = idMatch[1];
              // Determine type mostly by checking Chinese keywords if present in title
              var type = title.indexOf('待授权') !== -1 ? 'Pending Patent' : 'Granted Patent';
              title = type + ' ' + id;
              url = 'https://patents.google.com/patent/' + id + '/en';
            }
          }

          return '<li class="blog-list-item"><a href="' + url + '"' + (isEn ? ' target="_blank"' : '') + '>' + title + '</a></li>';
        })
        .join('') +
      '</ul>';
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

    // Color palette for word cloud
    var colors = [
      '#2563eb', // blue
      '#dc2626', // red
      '#16a34a', // green
      '#ca8a04', // yellow
      '#9333ea', // purple
      '#ea580c', // orange
      '#0891b2', // cyan
      '#be185d', // pink
      '#059669', // emerald
      '#7c3aed', // violet
      '#c2410c', // orange-red
      '#1e40af', // blue-dark
      '#166534', // green-dark
      '#991b1b', // red-dark
      '#581c87'  // purple-dark
    ];

    var colorMap = Object.create(null);
    var colorIndex = 0;

    var color = function (t) {
      if (activeTag && t === activeTag) return 'var(--link-color)';
      // Assign consistent color to each tag
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

      // Add hover effect: increase font size on mouseover (doesn't change position)
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

      // Click event - must be bound separately
      texts.on('click', function (d) {
        if (!d || !d.text) return;
        // Stop any ongoing transitions
        window.d3.select(this).interrupt();
        if (onPickCallback && typeof onPickCallback === 'function') {
          onPickCallback(d.text);
        }
      });
    }
  }

  function init() {
    var cloudEl = qs('#tag-cloud');
    var listEl = qs('#blog-list');
    if (!cloudEl || !listEl) return;

    var posts = Array.isArray(window.__BLOG_POSTS__) ? window.__BLOG_POSTS__ : [];
    var tags = buildTagStats(posts);

    renderList(posts, '');

    if (!posts.length) {
      setCloudStatus('No posts data');
      return;
    }

    if (!tags.length) {
      setCloudStatus('No tags found in posts');
      return;
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
      renderList(posts, active);
      renderCloud(tags, active, setActive);
    }

    // Expose for external language switcher
    window.refreshPatentList = function () {
      renderList(posts, active);
    };

    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        setActive(active);
      });
    }

    renderCloud(tags, '', setActive);

    window.addEventListener('resize', function () {
      renderCloud(tags, active, setActive);
    });

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
