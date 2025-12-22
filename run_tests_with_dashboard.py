import os
import sys
import django
import subprocess
from datetime import datetime

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from django.utils import timezone
from test_dashboard.models import TestRun, TestCase, TestNotification


def run_tests_with_integration():
    """تشغيل الاختبارات مع تكامل Test Dashboard"""
    
    print("🚀 بدء تشغيل الاختبارات مع تسجيل النتائج...")
    print("=" * 60)
    
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            '-v',
            '--tb=short',
            '--disable-warnings',
            '-p', 'pytest_integration',
            'tests/'
        ], capture_output=False, text=True)
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الاختبارات: {e}")
        return 1


def show_latest_results():
    """عرض آخر نتائج الاختبارات"""
    print("\n" + "=" * 60)
    print("📊 آخر نتائج الاختبارات:")
    
    latest_run = TestRun.objects.order_by('-start_time').first()
    
    if latest_run:
        print(f"🆔 معرف التشغيل: {latest_run.id}")
        print(f"📅 التاريخ: {latest_run.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏱️  المدة: {latest_run.duration:.2f} ثانية")
        print(f"📈 الحالة: {latest_run.status}")
        print(f"📊 الإحصائيات:")
        print(f"   - إجمالي: {latest_run.total_tests}")
        print(f"   - نجح: {latest_run.passed_tests}")
        print(f"   - فشل: {latest_run.failed_tests}")
        print(f"   - خطأ: {latest_run.error_tests}")
        
        if latest_run.coverage_percentage:
            print(f"   - التغطية: {latest_run.coverage_percentage}%")
        
        success_rate = (latest_run.passed_tests / latest_run.total_tests * 100) if latest_run.total_tests > 0 else 0
        print(f"   - معدل النجاح: {success_rate:.1f}%")
        
        print(f"\n🌐 يمكنك مشاهدة النتائج على:")
        print(f"   - Test Dashboard: http://127.0.0.1:8000/test-dashboard/")
        print(f"   - Test Trends: http://127.0.0.1:8000/test-dashboard/trends/")
        
    else:
        print("❌ لا توجد نتائج اختبارات مسجلة")


def main():
    """الدالة الرئيسية"""
    print("🧪 مشغل الاختبارات مع Test Dashboard Integration")
    print("=" * 60)
    
    print("الخيارات المتاحة:")
    print("1. تشغيل جميع الاختبارات")
    print("2. تشغيل اختبارات النماذج فقط")
    print("3. تشغيل اختبارات سريعة (بدون coverage)")
    print("4. عرض آخر النتائج")
    print("5. تشغيل اختبار واحد")
    
    choice = input("\nاختر رقم الخيار (1-5): ").strip()
    
    if choice == '1':
        print("\n🚀 تشغيل جميع الاختبارات...")
        exit_code = run_tests_with_integration()
        
    elif choice == '2':
        print("\n🚀 تشغيل اختبارات النماذج...")
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            '-v', '--tb=short', '--disable-warnings',
            '-p', 'pytest_integration',
            'tests/test_models.py'
        ])
        exit_code = result.returncode
        
    elif choice == '3':
        print("\n🚀 تشغيل اختبارات سريعة...")
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            '-v', '--tb=short', '--disable-warnings',
            '--no-cov',
            '-p', 'pytest_integration',
            'tests/'
        ])
        exit_code = result.returncode
        
    elif choice == '4':
        show_latest_results()
        return 0
        
    elif choice == '5':
        test_name = input("أدخل اسم الاختبار (مثال: test_user_creation): ").strip()
        if test_name:
            print(f"\n🚀 تشغيل الاختبار: {test_name}")
            result = subprocess.run([
                sys.executable, '-m', 'pytest',
                '-v', '--tb=short', '--disable-warnings',
                '-p', 'pytest_integration',
                '-k', test_name,
                'tests/'
            ])
            exit_code = result.returncode
        else:
            print("❌ لم تدخل اسم اختبار صحيح")
            return 1
    else:
        print("❌ خيار غير صحيح")
        return 1
    
    if exit_code == 0:
        print("\n✅ تمت الاختبارات بنجاح!")
    else:
        print(f"\n❌ فشلت الاختبارات (كود الخروج: {exit_code})")
    
    show_latest_results()
    return exit_code


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)