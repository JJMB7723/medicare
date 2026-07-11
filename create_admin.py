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

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password, role='Admin')
    print(f"STATUS: Admin superuser '{username}' was successfully created.")
else:
    print(f"STATUS: Admin superuser '{username}' already exists in database.")
