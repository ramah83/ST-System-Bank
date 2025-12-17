
"""
System setup script for Banking Management System
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        if e.stdout:
            print(f"   Output: {e.stdout.strip()}")
        return False

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not supported. Need Python 3.8+")
        return False

def check_virtual_environment():
    """Check if virtual environment is active"""
    print("🔍 Checking virtual environment...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is active")
        return True
    else:
        print("⚠️  Virtual environment not detected. It's recommended to use a virtual environment.")
        response = input("Continue anyway? (y/N): ")
        return response.lower() == 'y'

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing requirements...")
    

    if not run_command("pip install -r requirements.txt", "Installing main requirements"):
        return False
    

    if Path("requirements-test.txt").exists():
        response = input("Install test requirements? (Y/n): ")
        if response.lower() != 'n':
            run_command("pip install -r requirements-test.txt", "Installing test requirements")
    
    return True

def setup_database():
    """Setup database"""
    print("🗄️  Setting up database...")
    

    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return False
    

    if not run_command("python manage.py migrate", "Applying migrations"):
        return False
    
    return True

def create_superuser():
    """Create superuser"""
    print("👤 Creating superuser...")
    response = input("Create superuser now? (Y/n): ")
    if response.lower() != 'n':
        try:
            subprocess.run("python manage.py createsuperuser", shell=True, check=True)
            print("✅ Superuser created successfully")
        except subprocess.CalledProcessError:
            print("⚠️  Superuser creation skipped or failed")
    return True

def collect_static_files():
    """Collect static files"""
    print("🎨 Collecting static files...")
    return run_command("python manage.py collectstatic --noinput", "Collecting static files")

def create_sample_data():
    """Create sample test data"""
    print("📊 Creating sample data...")
    response = input("Create sample test dashboard data? (Y/n): ")
    if response.lower() != 'n':
        return run_command(
            "python manage.py create_sample_test_data --runs 5", 
            "Creating sample test data"
        )
    return True

def run_system_test():
    """Run system test"""
    print("🧪 Running system test...")
    response = input("Run system test to verify setup? (Y/n): ")
    if response.lower() != 'n':
        return run_command("python test_system.py", "Running system test")
    return True

def main():
    """Main setup function"""
    print("🏦 Banking Management System Setup")
    print("=" * 40)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Checking virtual environment", check_virtual_environment),
        ("Installing requirements", install_requirements),
        ("Setting up database", setup_database),
        ("Creating superuser", create_superuser),
        ("Collecting static files", collect_static_files),
        ("Creating sample data", create_sample_data),
        ("Running system test", run_system_test),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 Step: {step_name}")
        if not step_func():
            print(f"\n❌ Setup failed at step: {step_name}")
            print("Please fix the issue and run the setup again.")
            return False
        print()
    
    print("🎉 Setup completed successfully!")
    print("\n🚀 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://localhost:8000/")
    print("3. Login with your superuser account")
    print("4. Visit: http://localhost:8000/admin/ (admin panel)")
    print("5. Visit: http://localhost:8000/test-dashboard/ (test dashboard)")
    
    print("\n📚 Additional commands:")
    print("- Run tests: python run_tests.py")
    print("- Create test data: python manage.py create_sample_test_data")
    print("- System test: python test_system.py")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)