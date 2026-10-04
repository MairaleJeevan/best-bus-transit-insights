/**
 * API client service for communicating with Flask backend.
 */

const Api = {
  baseUrl: '/api',

  /**
   * Generic fetch wrapper with JSON parsing and error handling.
   */
  async request(endpoint, options = {}) {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        headers: {
          'Accept': 'application/json',
          ...(options.headers || {})
        },
        ...options
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.message || `HTTP Error ${response.status}`);
      }
      return data;
    } catch (error) {
      console.error(`[API Error] ${endpoint}:`, error);
      throw error;
    }
  },

  /**
   * Health check.
   */
  async getHealth() {
    return this.request('/health');
  },

  /**
   * Fetch complete analytics with filters.
   */
  async getAnalytics(filterParams = {}) {
    const query = new URLSearchParams();
    Object.entries(filterParams).forEach(([key, value]) => {
      if (value && value !== 'all') {
        query.append(key, value);
      }
    });
    const queryString = query.toString() ? `?${query.toString()}` : '';
    return this.request(`/analytics${queryString}`);
  },

  /**
   * Fetch filter option lists (routes, occupations, age groups).
   */
  async getFilterOptions() {
    const [routes, occupations, ageGroups] = await Promise.all([
      this.request('/routes'),
      this.request('/occupations'),
      this.request('/age-groups')
    ]);
    return {
      routes: routes.routes || [],
      occupations: occupations.occupations || [],
      ageGroups: ageGroups.age_groups || []
    };
  },

  /**
   * Trigger backend dataset refresh.
   */
  async refreshData() {
    return this.request('/refresh', { method: 'POST' });
  },

  /**
   * Upload CSV file to backend.
   */
  async uploadCSV(formData) {
    const response = await fetch(`${this.baseUrl}/upload-csv`, {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'CSV Upload failed');
    }
    return data;
  }
};
