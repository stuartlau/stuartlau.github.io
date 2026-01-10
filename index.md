---
layout: page
---

<h2 id="about-header-cn">关于我</h2>
<h2 id="about-header-en" style="display:none;">About Me</h2>
<img src="/images/linkedin_avatar.jpg" class="floatpic">

<div style="font-size: 0.9rem; text-align: right; margin-bottom: 0;">
    <span id="lang-btn-cn" onclick="switchLang('cn')" style="cursor: pointer; font-weight: bold; color: #333;">中文</span> 
    <span style="color: #ccc; margin: 0 4px;">/</span> 
    <span id="lang-btn-en" onclick="switchLang('en')" style="cursor: pointer; color: #999;">EN</span>
</div>

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
            white-space: normal;
            position: fixed;
            left: 50%;
            top: 50%;
            bottom: auto;
            transform: translate(-50%, -50%);
            width: 85vw;
            max-width: 400px;
            z-index: 9999;
        }
        
        .company-link-container:hover .company-tooltip,
        .company-link-container.touch-active .company-tooltip {
            transform: translate(-50%, -50%); /* Override hover transform */
        }
        
        /* Hide arrow on mobile as position is detached */
        .company-link-container .company-tooltip::after {
            display: none;
        }
    }
</style>
<script>
window.CURRENT_LANG = 'cn'; // Default

function switchLang(lang) {
    window.CURRENT_LANG = lang;
    
    var showCn = (lang === 'cn');
    var displayCn = showCn ? 'block' : 'none';
    var displayEn = showCn ? 'none' : 'block';
    
    // Helper to toggle pairs
    function togglePair(idCn, idEn, mode) {
        var elCn = document.getElementById(idCn);
        var elEn = document.getElementById(idEn);
        if (elCn) elCn.style.display = (mode || displayCn);
        if (elEn) elEn.style.display = (showCn ? 'none' : (mode || 'block'));
    }

    // Toggle Content
    togglePair('about-header-cn', 'about-header-en');
    togglePair('about-content-cn', 'about-content-en');
    togglePair('patent-header-cn', 'patent-header-en');
    togglePair('patent-stats-cn', 'patent-stats-en');
    togglePair('paper-header-cn', 'paper-header-en');
    togglePair('community-header-cn', 'community-header-en');

    // Cloud title is inline
    var cloudCn = document.getElementById('patent-cloud-title-cn');
    var cloudEn = document.getElementById('patent-cloud-title-en');
    if (cloudCn) cloudCn.style.display = showCn ? 'inline' : 'none';
    if (cloudEn) cloudEn.style.display = showCn ? 'none' : 'inline';

    // Toggle Button Style
    var btnCn = document.getElementById('lang-btn-cn');
    var btnEn = document.getElementById('lang-btn-en');
    if (btnCn && btnEn) {
        btnCn.style.fontWeight = showCn ? 'bold' : 'normal';
        btnCn.style.color = showCn ? '#333' : '#999';
        btnEn.style.fontWeight = showCn ? 'normal' : 'bold';
        btnEn.style.color = showCn ? '#999' : '#333';
    }
    
    // Refresh Patent List for translation
    if (window.refreshPatentList) {
        window.refreshPatentList();
    }
}

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

    // Random animal icon logic (reusing or simple inline if needed, but search.js has it)
    // Actually the icon logic in search.js works on ID 'title-animal-icon', so putting it here works.
});
</script>

    <div id="about-content-cn">
        <p>
           <strong>Stuart Lau</strong><span id="title-animal-icon-cn" class="title-animal-icon" style="display:inline-block; width:28px; height:28px; vertical-align:text-bottom; margin-left:8px; cursor: pointer;" title="点击发现新朋友！"></span> 拥有<a href="https://www.bupt.edu.cn">北京邮电大学</a>信息安全工程硕士学位。他先后就职于
           
           <span class="company-link-container">
               <a href="https://www.zdns.cn/">ZDNS</a>
               <span class="company-tooltip">
                   2012年，作为创始团队的核心工程师，他从零开始开发了新的 gTLD 注册局云服务平台 <a href="https://www.zdns.cn/tldcloud.html" style="color: #4db8ff;">TLD Cloud</a>（目前在 <a href="https://ntldstats.com/backend" style="color: #4db8ff;">ntldstats.com</a> 全球排名第四）。他深度参与了 RFC 标准协议的工程设计、服务端架构设计以及顶级域名注册局核心能力（如 EPP、WHOIS、DNS、ESCROW）的开发。完成了平台的开发测试，通过了 ICANN（<a href="https://www.icann.org/" style="color: #4db8ff;">互联网名称与数字地址分配机构</a>）的验收与授权，并通过对接 <a href="https://www.internic.net/domain/root.zone" style="color: #4db8ff;">DNS 根名字服务器</a>，协助 .top、.wang、.ren、.中信 等多个新顶级域名的上线运营。
               </span>
           </span>、
    
           <span class="company-link-container">
               <a href="https://www.xiaomi.com">小米</a>
               <span class="company-tooltip">
                   2014年加入小米，担任小米游戏中心后端项目的高级开发人员和架构师。负责小米游戏中心 APP、游戏运营平台等基础设施服务的服务器端架构设计和平台化开发。涵盖小米游戏中心 APP、小米电竞 APP 等 C 端产品，以及游戏运营平台、联运平台等 B 端平台，整体日活跃用户（DAU）数千万。
               </span>
           </span>、
    
           <span class="company-link-container">
               <a href="https://www.amazon.com">亚马逊</a>
               <span class="company-tooltip">
                   2017年加入亚马逊，任职于供应链优化技术（SCOT）团队。主要负责为亚马逊全球业务（北美、欧洲、日本和中国）的数千万种商品提供自动化仓库管理、调度分配和定价策略支持。这支持了亚马逊的零售业务和 FBA（亚马逊物流）服务，每年为亚马逊节省数千万美元。核心技术包括海量数据分析、机器学习、优化算法、经济模型、大规模分布式系统和 AWS 云服务。
               </span>
           </span>、
    
           <span class="company-link-container">
               <a href="https://www.kuaishou.com">快手</a>
               <span class="company-tooltip">
                   2018年加入快手担任技术负责人，带领团队从零搭建快手即时通讯（IM）云平台。作为一站式 IM 解决方案平台，提供端到端的 IM+RTC 能力，覆盖社交、社区、客服、办公协作、游戏、付费咨询等众多场景。提供 C 端（API、Android、iOS、Web、小程序等）和 B 端集成方式。IM 云支持快手 APP/极速版 APP、快手办公软件 Kim、电商客服、商业化客服、海外 Kwai APP 以及其他孵化生态产品（二次元、游戏、新闻）等 30 多条业务线。
               </span>
           </span>
           
           以及
    
           <span class="company-link-container">
               <a href="https://www.xiaohongshu.com">小红书</a>
               <span class="company-tooltip">
                   2024年加入小红书，担任社交互动研发后端负责人，负责小红书社交互动后端团队的研发和管理工作。支持小红书社交业务发展，为国内小红书 APP 和海外 RedNote APP 的超过 1.2 亿 DAU 用户提供用户消息、群聊互动、系统通知以及创新 AI 服务等互动能力。
               </span>
           </span>。
           
           他拥有超过十年的互联网行业丰富经验以及多年的团队管理经验，作为第一发明人拥有 超过 120 项授权技术发明专利。这些专利涵盖即时通讯、社交网络、短视频、直播、游戏、算法工程、DNS 和网络基础设施等多个领域，并在中国、美国、欧洲、日本和俄罗斯获得授权。
        </p>
    </div>

    <div id="about-content-en" style="display: none;">
        <p>
           <strong>Stuart Lau</strong><span id="title-animal-icon" class="title-animal-icon" style="display:inline-block; width:28px; height:28px; vertical-align:text-bottom; margin-left:8px; cursor: pointer;" title="Click for a new friend!"></span> holds a Master of Engineering in Information Security from <a href="https://www.bupt.edu.cn">Beijing University of Posts and Telecommunications</a>. He has worked successively at 
           
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
           
           Boasting over a decade of extensive experience in the internet industry coupled with years of team management expertise, he holds over 120 authorized technical invention patents as the first inventor. These patents span diverse domains including instant messaging, social networking, short-video, live streaming, gaming, algorithm engineering, DNS, and network infrastructure, with authorizations in China, the United States, Europe, Japan, and Russia.
        </p>
    </div>
