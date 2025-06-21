#!/usr/bin/env python
"""
Test script to verify deployment configuration
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_root = Path(__file__).resolve().parent
sys.path.append(str(project_root))

def test_production_settings():
    """Test production settings"""
    print("Testing production settings...")
    
    # Set environment for production
    os.environ['DJANGO_SETTINGS_MODULE'] = 'OCRtesrect.settings_production'
    os.environ['DATABASE_URL'] = 'postgresql://USER:PASSWORD@HOST.neon.tech/neondb?sslmode=require'
    
    try:
        django.setup()
        from django.conf import settings
        
        print(f"✅ Production settings loaded successfully")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   Database: {settings.DATABASES['default']['ENGINE']}")
        print(f"   Installed Apps: {len(settings.INSTALLED_APPS)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Production settings failed: {e}")
        return False

def test_development_settings():
    """Test development settings"""
    print("\nTesting development settings...")
    
    # Set environment for development
    os.environ['DJANGO_SETTINGS_MODULE'] = 'OCRtesrect.settings_development'
    
    try:
        django.setup()
        from django.conf import settings
        
        print(f"✅ Development settings loaded successfully")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   Database: {settings.DATABASES['default']['ENGINE']}")
        print(f"   Installed Apps: {len(settings.INSTALLED_APPS)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Development settings failed: {e}")
        return False

def test_ocr_view():
    """Test OCR view import"""
    print("\nTesting OCR view...")
    
    try:
        from OCRtesrect.ocrapp.views import ocr_image_view, health_check
        print("✅ OCR views imported successfully")
        return True
        
    except Exception as e:
        print(f"❌ OCR view import failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Django OCR Application Configuration")
    print("=" * 50)
    
    # Test development settings
    dev_ok = test_development_settings()
    
    # Test production settings
    prod_ok = test_production_settings()
    
    # Test OCR views
    ocr_ok = test_ocr_view()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Development Settings: {'✅ PASS' if dev_ok else '❌ FAIL'}")
    print(f"   Production Settings:  {'✅ PASS' if prod_ok else '❌ FAIL'}")
    print(f"   OCR Views:            {'✅ PASS' if ocr_ok else '❌ FAIL'}")
    
    if all([dev_ok, prod_ok, ocr_ok]):
        print("\n🎉 All tests passed! Ready for deployment.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.") 