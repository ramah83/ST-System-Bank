#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from accounts.models import User

user = User.objects.get(email='rammah@bank.com')
user.set_password('rammah123')
user.save()
print('تم تعيين كلمة المرور: admin123')