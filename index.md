---
layout: page
---

## About Me
<img src="/images/linkedin_avatar.jpg" class="floatpic">
<div class="en post-container">
<style>
    .company-link-container {
        position: relative;
        display: inline-block;
        border-bottom: 1px dashed #666; 
        cursor: help;
    }

    .company-link-container .company-tooltip {
        visibility: hidden;
        width: 450px; /* Wider */
        max-width: 90vw; /* Responsive width */
        background-color: #222;
        color: #fff;
        text-align: left;
        border-radius: 8px;
        padding: 12px; /* Less padding for 'shorter' feel */
        position: absolute;
        z-index: 1000;
        bottom: 100%; 
        left: 50%;
        transform: translateX(-50%) translateY(-10px);
        opacity: 0;
        transition: opacity 0.3s, transform 0.3s;
        font-size: 0.85em;
        line-height: 1.5;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.3);
        pointer-events: none; 
        font-weight: normal;
    }
    
    /* Arrow */
    .company-link-container .company-tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -6px;
        border-width: 6px;
        border-style: solid;
        border-color: #222 transparent transparent transparent;
    }

    /* Bridge */
    .company-link-container .company-tooltip::before {
        content: "";
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        height: 20px; 
    }

    .company-link-container:hover .company-tooltip,
    .company-link-container.touch-active .company-tooltip {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(-5px);
        pointer-events: auto;
    }

    /* Mobile adjustments */
    @media (max-width: 600px) {
        .company-link-container .company-tooltip {
            /* Adjust positioning if needed for small screens, 
               but max-width 90vw + left 50% usually works unless at edges. 
               Since these are inline, we trust the flow. */
            white-space: normal;
        }
    }
</style>
<script>
document.addEventListener("DOMContentLoaded", function() {
    // Mobile touch support for tooltips
    const containers = document.querySelectorAll('.company-link-container');
    
    // Add touch listener
    containers.forEach(container => {
        container.addEventListener('touchend', function(e) {
             // Simple interaction: First tap shows tooltip, Second tap follows link
             if (!this.classList.contains('touch-active')) {
                 e.preventDefault(); // Stop link navigation
                 // Close others
                 containers.forEach(c => c.classList.remove('touch-active'));
                 this.classList.add('touch-active');
             }
             // If already active, basic link click behavior proceeds
        });
    });
    
    // Close on outside touch
    document.addEventListener('touchstart', function(e) {
        if (!e.target.closest('.company-link-container')) {
            containers.forEach(c => c.classList.remove('touch-active'));
        }
    });
});
</script>
    <p>
       <strong>Stuart Lau</strong><span id="title-animal-icon" style="display:inline-block; width:28px; height:28px; vertical-align:text-bottom; margin-left:8px; cursor: pointer;" title="Click for a new friend!"></span> holds a Master of Engineering in Information Security from <a href="https://www.bupt.edu.cn">Beijing University of Posts and Telecommunications</a>. He has worked successively at 
       
       <span class="company-link-container">
           <a href="https://www.zdns.cn/">ZDNS</a>
           <span class="company-tooltip">
               In 2012, as a core engineer of the founding team, he developed <a href="https://www.zdns.cn/tldcloud.html" style="color: #4db8ff;">TLD Cloud</a>, a new gTLD registry cloud service platform that currently ranks 4th globally (as per <a href="https://ntldstats.com/backend" style="color: #4db8ff;">ntldstats.com</a>), from scratch. He was deeply involved in the engineering design of RFC standard protocols, server-side architecture design, and the development of core capabilities required for top-level domain registries such as EPP, WHOIS, DNS, and ESCROW. He completed the platform's development and testing, obtained acceptance and authorization from the Internet Corporation for Assigned Names and Numbers (<a href="https://www.icann.org/" style="color: #4db8ff;">ICANN</a>), and facilitated the integration and operation of several new top-level domains (e.g., .top, .wang, .ren, .中信) by connecting them to the <a href="https://www.internic.net/domain/root.zone" style="color: #4db8ff;">DNS root name servers</a> for hosting and operation.
           </span>
       </span>,

       <span class="company-link-container">
           <a href="https://www.xiaomi.com">Xiaomi</a>
           <span class="company-tooltip">
               In 2014, joined Xiaomi as a Senior Developer and Architect for Xiaomi Game Center backend projects. He was responsible for the design and development of server-side architecture and platformization for the Xiaomi Game Center APP, game operation platforms, and other game infrastructure services. This covered C-end products such as the Xiaomi Game Center APP and Xiaomi E-Sports APP, as well as B-end platforms including game operation platforms and joint-operation platforms, with an overall DAU (Daily Active Users) of tens of millions.
           </span>
       </span>, 

       <span class="company-link-container">
           <a href="https://www.amazon.com">Amazon</a>
           <span class="company-tooltip">
               In 2017, joined Amazon and worked in the Supply Chain Optimization Technology (SCOT) team. He was primarily responsible for providing support in automated warehouse management, scheduling and allocation, and pricing strategies for tens of millions of products across Amazon's global operations (North America, Europe, Japan, and China). This supported Amazon's retail business and FBA (Fulfillment by Amazon) services, resulting in tens of millions of U.S. dollars in annual savings for Amazon. Core technologies included massive data analysis, machine learning, optimization algorithms, economic models, large-scale distributed systems, and AWS cloud services.
           </span>
       </span>, 

       <span class="company-link-container">
           <a href="https://www.kuaishou.com">Kuaishou</a>
           <span class="company-tooltip">
               In 2018, joined Kuaishou as the Technical Lead, spearheading the team in building Kuaishou's Instant Messaging (IM) Cloud platform from scratch. As an all-in-one IM solution platform, it provides end-to-end IM+RTC capabilities covering numerous scenarios including social networking, communities, customer service, office collaboration, gaming, and paid consulting. It offers C-end (API, Android, iOS, Web, Mini Programs, etc.) and B-end (API, B-end workbench, etc.) integration methods. The IM Cloud supports over 30 business lines including Kuaishou APP/Lite APP, Kuaishou's office software Kim, e-commerce customer service, commercial customer service, the overseas Kwai APP, and other incubated ecosystem products (ACGN, gaming, news).
           </span>
       </span>, and 

       <span class="company-link-container">
           <a href="https://www.xiaohongshu.com">Xiaohongshu</a>
           <span class="company-tooltip">
               In 2024, joined Xiaohongshu as the Backend Lead for Social Interaction R&D, overseeing the research, development, and management of Xiaohongshu's social interaction backend team. He supports the business development of Xiaohongshu's social networking initiatives, delivering interactive capabilities such as user messaging, group chat interactions, system notifications, and innovative AI services to over 120 million DAU users across the domestic Xiaohongshu APP and the overseas RedNote APP.
           </span>
       </span>.
       
       Boasting over a decade of extensive experience in the internet industry coupled with years of team management expertise, he holds <strong><a href="/publications/index.html">over 120 authorized technical invention patents</a></strong> as the first inventor. These patents span diverse domains including instant messaging, social networking, short-video, live streaming, gaming, algorithm engineering, DNS, and network infrastructure, with authorizations in China, the United States, Europe, Japan, and Russia.
    </p>



