import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
Minimal RFM - Windows Compatible
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=" * 60)
    print("RFM SEGMENTATION")
    print("=" * 60)
    
    # Get project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Create output directories
    os.makedirs(os.path.join(project_root, 'data', 'processed'), exist_ok=True)
    
    # Load data
    data_file = os.path.join(project_root, 'data', 'raw', 'DataCoSupplyChainDataset.csv')
    
    if not os.path.exists(data_file):
        print('[FAIL] Data file not found')
        return
    
    try:
        df = pd.read_csv(data_file, encoding='latin-1')
        print(f'[OK] Loaded {len(df):,} rows')
        
        # Simple segmentation based on sales
        if 'Sales' in df.columns and 'Customer Id' in df.columns:
            customer_sales = df.groupby('Customer Id')['Sales'].agg(['sum', 'count']).reset_index()
            customer_sales.columns = ['Customer_ID', 'Total_Sales', 'Order_Count']
            
            # Simple segmentation
            customer_sales['Segment'] = 'Regular'
            customer_sales.loc[customer_sales['Total_Sales'] > customer_sales['Total_Sales'].quantile(0.8), 'Segment'] = 'VIP'
            customer_sales.loc[customer_sales['Total_Sales'] < customer_sales['Total_Sales'].quantile(0.2), 'Segment'] = 'Low Value'
            
            customer_sales.to_csv(os.path.join(project_root, 'data', 'processed', 'customer_segments.csv'), index=False)
            print('[OK] Created customer segments')
        else:
            print('[WARN] Missing required columns for RFM')
        
    except Exception as e:
        print(f'[FAIL] Error: {e}')

if __name__ == '__main__':
    main()
