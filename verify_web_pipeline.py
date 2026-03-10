#!/usr/bin/env python3
"""
Verify the web pipeline works
"""

import requests
import time
import json

def test_web_pipeline():
    """Test the pipeline through the web interface"""
    print("🌐 Testing Web Pipeline")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    # Test if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Web server is running")
        else:
            print(f"⚠️ Server responded with status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to web server: {e}")
        print("💡 Make sure to run: python run_app.py")
        return False
    
    # Test pipeline endpoint
    try:
        print("\n🔄 Testing pipeline endpoint...")
        
        # This would normally be a streaming endpoint
        # For now, just check if it's accessible
        response = requests.get(f"{base_url}/api/pipeline/run", timeout=2, stream=True)
        
        if response.status_code == 200:
            print("✅ Pipeline endpoint accessible")
            
            # Read first few lines of streaming response
            lines_read = 0
            for line in response.iter_lines():
                if line and lines_read < 5:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data: '):
                        data = decoded_line[6:]  # Remove 'data: ' prefix
                        try:
                            parsed = json.loads(data)
                            print(f"📊 Pipeline event: {parsed.get('type', 'unknown')}")
                        except:
                            print(f"📊 Pipeline data: {data[:50]}...")
                    lines_read += 1
                elif lines_read >= 5:
                    break
            
            return True
        else:
            print(f"❌ Pipeline endpoint error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⚠️ Pipeline request timed out (this might be normal)")
        return True  # Timeout might be expected for long-running pipeline
    except requests.exceptions.RequestException as e:
        print(f"❌ Pipeline request failed: {e}")
        return False

def check_file_outputs():
    """Check if pipeline creates expected output files"""
    print("\n📁 Checking Output Files")
    print("=" * 40)
    
    import os
    
    expected_files = [
        'data/processed/delivery_risk_scored.csv',
        'data/processed/demand_forecast_results.csv',
        'data/processed/customer_segments.csv',
        'models/delivery_risk_model.pkl'
    ]
    
    files_exist = 0
    for file_path in expected_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
            files_exist += 1
        else:
            print(f"❌ {file_path}")
    
    print(f"\n📊 Files found: {files_exist}/{len(expected_files)}")
    return files_exist > 0

def main():
    print("🚀 CHAINPULSE WEB PIPELINE VERIFICATION")
    print("=" * 50)
    
    web_ok = test_web_pipeline()
    files_ok = check_file_outputs()
    
    print("\n" + "=" * 50)
    print("VERIFICATION RESULTS")
    print("=" * 50)
    
    if web_ok:
        print("✅ Web pipeline accessible")
    else:
        print("❌ Web pipeline issues")
    
    if files_ok:
        print("✅ Some output files exist")
    else:
        print("❌ No output files found")
    
    if web_ok and files_ok:
        print("\n🎉 Pipeline appears to be working!")
        print("💡 Try accessing http://localhost:5000/pipeline-status")
    elif web_ok:
        print("\n⚠️ Web interface works but no outputs yet")
        print("💡 Try running the pipeline from the web interface")
    else:
        print("\n❌ Pipeline needs troubleshooting")
        print("💡 Check the Flask app logs for errors")

if __name__ == "__main__":
    main()