#!/usr/bin/env python3
"""
Dynamic Column Detection for Supply Chain Analytics
Detects column names in any supply chain CSV using fuzzy matching
"""

import difflib
import pandas as pd

def detect_columns(df):
    """
    Detect column names in any supply chain CSV
    Returns dict with detected column names or None if not found
    """
    
    # Column aliases for fuzzy matching
    aliases = {
        'date': [
            'order date (dateorders)', 'order date', 'date', 'orderdate',
            'transaction_date', 'order_date', 'created_at', 'ship date',
            'shipping date (dateorders)', 'shipping date', 'order_time',
            'purchase_date', 'sale_date', 'invoice_date'
        ],
        'sales': [
            'sales', 'revenue', 'amount', 'order item total', 'total',
            'sales per customer', 'gmv', 'order item cardprod total',
            'order_total', 'net_sales', 'gross_sales', 'order_amount',
            'transaction_amount', 'invoice_amount', 'line_total'
        ],
        'delivery_status': [
            'delivery status', 'delivery_status', 'status', 'order_status',
            'fulfillment_status', 'shipment_status', 'order status'
        ],
        'shipping_mode': [
            'shipping mode', 'shipping_mode', 'ship mode', 'ship_mode',
            'delivery method', 'shipment_mode', 'carrier', 'shipping_method'
        ],
        'region': [
            'order region', 'order_region', 'region', 'area', 'market',
            'territory', 'geography', 'zone', 'state', 'country',
            'customer_region', 'ship_region'
        ],
        'category': [
            'category name', 'category_name', 'category', 'department',
            'product_category', 'department name', 'product_type',
            'item_category', 'product_group'
        ],
        'customer_id': [
            'customer id', 'customer_id', 'customerid', 'order customer id',
            'client_id', 'user_id', 'cust_id', 'customer_number'
        ],
        'product_name': [
            'product name', 'product_name', 'product', 'item name',
            'item_name', 'product_description', 'item', 'sku_name'
        ],
        'quantity': [
            'order item quantity', 'quantity', 'qty', 'units',
            'item_quantity', 'order_qty', 'units_sold', 'pieces'
        ],
        'discount_rate': [
            'order item discount rate', 'discount rate', 'discount_rate',
            'discount', 'discount_pct', 'discount_percent', 'rebate'
        ],
        'profit_ratio': [
            'order item profit ratio', 'profit ratio', 'profit_ratio',
            'margin', 'gross_margin', 'profit_margin', 'margin_pct'
        ],
        'profit': [
            'order profit per order', 'profit', 'order_profit',
            'net_profit', 'benefit per order', 'gross_profit', 'margin_amount'
        ],
        'late_flag': [
            'late_delivery_risk', 'late delivery risk', 'is_late',
            'late', 'delayed', 'late_flag', 'delivery_delay'
        ],
        'scheduled_days': [
            'days for shipment (scheduled)', 'scheduled_days', 'sla_days',
            'delivery days', 'promised_days', 'expected_days', 'lead_time'
        ],
        'actual_days': [
            'days for shipping (real)', 'actual_days', 'real_days',
            'shipping_days', 'delivery_time', 'actual_delivery_days'
        ]
    }
    
    # Get all column names (lowercase for matching)
    columns = df.columns.tolist()
    columns_lower = [col.lower().strip() for col in columns]
    
    detected = {}
    
    for key, alias_list in aliases.items():
        detected_col = None
        
        # Step 1: Exact match (case insensitive)
        for alias in alias_list:
            alias_lower = alias.lower().strip()
            if alias_lower in columns_lower:
                idx = columns_lower.index(alias_lower)
                detected_col = columns[idx]
                break
        
        # Step 2: Contains match
        if not detected_col:
            for alias in alias_list:
                alias_lower = alias.lower().strip()
                for i, col_lower in enumerate(columns_lower):
                    if alias_lower in col_lower or col_lower in alias_lower:
                        detected_col = columns[i]
                        break
                if detected_col:
                    break
        
        # Step 3: Fuzzy match (threshold 0.6)
        if not detected_col:
            best_match = None
            best_ratio = 0.6  # Minimum threshold
            
            for alias in alias_list:
                alias_lower = alias.lower().strip()
                for i, col_lower in enumerate(columns_lower):
                    ratio = difflib.SequenceMatcher(None, alias_lower, col_lower).ratio()
                    if ratio > best_ratio:
                        best_ratio = ratio
                        best_match = columns[i]
            
            if best_match:
                detected_col = best_match
        
        detected[key] = detected_col
    
    return detected

def print_detection_summary(detected_cols, df):
    """Print a summary of detected columns"""
    print("\n" + "="*60)
    print("COLUMN DETECTION SUMMARY")
    print("="*60)
    
    found_count = sum(1 for col in detected_cols.values() if col is not None)
    total_count = len(detected_cols)
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns detected: {found_count}/{total_count}")
    print()
    
    for key, col_name in detected_cols.items():
        status = "✅" if col_name else "❌"
        display_name = col_name if col_name else "Not found"
        print(f"{status} {key:15} → {display_name}")
    
    print("="*60)
    
    return found_count, total_count

def get_first_csv_file(data_dir):
    """Get the first CSV file in the data directory"""
    import os
    
    if not os.path.exists(data_dir):
        return None
    
    csv_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.csv')]
    
    if not csv_files:
        return None
    
    # Prefer DataCo file if it exists
    for f in csv_files:
        if 'dataco' in f.lower() or 'supply' in f.lower():
            return os.path.join(data_dir, f)
    
    # Otherwise return first CSV
    return os.path.join(data_dir, csv_files[0])

def load_dataset_with_encoding(file_path):
    """Load CSV with automatic encoding detection"""
    encodings = ['latin-1', 'utf-8', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            print(f"✅ Loaded with {encoding} encoding")
            return df
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            print(f"❌ Error with {encoding}: {e}")
            continue
    
    raise ValueError(f"Could not load {file_path} with any encoding")

# Test function
if __name__ == "__main__":
    import os
    
    # Test with DataCo dataset
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = get_first_csv_file(os.path.join(project_root, 'data', 'raw'))
    
    if data_file:
        print(f"Testing with: {os.path.basename(data_file)}")
        df = load_dataset_with_encoding(data_file)
        detected = detect_columns(df)
        print_detection_summary(detected, df)
    else:
        print("No CSV file found in data/raw/")