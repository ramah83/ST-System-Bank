"""
URLs for test dashboard
"""
from django.urls import path
from . import views

app_name = 'test_dashboard'

urlpatterns = [
    path('', views.TestDashboardView.as_view(), name='dashboard'),
    path('run/<int:pk>/', views.TestRunDetailView.as_view(), name='test_run_detail'),
    path('trends/', views.TestTrendsView.as_view(), name='trends'),
    path('notifications/', views.NotificationListView.as_view(), name='notifications'),
    

    path('api/stats/', views.api_test_stats, name='api_stats'),
    path('api/failures/', views.api_recent_failures, name='api_failures'),
    path('api/run-tests/', views.run_tests_api, name='api_run_tests'),
]