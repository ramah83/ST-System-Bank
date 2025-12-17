"""
Management command to create sample test data for dashboard
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import random

from test_dashboard.models import TestRun, TestCase, TestNotification


class Command(BaseCommand):
    help = 'Create sample test data for dashboard demonstration'

    def add_arguments(self, parser):
        parser.add_argument(
            '--runs',
            type=int,
            default=10,
            help='Number of test runs to create'
        )

    def handle(self, *args, **options):
        runs_count = options['runs']
        
        self.stdout.write(f'Creating {runs_count} sample test runs...')
        

        for i in range(runs_count):

            days_ago = random.randint(0, 30)
            start_time = timezone.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
            

            total_tests = random.randint(20, 100)
            passed_tests = random.randint(int(total_tests * 0.7), total_tests)
            failed_tests = random.randint(0, total_tests - passed_tests)
            error_tests = total_tests - passed_tests - failed_tests
            

            duration = random.uniform(30.0, 120.0)
            coverage = random.uniform(75.0, 95.0)
            

            if failed_tests > 0 or error_tests > 0:
                status = 'failed'
            else:
                status = 'passed'
            

            test_run = TestRun.objects.create(
                name=f'Test Run #{i+1} - {start_time.strftime("%Y-%m-%d %H:%M")}',
                status=status,
                start_time=start_time,
                end_time=start_time + timedelta(seconds=duration),
                duration=duration,
                total_tests=total_tests,
                passed_tests=passed_tests,
                failed_tests=failed_tests,
                error_tests=error_tests,
                coverage_percentage=coverage
            )
            

            test_cases_data = [
                ('test_user_login', 'TestAuthentication', 'tests.test_authentication'),
                ('test_user_registration', 'TestAuthentication', 'tests.test_authentication'),
                ('test_deposit_money', 'TestTransactions', 'tests.test_transactions'),
                ('test_withdraw_money', 'TestTransactions', 'tests.test_transactions'),
                ('test_user_search', 'TestSearch', 'tests.test_search_functionality'),
                ('test_transaction_search', 'TestSearch', 'tests.test_search_functionality'),
                ('test_login_flow', 'SeleniumTests', 'tests.test_selenium'),
                ('test_deposit_flow', 'SeleniumTests', 'tests.test_selenium'),
            ]
            
            for case_name, class_name, module_name in test_cases_data:

                if status == 'passed':
                    case_status = 'passed'
                else:
                    case_status = random.choices(
                        ['passed', 'failed', 'error'],
                        weights=[0.8, 0.15, 0.05]
                    )[0]
                
                case_duration = random.uniform(0.1, 5.0)
                error_message = ''
                
                if case_status in ['failed', 'error']:
                    error_messages = [
                        'AssertionError: Expected True but got False',
                        'TimeoutException: Element not found within timeout',
                        'ValidationError: Invalid form data',
                        'ConnectionError: Database connection failed',
                        'AttributeError: Object has no attribute'
                    ]
                    error_message = random.choice(error_messages)
                
                TestCase.objects.create(
                    test_run=test_run,
                    name=case_name,
                    class_name=class_name,
                    module_name=module_name,
                    status=case_status,
                    duration=case_duration,
                    error_message=error_message
                )
            

            if status == 'failed':
                notification_types = ['test_failure']
                if coverage < 80:
                    notification_types.append('coverage_drop')
                
                for notif_type in notification_types:
                    if notif_type == 'test_failure':
                        message = f'Test run failed with {failed_tests} failed tests and {error_tests} errors'
                    else:
                        message = f'Code coverage dropped to {coverage:.1f}%'
                    
                    TestNotification.objects.create(
                        test_run=test_run,
                        notification_type=notif_type,
                        message=message,
                        created_at=start_time + timedelta(minutes=5),
                        is_sent=random.choice([True, False])
                    )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {runs_count} test runs with sample data')
        )