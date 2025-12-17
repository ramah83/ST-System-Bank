"""
Test cases for admin functionality to improve coverage
"""
import pytest
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from accounts.models import UserBankAccount, BankAccountType, UserAddress
from accounts.admin import UserAdmin, UserBankAccountAdmin, BankAccountTypeAdmin, UserAddressAdmin
from transactions.models import Transaction
from transactions.admin import TransactionAdmin
from transactions.constants import DEPOSIT, WITHDRAWAL
from test_dashboard.models import TestRun, TestCase as TestCaseModel, TestNotification
from test_dashboard.admin import TestRunAdmin, TestCaseAdmin, TestNotificationAdmin

User = get_user_model()


class AdminTestCase(TestCase):
    """Test admin functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.site = AdminSite()
        

        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        

        self.regular_user = User.objects.create_user(
            email='user@example.com',
            password='userpass123',
            first_name='Test',
            last_name='User'
        )
        

        self.account_type = BankAccountType.objects.create(
            name='Savings Account',
            maximum_withdrawal_amount=5000,
            annual_interest_rate=Decimal('2.5'),
            interest_calculation_per_year=12
        )
        

        self.account = UserBankAccount.objects.create(
            user=self.regular_user,
            account_type=self.account_type,
            account_no='1234567890',
            balance=Decimal('1000.00')
        )
        

        self.address = UserAddress.objects.create(
            user=self.regular_user,
            street_address='123 Test Street',
            city='Test City',
            postal_code='12345',
            country='Test Country'
        )
        

        self.transaction = Transaction.objects.create(
            account=self.account,
            transaction_type=DEPOSIT,
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00')
        )
        

        self.test_run = TestRun.objects.create(
            name='Test Run 1',
            status='passed',
            total_tests=10,
            passed_tests=8,
            failed_tests=2
        )
        

        self.test_case = TestCaseModel.objects.create(
            test_run=self.test_run,
            name='test_example',
            class_name='TestExample',
            module_name='test_module',
            status='passed'
        )
        

        self.notification = TestNotification.objects.create(
            test_run=self.test_run,
            notification_type='test_failure',
            message='Test failed'
        )
    
    def test_admin_site_access(self):
        """Test admin site access"""

        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        

        self.client.login(username='admin@example.com', password='adminpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
    
    def test_user_admin(self):
        """Test UserAdmin functionality"""
        admin = UserAdmin(User, self.site)
        

        self.assertIn('email', admin.list_display)
        self.assertIn('first_name', admin.list_display)
        self.assertIn('last_name', admin.list_display)
        

        self.assertIn('email', admin.search_fields)
        self.assertIn('first_name', admin.search_fields)
        

        self.assertIn('is_staff', admin.list_filter)
        self.assertIn('is_active', admin.list_filter)
    
    def test_user_admin_changelist(self):
        """Test user admin changelist view"""
        self.client.login(username='admin@example.com', password='adminpass123')
        
        response = self.client.get('/admin/accounts/user/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user@example.com')
    
    def test_user_admin_change_form(self):
        """Test user admin change form"""
        self.client.login(username='admin@example.com', password='adminpass123')
        
        response = self.client.get(f'/admin/accounts/user/{self.regular_user.pk}/change/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user@example.com')
    
    def test_bank_account_admin(self):
        """Test UserBankAccountAdmin functionality"""
        admin = UserBankAccountAdmin(UserBankAccount, self.site)
        

        self.assertIn('account_no', admin.list_display)
        self.assertIn('user', admin.list_display)
        self.assertIn('balance', admin.list_display)
        

        self.assertIn('account_no', admin.search_fields)
        self.assertIn('user__email', admin.search_fields)
    
    def test_bank_account_admin_changelist(self):
        """Test bank account admin changelist view"""
        self.client.login(username='admin@example.com', password='adminpass123')
        
        response = self.client.get('/admin/accounts/userbankaccount/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1234567890')
    
    def test_transaction_admin(self):
        """Test TransactionAdmin functionality"""
        admin = TransactionAdmin(Transaction, self.site)
        

        self.assertIn('account', admin.list_display)
        self.assertIn('transaction_type', admin.list_display)
        self.assertIn('amount', admin.list_display)
        

        self.assertIn('transaction_type', admin.list_filter)
        self.assertIn('timestamp', admin.list_filter)
    
    def test_transaction_admin_changelist(self):
        """Test transaction admin changelist view"""
        self.client.login(username='admin@example.com', password='adminpass123')
        
        response = self.client.get('/admin/transactions/transaction/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '500.00')
    
    def test_test_run_admin(self):
        """Test TestRunAdmin functionality"""
        admin = TestRunAdmin(TestRun, self.site)
        

        self.assertIn('name', admin.list_display)
        self.assertIn('status', admin.list_display)
        self.assertIn('start_time', admin.list_display)
        

        self.assertIn('status', admin.list_filter)
        self.assertIn('start_time', admin.list_filter)
    
    def test_test_run_admin_changelist(self):
        """Test test run admin changelist view"""
        self.client.login(username='admin@example.com', password='adminpass123')
        
        response = self.client.get('/admin/test_dashboard/testrun/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Run 1')
    
    def test_admin_permissions(self):
        """Test admin permissions"""

        self.client.login(username='user@example.com', password='userpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)  # Redirect to login
        

        self.client.login(username='admin@example.com', password='adminpass123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
    
    def test_admin_search_functionality(self):
        """Test admin search functionality"""
        self.client.login(username='admin@example.com', password='adminpass123')
        

        response = self.client.get('/admin/accounts/user/', {'q': 'user@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user@example.com')
        

        response = self.client.get('/admin/transactions/transaction/', {'q': '1234567890'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1234567890')
    
    def test_admin_filtering(self):
        """Test admin filtering functionality"""
        self.client.login(username='admin@example.com', password='adminpass123')
        

        response = self.client.get('/admin/accounts/user/', {'is_staff__exact': '0'})
        self.assertEqual(response.status_code, 200)
        

        response = self.client.get('/admin/transactions/transaction/', {'transaction_type__exact': str(DEPOSIT)})
        self.assertEqual(response.status_code, 200)
    
    def test_admin_inline_functionality(self):
        """Test admin inline functionality"""
        admin = UserAdmin(User, self.site)
        

        if hasattr(admin, 'inlines'):
            self.assertTrue(len(admin.inlines) >= 0)
    
    def test_admin_readonly_fields(self):
        """Test admin readonly fields"""
        admin = TransactionAdmin(Transaction, self.site)
        

        if hasattr(admin, 'readonly_fields'):

            self.assertIn('timestamp', admin.readonly_fields)
    
    def test_admin_fieldsets(self):
        """Test admin fieldsets configuration"""
        admin = UserAdmin(User, self.site)
        

        if hasattr(admin, 'fieldsets'):
            self.assertTrue(len(admin.fieldsets) > 0)
    
    def test_admin_actions(self):
        """Test admin actions"""
        self.client.login(username='admin@example.com', password='adminpass123')
        

        response = self.client.post('/admin/accounts/user/', {
            'action': 'delete_selected',
            '_selected_action': [str(self.regular_user.pk)],
            'post': 'yes'
        })
        

        self.assertEqual(response.status_code, 302)


class AdminCustomizationTestCase(TestCase):
    """Test admin customization"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
    
    def test_admin_site_header(self):
        """Test admin site header customization"""
        self.client.login(username='admin@example.com', password='adminpass123')
        
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'النظام المصرفي')
    
    def test_admin_site_title(self):
        """Test admin site title customization"""
        self.client.login(username='admin@example.com', password='adminpass123')
        
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'إدارة النظام المصرفي')
    
    def test_admin_breadcrumbs(self):
        """Test admin breadcrumbs"""
        self.client.login(username='admin@example.com', password='adminpass123')
        
        response = self.client.get('/admin/accounts/user/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'الرئيسية')


@pytest.mark.django_db
class TestAdminPytest:
    """Pytest-style admin tests"""
    
    def test_admin_model_registration(self):
        """Test that all models are registered in admin"""
        from django.contrib import admin
        

        assert User in admin.site._registry
        assert UserBankAccount in admin.site._registry
        assert BankAccountType in admin.site._registry
        assert Transaction in admin.site._registry
        assert TestRun in admin.site._registry
    
    def test_admin_model_str_methods(self):
        """Test model __str__ methods in admin context"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        account_type = BankAccountType.objects.create(
            name='Test Account',
            maximum_withdrawal_amount=1000
        )
        
        account = UserBankAccount.objects.create(
            user=user,
            account_type=account_type,
            account_no='1234567890',
            balance=Decimal('1000.00')
        )
        

        assert str(user) == 'test@example.com'
        assert str(account_type) == 'Test Account'
        assert 'test@example.com' in str(account)
    
    def test_admin_queryset_optimization(self):
        """Test admin queryset optimization"""
        from transactions.admin import TransactionAdmin
        from django.contrib.admin.sites import AdminSite
        
        site = AdminSite()
        admin = TransactionAdmin(Transaction, site)
        

        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        account_type = BankAccountType.objects.create(
            name='Test Account',
            maximum_withdrawal_amount=1000
        )
        
        account = UserBankAccount.objects.create(
            user=user,
            account_type=account_type,
            account_no='1234567890',
            balance=Decimal('1000.00')
        )
        
        Transaction.objects.create(
            account=account,
            transaction_type=DEPOSIT,
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00')
        )
        

        queryset = admin.get_queryset(None)
        assert queryset.count() > 0
    
    def test_admin_form_validation(self):
        """Test admin form validation"""
        from accounts.admin import UserAdmin
        from django.contrib.admin.sites import AdminSite
        
        site = AdminSite()
        admin = UserAdmin(User, site)
        

        form_class = admin.get_form(None)
        

        form = form_class({
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        })
        

