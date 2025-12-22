"""
اختبارات النماذج (Models) للنظام المصرفي
"""

import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from decimal import Decimal
from datetime import date, datetime

from accounts.models import BankAccountType, UserBankAccount, UserAddress
from transactions.models import Transaction

User = get_user_model()


class UserModelTest(TestCase):
    """اختبارات نموذج المستخدم"""
    
    def test_create_user(self):
        """اختبار إنشاء مستخدم جديد"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='أحمد',
            last_name='محمد'
        )
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'أحمد')
        self.assertEqual(user.last_name, 'محمد')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """اختبار إنشاء مستخدم إداري"""
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
    
    def test_user_string_representation(self):
        """اختبار تمثيل المستخدم كنص"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        self.assertEqual(str(user), 'test@example.com')
    
    def test_email_required(self):
        """اختبار أن البريد الإلكتروني مطلوب"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                password='testpass123'
            )
    
    def test_unique_email(self):
        """اختبار أن البريد الإلكتروني فريد"""
        User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email='test@example.com',
                password='anotherpass123'
            )


class BankAccountTypeModelTest(TestCase):
    """اختبارات نموذج نوع الحساب البنكي"""
    
    def test_create_account_type(self):
        """اختبار إنشاء نوع حساب بنكي"""
        account_type = BankAccountType.objects.create(
            name='حساب توفير',
            maximum_withdrawal_amount=Decimal('5000.00'),
            annual_interest_rate=Decimal('3.5'),
            interest_calculation_per_year=12
        )
        
        self.assertEqual(account_type.name, 'حساب توفير')
        self.assertEqual(account_type.maximum_withdrawal_amount, Decimal('5000.00'))
        self.assertEqual(account_type.annual_interest_rate, Decimal('3.5'))
        self.assertEqual(account_type.interest_calculation_per_year, 12)
    
    def test_account_type_string_representation(self):
        """اختبار تمثيل نوع الحساب كنص"""
        account_type = BankAccountType.objects.create(
            name='حساب جاري',
            maximum_withdrawal_amount=Decimal('10000.00'),
            annual_interest_rate=Decimal('1.0'),
            interest_calculation_per_year=4
        )
        
        self.assertEqual(str(account_type), 'حساب جاري')
    
    def test_account_type_required_fields(self):
        """اختبار الحقول المطلوبة لنوع الحساب"""
        
        account_type = BankAccountType.objects.create(
            name='حساب اختبار',
            maximum_withdrawal_amount=Decimal('5000.00'),
            annual_interest_rate=Decimal('3.5'),
            interest_calculation_per_year=12
        )
        
        self.assertIsNotNone(account_type)
        self.assertGreater(account_type.maximum_withdrawal_amount, 0)


class UserBankAccountModelTest(TestCase):
    """اختبارات نموذج الحساب البنكي للمستخدم"""
    
    def setUp(self):
        """إعداد البيانات للاختبارات"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='أحمد',
            last_name='محمد'
        )
        
        self.account_type = BankAccountType.objects.create(
            name='حساب توفير',
            maximum_withdrawal_amount=Decimal('5000.00'),
            annual_interest_rate=Decimal('3.5'),
            interest_calculation_per_year=12
        )
    
    def test_create_bank_account(self):
        """اختبار إنشاء حساب بنكي"""
        bank_account = UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no=1000001,
            gender='M',
            birth_date=date(1990, 1, 1),
            initial_deposit_date=date.today(),
            interest_start_date=date.today()
        )
        
        self.assertEqual(bank_account.user, self.user)
        self.assertEqual(bank_account.account_type, self.account_type)
        self.assertEqual(bank_account.account_no, 1000001)
        self.assertEqual(bank_account.gender, 'M')
        self.assertEqual(bank_account.balance, Decimal('0.00'))
    
    def test_bank_account_string_representation(self):
        """اختبار تمثيل الحساب البنكي كنص"""
        bank_account = UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no=1000001,
            gender='M'
        )
        
        self.assertEqual(str(bank_account), '1000001')
    
    def test_unique_account_number(self):
        """اختبار أن رقم الحساب فريد"""
        UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no=1000001,
            gender='M'
        )
        
        
        another_user = User.objects.create_user(
            email='another@example.com',
            password='testpass123'
        )
        
        with self.assertRaises(IntegrityError):
            UserBankAccount.objects.create(
                user=another_user,
                account_type=self.account_type,
                account_no=1000001,  
                gender='F'
            )
    
    def test_one_account_per_user(self):
        """اختبار أن المستخدم لا يمكن أن يكون له أكثر من حساب واحد"""
        UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no=1000001,
            gender='M'
        )
        
        with self.assertRaises(IntegrityError):
            UserBankAccount.objects.create(
                user=self.user,  
                account_type=self.account_type,
                account_no=1000002,
                gender='M'
            )


