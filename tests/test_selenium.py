"""
Selenium automated tests for critical user flows
"""
import pytest
import time
from decimal import Decimal
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from accounts.models import UserBankAccount, BankAccountType

User = get_user_model()


class SeleniumTestCase(LiveServerTestCase):
    """Base class for Selenium tests"""
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        

        chrome_options = Options()
        chrome_options.add_argument('--headless')  
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        try:
            cls.selenium = webdriver.Chrome(options=chrome_options)
        except Exception:

            from selenium.webdriver.firefox.options import Options as FirefoxOptions
            firefox_options = FirefoxOptions()
            firefox_options.add_argument('--headless')
            cls.selenium = webdriver.Firefox(options=firefox_options)
        
        cls.selenium.implicitly_wait(10)
    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    
    def setUp(self):
        """Set up test data"""

        self.account_type = BankAccountType.objects.create(
            name='Savings Account',
            maximum_withdrawal_amount=5000,
            annual_interest_rate=Decimal("2.5"),
            interest_calculation_per_year=12
        )
        

        self.user = User.objects.create_user(
            email='selenium@example.com',
            password='testpass123',
            first_name='Selenium',
            last_name='Test'
        )
        

        self.account = UserBankAccount.objects.create(
            user=self.user,
            account_type=self.account_type,
            account_no='1234567890',
            balance=Decimal('1000.00')
        )


class UserAuthenticationSeleniumTest(SeleniumTestCase):
    """Test user authentication flows with Selenium"""
    
    def test_user_login_flow(self):
        """Test complete user login flow"""

        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        

        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        
        username_input.send_keys('selenium@example.com')
        password_input.send_keys('testpass123')
        

        login_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        

        WebDriverWait(self.selenium, 10).until(
            lambda driver: '/transactions/report/' in driver.current_url
        )
        

        self.assertIn('/transactions/report/', self.selenium.current_url)
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""

        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        

        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        
        username_input.send_keys('invalid@example.com')
        password_input.send_keys('wrongpassword')
        

        login_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'errorlist'))
        )
        

        error_element = self.selenium.find_element(By.CLASS_NAME, 'errorlist')
        self.assertTrue(error_element.is_displayed())


class TransactionSeleniumTest(SeleniumTestCase):
    """Test transaction flows with Selenium"""
    
    def login_user(self):
        """Helper method to login user"""
        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        
        username_input.send_keys('selenium@example.com')
        password_input.send_keys('testpass123')
        
        login_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        

        WebDriverWait(self.selenium, 10).until(
            lambda driver: '/transactions/report/' in driver.current_url
        )
    
    def test_deposit_money_flow(self):
        """Test complete deposit money flow"""
        self.login_user()
        

        self.selenium.get(f'{self.live_server_url}/transactions/deposit/')
        

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, 'amount'))
        )
        

        amount_input = self.selenium.find_element(By.NAME, 'amount')
        amount_input.send_keys('500')
        

        submit_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        

        WebDriverWait(self.selenium, 10).until(
            lambda driver: '/transactions/report/' in driver.current_url or 
                          driver.find_elements(By.CLASS_NAME, 'alert-success')
        )
        

        success = ('/transactions/report/' in self.selenium.current_url or 
                  len(self.selenium.find_elements(By.CLASS_NAME, 'alert-success')) > 0)
        self.assertTrue(success)
    
    def test_withdraw_money_flow(self):
        """Test complete withdraw money flow"""
        self.login_user()
        

        self.selenium.get(f'{self.live_server_url}/transactions/withdraw/')
        

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, 'amount'))
        )
        

        amount_input = self.selenium.find_element(By.NAME, 'amount')
        amount_input.send_keys('200')
        

        submit_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()
        

        WebDriverWait(self.selenium, 10).until(
            lambda driver: '/transactions/report/' in driver.current_url or 
                          driver.find_elements(By.CLASS_NAME, 'alert-success')
        )
        

        success = ('/transactions/report/' in self.selenium.current_url or 
                  len(self.selenium.find_elements(By.CLASS_NAME, 'alert-success')) > 0)
        self.assertTrue(success)
    
    def test_transaction_report_view(self):
        """Test transaction report page functionality"""
        self.login_user()
        


        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table'))
        )
        

        balance_elements = self.selenium.find_elements(By.CLASS_NAME, 'balance')
        if balance_elements:
            self.assertTrue(balance_elements[0].is_displayed())
        

        table = self.selenium.find_element(By.TAG_NAME, 'table')
        self.assertTrue(table.is_displayed())


class SearchFunctionalitySeleniumTest(SeleniumTestCase):
    """Test search functionality with Selenium"""
    
    def setUp(self):
        super().setUp()
        

        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )
    
    def login_admin(self):
        """Helper method to login admin user"""
        self.selenium.get(f'{self.live_server_url}/accounts/login/')
        
        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        
        username_input = self.selenium.find_element(By.NAME, 'username')
        password_input = self.selenium.find_element(By.NAME, 'password')
        
        username_input.send_keys('admin@example.com')
        password_input.send_keys('adminpass123')
        
        login_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        login_button.click()
        

        WebDriverWait(self.selenium, 10).until(
            lambda driver: '/transactions/report/' in driver.current_url
        )
    
    def test_user_search_functionality(self):
        """Test user search page functionality"""
        self.login_admin()
        

        self.selenium.get(f'{self.live_server_url}/transactions/search/users/')
        

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, 'search'))
        )
        

        search_input = self.selenium.find_element(By.NAME, 'search')
        search_input.send_keys('selenium')
        

        search_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()
        

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'table'))
        )
        

        page_source = self.selenium.page_source
        self.assertIn('selenium@example.com', page_source)
    
    def test_transaction_search_functionality(self):
        """Test transaction search page functionality"""
        self.login_admin()
        

        self.selenium.get(f'{self.live_server_url}/transactions/search/transactions/')
        

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, 'account_search'))
        )
        

        account_search = self.selenium.find_element(By.NAME, 'account_search')
        account_search.send_keys('1234567890')
        

        search_button = self.selenium.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()
        

        WebDriverWait(self.selenium, 10).until(
            lambda driver: driver.find_elements(By.TAG_NAME, 'table') or 
                          'لا توجد نتائج' in driver.page_source or
                          'ابدأ البحث' in driver.page_source
        )
        

        page_loaded = (len(self.selenium.find_elements(By.TAG_NAME, 'table')) > 0 or
                      'لا توجد نتائج' in self.selenium.page_source or
                      'ابدأ البحث' in self.selenium.page_source)
        self.assertTrue(page_loaded)


@pytest.mark.selenium
class TestSeleniumPytest:
    """Pytest-style Selenium tests"""
    
    @pytest.fixture(autouse=True)
    def setup_selenium(self, live_server):
        """Setup Selenium driver for pytest"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        self.selenium = webdriver.Chrome(options=chrome_options)
        self.selenium.implicitly_wait(10)
        self.live_server_url = live_server.url
        
        yield
        
        self.selenium.quit()
    
    @pytest.mark.django_db
    def test_homepage_loads(self):
        """Test that homepage loads correctly"""
        self.selenium.get(self.live_server_url)
        

        WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body'))
        )
        
        assert 'Banking' in self.selenium.title or 'مصرفي' in self.selenium.title