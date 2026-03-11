// Customer Dashboard - Dynamic Chart.js Implementation

async function loadCustomerCharts() {
    try {
        const res = await fetch('/api/customers/charts');
        const data = await res.json();
        
        if (data.no_data) {
            showNoDataMessage();
            return;
        }

        // Segment Distribution Pie Chart
        if (document.getElementById('segmentDistributionChart')) {
            new Chart(document.getElementById('segmentDistributionChart'), {
                type: 'doughnut',
                data: {
                    labels: data.segment_distribution.labels,
                    datasets: [{
                        data: data.segment_distribution.values,
                        backgroundColor: [
                            CHART_COLORS.blue,
                            CHART_COLORS.purple,
                            CHART_COLORS.green,
                            CHART_COLORS.orange,
                            CHART_COLORS.red,
                            CHART_COLORS.teal,
                            CHART_COLORS.pink
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
                            text: 'Customer Segment Distribution',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Segment Revenue Bar Chart
        if (document.getElementById('segmentRevenueChart')) {
            new Chart(document.getElementById('segmentRevenueChart'), {
                type: 'bar',
                data: {
                    labels: data.segment_revenue.labels,
                    datasets: [{
                        label: 'Revenue by Segment',
                        data: data.segment_revenue.values,
                        backgroundColor: CHART_COLORS.purple
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Revenue by Segment',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Cluster Sizes Pie Chart
        if (document.getElementById('clusterSizesChart')) {
            new Chart(document.getElementById('clusterSizesChart'), {
                type: 'pie',
                data: {
                    labels: data.cluster_sizes.labels,
                    datasets: [{
                        data: data.cluster_sizes.values,
                        backgroundColor: [
                            CHART_COLORS.green,
                            CHART_COLORS.blue,
                            CHART_COLORS.orange,
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
                            text: 'Cluster Sizes',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Recency Distribution Bar Chart
        if (document.getElementById('recencyDistributionChart')) {
            new Chart(document.getElementById('recencyDistributionChart'), {
                type: 'bar',
                data: {
                    labels: data.recency_distribution.labels,
                    datasets: [{
                        label: 'Customer Count',
                        data: data.recency_distribution.values,
                        backgroundColor: CHART_COLORS.teal
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Recency Distribution',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

    } catch (err) {
        console.error('Customer charts error:', err);
        showNoDataMessage();
    }
}

function showNoDataMessage() {
    document.querySelectorAll('.chart-container').forEach(el => {
        el.innerHTML = '<div class="no-data">Run pipeline to generate charts</div>';
    });
}

// Load charts when page loads
document.addEventListener('DOMContentLoaded', loadCustomerCharts);

// ChainPulse — customers.js
/**
 * Customer Segmentation Dashboard JavaScript
 * Interactive functionality for RFM analysis
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Customer Segmentation Dashboard loaded');
    
    // Initialize customer segmentation functionality
    initSegmentAnalysis();
    initCustomerFilters();
});

function initSegmentAnalysis() {
    // Add interactive segment analysis
    console.log('Segment analysis initialized');
}

function initCustomerFilters() {
    // Add customer filtering functionality
    console.log('Customer filters initialized');
}