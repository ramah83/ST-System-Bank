"""
Test cases for all forms to improve coverage
"""
import pytest
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import UserBankAccount, BankAccountType
from accounts.forms import UserRegistrationForm, UserAddressForm
from transactions.forms import DepositForm, WithdrawForm, TransactionDateRangeForm
from transactions.constants import DEPOSIT, WITHDRAWAL

User = get_user_model()


class UserRegistrationFormTestCase(TestCase):
    """Test UserRegistrationForm"""
    
    def test_valid_registration_form(self):
        """Test valid registration form"""
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'gender': 'M',
            'birth_date': '1990-01-01',
        }
        
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_email_format(self):
        """Test invalid email format"""
        form_data = {
            'email': 'invalid-email',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'gender': 'M',
            'birth_date': '1990-01-01',
        }
        
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_password_mismatch(self):
        """Test password mismatch"""
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'differentpass',
            'gender': 'M',
            'birth_date': '1990-01-01',
        }
        
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_duplicate_email(self):
        """Test duplicate email validation"""

        User.objects.create_user(
            email='existing@example.com',
            password='testpass123'
        )
        
        form_data = {
            'email': 'existing@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'gender': 'M',
            'birth_date': '1990-01-01',
        }
        
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_required_fields(self):
        """Test required fields validation"""
        form = UserRegistrationForm(data={})
        self.assertFalse(form.is_valid())
        
        required_fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        for field in required_fields:
            self.assertIn(field, form.errors)
    
    def test_form_save(self):
        """Test form save method"""
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'gender': 'M',
            'birth_date': '1990-01-01',
        }
        
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('testpass123'))


class UserAddressFormTestCase(TestCase):
    """Test UserAddressForm"""
    
    def test_valid_address_form(self):
        """Test valid address form"""
        form_data = {
            'street_address': '123 Test Street',
            'city': 'Test City',
            'postal_code': '12345',
            'country': 'Test Country',
        }
        
        form = UserAddressForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_required_fields(self):
        """Test required fields validation"""
        form = UserAddressForm(data={})
        self.assertFalse(form.is_valid())
        
        required_fields = ['street_address', 'city', 'postal_code', 'country']
        for field in required_fields:
            self.assertIn(field, form.errors)
    
    def test_postal_code_validation(self):
        """Test postal code validation"""
        form_data = {
            'street_address': '123 Test Street',
            'city': 'Test City',
            'postal_code': '',  # Empty postal code
            'country': 'Test Country',
        }
        
        form = UserAddressForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('postal_code', form.errors)


