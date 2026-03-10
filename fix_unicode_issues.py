#!/usr/bin/env python3
"""
Fix Unicode/Emoji issues in all scripts for Windows compatibility
"""

import os
import re

def fix_unicode_in_file(file_path):
    """Remove emoji and unicode characters from a Python file"""
    if not os.path.exists(file_path):
        return False
    
    print(f"Fixing {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace common emojis with text equivalents
        emoji_replacements = {
            '🚚': '[TRUCK]',
            '📂': '[FOLDER]',
            '✅': '[OK]',
            '❌': '[ERROR]',
            '⚠️': '[WARNING]',
            '📊': '[CHART]',
            '🔧': '[TOOL]',
            '💰': '[MONEY]',
            '📦': '[PACKAGE]',
            '🔄': '[LOADING]',
            '🤖': '[AI]',
            '🏆': '[TROPHY]',
            '📁': '[FILES]',
            '📈': '[GRAPH]',
            '📉': '[DECLINE]',
            '🎯': '[TARGET]',
            '✨': '[SPARKLE]',
            '🎉': '[PARTY]',
            '💡': '[IDEA]',
            '🌐': '[WEB]',
            '🚀': '[ROCKET]',
            '🔍': '[SEARCH]',
            '📝': '[NOTE]',
            '📋': '[CLIPBOARD]',
            '📄': '[DOCUMENT]',
            '📑': '[PAGES]',
            '📓': '[NOTEBOOK]',
            '📔': '[BOOK]',
            '📕': '[BOOK]',
            '📗': '[BOOK]',
            '📘': '[BOOK]',
            '📙': '[BOOK]',
            '📚': '[BOOKS]',
            '📖': '[OPEN_BOOK]',
            '🔖': '[BOOKMARK]',
            '🏷️': '[LABEL]',
            '💼': '[BRIEFCASE]',
            '📊': '[BAR_CHART]',
            '📈': '[TRENDING_UP]',
            '📉': '[TRENDING_DOWN]',
            '📋': '[CLIPBOARD]',
            '📌': '[PIN]',
            '📍': '[LOCATION]',
            '📎': '[PAPERCLIP]',
            '🖇️': '[LINKED_PAPERCLIPS]',
            '📏': '[RULER]',
            '📐': '[TRIANGULAR_RULER]',
            '✂️': '[SCISSORS]',
            '🗃️': '[CARD_FILE_BOX]',
            '🗄️': '[FILE_CABINET]',
            '🗑️': '[WASTEBASKET]',
            '🔒': '[LOCKED]',
            '🔓': '[UNLOCKED]',
            '🔏': '[LOCKED_WITH_PEN]',
            '🔐': '[LOCKED_WITH_KEY]',
            '🔑': '[KEY]',
            '🗝️': '[OLD_KEY]',
            '🔨': '[HAMMER]',
            '⛏️': '[PICK]',
            '🛠️': '[HAMMER_AND_WRENCH]',
            '🗡️': '[DAGGER]',
            '⚔️': '[CROSSED_SWORDS]',
            '🔫': '[PISTOL]',
            '🏹': '[BOW_AND_ARROW]',
            '🛡️': '[SHIELD]',
            '🔧': '[WRENCH]',
            '🔩': '[NUT_AND_BOLT]',
            '⚙️': '[GEAR]',
            '🗜️': '[CLAMP]',
            '⚖️': '[BALANCE_SCALE]',
            '🔗': '[LINK]',
            '⛓️': '[CHAINS]',
            '🧰': '[TOOLBOX]',
            '🧲': '[MAGNET]',
            '⚗️': '[ALEMBIC]'
        }
        
        # Apply replacements
        for emoji, replacement in emoji_replacements.items():
            content = content.replace(emoji, replacement)
        
        # Remove any remaining non-ASCII characters in print statements
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            if 'print(' in line or 'print "' in line:
                # Remove any remaining non-ASCII characters from print statements
                line = re.sub(r'[^\x00-\x7F]+', '[SYMBOL]', line)
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  Fixed {file_path}")
        return True
        
    except Exception as e:
        print(f"  Error fixing {file_path}: {e}")
        return False

def main():
    print("Fixing Unicode issues in all scripts...")
    print("=" * 50)
    
    # List of script files to fix
    script_files = [
        'scripts/01_eda.py',
        'scripts/02_demand_forecasting.py',
        'scripts/03_delivery_risk_model.py',
        'scripts/04_rfm_segmentation.py',
        'scripts/05_nlp_analysis.py',
        'scripts/06_export_powerbi_tables.py'
    ]
    
    fixed_count = 0
    for script_file in script_files:
        if fix_unicode_in_file(script_file):
            fixed_count += 1
    
    print(f"\nFixed {fixed_count}/{len(script_files)} scripts")
    print("Unicode issues should now be resolved!")

if __name__ == "__main__":
    main()