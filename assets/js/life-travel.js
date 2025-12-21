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
    // Handle absolute URLs
    if (/^https?:\/\//.test(t)) return t;
    if (t.indexOf('//') === 0) return window.location.protocol + t;
    // Handle paths starting with /
    if (t.charAt(0) === '/') return t;
    // Handle paths like "img/in-post/xxx.jpg" -> "/images/in-post/xxx.jpg"
    if (t.indexOf('img/') === 0) {
      return '/images/' + t.substring(4);
    }
    // Default: add leading /
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
      .on('end', function(words) {
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

      // Add hover effect: increase font size on mouseover (doesn't change position)
      texts.on('mouseenter', function(d) {
        var self = window.d3.select(this);
        var originalSize = parseFloat(self.attr('data-original-size'));
        self.transition()
          .duration(200)
          .style('font-size', (originalSize * 1.3) + 'px');
      });

      texts.on('mouseleave', function(d) {
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
    var pointsByLocation = Object.create(null);

    function iconForStatus(status) {
      var s = String(status || 'visited').toLowerCase();
      var cls = s === 'planned' ? 'travel-marker travel-marker-planned' : 'travel-marker travel-marker-visited';
      return window.L.divIcon({
        className: cls,
        iconSize: [14, 14]
      });
    }

    // Group points by location (round to 4 decimal places to handle slight variations)
    (points || []).forEach(function (p) {
      var loc = p && p.location;
      if (!Array.isArray(loc) || loc.length < 2) return;
      var lng = Number(loc[0]);
      var lat = Number(loc[1]);
      if (!isFinite(lng) || !isFinite(lat)) return;

      // Round coordinates to group nearby points
      var roundedLng = Math.round(lng * 10000) / 10000;
      var roundedLat = Math.round(lat * 10000) / 10000;
      var locKey = roundedLat + ',' + roundedLng;

      if (!pointsByLocation[locKey]) {
        pointsByLocation[locKey] = [];
      }
      pointsByLocation[locKey].push(p);
    });

    // Create markers for each location
    Object.keys(pointsByLocation).forEach(function (locKey) {
      var locationPoints = pointsByLocation[locKey];
      if (!locationPoints.length) return;

      var firstPoint = locationPoints[0];
      var loc = firstPoint.location;
      var lng = Number(loc[0]);
      var lat = Number(loc[1]);
      var ll = [lat, lng];

      // Build popup content for all points at this location
      var popup = '<div class="travel-popup">';
      
      if (locationPoints.length === 1) {
        // Single point - show thumbnail if available
        var p = locationPoints[0];
        var thumb = resolveThumb(p.thumbnail);
        if (thumb) {
          popup += '<div class="travel-popup-thumb"><img src="' + escHtml(thumb) + '" alt="" loading="lazy" /></div>';
        }
        popup += '<div class="travel-popup-title"><a href="' + escHtml(p.url || '#') + '">' + escHtml(p.title || '') + '</a></div>';
      } else {
        // Multiple points - show list
        popup += '<div class="travel-popup-multiple">';
        popup += '<div class="travel-popup-count">' + locationPoints.length + ' posts</div>';
        locationPoints.forEach(function (p) {
          var thumb = resolveThumb(p.thumbnail);
          popup += '<div class="travel-popup-item">';
          if (thumb) {
            popup += '<div class="travel-popup-item-thumb"><img src="' + escHtml(thumb) + '" alt="" loading="lazy" /></div>';
          }
          popup += '<div class="travel-popup-item-title"><a href="' + escHtml(p.url || '#') + '">' + escHtml(p.title || '') + '</a></div>';
          popup += '</div>';
        });
        popup += '</div>';
      }
      popup += '</div>';

      // Use status from first point (or most recent)
      var status = locationPoints[0].status || 'visited';
      var marker = window.L.marker(ll, {
        icon: iconForStatus(status)
      }).bindPopup(popup, {
        maxWidth: 400,
        className: 'travel-popup-wrapper'
      });

      marker.addTo(map);
      layers.push(marker);

      // Add tags from all points at this location
      locationPoints.forEach(function (p) {
        var tags = Array.isArray(p.tags) ? p.tags : [];
        tags.forEach(function (t) {
          var tag = normalizeTag(t);
          if (!tag || tag === 'Travelling') return;
          if (!markersByTag[tag]) markersByTag[tag] = [];
          if (markersByTag[tag].indexOf(marker) === -1) {
            markersByTag[tag].push(marker);
          }
        });
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