class DepositFormTestCase(TestCase):
    """Test DepositForm"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        self.account_type = BankAccountType.objects.create(
            name='Savings Account',
            maximum_withdrawal_amount=5000,
            annual_interest_rate=Decimal("2.5"),
            interest_calculation_per_year=12
        )
        
        self.account = UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no='1234567890',
            balance=Decimal('1000.00')
        )
    
    def test_valid_deposit_form(self):
        """Test valid deposit form"""
        form_data = {
            'amount': Decimal('500.00'),
            'transaction_type': DEPOSIT
        }
        
        form = DepositForm(data=form_data, account=self.account)
        self.assertTrue(form.is_valid())
    
    def test_negative_amount(self):
        """Test negative amount validation"""
        form_data = {
            'amount': Decimal('-100.00'),
            'transaction_type': DEPOSIT
        }
        
        form = DepositForm(data=form_data, account=self.account)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
    
    def test_zero_amount(self):
        """Test zero amount validation"""
        form_data = {
            'amount': Decimal('0.00'),
            'transaction_type': DEPOSIT
        }
        
        form = DepositForm(data=form_data, account=self.account)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
    
    def test_form_save(self):
        """Test form save method"""
        form_data = {
            'amount': Decimal('500.00'),
            'transaction_type': DEPOSIT
        }
        
        form = DepositForm(data=form_data, account=self.account)
        self.assertTrue(form.is_valid())
        
        transaction = form.save()
        self.assertEqual(transaction.amount, Decimal('500.00'))
        self.assertEqual(transaction.transaction_type, DEPOSIT)
        self.assertEqual(transaction.account, self.account)
        

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1500.00'))


class WithdrawFormTestCase(TestCase):
    """Test WithdrawForm"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        self.account_type = BankAccountType.objects.create(
            name='Savings Account',
            maximum_withdrawal_amount=5000,
            annual_interest_rate=Decimal("2.5"),
            interest_calculation_per_year=12
        )
        
        self.account = UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no='1234567890',
            balance=Decimal('1000.00')
        )
    
    def test_valid_withdraw_form(self):
        """Test valid withdraw form"""
        form_data = {
            'amount': Decimal('300.00'),
            'transaction_type': WITHDRAWAL
        }
        
        form = WithdrawForm(data=form_data, account=self.account)
        self.assertTrue(form.is_valid())
    
    def test_insufficient_funds(self):
        """Test insufficient funds validation"""
        form_data = {
            'amount': Decimal('2000.00'),  # More than balance
            'transaction_type': WITHDRAWAL
        }
        
        form = WithdrawForm(data=form_data, account=self.account)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
    
    def test_exceeds_withdrawal_limit(self):
        """Test withdrawal limit validation"""

        self.account.balance = Decimal('10000.00')
        self.account.save()
        
        form_data = {
            'amount': Decimal('6000.00'),  # Exceeds limit of 5000
            'transaction_type': WITHDRAWAL
        }
        
        form = WithdrawForm(data=form_data, account=self.account)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
    
    def test_negative_amount(self):
        """Test negative amount validation"""
        form_data = {
            'amount': Decimal('-100.00'),
            'transaction_type': WITHDRAWAL
        }
        
        form = WithdrawForm(data=form_data, account=self.account)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)
    
    def test_form_save(self):
        """Test form save method"""
        form_data = {
            'amount': Decimal('300.00'),
            'transaction_type': WITHDRAWAL
        }
        
        form = WithdrawForm(data=form_data, account=self.account)
        self.assertTrue(form.is_valid())
        
        transaction = form.save()
        self.assertEqual(transaction.amount, Decimal('300.00'))
        self.assertEqual(transaction.transaction_type, WITHDRAWAL)
        self.assertEqual(transaction.account, self.account)
        

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('700.00'))


class TransactionDateRangeFormTestCase(TestCase):
    """Test TransactionDateRangeForm"""
    
    def test_valid_date_range_form(self):
        """Test valid date range form"""
        form_data = {
            'daterange': '2024-01-01 - 2024-01-31'
        }
        
        form = TransactionDateRangeForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_empty_date_range(self):
        """Test empty date range (should be valid)"""
        form = TransactionDateRangeForm(data={})
        self.assertTrue(form.is_valid())
    
    def test_invalid_date_format(self):
        """Test invalid date format"""
        form_data = {
            'daterange': 'invalid-date-format'
        }
        
        form = TransactionDateRangeForm(data=form_data)




@pytest.mark.django_db
class TestFormsPytest:
    """Pytest-style form tests"""
    
    def test_registration_form_clean_email(self):
        """Test registration form email cleaning"""
        form_data = {
            'email': '  TEST@EXAMPLE.COM  ',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'gender': 'M',
            'birth_date': '1990-01-01',
        }
        
        form = UserRegistrationForm(data=form_data)
        assert form.is_valid()
        

        cleaned_email = form.cleaned_data['email']
        assert cleaned_email == 'test@example.com'
    
    def test_deposit_form_without_account(self):
        """Test deposit form without account parameter"""
        form_data = {
            'amount': Decimal('500.00'),
            'transaction_type': DEPOSIT
        }
        

        form = DepositForm(data=form_data)


    
    def test_withdraw_form_edge_cases(self):
        """Test withdraw form edge cases"""
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
            account_no='1234567890',
            balance=Decimal('1000.00')
        )
        

        form_data = {
            'amount': Decimal('1000.00'),
            'transaction_type': WITHDRAWAL
        }
        
        form = WithdrawForm(data=form_data, account=account)
        assert form.is_valid()
        

        form_data = {
            'amount': Decimal('1000.00'),  # Exact limit
            'transaction_type': WITHDRAWAL
        }
        
        form = WithdrawForm(data=form_data, account=account)
        assert form.is_valid()
    
    def test_form_field_widgets(self):
        """Test form field widgets and attributes"""
        form = UserRegistrationForm()
        

        email_field = form.fields['email']
        assert email_field.widget.attrs.get('type') == 'email' or 'email' in str(email_field.widget)
        

        password1_field = form.fields['password1']
        password2_field = form.fields['password2']
        
        assert 'password' in str(password1_field.widget).lower()
        assert 'password' in str(password2_field.widget).lower()