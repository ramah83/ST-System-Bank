from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'core/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # الأدمن لا يجب أن يكون له حساب بنكي - إخفاء الحساب إذا كان أدمن
        if (self.request.user.is_authenticated 
            and hasattr(self.request.user, 'account')
            and not self.request.user.is_staff 
            and not self.request.user.is_superuser):
            context['user_account'] = self.request.user.account
        return context
