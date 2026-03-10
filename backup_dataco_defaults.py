#!/usr/bin/env python3
"""
Backup DataCo processed results as defaults
"""

import os
import shutil
import json

PROJECT_ROOT = r'C:\Users\saakshi.jaiswal\Downloads\Project\supply-chain-analytics'

def backup_dataco_defaults():
    print("🔄 Creating DataCo default backup...")
    
    # Create DataCo default backup folder
    backup_dir = os.path.join(PROJECT_ROOT, 'data', 'defaults', 'dataco')
    os.makedirs(backup_dir, exist_ok=True)
    
    # Copy all processed files
    processed_dir = os.path.join(PROJECT_ROOT, 'data', 'processed')
    if os.path.exists(processed_dir):
        for f in os.listdir(processed_dir):
            if f.endswith('.csv') or f.endswith('.json'):
                src = os.path.join(processed_dir, f)
                dst = os.path.join(backup_dir, f)
                shutil.copy2(src, dst)
                print(f'✅ Backed up: {f}')
    
    # Copy visuals
    visuals_src = os.path.join(PROJECT_ROOT, 'visuals')
    visuals_dst = os.path.join(PROJECT_ROOT, 'data', 'defaults', 'dataco', 'visuals')
    if os.path.exists(visuals_src):
        if os.path.exists(visuals_dst):
            shutil.rmtree(visuals_dst)
        shutil.copytree(visuals_src, visuals_dst)
        print('✅ Backed up visuals')
    
    # Copy models
    models_src = os.path.join(PROJECT_ROOT, 'models')
    models_dst = os.path.join(PROJECT_ROOT, 'data', 'defaults', 'dataco', 'models')
    os.makedirs(models_dst, exist_ok=True)
    if os.path.exists(models_src):
        for f in os.listdir(models_src):
            if f.endswith('.pkl'):
                src = os.path.join(models_src, f)
                dst = os.path.join(models_dst, f)
                shutil.copy2(src, dst)
                print(f'✅ Backed up model: {f}')
    
    # Copy PowerBI data
    powerbi_src = os.path.join(PROJECT_ROOT, 'data', 'powerbi')
    powerbi_dst = os.path.join(PROJECT_ROOT, 'data', 'defaults', 'dataco', 'powerbi')
    if os.path.exists(powerbi_src):
        if os.path.exists(powerbi_dst):
            shutil.rmtree(powerbi_dst)
        shutil.copytree(powerbi_src, powerbi_dst)
        print('✅ Backed up PowerBI data')
    
    print(f'\n✅ DataCo defaults backed up')
    print(f'Location: {backup_dir}')
    
    return backup_dir

if __name__ == "__main__":
    backup_dataco_defaults()