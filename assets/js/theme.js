// Theme Toggle Functionality
(function () {
  // Set theme immediately to prevent flash
  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateToggleButton(theme);
    updateGiscusTheme(theme);
  }

  // Update toggle button state
  function updateToggleButton(theme) {
    const themeToggles = document.querySelectorAll('.theme-toggle');
    if (!themeToggles.length) return;

    const isDark = theme === 'dark';

    themeToggles.forEach(toggle => {
      toggle.setAttribute('aria-pressed', isDark);

      // Update icons
      const icons = toggle.querySelectorAll('.theme-icon');
      if (icons.length) {
        icons.forEach(icon => icon.style.display = 'none');

        const activeIcon = isDark
          ? toggle.querySelector('.theme-icon-sun')
          : toggle.querySelector('.theme-icon-moon');

        if (activeIcon) activeIcon.style.display = 'block';
      }
    });
  }

  // Update Giscus theme
  function updateGiscusTheme(theme) {
    const giscusTheme = theme === 'dark' ? 'dark' : 'light';
    const iframes = document.querySelectorAll('iframe.giscus-frame');
    iframes.forEach(function (iframe) {
      if (iframe.contentWindow) {
        iframe.contentWindow.postMessage({
          giscus: { setConfig: { theme: giscusTheme } }
        }, 'https://giscus.app');
      }
    });
  }

  // Initialize theme
  function initTheme() {
    try {
      const savedTheme = localStorage.getItem('theme');
      // Force 'light' as initial theme unless explicitly saved
      const initialTheme = savedTheme || 'light';
      setTheme(initialTheme);
    } catch (e) {
      console.error('Error initializing theme:', e);
    }
  }

  // Toggle theme
  function toggleTheme() {
    try {
      const current = document.documentElement.getAttribute('data-theme');
      const newTheme = current === 'dark' ? 'light' : 'dark';
      setTheme(newTheme);
    } catch (e) {
      console.error('Error toggling theme:', e);
    }
  }

  // Initialize when DOM is loaded
  document.addEventListener('DOMContentLoaded', function () {
    // Set up event listeners for ALL buttons
    const themeToggles = document.querySelectorAll('.theme-toggle');
    themeToggles.forEach(toggle => {
      toggle.addEventListener('click', toggleTheme);
    });

    // Watch for system theme changes disabled to force light mode preference
    /*
    const colorSchemeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    colorSchemeQuery.addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'light');
      }
    });
    */

    // Initialize theme
    initTheme();
  });

  // Also set theme immediately for faster initial render
  initTheme();

  // Expose function for dynamic content
  window.refreshGiscusTheme = function () {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    updateGiscusTheme(current);
  };
})();
