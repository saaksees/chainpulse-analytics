document.addEventListener('DOMContentLoaded', function() {
    const startButton = document.getElementById('startButton');
    const startSection = document.getElementById('startSection');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const completionMessage = document.getElementById('completionMessage');
    const completionContent = document.getElementById('completionContent');

    let autoMLMode = false;

    // Check if pipeline should auto-start
    if (sessionStorage.getItem('pipeline_running') === 'true') {
        sessionStorage.removeItem('pipeline_running');
        startPipeline();
    }

    startButton.addEventListener('click', startPipeline);

    function togglePipelineMode() {
        autoMLMode = !autoMLMode;
        const knob = document.getElementById('toggle-knob');
        const toggle = document.getElementById('mode-toggle');
        const desc = document.getElementById('pipeline-mode-desc');
        const info = document.getElementById('automl-info');

        if (autoMLMode) {
            knob.style.left = '26px';
            knob.style.background = '#38BDF8';
            toggle.style.background = '#0C4A6E';
            toggle.style.borderColor = '#38BDF8';
            desc.textContent = 'AutoML: selects best model for your data';
            info.style.display = 'block';
        } else {
            knob.style.left = '2px';
            knob.style.background = '#94A3B8';
            toggle.style.background = '#1E293B';
            toggle.style.borderColor = '#334155';
            desc.textContent = 'Standard: runs fixed scripts';
            info.style.display = 'none';
        }
    }

    // Make togglePipelineMode globally available
    window.togglePipelineMode = togglePipelineMode;

    function startPipeline() {
        startSection.style.display = 'none';
        
        // Reset all steps
        for (let i = 1; i <= 6; i++) {
            updateStep(i, 'waiting', '⏳ Waiting');
        }
        
        // Choose URL based on mode
        const url = autoMLMode ? '/api/pipeline/auto' : '/api/pipeline/run';
        
        // Start SSE connection
        const eventSource = new EventSource(url);
        
        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            handleEvent(data, eventSource);
        };
        
        eventSource.onerror = function(event) {
            console.error('SSE error:', event);
            showError('Connection lost. Please refresh the page.');
            eventSource.close();
        };
    }

    function handleEvent(data, eventSource) {
        switch (data.type) {
            case 'start':
                updateProgress(0);
                break;
                
            case 'step_start':
                updateStep(data.step, 'running', '🔄 Running');
                scrollToStep(data.step);
                break;
                
            case 'step_done':
                const status = data.success ? 'complete' : 'failed';
                let statusText = data.success ? '✅ Complete' : '❌ Failed';
                
                // Add AutoML details if available
                if (autoMLMode && data.model) {
                    statusText += ` (${data.model})`;
                }
                
                updateStep(data.step, status, statusText);
                updateProgress(data.progress);
                break;
                
            case 'profile_done':
                showProfileSummary(data.profile);
                break;
                
            case 'complete':
                if (data.auto_report) {
                    showAutoMLReport(data.auto_report);
                }
                showSuccess();
                eventSource.close();
                break;
                
            case 'error':
                showError(data.message);
                eventSource.close();
                break;
        }
    }

    function showProfileSummary(profile) {
        const el = document.getElementById('automl-info');
        if (!el) return;
        
        el.innerHTML = `
            <div style="font-weight:700;color:#38BDF8;margin-bottom:8px">📋 Dataset Profile</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:13px">
                <span>📦 Rows: <b>${profile.rows?.toLocaleString()}</b></span>
                <span>📅 Days: <b>${profile.days}</b></span>
                <span>👥 Customers: <b>${profile.customers?.toLocaleString()}</b></span>
                <span>🌊 Seasonality: <b>${profile.seasonality}</b></span>
                <span>⭐ Quality: <b>${profile.quality_score}/100</b></span>
            </div>
        `;
    }

    function showAutoMLReport(report) {
        const container = document.getElementById('completionMessage') || document.body;
        const div = document.createElement('div');
        div.style.cssText = `
            background:#111827;border:1px solid #38BDF8;border-radius:12px;
            padding:20px;margin-top:16px
        `;
        div.innerHTML = `
            <div style="color:#38BDF8;font-weight:700;margin-bottom:12px">🤖 AutoML Selection Report</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:13px;color:#F1F5F9">
                <div style="background:#1E293B;padding:10px;border-radius:8px">
                    📈 Forecast Model<br>
                    <b style="color:#38BDF8">${report.forecast_model}</b><br>
                    <span style="color:#94A3B8">MAE: ${report.forecast_mae}</span>
                </div>
                <div style="background:#1E293B;padding:10px;border-radius:8px">
                    🚨 Risk Model<br>
                    <b style="color:#38BDF8">${report.risk_model}</b><br>
                    <span style="color:#94A3B8">AUC: ${report.risk_auc} ${report.risk_retrained ? '(retrained)' : '(reused)'}</span>
                </div>
                <div style="background:#1E293B;padding:10px;border-radius:8px">
                    👥 Segments<br>
                    <b style="color:#38BDF8">K = ${report.segments_k}</b><br>
                    <span style="color:#94A3B8">${report.customers_segmented?.toLocaleString()} customers</span>
                </div>
                <div style="background:#1E293B;padding:10px;border-radius:8px">
                    ⭐ Data Quality<br>
                    <b style="color:#38BDF8">${report.data_quality}/100</b><br>
                    <span style="color:#94A3B8">${report.seasonality} seasonality</span>
                </div>
            </div>
            ${report.errors?.length > 0 ? `
                <div style="margin-top:12px;color:#EF4444;font-size:12px">
                    ⚠️ ${report.errors.length} warning(s): ${report.errors.join(', ')}
                </div>
            ` : ''}
        `;
        container.appendChild(div);
    }

    function updateStep(stepNum, status, statusText) {
        const stepElement = document.getElementById(`step-${stepNum}`);
        const statusElement = stepElement.querySelector('.step-status');
        
        // Remove all status classes
        stepElement.classList.remove('running', 'complete', 'failed');
        statusElement.classList.remove('running', 'complete', 'failed');
        
        // Add new status
        if (status !== 'waiting') {
            stepElement.classList.add(status);
            statusElement.classList.add(status);
        }
        
        statusElement.textContent = statusText;
    }

    function updateProgress(percent) {
        progressFill.style.width = percent + '%';
        progressText.textContent = percent + '% Complete';
    }

    function scrollToStep(stepNum) {
        const stepElement = document.getElementById(`step-${stepNum}`);
        stepElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    function showSuccess() {
        completionContent.innerHTML = `
            <div style="font-size: 48px; margin-bottom: 16px;">🎉</div>
            <h3 style="color: var(--green); margin-bottom: 16px;">Pipeline Complete!</h3>
            <p style="color: var(--text-secondary); margin-bottom: 32px;">
                All analyses have been updated with your new data
            </p>
            <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap;">
                <a href="/" class="cp-btn cp-btn-primary">View Dashboard</a>
                <a href="/eda" class="cp-btn cp-btn-secondary">View EDA</a>
                <a href="/risk" class="cp-btn cp-btn-secondary">Check Risk</a>
            </div>
        `;
        completionMessage.style.display = 'block';
        completionMessage.scrollIntoView({ behavior: 'smooth' });
    }

    function showError(message) {
        completionContent.innerHTML = `
            <div style="font-size: 48px; margin-bottom: 16px;">❌</div>
            <h3 style="color: var(--red); margin-bottom: 16px;">Pipeline Failed</h3>
            <p style="color: var(--text-secondary); margin-bottom: 32px;">
                ${message}
            </p>
            <div style="display: flex; gap: 16px; justify-content: center;">
                <button onclick="location.reload()" class="cp-btn cp-btn-secondary">
                    🔄 Try Again
                </button>
                <a href="/health" class="cp-btn cp-btn-secondary">Check System Health</a>
            </div>
        `;
        completionMessage.style.display = 'block';
        completionMessage.scrollIntoView({ behavior: 'smooth' });
    }
});