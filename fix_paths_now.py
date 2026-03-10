#!/usr/bin/env python3
"""Quick fix for all remaining scripts"""
import os
import re

scripts_to_fix = [
    'scripts/04_rfm_segmentation.py',
    'scripts/05_nlp_analysis.py',
    'scripts/06_export_powerbi_tables.py'
]

project_root = os.path.dirname(os.path.abspath(__file__))

for script_rel in scripts_to_fix:
    script_path = os.path.join(project_root, script_rel)
    
    if not os.path.exists(script_path):
        print(f"❌ Not found: {script_path}")
        continue
    
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Add path setup at the beginning of main() or after imports if no main()
    if "script_dir = os.path.dirname(os.path.abspath(__file__))" not in content:
        # Find first print statement or first code line after imports
        lines = content.split('\n')
        insert_line = 0
        
        # Find where to insert (after imports and docstring)
        in_docstring = False
        for i, line in enumerate(lines):
            if '"""' in line or "'''" in line:
                in_docstring = not in_docstring
            elif not in_docstring and line.strip() and not line.startswith('import') and not line.startswith('from'):
                insert_line = i
                break
        
        path_setup = """
# Get project root (parent of scripts directory)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
"""
        lines.insert(insert_line, path_setup)
        content = '\n'.join(lines)
    
    # Replace all relative paths
    replacements = [
        (r"'\.\.\/data\/raw\/", "os.path.join(project_root, 'data', 'raw', '"),
        (r'"\.\.\/data\/raw\/', 'os.path.join(project_root, "data", "raw", "'),
        (r"'\.\.\/data\/processed\/", "os.path.join(project_root, 'data', 'processed', '"),
        (r'"\.\.\/data\/processed\/', 'os.path.join(project_root, "data", "processed", "'),
        (r"'\.\.\/visuals\/", "os.path.join(project_root, 'visuals', '"),
        (r'"\.\.\/visuals\/', 'os.path.join(project_root, "visuals", "'),
        (r"'\.\.\/models\/", "os.path.join(project_root, 'models', '"),
        (r'"\.\.\/models\/', 'os.path.join(project_root, "models", "'),
        (r"'\.\.\/data\/powerbi\/", "os.path.join(project_root, 'data', 'powerbi', '"),
        (r'"\.\.\/data\/powerbi\/', 'os.path.join(project_root, "data", "powerbi", "'),
    ]
    
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    if content != original:
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Fixed: {script_rel}")
    else:
        print(f"⏭️  Already fixed: {script_rel}")

print("\n✅ All scripts updated!")
