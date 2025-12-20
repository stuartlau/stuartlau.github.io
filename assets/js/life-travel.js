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

  function normalizeTag(t) {
    return String(t || '').trim();
  }

  function buildTagStats(points) {
    var map = Object.create(null);
    (points || []).forEach(function (p) {
      var tags = Array.isArray(p.tags) ? p.tags : [];
      tags.forEach(function (t) {
        var tag = normalizeTag(t);
        if (!tag || tag === 'Travelling') return;
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
    var el = qs('#life-tag-cloud');
    if (!el) return;
    el.innerHTML = '<div class="tag-cloud-status">' + escHtml(msg) + '</div>';
  }

  function resolveThumb(thumb) {
    if (!thumb) return '';
    var t = String(thumb);
    if (/^https?:\/\//.test(t)) return t;
    if (t.indexOf('//') === 0) return window.location.protocol + t;
    if (t.charAt(0) === '/') return t;
    return '/' + t;
  }

  function renderCloud(tags, activeTag, onPick) {
    var cloudEl = qs('#life-tag-cloud');
    if (!cloudEl) return;

    if (!tags || !tags.length) {
      setCloudStatus('No travel tags');
      return;
    }

    if (!window.d3 || !window.d3.layout || !window.d3.layout.cloud) {
      setCloudStatus('d3/d3-cloud not loaded');
      return;
    }

    cloudEl.innerHTML = '';

    var width = Math.min(920, cloudEl.clientWidth || 920);
    var height = 260;

    var counts = tags.map(function (t) {
      return t.count;
    });
    var min = Math.min.apply(Math, counts);
    var max = Math.max.apply(Math, counts);

    var size = window.d3.scale
      .sqrt()
      .domain([min || 1, max || 1])
      .range([12, 52]);

    var color = function (t) {
      if (activeTag && t === activeTag) return 'var(--link-color)';
      return 'var(--text-color)';
    };

    var layout = window.d3.layout
      .cloud()
      .size([width, height])
      .words(
        tags.map(function (t) {
          return { text: t.tag, size: size(t.count), count: t.count };
        })
      )
      .padding(2)
      .rotate(function () {
        return 0;
      })
      .font('Inter')
      .fontSize(function (d) {
        return d.size;
      })
      .on('end', draw);

    layout.start();

    function draw(words) {
      var svg = window.d3
        .select(cloudEl)
        .append('svg')
        .attr('width', width)
        .attr('height', height);

      var g = svg
        .append('g')
        .attr('transform', 'translate(' + width / 2 + ',' + height / 2 + ')');

      g.selectAll('text')
        .data(words)
        .enter()
        .append('text')
        .style('font-size', function (d) {
          return d.size + 'px';
        })
        .style('font-family', 'Inter')
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
        })
        .append('title')
        .text(function (d) {
          return d.text + ' (' + d.count + ')';
        });

      g.selectAll('text').on('click', function (d) {
        if (!d || !d.text) return;
        onPick(d.text);
      });
    }
  }

  function initMap(points, onReady) {
    var mapEl = qs('#life-travel-map');
    if (!mapEl) return null;

    if (!window.L) {
      mapEl.innerHTML = '<div class="travel-map-status">Leaflet not loaded</div>';
      return null;
    }

    var map = window.L.map(mapEl, {
      scrollWheelZoom: false,
      worldCopyJump: true
    });

    window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap'
    }).addTo(map);

    var layers = [];
    var markersByTag = Object.create(null);

    function iconForStatus(status) {
      var s = String(status || 'visited').toLowerCase();
      var cls = s === 'planned' ? 'travel-marker travel-marker-planned' : 'travel-marker travel-marker-visited';
      return window.L.divIcon({
        className: cls,
        iconSize: [14, 14]
      });
    }

    (points || []).forEach(function (p) {
      var loc = p && p.location;
      if (!Array.isArray(loc) || loc.length < 2) return;
      var lng = Number(loc[0]);
      var lat = Number(loc[1]);
      if (!isFinite(lng) || !isFinite(lat)) return;

      var ll = [lat, lng];
      var title = escHtml(p.title || '');
      var url = escHtml(p.url || '#');
      var thumb = resolveThumb(p.thumbnail);

      var popup = '<div class="travel-popup">';
      if (thumb) popup += '<div class="travel-popup-thumb"><img src="' + escHtml(thumb) + '" alt="" loading="lazy" /></div>';
      popup += '<div class="travel-popup-title"><a href="' + url + '">' + title + '</a></div>';
      popup += '</div>';

      var marker = window.L.marker(ll, {
        icon: iconForStatus(p.status)
      }).bindPopup(popup);

      marker.addTo(map);
      layers.push(marker);

      var tags = Array.isArray(p.tags) ? p.tags : [];
      tags.forEach(function (t) {
        var tag = normalizeTag(t);
        if (!tag || tag === 'Travelling') return;
        if (!markersByTag[tag]) markersByTag[tag] = [];
        markersByTag[tag].push(marker);
      });
    });

    if (layers.length) {
      var group = window.L.featureGroup(layers);
      map.fitBounds(group.getBounds().pad(0.2));
    } else {
      map.setView([0, 0], 2);
    }

    function setHighlight(tag) {
      Object.keys(markersByTag).forEach(function (k) {
        (markersByTag[k] || []).forEach(function (m) {
          var el = m.getElement && m.getElement();
          if (!el) return;
          el.classList.remove('is-highlighted');
          el.classList.remove('is-dimmed');
        });
      });

      if (!tag) return;

      Object.keys(markersByTag).forEach(function (k) {
        (markersByTag[k] || []).forEach(function (m) {
          var el = m.getElement && m.getElement();
          if (!el) return;
          if (k === tag) {
            el.classList.add('is-highlighted');
          } else {
            el.classList.add('is-dimmed');
          }
        });
      });

      var ms = markersByTag[tag] || [];
      if (ms.length) {
        var fg = window.L.featureGroup(ms);
        map.fitBounds(fg.getBounds().pad(0.35), { animate: true, duration: 0.6 });
      }
    }

    onReady && onReady({ map: map, setHighlight: setHighlight });
    return map;
  }

  function init() {
    var wrap = qs('#life-travel-wrap');
    if (!wrap) return;

    setCloudStatus('Loading...');

    fetch('/travel-points.json')
      .then(function (r) {
        if (!r.ok) throw new Error('points.json fetch failed');
        return r.json();
      })
      .then(function (points) {
        points = Array.isArray(points) ? points : [];
        if (!points.length) {
          setCloudStatus('No travel points (missing location in posts?)');
        }

        var tags = buildTagStats(points);

        var active = '';
        var clearBtn = qs('#life-tag-cloud-clear');
        var activeEl = qs('#life-tag-cloud-active');

        var mapApi = { setHighlight: function () {} };
        initMap(points, function (api) {
          mapApi = api || mapApi;
        });

        function setActive(tag) {
          active = active === tag ? '' : tag;
          if (clearBtn) clearBtn.hidden = !active;
          if (activeEl) {
            activeEl.hidden = !active;
            activeEl.textContent = active ? 'Filter: ' + active : '';
          }

          renderCloud(tags, active, setActive);
          mapApi.setHighlight(active);
        }

        if (clearBtn) {
          clearBtn.addEventListener('click', function () {
            setActive(active);
          });
        }

        renderCloud(tags, '', setActive);
      })
      .catch(function (e) {
        setCloudStatus('Travel map error: ' + (e && e.message ? e.message : String(e)));
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
