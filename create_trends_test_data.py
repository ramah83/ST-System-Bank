
"""
Create test data for trends dashboard
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from django.utils import timezone
from test_dashboard.models import TestRun, TestCase, TestNotification

def create_test_runs():
    """Create sample test runs for the last 14 days"""
    
    print("Creating test runs for trends dashboard...")
    

    TestRun.objects.all().delete()
    TestCase.objects.all().delete()
    TestNotification.objects.all().delete()
    

    base_date = timezone.now() - timedelta(days=14)
    
    test_modules = [
        'test_authentication',
        'test_transactions', 
        'test_accounts',
        'test_security',
        'test_performance',
        'test_ui',
        'test_database'
    ]
    
    for i in range(14):
        run_date = base_date + timedelta(days=i)
        

        runs_per_day = random.randint(1, 3)
        
        for run_num in range(runs_per_day):

            total_tests = random.randint(20, 50)
            success_rate = random.uniform(85, 98)  # 85-98% success rate
            
            passed_tests = int(total_tests * (success_rate / 100))
            failed_tests = random.randint(0, total_tests - passed_tests)
            error_tests = total_tests - passed_tests - failed_tests
            

            if failed_tests == 0 and error_tests == 0:
                status = 'passed'
            elif failed_tests > total_tests * 0.1:  # More than 10% failure
                status = 'failed'
            else:
                status = 'passed'
            

            duration = random.uniform(25, 65)  # 25-65 seconds
            coverage = random.uniform(82, 94)  # 82-94% coverage
            
            test_run = TestRun.objects.create(
                name=f'اختبار يومي {run_date.strftime("%Y-%m-%d")} - الجولة {run_num + 1}',
                status=status,
                start_time=run_date.replace(
                    hour=random.randint(8, 18),
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                ),
                end_time=run_date.replace(
                    hour=random.randint(8, 18),
                    minute=random.randint(0, 59),
                    second=random.randint(0, 59)
                ) + timedelta(seconds=duration),
                duration=duration,
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                error_tests=error_tests,
                coverage_percentage=coverage
            )
            

            for test_num in range(total_tests):
                module = random.choice(test_modules)
                test_name = f'test_{random.choice(["login", "transfer", "balance", "security", "validation"])}_{test_num}'
                

                if test_num < passed_tests:
                    test_status = 'passed'
                    error_message = ''
                elif test_num < passed_tests + failed_tests:
                    test_status = 'failed'
                    error_message = f'AssertionError: Expected value did not match actual value in {test_name}'
                else:
                    test_status = 'error'
                    error_message = f'RuntimeError: Unexpected error occurred in {test_name}'
                
                TestCase.objects.create(
                    test_run=test_run,
                    name=test_name,
                    class_name=f'{module}.{test_name.title()}TestCase',
                    module_name=module,
                    status=test_status,
                    duration=random.uniform(0.1, 2.0),
                    error_message=error_message
                )
            

            if status == 'failed' and (failed_tests > 0 or error_tests > 0):
                TestNotification.objects.create(
                    test_run=test_run,
                    notification_type='test_failure',
                    message=f'{failed_tests + error_tests} اختبار فشل في {test_run.name}',
                    created_at=test_run.end_time,
                    is_sent=False
                )
    
    print(f"Created {TestRun.objects.count()} test runs")
    print(f"Created {TestCase.objects.count()} test cases")
    print(f"Created {TestNotification.objects.count()} notifications")
    print("Test data creation completed!")

if __name__ == '__main__':
    create_test_runs()