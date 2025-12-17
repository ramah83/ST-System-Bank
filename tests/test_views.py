"""
Test cases for all views to improve coverage
"""
import pytest
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from accounts.models import UserBankAccount, BankAccountType, UserAddress
from transactions.models import Transaction
from transactions.constants import DEPOSIT, WITHDRAWAL
from test_dashboard.models import TestRun, TestCase as TestCaseModel, TestNotification

User = get_user_model()


class HomeViewTestCase(TestCase):
    """Test HomeView"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
    
    def test_home_view_get(self):
        """Test home view GET request"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'النظام المصرفي')
    
    def test_home_view_context(self):
        """Test home view context"""
        response = self.client.get(reverse('home'))
        self.assertIn('title', response.context)


class UserRegistrationViewTestCase(TestCase):
    """Test UserRegistrationView"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.registration_url = reverse('accounts:user_registration')
    
    def test_registration_view_get(self):
        """Test registration view GET request"""
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'تسجيل حساب جديد')
    
    def test_registration_view_post_success(self):
        """Test successful registration"""
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'gender': 'M',
            'birth_date': '1990-01-01',
            'street_address': '123 Test Street',
            'city': 'Test City',
            'postal_code': '12345',
            'country': 'Test Country',
        }
        
        response = self.client.post(self.registration_url, form_data)
        

        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        

        self.assertEqual(response.status_code, 302)
    
    def test_registration_view_post_invalid(self):
        """Test registration with invalid data"""
        form_data = {
            'email': 'invalid-email',
            'first_name': '',
            'password1': 'pass',
            'password2': 'different',
        }
        
        response = self.client.post(self.registration_url, form_data)
        

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'خطأ')
    
    def test_authenticated_user_redirect(self):
        """Test authenticated user redirect"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='test@example.com', password='testpass123')
        
        response = self.client.get(self.registration_url)
        self.assertEqual(response.status_code, 302)


