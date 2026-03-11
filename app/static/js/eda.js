// EDA Dashboard - Dynamic Chart.js Implementation

async function loadEDACharts() {
    try {
        const res = await fetch('/api/eda/charts');
        const data = await res.json();
        
        if (data.no_data) {
            showNoDataMessage();
            return;
        }

        // Revenue Trend Line Chart
        if (document.getElementById('revenueTrendChart')) {
            new Chart(document.getElementById('revenueTrendChart'), {
                type: 'line',
                data: {
                    labels: data.revenue_trend.labels,
                    datasets: [{
                        label: 'Revenue',
                        data: data.revenue_trend.values,
                        borderColor: CHART_COLORS.blue,
                        backgroundColor: 'rgba(56,189,248,0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Revenue Trend',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Region Bar Chart
        if (document.getElementById('regionChart')) {
            new Chart(document.getElementById('regionChart'), {
                type: 'bar',
                data: {
                    labels: data.revenue_by_region.labels,
                    datasets: [{
                        label: 'Revenue by Region',
                        data: data.revenue_by_region.values,
                        backgroundColor: [
                            CHART_COLORS.blue,
                            CHART_COLORS.purple,
                            CHART_COLORS.green,
                            CHART_COLORS.orange,
                            CHART_COLORS.pink,
                            CHART_COLORS.teal,
                            CHART_COLORS.yellow,
                            CHART_COLORS.red
                        ]
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Revenue by Region',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Category Horizontal Bar
        if (document.getElementById('categoryChart')) {
            new Chart(document.getElementById('categoryChart'), {
                type: 'bar',
                data: {
                    labels: data.revenue_by_category.labels,
                    datasets: [{
                        label: 'Revenue by Category',
                        data: data.revenue_by_category.values,
                        backgroundColor: CHART_COLORS.purple
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    indexAxis: 'y',
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Revenue by Category',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Late Rate Bar Chart
        if (document.getElementById('lateRateChart')) {
            new Chart(document.getElementById('lateRateChart'), {
                type: 'bar',
                data: {
                    labels: data.late_rate_by_shipping.labels,
                    datasets: [{
                        label: 'Late Rate %',
                        data: data.late_rate_by_shipping.values,
                        backgroundColor: CHART_COLORS.red
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Late Rate by Shipping Mode',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Orders by Month Line Chart
        if (document.getElementById('ordersMonthChart')) {
            new Chart(document.getElementById('ordersMonthChart'), {
                type: 'line',
                data: {
                    labels: data.orders_by_month.labels,
                    datasets: [{
                        label: 'Orders per Month',
                        data: data.orders_by_month.values,
                        borderColor: CHART_COLORS.green,
                        backgroundColor: 'rgba(52,211,153,0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Orders by Month',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Order Status Doughnut
        if (document.getElementById('orderStatusChart')) {
            new Chart(document.getElementById('orderStatusChart'), {
                type: 'doughnut',
                data: {
                    labels: data.order_status_dist.labels,
                    datasets: [{
                        data: data.order_status_dist.values,
                        backgroundColor: [
                            CHART_COLORS.red,
                            CHART_COLORS.green,
                            CHART_COLORS.yellow,
                            CHART_COLORS.blue,
                            CHART_COLORS.purple
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { color: '#94A3B8' }
                        },
                        title: {
                            display: true,
                            text: 'Order Status Distribution',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

    } catch (err) {
        console.error('EDA charts error:', err);
        showNoDataMessage();
    }
}

function showNoDataMessage() {
    document.querySelectorAll('.chart-container').forEach(el => {
        el.innerHTML = '<div class="no-data">Run pipeline to generate charts</div>';
    });
}

// Load charts when page loads
document.addEventListener('DOMContentLoaded', loadEDACharts);

// Export functionality (placeholder)
function exportChart(chartName) {
    console.log(`Exporting ${chartName} chart...`);
    // TODO: Implement chart export functionality
}

// Refresh charts function
function refreshCharts() {
    loadEDACharts();
}