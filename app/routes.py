# ChainPulse — routes.py
from flask import Blueprint, render_template, jsonify, request, current_app
from .auth import require_auth
import pandas as pd
import os
import json
from datetime import datetime

main = Blueprint('main', __name__)

def safe_json(obj):
    import numpy as np
    if isinstance(obj, dict):
        return {k: safe_json(v)
                for k, v in obj.items()}
    elif isinstance(obj, list):
        return [safe_json(i)
                for i in obj]
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif hasattr(obj, 'item'):
        return obj.item()
    return obj

@main.route('/')
@require_auth
def home():
    """Homepage with project overview and key metrics"""
    from flask_login import current_user
    print(f"DEBUG: User authenticated: {current_user.is_authenticated}")
    if current_user.is_authenticated:
        print(f"DEBUG: Current user: {current_user.username}")
        print(f"DEBUG: Current user role: {current_user.role}")
        print(f"DEBUG: Current user initials: {getattr(current_user, 'initials', 'NO_INITIALS')}")
    else:
        print("DEBUG: No user authenticated")
    try:
        # Load key metrics from processed data
        stats = get_dashboard_stats()
        return render_template('home.html', stats=stats)
    except Exception as e:
        print(f"Error loading home page: {e}")
        return render_template('home.html', stats={})

@main.route('/eda')
@require_auth
def eda():
    """Exploratory Data Analysis dashboard"""
    return render_template('eda.html')

@main.route('/risk')
@require_auth
def risk():
    """Delivery Risk Analysis dashboard"""
    try:
        # Load risk analysis data
        risk_data = get_risk_analysis_data()
        return render_template('risk.html', risk_data=risk_data)
    except Exception as e:
        print(f"Error loading risk page: {e}")
        return render_template('risk.html', risk_data={})

@main.route('/forecast')
@require_auth
def forecast():
    """Demand Forecasting dashboard"""
    try:
        # Load forecast data
        forecast_data = get_forecast_data()
        return render_template('forecast.html', forecast_data=forecast_data)
    except Exception as e:
        print(f"Error loading forecast page: {e}")
        return render_template('forecast.html', forecast_data={})

@main.route('/customers')
@require_auth
def customers():
    """Customer Segmentation (RFM) dashboard"""
    try:
        # Load customer segmentation data
        customer_data = get_customer_data()
        return render_template('customers.html', customer_data=customer_data)
    except Exception as e:
        print(f"Error loading customers page: {e}")
        return render_template('customers.html', customer_data={})

@main.route('/nlp')
@require_auth
def nlp():
    """NLP Product Analysis dashboard"""
    try:
        # Load NLP analysis data
        nlp_data = get_nlp_data()
        return render_template('nlp.html', nlp_data=nlp_data)
    except Exception as e:
        print(f"Error loading NLP page: {e}")
        return render_template('nlp.html', nlp_data={})

# API Endpoints for dynamic data
@main.route('/api/stats')
@require_auth
def api_stats():
    """API endpoint for dashboard statistics"""
    return jsonify(get_dashboard_stats())

def get_dashboard_stats():
    """Load key statistics for the dashboard"""
    stats = {
        'total_orders': 0,
        'total_revenue': 0,
        'high_risk_orders': 0,
        'customer_segments': 0,
        'forecast_accuracy': 0,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    try:
        # Load processed data files if they exist
        if os.path.exists(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'delivery_risk_scored.csv')):
            risk_df = pd.read_csv(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'delivery_risk_scored.csv'), encoding='latin-1', low_memory=False)
            stats['total_orders'] = len(risk_df)
            stats['high_risk_orders'] = len(risk_df[risk_df.get('Risk_Level', '') == 'High Risk'])
            stats['total_revenue'] = risk_df.get('Sales', pd.Series()).sum()
        
        if os.path.exists(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'customer_segments.csv')):
            customer_df = pd.read_csv(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'customer_segments.csv'), encoding='latin-1', low_memory=False)
            stats['customer_segments'] = customer_df.get('Segment', pd.Series()).nunique()
            
    except Exception as e:
        print(f"Error loading stats: {e}")
    
    return stats