class UserLoginViewTestCase(TestCase):
    """Test UserLoginView"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.login_url = reverse('accounts:user_login')
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Test login view GET request"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'تسجيل الدخول')
    
    def test_login_view_post_success(self):
        """Test successful login"""
        form_data = {
            'username': 'test@example.com',
            'password': 'testpass123'
        }
        
        response = self.client.post(self.login_url, form_data)
        

        self.assertTrue('_auth_user_id' in self.client.session)
        

        self.assertEqual(response.status_code, 302)
    
    def test_login_view_post_invalid(self):
        """Test login with invalid credentials"""
        form_data = {
            'username': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(self.login_url, form_data)
        

        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)


class TransactionViewsTestCase(TestCase):
    """Test transaction views"""
    
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
    
    def test_deposit_view_get(self):
        """Test deposit view GET request"""
        response = self.client.get(reverse('transactions:deposit_money'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'إيداع أموال')
    
    def test_deposit_view_post_success(self):
        """Test successful deposit"""
        form_data = {
            'amount': Decimal('500.00'),
            'transaction_type': DEPOSIT
        }
        
        response = self.client.post(reverse('transactions:deposit_money'), form_data)
        

        self.assertTrue(Transaction.objects.filter(
            account=self.account,
            transaction_type=DEPOSIT,
            amount=Decimal('500.00')
        ).exists())
        

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('1500.00'))
    
    def test_withdraw_view_get(self):
        """Test withdraw view GET request"""
        response = self.client.get(reverse('transactions:withdraw_money'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'سحب أموال')
    
    def test_withdraw_view_post_success(self):
        """Test successful withdrawal"""
        form_data = {
            'amount': Decimal('300.00'),
            'transaction_type': WITHDRAWAL
        }
        
        response = self.client.post(reverse('transactions:withdraw_money'), form_data)
        

        self.assertTrue(Transaction.objects.filter(
            account=self.account,
            transaction_type=WITHDRAWAL,
            amount=Decimal('300.00')
        ).exists())
        

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal('700.00'))
    
    def test_transaction_report_view(self):
        """Test transaction report view"""

        Transaction.objects.create(
            account=self.account,
            transaction_type=DEPOSIT,
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00')
        )
        
        response = self.client.get(reverse('transactions:transaction_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '500.00')
    
    def test_user_search_view(self):
        """Test user search view"""

        admin_user = User.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        

        self.client.login(username='admin@example.com', password='adminpass123')
        
        response = self.client.get(reverse('transactions:user_search'), {
            'search': 'test'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test@example.com')
    
    def test_transaction_search_view(self):
        """Test transaction search view"""

        admin_user = User.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        

        self.client.login(username='admin@example.com', password='adminpass123')
        

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


class TestDashboardViewsTestCase(TestCase):
    """Test test dashboard views"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        

        self.staff_user = User.objects.create_user(
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )
        

        self.regular_user = User.objects.create_user(
            email='user@example.com',
            password='userpass123'
        )
        

        self.test_run = TestRun.objects.create(
            name='Test Run 1',
            status='passed',
            total_tests=10,
            passed_tests=8,
            failed_tests=2,
            duration=45.5,
            coverage_percentage=85.5
        )
    
    def test_dashboard_view_staff_access(self):
        """Test dashboard view with staff access"""
        self.client.login(username='staff@example.com', password='staffpass123')
        
        response = self.client.get(reverse('test_dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'لوحة اختبار النظام')
    
    def test_dashboard_view_regular_user_denied(self):
        """Test dashboard view denies regular users"""
        self.client.login(username='user@example.com', password='userpass123')
        
        response = self.client.get(reverse('test_dashboard:dashboard'))

        self.assertIn(response.status_code, [302, 403])
    
    def test_test_run_detail_view(self):
        """Test test run detail view"""
        self.client.login(username='staff@example.com', password='staffpass123')
        
        response = self.client.get(
            reverse('test_dashboard:test_run_detail', kwargs={'pk': self.test_run.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Run 1')
    
    def test_trends_view(self):
        """Test trends view"""
        self.client.login(username='staff@example.com', password='staffpass123')
        
        response = self.client.get(reverse('test_dashboard:trends'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'اتجاهات وتحليلات الاختبارات')
    
    def test_notifications_view(self):
        """Test notifications view"""
        self.client.login(username='staff@example.com', password='staffpass123')
        

        TestNotification.objects.create(
            test_run=self.test_run,
            notification_type='test_failure',
            message='Test failed'
        )
        
        response = self.client.get(reverse('test_dashboard:notifications'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test failed')
    
    def test_api_test_stats(self):
        """Test API test stats endpoint"""
        self.client.login(username='staff@example.com', password='staffpass123')
        
        response = self.client.get(reverse('test_dashboard:api_stats'))
        self.assertEqual(response.status_code, 200)
        

        data = response.json()
        self.assertIn('total_runs', data)
        self.assertIn('success_rate', data)
    
    def test_api_run_tests(self):
        """Test API run tests endpoint"""
        self.client.login(username='staff@example.com', password='staffpass123')
        
        response = self.client.post(reverse('test_dashboard:api_run_tests'), {
            'test_type': 'unit'
        })
        self.assertEqual(response.status_code, 200)
        

        data = response.json()
        self.assertIn('status', data)


class PermissionTestCase(TestCase):
    """Test view permissions"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        

        self.regular_user = User.objects.create_user(
            email='user@example.com',
            password='userpass123'
        )
        
        self.staff_user = User.objects.create_user(
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )
        
        self.superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
    
    def test_anonymous_user_access(self):
        """Test anonymous user access to protected views"""
        protected_urls = [
            reverse('transactions:deposit_money'),
            reverse('transactions:withdraw_money'),
            reverse('transactions:transaction_report'),
            reverse('test_dashboard:dashboard'),
        ]
        
        for url in protected_urls:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 302)
    
    def test_staff_only_views(self):
        """Test staff-only views"""
        staff_only_urls = [
            reverse('transactions:user_search'),
            reverse('transactions:transaction_search'),
            reverse('test_dashboard:dashboard'),
        ]
        

        self.client.login(username='user@example.com', password='userpass123')
        for url in staff_only_urls:
            response = self.client.get(url)

            self.assertIn(response.status_code, [302, 403])
        

        self.client.login(username='staff@example.com', password='staffpass123')
        for url in staff_only_urls:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)


@pytest.mark.django_db
class TestViewsPytest:
    """Pytest-style view tests"""
    
    def test_home_view_template_used(self, client):
        """Test home view uses correct template"""
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert 'core/home.html' in [t.name for t in response.templates]
    
    def test_view_context_processors(self, client):
        """Test view context processors"""
        response = client.get(reverse('home'))
        

        assert 'request' in response.context
    
    def test_form_error_handling(self, client):
        """Test form error handling in views"""

        response = client.post(reverse('accounts:user_registration'), {
            'email': 'invalid-email',
            'password1': 'short',
            'password2': 'different'
        })
        
        assert response.status_code == 200

        assert 'form' in response.context
        form = response.context['form']
        assert not form.is_valid()
    
    def test_message_framework(self, client):
        """Test Django message framework usage"""

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
        
        client.login(username='test@example.com', password='testpass123')
        

        response = client.post(reverse('transactions:deposit_money'), {
            'amount': Decimal('500.00'),
            'transaction_type': DEPOSIT
        }, follow=True)
        

        messages = list(get_messages(response.wsgi_request))
        assert len(messages) > 0
        assert any('نجح' in str(message) or 'تم' in str(message) for message in messages)