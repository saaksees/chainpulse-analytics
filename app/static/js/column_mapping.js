document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('mappingForm');
    const confirmButton = document.getElementById('confirmButton');
    const validationWarning = document.getElementById('validationWarning');
    const warningText = document.getElementById('warningText');
    
    // Check validation on page load
    checkValidation();
    
    // Add event listeners to all dropdowns
    const selects = document.querySelectorAll('.mapping-select');
    selects.forEach(select => {
        select.addEventListener('change', function() {
            checkValidation();
        });
    });
    
    // Confirm button click handler
    confirmButton.addEventListener('click', function(e) {
        e.preventDefault();
        
        const validation = validateRequiredFields();
        if (!validation.valid) {
            showValidationWarning(validation.missing);
            scrollToFirstMissing();
            return;
        }
        
        // Collect mappings
        const mappings = {};
        selects.forEach(select => {
            const coreKey = select.dataset.coreKey;
            const selectedValue = select.value;
            if (selectedValue) {
                mappings[coreKey] = selectedValue;
            }
        });
        
        // Show loading state
        confirmButton.disabled = true;
        confirmButton.innerHTML = '⏳ Applying Mapping...';
        
        // Submit mappings
        fetch('/api/apply-mapping', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(mappings)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Save pipeline state and redirect
                sessionStorage.setItem('pipeline_running', 'true');
                window.location.href = '/pipeline-status';
            } else {
                showError(data.message || 'Failed to apply mapping');
                resetButton();
            }
        })
        .catch(error => {
            showError('Network error: ' + error.message);
            resetButton();
        });
    });
    
    function checkValidation() {
        const validation = validateRequiredFields();
        
        if (validation.valid) {
            hideValidationWarning();
            clearMissingHighlights();
        } else {
            showValidationWarning(validation.missing);
            highlightMissingRequired(validation.missing);
        }
    }
    
    function validateRequiredFields() {
        const missing = [];
        const requiredRows = document.querySelectorAll('.mapping-row[data-required="true"]');
        
        requiredRows.forEach(row => {
            const coreKey = row.dataset.coreKey;
            const select = row.querySelector('.mapping-select');
            const standardName = row.querySelector('.mapping-standard-name').textContent;
            
            if (!select.value) {
                missing.push({
                    key: coreKey,
                    name: standardName,
                    element: row
                });
            }
        });
        
        return {
            valid: missing.length === 0,
            missing: missing
        };
    }
    
    function showValidationWarning(missing) {
        const missingNames = missing.map(m => m.name).join(', ');
        warningText.textContent = `Please map required columns: ${missingNames}`;
        validationWarning.style.display = 'block';
    }
    
    function hideValidationWarning() {
        validationWarning.style.display = 'none';
    }
    
    function highlightMissingRequired(missing) {
        // Clear existing highlights
        clearMissingHighlights();
        
        // Add highlights to missing required fields
        missing.forEach(item => {
            item.element.classList.add('missing-required');
        });
    }
    
    function clearMissingHighlights() {
        const highlighted = document.querySelectorAll('.missing-required');
        highlighted.forEach(element => {
            element.classList.remove('missing-required');
        });
    }
    
    function scrollToFirstMissing() {
        const firstMissing = document.querySelector('.missing-required');
        if (firstMissing) {
            firstMissing.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }
    }
    
    function showError(message) {
        // Create or update error display
        let errorDiv = document.getElementById('errorMessage');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'errorMessage';
            errorDiv.style.cssText = `
                background: var(--red-glow);
                border: 2px solid var(--red);
                color: var(--red);
                padding: 16px 24px;
                border-radius: 12px;
                margin-bottom: 24px;
                font-weight: 600;
            `;
            validationWarning.parentNode.insertBefore(errorDiv, validationWarning.nextSibling);
        }
        
        errorDiv.innerHTML = `❌ ${message}`;
        errorDiv.style.display = 'block';
        errorDiv.scrollIntoView({ behavior: 'smooth' });
    }
    
    function resetButton() {
        confirmButton.disabled = false;
        confirmButton.innerHTML = '✅ Confirm Mapping & Run Pipeline';
    }
});