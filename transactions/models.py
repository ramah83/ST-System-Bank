from django.db import models

from .constants import TRANSACTION_TYPE_CHOICES
from accounts.models import UserBankAccount


class Transaction(models.Model):
    account = models.ForeignKey(
        UserBankAccount,
        related_name='transactions',
        on_delete=models.CASCADE,
        verbose_name='الحساب'
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        verbose_name='المبلغ'
    )
    balance_after_transaction = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        verbose_name='الرصيد بعد المعاملة'
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name='نوع المعاملة'
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='وقت المعاملة')

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'معاملة مالية'
        verbose_name_plural = 'المعاملات المالية'

    def __str__(self):
        return f'{self.account.account_no} - {self.get_transaction_type_display()}'
