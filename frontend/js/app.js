/**
 * Main application orchestrator for BEST Bus Transit Insights.
 * Integrates API client, Filters, Charts, Dashboard UI, Auto-refresh, and CSV Export.
 */

let autoRefreshTimer = null;

document.addEventListener('DOMContentLoaded', async () => {
  console.log('BEST Bus Transit Insights Dashboard Initializing...');

  // Initialize Chart.js defaults
  Charts.initDefaults();

  // Initialize Table search/status filter listeners
  Dashboard.initTableListeners();

  // Initialize filter handlers
  await Filters.init(async (filters) => {
    await loadDashboardData(filters);
  });

  // Modal setup
  const btnUploadModal = document.getElementById('btnUploadModal');
  const btnCloseModal = document.getElementById('btnCloseModal');
  const btnCancelUpload = document.getElementById('btnCancelUpload');
  const uploadModal = document.getElementById('uploadModal');
  const uploadForm = document.getElementById('uploadCsvForm');
  const csvFileInput = document.getElementById('csvFileInput');
  const selectedFileName = document.getElementById('selectedFileName');

  if (btnUploadModal && uploadModal) {
    btnUploadModal.addEventListener('click', () => uploadModal.classList.remove('hidden'));
    if (btnCloseModal) btnCloseModal.addEventListener('click', () => uploadModal.classList.add('hidden'));
    if (btnCancelUpload) btnCancelUpload.addEventListener('click', () => uploadModal.classList.add('hidden'));
  }

  if (csvFileInput && selectedFileName) {
    csvFileInput.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        selectedFileName.textContent = `Selected: ${e.target.files[0].name} (${(e.target.files[0].size / 1024).toFixed(1)} KB)`;
        selectedFileName.classList.remove('hidden');
      }
    });
  }

  // Handle CSV Upload Form Submission
  if (uploadForm) {
    uploadForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!csvFileInput.files || csvFileInput.files.length === 0) {
        Utils.showToast('Please select a CSV file to upload.', 'error');
        return;
      }

      const formData = new FormData();
      formData.append('file', csvFileInput.files[0]);

      const submitBtn = document.getElementById('btnSubmitUpload');
      try {
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = 'Uploading...';
        }
        const res = await Api.uploadCSV(formData);
        Utils.showToast(res.message || 'Dataset uploaded successfully!', 'success');
        if (uploadModal) uploadModal.classList.add('hidden');
        uploadForm.reset();
        if (selectedFileName) selectedFileName.classList.add('hidden');
        await loadDashboardData(Filters.getValues());
      } catch (err) {
        Utils.showToast(err.message || 'Upload failed', 'error');
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = 'Upload & Analyze';
        }
      }
    });
  }

  // Refresh Button setup
  const btnRefresh = document.getElementById('btnRefreshData');
  if (btnRefresh) {
    btnRefresh.addEventListener('click', async () => {
      try {
        btnRefresh.disabled = true;
        btnRefresh.classList.add('loading');
        Utils.showToast('Refreshing survey data from source...', 'info');
        await Api.refreshData();
        await loadDashboardData(Filters.getValues());
        Utils.showToast('Survey dataset successfully updated!', 'success');
      } catch (err) {
        Utils.showToast(err.message || 'Failed to refresh data', 'error');
      } finally {
        btnRefresh.disabled = false;
        btnRefresh.classList.remove('loading');
      }
    });
  }

  // Auto-Refresh Selector setup
  const autoRefreshSelect = document.getElementById('autoRefreshSelect');
  if (autoRefreshSelect) {
    autoRefreshSelect.addEventListener('change', (e) => {
      const intervalSec = parseInt(e.target.value, 10);
      if (autoRefreshTimer) {
        clearInterval(autoRefreshTimer);
        autoRefreshTimer = null;
      }

      if (intervalSec > 0) {
        Utils.showToast(`Auto-refresh enabled (${intervalSec}s)`, 'info');
        autoRefreshTimer = setInterval(async () => {
          console.log(`[Auto-Refresh] Triggered every ${intervalSec}s...`);
          try {
            await Api.refreshData();
            await loadDashboardData(Filters.getValues());
          } catch (err) {
            console.warn('[Auto-Refresh Error]', err);
          }
        }, intervalSec * 1000);
      } else {
        Utils.showToast('Auto-refresh disabled', 'info');
      }
    });
  }

  // Export Filtered CSV Button setup
  const btnExportCSV = document.getElementById('btnExportCSV');
  if (btnExportCSV) {
    btnExportCSV.addEventListener('click', () => {
      const filters = Filters.getValues();
      const query = new URLSearchParams();
      Object.entries(filters).forEach(([k, v]) => {
        if (v && v !== 'all') query.append(k, v);
      });
      const queryString = query.toString() ? `?${query.toString()}` : '';
      window.location.href = `/api/export-csv${queryString}`;
      Utils.showToast('Downloading filtered dataset CSV...', 'success');
    });
  }

  // Initial Health & Dashboard Load
  try {
    const health = await Api.getHealth();
    const sourceLabel = document.getElementById('sourceLabel');
    if (sourceLabel) {
      sourceLabel.textContent = `Source: ${health.data_source.toUpperCase()}`;
    }
    await loadDashboardData(Filters.getValues());
  } catch (err) {
    console.warn('Initial load status:', err.message);
    Utils.showToast('Loaded in offline/demo mode.', 'info');
    await loadDashboardData(Filters.getValues());
  }
});

/**
 * Loads analytics data from API and updates all dashboard components.
 */
async function loadDashboardData(filters = {}) {
  try {
    const response = await Api.getAnalytics(filters);
    if (response && response.data) {
      const data = response.data;
      Dashboard.updateKPIs(data.summary);
      Dashboard.updateValidationStats(data.validation);
      Dashboard.updateParameterTable(data.parameters);
      Charts.renderAll(data.charts);
    }
  } catch (error) {
    console.error('Failed to load dashboard data:', error);
    Utils.showToast('Failed to load analytics: ' + error.message, 'error');
  }
}
