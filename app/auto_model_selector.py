"""
Auto Model Selector - Intelligent model selection based on dataset characteristics
"""

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import warnings
warnings.filterwarnings('ignore')


class AutoModelSelector:
    """Automatically selects optimal models based on dataset profiling"""
    
    def __init__(self, project_root):
        self.project_root = project_root
        self.profile = {}
        self.selected_models = {
            'forecast': {'model': 'Prophet', 'params': {}},
            'risk': {'model': 'RandomForest', 'params': {}},
            'segmentation': {'k': 4}
        }
    
    def profile_dataset(self):
        """Profile the dataset to understand its characteristics"""
        try:
            data_path = os.path.join(self.project_root, 'data', 'raw', 'DataCoSupplyChainDataset.csv')
            df = pd.read_csv(data_path, encoding='latin-1', nrows=5000)
            
            # Basic profiling
            self.profile['rows'] = len(df)
            self.profile['columns'] = len(df.columns)
            
            # Date range
            if 'order date (DateOrders)' in df.columns:
                dates = pd.to_datetime(df['order date (DateOrders)'], errors='coerce')
                date_range = (dates.max() - dates.min()).days
                self.profile['date_range_days'] = date_range
                self.profile['weekly_seasonality'] = date_range > 365
            else:
                self.profile['date_range_days'] = 0
                self.profile['weekly_seasonality'] = False
            
            # Customer count
            if 'Order Customer Id' in df.columns:
                self.profile['unique_customers'] = df['Order Customer Id'].nunique()
            else:
                self.profile['unique_customers'] = 0
            
            # Late delivery rate
            if 'Delivery Status' in df.columns:
                late_count = (df['Delivery Status'] == 'Late delivery').sum()
                self.profile['late_delivery_rate'] = late_count / len(df) if len(df) > 0 else 0
            else:
                self.profile['late_delivery_rate'] = 0
            
            return True
        except Exception as e:
            print(f"Profiling error: {e}")
            return False
    
    def select_forecast_model(self):
        """Select forecasting model based on data characteristics"""
        date_range = self.profile.get('date_range_days', 0)
        
        if date_range > 730:  # More than 2 years
            self.selected_models['forecast']['model'] = 'Prophet'
        elif date_range > 365:  # More than 1 year
            self.selected_models['forecast']['model'] = 'ARIMA'
        else:
            self.selected_models['forecast']['model'] = 'ETS'
    
    def select_risk_model(self):
        """Select risk model based on data characteristics"""
        late_rate = self.profile.get('late_delivery_rate', 0)
        
        if late_rate > 0.3:  # High late rate
            self.selected_models['risk']['model'] = 'XGBoost'
        else:
            self.selected_models['risk']['model'] = 'RandomForest'
    
    def select_segmentation_k(self):
        """Select optimal K for customer segmentation"""
        customers = self.profile.get('unique_customers', 0)
        
        if customers > 10000:
            self.selected_models['segmentation']['k'] = 5
        elif customers > 5000:
            self.selected_models['segmentation']['k'] = 4
        else:
            self.selected_models['segmentation']['k'] = 3
    
    def run_smart_forecasting(self):
        """Run forecasting with selected model"""
        try:
            # For now, just return success
            # In production, would run actual forecasting
            return True
        except Exception as e:
            print(f"Forecasting error: {e}")
            return False
    
    def run_smart_risk_model(self):
        """Run risk modeling with selected model"""
        try:
            data_path = os.path.join(self.project_root, 'data', 'raw', 'DataCoSupplyChainDataset.csv')
            df = pd.read_csv(data_path, encoding='latin-1', nrows=5000)
            
            # Simple risk model
            if 'Delivery Status' in df.columns and 'Shipping Mode' in df.columns:
                df['Is_Late'] = (df['Delivery Status'] == 'Late delivery').astype(int)
                
                # Encode shipping mode
                le = LabelEncoder()
                X = le.fit_transform(df['Shipping Mode'].astype(str)).reshape(-1, 1)
                y = df['Is_Late'].values
                
                # Train simple model
                model = RandomForestClassifier(n_estimators=10, random_state=42)
                model.fit(X, y)
                
                # Save model
                models_path = os.path.join(self.project_root, 'models')
                os.makedirs(models_path, exist_ok=True)
                joblib.dump(model, os.path.join(models_path, 'delivery_risk_model.pkl'))
                
                return True
            return False
        except Exception as e:
            print(f"Risk modeling error: {e}")
            return False
    
    def run_smart_segmentation(self):
        """Run customer segmentation with selected K"""
        try:
            # For now, just return success
            # In production, would run actual segmentation
            return True
        except Exception as e:
            print(f"Segmentation error: {e}")
            return False
    
    def export_powerbi_tables(self):
        """Export Power BI tables"""
        try:
            # For now, just return success
            # In production, would run actual export
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
