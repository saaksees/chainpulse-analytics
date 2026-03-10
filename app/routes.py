# ChainPulse — routes.py
from flask import Blueprint, render_template, jsonify, request, current_app
from .auth import require_auth
import pandas as pd
import os
import json
from datetime import datetime

main = Blueprint('main', __name__)

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
        if os.path.exists('data/processed/delivery_risk_scored.csv'):
            risk_df = pd.read_csv('data/processed/delivery_risk_scored.csv')
            stats['total_orders'] = len(risk_df)
            stats['high_risk_orders'] = len(risk_df[risk_df.get('Risk_Level', '') == 'High Risk'])
            stats['total_revenue'] = risk_df.get('Sales', pd.Series()).sum()
        
        if os.path.exists('data/processed/customer_segments.csv'):
            customer_df = pd.read_csv('data/processed/customer_segments.csv')
            stats['customer_segments'] = customer_df.get('Segment', pd.Series()).nunique()
            
    except Exception as e:
        print(f"Error loading stats: {e}")
    
    return stats
def get_risk_analysis_data():
    """Load risk analysis data"""
    data = {'risk_summary': {}, 'risk_distribution': []}
    
    try:
        if os.path.exists('data/processed/delivery_risk_scored.csv'):
            df = pd.read_csv('data/processed/delivery_risk_scored.csv')
            
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
        if os.path.exists('data/processed/demand_forecast_results.csv'):
            df = pd.read_csv('data/processed/demand_forecast_results.csv')
            
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
        if os.path.exists('data/processed/customer_segments.csv'):
            df = pd.read_csv('data/processed/customer_segments.csv')
            
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
        if os.path.exists('data/processed/product_nlp_analysis.csv'):
            df = pd.read_csv('data/processed/product_nlp_analysis.csv')
            
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