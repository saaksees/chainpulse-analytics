// ── Reset to Default ─────────────────
async function resetToDefault() {
    if (!confirm('Reset to DataCo default dataset?\n' +
                'Current analysis will be ' +
                'preserved in version history.')) {
        return;
    }
    
    try {
        const res = await fetch('/api/restore/defaults', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'}
        });
        
        const data = await res.json();
        
        if (data.success) {
            showToast('✅ DataCo defaults restored!', 'success');
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        } else {
            showToast('❌ ' + data.message, 'error');
        }
    } catch (err) {
        showToast('❌ Reset failed: ' + err, 'error');
    }
}

// ── Switch Version ───────────────────
async function switchVersion(versionId, versionNum, filename) {
    const confirmed = confirm(`Switch dashboard to ${versionNum}?\n\n` +
        `File: ${filename}\n\n` +
        `All analytics will instantly restore ` +
        `to this version's data.\n` +
        `No re-running needed.`);
    
    if (!confirmed) return;
    
    const btn = document.getElementById(`switch-btn-${versionId}`);
    if (btn) {
        btn.textContent = '⏳ Switching...';
        btn.disabled = true;
    }
    
    try {
        const res = await fetch(`/api/versions/switch/${versionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await res.json();
        
        if (data.success) {
            showToast(`✅ Switched to ${versionNum}!`, 'success');
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            showToast(`❌ ${data.message}`, 'error');
            if (btn) {
                btn.textContent = '🔄 Switch to This';
                btn.disabled = false;
            }
        }
    } catch (err) {
        showToast('❌ Switch failed. Try again.', 'error');
        if (btn) {
            btn.textContent = '🔄 Switch to This';
            btn.disabled = false;
        }
    }
}

// ── Compare Versions ─────────────────
async function compareVersion(v2Id, v2Num, v1Id, v1Num) {
    // Show modal with loading state
    document.getElementById('compare-modal').style.display = 'flex';
    document.getElementById('compare-title').textContent = `${v1Num} (Active) vs ${v2Num}`;
    document.getElementById('compare-v1-header').textContent = `✅ ${v1Num} (Active)`;
    document.getElementById('compare-v2-header').textContent = `📦 ${v2Num}`;
    document.getElementById('compare-rows').innerHTML = 
        '<div style="text-align:center;' +
        'color:#94A3B8;padding:40px">' +
        '⏳ Loading comparison...</div>';
    
    try {
        const res = await fetch('/api/versions/compare', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                v1_id: v1Id,
                v2_id: v2Id
            })
        });
        
        const data = await res.json();
        
        if (data.success) {
            renderComparison(data.comparison, v1Num, v2Num);
        } else {
            document.getElementById('compare-rows').innerHTML = 
                '<div style="color:#EF4444;' +
                'text-align:center;padding:40px">' +
                '❌ Could not load comparison' +
                '</div>';
        }
    } catch (err) {
        document.getElementById('compare-rows').innerHTML = 
            '<div style="color:#EF4444;' +
            'text-align:center;padding:40px">' +
            '❌ Error loading data</div>';
    }
}

// ── Render comparison table ───────────
function renderComparison(comp, v1Num, v2Num) {
    const v1 = comp.v1;
    const v2 = comp.v2;
    const changes = comp.changes;
    
    const metrics = [
        {
            label: '📦 Total Orders',
            v1val: fmt(v1.total_orders),
            v2val: fmt(v2.total_orders),
            change: changes.orders,
            higherIsBetter: true
        },
        {
            label: '💰 Total Revenue',
            v1val: fmtRev(v1.total_revenue),
            v2val: fmtRev(v2.total_revenue),
            change: changes.revenue,
            higherIsBetter: true
        },
        {
            label: '⏰ Late Rate %',
            v1val: (v1.late_rate || 0).toFixed(1) + '%',
            v2val: (v2.late_rate || 0).toFixed(1) + '%',
            change: changes.late_rate,
            higherIsBetter: false
        }
    ];
    
    // Add segment data if available
    if (v1.segments && v2.segments) {
        const segs = new Set([
            ...Object.keys(v1.segments || {}),
            ...Object.keys(v2.segments || {})
        ]);
        
        segs.forEach(seg => {
            metrics.push({
                label: `👥 ${seg}`,
                v1val: fmt(v1.segments[seg] || 0),
                v2val: fmt(v2.segments[seg] || 0),
                change: (v2.segments[seg] || 0) - (v1.segments[seg] || 0),
                higherIsBetter: true
            });
        });
    }
    
    let html = '';
    metrics.forEach(m => {
        const isPositive = m.higherIsBetter ? m.change > 0 : m.change < 0;
        const isNeutral = m.change === 0;
        const arrow = isNeutral ? '→' : isPositive ? '↑' : '↓';
        const color = isNeutral ? '#94A3B8' : isPositive ? '#10b981' : '#EF4444';
        const changePct = m.change !== 0 ? 
            ` (${m.change > 0 ? '+' : ''}${typeof m.change === 'number' ? m.change.toFixed(1) : m.change})` : '';
        
        html += `
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;padding:12px 16px;background:#0A0E1A;border-radius:8px;align-items:center">
                <div style="color:#94A3B8;font-size:13px">${m.label}</div>
                <div style="color:#F1F5F9;font-size:15px;font-weight:600;text-align:center">${m.v1val}</div>
                <div style="display:flex;align-items:center;justify-content:center;gap:8px">
                    <span style="color:#F1F5F9;font-size:15px;font-weight:600">${m.v2val}</span>
                    <span style="color:${color};font-size:13px;font-weight:700">${arrow}${changePct}</span>
                </div>
            </div>
        `;
    });
    
    document.getElementById('compare-rows').innerHTML = html;
}

// ── Close modal ───────────────────────
function closeCompare() {
    document.getElementById('compare-modal').style.display = 'none';
}

// Close on backdrop click
document.getElementById('compare-modal').addEventListener('click', function(e) {
    if (e.target === this) closeCompare();
});

// ── Toast notification ────────────────
function showToast(message, type) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.display = 'block';
    
    if (type === 'success') {
        toast.style.background = '#052e16';
        toast.style.color = '#10b981';
        toast.style.border = '1px solid #10b981';
    } else {
        toast.style.background = '#7F1D1D';
        toast.style.color = '#FCA5A5';
        toast.style.border = '1px solid #EF4444';
    }
    
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

// ── Format helpers ────────────────────
function fmt(num) {
    if (!num && num !== 0) return '—';
    return Number(num).toLocaleString();
}

function fmtRev(num) {
    if (!num && num !== 0) return '—';
    if (num >= 1000000) return '$' + (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return '$' + (num / 1000).toFixed(1) + 'K';
    return '$' + num.toFixed(2);
}