#!/usr/bin/env python3
"""
Install all required packages for ChainPulse
"""

import subprocess
import sys

packages = [
    "pandas",
    "numpy", 
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "xgboost",
    "imbalanced-learn",
    "prophet",
    "joblib",
    "nltk",
    "wordcloud",
    "squarify",
    "openpyxl",
    "flask",
    "flask-cors",
    "reportlab",
    "statsmodels",
    "lightgbm"
]

print("🚀 Installing ChainPulse Dependencies...")
print("=" * 50)

for package in packages:
    print(f"\n📦 Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")

print("\n" + "=" * 50)
print("✅ Installation complete!")
print("Now restart Flask and try the pipeline again.")
print("=" * 50)