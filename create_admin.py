import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicare.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Retrieve credentials from environment variables or default to fallback credentials
username = os.environ.get('SUPERUSER_USERNAME', 'admin')
email = os.environ.get('SUPERUSER_EMAIL', 'admin@medicare-hospital.com')
password = os.environ.get('SUPERUSER_PASSWORD', 'AdminPass123!')

# Retrieve or create user
user, created = User.objects.get_or_create(username=username, defaults={'email': email})

# Force password, role, and staff privileges
user.set_password(password)
user.role = 'Admin'
user.is_staff = True
user.is_superuser = True
user.is_active = True
user.save()

if created:
    print(f"STATUS: Admin superuser '{username}' was successfully created.")
else:
    print(f"STATUS: Admin superuser '{username}' credentials were reset and updated.")

