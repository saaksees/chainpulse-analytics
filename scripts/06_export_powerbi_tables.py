import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
Minimal PowerBI Export - Windows Compatible
"""

import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=" * 60)
    print("POWERBI EXPORT")
    print("=" * 60)
    
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Create output directories
    powerbi_dir = os.path.join(project_root, 'data', 'powerbi')
    os.makedirs(powerbi_dir, exist_ok=True)
    
    # Load data
    data_file = os.path.join(project_root, 'data', 'raw', 'DataCoSupplyChainDataset.csv')
    
    if not os.path.exists(data_file):
        print('[FAIL] Data file not found')
        return
    
    try:
        df = pd.read_csv(data_file, encoding='latin-1')
        print(f'[OK] Loaded {len(df):,} rows')
        
        # Export basic tables
        if 'Sales' in df.columns:
            # Fact orders table
            fact_orders = df[['Order Id', 'Sales', 'Order Item Quantity']].head(1000)
            fact_orders.to_csv(os.path.join(powerbi_dir, 'fact_orders.csv'), index=False)
            print('[OK] Created fact_orders.csv')
        
        if 'Category Name' in df.columns:
            # Dim product table
            dim_product = df[['Product Name', 'Category Name']].drop_duplicates().head(500)
            dim_product.to_csv(os.path.join(powerbi_dir, 'dim_product.csv'), index=False)
            print('[OK] Created dim_product.csv')
        
        print('[OK] PowerBI export complete')
        
    except Exception as e:
        print(f'[FAIL] Error: {e}')

if __name__ == '__main__':
    main()
