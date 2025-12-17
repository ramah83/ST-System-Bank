"""
Test cases for all models to improve coverage
"""
import pytest
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from accounts.models import UserBankAccount, BankAccountType, UserAddress
from transactions.models import Transaction
from transactions.constants import DEPOSIT, WITHDRAWAL
from test_dashboard.models import TestRun, TestCase as TestCaseModel, TestNotification

User = get_user_model()


class UserModelTestCase(TestCase):
    """Test User model functionality"""
    
    def test_user_creation(self):
        """Test user creation"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(str(user), 'test@example.com')
    
    def test_user_full_name_property(self):
        """Test user full name property"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(user.get_full_name(), 'John Doe')
    
    def test_superuser_creation(self):
        """Test superuser creation"""
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class BankAccountTypeModelTestCase(TestCase):
    """Test BankAccountType model"""
    
    def test_account_type_creation(self):
        """Test account type creation"""
        account_type = BankAccountType.objects.create(
            name='Savings Account',
            maximum_withdrawal_amount=5000,
            annual_interest_rate=Decimal('2.5'),
            interest_calculation_per_year=12
        )
        
        self.assertEqual(account_type.name, 'Savings Account')
        self.assertEqual(account_type.maximum_withdrawal_amount, 5000)
    
    def test_account_type_str_representation(self):
        """Test account type string representation"""
        account_type = BankAccountType.objects.create(
            name='Current Account',
            maximum_withdrawal_amount=10000,
            annual_interest_rate=Decimal('2.5'),
            interest_calculation_per_year=12
        )
        self.assertEqual(str(account_type), 'Current Account')


class UserBankAccountModelTestCase(TestCase):
    """Test UserBankAccount model"""
    
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
    
    def test_bank_account_creation(self):
        """Test bank account creation"""
        account = UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no='1234567890',
            balance=Decimal('1000.00')
        )
        
        self.assertEqual(account.user, self.user)
        self.assertEqual(account.account_type, self.account_type)
        self.assertEqual(account.account_no, '1234567890')
        self.assertEqual(account.balance, Decimal('1000.00'))
    
    def test_bank_account_str_representation(self):
        """Test bank account string representation"""
        account = UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no='1234567890',
            balance=Decimal('1000.00')
        )
        expected_str = f"{account.account_no} - {self.user.get_full_name()}"
        self.assertEqual(str(account), expected_str)
    
    def test_account_balance_update(self):
        """Test account balance update"""
        account = UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no='1234567890',
            balance=Decimal('1000.00')
        )
        

        account.balance = Decimal('1500.00')
        account.save()
        

        account.refresh_from_db()
        self.assertEqual(account.balance, Decimal('1500.00'))


