"""
إزالة الحسابات البنكية من حسابات الأدمن
الأدمن لا يجب أن يكون له حساب بنكي - مخصص للإدارة فقط
"""
from django.core.management.base import BaseCommand
from accounts.models import User, UserBankAccount


class Command(BaseCommand):
    help = 'إزالة الحسابات البنكية من جميع حسابات الأدمن'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='عرض الحسابات التي سيتم حذفها دون حذفها فعلياً'
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        

        admin_users = User.objects.filter(
            is_staff=True
        ).exclude(
            account__isnull=True
        )
        
        if not admin_users.exists():
            self.stdout.write(
                self.style.SUCCESS('لا توجد حسابات بنكية للأدمن')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(
                f'تم العثور على {admin_users.count()} أدمن لديهم حسابات بنكية'
            )
        )
        
        for user in admin_users:
            account = user.account
            self.stdout.write(
                f'  - {user.email}: حساب رقم {account.account_no}, رصيد: ${account.balance}'
            )
            
            if not dry_run:
                account.delete()
                self.stdout.write(
                    self.style.SUCCESS(f'  ✓ تم حذف الحساب البنكي لـ {user.email}')
                )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    '\nهذا كان dry-run. لتطبيق التغييرات، قم بتشغيل الأمر بدون --dry-run'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nتم حذف جميع الحسابات البنكية للأدمن بنجاح!'
                )
            )
