// Inventory Dashboard - Dynamic Chart.js Implementation

async function loadInventoryCharts() {
    try {
        const res = await fetch('/api/inventory/charts');
        const data = await res.json();
        
        if (data.no_data) {
            showNoDataMessage();
            return;
        }

        // ABC Analysis Pie Chart
        if (document.getElementById('abcAnalysisChart')) {
            new Chart(document.getElementById('abcAnalysisChart'), {
                type: 'doughnut',
                data: {
                    labels: data.abc_analysis.labels,
                    datasets: [{
                        data: data.abc_analysis.values,
                        backgroundColor: [
                            CHART_COLORS.green,   // Category A
                            CHART_COLORS.orange,  // Category B
                            CHART_COLORS.red      // Category C
                        ],
                        borderWidth: 2,
                        borderColor: '#1E293B'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { 
                                color: '#94A3B8',
                                padding: 20,
                                usePointStyle: true
                            }
                        },
                        title: {
                            display: true,
                            text: 'ABC Classification',
                            color: '#E2E8F0'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${label}: ${value} products (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }

        // Stock Movement Bar Chart
        if (document.getElementById('stockMovementChart')) {
            new Chart(document.getElementById('stockMovementChart'), {
                type: 'bar',
                data: {
                    labels: data.stock_movement.labels,
                    datasets: [{
                        label: 'Product Count',
                        data: data.stock_movement.values,
                        backgroundColor: [
                            CHART_COLORS.green,   // Fast Moving
                            CHART_COLORS.orange,  // Medium Moving
                            CHART_COLORS.red      // Slow Moving
                        ],
                        borderRadius: 8,
                        borderSkipped: false
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Stock Movement Classification',
                            color: '#E2E8F0'
                        },
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { 
                                color: '#94A3B8',
                                callback: function(value) {
                                    return Math.floor(value);
                                }
                            },
                            grid: { color: '#1E293B' }
                        },
                        x: {
                            ticks: { color: '#94A3B8' },
                            grid: { color: '#1E293B' }
                        }
                    }
                }
            });
        }

        // Turnover by Category Bar Chart
        if (document.getElementById('turnoverCategoryChart')) {
            new Chart(document.getElementById('turnoverCategoryChart'), {
                type: 'bar',
                data: {
                    labels: data.turnover_by_category.labels,
                    datasets: [{
                        label: 'Turnover Ratio',
                        data: data.turnover_by_category.values,
                        backgroundColor: CHART_COLORS.purple,
                        borderRadius: 8,
                        borderSkipped: false
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    indexAxis: 'y',
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Annual Turnover by Category',
                            color: '#E2E8F0'
                        },
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            beginAtZero: true,
                            ticks: { 
                                color: '#94A3B8',
                                callback: function(value) {
                                    return value.toFixed(1) + 'x';
                                }
                            },
                            grid: { color: '#1E293B' }
                        },
                        y: {
                            ticks: { color: '#94A3B8' },
                            grid: { color: '#1E293B' }
                        }
                    }
                }
            });
        }

        // Inventory Value Distribution Pie Chart
        if (document.getElementById('inventoryValueChart')) {
            new Chart(document.getElementById('inventoryValueChart'), {
                type: 'pie',
                data: {
                    labels: data.inventory_value.labels,
                    datasets: [{
                        data: data.inventory_value.values,
                        backgroundColor: [
                            CHART_COLORS.blue,
                            CHART_COLORS.purple,
                            CHART_COLORS.green,
                            CHART_COLORS.orange,
                            CHART_COLORS.teal,
                            CHART_COLORS.pink
                        ],
                        borderWidth: 2,
                        borderColor: '#1E293B'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: { 
                                color: '#94A3B8',
                                padding: 15,
                                usePointStyle: true
                            }
                        },
                        title: {
                            display: true,
                            text: 'Inventory Value by Category',
                            color: '#E2E8F0'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.parsed;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return `${label}: $${value.toLocaleString()} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }

        // Reorder Analysis Scatter Chart
        if (document.getElementById('reorderAnalysisChart')) {
            new Chart(document.getElementById('reorderAnalysisChart'), {
                type: 'scatter',
                data: {
                    datasets: [{
                        label: 'Reorder Points',
                        data: data.reorder_analysis.data,
                        backgroundColor: CHART_COLORS.teal,
                        borderColor: CHART_COLORS.teal,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: { color: '#94A3B8' }
                        },
                        title: {
                            display: true,
                            text: 'Demand vs Reorder Point Analysis',
                            color: '#E2E8F0'
                        },
                        tooltip: {
                            callbacks: {
                                title: function(context) {
                                    return `Product Analysis`;
                                },
                                label: function(context) {
                                    return [
                                        `Daily Demand: ${context.parsed.x}`,
                                        `Reorder Point: ${context.parsed.y}`
                                    ];
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            type: 'linear',
                            position: 'bottom',
                            title: {
                                display: true,
                                text: 'Average Daily Demand',
                                color: '#94A3B8'
                            },
                            ticks: { color: '#94A3B8' },
                            grid: { color: '#1E293B' }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Reorder Point',
                                color: '#94A3B8'
                            },
                            ticks: { color: '#94A3B8' },
                            grid: { color: '#1E293B' }
                        }
                    }
                }
            });
        }

    } catch (err) {
        console.error('Inventory charts error:', err);
        showNoDataMessage();
    }
}

function showNoDataMessage() {
    document.querySelectorAll('.chart-container').forEach(el => {
        el.innerHTML = '<div class="no-data">Run inventory analysis to generate charts</div>';
    });
}

// Load charts when page loads
document.addEventListener('DOMContentLoaded', loadInventoryCharts);

// Refresh charts function
function refreshCharts() {
    loadInventoryCharts();
}

// Export functionality
function exportChart(chartName) {
    console.log(`Exporting ${chartName} chart...`);
    // TODO: Implement chart export functionality
}