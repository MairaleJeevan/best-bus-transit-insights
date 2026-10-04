/**
 * Chart.js Visualizations Manager for BEST Bus Transit Insights.
 * Handles rendering, updates, color palettes, and responsive resizing.
 */

const Charts = {
  instances: {},

  colors: {
    cyan: '#00d2ff',
    blue: '#38bdf8',
    indigo: '#6366f1',
    purple: '#a855f7',
    amber: '#f59e0b',
    red: '#ef4444',
    emerald: '#10b981',
    orange: '#f97316',
    slate: '#64748b',
    grid: 'rgba(255, 255, 255, 0.06)',
    text: '#94a3b8'
  },

  /**
   * Initializes default Chart.js styling.
   */
  initDefaults() {
    if (typeof Chart === 'undefined') return;
    Chart.defaults.color = this.colors.text;
    Chart.defaults.font.family = "'Plus Jakarta Sans', sans-serif";
    Chart.defaults.font.size = 12;
    Chart.defaults.responsive = true;
    Chart.defaults.maintainAspectRatio = false;
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    Chart.defaults.plugins.legend.labels.boxWidth = 8;
    Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 23, 42, 0.95)';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(255, 255, 255, 0.15)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
  },

  /**
   * Helper to create or update chart instance.
   */
  _createOrUpdate(id, config) {
    if (this.instances[id]) {
      this.instances[id].destroy();
    }
    const canvas = document.getElementById(id);
    if (!canvas) return null;
    const ctx = canvas.getContext('2d');
    this.instances[id] = new Chart(ctx, config);
    return this.instances[id];
  },

  /**
   * Chart 1: Route Usage Distribution (Bar Chart)
   */
  renderRouteUsage(data) {
    if (!data) return;
    this._createOrUpdate('chartRouteUsage', {
      type: 'bar',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Survey Respondents',
          data: data.counts,
          backgroundColor: [
            'rgba(56, 189, 248, 0.85)',
            'rgba(0, 210, 255, 0.85)',
            'rgba(99, 102, 241, 0.85)',
            'rgba(168, 85, 247, 0.85)',
            'rgba(100, 116, 139, 0.85)'
          ],
          borderColor: [
            '#38bdf8',
            '#00d2ff',
            '#6366f1',
            '#a855f7',
            '#64748b'
          ],
          borderWidth: 1.5,
          borderRadius: 6
        }]
      },
      options: {
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` Commuters: ${ctx.parsed.y} (${data.percentages[ctx.dataIndex]}%)`
            }
          }
        },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: this.colors.grid }, beginAtZero: true }
        }
      }
    });
  },

  /**
   * Chart 2: Peak-Hour Frequency & Schedule Reliability (Grouped Bar Chart)
   */
  renderPeakReliability(data) {
    if (!data) return;
    this._createOrUpdate('chartPeakReliability', {
      type: 'bar',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: 'Bus Frequency Rating',
            data: data.frequency,
            backgroundColor: 'rgba(245, 158, 11, 0.8)',
            borderColor: '#f59e0b',
            borderWidth: 1,
            borderRadius: 4
          },
          {
            label: 'Schedule Arrival Reliability',
            data: data.reliability,
            backgroundColor: 'rgba(56, 189, 248, 0.8)',
            borderColor: '#38bdf8',
            borderWidth: 1,
            borderRadius: 4
          }
        ]
      },
      options: {
        plugins: {
          legend: { position: 'top' }
        },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: this.colors.grid }, beginAtZero: true }
        }
      }
    });
  },

  /**
   * Chart 3: Operational Bottlenecks Intensity (Horizontal Bar Chart)
   */
  renderBottlenecks(data) {
    if (!data) return;
    this._createOrUpdate('chartBottlenecks', {
      type: 'bar',
      data: {
        labels: data.labels,
        datasets: [{
          label: '% Commuters Delayed',
          data: data.percentages,
          backgroundColor: 'rgba(239, 68, 68, 0.8)',
          borderColor: '#ef4444',
          borderWidth: 1.5,
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` Delayed: ${ctx.parsed.x}% (${data.counts[ctx.dataIndex]} respondents - ${data.severity[ctx.dataIndex]})`
            }
          }
        },
        scales: {
          x: {
            grid: { color: this.colors.grid },
            beginAtZero: true,
            ticks: { callback: (v) => `${v}%` }
          },
          y: { grid: { display: false } }
        }
      }
    });
  },

  /**
   * Chart 4: Hourly Overcrowding vs Bus Frequency Trend (Line Chart)
   */
  renderHourlyTrend(data) {
    const noticeEl = document.getElementById('hourlyNotice');
    const noticeText = document.getElementById('hourlyNoticeText');
    const canvas = document.getElementById('chartHourlyTrend');

    if (!data || !data.available) {
      if (noticeEl) {
        noticeEl.classList.remove('hidden');
        if (noticeText && data && data.message) {
          noticeText.textContent = data.message;
        }
      }
      if (this.instances['chartHourlyTrend']) {
        this.instances['chartHourlyTrend'].destroy();
        delete this.instances['chartHourlyTrend'];
      }
      return;
    }

    if (noticeEl) noticeEl.classList.add('hidden');

    this._createOrUpdate('chartHourlyTrend', {
      type: 'line',
      data: {
        labels: data.labels,
        datasets: [
          {
            label: 'Overcrowding Level (%)',
            data: data.overcrowding_index,
            borderColor: '#ef4444',
            backgroundColor: 'rgba(239, 68, 68, 0.15)',
            borderWidth: 2.5,
            fill: true,
            tension: 0.35,
            pointBackgroundColor: '#ef4444',
            pointRadius: 4
          },
          {
            label: 'Bus Frequency Index',
            data: data.bus_frequency,
            borderColor: '#00d2ff',
            backgroundColor: 'rgba(0, 210, 255, 0.15)',
            borderWidth: 2.5,
            fill: true,
            tension: 0.35,
            pointBackgroundColor: '#00d2ff',
            pointRadius: 4
          }
        ]
      },
      options: {
        plugins: {
          legend: { position: 'top' }
        },
        scales: {
          x: { grid: { display: false } },
          y: {
            grid: { color: this.colors.grid },
            beginAtZero: true,
            ticks: { callback: (v) => `${v}%` }
          }
        }
      }
    });
  },

  /**
   * Chart 5: Transit Health Profile (Radar Chart)
   */
  renderTransitHealth(data) {
    if (!data) return;
    this._createOrUpdate('chartTransitHealth', {
      type: 'radar',
      data: {
        labels: data.labels,
        datasets: [{
          label: 'Corridor Performance Score (0-100)',
          data: data.scores,
          backgroundColor: 'rgba(0, 210, 255, 0.25)',
          borderColor: '#00d2ff',
          pointBackgroundColor: '#00d2ff',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: '#00d2ff',
          borderWidth: 2
        }]
      },
      options: {
        plugins: {
          legend: { display: false }
        },
        scales: {
          r: {
            angleLines: { color: this.colors.grid },
            grid: { color: this.colors.grid },
            pointLabels: { color: '#f8fafc', font: { size: 11, weight: '600' } },
            ticks: { display: false, backdropColor: 'transparent', max: 100, min: 0 }
          }
        }
      }
    });
  },

  /**
   * Chart 6: Payment Method Adoption (Donut Chart)
   */
  renderPayments(data) {
    if (!data) return;
    this._createOrUpdate('chartPayments', {
      type: 'doughnut',
      data: {
        labels: data.labels,
        datasets: [{
          data: data.counts,
          backgroundColor: [
            '#10b981',
            '#38bdf8',
            '#f59e0b',
            '#a855f7',
            '#64748b'
          ],
          borderColor: '#080c14',
          borderWidth: 2
        }]
      },
      options: {
        plugins: {
          legend: { position: 'right' },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.label}: ${ctx.parsed} (${data.percentages[ctx.dataIndex]}%)`
            }
          }
        },
        cutout: '65%'
      }
    });
  },

  /**
   * Chart 7: Demographics (Bar Chart - Age & Occupation)
   */
  renderDemographics(data) {
    if (!data || !data.age_groups) return;
    this._createOrUpdate('chartDemographics', {
      type: 'bar',
      data: {
        labels: data.age_groups.labels,
        datasets: [{
          label: 'Age Group Commuters',
          data: data.age_groups.counts,
          backgroundColor: 'rgba(99, 102, 241, 0.8)',
          borderColor: '#6366f1',
          borderWidth: 1,
          borderRadius: 6
        }]
      },
      options: {
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: this.colors.grid }, beginAtZero: true }
        }
      }
    });
  },

  /**
   * Chart 8: Bus Physical Condition Rating (Bar Chart)
   */
  renderBusCondition(data) {
    if (!data) return;
    this._createOrUpdate('chartBusCondition', {
      type: 'bar',
      data: {
        labels: data.parameters,
        datasets: [{
          label: 'Average Score (out of 5)',
          data: data.averages,
          backgroundColor: [
            'rgba(249, 115, 22, 0.8)',
            'rgba(56, 189, 248, 0.8)',
            'rgba(16, 185, 129, 0.8)'
          ],
          borderColor: ['#f97316', '#38bdf8', '#10b981'],
          borderWidth: 1.5,
          borderRadius: 6
        }]
      },
      options: {
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` Rating: ${ctx.parsed.y}/5 (${data.satisfaction_pct[ctx.dataIndex]}% satisfied)`
            }
          }
        },
        scales: {
          x: { grid: { display: false } },
          y: {
            grid: { color: this.colors.grid },
            beginAtZero: true,
            max: 5,
            ticks: { stepSize: 1 }
          }
        }
      }
    });
  },

  /**
   * Render all charts simultaneously.
   */
  renderAll(chartsData) {
    if (!chartsData) return;
    this.renderRouteUsage(chartsData.route_usage);
    this.renderPeakReliability(chartsData.peak_reliability);
    this.renderBottlenecks(chartsData.bottlenecks);
    this.renderHourlyTrend(chartsData.hourly_trend);
    this.renderTransitHealth(chartsData.transit_health);
    this.renderPayments(chartsData.payments);
    this.renderDemographics(chartsData.demographics);
    this.renderBusCondition(chartsData.bus_condition);
  }
};
