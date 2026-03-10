import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("DEMAND FORECASTING - DATACO SUPPLY CHAIN")
print("="*80)

# Load dataset
print("\n1. LOADING DATA...")
df = pd.read_csv('dataset/DataCoSupplyChainDataset.csv', encoding='latin-1')
print(f"Dataset loaded: {df.shape[0]:,} rows")

# Convert date
df['order date (DateOrders)'] = pd.to_datetime(df['order date (DateOrders)'])

# Filter to Oct 2017
df_filtered = df[df['order date (DateOrders)'] <= '2017-10-31'].copy()
print(f"Filtered to Oct 2017: {df_filtered.shape[0]:,} rows")

# Top 5 categories
top_5_categories = ['Fishing', 'Cleats', 'Camping & Hiking', 'Cardio Equipment', "Women's Apparel"]
df_top5 = df_filtered[df_filtered['Category Name'].isin(top_5_categories)].copy()
print(f"Top 5 categories: {df_top5.shape[0]:,} rows")

# Aggregate daily sales
daily_sales = df_top5.groupby(['order date (DateOrders)', 'Category Name'])['Sales'].sum().reset_index()
daily_sales.columns = ['date', 'category', 'sales']
print(f"Daily aggregated data: {daily_sales.shape[0]:,} rows")

print("\n2. INSTALLING PROPHET...")
import subprocess
result = subprocess.run(['pip', 'install', 'prophet'], capture_output=True, text=True)
if result.returncode == 0:
    print("Prophet installed successfully!")
else:
    print("Prophet may already be installed or installation in progress...")

print("\n3. IMPORTING PROPHET...")
try:
    from prophet import Prophet
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    print("Prophet imported successfully!")
except ImportError as e:
    print(f"Error importing Prophet: {e}")
    print("Please run: pip install prophet")
    exit(1)

print("\n4. BUILDING FORECASTS FOR TOP 5 CATEGORIES...")
print("="*80)

forecast_results = {}
all_forecasts = []
train_end_date = pd.Timestamp('2016-12-31')

for category in top_5_categories:
    print(f"\n{'='*80}")
    print(f"CATEGORY: {category}")
    print(f"{'='*80}")
    
    # Prepare data
    cat_data = daily_sales[daily_sales['category'] == category].copy()
    cat_data = cat_data[['date', 'sales']].rename(columns={'date': 'ds', 'sales': 'y'})
    cat_data = cat_data.sort_values('ds').reset_index(drop=True)
    
    print(f"Data points: {len(cat_data)}")
    
    # Split train/test
    train = cat_data[cat_data['ds'] < '2017-01-01']
    test = cat_data[cat_data['ds'] >= '2017-01-01']
    
    print(f"Train: {len(train)} days | Test: {len(test)} days")
    
    # Build model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        interval_width=0.95
    )
    
    # Fit on FULL data (train + test) for future forecasting
    print("Training model on full dataset...")
    model.fit(cat_data)
    
    # Predict on test for validation
    test_forecast = model.predict(test[['ds']])
    
    # Metrics
    mae = mean_absolute_error(test['y'], test_forecast['yhat'])
    rmse = np.sqrt(mean_squared_error(test['y'], test_forecast['yhat']))
    
    print(f"MAE: ${mae:,.2f}")
    print(f"RMSE: ${rmse:,.2f}")
    
    # Trend
    recent_avg = test['y'].tail(30).mean()
    earlier_avg = test['y'].head(30).mean()
    trend = 'Increasing' if recent_avg > earlier_avg else 'Decreasing' if recent_avg < earlier_avg else 'Stable'
    print(f"Trend: {trend}")
    
    # Future forecast (90 days beyond last data point)
    print("Generating 90-day forecast...")
    future = model.make_future_dataframe(periods=90, freq='D')
    forecast = model.predict(future)
    
    # Extract ONLY the future 90 days (after last date in data)
    last_date = cat_data['ds'].max()
    future_forecast = forecast[forecast['ds'] > last_date].copy()
    future_forecast = future_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    future_forecast['Category'] = category
    
    # Clip negative predictions to 0
    future_forecast['yhat'] = future_forecast['yhat'].clip(lower=0)
    future_forecast['yhat_lower'] = future_forecast['yhat_lower'].clip(lower=0)
    future_forecast['yhat_upper'] = future_forecast['yhat_upper'].clip(lower=0)
    
    avg_forecast = future_forecast['yhat'].mean()
    total_forecast = future_forecast['yhat'].sum()
    
    print(f"Future forecast rows: {len(future_forecast)}")
    print(f"Avg daily forecast: ${avg_forecast:,.0f}")
    print(f"90-day total: ${total_forecast:,.0f}")
    
    # Store results
    forecast_results[category] = {
        'mae': mae,
        'rmse': rmse,
        'trend': trend,
        'avg_daily': avg_forecast,
        'total_90day': total_forecast,
        'model': model,
        'full_data': cat_data,
        'test': test,
        'future_forecast': future_forecast
    }
    
    # Append to results list BEFORE the loop ends
    all_forecasts.append(future_forecast)

