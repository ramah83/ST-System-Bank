
"""
Script to create sample test data for test dashboard
"""
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from test_dashboard.models import TestRun, TestCase, TestNotification

def create_sample_data():
    """Create sample test data"""
    print("Creating sample test data...")
    

    TestRun.objects.all().delete()
    

    test_runs = []
    

    run1 = TestRun.objects.create(
        name="Banking System Tests - Full Suite",
        status="passed",
        start_time=timezone.now() - timedelta(hours=2),
        end_time=timezone.now() - timedelta(hours=1, minutes=45),
        duration=900.5,  # 15 minutes
        total_tests=45,
        passed_tests=43,
        failed_tests=2,
        error_tests=0,
        coverage_percentage=87.5
    )
    test_runs.append(run1)
    

    run2 = TestRun.objects.create(
        name="Authentication Tests",
        status="failed",
        start_time=timezone.now() - timedelta(days=1, hours=3),
        end_time=timezone.now() - timedelta(days=1, hours=2, minutes=30),
        duration=1800.2,  # 30 minutes
        total_tests=25,
        passed_tests=20,
        failed_tests=4,
        error_tests=1,
        coverage_percentage=82.1
    )
    test_runs.append(run2)
    

    run3 = TestRun.objects.create(
        name="Transaction Processing Tests",
        status="running",
        start_time=timezone.now() - timedelta(minutes=10),
        total_tests=30,
        passed_tests=25,
        failed_tests=0,
        error_tests=0,
        coverage_percentage=None
    )
    test_runs.append(run3)
    

    run4 = TestRun.objects.create(
        name="Account Management Tests",
        status="passed",
        start_time=timezone.now() - timedelta(days=2, hours=1),
        end_time=timezone.now() - timedelta(days=2, hours=0, minutes=45),
        duration=900.0,
        total_tests=35,
        passed_tests=35,
        failed_tests=0,
        error_tests=0,
        coverage_percentage=92.3
    )
    test_runs.append(run4)
    

    TestCase.objects.create(
        test_run=run2,
        name="test_user_login_invalid_credentials",
        class_name="TestAuthentication",
        module_name="tests.test_authentication",
        status="failed",
        duration=2.5,
        error_message="AssertionError: Expected login to fail but it succeeded",
        traceback="Traceback (most recent call last):\n  File 'test_auth.py', line 45, in test_login\n    self.assertFalse(result)\nAssertionError: Expected login to fail"
    )
    
    TestCase.objects.create(
        test_run=run2,
        name="test_password_reset_flow",
        class_name="TestAuthentication", 
        module_name="tests.test_authentication",
        status="failed",
        duration=5.1,
        error_message="TimeoutError: Password reset email not received within 30 seconds",
        traceback="Traceback (most recent call last):\n  File 'test_auth.py', line 78, in test_reset\n    self.wait_for_email()\nTimeoutError: Email timeout"
    )
    
    TestCase.objects.create(
        test_run=run2,
        name="test_session_timeout",
        class_name="TestAuthentication",
        module_name="tests.test_authentication", 
        status="error",
        duration=0.1,
        error_message="ImportError: Module 'session_manager' not found",
        traceback="Traceback (most recent call last):\n  File 'test_auth.py', line 12, in <module>\n    from session_manager import SessionManager\nImportError: No module named 'session_manager'"
    )
    

    for i in range(5):
        TestCase.objects.create(
            test_run=run1,
            name=f"test_banking_operation_{i+1}",
            class_name="TestBankingOperations",
            module_name="tests.test_banking",
            status="passed",
            duration=1.2 + (i * 0.3)
        )
    

    TestNotification.objects.create(
        test_run=run2,
        notification_type="test_failure",
        message="4 tests failed in Authentication Tests suite. Immediate attention required.",
        created_at=timezone.now() - timedelta(days=1, hours=2),
        is_sent=True
    )
    
    TestNotification.objects.create(
        test_run=run2,
        notification_type="coverage_drop", 
        message="Code coverage dropped to 82.1% (below 85% threshold)",
        created_at=timezone.now() - timedelta(days=1, hours=1, minutes=30),
        is_sent=False
    )
    
    TestNotification.objects.create(
        test_run=run1,
        notification_type="test_failure",
        message="2 tests failed in Banking System Tests - Full Suite",
        created_at=timezone.now() - timedelta(hours=1, minutes=45),
        is_sent=True
    )
    
    print(f"Created {len(test_runs)} test runs")
    print(f"Created {TestCase.objects.count()} test cases")
    print(f"Created {TestNotification.objects.count()} notifications")
    print("Sample data creation completed!")

if __name__ == "__main__":
    create_sample_data()