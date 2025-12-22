"""
Test cases for transaction functionality
"""
import pytest
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import UserBankAccount, BankAccountType
from transactions.models import Transaction
from transactions.constants import DEPOSIT, WITHDRAWAL
from transactions.forms import DepositForm, WithdrawForm

User = get_user_model()


class TransactionTestCase(TestCase):
    """Test transaction functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        

        self.account_type = BankAccountType.objects.create(
            name='Savings Account',
            maximum_withdrawal_amount=5000,
            annual_interest_rate=Decimal("2.5"),
            interest_calculation_per_year=12
        )
        

        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        

        self.account = UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no='1234567890',
            balance=Decimal('1000.00')
        )
        

        self.client.login(username='test@example.com', password='testpass123')
    
    def test_deposit_money_success(self):
        """Test successful money deposit"""
        initial_balance = self.account.balance
        deposit_amount = Decimal('500.00')
        
        response = self.client.post(reverse('transactions:deposit_money'), {
            'amount': deposit_amount,
            'transaction_type': DEPOSIT
        })
        

        self.account.refresh_from_db()
        

        self.assertEqual(self.account.balance, initial_balance + deposit_amount)
        

        transaction = Transaction.objects.filter(
            account=self.account,
            transaction_type=DEPOSIT,
            amount=deposit_amount
        ).first()
        
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.balance_after_transaction, self.account.balance)
    
    def test_withdraw_money_success(self):
        """Test successful money withdrawal"""
        initial_balance = self.account.balance
        withdraw_amount = Decimal('300.00')
        
        response = self.client.post(reverse('transactions:withdraw_money'), {
            'amount': withdraw_amount,
            'transaction_type': WITHDRAWAL
        })
        

        self.account.refresh_from_db()
        

        self.assertEqual(self.account.balance, initial_balance - withdraw_amount)
        

        transaction = Transaction.objects.filter(
            account=self.account,
            transaction_type=WITHDRAWAL,
            amount=withdraw_amount
        ).first()
        
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.balance_after_transaction, self.account.balance)
    
    def test_withdraw_insufficient_funds(self):
        """Test withdrawal with insufficient funds"""
        withdraw_amount = Decimal('2000.00')  
        
        form = WithdrawForm(
            data={'amount': withdraw_amount, 'transaction_type': WITHDRAWAL},
            account=self.account
        )
        
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
    
    def test_withdraw_exceeds_limit(self):
        """Test withdrawal exceeding account limit"""

        self.account.balance = Decimal('10000.00')
        self.account.save()
        
        withdraw_amount = Decimal('6000.00')  
        
        form = WithdrawForm(
            data={'amount': withdraw_amount, 'transaction_type': WITHDRAWAL},
            account=self.account
        )
        
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
    
    def test_deposit_form_validation(self):
        """Test deposit form validation"""

        valid_form = DepositForm(
            data={'amount': Decimal('100.00'), 'transaction_type': DEPOSIT},
            account=self.account
        )
        self.assertTrue(valid_form.is_valid())
        

        invalid_form = DepositForm(
            data={'amount': Decimal('-100.00'), 'transaction_type': DEPOSIT},
            account=self.account
        )
        self.assertFalse(invalid_form.is_valid())
    
    def test_transaction_report_view(self):
        """Test transaction report view"""

        Transaction.objects.create(
            account=self.account,
            transaction_type=DEPOSIT,
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00')
        )
        
        Transaction.objects.create(
            account=self.account,
            transaction_type=WITHDRAWAL,
            amount=Decimal('200.00'),
            balance_after_transaction=Decimal('1300.00')
        )
        
        response = self.client.get(reverse('transactions:transaction_report'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '500.00')
        self.assertContains(response, '200.00')
    
    def test_transaction_search_functionality(self):
        """Test transaction search functionality"""

        Transaction.objects.create(
            account=self.account,
            transaction_type=DEPOSIT,
            amount=Decimal('750.00'),
            balance_after_transaction=Decimal('1750.00')
        )
        

        response = self.client.get(reverse('transactions:transaction_search'), {
            'search': '750'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '750.00')
    
    def test_user_without_account_redirect(self):
        """Test that users without bank accounts are redirected"""

        user_no_account = User.objects.create_user(
            email='nobank@example.com',
            password='testpass123'
        )
        

        self.client.login(username='nobank@example.com', password='testpass123')
        

        response = self.client.get(reverse('transactions:deposit_money'))
        self.assertEqual(response.status_code, 302)  
        
        response = self.client.get(reverse('transactions:withdraw_money'))
        self.assertEqual(response.status_code, 302)  


@pytest.mark.django_db
class TestTransactionsPytest:
    """Pytest-style transaction tests"""
    
    def test_transaction_creation(self):
        """Test transaction creation with pytest"""
        user = User.objects.create_user(
            email='pytest@example.com',
            password='testpass123'
        )
        
        account_type = BankAccountType.objects.create(
            name='Test Account',
            maximum_withdrawal_amount=1000,
            annual_interest_rate=Decimal("2.5"),
            interest_calculation_per_year=12
        )
        
        account = UserBankAccount.objects.create(
            user=user,
            account_type=account_type,
            account_no='9876543210',
            balance=Decimal('500.00')
        )
        
        transaction = Transaction.objects.create(
            account=account,
            transaction_type=DEPOSIT,
            amount=Decimal('200.00'),
            balance_after_transaction=Decimal('700.00')
        )
        
        assert transaction.account == account
        assert transaction.amount == Decimal('200.00')
        assert transaction.transaction_type == DEPOSIT
    
    def test_transaction_str_representation(self):
        """Test transaction string representation"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        account_type = BankAccountType.objects.create(
            name='Test Account',
            maximum_withdrawal_amount=1000,
            annual_interest_rate=Decimal("2.5"),
            interest_calculation_per_year=12
        )
        
        account = UserBankAccount.objects.create(
            user=user,
            account_type=account_type,
            account_no='1111111111',
            balance=Decimal('1000.00')
        )
        
        transaction = Transaction.objects.create(
            account=account,
            transaction_type=DEPOSIT,
            amount=Decimal('100.00'),
            balance_after_transaction=Decimal('1100.00')
        )
        
        expected_str = f"{account.account_no} - {transaction.get_transaction_type_display()}"
        assert str(transaction) == expected_str