print(f"\n{'='*80}")
print("5. EXPORTING RESULTS...")
print(f"{'='*80}")

# Combine all forecasts
final_forecast_df = pd.concat(all_forecasts, ignore_index=True)

# Rename columns properly
final_forecast_df.columns = ['Date', 'Predicted_Sales', 'Lower_Bound', 'Upper_Bound', 'Category']

# Reorder columns
final_forecast_df = final_forecast_df[['Category', 'Date', 'Predicted_Sales', 'Lower_Bound', 'Upper_Bound']]

# Export
final_forecast_df.to_csv('demand_forecast_results.csv', index=False)

print(f"Saved {len(final_forecast_df)} rows to demand_forecast_results.csv")
print(f"\nSample data:")
print(final_forecast_df.head(10))
print(f"\nLast 5 rows:")
print(final_forecast_df.tail(5))

print(f"\n{'='*80}")
print("6. SUMMARY TABLE")
print(f"{'='*80}\n")

summary_data = []
for category in top_5_categories:
    result = forecast_results[category]
    summary_data.append({
        'Category': category,
        'MAE': f"${result['mae']:,.0f}",
        'RMSE': f"${result['rmse']:,.0f}",
        'Trend': result['trend'],
        'Avg Daily Forecast': f"${result['avg_daily']:,.0f}",
        '90-Day Total': f"${result['total_90day']:,.0f}"
    })

summary_df = pd.DataFrame(summary_data)
print(summary_df.to_string(index=False))

print(f"\n{'='*80}")
print("7. GENERATING VISUALIZATIONS...")
print(f"{'='*80}\n")

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

for category in top_5_categories:
    result = forecast_results[category]
    
    plt.figure(figsize=(14, 6))
    
    # Historical actual sales (blue line)
    plt.plot(result['full_data']['ds'], result['full_data']['y'], 
             'b-', label='Historical Sales', linewidth=1.5, alpha=0.7)
    
    # Test period predicted (orange dashed)
    test_pred = result['model'].predict(result['test'][['ds']])
    plt.plot(test_pred['ds'], test_pred['yhat'], 
             'orange', linestyle='--', label='Test Predictions', linewidth=2)
    
    # Future 90-day forecast (green line)
    future_fc = result['future_forecast']
    plt.plot(future_fc['ds'], future_fc['yhat'], 
             'g-', label='90-Day Forecast', linewidth=2.5)
    
    # Confidence interval shaded area
    plt.fill_between(future_fc['ds'], 
                     future_fc['yhat_lower'], 
                     future_fc['yhat_upper'], 
                     alpha=0.3, color='green', label='95% Confidence')
    
    # Vertical dotted line separating historical vs forecast
    last_date = result['full_data']['ds'].max()
    plt.axvline(x=last_date, color='red', linestyle=':', linewidth=2, label='Forecast Start')
    
    plt.title(f"{category} - Sales Forecast", fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Daily Sales ($)', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    filename = f"forecast_{category.replace(' ', '_').replace('&', 'and')}.png"
    plt.savefig(filename, dpi=100, bbox_inches='tight')
    plt.close()
    
    print(f"Saved: {filename}")

print(f"\n{'='*80}")
print("FORECASTING COMPLETE!")
print(f"{'='*80}")
print(f"\nOutput file: demand_forecast_results.csv")
print(f"Total forecast rows: {len(final_forecast_df)} (should be 450 = 90 days x 5 categories)")
print(f"Visualization files: 5 PNG files saved")
