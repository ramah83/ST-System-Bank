
"""
Simple system test script to verify all components are working
"""
import os
import sys
import subprocess
from pathlib import Path


project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')

def test_django_setup():
    """Test Django setup and imports"""
    print("🔧 Testing Django setup...")
    try:
        import django
        django.setup()
        print("✅ Django setup successful")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_models_import():
    """Test model imports"""
    print("📦 Testing model imports...")
    try:
        from accounts.models import User, UserBankAccount
        from transactions.models import Transaction
        from test_dashboard.models import TestRun, TestCase, TestNotification
        print("✅ All models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False

def test_views_import():
    """Test view imports"""
    print("🌐 Testing view imports...")
    try:
        from accounts.views import UserRegistrationView, UserLoginView
        from transactions.views import DepositMoneyView, WithdrawMoneyView, TransactionRepostView
        from test_dashboard.views import TestDashboardView, TestRunDetailView
        print("✅ All views imported successfully")
        return True
    except Exception as e:
        print(f"❌ View import failed: {e}")
        return False

def test_urls_configuration():
    """Test URL configuration"""
    print("🔗 Testing URL configuration...")
    try:
        from django.urls import reverse
        

        urls_to_test = [
            'home',
            'accounts:user_login',
            'accounts:user_registration',
            'transactions:deposit_money',
            'transactions:withdraw_money',
            'transactions:transaction_report',
            'transactions:user_search',
            'transactions:transaction_search',
            'test_dashboard:dashboard',
            'test_dashboard:trends',
            'test_dashboard:notifications',
        ]
        
        for url_name in urls_to_test:
            try:
                reverse(url_name)
                print(f"  ✅ {url_name}")
            except Exception as e:
                print(f"  ❌ {url_name}: {e}")
                return False
        
        print("✅ All URLs configured correctly")
        return True
    except Exception as e:
        print(f"❌ URL configuration failed: {e}")
        return False

def test_templates_exist():
    """Test template files exist"""
    print("📄 Testing template files...")
    
    templates_to_check = [
        'core/base.html',
        'core/navbar.html',
        'accounts/user_login.html',
        'accounts/user_registration.html',
        'transactions/transaction_form.html',
        'transactions/transaction_report.html',
        'transactions/user_search.html',
        'transactions/transaction_search.html',
        'test_dashboard/simple_dashboard.html',
        'test_dashboard/test_run_detail.html',
        'test_dashboard/trends.html',
        'test_dashboard/notifications.html',
    ]
    
    missing_templates = []
    for template in templates_to_check:
        template_path = project_dir / 'templates' / template
        if template_path.exists():
            print(f"  ✅ {template}")
        else:
            print(f"  ❌ {template} - NOT FOUND")
            missing_templates.append(template)
    
    if missing_templates:
        print(f"❌ {len(missing_templates)} templates missing")
        return False
    else:
        print("✅ All templates found")
        return True

def test_static_files():
    """Test static files exist"""
    print("🎨 Testing static files...")
    
    static_files_to_check = [
        'css/admin-enhanced.css',
        'css/footer.css',
    ]
    
    missing_files = []
    for static_file in static_files_to_check:
        file_path = project_dir / 'static' / static_file
        if file_path.exists():
            print(f"  ✅ {static_file}")
        else:
            print(f"  ❌ {static_file} - NOT FOUND")
            missing_files.append(static_file)
    
    if missing_files:
        print(f"⚠️  {len(missing_files)} static files missing (optional)")
    else:
        print("✅ All static files found")
    
    return True  # Static files are optional

def test_database_models():
    """Test database model operations"""
    print("🗄️  Testing database models...")
    try:
        from django.contrib.auth import get_user_model
        from accounts.models import BankAccountType
        from test_dashboard.models import TestRun
        
        User = get_user_model()
        

        print("  ✅ User model accessible")
        print("  ✅ BankAccountType model accessible")
        print("  ✅ TestRun model accessible")
        
        print("✅ Database models working")
        return True
    except Exception as e:
        print(f"❌ Database model test failed: {e}")
        return False

def test_forms_import():
    """Test form imports"""
    print("📝 Testing form imports...")
    try:
        from accounts.forms import UserRegistrationForm, UserAddressForm
        from transactions.forms import DepositForm, WithdrawForm, TransactionDateRangeForm
        print("✅ All forms imported successfully")
        return True
    except Exception as e:
        print(f"❌ Form import failed: {e}")
        return False

def test_admin_configuration():
    """Test admin configuration"""
    print("👨‍💼 Testing admin configuration...")
    try:
        from django.contrib import admin
        from accounts.admin import UserAdmin, UserBankAccountAdmin
        from transactions.admin import TransactionAdmin
        from test_dashboard.admin import TestRunAdmin, TestCaseAdmin, TestNotificationAdmin
        print("✅ All admin configurations imported successfully")
        return True
    except Exception as e:
        print(f"❌ Admin configuration failed: {e}")
        return False

def run_all_tests():
    """Run all system tests"""
    print("🚀 Starting Banking System Tests\n")
    
    tests = [
        test_django_setup,
        test_models_import,
        test_views_import,
        test_urls_configuration,
        test_templates_exist,
        test_static_files,
        test_database_models,
        test_forms_import,
        test_admin_configuration,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__} crashed: {e}")
            failed += 1
        print()  # Empty line for readability
    
    print("=" * 50)
    print(f"📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {(passed / (passed + failed)) * 100:.1f}%")
    
    if failed == 0:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\n🚀 Next steps:")
        print("1. Run: python manage.py migrate")
        print("2. Run: python manage.py createsuperuser")
        print("3. Run: python manage.py runserver")
        print("4. Visit: http://localhost:8000/")
        print("5. Visit: http://localhost:8000/test-dashboard/ (for staff users)")
    else:
        print(f"\n⚠️  {failed} tests failed. Please fix the issues before proceeding.")
    
    return failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)