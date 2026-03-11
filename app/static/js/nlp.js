// NLP Dashboard - Dynamic Chart.js Implementation

async function loadNLPCharts() {
    try {
        const res = await fetch('/api/nlp/charts');
        const data = await res.json();
        
        if (data.no_data) {
            showNoDataMessage();
            return;
        }

        // Top Keywords Bar Chart
        if (document.getElementById('topKeywordsChart')) {
            new Chart(document.getElementById('topKeywordsChart'), {
                type: 'bar',
                data: {
                    labels: data.top_keywords.labels,
                    datasets: [{
                        label: 'Frequency',
                        data: data.top_keywords.values,
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
                            text: 'Top Keywords',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Top Bigrams Bar Chart
        if (document.getElementById('topBigramsChart')) {
            new Chart(document.getElementById('topBigramsChart'), {
                type: 'bar',
                data: {
                    labels: data.top_bigrams.labels,
                    datasets: [{
                        label: 'Frequency',
                        data: data.top_bigrams.values,
                        backgroundColor: CHART_COLORS.green
                    }]
                },
                options: {
                    ...CHART_DEFAULTS,
                    indexAxis: 'y',
                    plugins: {
                        ...CHART_DEFAULTS.plugins,
                        title: {
                            display: true,
                            text: 'Top Bigrams',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Topic Distribution Pie Chart
        if (document.getElementById('topicDistributionChart')) {
            new Chart(document.getElementById('topicDistributionChart'), {
                type: 'doughnut',
                data: {
                    labels: data.topic_distribution.labels,
                    datasets: [{
                        data: data.topic_distribution.values,
                        backgroundColor: [
                            CHART_COLORS.blue,
                            CHART_COLORS.green,
                            CHART_COLORS.orange,
                            CHART_COLORS.purple,
                            CHART_COLORS.red
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
                            text: 'Topic Distribution',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

        // Sentiment Distribution Pie Chart
        if (document.getElementById('sentimentDistributionChart')) {
            new Chart(document.getElementById('sentimentDistributionChart'), {
                type: 'pie',
                data: {
                    labels: data.sentiment_distribution.labels,
                    datasets: [{
                        data: data.sentiment_distribution.values,
                        backgroundColor: [
                            CHART_COLORS.green,
                            CHART_COLORS.yellow,
                            CHART_COLORS.red
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
                            text: 'Sentiment Distribution',
                            color: '#E2E8F0'
                        }
                    }
                }
            });
        }

    } catch (err) {
        console.error('NLP charts error:', err);
        showNoDataMessage();
    }
}

function showNoDataMessage() {
    document.querySelectorAll('.chart-container').forEach(el => {
        el.innerHTML = '<div class="no-data">Run pipeline to generate charts</div>';
    });
}

// Load charts when page loads
document.addEventListener('DOMContentLoaded', loadNLPCharts);

// ChainPulse — nlp.js
/**
 * NLP Analysis Dashboard JavaScript
 * Interactive functionality for natural language processing insights
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('NLP Analysis Dashboard loaded');
    
    // Initialize NLP functionality
    initWordCloudInteractions();
    initTopicFilters();
});

function initWordCloudInteractions() {
    // Add interactive word cloud functionality
    console.log('Word cloud interactions initialized');
}

function initTopicFilters() {
    // Add topic filtering functionality
    console.log('Topic filters initialized');
}