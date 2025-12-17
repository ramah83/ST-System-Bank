
"""
Fix escaped quotes in test files
"""
import os

def fix_file(file_path):
    """Fix escaped quotes in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        

        original_content = content
        content = content.replace("Decimal(\\'2.5\\')", 'Decimal("2.5")')
        content = content.replace("Decimal(\\'1000\\')", 'Decimal("1000")')
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'Fixed {file_path}')
            return True
        else:
            print(f'No changes needed for {file_path}')
            return False
    except Exception as e:
        print(f'Error fixing {file_path}: {e}')
        return False

def main():
    """Main function"""
    files = [
        'tests/test_models.py', 
        'tests/test_forms.py', 
        'tests/test_views.py', 
        'tests/test_transactions.py', 
        'tests/test_search_functionality.py', 
        'tests/test_selenium.py'
    ]
    
    fixed_count = 0
    for file_path in files:
        if os.path.exists(file_path):
            if fix_file(file_path):
                fixed_count += 1
        else:
            print(f'File not found: {file_path}')
    
    print(f'\nFixed {fixed_count} files')

if __name__ == '__main__':
    main()