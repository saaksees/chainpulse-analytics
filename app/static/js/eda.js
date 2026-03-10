// ChainPulse — eda.js
/**
 * EDA Dashboard JavaScript
 * Interactive functionality for exploratory data analysis
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('EDA Dashboard loaded');
    
    // Initialize EDA-specific functionality
    initChartInteractions();
    initDataFilters();
});

function initChartInteractions() {
    // Add click handlers for chart images to show full-screen view
    const chartImages = document.querySelectorAll('.chart-image');
    
    chartImages.forEach(image => {
        image.addEventListener('click', function() {
            showFullScreenChart(this);
        });
        
        // Add hover effects
        image.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        image.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

function initDataFilters() {
    // Add any filtering functionality here
    console.log('Data filters initialized');
}

function showFullScreenChart(imageElement) {
    // Create modal overlay
    const modal = document.createElement('div');
    modal.className = 'fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50';
    modal.innerHTML = `
        <div class="max-w-6xl max-h-full p-4">
            <img src="${imageElement.src}" alt="${imageElement.alt}" class="max-w-full max-h-full object-contain">
            <button class="absolute top-4 right-4 text-white text-2xl hover:text-gray-300" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Close on click outside
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
}