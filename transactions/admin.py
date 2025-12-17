from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils.html import format_html

from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type_display', 'amount_display', 'balance_after_transaction', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('account__user__email', 'account__account_no')
    readonly_fields = ('account', 'transaction_type', 'amount', 'timestamp', 'balance_after_transaction', 'admin_warning')
    date_hierarchy = 'timestamp'
    actions = ['delete_selected_with_warning']
    
    def transaction_type_display(self, obj):
        type_map = {
            1: format_html('<span style="color: green;">إيداع</span>'),
            2: format_html('<span style="color: red;">سحب</span>'),
            3: format_html('<span style="color: blue;">فائدة</span>')
        }
        return type_map.get(obj.transaction_type, 'غير معروف')
    transaction_type_display.short_description = 'نوع المعاملة'
    
    def amount_display(self, obj):
        """عرض المبلغ مع تنسيق جميل"""
        if obj.transaction_type == 1:  # إيداع
            return format_html(
                '<span style="color: green; font-weight: bold;">+{:,.2f} ريال</span>',
                obj.amount
            )
        elif obj.transaction_type == 2:  # سحب
            return format_html(
                '<span style="color: red; font-weight: bold;">-{:,.2f} ريال</span>',
                obj.amount
            )
        else:  # فائدة
            return format_html(
                '<span style="color: blue; font-weight: bold;">+{:,.2f} ريال</span>',
                obj.amount
            )
    amount_display.short_description = 'المبلغ'
    
    def admin_warning(self, obj):
        """رسالة تحذيرية للأدمن"""
        return format_html(
            '<div style="background: #f8d7da; border: 1px solid #f5c6cb; padding: 10px; border-radius: 5px; color: #721c24;">'
            '<strong>تحذير:</strong> المعاملات المالية للعرض والتحليل فقط. '
            'لا يمكن إضافة أو تعديل معاملات من لوحة الإدارة. '
            'الحذف متاح للسوبر أدمن فقط لأغراض الإدارة.'
            '</div>'
        )
    admin_warning.short_description = ''
    
    fieldsets = (
        ('تنبيه هام', {
            'fields': ('admin_warning',),
            'classes': ('collapse',),
        }),
        ('معلومات المعاملة', {
            'fields': ('account', 'transaction_type', 'amount')
        }),
        ('معلومات إضافية', {
            'fields': ('balance_after_transaction', 'timestamp')
        }),
    )
    
    def has_add_permission(self, request):
        """
        منع إضافة معاملات جديدة من لوحة الإدارة
        المعاملات يجب أن تتم فقط من خلال النظام
        """
        return False
    
    def has_change_permission(self, request, obj=None):
        """
        منع تعديل المعاملات - للعرض فقط
        """
        return False
    
    def has_delete_permission(self, request, obj=None):
        """
        السماح للأدمن بحذف المعاملات للتحليل والإدارة
        لكن مع تحذير
        """
        return request.user.is_superuser
    
    def get_readonly_fields(self, request, obj=None):
        """
        جعل جميع الحقول للقراءة فقط
        """
        return [field.name for field in self.model._meta.fields]
    
    def delete_selected_with_warning(self, request, queryset):
        """حذف المعاملات المحددة مع تحذير"""
        if not request.user.is_superuser:
            messages.error(request, 'فقط السوبر أدمن يمكنه حذف المعاملات')
            return
        
        count = queryset.count()
        queryset.delete()
        messages.success(request, f'تم حذف {count} معاملة بنجاح')
    
    delete_selected_with_warning.short_description = 'حذف المعاملات المحددة (سوبر أدمن فقط)'
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """
        تخصيص عرض النموذج لإظهار رسالة تنبيه
        """
        extra_context = extra_context or {}
        extra_context['readonly_message'] = 'المعاملات المالية للعرض والتحليل فقط - لا يمكن تعديلها من لوحة الإدارة'
        return super().changeform_view(request, object_id, form_url, extra_context)
    
    def changelist_view(self, request, extra_context=None):
        """إضافة رسالة تحذيرية في قائمة المعاملات"""
        messages.info(request, 'المعاملات المالية للعرض والتحليل فقط. الحذف متاح للسوبر أدمن فقط.')
        return super().changelist_view(request, extra_context)
