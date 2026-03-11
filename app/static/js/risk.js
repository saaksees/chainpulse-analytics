// Risk Dashboard - Dynamic Chart.js Implementation

async function loadRiskCharts() {
    try {
        const res = await fetch('/api/risk/charts');
        const data = await res.json();
        
        if (data.no_data) {
            showNoDataMessage();
            return;
        }

        // Risk Distribution Pie Chart
        if (document.getElementById('riskDistributionChart')) {
            new Chart(document.getElementById('riskDistributionChart'), {
                type: 'doughnut',
                data: {
                    labels: data.risk_distribution.labels,
                    datasets: [{
                        data: data.risk_distribution.values,
                        backgroundColor: [
                            CHART_COLORS.red,
                            CHART_COLORS.orange,
                            CHART_COLORS.green
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
                            text: 'Risk Distribution',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Risk by Region Stacked Bar
        if (document.getElementById('riskByRegionChart')) {
            new Chart(document.getElementById('riskByRegionChart'), {
                type: 'bar',
                data: {
                    labels: data.risk_by_region.labels,
                    datasets: [{
                        label: 'High Risk %',
                        data: data.risk_by_region.high,
                        backgroundColor: CHART_COLORS.red
                    }, {
                        label: 'Medium Risk %',
                        data: data.risk_by_region.medium,
                        backgroundColor: CHART_COLORS.orange
                    }, {
                        label: 'Low Risk %',
                        data: data.risk_by_region.low,
                        backgroundColor: CHART_COLORS.green
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    scales: {
                        x: { stacked: true },
                        y: { stacked: true }
                    },
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Risk by Region',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Risk by Shipping Mode Bar Chart
        if (document.getElementById('riskByShippingChart')) {
            new Chart(document.getElementById('riskByShippingChart'), {
                type: 'bar',
                data: {
                    labels: data.risk_by_shipping.labels,
                    datasets: [{
                        label: 'Late Rate %',
                        data: data.risk_by_shipping.values,
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

        // Feature Importance Horizontal Bar
        if (document.getElementById('featureImportanceChart')) {
            new Chart(document.getElementById('featureImportanceChart'), {
                type: 'bar',
                data: {
                    labels: data.feature_importance.labels,
                    datasets: [{
                        label: 'Importance',
                        data: data.feature_importance.values,
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
                            text: 'Feature Importance',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

    } catch (err) {
        console.error('Risk charts error:', err);
        showNoDataMessage();
    }
}

function showNoDataMessage() {
    document.querySelectorAll('.chart-container').forEach(el => {
        el.innerHTML = '<div class="no-data">Run pipeline to generate charts</div>';
    });
}

// Load charts when page loads
document.addEventListener('DOMContentLoaded', loadRiskCharts);

// ChainPulse — risk.js
/**
 * Risk Analysis Dashboard JavaScript
 * Interactive functionality for delivery risk analysis
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Risk Analysis Dashboard loaded');
    
    // Initialize risk-specific functionality
    initRiskMetrics();
    initRiskPrediction();
    
    // Connect demo button
    const demoBtn = document.querySelector('button[onclick*="loadDemo"]');
    if (demoBtn) {
        demoBtn.onclick = loadDemoWhatIf;
    }
});

function initRiskMetrics() {
    // Animate risk level counters
    const statValues = document.querySelectorAll('.stat-value');
    
    statValues.forEach(element => {
        const finalValue = element.textContent;
        if (!isNaN(finalValue.replace(/[^0-9]/g, ''))) {
            animateCounter(element, parseInt(finalValue.replace(/[^0-9]/g, '')));
        }
    });
}

function initRiskPrediction() {
    // Add interactive risk prediction functionality
    console.log('Risk prediction tools initialized');
}

function animateCounter(element, targetValue) {
    let currentValue = 0;
    const increment = targetValue / 50;
    const timer = setInterval(() => {
        currentValue += increment;
        if (currentValue >= targetValue) {
            currentValue = targetValue;
            clearInterval(timer);
        }
        element.textContent = Math.floor(currentValue).toLocaleString();
    }, 30);
}

// Demo function to test what-if simulator
function loadDemoWhatIf() {
    console.log('Loading demo What-If data...');
    
    // Call the whatif.js function
    if (typeof window.loadDemoWhatIf === 'function') {
        window.loadDemoWhatIf();
    } else {
        // Fallback if whatif.js not loaded yet
        setTimeout(() => {
            if (typeof window.loadDemoWhatIf === 'function') {
                window.loadDemoWhatIf();
            }
        }, 100);
    }
}

// Make globally available
window.loadDemoWhatIf = loadDemoWhatIf;