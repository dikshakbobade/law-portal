#!/usr/bin/env python
"""
Automated setup script for Render deployment
Run: python setup_render.py
"""

import os
import subprocess

def create_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created {filename}")

print("🚀 Setting up Law Portal for Render deployment\n")

# 1. Create runtime.txt with FULL Python version
runtime_content = "python-3.10.12"
create_file("runtime.txt", runtime_content)

# 2. Create build.sh
build_content = """#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create default superuser (optional)
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@lawportal.com', 'admin123')
    print('Superuser created!')
EOF
"""
create_file("build.sh", build_content)

# 3. Create render.yaml
render_yaml = """databases:
  - name: law-portal-db
    databaseName: law_portal_db
    user: law_portal_user
    region: oregon

services:
  - type: web
    name: law-portal
    runtime: python
    region: oregon
    plan: free
    buildCommand: "./build.sh"
    startCommand: "gunicorn law_portal.wsgi:application"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: law-portal-db
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: PYTHON_VERSION
        value: 3.10.12
      - key: DEBUG
        value: False
"""
create_file("render.yaml", render_yaml)

# 4. Update requirements.txt
requirements = """Django==4.2.7
djangorestframework==3.14.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
gunicorn==21.2.0
whitenoise==6.5.0
dj-database-url==2.1.0
Pillow==10.0.1
"""
create_file("requirements.txt", requirements)

# 5. Make build.sh executable (for Unix systems)
if os.name != 'nt':  # Not Windows
    subprocess.run("chmod +x build.sh", shell=True)

print("\n✅ All files created successfully!")
print("\n" + "="*50)
print("📋 NEXT STEPS:")
print("="*50)
print("\n1. Update your settings.py with the provided code")
print("\n2. Commit and push to GitHub:")
print("   git add .")
print('   git commit -m "Configure for Render deployment"')
print("   git push origin main")
print("\n3. Go to Render.com and:")
print("   - Click 'New +' → 'Web Service'")
print("   - Connect your GitHub repository")
print("   - Render will auto-detect settings from render.yaml")
print("\n4. Your app will be live at:")
print("   https://law-portal.onrender.com")
print("\n✨ That's it! Your app will deploy automatically!")