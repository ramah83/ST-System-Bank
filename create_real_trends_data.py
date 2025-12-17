
"""
Create real test data for trends dashboard
"""
import os
import sys
import django
from pathlib import Path


project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from test_dashboard.models import TestRun, TestCase, TestNotification
from datetime import datetime, timedelta
from django.utils import timezone
import random


def create_real_trends_data():
    """Create realistic test data for trends dashboard"""
    
    print("Creating realistic test data for trends dashboard...")
    

    

    for i in range(14):
        date = timezone.now() - timedelta(days=i)
        

        for j in range(random.randint(2, 4)):
            total_tests = random.randint(45, 85)
            success_rate = random.uniform(0.75, 0.95)
            passed_tests = int(total_tests * success_rate)
            failed_tests = random.randint(0, total_tests - passed_tests)
            error_tests = total_tests - passed_tests - failed_tests
            
            status = 'passed' if failed_tests <= 3 and error_tests <= 2 else 'failed'
            
            test_name = f'اختبار تلقائي - {date.strftime("%Y-%m-%d")} #{j+1}'
            
            test_run = TestRun.objects.create(
                name=test_name,
                status=status,
                start_time=date.replace(hour=random.randint(8, 18), minute=random.randint(0, 59)),
                end_time=date.replace(hour=random.randint(8, 18), minute=random.randint(0, 59)),
                duration=random.uniform(25, 120),
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                error_tests=error_tests,
                coverage_percentage=random.uniform(75, 95)
            )
            

            if status == 'failed' and failed_tests > 0:
                test_modules = [
                    'test_authentication', 'test_transactions', 'test_accounts', 
                    'test_security', 'test_performance', 'test_ui'
                ]
                
                for k in range(min(failed_tests, 5)):  # Create up to 5 failed test cases
                    TestCase.objects.create(
                        test_run=test_run,
                        name=f'test_function_{k+1}',
                        class_name=f'TestClass{k+1}',
                        module_name=random.choice(test_modules),
                        status='failed',
                        duration=random.uniform(0.5, 5.0),
                        error_message=f'AssertionError: Test failed in {test_name}'
                    )
    

    failed_runs = TestRun.objects.filter(status='failed')[:5]
    for run in failed_runs:
        TestNotification.objects.create(
            test_run=run,
            notification_type='test_failure',
            message=f'فشل في الاختبار: {run.failed_tests} اختبار فشل في {run.name}',
            is_sent=False
        )
    
    total_runs = TestRun.objects.count()
    total_cases = TestCase.objects.count()
    total_notifications = TestNotification.objects.count()
    
    print(f"Created {total_runs} test runs")
    print(f"Created {total_cases} test cases")
    print(f"Created {total_notifications} notifications")
    print("Real test data creation completed!")


if __name__ == '__main__':
    create_real_trends_data()