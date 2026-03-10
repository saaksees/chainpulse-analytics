"""
Simple, bulletproof pipeline runner
Runs scripts sequentially with proper error handling
"""

import os
import sys
import subprocess

def run_pipeline(project_root):
    """Run all analytics scripts"""
    
    scripts = [
        ('01_eda.py', 'EDA Analysis'),
        ('02_demand_forecasting.py', 'Demand Forecasting'),
        ('03_delivery_risk_model.py', 'Risk Model'),
        ('04_rfm_segmentation.py', 'Customer Segmentation'),
        ('05_nlp_analysis.py', 'NLP Analysis'),
        ('06_export_powerbi_tables.py', 'Power BI Export')
    ]
    
    print("🚀 Starting ChainPulse Pipeline")
    print("=" * 50)
    
    for i, (script, name) in enumerate(scripts, 1):
        print(f"\n🔄 Step {i}/6: {name}")
        
        script_path = os.path.join(project_root, 'scripts', script)
        
        if not os.path.exists(script_path):
            print(f"❌ Script not found: {script_path}")
            continue
        
        try:
            # Run with minimal overhead
            result = subprocess.run(
                [sys.executable, script_path],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                print(f"✅ {name} completed successfully")
            else:
                print(f"❌ {name} failed")
                if result.stderr:
                    print(f"Error: {result.stderr[:200]}")
                    
        except subprocess.TimeoutExpired:
            print(f"⏰ {name} timed out")
        except Exception as e:
            print(f"❌ {name} error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Pipeline execution complete")

if __name__ == "__main__":
    project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    run_pipeline(project_root)
