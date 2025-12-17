from dateutil.relativedelta import relativedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.contrib.auth import get_user_model
from django.db.models import Q

from transactions.constants import DEPOSIT, WITHDRAWAL
from transactions.forms import (
    DepositForm,
    TransactionDateRangeForm,
    WithdrawForm,
)
from transactions.models import Transaction


class TransactionRepostView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'account'):
            messages.error(request, 'يجب أن يكون لديك حساب بنكي للوصول إلى هذه الصفحة.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = TransactionDateRangeForm(request.GET or None)
        if form.is_valid():
            self.form_data = form.cleaned_data

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )

        daterange = self.form_data.get("daterange")
        search_query = self.request.GET.get('search', '')
        transaction_type = self.request.GET.get('transaction_type', '')

        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)
        
        if search_query:
            queryset = queryset.filter(
                Q(amount__icontains=search_query) |
                Q(balance_after_transaction__icontains=search_query)
            )
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account,
            'form': TransactionDateRangeForm(self.request.GET or None)
        })

        return context


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_staff or request.user.is_superuser:
            messages.error(
                request, 
                'حسابات الإدارة غير مسموح لها بإجراء المعاملات المالية (إيداع/سحب). هذه الحسابات مخصصة للإدارة والتحليل فقط.'
            )
            return redirect('home')
        
        if not hasattr(request.user, 'account'):
            messages.error(request, 'يجب أن يكون لديك حساب بنكي لإجراء المعاملات.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'إيداع أموال في حسابك'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account

        if not account.initial_deposit_date:
            now = timezone.now()
            next_interest_month = int(
                12 / account.account_type.interest_calculation_per_year
            )
            account.initial_deposit_date = now
            account.interest_start_date = (
                now + relativedelta(
                    months=+next_interest_month
                )
            )

        account.balance += amount
        account.save(
            update_fields=[
                'initial_deposit_date',
                'balance',
                'interest_start_date'
            ]
        )

        messages.success(
            self.request,
            f'تم إيداع {amount}$ في حسابك بنجاح'
        )

        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'سحب أموال من حسابك'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.account.balance -= form.cleaned_data.get('amount')
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'تم سحب {amount}$ من حسابك بنجاح'
        )

        return super().form_valid(form)


class UserSearchView(LoginRequiredMixin, ListView):
    """View for searching users - Admin functionality"""
    template_name = 'transactions/user_search.html'
    model = get_user_model()
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(email__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        
        return queryset.order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class TransactionSearchView(LoginRequiredMixin, ListView):
    """View for searching all transactions - Admin functionality"""
    template_name = 'transactions/transaction_search.html'
    model = Transaction
    context_object_name = 'transactions'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        transaction_type = self.request.GET.get('transaction_type', '')
        account_search = self.request.GET.get('account_search', '')
        
        if search_query:
            queryset = queryset.filter(
                Q(amount__icontains=search_query) |
                Q(balance_after_transaction__icontains=search_query)
            )
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
            
        if account_search:
            queryset = queryset.filter(
                Q(account__account_no__icontains=account_search) |
                Q(account__user__email__icontains=account_search)
            )
        
        return queryset.order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.request.GET.get('search', ''),
            'transaction_type': self.request.GET.get('transaction_type', ''),
            'account_search': self.request.GET.get('account_search', ''),
            'DEPOSIT': DEPOSIT,
            'WITHDRAWAL': WITHDRAWAL,
        })
        return context