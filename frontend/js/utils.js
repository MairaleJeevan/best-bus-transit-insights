/**
 * Utility functions for BEST Bus Transit Insights Frontend.
 */

const Utils = {
  /**
   * Format number with comma separators.
   */
  formatNumber(val) {
    if (val === null || val === undefined || isNaN(val)) return '--';
    return Number(val).toLocaleString();
  },

  /**
   * Format percentage string.
   */
  formatPercent(val) {
    if (val === null || val === undefined || isNaN(val)) return '--%';
    return `${Number(val).toFixed(1)}%`;
  },

  /**
   * Show notification toast.
   */
  showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(50px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },

  /**
   * Debounce helper function.
   */
  debounce(func, wait) {
    let timeout;
    return function (...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }
};
