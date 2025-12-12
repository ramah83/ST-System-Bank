from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Sum
from django.template.response import TemplateResponse
from django.urls import path
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

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

        if self.model._meta.app_label == 'transactions':
            return False
        return super().has_delete_permission(request, obj)


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


@admin.register(UserBankAccount)
class UserBankAccountAdmin(RestrictedAdminMixin, admin.ModelAdmin):
    list_display = ('account_no', 'user', 'account_type', 'balance', 'gender', 'initial_deposit_date')
    list_filter = ('account_type', 'gender', 'initial_deposit_date')
    search_fields = ('account_no', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('account_no', 'balance')  # جعل الرصيد للقراءة فقط
    
    fieldsets = (
        ('معلومات الحساب', {
            'fields': ('user', 'account_type', 'account_no', 'balance')
        }),
        ('معلومات شخصية', {
            'fields': ('gender', 'birth_date')
        }),
        ('تواريخ مهمة', {
            'fields': ('initial_deposit_date', 'interest_start_date')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """
        جعل الرصيد للقراءة فقط لمنع الأدمن من تعديله مباشرة
        """
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if 'balance' not in readonly_fields:
            readonly_fields.append('balance')
        return readonly_fields


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'country', 'postal_code')
    list_filter = ('country', 'city')
    search_fields = ('user__email', 'city', 'country', 'street_address')
