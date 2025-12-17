
"""
Test runner script with dashboard integration
"""
import os
import sys
import subprocess
import json
import time
from datetime import datetime
from pathlib import Path


project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')

import django
django.setup()

from test_dashboard.models import TestRun, TestCase, TestNotification


class TestRunner:
    """Custom test runner with dashboard integration"""
    
    def __init__(self):
        self.test_run = None
    
    def run_tests(self, test_type='all'):
        """Run tests and record results"""
        

        self.test_run = TestRun.objects.create(
            name=f"Test Run - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            status='running'
        )
        
        try:
            if test_type == 'unit':
                self._run_unit_tests()
            elif test_type == 'selenium':
                self._run_selenium_tests()
            elif test_type == 'all':
                self._run_all_tests()
            else:
                raise ValueError(f"Unknown test type: {test_type}")
                
        except Exception as e:
            self.test_run.status = 'error'
            self.test_run.save()
            self._create_notification('build_failure', f"Test execution failed: {str(e)}")
            raise
        
        return self.test_run
    
    def _run_unit_tests(self):
        """Run unit tests using pytest"""
        print("Running unit tests...")
        
        start_time = time.time()
        

        cmd = [
            'python', '-m', 'pytest',
            'tests/test_authentication.py',
            'tests/test_transactions.py',
            'tests/test_search_functionality.py',
            '--json-report',
            '--json-report-file=test_results.json',
            '--cov=.',
            '--cov-report=json',
            '-v'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        end_time = time.time()
        duration = end_time - start_time
        

        self._parse_pytest_results('test_results.json', duration)
        

        self._parse_coverage_results()
        
        print(f"Unit tests completed in {duration:.2f} seconds")
    
    def _run_selenium_tests(self):
        """Run Selenium tests"""
        print("Running Selenium tests...")
        
        start_time = time.time()
        
        cmd = [
            'python', '-m', 'pytest',
            'tests/test_selenium.py',
            '--json-report',
            '--json-report-file=selenium_results.json',
            '-v'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        end_time = time.time()
        duration = end_time - start_time
        

        self._parse_pytest_results('selenium_results.json', duration)
        
        print(f"Selenium tests completed in {duration:.2f} seconds")
    
    def _run_all_tests(self):
        """Run all tests"""
        print("Running all tests...")
        
        start_time = time.time()
        
        cmd = [
            'python', '-m', 'pytest',
            'tests/',
            '--json-report',
            '--json-report-file=all_results.json',
            '--cov=.',
            '--cov-report=json',
            '-v'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        end_time = time.time()
        duration = end_time - start_time
        

        self._parse_pytest_results('all_results.json', duration)
        

        self._parse_coverage_results()
        
        print(f"All tests completed in {duration:.2f} seconds")
    
    def _parse_pytest_results(self, results_file, duration):
        """Parse pytest JSON results"""
        
        if not os.path.exists(results_file):
            print(f"Results file {results_file} not found")
            return
        
        try:
            with open(results_file, 'r') as f:
                data = json.load(f)
            

            self.test_run.duration = duration
            self.test_run.end_time = datetime.now()
            

            summary = data.get('summary', {})
            self.test_run.total_tests = summary.get('total', 0)
            self.test_run.passed_tests = summary.get('passed', 0)
            self.test_run.failed_tests = summary.get('failed', 0)
            self.test_run.error_tests = summary.get('error', 0)
            

            if self.test_run.failed_tests > 0 or self.test_run.error_tests > 0:
                self.test_run.status = 'failed'
                self._create_notification(
                    'test_failure',
                    f"Test run failed: {self.test_run.failed_tests} failed, {self.test_run.error_tests} errors"
                )
            else:
                self.test_run.status = 'passed'
            
            self.test_run.save()
            

            for test in data.get('tests', []):
                TestCase.objects.create(
                    test_run=self.test_run,
                    name=test.get('nodeid', ''),
                    class_name=test.get('keywords', {}).get('class', ''),
                    module_name=test.get('keywords', {}).get('module', ''),
                    status=test.get('outcome', 'unknown'),
                    duration=test.get('duration', 0),
                    error_message=test.get('call', {}).get('longrepr', '') if test.get('outcome') in ['failed', 'error'] else '',
                )
            
        except Exception as e:
            print(f"Error parsing results: {e}")
    
    def _parse_coverage_results(self):
        """Parse coverage results"""
        
        coverage_file = 'coverage.json'
        if not os.path.exists(coverage_file):
            return
        
        try:
            with open(coverage_file, 'r') as f:
                data = json.load(f)
            

            totals = data.get('totals', {})
            if 'percent_covered' in totals:
                self.test_run.coverage_percentage = totals['percent_covered']
                self.test_run.save()
                

                previous_runs = TestRun.objects.filter(
                    coverage_percentage__isnull=False
                ).exclude(id=self.test_run.id).order_by('-start_time')[:5]
                
                if previous_runs:
                    avg_previous_coverage = sum(run.coverage_percentage for run in previous_runs) / len(previous_runs)
                    if self.test_run.coverage_percentage < avg_previous_coverage - 5:  # 5% drop threshold
                        self._create_notification(
                            'coverage_drop',
                            f"Coverage dropped to {self.test_run.coverage_percentage:.1f}% (avg was {avg_previous_coverage:.1f}%)"
                        )
        
        except Exception as e:
            print(f"Error parsing coverage: {e}")
    
    def _create_notification(self, notification_type, message):
        """Create a test notification"""
        
        TestNotification.objects.create(
            test_run=self.test_run,
            notification_type=notification_type,
            message=message
        )


def main():
    """Main function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Run tests with dashboard integration')
    parser.add_argument(
        '--type',
        choices=['unit', 'selenium', 'all'],
        default='all',
        help='Type of tests to run'
    )
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    try:
        test_run = runner.run_tests(args.type)
        print(f"\nTest run completed: {test_run.name}")
        print(f"Status: {test_run.status}")
        print(f"Total tests: {test_run.total_tests}")
        print(f"Passed: {test_run.passed_tests}")
        print(f"Failed: {test_run.failed_tests}")
        print(f"Errors: {test_run.error_tests}")
        if test_run.coverage_percentage:
            print(f"Coverage: {test_run.coverage_percentage:.1f}%")
        print(f"Duration: {test_run.duration:.2f} seconds")
        

        print(f"\nView results at: http://localhost:8000/test-dashboard/")
        
    except Exception as e:
        print(f"Test execution failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()