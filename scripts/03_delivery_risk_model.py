import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
Dynamic Delivery Risk Prediction Model
Works with ANY supply chain CSV using column detection
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix, 
                             accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, roc_curve)
try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
import joblib
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Add scripts directory to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from column_detector import detect_columns, get_first_csv_file, load_dataset_with_encoding, print_detection_summary

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 150

def main():
    print("=" * 60)
    print("DELIVERY RISK PREDICTION MODEL")
    print("=" * 60)

    # Get project root (parent of scripts directory)
    project_root = os.path.dirname(script_dir)

    # Create output directories
    os.makedirs(os.path.join(project_root, 'visuals', 'risk_model'), exist_ok=True)
    os.makedirs(os.path.join(project_root, 'data', 'processed'), exist_ok=True)
    os.makedirs(os.path.join(project_root, 'models'), exist_ok=True)

    # Load dataset
    data_dir = os.path.join(project_root, 'data', 'raw')
    data_file = get_first_csv_file(data_dir)
    
    if not data_file:
        print('No CSV file found in data/raw/')
        return
    
    print(f'Loading: {os.path.basename(data_file)}')
    df = load_dataset_with_encoding(data_file)
    print(f'Dataset loaded: {df.shape}')
    
    # Detect columns
    cols = detect_columns(df)
    found_count, total_count = print_detection_summary(cols, df)
    
    # Check if we have minimum required columns for risk modeling
    required_cols = ['delivery_status', 'shipping_mode']
    missing_required = [col for col in required_cols if not cols[col]]
    
    if missing_required:
        print(f'[ERROR] Missing required columns for risk modeling: {missing_required}')
        print('[WARNING] Creating empty risk model files and exiting')
        
        # Create empty files
        empty_risk = pd.DataFrame({
            'Risk_Score': [0],
            'Risk_Level': ['Low Risk'],
            'Sales': [0]
        })
        empty_risk.to_csv(os.path.join(project_root, 'data', 'processed', 'delivery_risk_scored.csv'), index=False)
        
        # Create dummy model
        from sklearn.dummy import DummyClassifier
        dummy_model = DummyClassifier(strategy='constant', constant=0)
        dummy_model.fit([[0]], [0])
        joblib.dump(dummy_model, os.path.join(project_root, 'models', 'delivery_risk_model.pkl'))
        
        return
    
    # Convert date if available
    if cols['date']:
        df[cols['date']] = pd.to_datetime(df[cols['date']], errors='coerce')
    
    # Create target variable
    if cols['late_flag']:
        # Direct late flag column
        if df[cols['late_flag']].dtype == 'object':
            df['Is_Late'] = df[cols['late_flag']].astype(str).str.lower().str.contains('late|1|true', na=False).astype(int)
        else:
            df['Is_Late'] = df[cols['late_flag']].astype(int)
    elif cols['delivery_status']:
        # Derive from delivery status
        df['Is_Late'] = df[cols['delivery_status']].astype(str).str.lower().str.contains('late', na=False).astype(int)
    else:
        print('[ERROR] Cannot create target variable - no delivery status or late flag column')
        return
    
    # Print class distribution
    late_counts = df['Is_Late'].value_counts()
    late_pct = df['Is_Late'].value_counts(normalize=True) * 100
    
    print("\n[BAR_CHART] Target Variable Distribution:")
    if 1 in late_counts.index:
        print(f"   Late deliveries (1):    {late_counts[1]:,} ({late_pct[1]:.1f}%)")
    if 0 in late_counts.index:
        print(f"   On-time deliveries (0): {late_counts[0]:,} ({late_pct[0]:.1f}%)")
    
    # Select features dynamically
    numerical_features = []
    categorical_features = []
    
    # Map detected columns to features
    feature_mapping = {
        'scheduled_days': 'numerical',
        'quantity': 'numerical', 
        'discount_rate': 'numerical',
        'profit_ratio': 'numerical',
        'sales': 'numerical',
        'profit': 'numerical',
        'shipping_mode': 'categorical',
        'region': 'categorical',
        'category': 'categorical'
    }
    
    for col_key, col_name in cols.items():
        if col_name and col_key in feature_mapping:
            if feature_mapping[col_key] == 'numerical':
                numerical_features.append(col_name)
            else:
                categorical_features.append(col_name)
    
    all_features = numerical_features + categorical_features
    
    if not all_features:
        print('[ERROR] No suitable features found for modeling')
        return
    
    print(f"\n[WRENCH] Selected Features:")
    print(f"   Numerical: {numerical_features}")
    print(f"   Categorical: {categorical_features}")
    
    # Prepare feature dataframe
    df_model = df[all_features + ['Is_Late']].copy()
    
    # Handle missing values
    for col in numerical_features:
        if col in df_model.columns:
            df_model[col] = pd.to_numeric(df_model[col], errors='coerce')
            df_model[col].fillna(df_model[col].median(), inplace=True)
    
    for col in categorical_features:
        if col in df_model.columns:
            df_model[col] = df_model[col].astype(str).fillna('Unknown')
    
    # Remove any remaining missing values
    df_model = df_model.dropna()
    print(f"After cleaning: {len(df_model):,} rows")
    
    if len(df_model) < 100:
        print('[ERROR] Insufficient data for modeling after cleaning')
        return
    
    # Prepare features and target
    X = df_model[all_features].copy()
    y = df_model['Is_Late'].copy()
    
    # Encode categorical features
    encoders = {}
    for col in categorical_features:
        if col in X.columns:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            encoders[col] = le
    
    # Save encoders
    joblib.dump(encoders, os.path.join(project_root, 'models', 'label_encoders.pkl'))
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"\n[BAR_CHART] Data Split:")
    print(f"   Training: {len(X_train):,} samples")
    print(f"   Testing:  {len(X_test):,} samples")
    
    # Train models
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    if HAS_XGBOOST:
        models['XGBoost'] = XGBClassifier(random_state=42, eval_metric='logloss')
    
    results = {}
    
    print(f"\n[AI] Training Models:")
    for name, model in models.items():
        print(f"   Training {name}...")
        
        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else y_pred
            
            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            
            try:
                auc = roc_auc_score(y_test, y_prob)
            except:
                auc = 0.5
            
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'auc': auc,
                'predictions': y_pred,
                'probabilities': y_prob
            }
            
            print(f"   [OK] {name}: AUC = {auc:.3f}")
            
        except Exception as e:
            print(f"   [ERROR] {name} failed: {e}")
    
    if not results:
        print('[ERROR] No models trained successfully')
        return
    
    # Select best model
    best_model_name = max(results.keys(), key=lambda x: results[x]['auc'])
    best_model = results[best_model_name]['model']
    
    print(f"\n[TROPHY] Best Model: {best_model_name} (AUC: {results[best_model_name]['auc']:.3f})")
    
    # Save best model
    joblib.dump(best_model, os.path.join(project_root, 'models', 'delivery_risk_model.pkl'))
    
    # Generate risk scores for all data
    risk_scores = best_model.predict_proba(X)[:, 1] if hasattr(best_model, 'predict_proba') else best_model.predict(X)
    
    # Create risk levels
    risk_levels = pd.cut(risk_scores, 
                         bins=[0, 0.4, 0.7, 1.0],
                         labels=['Low Risk', 'Medium Risk', 'High Risk'])
    
    # Create scored dataset
    scored_df = df_model.copy()
    scored_df['Risk_Score'] = risk_scores
    scored_df['Risk_Level'] = risk_levels.astype(str)
    
    # Add original columns if available
    if cols['sales']:
        scored_df['Sales'] = df.loc[scored_df.index, cols['sales']]
    
    # Save scored data
    scored_df.to_csv(os.path.join(project_root, 'data', 'processed', 'delivery_risk_scored.csv'), index=False)
    
    # Create visualizations
    print(f"\n[BAR_CHART] Creating visualizations...")
    
    # Risk distribution
    risk_dist = pd.Series(risk_levels).value_counts().sort_index()
    
    plt.figure(figsize=(8, 8))
    colors_risk = ['#2ecc71', '#f39c12', '#e74c3c']
    plt.pie(risk_dist.values, labels=risk_dist.index, autopct='%1.1f%%',
            colors=colors_risk, startangle=90)
    plt.title('Delivery Risk Distribution', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(project_root, 'visuals', 'risk_model', 'risk_distribution.png'), 
                dpi=150, bbox_inches='tight')
    plt.close()
    
    print('[OK] Saved: visuals/risk_model/risk_distribution.png')
    
    # Model comparison
    if len(results) > 1:
        plt.figure(figsize=(10, 6))
        model_names = list(results.keys())
        aucs = [results[name]['auc'] for name in model_names]
        
        bars = plt.bar(model_names, aucs, color=['#3498db', '#e74c3c', '#2ecc71'][:len(model_names)])
        plt.title('Model Performance Comparison (ROC-AUC)', fontsize=16, fontweight='bold')
        plt.ylabel('ROC-AUC Score', fontsize=12)
        plt.ylim(0, 1)
        
        # Add value labels on bars
        for bar, auc in zip(bars, aucs):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{auc:.3f}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(project_root, 'visuals', 'risk_model', 'model_comparison.png'), 
                    dpi=150, bbox_inches='tight')
        plt.close()
        
        print('[OK] Saved: visuals/risk_model/model_comparison.png')
    
    # Print summary
    print(f"\n" + "=" * 60)
    print("DELIVERY RISK MODEL SUMMARY")
    print("=" * 60)
    
    print(f"\n[OK] Model trained successfully")
    print(f"   Best model: {best_model_name}")
    print(f"   ROC-AUC: {results[best_model_name]['auc']:.3f}")
    print(f"   Features used: {len(all_features)}")
    
    risk_summary = pd.Series(risk_levels).value_counts().sort_index()
    print(f"\n[BAR_CHART] Risk Distribution:")
    for level, count in risk_summary.items():
        pct = (count / len(risk_levels)) * 100
        print(f"   {level}: {count:,} ({pct:.1f}%)")
    
    print(f"\n[FILES] Files saved:")
    print(f"   [SYMBOL] models/delivery_risk_model.pkl")
    print(f"   [SYMBOL] models/label_encoders.pkl") 
    print(f"   [SYMBOL] data/processed/delivery_risk_scored.csv")
    print(f"   [SYMBOL] visuals/risk_model/risk_distribution.png")
    if len(results) > 1:
        print(f"   [SYMBOL] visuals/risk_model/model_comparison.png")
    
    print(f"\n[OK] Delivery risk model complete!")

if __name__ == '__main__':
    main()