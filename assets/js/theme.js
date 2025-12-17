// Theme Toggle Functionality
(function() {
  // Set theme immediately to prevent flash
  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    updateToggleButton(theme);
  }

  // Update toggle button state
  function updateToggleButton(theme) {
    const themeToggle = document.querySelector('.theme-toggle');
    if (!themeToggle) return;
    
    const isDark = theme === 'dark';
    themeToggle.setAttribute('aria-pressed', isDark);
    
    // Update icons
    const icons = themeToggle.querySelectorAll('.theme-icon');
    if (!icons.length) return;
    
    icons.forEach(icon => {
      icon.style.display = 'none';
    });
    
    const activeIcon = isDark 
      ? themeToggle.querySelector('.theme-icon-sun') 
      : themeToggle.querySelector('.theme-icon-moon');
      
    if (activeIcon) activeIcon.style.display = 'block';
  }

  // Initialize theme
  function initTheme() {
    try {
      const savedTheme = localStorage.getItem('theme');
      const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
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
  document.addEventListener('DOMContentLoaded', function() {
    // Set up event listeners
    const themeToggle = document.querySelector('.theme-toggle');
    if (themeToggle) {
      themeToggle.addEventListener('click', toggleTheme);
    }

    // Watch for system theme changes
    const colorSchemeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    colorSchemeQuery.addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'light');
      }
    });

    // Initialize theme
    initTheme();
  });

  // Also set theme immediately for faster initial render
  initTheme();
})();
