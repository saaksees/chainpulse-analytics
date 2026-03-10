import pandas as pd
import os
from datetime import datetime

# Semantic column matching - only require date + sales columns
REQUIRED_SEMANTIC = {
    'date': ['order date (dateorders)', 'order date', 'date', 'orderdate',
             'transaction_date', 'created_at', 'order_date', 'ship date',
             'shipping date (dateorders)', 'shipping date'],
    'sales': ['sales', 'revenue', 'amount', 'total', 'order total',
              'order item total', 'gmv', 'sales per customer',
              'order item cardprod total']
}

def check_required_columns(df):
    """Checks semantically not by exact name.
    Only needs: 1 date col + 1 sales col.
    Returns list of errors (empty = pass)."""
    errors = []
    cols_lower = [c.lower().strip() for c in df.columns]
    
    # Check date column exists
    date_found = any(alias in cols_lower for alias in REQUIRED_SEMANTIC['date'])
    if not date_found:
        # Try fuzzy — any col with 'date'
        date_found = any('date' in c for c in cols_lower)
    if not date_found:
        errors.append('No date column found. Need a column containing order or transaction dates.')
    
    # Check sales column exists
    sales_found = any(alias in cols_lower for alias in REQUIRED_SEMANTIC['sales'])
    if not sales_found:
        # Try fuzzy — any col with 'sale', 'revenue', 'amount'
        sales_found = any(any(kw in c for kw in ['sale', 'revenue', 'amount', 'total']) for c in cols_lower)
    if not sales_found:
        errors.append('No sales/revenue column found. Need a numeric column with order amounts.')
    
    return errors

def validate_csv(filepath):
    """Validate uploaded CSV file"""
    result = {
        'valid': False,
        'errors': [],
        'warnings': [],
        'info': {}
    }
    
    try:
        # Try to read the file
        try:
            df = pd.read_csv(filepath, encoding='latin-1')
        except Exception as e:
            result['errors'].append(f"Cannot read CSV file: {str(e)}")
            return result
        
        # Basic info
        result['info']['rows'] = len(df)
        result['info']['columns'] = len(df.columns)
        
        # Check minimum rows
        if len(df) < 1000:
            result['errors'].append(f"File has only {len(df)} rows. Minimum 1,000 required.")
        
        # Check required columns semantically
        col_errors = check_required_columns(df)
        if col_errors:
            result['errors'].extend(col_errors)
        
        # Find sales column for revenue calculation
        sales_col = None
        cols_lower = [c.lower().strip() for c in df.columns]
        for i, col_lower in enumerate(cols_lower):
            if any(alias in col_lower for alias in REQUIRED_SEMANTIC['sales']):
                sales_col = df.columns[i]
                break
        
        if sales_col:
            try:
                sales_numeric = pd.to_numeric(df[sales_col], errors='coerce')
                total_revenue = sales_numeric.sum()
                result['info']['total_revenue'] = f"${total_revenue/1000000:.1f}M"
            except:
                result['warnings'].append(f"Sales column '{sales_col}' contains non-numeric values")
                result['info']['total_revenue'] = "Unknown"
        else:
            result['info']['total_revenue'] = "Unknown"
        
        # Find date column for date range
        date_col = None
        for i, col_lower in enumerate(cols_lower):
            if any(alias in col_lower for alias in REQUIRED_SEMANTIC['date']):
                date_col = df.columns[i]
                break
        
        if date_col:
            try:
                dates = pd.to_datetime(df[date_col], errors='coerce')
                valid_dates = dates.dropna()
                if len(valid_dates) > 0:
                    min_date = valid_dates.min().strftime('%Y-%m-%d')
                    max_date = valid_dates.max().strftime('%Y-%m-%d')
                    result['info']['date_range'] = f"{min_date} to {max_date}"
                else:
                    result['warnings'].append(f"Date column '{date_col}' has no valid dates")
                    result['info']['date_range'] = "Unknown"
            except:
                result['warnings'].append(f"Date column '{date_col}' has invalid dates")
                result['info']['date_range'] = "Unknown"
        else:
            result['info']['date_range'] = "Unknown"
        
        # Check for delivery status or late delivery indicators (optional)
        delivery_indicators = ['delivery status', 'late_delivery_risk', 'delivery_risk', 'on_time']
        delivery_col = None
        for col in df.columns:
            if any(indicator in col.lower() for indicator in delivery_indicators):
                delivery_col = col
                break
        
        if delivery_col:
            try:
                if 'late' in delivery_col.lower() or 'risk' in delivery_col.lower():
                    # Binary risk column
                    late_rate = (df[delivery_col] == 1).mean() * 100
                else:
                    # Status column
                    late_rate = df[delivery_col].str.contains('Late', na=False).mean() * 100
                result['info']['late_rate'] = f"{late_rate:.1f}%"
            except:
                result['warnings'].append("Cannot calculate late delivery rate")
                result['info']['late_rate'] = "Unknown"
        else:
            result['info']['late_rate'] = "Unknown"
        
        # Check for excessive nulls
        for col in df.columns:
            null_pct = df[col].isnull().mean()
            if null_pct > 0.8:
                result['warnings'].append(f"Column '{col}' is {null_pct*100:.0f}% empty")
        
        # Final validation
        if not result['errors']:
            result['valid'] = True
        
        return result
        
    except Exception as e:
        result['errors'].append(f"Validation failed: {str(e)}")
        return result