#!/usr/bin/env python3
"""
Standalone Pipeline Runner
Runs all analytics scripts without Flask context
"""

import os
import sys
import subprocess
import json
from datetime import datetime

def run_pipeline():
    """Run all analytics scripts in sequence"""
    
    # Get project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    scripts = [
        ('01_eda.py', 'EDA Analysis'),
        ('02_demand_forecasting.py', 'Demand Forecasting'),
        ('03_delivery_risk_model.py', 'Risk Model'),
        ('04_rfm_segmentation.py', 'Customer Segmentation'),
        ('05_nlp_analysis.py', 'NLP Analysis'),
        ('06_export_powerbi_tables.py', 'Power BI Export')
    ]
    
    results = {}
    
    print("🚀 Starting ChainPulse Analytics Pipeline")
    print("=" * 50)
    
    for i, (script, name) in enumerate(scripts, 1):
        print(f"\n🔄 Step {i}/6: {name}")
        
        script_path = os.path.join(project_root, 'scripts', script)
        
        if not os.path.exists(script_path):
            print(f"❌ Script not found: {script_path}")
            results[script] = False
            continue
        
        try:
            # Run script with proper environment
            env = os.environ.copy()
            env['PYTHONPATH'] = project_root
            
            result = subprocess.run(
                [sys.executable, script_path],
                cwd=project_root,
                env=env,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout per script
            )
            
            success = result.returncode == 0
            results[script] = success
            
            if success:
                print(f"✅ {name} completed successfully")
            else:
                print(f"❌ {name} failed")
                print(f"Error: {result.stderr[:200]}...")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {name} timed out (5 minutes)")
            results[script] = False
        except Exception as e:
            print(f"❌ {name} error: {e}")
            results[script] = False
    
    # Summary
    successful = sum(results.values())
    total = len(results)
    
    print("\n" + "=" * 50)
    print("📊 PIPELINE SUMMARY")
    print(f"✅ Successful: {successful}/{total}")
    print(f"❌ Failed: {total - successful}/{total}")
    
    if successful == total:
        print("🎉 All scripts completed successfully!")
        return True
    else:
        print("⚠️ Some scripts failed. Check logs above.")
        return False

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)