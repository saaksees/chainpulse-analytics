// ── State ─────────────────────────────
let currentPrediction = null;

// ── Demo loader ───────────────────────
function loadDemoPrediction() {
    initWhatIf({
        shipping: 'First Class',
        region: 'Western Europe',
        category: 'Fishing',
        sales: 250,
        quantity: 2,
        discount_rate: 0.1,
        profit_ratio: 0.3,
        scheduled_days: 4
    });

    // Also fill in the current order display immediately
    document.getElementById('wi-cur-shipping').textContent = 'First Class';
    document.getElementById('wi-cur-region').textContent = 'Western Europe';
    document.getElementById('wi-cur-category').textContent = 'Fishing';

    // Show feedback to user
    const btn = document.querySelector('[onclick="loadDemoPrediction()"]');
    if (btn) {
        btn.textContent = '✅ Demo Loaded!';
        btn.style.background = '#10b981';
        setTimeout(() => {
            btn.textContent = '🚀 Load Demo Prediction';
            btn.style.background = '#38BDF8';
        }, 2000);
    }
}

// ── Called after real risk prediction ─
function initWhatIf(predictionData) {
    currentPrediction = predictionData;

    // Populate current order display
    const shipping = predictionData.shipping || 'Standard Class';
    const region = predictionData.region || 'Western Europe';
    const category = predictionData.category || 'Fishing';

    const shippingEl = document.getElementById('wi-cur-shipping');
    const regionEl = document.getElementById('wi-cur-region');
    const categoryEl = document.getElementById('wi-cur-category');

    if (shippingEl) shippingEl.textContent = shipping;
    if (regionEl) regionEl.textContent = region;
    if (categoryEl) categoryEl.textContent = category;

    // Store values
    currentPrediction.shipping = shipping;
    currentPrediction.region = region;
    currentPrediction.category = category;

    // Set what-if dropdowns to match current values as starting point
    const wiShipping = document.getElementById('wi-shipping');
    const wiRegion = document.getElementById('wi-region');
    const wiCategory = document.getElementById('wi-category');

    if (wiShipping) {
        // Try to select matching option
        for (let opt of wiShipping.options) {
            if (opt.value === shipping) {
                wiShipping.value = shipping;
                break;
            }
        }
    }

    if (wiRegion) {
        for (let opt of wiRegion.options) {
            if (opt.value === region) {
                wiRegion.value = region;
                break;
            }
        }
    }

    // Enable the run button
    const btn = document.getElementById('wi-run-btn');
    if (btn) {
        btn.disabled = false;
        btn.textContent = '🎮 Run What-If Analysis';
        btn.style.background = '#38BDF8';
        btn.style.color = '#0A0E1A';
        btn.style.border = 'none';
        btn.style.cursor = 'pointer';
        btn.style.opacity = '1';
    }

    // Scroll to simulator section
    const section = document.getElementById('whatif-section');
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// ── Run what-if prediction ────────────
async function runWhatIf() {
    if (!currentPrediction) {
        alert('Please load a prediction first using the demo button or run a risk prediction above.');
        return;
    }

    const btn = document.getElementById('wi-run-btn');
    if (btn) {
        btn.textContent = '⏳ Analyzing...';
        btn.disabled = true;
        btn.style.opacity = '0.7';
    }

    const wiShipping = document.getElementById('wi-shipping')?.value || 'Standard Class';
    const wiRegion = document.getElementById('wi-region')?.value || 'Western Europe';
    const wiCategory = document.getElementById('wi-category')?.value || 'Fishing';

    const payload = {
        original_shipping: currentPrediction.shipping,
        original_region: currentPrediction.region,
        original_category: currentPrediction.category,
        whatif_shipping: wiShipping,
        whatif_region: wiRegion,
        whatif_category: wiCategory,
        sales: currentPrediction.sales || 250,
        quantity: currentPrediction.quantity || 2,
        discount_rate: currentPrediction.discount_rate || 0.1,
        profit_ratio: currentPrediction.profit_ratio || 0.3,
        scheduled_days: currentPrediction.scheduled_days || 4
    };

    console.log('What-If payload:', payload);

    try {
        const res = await fetch('/api/risk/whatif', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        console.log('Response status:', res.status);

        if (!res.ok) {
            const errText = await res.text();
            console.error('Error:', errText);
            alert('Server error: ' + res.status + '\n' + errText);
            return;
        }

        const data = await res.json();
        console.log('What-If result:', data);

        if (data.success) {
            displayWhatIfResults(data);
        } else {
            alert('Prediction error:\n' + (data.error || 'Unknown error'));
        }
    } catch (err) {
        console.error('Fetch error:', err);
        alert('Request failed: ' + err.message + '\nCheck console for details.');
    } finally {
        if (btn) {
            btn.textContent = '🎮 Run What-If Analysis';
            btn.disabled = false;
            btn.style.opacity = '1';
        }
    }
}

// ── Display results ───────────────────
function displayWhatIfResults(data) {
    const resultsEl = document.getElementById('wi-results');
    if (resultsEl) {
        resultsEl.style.display = 'block';
    }

    // Original badge
    setRiskBadge('wi-orig-badge', data.original.risk_level);
    const origProb = document.getElementById('wi-orig-prob');
    if (origProb) {
        origProb.textContent = 'Probability: ' + ((data.original.probability || 0) * 100).toFixed(1) + '%';
    }
    const origRev = document.getElementById('wi-orig-rev');
    if (origRev) {
        origRev.textContent = 'At Risk: $' + (data.original.revenue_at_risk || 0).toFixed(2);
    }

    // What-if badge
    setRiskBadge('wi-whatif-badge', data.whatif.risk_level);
    const whatifProb = document.getElementById('wi-whatif-prob');
    if (whatifProb) {
        whatifProb.textContent = 'Probability: ' + ((data.whatif.probability || 0) * 100).toFixed(1) + '%';
    }
    const whatifRev = document.getElementById('wi-whatif-rev');
    if (whatifRev) {
        whatifRev.textContent = 'At Risk: $' + (data.whatif.revenue_at_risk || 0).toFixed(2);
    }

    // Arrow
    const arrow = document.getElementById('wi-arrow');
    if (arrow) {
        if (data.improved) {
            arrow.textContent = '↓';
            arrow.style.color = '#10b981';
            arrow.style.fontSize = '36px';
        } else if (data.worsened) {
            arrow.textContent = '↑';
            arrow.style.color = '#EF4444';
            arrow.style.fontSize = '36px';
        } else {
            arrow.textContent = '→';
            arrow.style.color = '#94A3B8';
            arrow.style.fontSize = '28px';
        }
    }

    // Savings box
    const savingsBox = document.getElementById('wi-savings-box');
    const savingsAmt = document.getElementById('wi-savings-amt');
    if (savingsAmt) {
        const savings = data.savings || 0;
        savingsAmt.textContent = (savings >= 0 ? '+' : '-') + '$' + Math.abs(savings).toFixed(2);
    }

    if (savingsBox) {
        if (data.improved) {
            savingsBox.style.background = '#052e16';
            savingsBox.style.borderColor = '#10b981';
            if (savingsAmt) savingsAmt.style.color = '#10b981';
        } else if (data.worsened) {
            savingsBox.style.background = '#7F1D1D';
            savingsBox.style.borderColor = '#EF4444';
            if (savingsAmt) savingsAmt.style.color = '#EF4444';
        } else {
            savingsBox.style.background = '#1E293B';
            savingsBox.style.borderColor = '#334155';
            if (savingsAmt) savingsAmt.style.color = '#94A3B8';
        }
    }

    // Recommendation
    const recEl = document.getElementById('wi-recommendation');
    if (recEl) {
        recEl.textContent = data.recommendation || '';
    }

    // Scroll to results
    if (resultsEl) {
        resultsEl.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest'
        });
    }
}

// ── Risk badge helper ─────────────────
function setRiskBadge(elemId, riskLevel) {
    const el = document.getElementById(elemId);
    if (!el) return;

    el.textContent = riskLevel || 'Unknown';

    const styles = {
        'High Risk': {
            bg: '#7F1D1D',
            color: '#FCA5A5',
            border: '#EF4444'
        },
        'Medium Risk': {
            bg: '#78350F',
            color: '#FCD34D',
            border: '#F59E0B'
        },
        'Low Risk': {
            bg: '#052e16',
            color: '#6EE7B7',
            border: '#10b981'
        }
    };

    const s = styles[riskLevel] || styles['Medium Risk'];
    el.style.background = s.bg;
    el.style.color = s.color;
    el.style.border = `1px solid ${s.border}`;
    el.style.padding = '6px 16px';
    el.style.borderRadius = '8px';
    el.style.display = 'inline-block';
}