def get_risk_analysis_data():
    """Load risk analysis data"""
    data = {'risk_summary': {}, 'risk_distribution': []}
    
    try:
        if os.path.exists(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'delivery_risk_scored.csv')):
            df = pd.read_csv(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'delivery_risk_scored.csv'), encoding='latin-1', low_memory=False)
            
            # Risk level distribution
            if 'Risk_Level' in df.columns:
                risk_counts = df['Risk_Level'].value_counts()
                data['risk_distribution'] = [
                    {'level': level, 'count': int(count), 'percentage': round(count/len(df)*100, 1)}
                    for level, count in risk_counts.items()
                ]
                
                # Risk summary
                data['risk_summary'] = {
                    'total_orders': len(df),
                    'high_risk': int(risk_counts.get('High Risk', 0)),
                    'medium_risk': int(risk_counts.get('Medium Risk', 0)),
                    'low_risk': int(risk_counts.get('Low Risk', 0))
                }
    except Exception as e:
        print(f"Error loading risk data: {e}")
    
    return data

def get_forecast_data():
    """Load demand forecasting data"""
    data = {'categories': [], 'forecast_summary': {}}
    
    try:
        if os.path.exists(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'demand_forecast_results.csv')):
            df = pd.read_csv(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'demand_forecast_results.csv'), encoding='latin-1', low_memory=False)
            
            # Category forecasts
            if 'Category' in df.columns and 'Predicted_Sales' in df.columns:
                category_totals = df.groupby('Category')['Predicted_Sales'].sum().round(2)
                data['categories'] = [
                    {'name': cat, 'forecast': float(total)}
                    for cat, total in category_totals.items()
                ]
                
                data['forecast_summary'] = {
                    'total_forecast': float(df['Predicted_Sales'].sum()),
                    'categories_count': df['Category'].nunique(),
                    'forecast_days': 90
                }
    except Exception as e:
        print(f"Error loading forecast data: {e}")
    
    return data

def get_customer_data():
    """Load customer segmentation data"""
    data = {'segments': [], 'segment_summary': {}}
    
    try:
        if os.path.exists(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'customer_segments.csv')):
            df = pd.read_csv(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'customer_segments.csv'), encoding='latin-1', low_memory=False)
            
            if 'Segment' in df.columns:
                segment_counts = df['Segment'].value_counts()
                data['segments'] = [
                    {'name': seg, 'count': int(count), 'percentage': round(count/len(df)*100, 1)}
                    for seg, count in segment_counts.items()
                ]
                
                data['segment_summary'] = {
                    'total_customers': len(df),
                    'segments_count': df['Segment'].nunique()
                }
    except Exception as e:
        print(f"Error loading customer data: {e}")
    
    return data

