from django.http import HttpResponseForbidden
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect


class AdminTransactionRestrictionMiddleware:
    """
    Middleware لمنع الأدمن من الوصول لصفحات المعاملات المالية
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        restricted_paths = [
            '/admin/transactions/transaction/add/',
        ]
        

        if (request.user.is_authenticated and 
            request.user.is_staff and 
            any(request.path.startswith(path) for path in restricted_paths)):
            
            messages.error(
                request, 
                'لا يمكن للمديرين إضافة أو تعديل المعاملات المالية. '
                'المعاملات يتم إنشاؤها تلقائياً من خلال النظام.'
            )
            return redirect('admin:transactions_transaction_changelist')
        
        response = self.get_response(request)
        return response