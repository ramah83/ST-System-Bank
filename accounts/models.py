from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models

from .constants import GENDER_CHOICE
from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمين'

    def __str__(self):
        return self.email

    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return 0


class BankAccountType(models.Model):
    name = models.CharField(max_length=128, verbose_name='اسم نوع الحساب')
    maximum_withdrawal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        verbose_name='الحد الأقصى للسحب'
    )
    annual_interest_rate = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        decimal_places=2,
        max_digits=5,
        help_text='معدل الفائدة السنوي من 0 إلى 100',
        verbose_name='معدل الفائدة السنوي'
    )
    interest_calculation_per_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text='عدد مرات حساب الفائدة في السنة',
        verbose_name='عدد مرات حساب الفائدة سنوياً'
    )

    class Meta:
        verbose_name = 'نوع حساب بنكي'
        verbose_name_plural = 'أنواع الحسابات البنكية'

    def __str__(self):
        return self.name

    def calculate_interest(self, principal):
        """
        Calculate interest for each account type.

        This uses a basic interest calculation formula
        """
        p = principal
        r = self.annual_interest_rate
        n = Decimal(self.interest_calculation_per_year)


        interest = (p * (1 + ((r/100) / n))) - p

        return round(interest, 2)


class UserBankAccount(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
        verbose_name='المستخدم'
    )
    account_type = models.ForeignKey(
        BankAccountType,
        related_name='accounts',
        on_delete=models.CASCADE,
        verbose_name='نوع الحساب'
    )
    account_no = models.PositiveIntegerField(unique=True, verbose_name='رقم الحساب')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, verbose_name='الجنس')
    birth_date = models.DateField(null=True, blank=True, verbose_name='تاريخ الميلاد')
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2,
        verbose_name='الرصيد'
    )
    interest_start_date = models.DateField(
        null=True, blank=True,
        help_text='تاريخ بداية حساب الفائدة',
        verbose_name='تاريخ بداية الفائدة'
    )
    initial_deposit_date = models.DateField(null=True, blank=True, verbose_name='تاريخ أول إيداع')

    class Meta:
        verbose_name = 'حساب بنكي'
        verbose_name_plural = 'الحسابات البنكية'

    def __str__(self):
        return str(self.account_no)

    def get_interest_calculation_months(self):
        """
        List of month numbers for which the interest will be calculated

        returns [2, 4, 6, 8, 10, 12] for every 2 months interval
        """
        interval = int(
            12 / self.account_type.interest_calculation_per_year
        )
        start = self.interest_start_date.month
        return [i for i in range(start, 13, interval)]


class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE,
        verbose_name='المستخدم'
    )
    street_address = models.CharField(max_length=512, verbose_name='عنوان الشارع')
    city = models.CharField(max_length=256, verbose_name='المدينة')
    postal_code = models.PositiveIntegerField(verbose_name='الرمز البريدي')
    country = models.CharField(max_length=256, verbose_name='البلد')

    class Meta:
        verbose_name = 'عنوان مستخدم'
        verbose_name_plural = 'عناوين المستخدمين'

    def __str__(self):
        return self.user.email
