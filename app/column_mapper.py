import pandas as pd
import difflib
import re

# PART A: CHAINPULSE STANDARD SCHEMA
CORE_COLUMNS = {
    'order_id': {
        'standard_name': 'Order Id',
        'description': 'Unique order identifier',
        'required': True,
        'dtype': 'any',
        'aliases': ['order_id', 'orderid', 'order id', 'id', 'order_number',
                   'ordernumber', 'transaction_id']
    },
    'order_date': {
        'standard_name': 'order date (DateOrders)',
        'description': 'Date the order was placed',
        'required': True,
        'dtype': 'datetime',
        'aliases': ['order_date', 'orderdate', 'date', 'order date', 'transaction_date', 
                   'created_at', 'purchase_date']
    },
    'sales': {
        'standard_name': 'Sales',
        'description': 'Sales amount / revenue',
        'required': True,
        'dtype': 'numeric',
        'aliases': ['sales', 'revenue', 'amount', 'total', 'order_total', 'sale_amount', 
                   'price', 'order_value', 'gmv']
    },
    'customer_id': {
        'standard_name': 'Customer Id',
        'description': 'Unique customer identifier',
        'required': True,
        'dtype': 'any',
        'aliases': ['customer_id', 'customerid', 'customer id', 'client_id',
                   'user_id', 'buyer_id']
    },
    'delivery_status': {
        'standard_name': 'Delivery Status',
        'description': 'Order delivery status',
        'required': True,
        'dtype': 'categorical',
        'aliases': ['delivery_status', 'delivery status', 'status', 'order_status', 
                   'shipment_status', 'fulfillment_status']
    },
    'shipping_mode': {
        'standard_name': 'Shipping Mode',
        'description': 'Shipping method used',
        'required': False,
        'dtype': 'categorical',
        'aliases': ['shipping_mode', 'shipping mode', 'ship_mode', 'shipment_type',
                   'delivery_method', 'ship_method', 'shipping_type', 'ship_type',
                   'carrier', 'shipping_carrier', 'fulfillment_method', 'dispatch_mode',
                   'courier', 'courier_type', 'shipment_mode', 'mode_of_shipping']
    },
    'product_name': {
        'standard_name': 'Product Name',
        'description': 'Name of the product',
        'required': False,
        'dtype': 'text',
        'aliases': ['product_name', 'product name', 'product', 'item_name', 'item',
                   'sku_name', 'product_description']
    },
    'category': {
        'standard_name': 'Category Name',
        'description': 'Product category',
        'required': False,
        'dtype': 'categorical',
        'aliases': ['category', 'category_name', 'category name', 'dept',
                   'department', 'product_category', 'product_type']
    },
    'customer_segment': {
        'standard_name': 'Customer Segment',
        'description': 'Customer segment/type',
        'required': False,
        'dtype': 'categorical',
        'aliases': ['customer_segment', 'segment', 'customer_type', 'client_type',
                   'tier', 'customer_tier']
    },
    'region': {
        'standard_name': 'Order Region',
        'description': 'Geographic region',
        'required': False,
        'dtype': 'categorical',
        'aliases': ['region', 'order_region', 'order region', 'area', 'zone',
                   'geography', 'market', 'territory']
    }
}

def normalize_column_name(col_name):
    """Normalize column name for matching"""
    if pd.isna(col_name) or col_name is None:
        return ""
    
    # Convert to string and lowercase
    normalized = str(col_name).lower().strip()
    
    # Replace spaces and hyphens with underscores
    normalized = re.sub(r'[\s\-]+', '_', normalized)
    
    # Remove special characters except underscores
    normalized = re.sub(r'[^\w]', '', normalized)
    
    return normalized

