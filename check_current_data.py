#!/usr/bin/env python3
"""
Check what data is currently being displayed on the dashboard
"""

import pandas as pd
import os
from datetime import datetime

def check_dashboard_data():
    """Check the current data behind the dashboard"""
    
    print("🔍 CHECKING CURRENT DASHBOARD DATA")
    print("=" * 50)
    
    # Check raw data
    raw_file = 'data/raw/DataCoSupplyChainDataset.csv'
    if os.path.exists(raw_file):
        df_raw = pd.read_csv(raw_file, encoding='latin-1')
        print(f"\n📊 RAW DATA:")
        print(f"   Rows: {len(df_raw):,}")
        print(f"   Columns: {len(df_raw.columns)}")
        
        if 'Sales' in df_raw.columns:
            total_revenue = df_raw['Sales'].sum()
            print(f"   Total Revenue: ${total_revenue:,.0f}")
        
        if 'Delivery Status' in df_raw.columns:
            late_rate = (df_raw['Delivery Status'] == 'Late delivery').mean() * 100
            print(f"   Late Delivery Rate: {late_rate:.1f}%")
        
        if 'Customer Id' in df_raw.columns:
            unique_customers = df_raw['Customer Id'].nunique()
            print(f"   Unique Customers: {unique_customers:,}")
    else:
        print("❌ No raw data file found")
    
    # Check processed files
    processed_files = [
        'data/processed/delivery_risk_scored.csv',
        'data/processed/customer_segments.csv',
        'data/processed/demand_forecast_results.csv'
    ]
    
    print(f"\n📁 PROCESSED FILES:")
    for file_path in processed_files:
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                file_size = os.path.getsize(file_path)
                mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                
                print(f"   ✅ {os.path.basename(file_path)}")
                print(f"      Rows: {len(df):,}")
                print(f"      Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"      Size: {file_size:,} bytes")
                
                # Show sample data
                if 'Sales' in df.columns:
                    total_sales = df['Sales'].sum()
                    print(f"      Total Sales: ${total_sales:,.0f}")
                
                if 'Risk_Level' in df.columns:
                    risk_counts = df['Risk_Level'].value_counts()
                    print(f"      Risk Distribution: {dict(risk_counts)}")
                
            except Exception as e:
                print(f"   ❌ {os.path.basename(file_path)}: Error reading - {e}")
        else:
            print(f"   ❌ {os.path.basename(file_path)}: Not found")
    
    # Check active dataset tracking
    active_dataset_file = 'data/active_dataset.json'
    if os.path.exists(active_dataset_file):
        try:
            import json
            with open(active_dataset_file, 'r') as f:
                active_info = json.load(f)
            
            print(f"\n📋 ACTIVE DATASET INFO:")
            print(f"   Dataset: {active_info.get('dataset_name', 'Unknown')}")
            print(f"   Upload Date: {active_info.get('upload_date', 'Unknown')}")
            print(f"   Rows: {active_info.get('rows', 'Unknown'):,}")
            
        except Exception as e:
            print(f"\n❌ Error reading active dataset info: {e}")
    else:
        print(f"\n⚠️ No active dataset tracking file found")
    
    # Check version history
    print(f"\n📚 VERSION HISTORY:")
    try:
        from app.database import get_all_versions, get_active_version
        versions = get_all_versions()
        active = get_active_version()
        
        if versions:
            print(f"   Total versions: {len(versions)}")
            if active:
                print(f"   Active version: {active['version_number']} ({active['filename']})")
                print(f"   Active rows: {active['rows']:,}")
                print(f"   Active revenue: ${active['revenue']:,.0f}")
            
            print(f"   Recent versions:")
            for v in versions[:3]:  # Show last 3
                print(f"     v{v['version_number']}: {v['filename']} ({v['rows']:,} rows)")
        else:
            print(f"   No versions found")
            
    except Exception as e:
        print(f"   Error checking versions: {e}")
    
    print(f"\n" + "=" * 50)
    print("CONCLUSION:")
    
    # Determine if data matches dashboard
    dashboard_revenue = 3900000  # 3.9M from screenshot
    dashboard_orders = 15000     # 15K from screenshot
    dashboard_late_rate = 54.8   # 54.8% from screenshot
    
    if os.path.exists(raw_file):
        df_raw = pd.read_csv(raw_file, encoding='latin-1')
        actual_revenue = df_raw['Sales'].sum() if 'Sales' in df_raw.columns else 0
        actual_orders = len(df_raw)
        actual_late_rate = (df_raw['Delivery Status'] == 'Late delivery').mean() * 100 if 'Delivery Status' in df_raw.columns else 0
        
        revenue_match = abs(actual_revenue - dashboard_revenue) < 100000  # Within 100K
        orders_match = abs(actual_orders - dashboard_orders) < 1000      # Within 1K
        late_rate_match = abs(actual_late_rate - dashboard_late_rate) < 5  # Within 5%
        
        if revenue_match and orders_match and late_rate_match:
            print("✅ Dashboard numbers MATCH your current dataset")
        else:
            print("⚠️ Dashboard numbers may be from CACHED/OLD data")
            print(f"   Current vs Dashboard:")
            print(f"   Revenue: ${actual_revenue:,.0f} vs ${dashboard_revenue:,.0f}")
            print(f"   Orders: {actual_orders:,} vs {dashboard_orders:,}")
            print(f"   Late Rate: {actual_late_rate:.1f}% vs {dashboard_late_rate}%")

if __name__ == "__main__":
    check_dashboard_data()