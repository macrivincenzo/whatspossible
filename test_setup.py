#!/usr/bin/env python3
"""
Test script to validate KDP Research Tool setup
This script checks all dependencies and basic functionality
"""

import sys
import os

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (Compatible)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Requires 3.8+)")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'requests', 'beautifulsoup4', 'pandas', 'matplotlib', 
        'seaborn', 'nltk', 'textblob', 'python-dotenv', 
        'openpyxl', 'lxml', 'fake-useragent', 'click', 'tabulate'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'beautifulsoup4':
                import bs4
                print(f"   ✅ {package} (as bs4)")
            elif package == 'python-dotenv':
                import dotenv
                print(f"   ✅ {package} (as dotenv)")
            elif package == 'fake-useragent':
                import fake_useragent
                print(f"   ✅ {package}")
            else:
                __import__(package)
                print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (Missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("   ✅ All dependencies installed")
        return True

def test_modules():
    """Test custom modules"""
    print("\n🔧 Testing custom modules...")
    
    modules = ['config', 'amazon_scraper', 'keyword_researcher', 'market_analyzer', 'report_generator']
    
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module} - {e}")
            return False
    
    return True

def test_directories():
    """Test required directories"""
    print("\n📁 Testing directories...")
    
    from config import OUTPUT_DIR, REPORTS_DIR, DATA_DIR
    
    directories = [OUTPUT_DIR, REPORTS_DIR, DATA_DIR]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"   ✅ {directory}")
        else:
            print(f"   ⚠️  {directory} (Will be created)")
    
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\n⚡ Testing basic functionality...")
    
    try:
        from kdp_researcher import KDPResearcher
        researcher = KDPResearcher()
        print("   ✅ KDPResearcher initialization")
        
        # Test config access
        from config import MAX_BOOKS_PER_CATEGORY, TARGET_PRICE_RANGE
        print(f"   ✅ Configuration loaded (max books: {MAX_BOOKS_PER_CATEGORY})")
        
        return True
    except Exception as e:
        print(f"   ❌ Basic functionality test failed: {e}")
        return False

def run_all_tests():
    """Run all setup tests"""
    print("🧪 KDP Research Tool Setup Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Custom Modules", test_modules),
        ("Directories", test_directories),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        if result:
            print(f"✅ {test_name}")
            passed += 1
        else:
            print(f"❌ {test_name}")
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Run demo: python demo.py")
        print("2. Check status: python kdp_researcher.py status")
        print("3. Start research: python kdp_researcher.py research")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        if any("Dependencies" in result[0] for result in results if not result[1]):
            print("\nTo fix dependency issues:")
            print("pip install -r requirements.txt")
    
    return failed == 0

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        sys.exit(1)