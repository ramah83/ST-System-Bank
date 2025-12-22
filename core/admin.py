"""
Core admin configuration
"""
from django.contrib import admin
from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule



try:
    admin.site.unregister(PeriodicTask)
    admin.site.unregister(IntervalSchedule)
    admin.site.unregister(CrontabSchedule)
except admin.sites.NotRegistered:
    pass


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(admin.ModelAdmin):
    """Enhanced PeriodicTask admin with Arabic interface"""
    
    list_display = ('name', 'task', 'enabled', 'interval', 'crontab', 'last_run_at')
    list_filter = ('enabled', 'last_run_at')
    search_fields = ('name', 'task')
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name', 'task', 'enabled')
        }),
        ('الجدولة', {
            'fields': ('interval', 'crontab', 'solar', 'clocked')
        }),
        ('إعدادات متقدمة', {
            'fields': ('args', 'kwargs', 'queue', 'exchange', 'routing_key', 'priority', 'expires', 'one_off'),
            'classes': ('collapse',)
        }),
        ('معلومات التشغيل', {
            'fields': ('last_run_at', 'total_run_count', 'date_changed'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('last_run_at', 'total_run_count', 'date_changed')


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(admin.ModelAdmin):
    """Enhanced IntervalSchedule admin with Arabic interface"""
    
    list_display = ('every', 'period')
    list_filter = ('period',)
    
    fieldsets = (
        ('إعدادات الفترة الزمنية', {
            'fields': ('every', 'period')
        }),
    )


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(admin.ModelAdmin):
    """Enhanced CrontabSchedule admin with Arabic interface"""
    
    list_display = ('minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year', 'timezone')
    list_filter = ('timezone',)
    
    fieldsets = (
        ('إعدادات Crontab', {
            'fields': ('minute', 'hour', 'day_of_week', 'day_of_month', 'month_of_year')
        }),
        ('المنطقة الزمنية', {
            'fields': ('timezone',)
        }),
    )