"""
Smart Supply Chain Analytics Pipeline Runner
Automated execution of all analysis scripts in sequence

Author: Saakshi Jaiswal
Project: DataCo Supply Chain Analytics
"""

import subprocess
import sys
import os
import time
from datetime import datetime

# Change working directory to project root automatically
# so all relative paths work correctly
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ============================================================================
# PIPELINE CONFIGURATION
# ============================================================================

pipeline = [
    {
        "step": 1,
        "name": "Exploratory Data Analysis",
        "script": "scripts/01_eda.py",
        "expected_outputs": [
            "visuals/eda/top_10_categories.png",
            "visuals/eda/monthly_sales_trend.png"
        ],
        "critical": True
    },
    {
        "step": 2,
        "name": "Demand Forecasting (Prophet)",
        "script": "scripts/02_demand_forecasting.py",
        "expected_outputs": [
            "data/processed/demand_forecast_results.csv",
            "visuals/forecasting/90day_forecast.png"
        ],
        "critical": True
    },
    {
        "step": 3,
        "name": "Delivery Risk ML Model",
        "script": "scripts/03_delivery_risk_model.py",
        "expected_outputs": [
            "models/delivery_risk_model.pkl",
            "data/processed/delivery_risk_scored.csv",
            "visuals/risk_model/roc_curves.png"
        ],
        "critical": True
    },
    {
        "step": 4,
        "name": "Customer Segmentation (RFM)",
        "script": "scripts/04_rfm_segmentation.py",
        "expected_outputs": [
            "data/processed/customer_segments.csv",
            "visuals/rfm/segment_distribution.png"
        ],
        "critical": True
    },
    {
        "step": 5,
        "name": "NLP Product Analysis",
        "script": "scripts/05_nlp_analysis.py",
        "expected_outputs": [
            "data/processed/product_nlp_analysis.csv",
            "visuals/nlp/wordcloud_products.png"
        ],
        "critical": False
    },
    {
        "step": 6,
        "name": "Power BI Export Tables",
        "script": "scripts/06_export_powerbi_tables.py",
        "expected_outputs": [
            "data/powerbi/fact_orders.csv",
            "data/powerbi/dim_customer.csv",
            "data/powerbi/fact_forecast.csv",
            "data/powerbi/fact_rfm_segments.csv"
        ],
        "critical": False
    }
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def print_banner():
    """Print startup banner"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║       🚚 SMART SUPPLY CHAIN ANALYTICS PIPELINE          ║")
    print("║              Automated Pipeline Runner                   ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║  Author  : Saakshi Jaiswal                              ║")
    print(f"║  Project : DataCo Supply Chain Analytics                ║")
    print(f"║  Started : {current_time}                     ║")
    print("╚══════════════════════════════════════════════════════════╝\n")

def pre_flight_checks():
    """Run pre-flight checks before starting pipeline"""
    print("🔍 Running pre-flight checks...\n")
    
    # Check 1: Raw data file exists
    raw_data_path = "data/raw/DataCoSupplyChainDataset.csv"
    if not os.path.exists(raw_data_path):
        print("❌ ERROR: Raw dataset not found!")
        print("Please add DataCoSupplyChainDataset.csv to data/raw/ folder")
        sys.exit(1)
    print(f"✅ Raw dataset found: {raw_data_path}")
    
    # Check 2: All script files exist
    missing_scripts = []
    for step in pipeline:
        if not os.path.exists(step['script']):
            print(f"⚠️  WARNING: {step['script']} not found — will skip")
            missing_scripts.append(step['step'])
    
    if not missing_scripts:
        print("✅ All 6 script files found")
    
    # Check 3: Required folders exist, create if missing
    required_folders = [
        "data/raw",
        "data/processed",
        "data/powerbi",
        "models",
        "visuals/eda",
        "visuals/forecasting",
        "visuals/risk_model",
        "visuals/rfm",
        "visuals/nlp"
    ]
    
    for folder in required_folders:
        os.makedirs(folder, exist_ok=True)
    print("✅ All required folders verified/created")
    
    print("\n✅ Pre-flight checks complete. Starting pipeline...")
    print("━" * 60 + "\n")
    
    return missing_scripts

def run_step(step_info):
    """Run a single pipeline step"""
    # Print step header
    print("┌─────────────────────────────────────────┐")
    print(f"│ STEP {step_info['step']}/6 — {step_info['name']:<28} │")
    print(f"│ Script: {step_info['script']:<31} │")
    print(f"│ Started: {datetime.now().strftime('%H:%M:%S'):<31} │")
    print("└─────────────────────────────────────────┘\n")
    
    # Check if script exists
    if not os.path.exists(step_info['script']):
        print(f"❌ STEP {step_info['step']} SKIPPED — Script not found")
        return not step_info['critical']  # Non-critical can continue
    
    # Record start time
    start_time = time.time()
    
    # Run the script (change to scripts directory first)
    try:
        result = subprocess.run(
            [sys.executable, os.path.basename(step_info['script'])],
            capture_output=False,
            text=True,
            cwd='scripts'
        )
        returncode = result.returncode
    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        returncode = 1
    
    # Record end time
    end_time = time.time()
    elapsed = end_time - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    # Check return code
    if returncode == 0:
        print(f"\n✅ STEP {step_info['step']} COMPLETE in {minutes} min {seconds} sec")
        
        # Check expected outputs
        for output in step_info['expected_outputs']:
            if os.path.exists(output):
                print(f"  ✅ {output}")
            else:
                print(f"  ⚠️  {output} NOT FOUND")
        
        return True
    else:
        print(f"\n❌ STEP {step_info['step']} FAILED after {minutes} min {seconds} sec")
        print(f"Error in: {step_info['script']}")
        
        if step_info['critical']:
            print("🛑 Critical step failed — stopping pipeline")
            print("Fix the error above and re-run pipeline")
            return False
        else:
            print("⚠️  Non-critical step — continuing...")
            return True

def count_output_files():
    """Count generated output files"""
    counts = {}
    
    folders = {
        "data/processed": "processed",
        "data/powerbi": "powerbi",
        "models": "models",
        "visuals": "visuals"
    }
    
    for folder, key in folders.items():
        if os.path.exists(folder):
            if key == "visuals":
                # Count all files in subdirectories
                count = 0
                for root, dirs, files in os.walk(folder):
                    count += len([f for f in files if f.endswith('.png')])
                counts[key] = count
            else:
                files = os.listdir(folder)
                if key == "models":
                    counts[key] = len([f for f in files if f.endswith('.pkl')])
                else:
                    counts[key] = len([f for f in files if f.endswith('.csv')])
        else:
            counts[key] = 0
    
    return counts

def print_summary(results, total_time):
    """Print final summary report"""
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    
    passed = sum(1 for r in results if r['success'])
    total = len(results)
    
    print("\n" + "━" * 60)
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║              PIPELINE EXECUTION SUMMARY                  ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║  Completed : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}                     ║")
    print(f"║  Total Time: {minutes} minutes {seconds} seconds{' ' * (29 - len(str(minutes)) - len(str(seconds)))}║")
    print(f"║  Steps Done: {passed}/{total}{' ' * 48}║")
    print("╠══════════════════════════════════════════════════════════╣")
    print("║  STEP RESULTS:                                          ║")
    
    for result in results:
        status = "✅" if result['success'] else "❌"
        name = result['name']
        print(f"║  {status} Step {result['step']} — {name:<42} ║")
    
    print("╠══════════════════════════════════════════════════════════╣")
    print("║  OUTPUT FILES GENERATED:                                ║")
    
    counts = count_output_files()
    print(f"║  📁 data/processed/  → {counts['processed']} CSV files{' ' * (28 - len(str(counts['processed'])))}║")
    print(f"║  📁 data/powerbi/    → {counts['powerbi']} CSV files{' ' * (28 - len(str(counts['powerbi'])))}║")
    print(f"║  📁 models/          → {counts['models']} PKL files{' ' * (28 - len(str(counts['models'])))}║")
    print(f"║  📁 visuals/         → {counts['visuals']} PNG files{' ' * (28 - len(str(counts['visuals'])))}║")
    print("╚══════════════════════════════════════════════════════════╝\n")
    
    if passed == total:
        print("🎉 PIPELINE COMPLETE — All steps successful!")
        print("📊 Open data/powerbi/ files in Power BI to build dashboard\n")
    else:
        print("⚠️  PIPELINE FINISHED WITH ERRORS")
        print("Fix failed steps and re-run: python run_pipeline.py\n")

def parse_arguments():
    """Parse command line arguments"""
    args = sys.argv[1:]
    
    if not args:
        return pipeline  # Run all steps
    
    selected_steps = []
    
    if '--steps' in args:
        idx = args.index('--steps')
        step_numbers = []
        for i in range(idx + 1, len(args)):
            if args[i].startswith('--'):
                break
            try:
                step_numbers.append(int(args[i]))
            except ValueError:
                break
        selected_steps = [s for s in pipeline if s['step'] in step_numbers]
        print(f"🎯 Running steps: {', '.join(map(str, step_numbers))}\n")
    
    elif '--from' in args:
        idx = args.index('--from')
        if idx + 1 < len(args):
            try:
                from_step = int(args[idx + 1])
                selected_steps = [s for s in pipeline if s['step'] >= from_step]
                step_nums = [s['step'] for s in selected_steps]
                print(f"🎯 Running steps: {', '.join(map(str, step_nums))} (from step {from_step})\n")
            except ValueError:
                print("❌ Invalid step number after --from")
                sys.exit(1)
    
    elif '--step' in args:
        idx = args.index('--step')
        if idx + 1 < len(args):
            try:
                step_num = int(args[idx + 1])
                selected_steps = [s for s in pipeline if s['step'] == step_num]
                print(f"🎯 Running step: {step_num}\n")
            except ValueError:
                print("❌ Invalid step number after --step")
                sys.exit(1)
    
    if not selected_steps:
        print("❌ No valid steps selected")
        sys.exit(1)
    
    return selected_steps

# ============================================================================
# MAIN PIPELINE EXECUTION
# ============================================================================

def main():
    """Main pipeline execution"""
    # Print banner
    print_banner()
    
    # Parse command line arguments
    steps_to_run = parse_arguments()
    
    # Pre-flight checks
    missing_scripts = pre_flight_checks()
    
    # Run pipeline
    results = []
    pipeline_start = time.time()
    
    for step in steps_to_run:
        success = run_step(step)
        results.append({
            'step': step['step'],
            'name': step['name'],
            'success': success
        })
        
        if not success and step['critical']:
            break  # Stop pipeline on critical failure
        
        print()  # Blank line between steps
    
    # Calculate total time
    pipeline_end = time.time()
    total_time = pipeline_end - pipeline_start
    
    # Print summary
    print_summary(results, total_time)

if __name__ == '__main__':
    main()
