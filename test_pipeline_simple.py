#!/usr/bin/env python3
"""
Simple pipeline test - run one script at a time
"""

import os
import sys
import subprocess

def test_script(script_name):
    """Test a single script"""
    print(f"\n🔄 Testing {script_name}...")
    
    script_path = os.path.join('scripts', script_name)
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        # Run script with timeout
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes
        )
        
        if result.returncode == 0:
            print(f"✅ {script_name} completed successfully")
            if result.stdout:
                print("Output:", result.stdout[-200:])  # Last 200 chars
            return True
        else:
            print(f"❌ {script_name} failed")
            if result.stderr:
                print("Error:", result.stderr[-300:])  # Last 300 chars
            if result.stdout:
                print("Output:", result.stdout[-200:])
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {script_name} timed out")
        return False
    except Exception as e:
        print(f"❌ {script_name} error: {e}")
        return False

def main():
    print("🚀 Testing ChainPulse Pipeline Scripts")
    print("=" * 50)
    
    scripts = [
        '03_delivery_risk_model.py',  # Test the one we just fixed
        '01_eda.py',
        '02_demand_forecasting.py',
        '04_rfm_segmentation.py',
        '05_nlp_analysis.py',
        '06_export_powerbi_tables.py'
    ]
    
    results = {}
    
    for script in scripts:
        results[script] = test_script(script)
    
    print("\n" + "=" * 50)
    print("PIPELINE TEST RESULTS")
    print("=" * 50)
    
    for script, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {script}")
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nSummary: {passed}/{total} scripts passed")
    
    if passed == total:
        print("🎉 All scripts working!")
    else:
        print("⚠️ Some scripts need fixing")

if __name__ == "__main__":
    main()