#!/usr/bin/env python3
"""
Final fix for all emoji characters in all scripts
"""

import os
import re

def fix_emojis_in_file(file_path):
    """Fix all emoji characters in a file"""
    if not os.path.exists(file_path):
        return False
    
    print(f"Fixing emojis in {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Comprehensive emoji replacements
        emoji_map = {
            '📂': '[LOAD]',
            '🚚': '[TRUCK]', 
            '📊': '[CHART]',
            '📝': '[NLP]',
            '📈': '[TREND]',
            '🚨': '[RISK]',
            '👥': '[SEG]',
            '💰': '[MONEY]',
            '🏆': '[TOP]',
            '🔍': '[SEARCH]',
            '📤': '[EXPORT]',
            '✅': '[OK]',
            '❌': '[FAIL]',
            '⚠️': '[WARN]',
            '🔄': '[RUN]',
            '🚀': '[START]',
            '📌': '[PIN]',
            '💯': '[DONE]',
            '🟢': '[GREEN]',
            '🔴': '[RED]',
            '🟡': '[YELLOW]',
            '⭐': '[STAR]',
            '📋': '[PROFILE]',
            '🤖': '[AUTO]',
            '💡': '[TIP]',
            '🔧': '[TOOL]',
            '📁': '[FILES]',
            '📄': '[DOC]',
            '📑': '[PAGES]',
            '🎯': '[TARGET]',
            '✨': '[SPARKLE]',
            '🎉': '[PARTY]',
            '🌐': '[WEB]',
            '📞': '[PHONE]',
            '📧': '[EMAIL]',
            '📮': '[MAILBOX]',
            '📬': '[MAILBOX_WITH_MAIL]',
            '📭': '[MAILBOX_WITHOUT_MAIL]',
            '📫': '[MAILBOX_CLOSED]',
            '📪': '[MAILBOX_LOWERED]',
            '📩': '[ENVELOPE_WITH_ARROW]',
            '📨': '[INCOMING_ENVELOPE]',
            '💌': '[LOVE_LETTER]',
            '📯': '[POSTAL_HORN]',
            '📮': '[POSTBOX]',
            '🗳️': '[BALLOT_BOX]',
            '✏️': '[PENCIL]',
            '✒️': '[BLACK_NIB]',
            '🖋️': '[FOUNTAIN_PEN]',
            '🖊️': '[PEN]',
            '🖌️': '[PAINTBRUSH]',
            '🖍️': '[CRAYON]',
            '📐': '[TRIANGULAR_RULER]',
            '📏': '[STRAIGHT_RULER]',
            '📎': '[PAPERCLIP]',
            '🖇️': '[LINKED_PAPERCLIPS]',
            '📍': '[ROUND_PUSHPIN]',
            '📌': '[PUSHPIN]',
            '🗂️': '[CARD_INDEX_DIVIDERS]',
            '🗒️': '[SPIRAL_NOTEPAD]',
            '🗓️': '[SPIRAL_CALENDAR]',
            '📅': '[CALENDAR]',
            '📆': '[TEAR_OFF_CALENDAR]',
            '🗑️': '[WASTEBASKET]',
            '🔒': '[LOCKED]',
            '🔓': '[UNLOCKED]',
            '🔏': '[LOCKED_WITH_PEN]',
            '🔐': '[LOCKED_WITH_KEY]',
            '🔑': '[KEY]',
            '🗝️': '[OLD_KEY]'
        }
        
        # Apply all replacements
        for emoji, replacement in emoji_map.items():
            content = content.replace(emoji, replacement)
        
        # Remove any remaining high unicode characters in strings
        # This regex finds print statements and replaces non-ASCII chars
        def replace_unicode_in_strings(match):
            full_match = match.group(0)
            # Replace any remaining non-ASCII characters with [SYMBOL]
            cleaned = re.sub(r'[^\x00-\x7F]+', '[SYMBOL]', full_match)
            return cleaned
        
        # Apply to print statements, f-strings, and other string literals
        content = re.sub(r'print\([^)]*\)', replace_unicode_in_strings, content)
        content = re.sub(r'f["\'][^"\']*["\']', replace_unicode_in_strings, content)
        content = re.sub(r'["\'][^"\']*["\']', replace_unicode_in_strings, content)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  [OK] Fixed {file_path}")
        return True
        
    except Exception as e:
        print(f"  [FAIL] Error fixing {file_path}: {e}")
        return False

def main():
    print("FINAL EMOJI FIX FOR ALL SCRIPTS")
    print("=" * 50)
    
    scripts = [
        'scripts/01_eda.py',
        'scripts/02_demand_forecasting.py', 
        'scripts/03_delivery_risk_model.py',
        'scripts/04_rfm_segmentation.py',
        'scripts/05_nlp_analysis.py',
        'scripts/06_export_powerbi_tables.py'
    ]
    
    fixed_count = 0
    for script in scripts:
        if fix_emojis_in_file(script):
            fixed_count += 1
    
    print(f"\n[OK] Fixed {fixed_count}/{len(scripts)} scripts")
    print("All emoji characters should now be Windows-compatible!")

if __name__ == "__main__":
    main()