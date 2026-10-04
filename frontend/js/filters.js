/**
 * Analytical Filters Manager for BEST Bus Transit Insights.
 * Handles filter options population, dynamic state, URL querying, and reset actions.
 */

const Filters = {
  currentFilters: {
    route: 'all',
    user_status: 'all',
    age_group: 'all',
    occupation: 'all',
    frequency: 'all'
  },

  /**
   * Returns copy of active filter state.
   */
  getValues() {
    return { ...this.currentFilters };
  },

  /**
   * Initializes filters and binds event listeners.
   */
  async init(onFilterChangeCallback) {
    const routeSelect = document.getElementById('filterRoute');
    const userStatusSelect = document.getElementById('filterUserStatus');
    const ageSelect = document.getElementById('filterAgeGroup');
    const occupationSelect = document.getElementById('filterOccupation');
    const freqSelect = document.getElementById('filterFrequency');
    const btnApply = document.getElementById('btnApplyFilters');
    const btnReset = document.getElementById('btnResetFilters');

    // Populate dynamic filter options from API
    try {
      const options = await Api.getFilterOptions();
      if (options.routes && options.routes.length > 0 && routeSelect) {
        routeSelect.innerHTML = '<option value="all">All Routes (Corridor)</option>' +
          options.routes.map(r => `<option value="${r}">Route ${r}</option>`).join('');
      }

      if (options.occupations && options.occupations.length > 0 && occupationSelect) {
        occupationSelect.innerHTML = '<option value="all">All Occupations</option>' +
          options.occupations.map(o => `<option value="${o}">${o}</option>`).join('');
      }
    } catch (err) {
      console.warn('Could not load dynamic filter options from API:', err);
    }

    const updateFilterState = () => {
      if (routeSelect) this.currentFilters.route = routeSelect.value;
      if (userStatusSelect) this.currentFilters.user_status = userStatusSelect.value;
      if (ageSelect) this.currentFilters.age_group = ageSelect.value;
      if (occupationSelect) this.currentFilters.occupation = occupationSelect.value;
      if (freqSelect) this.currentFilters.frequency = freqSelect.value;
    };

    if (btnApply) {
      btnApply.addEventListener('click', () => {
        updateFilterState();
        this.updateFilterSummaryText();
        if (onFilterChangeCallback) onFilterChangeCallback(this.getValues());
      });
    }

    if (btnReset) {
      btnReset.addEventListener('click', () => {
        if (routeSelect) routeSelect.value = 'all';
        if (userStatusSelect) userStatusSelect.value = 'all';
        if (ageSelect) ageSelect.value = 'all';
        if (occupationSelect) occupationSelect.value = 'all';
        if (freqSelect) freqSelect.value = 'all';

        this.currentFilters = {
          route: 'all',
          user_status: 'all',
          age_group: 'all',
          occupation: 'all',
          frequency: 'all'
        };
        this.updateFilterSummaryText();
        if (onFilterChangeCallback) onFilterChangeCallback(this.getValues());
      });
    }
  },

  /**
   * Update text showing summary of active filters.
   */
  updateFilterSummaryText() {
    const summaryEl = document.getElementById('activeFilterSummary');
    if (!summaryEl) return;

    const activeList = [];
    if (this.currentFilters.route !== 'all') activeList.push(`Route: ${this.currentFilters.route}`);
    if (this.currentFilters.user_status !== 'all') activeList.push(`Segment: ${this.currentFilters.user_status}`);
    if (this.currentFilters.age_group !== 'all') activeList.push(`Age: ${this.currentFilters.age_group}`);
    if (this.currentFilters.occupation !== 'all') activeList.push(`Occ: ${this.currentFilters.occupation}`);
    if (this.currentFilters.frequency !== 'all') activeList.push(`Freq: ${this.currentFilters.frequency}`);

    if (activeList.length === 0) {
      summaryEl.textContent = 'Showing all responses';
    } else {
      summaryEl.textContent = `Filtered by: ${activeList.join(' | ')}`;
    }
  }
};
