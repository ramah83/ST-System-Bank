import datetime

from django import forms
from django.conf import settings

from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]
        labels = {
            'amount': 'المبلغ',
            'transaction_type': 'نوع المعاملة'
        }

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()
        

        self.fields['amount'].widget.attrs.update({
            'class': 'input-field w-full px-4 py-3 rounded-xl text-gray-700 leading-tight focus:outline-none',
            'placeholder': 'أدخل المبلغ'
        })

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):

    def clean_amount(self):
        min_deposit_amount = settings.MINIMUM_DEPOSIT_AMOUNT
        amount = self.cleaned_data.get('amount')

        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'يجب إيداع {min_deposit_amount}$ على الأقل'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = settings.MINIMUM_WITHDRAWAL_AMOUNT
        max_withdraw_amount = (
            account.account_type.maximum_withdrawal_amount
        )
        balance = account.balance

        amount = self.cleaned_data.get('amount')

        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'يمكنك سحب {min_withdraw_amount}$ على الأقل'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'يمكنك سحب {max_withdraw_amount}$ كحد أقصى'
            )

        if amount > balance:
            raise forms.ValidationError(
                f'رصيدك الحالي {balance}$. '
                'لا يمكنك سحب أكثر من رصيد حسابك'
            )

        return amount


class TransactionDateRangeForm(forms.Form):
    daterange = forms.CharField(
        required=False,
        label='نطاق التاريخ',
        widget=forms.TextInput(attrs={
            'placeholder': 'اختر نطاق التاريخ',
            'class': 'input-field w-full px-4 py-3 rounded-xl text-gray-700 leading-tight focus:outline-none'
        })
    )

    def clean_daterange(self):
        daterange = self.cleaned_data.get("daterange")

        if not daterange:
            return None

        try:
            daterange = daterange.split(' - ')
            if len(daterange) == 2:
                for date in daterange:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                return daterange
            else:
                raise forms.ValidationError("يرجى اختيار نطاق تاريخ صحيح.")
        except (ValueError, AttributeError):
            raise forms.ValidationError("نطاق تاريخ غير صحيح")
