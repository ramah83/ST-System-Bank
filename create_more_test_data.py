
"""
Script to create more comprehensive test data for trends analysis
"""
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from test_dashboard.models import TestRun, TestCase, TestNotification

def create_comprehensive_data():
    """Create comprehensive test data for the last 30 days"""
    print("Creating comprehensive test data for trends analysis...")
    

    TestRun.objects.all().delete()
    

    test_runs = []
    base_date = timezone.now() - timedelta(days=30)
    
    test_suites = [
        "Banking System Tests - Full Suite",
        "Authentication Tests", 
        "Transaction Processing Tests",
        "Account Management Tests",
        "Security Tests",
        "Performance Tests",
        "UI Integration Tests",
        "Database Tests"
    ]
    
    for day in range(30):

        runs_per_day = random.randint(1, 3)
        
        for run_num in range(runs_per_day):
            run_date = base_date + timedelta(days=day, hours=random.randint(8, 18), minutes=random.randint(0, 59))
            

            total_tests = random.randint(20, 60)
            

            base_success_rate = 85 + (day * 0.3)  # Gradual improvement
            success_rate = min(98, max(80, base_success_rate + random.uniform(-5, 5)))
            
            passed_tests = int(total_tests * success_rate / 100)
            failed_tests = random.randint(0, total_tests - passed_tests)
            error_tests = total_tests - passed_tests - failed_tests
            

            base_duration = total_tests * random.uniform(0.8, 2.5)
            duration = base_duration + random.uniform(-base_duration*0.2, base_duration*0.2)
            

            base_coverage = 82 + (day * 0.15)
            coverage = min(95, max(75, base_coverage + random.uniform(-3, 3)))
            

            if failed_tests == 0 and error_tests == 0:
                status = 'passed'
            elif failed_tests > total_tests * 0.1:
                status = 'failed'
            else:
                status = 'passed'
            
            run = TestRun.objects.create(
                name=random.choice(test_suites),
                status=status,
                start_time=run_date,
                end_time=run_date + timedelta(seconds=duration),
                duration=duration,
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                error_tests=error_tests,
                coverage_percentage=coverage
            )
            test_runs.append(run)
            

            if failed_tests > 0 or error_tests > 0:
                create_test_cases_for_run(run, failed_tests, error_tests)
    

    create_notifications(test_runs)
    
    print(f"Created {len(test_runs)} test runs over 30 days")
    print(f"Created {TestCase.objects.count()} test cases")
    print(f"Created {TestNotification.objects.count()} notifications")
    print("Comprehensive test data creation completed!")

def create_test_cases_for_run(test_run, failed_count, error_count):
    """Create test cases for a test run"""
    
    test_modules = [
        'tests.test_authentication',
        'tests.test_transactions', 
        'tests.test_banking',
        'tests.test_accounts',
        'tests.test_security',
        'tests.test_performance',
        'tests.test_ui',
        'tests.test_database'
    ]
    
    test_classes = [
        'TestAuthentication',
        'TestTransactions',
        'TestBankingOperations', 
        'TestAccountManagement',
        'TestSecurity',
        'TestPerformance',
        'TestUI',
        'TestDatabase'
    ]
    
    test_names = [
        'test_user_login_valid_credentials',
        'test_user_login_invalid_credentials',
        'test_password_reset_flow',
        'test_session_timeout',
        'test_deposit_transaction',
        'test_withdrawal_transaction',
        'test_transfer_funds',
        'test_account_balance_check',
        'test_create_new_account',
        'test_update_account_info',
        'test_sql_injection_protection',
        'test_xss_protection',
        'test_csrf_protection',
        'test_load_performance',
        'test_concurrent_users',
        'test_ui_responsiveness',
        'test_database_connection',
        'test_data_integrity'
    ]
    
    error_messages = [
        "AssertionError: Expected login to fail but it succeeded",
        "TimeoutError: Password reset email not received within 30 seconds",
        "ImportError: Module 'session_manager' not found",
        "ConnectionError: Database connection failed",
        "ValidationError: Invalid account number format",
        "PermissionError: Insufficient privileges for operation",
        "ValueError: Invalid transaction amount",
        "IntegrityError: Duplicate account number",
        "AuthenticationError: Invalid credentials provided",
        "NetworkError: API endpoint not responding"
    ]
    

    for i in range(failed_count):
        TestCase.objects.create(
            test_run=test_run,
            name=random.choice(test_names),
            class_name=random.choice(test_classes),
            module_name=random.choice(test_modules),
            status='failed',
            duration=random.uniform(0.5, 5.0),
            error_message=random.choice(error_messages),
            traceback=f"Traceback (most recent call last):\n  File 'test_file.py', line {random.randint(10, 100)}, in test_method\n    {random.choice(error_messages)}"
        )
    

    for i in range(error_count):
        TestCase.objects.create(
            test_run=test_run,
            name=random.choice(test_names),
            class_name=random.choice(test_classes),
            module_name=random.choice(test_modules),
            status='error',
            duration=random.uniform(0.1, 1.0),
            error_message=random.choice(error_messages),
            traceback=f"Traceback (most recent call last):\n  File 'test_file.py', line {random.randint(10, 100)}, in test_method\n    {random.choice(error_messages)}"
        )

def create_notifications(test_runs):
    """Create notifications for significant test failures"""
    
    for run in test_runs:

        if run.failed_tests > run.total_tests * 0.15:  # More than 15% failure
            TestNotification.objects.create(
                test_run=run,
                notification_type="test_failure",
                message=f"{run.failed_tests} tests failed in {run.name}. Failure rate: {(run.failed_tests/run.total_tests)*100:.1f}%",
                created_at=run.end_time + timedelta(minutes=5),
                is_sent=random.choice([True, False])
            )
        

        if run.coverage_percentage and run.coverage_percentage < 85:
            TestNotification.objects.create(
                test_run=run,
                notification_type="coverage_drop",
                message=f"Code coverage dropped to {run.coverage_percentage:.1f}% (below 85% threshold)",
                created_at=run.end_time + timedelta(minutes=10),
                is_sent=random.choice([True, False])
            )

if __name__ == "__main__":
    create_comprehensive_data()