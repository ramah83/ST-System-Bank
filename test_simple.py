
"""
Simple test to verify the test dashboard functionality
"""
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from test_dashboard.models import TestRun, TestCase, TestNotification

def test_dashboard_functionality():
    """Test basic dashboard functionality"""
    print("Testing dashboard functionality...")
    
    try:

        test_run = TestRun.objects.create(
            name="Simple Test Run",
            status='running',
            start_time=timezone.now(),
            total_tests=5,
            passed_tests=0,
            failed_tests=0,
            error_tests=0
        )
        print("✅ Test run created successfully")
        

        test_run.status = 'passed'
        test_run.end_time = timezone.now()
        test_run.duration = 10.5
        test_run.passed_tests = 4
        test_run.failed_tests = 1
        test_run.coverage_percentage = 88.5
        test_run.save()
        print("✅ Test run updated successfully")
        

        TestCase.objects.create(
            test_run=test_run,
            name="test_simple_function",
            class_name="TestSimple",
            module_name="tests.test_simple",
            status='passed',
            duration=2.1
        )
        
        TestCase.objects.create(
            test_run=test_run,
            name="test_failing_function",
            class_name="TestSimple", 
            module_name="tests.test_simple",
            status='failed',
            duration=1.5,
            error_message="AssertionError: Expected True but got False",
            traceback="Traceback (most recent call last):\n  File 'test.py', line 10, in test_failing_function\n    self.assertTrue(False)\nAssertionError: Expected True but got False"
        )
        print("✅ Test cases created successfully")
        

        TestNotification.objects.create(
            test_run=test_run,
            notification_type='test_failure',
            message='1 test failed in Simple Test Run',
            created_at=timezone.now(),
            is_sent=False
        )
        print("✅ Notification created successfully")
        

        total_runs = TestRun.objects.count()
        total_cases = TestCase.objects.count()
        total_notifications = TestNotification.objects.count()
        
        print(f"📊 Database status:")
        print(f"   - Total test runs: {total_runs}")
        print(f"   - Total test cases: {total_cases}")
        print(f"   - Total notifications: {total_notifications}")
        
        print("\n🎉 All tests passed! Dashboard should work correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_dashboard_functionality()
    sys.exit(0 if success else 1)