"""
Test cases for search functionality
"""
import pytest
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import UserBankAccount, BankAccountType
from transactions.models import Transaction
from transactions.constants import DEPOSIT, WITHDRAWAL

User = get_user_model()


class SearchFunctionalityTestCase(TestCase):
    """Test search functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        

        self.account_type = BankAccountType.objects.create(
            name='Savings Account',
            maximum_withdrawal_amount=5000,
            annual_interest_rate=Decimal("2.5"),
            interest_calculation_per_year=12
        )
        

        self.user1 = User.objects.create_user(
            email='john.doe@example.com',
            first_name='John',
            last_name='Doe',
            password='testpass123'
        )
        
        self.user2 = User.objects.create_user(
            email='jane.smith@example.com',
            first_name='Jane',
            last_name='Smith',
            password='testpass123'
        )
        
        self.user3 = User.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='testpass123',
            is_staff=True
        )
        

        self.account1 = UserBankAccount.objects.create(
            user=self.user1,
            account_type=self.account_type,
            account_no='1111111111',
            balance=Decimal('1000.00')
        )
        
        self.account2 = UserBankAccount.objects.create(
            user=self.user2,
            account_type=self.account_type,
            account_no='2222222222',
            balance=Decimal('2000.00')
        )
        

        Transaction.objects.create(
            account=self.account1,
            transaction_type=DEPOSIT,
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00')
        )
        
        Transaction.objects.create(
            account=self.account1,
            transaction_type=WITHDRAWAL,
            amount=Decimal('200.00'),
            balance_after_transaction=Decimal('1300.00')
        )
        
        Transaction.objects.create(
            account=self.account2,
            transaction_type=DEPOSIT,
            amount=Decimal('750.00'),
            balance_after_transaction=Decimal('2750.00')
        )
        

        self.client.login(username='admin@example.com', password='testpass123')
    
    def test_user_search_by_email(self):
        """Test searching users by email"""
        response = self.client.get(reverse('transactions:user_search'), {
            'search': 'john.doe'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'john.doe@example.com')
        self.assertNotContains(response, 'jane.smith@example.com')
    
    def test_user_search_by_first_name(self):
        """Test searching users by first name"""
        response = self.client.get(reverse('transactions:user_search'), {
            'search': 'Jane'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'jane.smith@example.com')
        self.assertNotContains(response, 'john.doe@example.com')
    
    def test_user_search_by_last_name(self):
        """Test searching users by last name"""
        response = self.client.get(reverse('transactions:user_search'), {
            'search': 'Smith'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'jane.smith@example.com')
        self.assertNotContains(response, 'john.doe@example.com')
    
    def test_user_search_no_results(self):
        """Test user search with no results"""
        response = self.client.get(reverse('transactions:user_search'), {
            'search': 'nonexistent'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'لا توجد نتائج')
    
    def test_transaction_search_by_amount(self):
        """Test searching transactions by amount"""
        response = self.client.get(reverse('transactions:transaction_search'), {
            'search': '500'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '500.00')
    
    def test_transaction_search_by_type(self):
        """Test searching transactions by type"""
        response = self.client.get(reverse('transactions:transaction_search'), {
            'transaction_type': str(DEPOSIT)
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'إيداع')

        self.assertContains(response, '500.00')
        self.assertContains(response, '750.00')
    
    def test_transaction_search_by_account(self):
        """Test searching transactions by account"""
        response = self.client.get(reverse('transactions:transaction_search'), {
            'account_search': '1111111111'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '1111111111')
        self.assertContains(response, 'john.doe@example.com')
        self.assertNotContains(response, '2222222222')
    
    def test_transaction_search_by_user_email(self):
        """Test searching transactions by user email"""
        response = self.client.get(reverse('transactions:transaction_search'), {
            'account_search': 'jane.smith'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'jane.smith@example.com')
        self.assertContains(response, '750.00')
    
    def test_combined_transaction_search(self):
        """Test combined search criteria"""
        response = self.client.get(reverse('transactions:transaction_search'), {
            'transaction_type': str(DEPOSIT),
            'account_search': 'john.doe'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '500.00')  # John's deposit
        self.assertNotContains(response, '200.00')  # John's withdrawal
        self.assertNotContains(response, '750.00')  # Jane's deposit
    
    def test_transaction_report_search_for_user(self):
        """Test transaction report search for logged-in user"""

        self.client.login(username='john.doe@example.com', password='testpass123')
        
        response = self.client.get(reverse('transactions:transaction_report'), {
            'search': '500'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '500.00')

        self.assertNotContains(response, '750.00')
    
    def test_search_pagination(self):
        """Test search results pagination"""

        for i in range(15):
            User.objects.create_user(
                email=f'user{i}@example.com',
                first_name=f'User{i}',
                password='testpass123'
            )
        
        response = self.client.get(reverse('transactions:user_search'), {
            'search': 'user'
        })
        
        self.assertEqual(response.status_code, 200)

        if response.context['is_paginated']:
            self.assertContains(response, 'من')  # Arabic pagination text


@pytest.mark.django_db
class TestSearchFunctionalityPytest:
    """Pytest-style search functionality tests"""
    
    def test_user_search_queryset_filtering(self):
        """Test user search queryset filtering logic"""
        from transactions.views import UserSearchView
        

        user1 = User.objects.create_user(
            email='test1@example.com',
            first_name='Test',
            last_name='One',
            password='pass123'
        )
        
        user2 = User.objects.create_user(
            email='test2@example.com',
            first_name='Another',
            last_name='User',
            password='pass123'
        )
        

        view = UserSearchView()
        view.request = type('Request', (), {'GET': {'search': 'Test'}})()
        
        queryset = view.get_queryset()
        

        assert user1 in queryset
        assert user2 not in queryset
    
    def test_transaction_search_queryset_filtering(self):
        """Test transaction search queryset filtering logic"""
        from transactions.views import TransactionSearchView
        

        user = User.objects.create_user(
            email='test@example.com',
            password='pass123'
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
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00')
        )
        
        transaction2 = Transaction.objects.create(
            account=account,
            transaction_type=WITHDRAWAL,
            amount=Decimal('200.00'),
            balance_after_transaction=Decimal('1300.00')
        )
        

        view = TransactionSearchView()
        view.request = type('Request', (), {
            'GET': {'transaction_type': str(DEPOSIT)}
        })()
        
        queryset = view.get_queryset()
        
        assert transaction1 in queryset
        assert transaction2 not in queryset