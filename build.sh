#!/usr/bin/env bash
# build.sh - Fixed version for Render

set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create staticfiles directory
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --no-input

# Make migrations (in case any are missing)
python manage.py makemigrations --no-input || true

# Apply database migrations
python manage.py migrate --no-input

# Create superuser (only if doesn't exist)
python manage.py shell <<EOF || true
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@lawportal.com', 'Admin@123456')
    print('Admin user created!')
EOF

echo "Build completed successfully!"