"""
إنشاء حساب أدمن محدود الصلاحيات للبنك
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import User


class Command(BaseCommand):
    help = 'إنشاء حساب أدمن محدود الصلاحيات للبنك'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='البريد الإلكتروني للأدمن')
        parser.add_argument('--password', type=str, help='كلمة المرور')
        parser.add_argument('--first-name', type=str, help='الاسم الأول')
        parser.add_argument('--last-name', type=str, help='الاسم الأخير')
        parser.add_argument('--readonly', action='store_true', help='إنشاء أدمن للقراءة فقط')

    def handle(self, *args, **options):
        email = options.get('email')
        password = options.get('password')
        first_name = options.get('first_name', '')
        last_name = options.get('last_name', '')
        readonly = options.get('readonly', False)
        
        if not email:
            email = input('البريد الإلكتروني: ')
        
        if not password:
            password = input('كلمة المرور: ')
        
        if not first_name:
            first_name = input('الاسم الأول: ')
        
        if not last_name:
            last_name = input('الاسم الأخير: ')
        

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f'المستخدم {email} موجود بالفعل')
            )
            return
        

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,  # للوصول للوحة الإدارة
            is_active=True
        )
        

        if readonly:
            group_name = 'Bank Readonly Admin'
            admin_type = 'للقراءة فقط'
        else:
            group_name = 'Bank Admin'
            admin_type = 'محدود الصلاحيات'
        
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'تم إنشاء أدمن {admin_type} بنجاح!'
                )
            )
            
            self.stdout.write(f'البريد الإلكتروني: {email}')
            self.stdout.write(f'الاسم: {first_name} {last_name}')
            self.stdout.write(f'نوع الأدمن: {admin_type}')
            
            if readonly:
                self.stdout.write('\nالصلاحيات:')
                self.stdout.write('- عرض جميع البيانات فقط')
                self.stdout.write('- لا يمكن إضافة أو تعديل أو حذف أي شيء')
            else:
                self.stdout.write('\nالصلاحيات:')
                self.stdout.write('- عرض وإضافة وتعديل وحذف المستخدمين والحسابات')
                self.stdout.write('- عرض وحذف المعاملات (للتحليل)')
                self.stdout.write('- لا يمكن إضافة أو تعديل معاملات مالية')
                self.stdout.write('- لا يمكن تعديل أرصدة الحسابات مباشرة')
            
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'المجموعة {group_name} غير موجودة. '
                    'قم بتشغيل: python manage.py create_admin_groups أولاً'
                )
            )
            user.delete()  # حذف المستخدم إذا فشل إضافته للمجموعة