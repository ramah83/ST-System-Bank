import os
import sys
from pathlib import Path


PROJECT_NAME = "Banking Management System"
PROJECT_VERSION = "1.0.0"
PYTHON_MIN_VERSION = (3, 8)


PROJECT_ROOT = Path(__file__).parent
APPS = [
    'accounts',
    'core', 
    'transactions',
    'test_dashboard'
]

REQUIRED_FILES = [
    'manage.py',
    'requirements.txt',
    'banking_system/settings.py',
    'banking_system/urls.py',
]

REQUIRED_TEMPLATES = [
    'templates/core/base.html',
    'templates/core/navbar.html',
    'templates/accounts/user_login.html',
    'templates/accounts/user_registration.html',
    'templates/transactions/transaction_form.html',
    'templates/transactions/transaction_report.html',
    'templates/test_dashboard/simple_dashboard.html',
]

OPTIONAL_FILES = [
    'requirements-test.txt',
    'pytest.ini',
    'static/css/admin-enhanced.css',
    'static/css/footer.css',
]


FEATURES = {
    'USER_AUTHENTICATION': True,
    'TRANSACTION_MANAGEMENT': True,
    'SEARCH_FUNCTIONALITY': True,
    'TEST_DASHBOARD': True,
    'ADMIN_INTERFACE': True,
    'ARABIC_LOCALIZATION': True,
    'AUTOMATED_TESTING': True,
}


SYSTEM_REQUIREMENTS = {
    'python_version': PYTHON_MIN_VERSION,
    'django_version': '>=3.2',
    'database': 'SQLite (development) / PostgreSQL (production)',
    'web_server': 'Django development server / Gunicorn + Nginx (production)',
}

def get_system_info():
    """Get system information"""
    return {
        'project_name': PROJECT_NAME,
        'version': PROJECT_VERSION,
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'project_root': str(PROJECT_ROOT),
        'apps': APPS,
        'features': FEATURES,
    }

def check_system_health():
    """Check system health"""
    health = {
        'status': 'healthy',
        'issues': [],
        'warnings': [],
    }
    

    if sys.version_info < PYTHON_MIN_VERSION:
        health['issues'].append(f"Python version {sys.version_info.major}.{sys.version_info.minor} is below minimum {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}")
        health['status'] = 'unhealthy'
    

    for file_path in REQUIRED_FILES:
        if not (PROJECT_ROOT / file_path).exists():
            health['issues'].append(f"Required file missing: {file_path}")
            health['status'] = 'unhealthy'
    

    for template_path in REQUIRED_TEMPLATES:
        if not (PROJECT_ROOT / template_path).exists():
            health['issues'].append(f"Required template missing: {template_path}")
            health['status'] = 'unhealthy'
    

    for file_path in OPTIONAL_FILES:
        if not (PROJECT_ROOT / file_path).exists():
            health['warnings'].append(f"Optional file missing: {file_path}")
    

    for app in APPS:
        app_path = PROJECT_ROOT / app
        if not app_path.exists():
            health['issues'].append(f"App directory missing: {app}")
            health['status'] = 'unhealthy'
        else:

            required_app_files = ['__init__.py', 'models.py', 'views.py']
            for app_file in required_app_files:
                if not (app_path / app_file).exists():
                    health['warnings'].append(f"App file missing: {app}/{app_file}")
    
    return health

if __name__ == '__main__':
    print(f"🏦 {PROJECT_NAME} v{PROJECT_VERSION}")
    print("=" * 50)
    

    info = get_system_info()
    print("📋 System Information:")
    for key, value in info.items():
        if isinstance(value, list):
            print(f"  {key}: {', '.join(value)}")
        elif isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    print()
    

    health = check_system_health()
    print(f"🏥 System Health: {health['status'].upper()}")
    
    if health['issues']:
        print("\n❌ Issues:")
        for issue in health['issues']:
            print(f"  - {issue}")
    
    if health['warnings']:
        print("\n⚠️  Warnings:")
        for warning in health['warnings']:
            print(f"  - {warning}")
    
    if health['status'] == 'healthy' and not health['warnings']:
        print("\n✅ System is fully operational!")
    elif health['status'] == 'healthy':
        print("\n✅ System is operational with minor warnings.")
    else:
        print("\n❌ System has critical issues that need to be resolved.")
    
    print("\n🚀 Quick Start:")
    print("1. python setup_system.py  # Run full setup")
    print("2. python test_system.py   # Test system")
    print("3. python manage.py runserver  # Start server")
    print("4. Visit: http://localhost:8000/")