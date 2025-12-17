"""
Admin configuration for test dashboard
"""
from django.contrib import admin
from .models import TestRun, TestCase, TestNotification


@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    """Admin for TestRun model"""
    
    list_display = [
        'name', 'status', 'start_time', 'duration', 
        'total_tests', 'passed_tests', 'failed_tests', 'coverage_percentage'
    ]
    list_filter = ['status', 'start_time']
    search_fields = ['name']
    readonly_fields = ['start_time', 'end_time']
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name', 'status')
        }),
        ('التوقيت', {
            'fields': ('start_time', 'end_time', 'duration')
        }),
        ('نتائج الاختبار', {
            'fields': ('total_tests', 'passed_tests', 'failed_tests', 'error_tests')
        }),
        ('التغطية', {
            'fields': ('coverage_percentage',)
        }),
    )
    
    def has_add_permission(self, request):
        """منع إضافة تشغيل اختبار يدوياً - يتم إنشاؤها تلقائياً"""
        return False


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    """Admin for TestCase model"""
    
    list_display = ['name', 'class_name', 'status', 'duration', 'test_run']
    list_filter = ['status', 'test_run__start_time']
    search_fields = ['name', 'class_name', 'module_name']
    readonly_fields = ['test_run']
    
    fieldsets = (
        ('معلومات الاختبار', {
            'fields': ('test_run', 'name', 'class_name', 'module_name')
        }),
        ('النتائج', {
            'fields': ('status', 'duration')
        }),
        ('تفاصيل الأخطاء', {
            'fields': ('error_message', 'traceback'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """منع إضافة حالة اختبار يدوياً - يتم إنشاؤها تلقائياً"""
        return False


@admin.register(TestNotification)
class TestNotificationAdmin(admin.ModelAdmin):
    """Admin for TestNotification model"""
    
    list_display = ['notification_type', 'test_run', 'created_at', 'is_sent']
    list_filter = ['notification_type', 'is_sent', 'created_at']
    search_fields = ['message']
    readonly_fields = ['test_run', 'created_at']
    
    fieldsets = (
        ('تفاصيل الإشعار', {
            'fields': ('test_run', 'notification_type', 'message')
        }),
        ('الحالة', {
            'fields': ('is_sent', 'created_at')
        }),
    )
    
    def has_add_permission(self, request):
        """منع إضافة إشعار يدوياً - يتم إنشاؤها تلقائياً"""
        return False