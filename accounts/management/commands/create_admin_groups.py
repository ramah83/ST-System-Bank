"""
إنشاء مجموعات الأدمن مع الصلاحيات المناسبة
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User, UserBankAccount
from transactions.models import Transaction


class Command(BaseCommand):
    help = 'إنشاء مجموعات الأدمن مع الصلاحيات المناسبة'

    def handle(self, *args, **options):

        bank_admin_group, created = Group.objects.get_or_create(
            name='Bank Admin'
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('تم إنشاء مجموعة "Bank Admin"')
            )
        

        user_ct = ContentType.objects.get_for_model(User)
        account_ct = ContentType.objects.get_for_model(UserBankAccount)
        transaction_ct = ContentType.objects.get_for_model(Transaction)
        

        user_permissions = [
            'view_user',
            'add_user', 
            'change_user',
            'delete_user'
        ]
        

        account_permissions = [
            'view_userbankaccount',
            'add_userbankaccount',
            'change_userbankaccount',
            'delete_userbankaccount'
        ]
        

        transaction_permissions = [
            'view_transaction',
            'delete_transaction'  # للتحليل والإدارة
        ]
        

        all_permissions = []
        

        for perm_name in user_permissions:
            try:
                perm = Permission.objects.get(
                    content_type=user_ct,
                    codename=perm_name
                )
                all_permissions.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'الصلاحية {perm_name} غير موجودة')
                )
        

        for perm_name in account_permissions:
            try:
                perm = Permission.objects.get(
                    content_type=account_ct,
                    codename=perm_name
                )
                all_permissions.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'الصلاحية {perm_name} غير موجودة')
                )
        

        for perm_name in transaction_permissions:
            try:
                perm = Permission.objects.get(
                    content_type=transaction_ct,
                    codename=perm_name
                )
                all_permissions.append(perm)
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'الصلاحية {perm_name} غير موجودة')
                )
        

        bank_admin_group.permissions.set(all_permissions)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'تم تطبيق {len(all_permissions)} صلاحية على مجموعة "Bank Admin"'
            )
        )
        

        readonly_admin_group, created = Group.objects.get_or_create(
            name='Bank Readonly Admin'
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('تم إنشاء مجموعة "Bank Readonly Admin"')
            )
        

        readonly_permissions = []
        for ct in [user_ct, account_ct, transaction_ct]:
            try:
                perm = Permission.objects.get(
                    content_type=ct,
                    codename=f'view_{ct.model}'
                )
                readonly_permissions.append(perm)
            except Permission.DoesNotExist:
                pass
        
        readonly_admin_group.permissions.set(readonly_permissions)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'تم تطبيق {len(readonly_permissions)} صلاحية قراءة على مجموعة "Bank Readonly Admin"'
            )
        )
        
        self.stdout.write(
            self.style.SUCCESS('تم إنشاء جميع مجموعات الأدمن بنجاح!')
        )
        

        self.stdout.write('\n' + '='*50)
        self.stdout.write('ملخص الصلاحيات:')
        self.stdout.write('='*50)
        
        self.stdout.write('\n1. Bank Admin:')
        self.stdout.write('   - عرض وإضافة وتعديل وحذف المستخدمين')
        self.stdout.write('   - عرض وإضافة وتعديل وحذف الحسابات (بدون تعديل الأرصدة)')
        self.stdout.write('   - عرض وحذف المعاملات (للتحليل والإدارة)')
        self.stdout.write('   - لا يمكن إضافة أو تعديل معاملات مالية')
        
        self.stdout.write('\n2. Bank Readonly Admin:')
        self.stdout.write('   - عرض جميع البيانات فقط')
        self.stdout.write('   - لا يمكن إضافة أو تعديل أو حذف أي شيء')
        
        self.stdout.write('\n3. Super Admin:')
        self.stdout.write('   - جميع الصلاحيات بما في ذلك حذف المعاملات')
        self.stdout.write('   - الوحيد الذي يمكنه حذف المعاملات المالية')