def get_nlp_data():
    """Load NLP analysis data"""
    data = {'product_insights': {}, 'categories': []}
    
    try:
        if os.path.exists(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'product_nlp_analysis.csv')):
            df = pd.read_csv(os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed', 'product_nlp_analysis.csv'), encoding='latin-1', low_memory=False)
            
            data['product_insights'] = {
                'total_products': len(df),
                'categories_analyzed': df.get('Category Name', pd.Series()).nunique() if 'Category Name' in df.columns else 0
            }
    except Exception as e:
        print(f"Error loading NLP data: {e}")
    
    return data

@main.route('/api/risk/whatif', methods=['POST'])
@require_auth
def risk_whatif():
    try:
        from app.ml_predictor import RiskPredictor
        import pandas as pd
        
        data = request.get_json()
        predictor = RiskPredictor(current_app.config['MODELS_PATH'])
        
        # Build original input
        original_input = {
            'Shipping Mode': data.get('original_shipping', 'Standard Class'),
            'Order Region': data.get('original_region', 'Western Europe'),
            'Category Name': data.get('original_category', 'Fishing'),
            'Sales': float(data.get('sales', 200)),
            'Order Item Quantity': int(data.get('quantity', 1)),
            'Order Item Discount Rate': float(data.get('discount_rate', 0.1)),
            'Order Item Profit Ratio': float(data.get('profit_ratio', 0.3)),
            'Days for shipment (scheduled)': int(data.get('scheduled_days', 4))
        }
        
        # Build what-if input
        whatif_input = original_input.copy()
        whatif_input['Shipping Mode'] = data.get('whatif_shipping', original_input['Shipping Mode'])
        whatif_input['Order Region'] = data.get('whatif_region', original_input['Order Region'])
        whatif_input['Category Name'] = data.get('whatif_category', original_input['Category Name'])
        
        # Get predictions
        orig = predictor.predict(original_input)
        whatif = predictor.predict(whatif_input)
        
        # Risk to number
        risk_map = {
            'High Risk': 3,
            'Medium Risk': 2,
            'Low Risk': 1
        }
        
        orig_score = risk_map.get(orig['risk_level'], 2)
        whatif_score = risk_map.get(whatif['risk_level'], 2)
        
        # Revenue at risk calcs
        sales = float(data.get('sales', 200))
        risk_mult = {
            'High Risk': 0.35,
            'Medium Risk': 0.15,
            'Low Risk': 0.05
        }
        
        orig_at_risk = sales * risk_mult.get(orig['risk_level'], 0.15)
        whatif_at_risk = sales * risk_mult.get(whatif['risk_level'], 0.15)
        savings = orig_at_risk - whatif_at_risk
        
        # Recommendation
        if whatif_score < orig_score:
            rec = (f"✅ Switching to "
                   f"{whatif_input['Shipping Mode']}"
                   f" reduces risk from "
                   f"{orig['risk_level']} to "
                   f"{whatif['risk_level']}. "
                   f"Estimated saving: "
                   f"${savings:.2f} per order.")
        elif whatif_score > orig_score:
            rec = (f"⚠️ This change INCREASES "
                   f"risk from {orig['risk_level']}"
                   f" to {whatif['risk_level']}. "
                   f"Not recommended.")
        else:
            rec = (f"ℹ️ No change in risk level. "
                   f"Both options result in "
                   f"{orig['risk_level']}.")
        
        return jsonify({
            'success': True,
            'original': {
                'risk_level': orig['risk_level'],
                'probability': orig.get('probability', 0),
                'score': orig_score,
                'revenue_at_risk': round(orig_at_risk, 2)
            },
            'whatif': {
                'risk_level': whatif['risk_level'],
                'probability': whatif.get('probability', 0),
                'score': whatif_score,
                'revenue_at_risk': round(whatif_at_risk, 2)
            },
            'savings': round(savings, 2),
            'improved': whatif_score < orig_score,
            'worsened': whatif_score > orig_score,
            'recommendation': rec
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
from datetime import datetime as dt

@main.route('/api/report/<page_name>')
@require_auth
def download_report(page_name):
    try:
        from app.report_generator import generate_report
        from flask import send_file
        
        valid = ['eda', 'risk', 'forecast', 'customers', 'nlp']
        if page_name not in valid:
            return jsonify({'error': 'Invalid page'}), 400
        
        project_root = current_app.config['PROJECT_ROOT']
        pdf_buffer = generate_report(page_name, project_root)
        
        filename = (f"chainpulse_{page_name}_"
                   f"{dt.now().strftime('%Y%m%d')}"
                   f".pdf")
        
        return send_file(pdf_buffer,
                        mimetype='application/pdf',
                        as_attachment=True,
                        download_name=filename)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ═══════════════════════════════════════════════════════════════════════════════
# CHART API ENDPOINTS - Dynamic Chart.js Data
# ═══════════════════════════════════════════════════════════════════════════════

@main.route('/api/eda/charts')
@require_auth
def eda_charts():
    import pandas as pd
    import os
    from flask import jsonify, current_app
    
    try:
        processed = os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed')
        risk_file = os.path.join(processed, 'delivery_risk_scored.csv')
        
        if not os.path.exists(risk_file):
            return jsonify({'no_data': True})
        
        df = pd.read_csv(risk_file, encoding='latin-1', low_memory=False)
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce').fillna(0)
        
        # Revenue by Region
        region_data = (df.groupby('Order Region')['Sales'].sum()
                      .sort_values(ascending=False).head(10))
        
        # Revenue by Category
        cat_data = (df.groupby('Category Name')['Sales'].sum()
                   .sort_values(ascending=False).head(10))
        
        # Late rate by Shipping Mode
        df['is_late'] = df['Delivery Status'].str.contains('Late', na=False).astype(int)
        ship_data = (df.groupby('Shipping Mode')['is_late'].mean() * 100).round(1)
        
        # Orders by month
        df['order_date'] = pd.to_datetime(df['order date (DateOrders)'], errors='coerce')
        df['month'] = df['order_date'].dt.to_period('M').astype(str)
        monthly = (df.groupby('month').size().sort_index().tail(24))
        
        # Revenue trend
        rev_trend = (df.groupby('month')['Sales'].sum().sort_index().tail(24))
        
        # Order status distribution
        status_data = (df['Delivery Status'].value_counts().head(6))
        
        # Risk level distribution
        risk_data = (df['Risk_Level'].value_counts())
        
        result = {
            'no_data': False,
            'revenue_by_region': {
                'labels': list(region_data.index),
                'values': [round(v, 2) for v in region_data.values]
            },
            'revenue_by_category': {
                'labels': list(cat_data.index),
                'values': [round(v, 2) for v in cat_data.values]
            },
            'late_rate_by_shipping': {
                'labels': list(ship_data.index),
                'values': list(ship_data.values)
            },
            'orders_by_month': {
                'labels': list(monthly.index),
                'values': list(monthly.values)
            },
            'revenue_trend': {
                'labels': list(rev_trend.index),
                'values': [round(v, 2) for v in rev_trend.values]
            },
            'order_status_dist': {
                'labels': list(status_data.index),
                'values': list(status_data.values)
            },
            'risk_distribution': {
                'labels': list(risk_data.index),
                'values': list(risk_data.values)
            }
        }
        return jsonify(safe_json(result))
        
    except Exception as e:
        import traceback
        print(f'[FAIL] eda_charts: {e}')
        print(traceback.format_exc())
        return jsonify({'no_data': True, 'error': str(e)})

@main.route('/api/forecast/charts')
@require_auth
def forecast_charts():
    """Forecast charts data for Chart.js"""
    try:
        processed_dir = os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed')
        forecast_file = os.path.join(processed_dir, 'demand_forecast_results.csv')
        
        if not os.path.exists(forecast_file):
            return jsonify({"no_data": True})
        
        df = pd.read_csv(forecast_file, encoding='latin-1', low_memory=False)
        
        # Summary by category
        summary = {"labels": [], "totals": []}
        if 'Category' in df.columns and 'Predicted_Sales' in df.columns:
            cat_totals = df.groupby('Category')['Predicted_Sales'].sum().head(10)
            summary = {
                "labels": cat_totals.index.tolist(),
                "totals": [round(val, 2) for val in cat_totals.values]
            }
        
        # Individual category forecasts
        categories = df['Category'].unique()[:5] if 'Category' in df.columns else []
        forecasts = {}
        
        for cat in categories:
            cat_data = df[df['Category'] == cat].head(30)
            if len(cat_data) > 0:
                forecasts[cat] = {
                    "dates": cat_data.get('Date', cat_data.index).astype(str).tolist(),
                    "predicted": [round(val, 2) for val in pd.to_numeric(cat_data.get('Predicted_Sales', []), errors='coerce').fillna(0)],
                    "lower": [round(val, 2) for val in pd.to_numeric(cat_data.get('Lower_Bound', []), errors='coerce').fillna(0)],
                    "upper": [round(val, 2) for val in pd.to_numeric(cat_data.get('Upper_Bound', []), errors='coerce').fillna(0)]
                }
        
        result = {
            "categories": categories.tolist(),
            "forecasts": forecasts,
            "summary": summary
        }
        return jsonify(safe_json(result))
        
    except Exception as e:
        print(f"Forecast charts error: {e}")
        return jsonify({"no_data": True})

@main.route('/api/customers/charts')
@require_auth
def customers_charts():
    """Customer charts data for Chart.js"""
    try:
        processed_dir = os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed')
        segments_file = os.path.join(processed_dir, 'customer_segments.csv')
        
        if not os.path.exists(segments_file):
            return jsonify({"no_data": True})
        
        df = pd.read_csv(segments_file, encoding='latin-1', low_memory=False)
        
        # Segment distribution
        segment_distribution = {"labels": [], "values": []}
        if 'Segment' in df.columns:
            seg_counts = df['Segment'].value_counts().head(10)
            segment_distribution = {
                "labels": seg_counts.index.tolist(),
                "values": seg_counts.values.tolist()
            }
        
        # Segment revenue
        segment_revenue = {"labels": [], "values": []}
        if 'Segment' in df.columns and 'Total_Sales' in df.columns:
            seg_revenue = df.groupby('Segment')['Total_Sales'].sum().head(10)
            segment_revenue = {
                "labels": seg_revenue.index.tolist(),
                "values": [round(val, 2) for val in seg_revenue.values]
            }
        
        # Cluster sizes (if cluster column exists)
        cluster_sizes = {"labels": [], "values": []}
        if 'Cluster' in df.columns:
            cluster_counts = df['Cluster'].value_counts().head(10)
            cluster_sizes = {
                "labels": [f"Cluster {i}" for i in cluster_counts.index],
                "values": cluster_counts.values.tolist()
            }
        
        # Recency distribution
        recency_distribution = {"labels": [], "values": []}
        if 'Recency' in df.columns:
            # Create recency bins
            df['Recency_Bin'] = pd.cut(pd.to_numeric(df['Recency'], errors='coerce'), 
                                     bins=[0, 30, 60, 90, 180, 365, float('inf')], 
                                     labels=['0-30', '31-60', '61-90', '91-180', '181-365', '365+'])
            recency_counts = df['Recency_Bin'].value_counts()
            recency_distribution = {
                "labels": recency_counts.index.astype(str).tolist(),
                "values": recency_counts.values.tolist()
            }
        
        result = {
            "segment_distribution": segment_distribution,
            "segment_revenue": segment_revenue,
            "cluster_sizes": cluster_sizes,
            "recency_distribution": recency_distribution
        }
        return jsonify(safe_json(result))
        
    except Exception as e:
        print(f"Customer charts error: {e}")
        return jsonify({"no_data": True})

@main.route('/api/nlp/charts')
@require_auth
def nlp_charts():
    """NLP charts data for Chart.js"""
    try:
        processed_dir = os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed')
        nlp_file = os.path.join(processed_dir, 'product_nlp_analysis.csv')
        
        if not os.path.exists(nlp_file):
            return jsonify({"no_data": True})
        
        df = pd.read_csv(nlp_file, encoding='latin-1', low_memory=False)
        
        # Top products/keywords
        top_keywords = {"labels": [], "values": []}
        if 'Product_Name' in df.columns and 'Frequency' in df.columns:
            top_products = df.nlargest(15, 'Frequency')
            top_keywords = {
                "labels": top_products['Product_Name'].tolist(),
                "values": top_products['Frequency'].tolist()
            }
        
        # Mock topic distribution (since we don't have real topic modeling)
        topic_distribution = {
            "labels": ["Sports Equipment", "Outdoor Gear", "Footwear", "Accessories", "Apparel"],
            "values": [35, 28, 22, 15, 10]
        }
        
        # Mock bigrams
        top_bigrams = {
            "labels": ["fishing rod", "soccer ball", "running shoes", "camping gear", "sports wear"],
            "values": [450, 380, 320, 280, 220]
        }
        
        # Mock sentiment
        sentiment_distribution = {
            "labels": ["Positive", "Neutral", "Negative"],
            "values": [65, 25, 10]
        }
        
        result = {
            "topic_distribution": topic_distribution,
            "top_bigrams": top_bigrams,
            "sentiment_distribution": sentiment_distribution,
            "top_keywords": top_keywords
        }
        return jsonify(safe_json(result))
        
    except Exception as e:
        print(f"NLP charts error: {e}")
        return jsonify({"no_data": True})

@main.route('/api/risk/charts')
@require_auth
def risk_charts():
    """Risk charts data for Chart.js"""
    try:
        processed_dir = os.path.join(current_app.config['PROJECT_ROOT'], 'data', 'processed')
        risk_file = os.path.join(processed_dir, 'delivery_risk_scored.csv')
        
        if not os.path.exists(risk_file):
            return jsonify({"no_data": True})
        
        df = pd.read_csv(risk_file, encoding='latin-1')
        
        # Risk distribution
        risk_distribution = {"labels": [], "values": []}
        if 'Risk_Level' in df.columns:
            risk_counts = df['Risk_Level'].value_counts()
            total = risk_counts.sum()
            risk_distribution = {
                "labels": risk_counts.index.tolist(),
                "values": [round((count/total)*100, 1) for count in risk_counts.values]
            }
        
        # Risk by region
        risk_by_region = {"labels": [], "high": [], "medium": [], "low": []}
        if 'Order Region' in df.columns and 'Risk_Level' in df.columns:
            regions = df['Order Region'].unique()[:8]
            for region in regions:
                region_data = df[df['Order Region'] == region]
                risk_counts = region_data['Risk_Level'].value_counts()
                total = len(region_data)
                
                risk_by_region["labels"].append(region)
                risk_by_region["high"].append(round((risk_counts.get('High Risk', 0)/total)*100, 1))
                risk_by_region["medium"].append(round((risk_counts.get('Medium Risk', 0)/total)*100, 1))
                risk_by_region["low"].append(round((risk_counts.get('Low Risk', 0)/total)*100, 1))
        
        # Risk by shipping mode
        risk_by_shipping = {"labels": [], "values": []}
        if 'Shipping Mode' in df.columns and 'Delivery Status' in df.columns:
            shipping_late = df.groupby('Shipping Mode').apply(
                lambda x: (x['Delivery Status'].str.contains('Late', na=False).sum() / len(x)) * 100
            ).head(8)
            risk_by_shipping = {
                "labels": shipping_late.index.tolist(),
                "values": [round(val, 1) for val in shipping_late.values]
            }
        
        # Risk trend over time
        risk_trend = {"labels": [], "values": []}
        if 'order date (DateOrders)' in df.columns and 'Delivery Status' in df.columns:
            df['order_date'] = pd.to_datetime(df['order date (DateOrders)'], errors='coerce')
            monthly_late = df.groupby(df['order_date'].dt.to_period('M')).apply(
                lambda x: (x['Delivery Status'].str.contains('Late', na=False).sum() / len(x)) * 100
            ).head(12)
            risk_trend = {
                "labels": [str(period) for period in monthly_late.index],
                "values": [round(val, 1) for val in monthly_late.values]
            }
        
        # Feature importance (mock data)
        feature_importance = {
            "labels": ["Shipping Mode", "Order Region", "Category", "Sales Amount", "Quantity"],
            "values": [0.28, 0.22, 0.18, 0.16, 0.12]
        }
        
        # Revenue at risk by category
        revenue_at_risk_by_category = {"labels": [], "values": []}
        if 'Category Name' in df.columns and 'Revenue_at_Risk' in df.columns:
            cat_risk = df.groupby('Category Name')['Revenue_at_Risk'].sum().head(10)
            revenue_at_risk_by_category = {
                "labels": cat_risk.index.tolist(),
                "values": [round(val, 2) for val in cat_risk.values]
            }
        
        result = {
            "risk_distribution": risk_distribution,
            "risk_by_region": risk_by_region,
            "risk_by_shipping": risk_by_shipping,
            "risk_trend": risk_trend,
            "feature_importance": feature_importance,
            "revenue_at_risk_by_category": revenue_at_risk_by_category
        }
        return jsonify(safe_json(result))
        
    except Exception as e:
        print(f"Risk charts error: {e}")
        return jsonify({"no_data": True})