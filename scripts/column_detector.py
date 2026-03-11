"""
Simple column detection for supply chain datasets
"""

import pandas as pd
import os
import glob

def get_first_csv_file(data_dir):
    """Find the first CSV file in the data directory"""
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))
    if csv_files:
        return csv_files[0]
    return None

def load_dataset_with_encoding(file_path):
    """Load CSV with proper encoding"""
    try:
        return pd.read_csv(file_path, encoding='latin-1')
    except:
        try:
            return pd.read_csv(file_path, encoding='utf-8')
        except:
            return pd.read_csv(file_path, encoding='latin-1', low_memory=False)

def detect_columns(df):
    """Detect key columns in the dataset"""
    columns = df.columns.tolist()
    
    detected = {
        'sales': None,
        'delivery_status': None,
        'shipping_mode': None,
        'region': None,
        'category': None,
        'order_date': None,
        'customer_id': None,
        'order_id': None
    }
    
    # Sales/Revenue column
    for col in columns:
        if any(term in col.lower() for term in ['sales', 'revenue', 'amount', 'profit']):
            detected['sales'] = col
            break
    
    # Delivery status
    for col in columns:
        if any(term in col.lower() for term in ['delivery', 'status', 'late']):
            detected['delivery_status'] = col
            break
    
    # Shipping mode
    for col in columns:
        if any(term in col.lower() for term in ['shipping', 'ship', 'mode']):
            detected['shipping_mode'] = col
            break
    
    # Region
    for col in columns:
        if any(term in col.lower() for term in ['region', 'state', 'country']):
            detected['region'] = col
            break
    
    # Category
    for col in columns:
        if any(term in col.lower() for term in ['category', 'product', 'item']):
            detected['category'] = col
            break
    
    # Date
    for col in columns:
        if any(term in col.lower() for term in ['date', 'time']):
            detected['order_date'] = col
            break
    
    # Customer ID
    for col in columns:
        if any(term in col.lower() for term in ['customer', 'client']):
            detected['customer_id'] = col
            break
    
    # Order ID
    for col in columns:
        if any(term in col.lower() for term in ['order', 'transaction', 'id']) and 'customer' not in col.lower():
            detected['order_id'] = col
            break
    
    return detected

def print_detection_summary(detected_cols, df=None):
    """Print summary of detected columns"""
    print("\n📊 COLUMN DETECTION SUMMARY")
    print("-" * 40)
    found_count = 0
    total_count = len(detected_cols)
    
    for key, col in detected_cols.items():
        if col:
            found_count += 1
        status = "✅" if col else "❌"
        print(f"{status} {key.replace('_', ' ').title()}: {col or 'Not found'}")
    print("-" * 40)
    
    return found_count, total_count