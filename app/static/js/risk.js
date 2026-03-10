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