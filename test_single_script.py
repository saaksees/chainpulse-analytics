#!/usr/bin/env python3
"""
Test a single script to debug issues
"""

import subprocess
import sys
import os

def test_risk_model():
    """Test the risk model script specifically"""
    print("Testing delivery risk model...")
    
    script_path = 'scripts/03_delivery_risk_model.py'
    
    if not os.path.exists(script_path):
        print(f"Script not found: {script_path}")
        return False
    
    try:
        # Set environment to handle unicode
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=120,
            env=env
        )
        
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running script: {e}")
        return False

if __name__ == "__main__":
    test_risk_model()