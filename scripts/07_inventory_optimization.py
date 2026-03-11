#!/usr/bin/env python3
"""
Inventory Optimization Analysis
Calculates optimal stock levels, reorder points, and safety stock
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

def calculate_inventory_metrics(df):
    """Calculate key inventory optimization metrics"""
    
    # Ensure required columns exist
    required_cols = ['Product Name', 'Category Name', 'Order Item Quantity', 'Sales', 'order date (DateOrders)']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Missing columns: {missing_cols}")
        return None
    
    # Convert date column
    df['order_date'] = pd.to_datetime(df['order date (DateOrders)'], errors='coerce')
    df = df.dropna(subset=['order_date'])
    
    # Calculate daily demand per product
    daily_demand = df.groupby(['Product Name', 'Category Name', df['order_date'].dt.date]).agg({
        'Order Item Quantity': 'sum',
        'Sales': 'sum'
    }).reset_index()
    
    # Calculate inventory metrics per product
    inventory_metrics = []
    
    for product in df['Product Name'].unique():
        product_data = daily_demand[daily_demand['Product Name'] == product]
        
        if len(product_data) < 7:  # Need at least 7 days of data
            continue
            
        category = product_data['Category Name'].iloc[0]
        
        # Basic demand statistics
        daily_qty = product_data['Order Item Quantity']
        avg_daily_demand = daily_qty.mean()
        demand_std = daily_qty.std()
        max_demand = daily_qty.max()
        
        # Lead time (assume 7-14 days based on category)
        lead_time_days = 10 if 'Fishing' in category else 7
        
        # Safety stock calculation (Z-score for 95% service level = 1.65)
        service_level_z = 1.65
        safety_stock = service_level_z * demand_std * np.sqrt(lead_time_days)
        
        # Reorder point
        reorder_point = (avg_daily_demand * lead_time_days) + safety_stock
        
        # Economic Order Quantity (EOQ) - simplified
        # Assume holding cost = 20% annually, ordering cost = $50
        annual_demand = avg_daily_demand * 365
        holding_cost_rate = 0.20
        ordering_cost = 50
        avg_unit_cost = product_data['Sales'].sum() / product_data['Order Item Quantity'].sum()
        
        if annual_demand > 0 and avg_unit_cost > 0:
            eoq = np.sqrt((2 * annual_demand * ordering_cost) / (holding_cost_rate * avg_unit_cost))
        else:
            eoq = avg_daily_demand * 30  # Default to 30 days supply
        
        # Stock turnover ratio
        total_sales = product_data['Sales'].sum()
        avg_inventory_value = eoq * avg_unit_cost
        turnover_ratio = total_sales / avg_inventory_value if avg_inventory_value > 0 else 0
        
        # Days of supply
        days_of_supply = eoq / avg_daily_demand if avg_daily_demand > 0 else 0
        
        # Stock status classification
        if turnover_ratio > 12:
            stock_status = "Fast Moving"
        elif turnover_ratio > 4:
            stock_status = "Medium Moving"
        else:
            stock_status = "Slow Moving"
        
        # Risk level based on demand variability
        cv = demand_std / avg_daily_demand if avg_daily_demand > 0 else 0
        if cv > 1.0:
            demand_risk = "High"
        elif cv > 0.5:
            demand_risk = "Medium"
        else:
            demand_risk = "Low"
        
        inventory_metrics.append({
            'Product_Name': product,
            'Category': category,
            'Avg_Daily_Demand': round(avg_daily_demand, 2),
            'Demand_Std': round(demand_std, 2),
            'Max_Daily_Demand': max_demand,
            'Lead_Time_Days': lead_time_days,
            'Safety_Stock': round(safety_stock, 0),
            'Reorder_Point': round(reorder_point, 0),
            'EOQ': round(eoq, 0),
            'Avg_Unit_Cost': round(avg_unit_cost, 2),
            'Turnover_Ratio': round(turnover_ratio, 2),
            'Days_of_Supply': round(days_of_supply, 1),
            'Stock_Status': stock_status,
            'Demand_Risk': demand_risk,
            'Total_Sales': round(total_sales, 2),
            'Data_Points': len(product_data)
        })
    
    return pd.DataFrame(inventory_metrics)

def generate_abc_analysis(inventory_df):
    """Generate ABC analysis based on sales value"""
    
    # Sort by total sales descending
    sorted_df = inventory_df.sort_values('Total_Sales', ascending=False).copy()
    
    # Calculate cumulative percentage
    sorted_df['Cumulative_Sales'] = sorted_df['Total_Sales'].cumsum()
    total_sales = sorted_df['Total_Sales'].sum()
    sorted_df['Cumulative_Percentage'] = (sorted_df['Cumulative_Sales'] / total_sales) * 100
    
    # Assign ABC categories
    def assign_abc_category(cum_pct):
        if cum_pct <= 80:
            return 'A'
        elif cum_pct <= 95:
            return 'B'
        else:
            return 'C'
    
    sorted_df['ABC_Category'] = sorted_df['Cumulative_Percentage'].apply(assign_abc_category)
    
    return sorted_df

def calculate_category_summary(inventory_df):
    """Calculate summary metrics by category"""
    
    category_summary = inventory_df.groupby('Category').agg({
        'Product_Name': 'count',
        'Total_Sales': 'sum',
        'Avg_Daily_Demand': 'sum',
        'EOQ': 'sum',
        'Safety_Stock': 'sum',
        'Turnover_Ratio': 'mean'
    }).round(2)
    
    category_summary.columns = [
        'Product_Count',
        'Total_Sales',
        'Total_Daily_Demand',
        'Total_EOQ',
        'Total_Safety_Stock',
        'Avg_Turnover_Ratio'
    ]
    
    # Calculate total inventory value
    inventory_df['Inventory_Value'] = inventory_df['EOQ'] * inventory_df['Avg_Unit_Cost']
    category_inventory = inventory_df.groupby('Category')['Inventory_Value'].sum()
    category_summary['Total_Inventory_Value'] = category_inventory.round(2)
    
    return category_summary.reset_index()

def main():
    """Main inventory optimization analysis"""
    
    print("🔄 Starting Inventory Optimization Analysis...")
    
    # Load the main dataset
    data_file = 'data/raw/DataCoSupplyChainDataset.csv'
    if not os.path.exists(data_file):
        print("❌ Dataset not found!")
        return
    
    # Read data
    print("📊 Loading dataset...")
    df = pd.read_csv(data_file, encoding='latin-1', low_memory=False)
    print(f"✅ Loaded {len(df):,} records")
    
    # Calculate inventory metrics
    print("🔢 Calculating inventory metrics...")
    inventory_df = calculate_inventory_metrics(df)
    
    if inventory_df is None or len(inventory_df) == 0:
        print("❌ Could not calculate inventory metrics")
        return
    
    print(f"✅ Calculated metrics for {len(inventory_df)} products")
    
    # Generate ABC analysis
    print("📈 Performing ABC analysis...")
    abc_df = generate_abc_analysis(inventory_df)
    
    # Calculate category summary
    print("📋 Generating category summary...")
    category_summary = calculate_category_summary(inventory_df)
    
    # Save results
    os.makedirs('data/processed', exist_ok=True)
    
    # Save detailed inventory metrics
    inventory_file = 'data/processed/inventory_optimization.csv'
    abc_df.to_csv(inventory_file, index=False)
    print(f"💾 Saved inventory analysis: {inventory_file}")
    
    # Save category summary
    category_file = 'data/processed/inventory_category_summary.csv'
    category_summary.to_csv(category_file, index=False)
    print(f"💾 Saved category summary: {category_file}")
    
    # Print summary statistics
    print("\n📊 INVENTORY OPTIMIZATION SUMMARY")
    print("=" * 50)
    print(f"Total Products Analyzed: {len(inventory_df):,}")
    print(f"Total Categories: {inventory_df['Category'].nunique()}")
    print(f"Total Sales Value: ${inventory_df['Total_Sales'].sum():,.2f}")
    print(f"Total EOQ Units: {inventory_df['EOQ'].sum():,.0f}")
    print(f"Total Safety Stock: {inventory_df['Safety_Stock'].sum():,.0f}")
    
    # ABC breakdown
    abc_counts = abc_df['ABC_Category'].value_counts()
    print(f"\nABC Analysis:")
    for category in ['A', 'B', 'C']:
        count = abc_counts.get(category, 0)
        pct = (count / len(abc_df)) * 100
        print(f"  Category {category}: {count} products ({pct:.1f}%)")
    
    # Stock status breakdown
    status_counts = inventory_df['Stock_Status'].value_counts()
    print(f"\nStock Movement Analysis:")
    for status in status_counts.index:
        count = status_counts[status]
        pct = (count / len(inventory_df)) * 100
        print(f"  {status}: {count} products ({pct:.1f}%)")
    
    print("\n✅ Inventory optimization analysis completed!")

if __name__ == "__main__":
    main()