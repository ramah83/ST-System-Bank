"""
App configuration for test dashboard
"""
from django.apps import AppConfig


class TestDashboardConfig(AppConfig):
    """Configuration for test dashboard app"""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_dashboard'
    verbose_name = 'Test Dashboard'