</div>

<br>
<hr>

<h2 id="patent-header-cn">专利</h2>
<h2 id="patent-header-en" style="display:none;">Patents</h2>

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

<div class="tag-cloud-wrap">
  <div class="tag-cloud-head">
    <div class="tag-cloud-title">
        <span id="patent-cloud-title-cn">专利图谱</span>
        <span id="patent-cloud-title-en" style="display:none;">Patents Cloud</span>
    </div>
    <button id="tag-cloud-clear" type="button" class="tag-cloud-clear" hidden>Clear</button>
    <div id="tag-cloud-active" class="tag-cloud-active" hidden></div>
  </div>
  <div id="tag-cloud" class="tag-cloud"></div>
</div>

<p id="patent-stats-cn" style="margin-top: 1.5rem; margin-bottom: 1.5rem;">
  已授权（{{ granted_count }}个）、待授权（{{ pending_count }}个）
</p>
<p id="patent-stats-en" style="margin-top: 1.5rem; margin-bottom: 1.5rem; display:none;">
    Granted ({{ granted_count }}), Pending ({{ pending_count }})
</p>

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
<script src="{{ site.url }}/assets/js/patent-toggle.js"></script>

<br>

---
<h2 id="paper-header-cn">会议论文</h2>
<h2 id="paper-header-en" style="display:none;">Conference Paper</h2>
- Shuo Liu, Qiaoyan Wen, <a href="https://ieeexplore.ieee.org/abstract/document/6155893/">Distributed cluster
  authentication model based on CAS</a>
  <em>2011 4th IEEE International Conference on Broadband Network and Multimedia
  Technology(<strong>IEEE</strong>)</em>, 2012
<br>

---
<h2 id="community-header-cn">社区贡献</h2>
<h2 id="community-header-en" style="display:none;">Community Contribution</h2>
- <a href="https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=180194">OpenDNSSEC 1.4.1 Bugfixes, 2013</a>