import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
# Add scripts directory to path
# so column_detector can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

"""
Minimal EDA - Windows Compatible
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
        print('[FAIL] Data file not found')
        return
    
    try:
        df = pd.read_csv(data_file, encoding='latin-1')
        print(f'[OK] Loaded {len(df):,} rows, {len(df.columns)} columns')
        
        # Basic stats
        if 'Sales' in df.columns:
            total_sales = df['Sales'].sum()
            print(f'[MONEY] Total Sales: ${total_sales:,.2f}')
        
        if 'Delivery Status' in df.columns:
            late_rate = (df['Delivery Status'] == 'Late delivery').mean() * 100
            print(f'[TRUCK] Late Delivery Rate: {late_rate:.1f}%')
        
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
            print('[OK] Created: top_categories.png')
        
        print('[OK] EDA Complete')
        
    except Exception as e:
        print(f'[FAIL] Error: {e}')

if __name__ == '__main__':
    main()
