# ChainPulse — ml_predictor.py
"""
Machine Learning Prediction Module
Handles loading trained models and making predictions
"""

import pickle
import pandas as pd
import numpy as np
import os
from datetime import datetime

class RiskPredictor:
    """Risk prediction using trained model"""
    
    def __init__(self, models_path='models'):
        self.models_path = models_path
        self.model = None
        self.label_encoders = None
        self.model_loaded = False
        self.load_model()
    
    def load_model(self):
        """Load the trained model and encoders"""
        try:
            model_path = os.path.join(self.models_path, 'delivery_risk_model.pkl')
            encoders_path = os.path.join(self.models_path, 'label_encoders.pkl')
            
            if os.path.exists(model_path) and os.path.exists(encoders_path):
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(encoders_path, 'rb') as f:
                    self.label_encoders = pickle.load(f)
                self.model_loaded = True
                print("✅ Risk prediction model loaded successfully")
            else:
                print("⚠️ Model files not found. Using fallback prediction.")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model_loaded = False
    
    def predict(self, order_data):
        """
        Predict delivery risk for a single order
        
        Args:
            order_data (dict): Order information with required features
            
        Returns:
            dict: Prediction results with risk level and probability
        """
        if not self.model_loaded:
            return self._fallback_prediction(order_data)
        
        try:
            # Prepare features
            features = self._prepare_features(order_data)
            
            # Make prediction
            risk_probability = self.model.predict_proba([features])[0][1]
            
            # Determine risk level
            if risk_probability >= 0.7:
                risk_level = 'High Risk'
            elif risk_probability >= 0.4:
                risk_level = 'Medium Risk'
            else:
                risk_level = 'Low Risk'
            
            return {
                'risk_level': risk_level,
                'probability': float(risk_probability)
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return self._fallback_prediction(order_data)
    
    def _prepare_features(self, order_data):
        """Prepare features for model prediction"""
        # Expected features in order
        feature_names = ['Sales', 'Order Item Quantity', 'Order Item Discount Rate', 
                        'Order Item Profit Ratio', 'Days for shipment (scheduled)',
                        'Shipping Mode', 'Order Region', 'Category Name']
        
        features = []
        
        # Numeric features
        features.append(float(order_data.get('Sales', 200)))
        features.append(int(order_data.get('Order Item Quantity', 1)))
        features.append(float(order_data.get('Order Item Discount Rate', 0.1)))
        features.append(float(order_data.get('Order Item Profit Ratio', 0.3)))
        features.append(int(order_data.get('Days for shipment (scheduled)', 4)))
        
        # Categorical features (encoded)
        categorical_features = ['Shipping Mode', 'Order Region', 'Category Name']
        for feature in categorical_features:
            if feature in self.label_encoders and feature in order_data:
                try:
                    encoded_value = self.label_encoders[feature].transform([order_data[feature]])[0]
                    features.append(encoded_value)
                except:
                    features.append(0)  # Default for unknown categories
            else:
                features.append(0)
        
        return features
    
    def _fallback_prediction(self, order_data):
        """Fallback prediction when model is not available"""
        # Simple rule-based prediction
        shipping = order_data.get('Shipping Mode', 'Standard Class')
        days = int(order_data.get('Days for shipment (scheduled)', 4))
        
        # Basic risk assessment
        if shipping == 'Same Day' or days <= 1:
            risk_level = 'High Risk'
            probability = 0.8
        elif shipping == 'First Class' or days <= 2:
            risk_level = 'Medium Risk'
            probability = 0.5
        else:
            risk_level = 'Low Risk'
            probability = 0.2
        
        return {
            'risk_level': risk_level,
            'probability': probability
        }

# For backward compatibility
class DeliveryRiskPredictor(RiskPredictor):
    pass

# Global predictor instance
risk_predictor = RiskPredictor()