#!/usr/bin/env python3
"""
Fix pipeline issues immediately
"""

import os
import sys
import shutil

def fix_imports():
    """Fix import issues in all scripts"""
    print("🔧 Fixing import issues...")
    
    scripts_to_fix = [
        'scripts/01_eda.py',
        'scripts/02_demand_forecasting.py', 
        'scripts/04_rfm_segmentation.py',
        'scripts/05_nlp_analysis.py',
        'scripts/06_export_powerbi_tables.py'
    ]
    
    import_fix = '''import os
import sys

# Add scripts directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

try:
    from column_detector import detect_columns, get_first_csv_file, load_dataset_with_encoding, print_detection_summary
    HAS_COLUMN_DETECTOR = True
except ImportError:
    HAS_COLUMN_DETECTOR = False
    print("⚠️ Column detector not available - using fallback mode")
'''
    
    for script_path in scripts_to_fix:
        if os.path.exists(script_path):
            print(f"   Fixing {script_path}...")
            
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if already has the fix
            if 'HAS_COLUMN_DETECTOR' not in content:
                # Add import fix after the docstring
                lines = content.split('\n')
                
                # Find end of docstring
                in_docstring = False
                docstring_end = 0
                
                for i, line in enumerate(lines):
                    if '"""' in line:
                        if not in_docstring:
                            in_docstring = True
                        else:
                            docstring_end = i + 1
                            break
                
                # Insert import fix
                lines.insert(docstring_end, import_fix)
                
                # Write back
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                
                print(f"   ✅ Fixed {script_path}")

def create_fallback_scripts():
    """Create fallback versions of scripts that work without column detection"""
    print("🔧 Creating fallback scripts...")
    
    # Simple EDA fallback
    eda_fallback = '''"""
Simple EDA - Fallback version
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Create output directories
    os.makedirs(os.path.join(project_root, 'visuals', 'eda'), exist_ok=True)
    os.makedirs(os.path.join(project_root, 'data', 'processed'), exist_ok=True)
    
    print('='*60)
    print('SUPPLY CHAIN EDA - FALLBACK MODE')
    print('='*60)
    
    # Load data
    data_file = os.path.join(project_root, 'data', 'raw', 'DataCoSupplyChainDataset.csv')
    
    if not os.path.exists(data_file):
        print('❌ Data file not found')
        return
    
    try:
        df = pd.read_csv(data_file, encoding='latin-1')
        print(f'✅ Loaded {len(df):,} rows')
        
        # Basic analysis
        if 'Sales' in df.columns:
            total_sales = df['Sales'].sum()
            print(f'💰 Total Sales: ${total_sales:,.2f}')
        
        if 'Delivery Status' in df.columns:
            late_rate = (df['Delivery Status'] == 'Late delivery').mean() * 100
            print(f'📦 Late Delivery Rate: {late_rate:.1f}%')
        
        # Create simple chart
        if 'Category Name' in df.columns and 'Sales' in df.columns:
            top_categories = df.groupby('Category Name')['Sales'].sum().sort_values(ascending=False).head(10)
            
            plt.figure(figsize=(12, 6))
            top_categories.plot(kind='bar')
            plt.title('Top Categories by Sales')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(project_root, 'visuals', 'eda', 'top_categories.png'))
            plt.close()
            print('✅ Created top_categories.png')
        
        print('✅ EDA Complete')
        
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == '__main__':
    main()
'''
    
    # Write fallback EDA
    with open('scripts/01_eda_fallback.py', 'w') as f:
        f.write(eda_fallback)
    
    print("✅ Created fallback scripts")

def check_data_file():
    """Check if data file exists and is readable"""
    print("📊 Checking data file...")
    
    data_file = 'data/raw/DataCoSupplyChainDataset.csv'
    
    if not os.path.exists(data_file):
        print(f"❌ Data file missing: {data_file}")
        
        # Check if there's any CSV in the directory
        data_dir = 'data/raw'
        if os.path.exists(data_dir):
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            if csv_files:
                print(f"📁 Found CSV files: {csv_files}")
                # Copy first CSV to expected name
                first_csv = os.path.join(data_dir, csv_files[0])
                shutil.copy2(first_csv, data_file)
                print(f"✅ Copied {csv_files[0]} to DataCoSupplyChainDataset.csv")
            else:
                print("❌ No CSV files found in data/raw/")
        return False
    
    try:
        df = pd.read_csv(data_file, encoding='latin-1', nrows=5)
        print(f"✅ Data file readable: {df.shape}")
        return True
    except Exception as e:
        print(f"❌ Error reading data file: {e}")
        return False

def main():
    print("🚀 FIXING CHAINPULSE PIPELINE")
    print("=" * 50)
    
    # Import pandas here
    global pd
    import pandas as pd
    
    check_data_file()
    fix_imports()
    create_fallback_scripts()
    
    print("\n" + "=" * 50)
    print("✅ PIPELINE FIXES COMPLETE")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Try running: python run_app.py")
    print("2. Go to http://localhost:5000")
    print("3. Test the pipeline from the web interface")

if __name__ == "__main__":
    main()