class UserAddressModelTestCase(TestCase):
    """Test UserAddress model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_address_creation(self):
        """Test address creation"""
        address = UserAddress.objects.create(
            user=self.user,
            street_address='123 Test Street',
            city='Test City',
            postal_code='12345',
            country='Test Country'
        )
        
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.street_address, '123 Test Street')
        self.assertEqual(address.city, 'Test City')
        self.assertEqual(address.postal_code, '12345')
        self.assertEqual(address.country, 'Test Country')
    
    def test_address_str_representation(self):
        """Test address string representation"""
        address = UserAddress.objects.create(
            user=self.user,
            street_address='123 Test Street',
            city='Test City',
            postal_code='12345',
            country='Test Country'
        )
        expected_str = f"{address.street_address}, {address.city}"
        self.assertEqual(str(address), expected_str)


class TransactionModelTestCase(TestCase):
    """Test Transaction model"""
    
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
    
    def test_transaction_creation(self):
        """Test transaction creation"""
        transaction = Transaction.objects.create(
            account=self.account,
            transaction_type=DEPOSIT,
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00')
        )
        
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.transaction_type, DEPOSIT)
        self.assertEqual(transaction.amount, Decimal('500.00'))
        self.assertEqual(transaction.balance_after_transaction, Decimal('1500.00'))
    
    def test_transaction_str_representation(self):
        """Test transaction string representation"""
        transaction = Transaction.objects.create(
            account=self.account,
            transaction_type=DEPOSIT,
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00')
        )
        expected_str = f"{self.account.account_no} - {transaction.get_transaction_type_display()}"
        self.assertEqual(str(transaction), expected_str)
    
    def test_transaction_type_display(self):
        """Test transaction type display"""
        deposit_transaction = Transaction.objects.create(
            account=self.account,
            transaction_type=DEPOSIT,
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00')
        )
        
        withdrawal_transaction = Transaction.objects.create(
            account=self.account,
            transaction_type=WITHDRAWAL,
            amount=Decimal('200.00'),
            balance_after_transaction=Decimal('1300.00')
        )
        
        self.assertEqual(deposit_transaction.get_transaction_type_display(), 'إيداع')
        self.assertEqual(withdrawal_transaction.get_transaction_type_display(), 'سحب')


class TestDashboardModelsTestCase(TestCase):
    """Test TestDashboard models"""
    
    def test_test_run_creation(self):
        """Test TestRun model creation"""
        test_run = TestRun.objects.create(
            name='Test Run 1',
            status='passed',
            total_tests=10,
            passed_tests=8,
            failed_tests=2,
            error_tests=0,
            duration=45.5,
            coverage_percentage=85.5
        )
        
        self.assertEqual(test_run.name, 'Test Run 1')
        self.assertEqual(test_run.status, 'passed')
        self.assertEqual(test_run.total_tests, 10)
        self.assertEqual(test_run.passed_tests, 8)
        self.assertEqual(test_run.failed_tests, 2)
        self.assertEqual(test_run.error_tests, 0)
        self.assertEqual(test_run.duration, 45.5)
        self.assertEqual(test_run.coverage_percentage, 85.5)
    
    def test_test_run_success_rate_property(self):
        """Test TestRun success_rate property"""
        test_run = TestRun.objects.create(
            name='Test Run 1',
            total_tests=10,
            passed_tests=8,
            failed_tests=2,
            error_tests=0
        )
        
        self.assertEqual(test_run.success_rate, 80.0)
        

        empty_run = TestRun.objects.create(
            name='Empty Run',
            total_tests=0,
            passed_tests=0,
            failed_tests=0,
            error_tests=0
        )
        
        self.assertEqual(empty_run.success_rate, 0)
    
    def test_test_run_str_representation(self):
        """Test TestRun string representation"""
        test_run = TestRun.objects.create(
            name='Test Run 1',
            status='passed'
        )
        self.assertEqual(str(test_run), 'Test Run 1 - passed')
    
    def test_test_case_creation(self):
        """Test TestCase model creation"""
        test_run = TestRun.objects.create(
            name='Test Run 1',
            status='passed'
        )
        
        test_case = TestCaseModel.objects.create(
            test_run=test_run,
            name='test_example',
            class_name='TestExample',
            module_name='test_module',
            status='passed',
            duration=1.5
        )
        
        self.assertEqual(test_case.test_run, test_run)
        self.assertEqual(test_case.name, 'test_example')
        self.assertEqual(test_case.class_name, 'TestExample')
        self.assertEqual(test_case.module_name, 'test_module')
        self.assertEqual(test_case.status, 'passed')
        self.assertEqual(test_case.duration, 1.5)
    
    def test_test_case_str_representation(self):
        """Test TestCase string representation"""
        test_run = TestRun.objects.create(
            name='Test Run 1',
            status='passed'
        )
        
        test_case = TestCaseModel.objects.create(
            test_run=test_run,
            name='test_example',
            class_name='TestExample',
            module_name='test_module',
            status='passed'
        )
        
        self.assertEqual(str(test_case), 'test_example - passed')
    
    def test_test_notification_creation(self):
        """Test TestNotification model creation"""
        test_run = TestRun.objects.create(
            name='Test Run 1',
            status='failed'
        )
        
        notification = TestNotification.objects.create(
            test_run=test_run,
            notification_type='test_failure',
            message='Test failed with errors',
            is_sent=False
        )
        
        self.assertEqual(notification.test_run, test_run)
        self.assertEqual(notification.notification_type, 'test_failure')
        self.assertEqual(notification.message, 'Test failed with errors')
        self.assertFalse(notification.is_sent)
    
    def test_test_notification_str_representation(self):
        """Test TestNotification string representation"""
        test_run = TestRun.objects.create(
            name='Test Run 1',
            status='failed'
        )
        
        notification = TestNotification.objects.create(
            test_run=test_run,
            notification_type='test_failure',
            message='Test failed with errors'
        )
        
        expected_str = f"test_failure - {test_run.name}"
        self.assertEqual(str(notification), expected_str)


@pytest.mark.django_db
class TestModelsPytest:
    """Pytest-style model tests"""
    
    def test_user_model_fields(self):
        """Test user model fields"""
        user = User.objects.create_user(
            email='pytest@example.com',
            password='testpass123',
            first_name='Pytest',
            last_name='User',
            gender='M',
            birth_date='1990-01-01'
        )
        
        assert user.email == 'pytest@example.com'
        assert user.first_name == 'Pytest'
        assert user.last_name == 'User'
        assert user.gender == 'M'
        assert str(user.birth_date) == '1990-01-01'
    
    def test_bank_account_balance_precision(self):
        """Test bank account balance precision"""
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
            balance=Decimal('1234.56')
        )
        
        assert account.balance == Decimal('1234.56')
        assert isinstance(account.balance, Decimal)
    
    def test_transaction_ordering(self):
        """Test transaction ordering"""
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
        

        transaction1 = Transaction.objects.create(
            account=account,
            transaction_type=DEPOSIT,
            amount=Decimal('100.00'),
            balance_after_transaction=Decimal('1100.00')
        )
        
        transaction2 = Transaction.objects.create(
            account=account,
            transaction_type=WITHDRAWAL,
            amount=Decimal('50.00'),
            balance_after_transaction=Decimal('1050.00')
        )
        

        transactions = Transaction.objects.all()
        

        assert transactions[0].timestamp >= transactions[1].timestamp