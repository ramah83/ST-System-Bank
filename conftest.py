"""
Pytest configuration for Django tests
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner


sys.path.insert(0, os.path.dirname(__file__))

def pytest_configure():
    """Configure Django settings for pytest"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
    django.setup()

def pytest_sessionstart(session):
    """Called after the Session object has been created"""
    pass

def pytest_sessionfinish(session, exitstatus):
    """Called after whole test run finished"""
    pass