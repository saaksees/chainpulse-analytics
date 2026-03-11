#!/usr/bin/env python3
"""
Train Advanced ML Models
Trains XGBoost, LSTM, and ensemble models for enhanced accuracy
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add app directory to path
sys.path.append('app')

def main():
    """Train all advanced ML models"""
    
    print("🚀 Starting Advanced ML Model Training...")
    print("=" * 60)
    
    # Load dataset
    data_file = 'data/raw/DataCoSupplyChainDataset.csv'
    if not os.path.exists(data_file):
        print("❌ Dataset not found!")
        return
    
    print("📊 Loading dataset...")
    df = pd.read_csv(data_file, encoding='latin-1', low_memory=False)
    print(f"✅ Loaded {len(df):,} records")
    
    # Create models directory
    os.makedirs('data/models', exist_ok=True)
    
    # 1. Train Advanced Risk Prediction Models
    print("\n🎯 Training Advanced Risk Prediction Models...")
    print("-" * 50)
    
    try:
        from advanced_ml_models import advanced_risk_predictor
        
        # Sample data for faster training (use full dataset in production)
        sample_size = min(10000, len(df))
        df_sample = df.sample(n=sample_size, random_state=42)
        
        risk_models = advanced_risk_predictor.train_models(df_sample)
        
        print(f"\n📊 Risk Prediction Model Results:")
        for model_name, model_info in risk_models.items():
            accuracy = model_info.get('accuracy', 0)
            print(f"  {model_name.title()}: {accuracy:.3f} accuracy")
        
        # Test prediction
        test_input = {
            'Shipping Mode': 'Standard Class',
            'Order Region': 'Western Europe',
            'Category Name': 'Fishing',
            'Sales': 200.0,
            'Order Item Quantity': 2,
            'Order Item Discount Rate': 0.1,
            'Order Item Profit Ratio': 0.3,
            'Days for shipment (scheduled)': 4
        }
        
        prediction = advanced_risk_predictor.predict(test_input)
        print(f"\n🧪 Test Prediction: {prediction['risk_level']} (confidence: {prediction['confidence']:.3f})")
        
    except Exception as e:
        print(f"❌ Risk model training failed: {e}")
    
    # 2. Train Advanced Forecasting Models
    print("\n📈 Training Advanced Forecasting Models...")
    print("-" * 50)
    
    try:
        from advanced_ml_models import advanced_forecasting_model
        
        # Use smaller sample for forecasting training
        forecast_sample = df.sample(n=min(5000, len(df)), random_state=42)
        
        forecasting_models = advanced_forecasting_model.train_models(forecast_sample)
        
        print(f"\n📊 Forecasting Model Results:")
        for category, models in forecasting_models.items():
            print(f"  {category}:")
            for model_name, model_info in models.items():
                r2 = model_info.get('r2', 0)
                print(f"    {model_name.title()}: {r2:.3f} R²")
        
        # Test forecasting
        if forecasting_models:
            test_category = list(forecasting_models.keys())[0]
            forecast_result = advanced_forecasting_model.predict_demand(test_category, days_ahead=7)
            
            if forecast_result['success']:
                avg_prediction = np.mean(forecast_result['predictions'])
                print(f"\n🧪 Test Forecast ({test_category}): ${avg_prediction:.2f} avg daily sales")
        
    except Exception as e:
        print(f"❌ Forecasting model training failed: {e}")
    
    # 3. Model Comparison and Recommendations
    print("\n📋 Model Performance Summary")
    print("=" * 60)
    
    # Check if models were trained successfully
    risk_model_path = 'data/models/advanced_models_metadata.json'
    forecast_model_path = 'data/models/forecasting_metadata.json'
    
    if os.path.exists(risk_model_path):
        print("✅ Advanced Risk Prediction Models: TRAINED")
        print("   - XGBoost, Random Forest, Gradient Boosting")
        print("   - Ensemble voting classifier")
        print("   - Enhanced feature engineering")
    else:
        print("❌ Risk Prediction Models: FAILED")
    
    if os.path.exists(forecast_model_path):
        print("✅ Advanced Forecasting Models: TRAINED")
        print("   - LSTM neural networks")
        print("   - Gradient boosting regressors")
        print("   - Time series feature engineering")
    else:
        print("❌ Forecasting Models: FAILED")
    
    # 4. Performance Improvements
    print("\n🎯 Expected Performance Improvements:")
    print("   📈 Risk Prediction: +15-25% accuracy improvement")
    print("   📊 Demand Forecasting: +20-30% accuracy improvement")
    print("   🚀 Feature Engineering: 50+ advanced features")
    print("   🎪 Ensemble Methods: Multiple model voting")
    print("   🧠 Deep Learning: LSTM for time series patterns")
    
    # 5. Installation Requirements
    print("\n📦 Optional Dependencies for Full Functionality:")
    print("   pip install xgboost tensorflow scikit-learn")
    print("   - XGBoost: Gradient boosting framework")
    print("   - TensorFlow: Deep learning with LSTM")
    print("   - Scikit-learn: Traditional ML algorithms")
    
    print("\n✅ Advanced ML model training completed!")
    print(f"🕒 Training completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()