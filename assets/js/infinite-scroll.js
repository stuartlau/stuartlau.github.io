class InfiniteScroll {
  constructor(options) {
    this.options = {
      containerSelector: null,
      itemSelector: null,
      apiUrl: null,
      pageParam: 'page',
      renderItem: null,
      loadingClass: 'infinite-loading',
      endClass: 'infinite-end',
      errorClass: 'infinite-error',
      threshold: 200,
      initialPage: 1,
      ...options
    };

    this.currentPage = this.options.initialPage;
    this.isLoading = false;
    this.hasMore = true;
    this.observer = null;
    this.items = [];

    this.init();
  }

  init() {
    this.container = document.querySelector(this.options.containerSelector);
    if (!this.container) {
      console.warn('InfiniteScroll: Container not found', this.options.containerSelector);
      return;
    }

    this.setupObserver();
    this.createLoadingIndicator();
    this.createEndIndicator();
  }

  setupObserver() {
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && this.hasMore && !this.isLoading) {
            this.loadMore();
          }
        });
      },
      {
        rootMargin: `${this.options.threshold}px`
      }
    );
  }

  createLoadingIndicator() {
    this.loadingEl = document.createElement('div');
    this.loadingEl.className = this.options.loadingClass;
    this.loadingEl.innerHTML = `
      <div class="infinite-spinner">
        <div class="spinner"></div>
        <span>加载中...</span>
      </div>
    `;
    this.loadingEl.style.cssText = 'text-align: center; padding: 20px; display: none;';
  }

  createEndIndicator() {
    this.endEl = document.createElement('div');
    this.endEl.className = this.options.endClass;
    this.endEl.innerHTML = '<span>— 已经到底啦 —</span>';
    this.endEl.style.cssText = 'text-align: center; padding: 30px; color: #999; display: none;';
  }

  async loadMore() {
    if (this.isLoading || !this.hasMore) return;

    this.isLoading = true;
    this.loadingEl.style.display = 'block';

    try {
      const url = this.buildUrl(this.currentPage);
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (data.data && data.data.length > 0) {
        this.renderItems(data.data);
        this.currentPage++;
        this.hasMore = data.page < data.total_pages;
      } else {
        this.hasMore = false;
      }

      if (!this.hasMore) {
        this.endEl.style.display = 'block';
        this.observer.disconnect();
      }
    } catch (error) {
      console.error('InfiniteScroll: Failed to load more items', error);
      this.loadingEl.querySelector('span').textContent = '加载失败，点击重试';
      this.loadingEl.style.cursor = 'pointer';
      this.loadingEl.onclick = () => this.loadMore();
    } finally {
      this.isLoading = false;
      if (this.hasMore) {
        this.loadingEl.style.display = 'none';
      }
    }
  }

  buildUrl(page) {
    const baseUrl = this.options.apiUrl.replace(`/${this.options.pageParam}/1`, '');
    return `${baseUrl}/page-${page}.json`;
  }

  renderItems(items) {
    items.forEach((item) => {
      const html = this.options.renderItem(item);
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = html;
      const element = tempDiv.firstElementChild;
      element.style.opacity = '0';
      element.style.transform = 'translateY(10px)';
      this.container.appendChild(element);
      document.body.appendChild(tempDiv);

      requestAnimationFrame(() => {
        element.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
      });

      this.items.push(element);
    });

    if (this.observer) {
      this.observer.observe(this.endEl);
    }
  }

  observe() {
    if (this.observer && this.endEl) {
      this.observer.observe(this.endEl);
    }
  }
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = InfiniteScroll;
}
