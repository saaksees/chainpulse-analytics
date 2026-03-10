// Upload functionality
document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const validationResult = document.getElementById('validationResult');
    const validationContent = document.getElementById('validationContent');

    // Click to browse
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and drop handlers
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });

    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });

    function handleFile(file) {
        if (!file.name.toLowerCase().endsWith('.csv')) {
            showError('Only CSV files are allowed');
            return;
        }

        uploadFile(file);
    }

    function uploadFile(file) {
        // Show loading state
        dropZone.innerHTML = `
            <div class="upload-icon">⏳</div>
            <div class="upload-text">Uploading and validating...</div>
            <div class="upload-subtext">Please wait</div>
        `;

        const formData = new FormData();
        formData.append('file', file);

        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.valid) {
                handleUploadResponse(data);
            } else {
                showValidationError(data);
            }
            resetDropZone();
        })
        .catch(error => {
            showError('Upload failed: ' + error.message);
            resetDropZone();
        });
    }

    function showValidationSuccess(data) {
        validationContent.innerHTML = `
            <div class="validation-success">
                <div class="validation-title">
                    <span>✅</span>
                    <span>File Valid - Ready to Process</span>
                </div>
                
                <div class="validation-stats">
                    <div class="validation-stat">
                        <div class="validation-stat-value">${formatRows(data.info.rows)}</div>
                        <div class="validation-stat-label">Rows</div>
                    </div>
                    <div class="validation-stat">
                        <div class="validation-stat-value">${data.info.total_revenue || 'Unknown'}</div>
                        <div class="validation-stat-label">Revenue</div>
                    </div>
                    <div class="validation-stat">
                        <div class="validation-stat-value">${data.info.late_rate || 'Unknown'}</div>
                        <div class="validation-stat-label">Late Rate</div>
                    </div>
                    <div class="validation-stat">
                        <div class="validation-stat-value">${data.info.date_range || 'Unknown'}</div>
                        <div class="validation-stat-label">Date Range</div>
                    </div>
                </div>

                ${data.warnings && data.warnings.length > 0 ? `
                    <div class="warning-list">
                        <div style="font-weight: 600; margin-bottom: 8px;">⚠️ Warnings:</div>
                        ${data.warnings.map(w => `<div class="warning-item">• ${w}</div>`).join('')}
                    </div>
                ` : ''}

                <div style="background:#0C4A6E;border:1px solid #0369A1;border-radius:8px;padding:12px 16px;margin-bottom:12px;font-size:13px;color:#7DD3FC;display:flex;align-items:center;gap:10px">
                    <span style="font-size:16px">💾</span>
                    <span>This upload will be saved as a new version in the database. You can switch back to any previous version anytime from <a href="/versions" style="color:#38BDF8;font-weight:600">Version History</a>.</span>
                </div>

                <div style="text-align: center; margin-top: 24px;">
                    <button onclick="runPipeline()" class="cp-btn cp-btn-primary">
                        🚀 Run Pipeline
                    </button>
                </div>
            </div>
        `;
        validationResult.style.display = 'block';
    }

    function showValidationError(data) {
        validationContent.innerHTML = `
            <div class="validation-error">
                <div class="validation-title">
                    <span>❌</span>
                    <span>Validation Failed</span>
                </div>
                
                ${data.errors && data.errors.length > 0 ? `
                    <div class="error-list">
                        <div style="font-weight: 600; margin-bottom: 8px;">Errors:</div>
                        ${data.errors.map(e => `<div class="error-item">• ${e}</div>`).join('')}
                    </div>
                ` : ''}

                ${data.warnings && data.warnings.length > 0 ? `
                    <div class="warning-list">
                        <div style="font-weight: 600; margin-bottom: 8px;">⚠️ Warnings:</div>
                        ${data.warnings.map(w => `<div class="warning-item">• ${w}</div>`).join('')}
                    </div>
                ` : ''}

                <div style="text-align: center; margin-top: 24px;">
                    <button onclick="location.reload()" class="cp-btn cp-btn-secondary">
                        🔄 Try Again
                    </button>
                </div>
            </div>
        `;
        validationResult.style.display = 'block';
    }

    function showError(message) {
        validationContent.innerHTML = `
            <div class="validation-error">
                <div class="validation-title">
                    <span>❌</span>
                    <span>Error</span>
                </div>
                <div class="error-item">${message}</div>
            </div>
        `;
        validationResult.style.display = 'block';
    }

    function resetDropZone() {
        dropZone.innerHTML = `
            <div class="upload-icon">📁</div>
            <div class="upload-text">Drag & drop your CSV file here</div>
            <div class="upload-subtext">or click to browse</div>
        `;
    }

    function formatRows(num) {
        return num.toLocaleString() + ' rows';
    }

    // Global function for pipeline button
    window.runPipeline = function() {
        sessionStorage.setItem('pipeline_running', 'true');
        window.location.href = '/pipeline-status';
    };
    
    // Handle upload response with mapping check
    function handleUploadResponse(data) {
        if (data.needs_mapping) {
            // Redirect to column mapping page
            window.location.href = '/column-mapping';
        } else {
            // Show success and run pipeline button
            showValidationSuccess(data);
        }
    }
});