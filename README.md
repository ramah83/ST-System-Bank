# Banking Management System

<div align="center">

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**Advanced Django-based banking management system with secure user authentication, real-time transaction processing, and multi-account management. Features a fully localized Arabic admin interface with animated UI, role-based access control, and automated balance tracking.**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [API](#api) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Security Features](#security-features)
- [Localization](#localization)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### 🏦 Core Banking Features
- **Multi-Account Management** - Support for multiple bank account types
- **Real-time Transactions** - Instant deposit and withdrawal processing
- **Balance Tracking** - Automated balance calculation and history
- **Transaction History** - Comprehensive transaction logs with filtering
- **Account Types** - Different account categories with specific rules

### 🔐 Security & Authentication
- **Secure User Authentication** - Django's built-in authentication system
- **Role-based Access Control** - Different permission levels for users and admins
- **Admin Restrictions** - Prevents admin users from performing financial transactions
- **Session Management** - Secure session handling and timeout
- **CSRF Protection** - Built-in protection against cross-site request forgery

### 🎨 Modern UI/UX
- **Responsive Design** - Mobile-first approach with responsive layouts
- **Animated Interface** - Smooth animations and transitions
- **Arabic Localization** - Fully localized Arabic interface (RTL support)
- **Modern Admin Panel** - Custom-designed admin interface with enhanced styling
- **Interactive Elements** - Hover effects, loading states, and user feedback

### ⚡ Performance & Scalability
- **Celery Integration** - Asynchronous task processing
- **Database Optimization** - Efficient queries and database design
- **Caching Support** - Ready for Redis/Memcached integration
- **Static File Management** - Optimized static file serving

---

## 🛠 Technology Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Django 4.x, Python 3.8+ |
| **Database** | SQLite (Development), PostgreSQL (Production Ready) |
| **Frontend** | HTML5, CSS3, JavaScript, TailwindCSS |
| **Task Queue** | Celery, Redis |
| **Authentication** | Django Auth, Session Management |
| **Localization** | Django i18n, Arabic (RTL) |
| **Styling** | Custom CSS, Animations, Responsive Design |

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/banking-management-system.git
   cd banking-management-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@localhost:5432/banking_db

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Celery Setup (Optional)

For asynchronous task processing:

```bash
# Start Celery worker
celery -A banking_system worker -l info

# Start Celery beat (for scheduled tasks)
celery -A banking_system beat -l info
```

---

## 📖 Usage

### User Registration & Authentication

1. **Register a new account**
   - Navigate to `/accounts/register/`
   - Fill in personal information
   - Verify email (if configured)

2. **Login**
   - Use email and password
   - Access dashboard after successful login

### Banking Operations

1. **Create Bank Account**
   - Navigate to account creation page
   - Select account type
   - Initial deposit (if required)

2. **Deposit Money**
   - Go to deposit page
   - Enter amount
   - Confirm transaction

3. **Withdraw Money**
   - Access withdrawal page
   - Enter amount (within balance limits)
   - Confirm transaction

4. **View Transaction History**
   - Access transaction history page
   - Filter by date, type, or amount
   - Export reports (if needed)

### Admin Operations

1. **User Management**
   - View all users
   - Edit user details
   - Activate/deactivate accounts

2. **Account Management**
   - View all bank accounts
   - Monitor balances
   - Account type management

3. **Transaction Monitoring**
   - View all transactions
   - Transaction details
   - System-generated reports

---

## 📁 Project Structure

```
banking-management-system/
├── 📁 accounts/                 # User accounts and authentication
│   ├── 📄 models.py            # User and bank account models
│   ├── 📄 views.py             # Authentication views
│   ├── 📄 forms.py             # User forms
│   ├── 📄 admin.py             # Admin configuration
│   └── 📁 migrations/          # Database migrations
├── 📁 transactions/            # Transaction management
│   ├── 📄 models.py            # Transaction models
│   ├── 📄 views.py             # Transaction views
│   ├── 📄 forms.py             # Transaction forms
│   ├── 📄 tasks.py             # Celery tasks
│   └── 📁 migrations/          # Database migrations
├── 📁 core/                    # Core application
│   ├── 📄 models.py            # Core models
│   ├── 📄 views.py             # Core views
│   └── 📁 migrations/          # Database migrations
├── 📁 banking_system/          # Project settings
│   ├── 📄 settings.py          # Django settings
│   ├── 📄 urls.py              # URL configuration
│   ├── 📄 celery.py            # Celery configuration
│   └── 📄 wsgi.py              # WSGI configuration
├── 📁 templates/               # HTML templates
│   ├── 📁 accounts/            # Account templates
│   ├── 📁 transactions/        # Transaction templates
│   ├── 📁 core/                # Core templates
│   └── 📁 admin/               # Custom admin templates
├── 📁 static/                  # Static files
│   ├── 📁 css/                 # Stylesheets
│   ├── 📁 js/                  # JavaScript files
│   └── 📁 images/              # Images
├── 📁 locale/                  # Localization files
│   └── 📁 ar/                  # Arabic translations
├── 📄 manage.py                # Django management script
├── 📄 requirements.txt         # Python dependencies
└── 📄 README.md                # This file
```

---

## 🔒 Security Features

### Authentication & Authorization
- **Secure Password Hashing** - Django's PBKDF2 algorithm
- **Session Security** - Secure session cookies and CSRF protection
- **Permission System** - Role-based access control
- **Admin Restrictions** - Financial transaction restrictions for admin users

### Data Protection
- **Input Validation** - Server-side validation for all forms
- **SQL Injection Prevention** - Django ORM protection
- **XSS Protection** - Template auto-escaping
- **HTTPS Ready** - SSL/TLS configuration support

### Financial Security
- **Transaction Integrity** - Atomic database transactions
- **Balance Validation** - Server-side balance checks
- **Audit Trail** - Complete transaction logging
- **Concurrent Access** - Database-level locking for critical operations

---

## 🌍 Localization

The system supports full Arabic localization with RTL (Right-to-Left) layout:

### Supported Languages
- **Arabic (ar)** - Complete translation with RTL support
- **English (en)** - Default language

### Translation Files
- `locale/ar/LC_MESSAGES/django.po` - Arabic translations
- Admin interface fully translated
- User interface with Arabic support

### Adding New Languages

1. **Create translation files**
   ```bash
   python manage.py makemessages -l <language_code>
   ```

2. **Translate strings**
   - Edit the `.po` files in `locale/<language_code>/LC_MESSAGES/`

3. **Compile translations**
   ```bash
   python manage.py compilemessages
   ```
