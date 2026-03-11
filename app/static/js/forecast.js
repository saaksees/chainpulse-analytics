// Forecast Dashboard - Dynamic Chart.js Implementation

async function loadForecastCharts() {
    try {
        const res = await fetch('/api/forecast/charts');
        const data = await res.json();
        
        if (data.no_data) {
            showNoDataMessage();
            return;
        }

        // Forecast Summary Bar Chart
        if (document.getElementById('forecastSummaryChart')) {
            new Chart(document.getElementById('forecastSummaryChart'), {
                type: 'bar',
                data: {
                    labels: data.summary.labels,
                    datasets: [{
                        label: 'Forecast Total',
                        data: data.summary.totals,
                        backgroundColor: [
                            CHART_COLORS.blue,
                            CHART_COLORS.green,
                            CHART_COLORS.orange,
                            CHART_COLORS.purple,
                            CHART_COLORS.teal
                        ]
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: '90-Day Forecast by Category',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Forecast Trend Line Chart (first category)
        if (document.getElementById('forecastTrendChart') && data.categories.length > 0) {
            const firstCategory = data.categories[0];
            const categoryData = data.forecasts[firstCategory];
            
            if (categoryData) {
                new Chart(document.getElementById('forecastTrendChart'), {
                    type: 'line',
                    data: {
                        labels: categoryData.dates,
                        datasets: [{
                            label: 'Predicted Sales',
                            data: categoryData.predicted,
                            borderColor: CHART_COLORS.green,
                            backgroundColor: 'rgba(52,211,153,0.1)',
                            tension: 0.4,
                            fill: true
                        }, {
                            label: 'Lower Bound',
                            data: categoryData.lower,
                            borderColor: CHART_COLORS.red,
                            backgroundColor: 'rgba(239,68,68,0.1)',
                            tension: 0.4,
                            fill: false
                        }, {
                            label: 'Upper Bound',
                            data: categoryData.upper,
                            borderColor: CHART_COLORS.blue,
                            backgroundColor: 'rgba(56,189,248,0.1)',
                            tension: 0.4,
                            fill: false
                        }]
                    },
                    options: {
                        ...CHART_DEFAULTS,
                        plugins: {
                            ...CHART_DEFAULTS.plugins,
                            title: {
                                display: true,
                                text: `${firstCategory} - Forecast Trend`,
                                color: '#E2E8F0'
                            }
                        }
                    }
                });
            }
        }

    } catch (err) {
        console.error('Forecast charts error:', err);
        showNoDataMessage();
    }
}

function showNoDataMessage() {
    document.querySelectorAll('.chart-container').forEach(el => {
        el.innerHTML = '<div class="no-data">Run pipeline to generate charts</div>';
    });
}

// Load charts when page loads
document.addEventListener('DOMContentLoaded', loadForecastCharts);

// ChainPulse — forecast.js
/**
 * Forecasting Dashboard JavaScript
 * Interactive functionality for demand forecasting
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Forecasting Dashboard loaded');
    
    // Initialize forecasting functionality
    initForecastCharts();
    initCategoryFilters();
});

function initForecastCharts() {
    // Add interactive chart functionality
    console.log('Forecast charts initialized');
}

function initCategoryFilters() {
    // Add category filtering functionality
    console.log('Category filters initialized');
}