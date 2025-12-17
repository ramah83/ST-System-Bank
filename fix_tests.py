
"""
Fix all test files to include required BankAccountType fields
"""
import os
import re

def fix_bank_account_type_creation(file_path):
    """Fix BankAccountType.objects.create calls to include required fields"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    

    pattern = r'(BankAccountType\.objects\.create\(\s*name=\'[^\']+\',\s*maximum_withdrawal_amount=\d+)\s*\)'
    

    replacement = r'\1,\n            annual_interest_rate=Decimal(\'2.5\'),\n            interest_calculation_per_year=12\n        )'
    

    new_content = re.sub(pattern, replacement, content)
    

    pattern2 = r'(BankAccountType\.objects\.create\(\s*name=[\'"][^\'\"]+[\'"],\s*maximum_withdrawal_amount=\d+)\s*\)'
    new_content = re.sub(pattern2, replacement, new_content)
    

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {file_path}")
        return True
    return False

def main():
    """Main function to fix all test files"""
    
    test_files = [
        'tests/test_models.py',
        'tests/test_forms.py', 
        'tests/test_views.py',
        'tests/test_transactions.py',
        'tests/test_search_functionality.py',
        'tests/test_selenium.py'
    ]
    
    fixed_count = 0
    
    for file_path in test_files:
        if os.path.exists(file_path):
            if fix_bank_account_type_creation(file_path):
                fixed_count += 1
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nFixed {fixed_count} files")

if __name__ == '__main__':
    main()