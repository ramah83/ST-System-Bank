import os
import django
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from accounts.models import BankAccountType, User, UserBankAccount
from test_dashboard.models import TestRun, TestCase, TestNotification
from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
import random

def setup_all_data():
    """Setup all required data"""
    
    print("🔧 إعداد البيانات الأساسية...")
    
    try:
        savings = BankAccountType.objects.create(
            name='حساب توفير',
            maximum_withdrawal_amount=Decimal('5000.00'),
            annual_interest_rate=Decimal('2.5'),
            interest_calculation_per_year=12
        )
        print('✅ تم إنشاء حساب التوفير')
    except Exception as e:
        print(f'حساب التوفير موجود بالفعل')

    try:
        current = BankAccountType.objects.create(
            name='حساب جاري',
            maximum_withdrawal_amount=Decimal('10000.00'),
            annual_interest_rate=Decimal('1.0'),
            interest_calculation_per_year=4
        )
        print('✅ تم إنشاء الحساب الجاري')
    except Exception as e:
        print(f'الحساب الجاري موجود بالفعل')

    try:
        test_user = User.objects.create_user(
            email='test@example.com',
            password='test123',
            first_name='محمد',
            last_name='أحمد'
        )
        print('✅ تم إنشاء المستخدم التجريبي')
    except Exception as e:
        print(f'المستخدم التجريبي موجود بالفعل')

    print("📊 تم تخطي إنشاء بيانات الاختبارات (استخدم create_test_dashboard_data.py إذا كنت تحتاجها)")
    
    print(f"📊 إجمالي المستخدمين: {User.objects.count()}")
    print(f"📊 إجمالي أنواع الحسابات: {BankAccountType.objects.count()}")
    
    print("🎉 تم إعداد جميع البيانات بنجاح!")

if __name__ == '__main__':
    setup_all_data()