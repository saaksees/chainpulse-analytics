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

def save_version_outputs(version_id, version_folder, project_root):
    import shutil, json
    from datetime import datetime
    
    os.makedirs(version_folder, exist_ok=True)
    
    # Files to copy to version folder
    files_to_copy = {
        'raw_data': os.path.join(project_root, 'data', 'raw'),
        'processed': os.path.join(project_root, 'data', 'processed'),
        'models': os.path.join(project_root, 'models'),
    }
    
    copied = []
    
    # Copy processed CSVs
    processed_src = files_to_copy['processed']
    processed_dst = os.path.join(version_folder, 'processed')
    os.makedirs(processed_dst, exist_ok=True)
    
    if os.path.exists(processed_src):
        for f in os.listdir(processed_src):
            if f.endswith('.csv') or f.endswith('.json'):
                try:
                    shutil.copy2(os.path.join(processed_src, f), os.path.join(processed_dst, f))
                    copied.append(f)
                except Exception as e:
                    print(f'[WARN] Copy {f}: {e}')
    
    # Copy raw CSV
    raw_src = files_to_copy['raw_data']
    raw_dst = os.path.join(version_folder, 'raw')
    os.makedirs(raw_dst, exist_ok=True)
    
    if os.path.exists(raw_src):
        for f in os.listdir(raw_src):
            if f.endswith('.csv'):
                try:
                    shutil.copy2(os.path.join(raw_src, f), os.path.join(raw_dst, f))
                    copied.append(f)
                except Exception as e:
                    print(f'[WARN] Copy raw {f}: {e}')
    
    # Copy models
    models_src = files_to_copy['models']
    models_dst = os.path.join(version_folder, 'models')
    os.makedirs(models_dst, exist_ok=True)
    
    if os.path.exists(models_src):
        for f in os.listdir(models_src):
            if f.endswith('.pkl'):
                try:
                    shutil.copy2(os.path.join(models_src, f), os.path.join(models_dst, f))
                    copied.append(f)
                except Exception as e:
                    print(f'[WARN] Copy model {f}: {e}')
    
    # Save metadata
    metadata = {
        'version_id': version_id,
        'saved_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'files_copied': copied,
        'folder': version_folder
    }
    
    with open(os.path.join(version_folder, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f'[OK] Version {version_id} saved: {len(copied)} files')
    return True

def restore_version(version_id, project_root):
    import shutil
    from app.database import get_version_by_id, set_active_version
    
    version = get_version_by_id(version_id)
    if not version:
        return False, 'Version not found'
    
    folder = version[-1]  # folder_path
    if not os.path.exists(folder):
        return False, f'Version folder missing: {folder}'
    
    # Restore processed files
    processed_src = os.path.join(folder, 'processed')
    processed_dst = os.path.join(project_root, 'data', 'processed')
    
    if os.path.exists(processed_src):
        for f in os.listdir(processed_src):
            try:
                shutil.copy2(os.path.join(processed_src, f), os.path.join(processed_dst, f))
            except Exception as e:
                print(f'[WARN] Restore {f}: {e}')
    
    # Restore models
    models_src = os.path.join(folder, 'models')
    models_dst = os.path.join(project_root, 'models')
    
    if os.path.exists(models_src):
        for f in os.listdir(models_src):
            if f.endswith('.pkl'):
                try:
                    shutil.copy2(os.path.join(models_src, f), os.path.join(models_dst, f))
                except Exception as e:
                    print(f'[WARN] Restore model {f}: {e}')
    
    set_active_version(version_id)
    print(f'[OK] Restored to version {version_id}')
    return True, 'Version restored'

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