"""
WSGI config for factors_Ecom project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'factors_Ecom.settings')

# Auto-create superuser on startup if environment variables are set
def create_superuser_if_needed():
    """
    Automatically create superuser if environment variables are set.
    This runs on application startup in production.
    """
    try:
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        from django.core.management import call_command
        import os
        
        # Check if admin credentials are set
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')
        
        if admin_email and admin_password:
            User = get_user_model()
            
            # Check if superuser already exists
            if not User.objects.filter(email=admin_email, is_superuser=True).exists():
                try:
                    # Use the management command
                    call_command('create_admin', verbosity=0)
                    print(f" Superuser created: {admin_email}")
                except Exception as e:
                    print(f" Error creating superuser: {e}")
            else:
                print(f" Superuser already exists: {admin_email}")
                
    except Exception as e:
        print(f" Error in superuser creation: {e}")

# Create superuser on startup
create_superuser_if_needed()

application = get_wsgi_application()

app = application