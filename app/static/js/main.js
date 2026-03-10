// ChainPulse — main.js

// Chart.js global defaults
if (typeof Chart !== 'undefined') {
    Chart.defaults.color = '#94A3B8';
    Chart.defaults.borderColor = '#1E293B';
    Chart.defaults.font.family = 'Inter';
    Chart.defaults.plugins.legend.labels.boxWidth = 12;
    Chart.defaults.plugins.tooltip.backgroundColor = '#111827';
    Chart.defaults.plugins.tooltip.borderColor = '#1E293B';
    Chart.defaults.plugins.tooltip.borderWidth = 1;
    Chart.defaults.plugins.tooltip.padding = 12;
}

// ChainPulse color palette for charts
const CP_COLORS = {
    blue:   '#38BDF8',
    purple: '#7C3AED',
    green:  '#10B981',
    red:    '#EF4444',
    amber:  '#F59E0B',
    teal:   '#06B6D4',
    pink:   '#EC4899',
    indigo: '#6366F1',
};

const CP_PALETTE = Object.values(CP_COLORS);

// Fetch helper with loading state
async function cpFetch(url, loadingEl) {
    try {
        if (loadingEl) {
            loadingEl.innerHTML = `<div class="cp-loading"><div class="cp-spinner"></div><span>Loading data...</span></div>`;
        }
        
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error('ChainPulse API error:', err);
        if (loadingEl) {
            loadingEl.innerHTML = `<div class="cp-loading"><span>⚠️ Failed to load data</span></div>`;
        }
        return null;
    }
}

// Format currency
function formatCurrency(num) {
    if (num >= 1000000)
        return '$' + (num/1000000).toFixed(1) + 'M';
    if (num >= 1000)
        return '$' + (num/1000).toFixed(0) + 'K';
    return '$' + num.toFixed(0);
}

// Format number with commas
function formatNumber(num) {
    return num.toLocaleString();
}

// Animate numbers counting up
function animateCountUp() {
    const cards = document.querySelectorAll('.cp-kpi-value[data-count]');
    cards.forEach(card => {
        const final = card.textContent.trim();
        card.setAttribute('data-final', final);
    });
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    animateCountUp();
    console.log('⚡ ChainPulse initialized');
});