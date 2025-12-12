from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

from transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type_display', 'amount', 'balance_after_transaction', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')
    search_fields = ('account__user__email', 'account__account_no')
    readonly_fields = ('account', 'transaction_type', 'amount', 'timestamp', 'balance_after_transaction')
    date_hierarchy = 'timestamp'
    
    def transaction_type_display(self, obj):
        type_map = {1: 'إيداع', 2: 'سحب', 3: 'فائدة'}
        return type_map.get(obj.transaction_type, 'غير معروف')
    transaction_type_display.short_description = 'نوع المعاملة'
    
    fieldsets = (
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
        منع حذف المعاملات
        """
        return False
    
    def get_readonly_fields(self, request, obj=None):
        """
        جعل جميع الحقول للقراءة فقط
        """
        return [field.name for field in self.model._meta.fields]
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        """
        تخصيص عرض النموذج لإظهار رسالة تنبيه
        """
        extra_context = extra_context or {}
        extra_context['readonly_message'] = 'المعاملات المالية للعرض فقط - لا يمكن تعديلها من لوحة الإدارة'
        return super().changeform_view(request, object_id, form_url, extra_context)
