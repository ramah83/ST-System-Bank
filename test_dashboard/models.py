"""
Models for test dashboard
"""
from django.db import models
from django.utils import timezone


class TestRun(models.Model):
    """Model to store test run information"""
    
    STATUS_CHOICES = [
        ('running', 'Running'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('error', 'Error'),
    ]
    
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)  
    total_tests = models.IntegerField(default=0)
    passed_tests = models.IntegerField(default=0)
    failed_tests = models.IntegerField(default=0)
    error_tests = models.IntegerField(default=0)
    coverage_percentage = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.name} - {self.status}"
    
    @property
    def success_rate(self):
        """Calculate success rate percentage"""
        if self.total_tests == 0:
            return 0
        return (self.passed_tests / self.total_tests) * 100


class TestCase(models.Model):
    """Model to store individual test case results"""
    
    STATUS_CHOICES = [
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('error', 'Error'),
        ('skipped', 'Skipped'),
    ]
    
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE, related_name='test_cases')
    name = models.CharField(max_length=300)
    class_name = models.CharField(max_length=200)
    module_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    duration = models.FloatField(default=0.0)  
    error_message = models.TextField(blank=True)
    traceback = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.status}"


class TestNotification(models.Model):
    """Model to store test failure notifications"""
    
    NOTIFICATION_TYPES = [
        ('test_failure', 'Test Failure'),
        ('build_failure', 'Build Failure'),
        ('coverage_drop', 'Coverage Drop'),
    ]
    
    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_sent = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} - {self.test_run.name}"