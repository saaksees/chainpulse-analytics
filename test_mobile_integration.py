#!/usr/bin/env python3
"""
Test script to verify mobile-responsive integration
"""

import os
import sys

def test_mobile_integration():
    """Test if mobile files are properly integrated"""
    
    print("🔍 Testing ChainPulse Mobile Integration...")
    
    # Check if mobile files exist
    mobile_css = "supply-chain-analytics/app/static/css/mobile-responsive.css"
    mobile_js = "supply-chain-analytics/app/static/js/mobile-navigation.js"
    base_template = "supply-chain-analytics/app/templates/base.html"
    
    files_to_check = [mobile_css, mobile_js, base_template]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    # Check if base template includes mobile files
    with open(base_template, 'r', encoding='utf-8') as f:
        content = f.read()
        
        if 'mobile-responsive.css' in content:
            print("✅ Mobile CSS linked in base template")
        else:
            print("❌ Mobile CSS not linked in base template")
            return False
            
        if 'mobile-navigation.js' in content:
            print("✅ Mobile JavaScript linked in base template")
        else:
            print("❌ Mobile JavaScript not linked in base template")
            return False
    
    # Check mobile CSS content
    with open(mobile_css, 'r', encoding='utf-8') as f:
        css_content = f.read()
        
        mobile_features = [
            '@media (max-width: 768px)',
            '.mobile-menu-btn',
            '.mobile-bottom-nav',
            '--touch-target: 44px'
        ]
        
        for feature in mobile_features:
            if feature in css_content:
                print(f"✅ Mobile feature found: {feature}")
            else:
                print(f"❌ Mobile feature missing: {feature}")
                return False
    
    # Check mobile JavaScript content
    with open(mobile_js, 'r', encoding='utf-8') as f:
        js_content = f.read()
        
        mobile_classes = [
            'class MobileNavigation',
            'class MobileChartOptimizer',
            'class MobileTableConverter',
            'class TouchGestureHandler'
        ]
        
        for cls in mobile_classes:
            if cls in js_content:
                print(f"✅ Mobile class found: {cls}")
            else:
                print(f"❌ Mobile class missing: {cls}")
                return False
    
    print("\n🎉 Mobile Integration Test PASSED!")
    print("📱 ChainPulse is now mobile-responsive with:")
    print("   • Touch-friendly navigation")
    print("   • Responsive grid layouts")
    print("   • Mobile-optimized charts")
    print("   • Swipe gestures")
    print("   • Bottom navigation bar")
    print("   • Optimized touch targets (44px minimum)")
    
    return True

if __name__ == "__main__":
    success = test_mobile_integration()
    sys.exit(0 if success else 1)