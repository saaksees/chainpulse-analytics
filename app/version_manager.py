import pandas as pd
import shutil
import os
import json
from datetime import datetime
from app.database import (create_version, set_active_version,
                         insert_orders, insert_risk_scores,
                         insert_forecasts, insert_segments,
                         get_active_version, get_all_versions)

def restore_defaults(project_root):
    """Restores DataCo processed results when no upload exists or user explicitly resets to defaults."""
    defaults_dir = os.path.join(project_root, 'data', 'defaults', 'dataco')
    if not os.path.exists(defaults_dir):
        return False, "No defaults found"
    
    try:
        # Restore processed CSVs
        processed_dir = os.path.join(project_root, 'data', 'processed')
        os.makedirs(processed_dir, exist_ok=True)
        
        for f in os.listdir(defaults_dir):
            if f.endswith('.csv') or f.endswith('.json'):
                src = os.path.join(defaults_dir, f)
                dst = os.path.join(processed_dir, f)
                shutil.copy2(src, dst)
        
        # Restore visuals
        visuals_src = os.path.join(defaults_dir, 'visuals')
        visuals_dst = os.path.join(project_root, 'visuals')
        if os.path.exists(visuals_src):
            if os.path.exists(visuals_dst):
                shutil.rmtree(visuals_dst)
            shutil.copytree(visuals_src, visuals_dst)
        
        # Restore models
        models_src = os.path.join(defaults_dir, 'models')
        models_dst = os.path.join(project_root, 'models')
        os.makedirs(models_dst, exist_ok=True)
        if os.path.exists(models_src):
            for f in os.listdir(models_src):
                if f.endswith('.pkl'):
                    src = os.path.join(models_src, f)
                    dst = os.path.join(models_dst, f)
                    shutil.copy2(src, dst)
        
        # Restore PowerBI data
        powerbi_src = os.path.join(defaults_dir, 'powerbi')
        powerbi_dst = os.path.join(project_root, 'data', 'powerbi')
        if os.path.exists(powerbi_src):
            if os.path.exists(powerbi_dst):
                shutil.rmtree(powerbi_dst)
            shutil.copytree(powerbi_src, powerbi_dst)
        
        # Update active dataset flag
        flag_path = os.path.join(project_root, 'data', 'active_dataset.json')
        with open(flag_path, 'w') as fl:
            json.dump({
                'name': 'DataCoSupplyChainDataset',
                'type': 'default',
                'uploaded_at': None,
                'is_default': True
            }, fl, indent=2)
        
        return True, "DataCo defaults restored"
        
    except Exception as e:
        return False, f"Error restoring defaults: {str(e)}"

# ── Save version after pipeline runs ─
def save_version_outputs(version_id, folder, project_root):
    """After pipeline runs, copy all output
    CSVs into the version folder AND
    insert data into SQLite database."""
    
    processed = os.path.join(project_root, 'data', 'processed')
    raw = os.path.join(project_root, 'data', 'raw', 'DataCoSupplyChainDataset.csv')
    
    # Files to copy into version folder
    files_to_copy = {
        'raw.csv': raw,
        'risk_scored.csv': os.path.join(processed, 'delivery_risk_scored.csv'),
        'forecasts.csv': os.path.join(processed, 'demand_forecast_results.csv'),
        'segments.csv': os.path.join(processed, 'customer_segments.csv'),
        'nlp.csv': os.path.join(processed, 'product_nlp_analysis.csv')
    }
    
    copied = []
    for dest_name, src_path in files_to_copy.items():
        if os.path.exists(src_path):
            dest = os.path.join(folder, dest_name)
            shutil.copy2(src_path, dest)
            copied.append(dest_name)
    
    print(f"📁 Saved {len(copied)} files to version folder")
    
    # Insert into SQLite
    try:
        # Orders
        if os.path.exists(raw):
            df = pd.read_csv(raw, encoding='latin-1', nrows=50000)
            insert_orders(version_id, df)
            print(f"✅ Inserted {len(df):,} orders to DB")
        
        # Risk scores
        risk_path = os.path.join(processed, 'delivery_risk_scored.csv')
        if os.path.exists(risk_path):
            df = pd.read_csv(risk_path)
            insert_risk_scores(version_id, df)
            print(f"✅ Inserted {len(df):,} risk scores to DB")
        
        # Forecasts
        fc_path = os.path.join(processed, 'demand_forecast_results.csv')
        if os.path.exists(fc_path):
            df = pd.read_csv(fc_path)
            insert_forecasts(version_id, df)
            print(f"✅ Inserted {len(df):,} forecasts to DB")
        
        # Segments
        seg_path = os.path.join(processed, 'customer_segments.csv')
        if os.path.exists(seg_path):
            df = pd.read_csv(seg_path)
            insert_segments(version_id, df)
            print(f"✅ Inserted {len(df):,} segments to DB")
        
        # Save metadata
        meta = {
            'version_id': version_id,
            'saved_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'files_saved': copied
        }
        
        with open(os.path.join(folder, 'metadata.json'), 'w') as f:
            json.dump(meta, f, indent=2)
            
    except Exception as e:
        print(f"⚠️ DB insert error: {e}")
    
    return copied

# ── Restore old version to active ────
def restore_version(version_id, project_root):
    """Switch active version.
    Copies version folder files back to 
    data/processed/ so dashboard shows them."""
    
    from app.database import get_version_by_id
    
    version = get_version_by_id(version_id)
    if not version:
        return False, "Version not found"
    
    folder = version['folder_path']
    if not os.path.exists(folder):
        return False, "Version files missing"
    
    processed = os.path.join(project_root, 'data', 'processed')
    raw_dir = os.path.join(project_root, 'data', 'raw')
    
    # Map version files back to processed/
    restore_map = {
        'raw.csv': os.path.join(raw_dir, 'DataCoSupplyChainDataset.csv'),
        'risk_scored.csv': os.path.join(processed, 'delivery_risk_scored.csv'),
        'forecasts.csv': os.path.join(processed, 'demand_forecast_results.csv'),
        'segments.csv': os.path.join(processed, 'customer_segments.csv')
    }
    
    restored = []
    for src_name, dest_path in restore_map.items():
        src = os.path.join(folder, src_name)
        if os.path.exists(src):
            shutil.copy2(src, dest_path)
            restored.append(src_name)
    
    # Update active version in DB
    set_active_version(version_id)
    
    return True, f"Restored {len(restored)} files from {version['version_number']}"

# ── Get version comparison ────────────
def compare_versions(v1_id, v2_id):
    """Compare stats between two versions."""
    from app.database import query_version_stats
    
    v1_stats = query_version_stats(v1_id)
    v2_stats = query_version_stats(v2_id)
    
    return {
        'v1': v1_stats,
        'v2': v2_stats,
        'changes': {
            'orders': (v2_stats.get('total_orders', 0) - v1_stats.get('total_orders', 0)),
            'revenue': (v2_stats.get('total_revenue', 0) - v1_stats.get('total_revenue', 0)),
            'late_rate': (v2_stats.get('late_rate', 0) - v1_stats.get('late_rate', 0))
        }
    }