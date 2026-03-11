import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import os
# Add scripts directory to path
# so column_detector can be found
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

"""
Minimal NLP - Windows Compatible
"""

import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

def main():
    print("=" * 60)
    print("NLP ANALYSIS")
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
        
        # Simple NLP analysis
        if 'Product Name' in df.columns:
            product_analysis = df['Product Name'].value_counts().head(20).reset_index()
            product_analysis.columns = ['Product_Name', 'Frequency']
            product_analysis.to_csv(os.path.join(project_root, 'data', 'processed', 'product_nlp_analysis.csv'), index=False)
            print('[OK] Created NLP analysis')
        else:
            print('[WARN] No Product Name column found')
        
    except Exception as e:
        print(f'[FAIL] Error: {e}')

if __name__ == '__main__':
    main()
