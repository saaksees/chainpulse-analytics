#!/usr/bin/env python3
"""
Pipeline Fix Script - Diagnose and fix pipeline issues
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def test_import(package_name, import_name=None):
    """Test if a package can be imported"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False

def main():
    print("🔧 ChainPulse Pipeline Fix Tool")
    print("=" * 50)
    
    # Required packages
    packages = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("scikit-learn", "sklearn"),
        ("xgboost", "xgboost"),
        ("imbalanced-learn", "imblearn"),
        ("prophet", "prophet"),
        ("joblib", "joblib"),
        ("nltk", "nltk"),
        ("wordcloud", "wordcloud"),
        ("squarify", "squarify"),
        ("flask", "flask"),
        ("reportlab", "reportlab")
    ]
    
    print("\n📦 Checking required packages...")
    
    missing_packages = []
    for package, import_name in packages:
        if test_import(import_name):
            print(f"✅ {package}")
        else:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🚨 Found {len(missing_packages)} missing packages")
        print("Installing missing packages...")
        
        for package in missing_packages:
            print(f"\n📥 Installing {package}...")
            if install_package(package):
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}")
    else:
        print("\n✅ All packages are installed!")
    
    # Test data file
    print("\n📁 Checking data files...")
    data_file = os.path.join("data", "raw", "DataCoSupplyChainDataset.csv")
    if os.path.exists(data_file):
        print(f"✅ Data file exists: {data_file}")
    else:
        print(f"❌ Data file missing: {data_file}")
    
    # Test script files
    print("\n📜 Checking script files...")
    scripts = [
        "01_eda.py",
        "02_demand_forecasting.py", 
        "03_delivery_risk_model.py",
        "04_rfm_segmentation.py",
        "05_nlp_analysis.py",
        "06_export_powerbi_tables.py"
    ]
    
    for script in scripts:
        script_path = os.path.join("scripts", script)
        if os.path.exists(script_path):
            print(f"✅ {script}")
        else:
            print(f"❌ {script} - MISSING")
    
    # Create output directories
    print("\n📂 Creating output directories...")
    directories = [
        "visuals/eda",
        "visuals/forecasting", 
        "visuals/risk_model",
        "visuals/rfm",
        "visuals/nlp",
        "data/processed",
        "data/powerbi",
        "models"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}")
    
    print("\n🎯 Testing simple script execution...")
    
    # Test simple Python execution
    test_script = """
import pandas as pd
import numpy as np
import os

print("✅ Basic imports work")

# Test data loading
data_path = os.path.join("data", "raw", "DataCoSupplyChainDataset.csv")
if os.path.exists(data_path):
    df = pd.read_csv(data_path, encoding='latin-1', nrows=10)
    print(f"✅ Data loaded: {df.shape}")
else:
    print("❌ Data file not found")
"""
    
    try:
        exec(test_script)
        print("✅ Script execution test passed")
    except Exception as e:
        print(f"❌ Script execution failed: {e}")
    
    print("\n" + "=" * 50)
    print("🚀 Fix complete! Try running the pipeline again.")
    print("   Go to: http://localhost:5000/pipeline-status")
    print("=" * 50)

if __name__ == "__main__":
    main()