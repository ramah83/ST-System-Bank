from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Sum
from django.template.response import TemplateResponse
from django.urls import path
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils.html import format_html

from .models import BankAccountType, User, UserAddress, UserBankAccount
from transactions.models import Transaction


try:
    from django.contrib.auth.models import User as DefaultUser
    admin.site.unregister(DefaultUser)
except admin.sites.NotRegistered:
    pass
except Exception:
    pass


try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


admin.site.site_header = "لوحة إدارة النظام المصرفي"
admin.site.site_title = "إدارة البنك"
admin.site.index_title = "مرحباً بك في لوحة إدارة النظام المصرفي"


class RestrictedAdminMixin:
    """
    Mixin لمنع الأدمن من القيام بالمعاملات المالية
    الأدمن يقدر يشوف ويحلل ويحذف ويضيف بس مش يودع أو يسحب
    """
    
    def has_add_permission(self, request):

        if self.model._meta.app_label == 'transactions':
            return False
        return super().has_add_permission(request)
    
    def has_change_permission(self, request, obj=None):

        if self.model._meta.app_label == 'transactions':
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):

        return super().has_delete_permission(request, obj)
    
    def has_view_permission(self, request, obj=None):

        return super().has_view_permission(request, obj)


class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):

        total_users = User.objects.count()
        total_accounts = UserBankAccount.objects.count()
        total_transactions = Transaction.objects.count()
        total_balance = UserBankAccount.objects.aggregate(
            total=Sum('balance')
        )['total'] or 0
        

        recent_transactions = Transaction.objects.select_related(
            'account__user'
        ).order_by('-timestamp')[:10]
        
        extra_context = extra_context or {}
        extra_context.update({
            'total_users': total_users,
            'total_accounts': total_accounts,
            'total_transactions': total_transactions,
            'total_balance': total_balance,
            'recent_transactions': recent_transactions,
        })
        
        return super().index(request, extra_context)



admin.site.__class__ = CustomAdminSite


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_per_page = 25
    
    fieldsets = (
        ('معلومات تسجيل الدخول', {'fields': ('email', 'password')}),
        ('معلومات شخصية', {'fields': ('first_name', 'last_name')}),
        ('صلاحيات', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('تواريخ مهمة', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        ('إنشاء مستخدم جديد', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    
    def get_queryset(self, request):
        """التأكد من عرض جميع المستخدمين"""
        qs = super().get_queryset(request)
        return qs.select_related()
    
    def has_view_permission(self, request, obj=None):
        """التأكد من وجود صلاحية العرض"""
        return request.user.is_staff or request.user.is_superuser
    
    def has_module_permission(self, request):
        """التأكد من وجود صلاحية الوصول للوحدة"""
        return request.user.is_staff or request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        """التأكد من وجود صلاحية التعديل"""
        return request.user.is_staff or request.user.is_superuser


@admin.register(BankAccountType)
class BankAccountTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'annual_interest_rate', 'maximum_withdrawal_amount', 'interest_calculation_per_year')
    list_filter = ('annual_interest_rate', 'interest_calculation_per_year')
    search_fields = ('name',)
    
    fieldsets = (
        ('معلومات أساسية', {
            'fields': ('name',)
        }),
        ('إعدادات مالية', {
            'fields': ('maximum_withdrawal_amount', 'annual_interest_rate', 'interest_calculation_per_year')
        }),
    )


@admin.register(UserBankAccount)
class UserBankAccountAdmin(RestrictedAdminMixin, admin.ModelAdmin):
    list_display = ('account_no', 'user', 'account_type', 'balance_display', 'gender', 'initial_deposit_date', 'account_status')
    list_filter = ('account_type', 'gender', 'initial_deposit_date')
    search_fields = ('account_no', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('balance', 'balance_display')  
    
    fieldsets = (
        ('معلومات الحساب', {
            'fields': ('user', 'account_type', 'account_no', 'balance_display')
        }),
        ('معلومات شخصية', {
            'fields': ('gender', 'birth_date')
        }),
        ('تواريخ مهمة', {
            'fields': ('initial_deposit_date', 'interest_start_date')
        }),
    )
    
    add_fieldsets = (
        ('إنشاء حساب بنكي جديد', {
            'fields': ('user', 'account_type', 'gender', 'birth_date', 'initial_deposit_date', 'interest_start_date')
        }),
    )
    
    def balance_display(self, obj):
        """عرض الرصيد مع تنسيق جميل"""
        if obj.balance >= 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{:,.2f} ريال</span>',
                obj.balance
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">{:,.2f} ريال</span>',
                obj.balance
            )
    balance_display.short_description = 'الرصيد الحالي'
    
    def account_status(self, obj):
        """عرض حالة الحساب"""
        if obj.balance > 1000:
            return format_html('<span style="color: green;">نشط</span>')
        elif obj.balance > 0:
            return format_html('<span style="color: orange;">رصيد منخفض</span>')
        else:
            return format_html('<span style="color: red;">رصيد سالب</span>')
    account_status.short_description = 'حالة الحساب'
    

    
    def get_readonly_fields(self, request, obj=None):
        """
        جعل الرصيد للقراءة فقط لمنع الأدمن من تعديله مباشرة
        """
        readonly_fields = list(super().get_readonly_fields(request, obj))
        financial_fields = ['balance', 'balance_display']
        

        if obj:
            financial_fields.append('account_no')
        
        for field in financial_fields:
            if field not in readonly_fields:
                readonly_fields.append(field)
        return readonly_fields
    
    def get_fieldsets(self, request, obj=None):
        """
        استخدام fieldsets مختلفة للإضافة والتعديل
        """
        if not obj: 
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
    
    def save_model(self, request, obj, form, change):
        """منع تعديل الرصيد من لوحة الإدارة ومنع إنشاء حساب بنكي للأدمن"""

        if not change:  
            if obj.user.is_staff or obj.user.is_superuser:
                messages.error(
                    request, 
                    'لا يمكن إنشاء حساب بنكي للأدمن. حسابات الإدارة مخصصة للإدارة والتحليل فقط وليس للمعاملات المالية.'
                )
                return  
            

            if not obj.account_no:
                last_account = UserBankAccount.objects.order_by('-account_no').first()
                if last_account:
                    obj.account_no = last_account.account_no + 1
                else:
                    obj.account_no = 1000001
        
        if change:  

            original = UserBankAccount.objects.get(pk=obj.pk)
            if original.balance != obj.balance:
                messages.error(request, 'لا يمكن تعديل الرصيد من لوحة الإدارة. استخدم نظام المعاملات.')
                obj.balance = original.balance 
        
        super().save_model(request, obj, form, change)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country', 'postal_code')
    list_filter = ('country', 'city')
    search_fields = ('user__email', 'city', 'country', 'street_address')
