#!/usr/bin/env python3
"""
Fix data loading issues in all scripts
"""

import os
import pandas as pd

def check_data_file():
    """Check if data file exists and is readable"""
    print("Checking data file...")
    
    data_file = 'data/raw/DataCoSupplyChainDataset.csv'
    
    if not os.path.exists(data_file):
        print(f"ERROR: Data file missing: {data_file}")
        
        # Check for any CSV files
        data_dir = 'data/raw'
        if os.path.exists(data_dir):
            csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
            print(f"Available CSV files: {csv_files}")
            
            if csv_files:
                # Use the first CSV file
                source_file = os.path.join(data_dir, csv_files[0])
                print(f"Using {csv_files[0]} as data source")
                
                # Copy to expected name
                import shutil
                shutil.copy2(source_file, data_file)
                print(f"Copied to {data_file}")
            else:
                print("No CSV files found!")
                return False
        else:
            print(f"Data directory {data_dir} does not exist!")
            return False
    
    # Test loading
    try:
        df = pd.read_csv(data_file, encoding='latin-1')
        print(f"SUCCESS: Data loaded - {len(df):,} rows, {len(df.columns)} columns")
        
        # Show sample columns
        print(f"Sample columns: {list(df.columns)[:5]}...")
        
        # Check for key columns
        key_columns = ['Sales', 'order date (DateOrders)', 'Delivery Status', 'Category Name']
        found_columns = [col for col in key_columns if col in df.columns]
        print(f"Key columns found: {found_columns}")
        
        return True
        
    except Exception as e:
        print(f"ERROR loading data: {e}")
        return False

def fix_column_detector():
    """Ensure column detector works properly"""
    print("\nTesting column detector...")
    
    try:
        import sys
        sys.path.append('scripts')
        
        from column_detector import detect_columns, get_first_csv_file, load_dataset_with_encoding
        
        # Test with actual data
        data_dir = 'data/raw'
        data_file = get_first_csv_file(data_dir)
        
        if data_file:
            print(f"Found data file: {os.path.basename(data_file)}")
            
            df = load_dataset_with_encoding(data_file)
            print(f"Loaded: {df.shape}")
            
            cols = detect_columns(df)
            detected_count = sum(1 for v in cols.values() if v is not None)
            print(f"Detected {detected_count}/{len(cols)} columns")
            
            # Show detected columns
            for key, col_name in cols.items():
                if col_name:
                    print(f"  {key}: {col_name}")
            
            return True
        else:
            print("No data file found by column detector")
            return False
            
    except Exception as e:
        print(f"Column detector error: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_minimal_working_scripts():
    """Create minimal versions that definitely work"""
    print("\nCreating minimal working scripts...")
    
    # Minimal EDA script
    minimal_eda = '''"""
Minimal EDA Script - Windows Compatible
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=" * 60)
    print("SUPPLY CHAIN EDA")
    print("=" * 60)
    
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Create output directories
    os.makedirs(os.path.join(project_root, 'visuals', 'eda'), exist_ok=True)
    os.makedirs(os.path.join(project_root, 'data', 'processed'), exist_ok=True)
    
    # Load data
    data_file = os.path.join(project_root, 'data', 'raw', 'DataCoSupplyChainDataset.csv')
    
    if not os.path.exists(data_file):
        print('ERROR: Data file not found')
        return
    
    try:
        df = pd.read_csv(data_file, encoding='latin-1')
        print(f'Loaded {len(df):,} rows, {len(df.columns)} columns')
        
        # Basic stats
        if 'Sales' in df.columns:
            total_sales = df['Sales'].sum()
            print(f'Total Sales: ${total_sales:,.2f}')
        
        if 'Delivery Status' in df.columns:
            late_rate = (df['Delivery Status'] == 'Late delivery').mean() * 100
            print(f'Late Delivery Rate: {late_rate:.1f}%')
        
        # Create simple visualization
        if 'Category Name' in df.columns and 'Sales' in df.columns:
            top_categories = df.groupby('Category Name')['Sales'].sum().sort_values(ascending=False).head(10)
            
            plt.figure(figsize=(12, 6))
            top_categories.plot(kind='bar')
            plt.title('Top 10 Categories by Sales')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(project_root, 'visuals', 'eda', 'top_categories.png'))
            plt.close()
            print('Created: top_categories.png')
        
        print('EDA Complete')
        
    except Exception as e:
        print(f'ERROR: {e}')

if __name__ == '__main__':
    main()
'''
    
    # Write minimal EDA
    with open('scripts/01_eda_minimal.py', 'w', encoding='utf-8') as f:
        f.write(minimal_eda)
    
    print("Created minimal working scripts")

def main():
    print("Fixing Data Loading Issues")
    print("=" * 50)
    
    data_ok = check_data_file()
    detector_ok = fix_column_detector()
    
    if not data_ok or not detector_ok:
        create_minimal_working_scripts()
    
    print("\n" + "=" * 50)
    print("Data loading fixes complete")
    
    if data_ok and detector_ok:
        print("SUCCESS: Data and column detection working")
    else:
        print("WARNING: Created fallback scripts")

if __name__ == "__main__":
    main()