class UserAddressModelTest(TestCase):
    """اختبارات نموذج عنوان المستخدم"""
    
    def setUp(self):
        """إعداد البيانات للاختبارات"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_user_address(self):
        """اختبار إنشاء عنوان للمستخدم"""
        address = UserAddress.objects.create(
            user=self.user,
            street_address='شارع الملك فهد، حي النخيل',
            city='الرياض',
            postal_code='12345',
            country='السعودية'
        )
        
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.street_address, 'شارع الملك فهد، حي النخيل')
        self.assertEqual(address.city, 'الرياض')
        self.assertEqual(address.postal_code, '12345')
        self.assertEqual(address.country, 'السعودية')
    
    def test_address_string_representation(self):
        """اختبار تمثيل العنوان كنص"""
        address = UserAddress.objects.create(
            user=self.user,
            street_address='شارع الملك فهد',
            city='الرياض',
            postal_code='12345',
            country='السعودية'
        )
        
        
        self.assertEqual(str(address), self.user.email)
    
    def test_one_address_per_user(self):
        """اختبار أن المستخدم لا يمكن أن يكون له أكثر من عنوان واحد"""
        UserAddress.objects.create(
            user=self.user,
            street_address='شارع الملك فهد',
            city='الرياض',
            postal_code='12345',
            country='السعودية'
        )
        
        with self.assertRaises(IntegrityError):
            UserAddress.objects.create(
                user=self.user,  
                street_address='شارع آخر',
                city='جدة',
                postal_code='54321',
                country='السعودية'
            )


class TransactionModelTest(TestCase):
    """اختبارات نموذج المعاملات"""
    
    def setUp(self):
        """إعداد البيانات للاختبارات"""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        
        self.account_type = BankAccountType.objects.create(
            name='حساب توفير',
            maximum_withdrawal_amount=Decimal('5000.00'),
            annual_interest_rate=Decimal('3.5'),
            interest_calculation_per_year=12
        )
        
        self.bank_account = UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no=1000001,
            gender='M'
        )
    
    def test_create_deposit_transaction(self):
        """اختبار إنشاء معاملة إيداع"""
        transaction = Transaction.objects.create(
            account=self.bank_account,
            amount=Decimal('1000.00'),
            balance_after_transaction=Decimal('1000.00'),
            transaction_type=1  
        )
        
        self.assertEqual(transaction.account, self.bank_account)
        self.assertEqual(transaction.amount, Decimal('1000.00'))
        self.assertEqual(transaction.balance_after_transaction, Decimal('1000.00'))
        self.assertEqual(transaction.transaction_type, 1)
        self.assertIsNotNone(transaction.timestamp)
    
    def test_create_withdrawal_transaction(self):
        """اختبار إنشاء معاملة سحب"""
        
        self.bank_account.balance = Decimal('2000.00')
        self.bank_account.save()
        
        transaction = Transaction.objects.create(
            account=self.bank_account,
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00'),
            transaction_type=2  
        )
        
        self.assertEqual(transaction.account, self.bank_account)
        self.assertEqual(transaction.amount, Decimal('500.00'))
        self.assertEqual(transaction.balance_after_transaction, Decimal('1500.00'))
        self.assertEqual(transaction.transaction_type, 2)
    
    def test_transaction_string_representation(self):
        """اختبار تمثيل المعاملة كنص"""
        transaction = Transaction.objects.create(
            account=self.bank_account,
            amount=Decimal('1000.00'),
            balance_after_transaction=Decimal('1000.00'),
            transaction_type=1
        )
        
        
        expected_str = f"{self.bank_account.account_no} - إيداع"
        self.assertEqual(str(transaction), expected_str)
    
    def test_transaction_ordering(self):
        """اختبار ترتيب المعاملات حسب التاريخ"""
        
        transaction1 = Transaction.objects.create(
            account=self.bank_account,
            amount=Decimal('1000.00'),
            balance_after_transaction=Decimal('1000.00'),
            transaction_type=1
        )
        
        transaction2 = Transaction.objects.create(
            account=self.bank_account,
            amount=Decimal('500.00'),
            balance_after_transaction=Decimal('1500.00'),
            transaction_type=1
        )
        
        
        transactions = Transaction.objects.all()
        self.assertEqual(transactions[0], transaction1)
        self.assertEqual(transactions[1], transaction2)