def auto_detect_columns(df_columns):
    """
    Auto-detect column mappings from uploaded CSV columns
    
    Input: list of column names from uploaded CSV
    Output: dict of suggested mappings
    """
    result = {}
    used_columns = set()
    
    # Normalize uploaded columns
    normalized_uploaded = {col: normalize_column_name(col) for col in df_columns}
    
    # Process REQUIRED columns first
    required_keys = [key for key, info in CORE_COLUMNS.items() if info['required']]
    optional_keys = [key for key, info in CORE_COLUMNS.items() if not info['required']]
    
    # Process required columns first, then optional
    for core_key in required_keys + optional_keys:
        core_info = CORE_COLUMNS[core_key]
        best_match = None
        best_confidence = 0.0
        
        # Normalize aliases for this core column
        normalized_aliases = [normalize_column_name(alias) for alias in core_info['aliases']]
        
        # Check each uploaded column that hasn't been used yet
        for original_col, normalized_col in normalized_uploaded.items():
            if original_col in used_columns:
                continue  # Skip already used columns
                
            confidence = 0.0
            
            # Exact match with aliases
            if normalized_col in normalized_aliases:
                confidence = 1.0
            else:
                # Fuzzy matching with aliases
                for alias in normalized_aliases:
                    if alias and normalized_col:  # Ensure both are not empty
                        similarity = difflib.SequenceMatcher(None, normalized_col, alias).ratio()
                        confidence = max(confidence, similarity)
            
            # Update best match if this is better and above threshold
            if confidence > best_confidence and confidence >= 0.7:
                best_match = original_col
                best_confidence = confidence
        
        # Store result
        if best_match:
            used_columns.add(best_match)
            result[core_key] = {
                'suggested': best_match,
                'confidence': round(best_confidence, 2),
                'standard': core_info['standard_name'],
                'matched': True
            }
        else:
            result[core_key] = {
                'suggested': None,
                'confidence': 0.0,
                'standard': core_info['standard_name'],
                'matched': False
            }
    
    return result

def validate_mapping(mapping):
    """
    Validate that all required columns are mapped
    
    Input: mapping dict {core_key: user_column_name}
    Output: {valid: bool, missing: [list]}
    """
    missing = []
    
    for core_key, core_info in CORE_COLUMNS.items():
        if core_info['required']:
            if core_key not in mapping or mapping[core_key] is None or mapping[core_key] == '':
                missing.append({
                    'key': core_key,
                    'name': core_info['standard_name'],
                    'description': core_info['description']
                })
    
    return {
        'valid': len(missing) == 0,
        'missing': missing
    }

def apply_mapping(df, mapping):
    """
    Apply column mapping to DataFrame
    
    Input:
    - df: pandas DataFrame from uploaded CSV
    - mapping: dict of {core_key: user_column_name}
    
    Output: new DataFrame with columns renamed to ChainPulse standard names
    """
    # Create rename dictionary: {user_column: standard_name}
    rename_dict = {}
    
    for core_key, user_column in mapping.items():
        if user_column and user_column in df.columns:
            standard_name = CORE_COLUMNS[core_key]['standard_name']
            rename_dict[user_column] = standard_name
    
    # Create a copy of the dataframe
    result_df = df.copy()
    
    # Rename columns
    result_df = result_df.rename(columns=rename_dict)
    
    # Add missing optional columns as None
    for core_key, core_info in CORE_COLUMNS.items():
        standard_name = core_info['standard_name']
        if not core_info['required'] and standard_name not in result_df.columns:
            result_df[standard_name] = None
    
    return result_df

def get_mapping_summary(mapping):
    """
    Get a summary of the mapping for display
    
    Input: mapping dict from auto_detect_columns
    Output: formatted summary dict
    """
    summary = {
        'total_columns': len(CORE_COLUMNS),
        'matched': 0,
        'required_matched': 0,
        'required_total': 0,
        'confidence_avg': 0.0,
        'details': []
    }
    
    confidences = []
    
    for core_key, match_info in mapping.items():
        core_info = CORE_COLUMNS[core_key]
        
        if core_info['required']:
            summary['required_total'] += 1
            if match_info['matched']:
                summary['required_matched'] += 1
        
        if match_info['matched']:
            summary['matched'] += 1
            confidences.append(match_info['confidence'])
        
        summary['details'].append({
            'core_key': core_key,
            'standard_name': core_info['standard_name'],
            'description': core_info['description'],
            'required': core_info['required'],
            'suggested': match_info['suggested'],
            'confidence': match_info['confidence'],
            'matched': match_info['matched']
        })
    
    # Calculate average confidence
    if confidences:
        summary['confidence_avg'] = round(sum(confidences) / len(confidences), 2)
    
    return summary