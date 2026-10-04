/**
 * Dashboard UI controller for BEST Bus Transit Insights.
 * Updates KPIs, parameter diagnostic table, validation summary, and empty states.
 */

const Dashboard = {
  currentParameters: [],

  /**
   * Updates KPI card displays.
   */
  updateKPIs(summary) {
    if (!summary) return;

    document.getElementById('valActiveBase').textContent = Utils.formatNumber(summary.total_responses || 0);
    document.getElementById('valPeakDelay').textContent = Utils.formatPercent(summary.peak_delay_pct || 0);
    document.getElementById('valOvercrowding').textContent = Utils.formatPercent(summary.overcrowding_pct || 0);
    document.getElementById('valDigitalPayment').textContent = Utils.formatPercent(summary.digital_payment_pct || 0);
    document.getElementById('valFrequentUsers').textContent = Utils.formatPercent(summary.frequent_users_pct || 0);
    document.getElementById('valWaitTime').textContent = summary.avg_waiting_time || '--';
    document.getElementById('valTopRoute').textContent = summary.top_route || '--';
    document.getElementById('valTopBottleneck').textContent = summary.top_bottleneck || '--';
  },

  /**
   * Updates data validation stats drawer.
   */
  updateValidationStats(validation) {
    if (!validation) return;

    const totalEl = document.getElementById('statTotalRecords');
    const validEl = document.getElementById('statValidRecords');
    const dupEl = document.getElementById('statDuplicates');
    const missEl = document.getElementById('statMissing');
    const pipeEl = document.getElementById('statPipeline');

    if (totalEl) totalEl.textContent = validation.total_records || 0;
    if (validEl) validEl.textContent = validation.valid_records || 0;
    if (dupEl) dupEl.textContent = validation.duplicates_removed || 0;
    if (missEl) missEl.textContent = validation.missing_values_handled || 0;
    if (pipeEl) pipeEl.textContent = validation.status || 'Active';
  },

  /**
   * Initializes and renders parameter diagnostic table.
   */
  updateParameterTable(parameters = []) {
    this.currentParameters = parameters;
    this.filterAndRenderTable();
  },

  /**
   * Filters and renders parameter table based on search input and status filter.
   */
  filterAndRenderTable() {
    const tbody = document.getElementById('parameterTableBody');
    const searchInput = document.getElementById('tableSearchInput');
    const statusFilter = document.getElementById('tableStatusFilter');

    if (!tbody) return;

    const query = (searchInput ? searchInput.value : '').trim().toLowerCase();
    const status = statusFilter ? statusFilter.value : 'all';

    let filtered = this.currentParameters || [];

    if (query) {
      filtered = filtered.filter(p =>
        p.parameter.toLowerCase().includes(query) ||
        p.recommendation.toLowerCase().includes(query) ||
        p.positive_label.toLowerCase().includes(query)
      );
    }

    if (status !== 'all') {
      filtered = filtered.filter(p => p.status === status);
    }

    if (filtered.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-center" style="padding: 2rem; color: #94a3b8;">No matching parameter indicators found.</td></tr>';
      return;
    }

    tbody.innerHTML = filtered.map(param => {
      let statusClass = 'status-acceptable';
      if (param.status === 'High Adoption') statusClass = 'status-high-adoption';
      else if (param.status === 'Operational Concern') statusClass = 'status-operational-concern';
      else if (param.status === 'Critical Deficit') statusClass = 'status-critical-deficit';

      return `
        <tr>
          <td><strong>${param.parameter}</strong></td>
          <td>${param.positive_label} (${param.positive_pct}%)</td>
          <td>${param.negative_label} (${param.negative_pct}%)</td>
          <td><strong style="color: #38bdf8;">${param.positive_pct}%</strong></td>
          <td><span class="status-tag ${statusClass}">${param.status}</span></td>
          <td><small style="color: #cbd5e1;">${param.recommendation}</small></td>
        </tr>
      `;
    }).join('');
  },

  /**
   * Bind parameter table search and status filter listeners.
   */
  initTableListeners() {
    const searchInput = document.getElementById('tableSearchInput');
    const statusFilter = document.getElementById('tableStatusFilter');

    if (searchInput) {
      searchInput.addEventListener('input', Utils.debounce(() => {
        this.filterAndRenderTable();
      }, 200));
    }

    if (statusFilter) {
      statusFilter.addEventListener('change', () => {
        this.filterAndRenderTable();
      });
    }
  }
};
