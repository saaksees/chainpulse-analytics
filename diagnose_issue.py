#!/usr/bin/env python3
"""
Diagnose pipeline issues
"""

import os
import sys
import pandas as pd

def check_environment():
    """Check Python environment"""
    print("🔍 ENVIRONMENT CHECK")
    print("=" * 40)
    
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}...")
    
    # Check key imports
    imports_to_check = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 
        'sklearn', 'joblib', 'prophet'
    ]
    
    print(f"\n📦 PACKAGE CHECK")
    print("=" * 40)
    
    for pkg in imports_to_check:
        try:
            __import__(pkg)
            print(f"✅ {pkg}")
        except ImportError as e:
            print(f"❌ {pkg}: {e}")

def check_files():
    """Check file structure"""
    print(f"\n📁 FILE STRUCTURE CHECK")
    print("=" * 40)
    
    required_files = [
        'data/raw/DataCoSupplyChainDataset.csv',
        'scripts/column_detector.py',
        'scripts/01_eda.py',
        'scripts/02_demand_forecasting.py', 
        'scripts/03_delivery_risk_model.py',
        'scripts/04_rfm_segmentation.py',
        'scripts/05_nlp_analysis.py',
        'scripts/06_export_powerbi_tables.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")

def check_data():
    """Check data file"""
    print(f"\n📊 DATA CHECK")
    print("=" * 40)
    
    data_file = 'data/raw/DataCoSupplyChainDataset.csv'
    
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return
    
    try:
        df = pd.read_csv(data_file, encoding='latin-1', nrows=5)
        print(f"✅ Data file loaded successfully")
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)[:5]}...")
    except Exception as e:
        print(f"❌ Error loading data: {e}")

def test_column_detector():
    """Test column detector import"""
    print(f"\n🔧 COLUMN DETECTOR TEST")
    print("=" * 40)
    
    try:
        # Add scripts to path
        scripts_dir = os.path.join(os.getcwd(), 'scripts')
        if scripts_dir not in sys.path:
            sys.path.append(scripts_dir)
        
        from column_detector import detect_columns, get_first_csv_file
        print("✅ Column detector imported successfully")
        
        # Test with data
        data_dir = 'data/raw'
        data_file = get_first_csv_file(data_dir)
        
        if data_file:
            print(f"✅ Found data file: {os.path.basename(data_file)}")
            
            df = pd.read_csv(data_file, encoding='latin-1', nrows=10)
            cols = detect_columns(df)
            
            detected_count = sum(1 for v in cols.values() if v is not None)
            print(f"✅ Detected {detected_count}/{len(cols)} columns")
        else:
            print("❌ No data file found")
            
    except Exception as e:
        print(f"❌ Column detector error: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("🚀 CHAINPULSE PIPELINE DIAGNOSTICS")
    print("=" * 50)
    
    check_environment()
    check_files()
    check_data()
    test_column_detector()
    
    print(f"\n" + "=" * 50)
    print("DIAGNOSIS COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    main()