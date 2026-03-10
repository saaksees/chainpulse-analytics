#!/usr/bin/env python3
"""
ChainPulse Analytics - Simple Flask App
"""

from flask import Flask, render_template_string
import os

# Create Flask app
app = Flask(__name__)

# HTML template with inline CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChainPulse ⚡ Analytics Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0A0E1A;
            --bg-card: #111827;
            --bg-sidebar: #080C16;
            --border: #1E293B;
            --blue: #38BDF8;
            --blue-glow: rgba(56,189,248,0.15);
            --purple: #7C3AED;
            --green: #10B981;
            --red: #EF4444;
            --amber: #F59E0B;
            --text-primary: #F1F5F9;
            --text-secondary: #94A3B8;
            --text-muted: #475569;
            --sidebar-width: 260px;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            display: flex;
            min-height: 100vh;
        }
        
        .cp-sidebar {
            width: var(--sidebar-width);
            background: var(--bg-sidebar);
            border-right: 1px solid var(--border);
            position: fixed;
            height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }
        
        .cp-logo {
            padding: 28px 24px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 14px;
            text-decoration: none;
        }
        
        .cp-logo-icon {
            font-size: 32px;
            filter: drop-shadow(0 0 12px rgba(56,189,248,0.6));
        }
        
        .cp-logo-text {
            font-size: 22px;
            font-weight: 800;
            background: linear-gradient(135deg, #38BDF8, #7C3AED);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }
        
        .cp-logo-version {
            font-size: 10px;
            color: var(--text-muted);
            margin-top: 2px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        
        .cp-nav {
            padding: 20px 12px;
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        
        .cp-nav-section {
            font-size: 10px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 2px;
            padding: 8px 16px;
            margin-top: 8px;
        }
        
        .cp-nav-item {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 13px 16px;
            border-radius: 12px;
            text-decoration: none;
            color: var(--text-secondary);
            font-size: 14px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .cp-nav-item:hover {
            background: var(--bg-card);
            color: var(--text-primary);
            transform: translateX(4px);
        }
        
        .cp-nav-item.active {
            background: linear-gradient(135deg, var(--blue-glow), rgba(124,58,237,0.15));
            color: var(--blue);
            border: 1px solid rgba(56,189,248,0.2);
        }
        
        .cp-nav-icon {
            font-size: 18px;
            width: 24px;
            text-align: center;
        }
        
        .cp-sidebar-footer {
            padding: 20px 24px;
            border-top: 1px solid var(--border);
        }
        
        .cp-sidebar-footer p {
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.8;
        }
        
        .cp-main {
            margin-left: var(--sidebar-width);
            flex: 1;
            background: var(--bg-primary);
        }
        
        .cp-content {
            padding: 40px;
            max-width: 1400px;
        }
        
        .cp-hero {
            text-align: center;
            padding: 80px 40px;
            position: relative;
        }
        
        .cp-hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 20px;
            background: var(--blue-glow);
            border: 1px solid rgba(56,189,248,0.3);
            border-radius: 50px;
            font-size: 13px;
            font-weight: 600;
            color: var(--blue);
            margin-bottom: 32px;
        }
        
        .cp-hero-title {
            font-size: 72px;
            font-weight: 800;
            line-height: 1;
            letter-spacing: -3px;
            margin-bottom: 16px;
        }
        
        .gradient {
            background: linear-gradient(135deg, #38BDF8, #7C3AED);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .cp-hero-subtitle {
            font-size: 22px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 16px;
        }
        
        .cp-hero-desc {
            font-size: 16px;
            color: var(--text-muted);
            max-width: 560px;
            margin: 0 auto 40px;
            line-height: 1.7;
        }
        
        .cp-hero-buttons {
            display: flex;
            gap: 16px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .cp-kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .cp-kpi-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 28px 24px;
            position: relative;
            transition: all 0.3s ease;
        }
        
        .cp-kpi-card::after {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            border-radius: 16px 16px 0 0;
        }
        
        .cp-kpi-card.blue::after { background: var(--blue); }
        .cp-kpi-card.green::after { background: var(--green); }
        .cp-kpi-card.red::after { background: var(--red); }
        .cp-kpi-card.amber::after { background: var(--amber); }
        .cp-kpi-card.purple::after { background: var(--purple); }
        
        .cp-kpi-card:hover {
            border-color: var(--blue);
            transform: translateY(-6px);
            box-shadow: 0 24px 48px rgba(0,0,0,0.3);
        }
        
        .cp-kpi-icon {
            font-size: 28px;
            margin-bottom: 16px;
            display: block;
        }
        
        .cp-kpi-label {
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 10px;
        }
        
        .cp-kpi-value {
            font-size: 32px;
            font-weight: 800;
            color: var(--text-primary);
            line-height: 1;
            margin-bottom: 8px;
            letter-spacing: -1px;
        }
        
        .cp-kpi-sub {
            font-size: 13px;
            color: var(--text-secondary);
        }
        
        .cp-btn {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 14px 28px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            border: none;
            font-family: 'Inter', sans-serif;
            text-decoration: none;
        }
        
        .cp-btn-primary {
            background: linear-gradient(135deg, #38BDF8, #0EA5E9);
            color: #0A0E1A;
            box-shadow: 0 4px 20px rgba(56,189,248,0.3);
        }
        
        .cp-btn-primary:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 32px rgba(56,189,248,0.4);
        }
        
        .cp-btn-secondary {
            background: transparent;
            color: var(--text-primary);
            border: 1px solid var(--border);
        }
        
        .cp-btn-secondary:hover {
            background: var(--bg-card);
            border-color: var(--blue);
            color: var(--blue);
            transform: translateY(-3px);
        }
        
        .cp-divider {
            height: 1px;
            background: var(--border);
            margin: 40px 0;
        }
        
        .cp-page-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 14px;
            background: var(--blue-glow);
            border: 1px solid rgba(56,189,248,0.3);
            border-radius: 50px;
            font-size: 12px;
            font-weight: 600;
            color: var(--blue);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 16px;
        }
        
        .cp-page-title {
            font-size: 36px;
            font-weight: 800;
            color: var(--text-primary);
            line-height: 1.2;
            margin-bottom: 12px;
            letter-spacing: -1px;
        }
        
        .cp-page-title span {
            background: linear-gradient(135deg, #38BDF8, #7C3AED);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .down { color: var(--red); }
    </style>
</head>
<body>
    <!-- SIDEBAR -->
    <nav class="cp-sidebar">
        <a href="/" class="cp-logo">
            <span class="cp-logo-icon">⚡</span>
            <div>
                <div class="cp-logo-text">ChainPulse</div>
                <div class="cp-logo-version">v1.0 · Analytics</div>
            </div>
        </a>
        
        <div class="cp-nav">
            <div class="cp-nav-section">Main</div>
            <a href="/" class="cp-nav-item active">
                <span class="cp-nav-icon">🏠</span>
                <span class="cp-nav-label">Home</span>
            </a>
            
            <div class="cp-nav-section">Analytics</div>
            <a href="/eda" class="cp-nav-item">
                <span class="cp-nav-icon">📊</span>
                <span class="cp-nav-label">EDA Explorer</span>
            </a>
            <a href="/risk" class="cp-nav-item">
                <span class="cp-nav-icon">🚨</span>
                <span class="cp-nav-label">Risk Analyzer</span>
            </a>
            <a href="/forecast" class="cp-nav-item">
                <span class="cp-nav-icon">📈</span>
                <span class="cp-nav-label">Demand Forecast</span>
            </a>
            <a href="/customers" class="cp-nav-item">
                <span class="cp-nav-icon">👥</span>
                <span class="cp-nav-label">Customer Intel</span>
            </a>
            <a href="/nlp" class="cp-nav-item">
                <span class="cp-nav-icon">🔍</span>
                <span class="cp-nav-label">NLP Insights</span>
            </a>
        </div>
        
        <div class="cp-sidebar-footer">
            <p><strong>Built by</strong></p>
            <p>Saakshi Jaiswal</p>
            <p style="margin-top:8px; color:#38BDF8">ChainPulse v1.0</p>
        </div>
    </nav>
    
    <!-- MAIN -->
    <main class="cp-main">
        <div class="cp-content">
            <!-- HERO SECTION -->
            <div class="cp-hero">
                <div class="cp-hero-badge">⚡ Supply Chain Intelligence Platform</div>
                <h1 class="cp-hero-title"><span class="gradient">ChainPulse</span></h1>
                <p class="cp-hero-subtitle">Feel the pulse of your supply chain</p>
                <p class="cp-hero-desc">Predict delivery failures, forecast demand, segment customers and uncover opportunities — powered by ML, Prophet and NLP on 180K+ real orders.</p>
                <div class="cp-hero-buttons">
                    <a href="/risk" class="cp-btn cp-btn-primary">🚨 Analyze Risk</a>
                    <a href="/eda" class="cp-btn cp-btn-secondary">📊 Explore Data</a>
                </div>
            </div>

            <div class="cp-divider"></div>

            <!-- KPI CARDS -->
            <div style="margin-bottom: 40px;">
                <div class="cp-page-badge">📊 Live Metrics</div>
                <h2 class="cp-page-title">Platform <span>Overview</span></h2>
            </div>

            <div class="cp-kpi-grid">
                <div class="cp-kpi-card blue">
                    <span class="cp-kpi-icon">💰</span>
                    <div class="cp-kpi-label">Total Revenue</div>
                    <div class="cp-kpi-value">$7.4M</div>
                    <div class="cp-kpi-sub">Across all markets</div>
                </div>
                
                <div class="cp-kpi-card purple">
                    <span class="cp-kpi-icon">📦</span>
                    <div class="cp-kpi-label">Total Orders</div>
                    <div class="cp-kpi-value">180K</div>
                    <div class="cp-kpi-sub">Jan 2015 – Oct 2017</div>
                </div>
                
                <div class="cp-kpi-card red">
                    <span class="cp-kpi-icon">🚨</span>
                    <div class="cp-kpi-label">Late Delivery Rate</div>
                    <div class="cp-kpi-value">54.8%</div>
                    <div class="cp-kpi-sub"><span class="down">↑ Critical issue</span></div>
                </div>
                
                <div class="cp-kpi-card amber">
                    <span class="cp-kpi-icon">⚠️</span>
                    <div class="cp-kpi-label">Revenue at Risk</div>
                    <div class="cp-kpi-value">$602K</div>
                    <div class="cp-kpi-sub">High risk orders</div>
                </div>
                
                <div class="cp-kpi-card green">
                    <span class="cp-kpi-icon">👥</span>
                    <div class="cp-kpi-label">Customers</div>
                    <div class="cp-kpi-value">14.3K</div>
                    <div class="cp-kpi-sub">Segmented into 7 groups</div>
                </div>
                
                <div class="cp-kpi-card purple">
                    <span class="cp-kpi-icon">🏆</span>
                    <div class="cp-kpi-label">Champion Customers</div>
                    <div class="cp-kpi-value">10.8%</div>
                    <div class="cp-kpi-sub">Drive 20% of revenue</div>
                </div>
            </div>

            <div class="cp-divider"></div>
            
            <div style="text-align: center; padding: 40px 0;">
                <h2 style="color: var(--text-primary); margin-bottom: 20px;">🎉 ChainPulse Dashboard Successfully Loaded!</h2>
                <p style="color: var(--text-secondary); font-size: 18px;">Dark theme with colorful KPI cards and professional styling</p>
            </div>
        </div>
    </main>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/eda')
def eda():
    return "<h1>EDA Explorer - Coming Soon</h1>"

@app.route('/risk')
def risk():
    return "<h1>Risk Analyzer - Coming Soon</h1>"

@app.route('/forecast')
def forecast():
    return "<h1>Demand Forecast - Coming Soon</h1>"

@app.route('/customers')
def customers():
    return "<h1>Customer Intel - Coming Soon</h1>"

@app.route('/nlp')
def nlp():
    return "<h1>NLP Insights - Coming Soon</h1>"

if __name__ == '__main__':
    print("🚀 Starting ChainPulse Analytics Dashboard...")
    print("📊 Dashboard will be available at: http://localhost:5000")
    print("⚡ ChainPulse v1.0 - Supply Chain Intelligence Platform")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )