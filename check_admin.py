#!/usr/bin/env python
"""
Diagnostic script to check superuser status in production.
Run this in Render Shell to debug admin login issues.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/opt/render/project/src')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'factors_Ecom.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model

def check_admin_status():
    """Check current admin users and environment variables."""
    
    print("=== DJANGO ADMIN DIAGNOSTIC ===\n")
    
    # Check environment variables
    print("🔍 Environment Variables:")
    admin_email = os.getenv('ADMIN_EMAIL')
    admin_password = os.getenv('ADMIN_PASSWORD')
    admin_username = os.getenv('ADMIN_USERNAME')
    
    print(f"ADMIN_EMAIL: {admin_email}")
    print(f"ADMIN_PASSWORD: {'*' * len(admin_password) if admin_password else 'NOT SET'}")
    print(f"ADMIN_USERNAME: {admin_username}")
    print()
    
    # Check database configuration
    print("🔍 Database Configuration:")
    from django.conf import settings
    db_config = settings.DATABASES['default']
    print(f"Database Engine: {db_config['ENGINE']}")
    print(f"Database Name: {db_config['NAME']}")
    print()
    
    # Check existing users
    print("🔍 Existing Users:")
    User = get_user_model()
    
    # All users
    all_users = User.objects.all()
    print(f"Total users in database: {all_users.count()}")
    
    # Superusers
    superusers = User.objects.filter(is_superuser=True)
    print(f"Superusers: {superusers.count()}")
    
    for user in superusers:
        print(f"  - Email: {user.email}")
        print(f"    Username: {user.username}")
        print(f"    is_active: {user.is_active}")
        print(f"    is_staff: {user.is_staff}")
        print(f"    is_admin: {user.is_admin}")
        print()
    
    # Check if expected admin exists
    if admin_email:
        try:
            admin_user = User.objects.get(email=admin_email)
            print(f"✅ User found with email: {admin_email}")
            print(f"   is_superuser: {admin_user.is_superuser}")
            print(f"   is_active: {admin_user.is_active}")
            print(f"   is_staff: {admin_user.is_staff}")
            
            if not admin_user.is_superuser:
                print("❌ User exists but is NOT a superuser!")
            elif not admin_user.is_active:
                print("❌ User exists but is NOT active!")
            else:
                print("✅ User is properly configured as superuser!")
                
        except User.DoesNotExist:
            print(f"❌ No user found with email: {admin_email}")
    
    print("\n=== RECOMMENDATIONS ===")
    
    if not admin_email or not admin_password:
        print("❌ Set ADMIN_EMAIL and ADMIN_PASSWORD environment variables")
    
    if superusers.count() == 0:
        print("❌ No superusers exist. Run: python manage.py create_admin")
    
    print("✅ To create superuser manually:")
    print("   python manage.py shell")
    print("   >>> from django.contrib.auth import get_user_model")
    print("   >>> User = get_user_model()")
    print(f"   >>> User.objects.create_superuser('admin', '{admin_email or 'admin@example.com'}', 'your-password')")

if __name__ == '__main__':
    check_admin_status()
