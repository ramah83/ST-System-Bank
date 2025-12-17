"""
Test cases for user authentication functionality
"""
import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import UserBankAccount, UserAddress
from accounts.forms import UserRegistrationForm, UserAddressForm

User = get_user_model()


class AuthenticationTestCase(TestCase):
    """Test user authentication functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'gender': 'M',
            'birth_date': '1990-01-01',
        }
        self.address_data = {
            'street_address': '123 Test Street',
            'city': 'Test City',
            'postal_code': '12345',
            'country': 'Test Country',
        }
    
    def test_user_registration_success(self):
        """Test successful user registration"""

        registration_form = UserRegistrationForm(data=self.user_data)
        address_form = UserAddressForm(data=self.address_data)
        
        self.assertTrue(registration_form.is_valid())
        self.assertTrue(address_form.is_valid())
        

        response = self.client.post(reverse('accounts:user_registration'), {
            **self.user_data,
            **self.address_data
        })
        

        self.assertTrue(User.objects.filter(email='test@example.com').exists())
        user = User.objects.get(email='test@example.com')
        

        self.assertTrue(hasattr(user, 'account'))
        self.assertIsInstance(user.account, UserBankAccount)
        

        self.assertTrue(UserAddress.objects.filter(user=user).exists())
    
    def test_user_registration_invalid_data(self):
        """Test user registration with invalid data"""
        invalid_data = self.user_data.copy()
        invalid_data['email'] = 'invalid-email'
        invalid_data['password2'] = 'different-password'
        
        registration_form = UserRegistrationForm(data=invalid_data)
        self.assertFalse(registration_form.is_valid())
        self.assertIn('email', registration_form.errors)
        self.assertIn('password2', registration_form.errors)
    
    def test_user_login_success(self):
        """Test successful user login"""

        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        

        response = self.client.post(reverse('accounts:user_login'), {
            'username': 'test@example.com',
            'password': 'testpass123'
        })
        

        self.assertTrue('_auth_user_id' in self.client.session)
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('accounts:user_login'), {
            'username': 'nonexistent@example.com',
            'password': 'wrongpassword'
        })
        

        self.assertFalse('_auth_user_id' in self.client.session)
    
    def test_user_logout(self):
        """Test user logout"""

        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='test@example.com', password='testpass123')
        

        response = self.client.get(reverse('accounts:user_logout'))
        

        self.assertFalse('_auth_user_id' in self.client.session)
    
    def test_authenticated_user_redirect(self):
        """Test that authenticated users are redirected from registration"""

        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='test@example.com', password='testpass123')
        

        response = self.client.get(reverse('accounts:user_registration'))
        

        self.assertEqual(response.status_code, 302)


@pytest.mark.django_db
class TestAuthenticationPytest:
    """Pytest-style authentication tests"""
    
    def test_user_creation(self):
        """Test user creation with pytest"""
        user = User.objects.create_user(
            email='pytest@example.com',
            password='testpass123'
        )
        assert user.email == 'pytest@example.com'
        assert user.check_password('testpass123')
    
    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        assert str(user) == 'test@example.com'