</div>

<br>
<hr>

## Patent

{% assign all_posts = site.pages | where: "layout", "post" %}
{% assign granted_count = 0 %}
{% assign pending_count = 0 %}
{% for p in all_posts %}
  {% if p.url contains '/blogs/' %}
    {% if p.title contains '待授权专利' %}
      {% assign pending_count = pending_count | plus: 1 %}
    {% elsif p.title contains '授权专利' %}
      {% assign granted_count = granted_count | plus: 1 %}
    {% endif %}
  {% endif %}
{% endfor %}

<p style="font-size: 1.1em; font-weight: 500; margin-bottom: 1.5rem;">
  已授权（{{ granted_count }}个）、待授权（{{ pending_count }}个）
</p>

<div class="tag-cloud-wrap">
  <div class="tag-cloud-head">
    <div class="tag-cloud-title">Patent Tags Cloud</div>
    <button id="tag-cloud-clear" type="button" class="tag-cloud-clear" hidden>Clear</button>
    <div id="tag-cloud-active" class="tag-cloud-active" hidden></div>
  </div>
  <div id="tag-cloud" class="tag-cloud"></div>
</div>

<!-- Container for filtered results when a tag is clicked -->
<div id="blog-list" class="blog-list"></div>

{%- assign patent_posts = site.pages | where: "layout", "post" | where_exp: "p", "p.url contains '/blogs/'" | where_exp: "p", "p.tags contains 'Patent'" -%}

<script>
  window.__BLOG_POSTS__ = [
    {%- for p in patent_posts -%}
      {
        title: {{ p.title | default: p.url | jsonify }},
        url: {{ p.url | relative_url | jsonify }},
        date: {{ p.date | date_to_xmlschema | jsonify }},
        tags: {{ p.tags | default: empty | jsonify }}
      }{%- unless forloop.last -%},{%- endunless -%}
    {%- endfor -%}
  ];
</script>

<script src="https://cdn.jsdelivr.net/npm/d3@3.5.17/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3-cloud@1/build/d3.layout.cloud.js"></script>
<script src="{{ site.url }}/assets/js/tag-cloud.js"></script>

<br>

---
## Conference Paper
- Shuo Liu, Qiaoyan Wen, <a href="https://ieeexplore.ieee.org/abstract/document/6155893/">Distributed cluster
  authentication model based on CAS</a>
  <em>2011 4th IEEE International Conference on Broadband Network and Multimedia
  Technology(<strong>IEEE</strong>)</em>, 2012
<br>

---
## Community Contribution
- <a href="https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=180194">OpenDNSSEC 1.4.1 Bugfixes, 2013</a>