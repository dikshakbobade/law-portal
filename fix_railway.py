#!/usr/bin/env python
"""
Quick fix script for Railway deployment
Run: python fix_railway.py
"""

import os
import subprocess

def create_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)
    print(f"✅ Created {filename}")

# Install required packages
print("📦 Installing required packages...")
subprocess.run("pip install dj-database-url whitenoise gunicorn", shell=True)

# Create Procfile
procfile = "web: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn law_portal.wsgi:application"
create_file("Procfile", procfile)

# Create runtime.txt
create_file("runtime.txt", "python-3.10.12")

# Create railway.json
railway_json = """{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn law_portal.wsgi:application",
    "restartPolicyType": "ON_FAILURE"
  }
}"""
create_file("railway.json", railway_json)

# Update requirements.txt
print("📝 Updating requirements.txt...")
subprocess.run("pip freeze > requirements.txt", shell=True)

print("\n✅ Files created successfully!")
print("\n📋 Next steps:")
print("1. Make sure you've added PostgreSQL in Railway")
print("2. Update your settings.py with the code provided")
print("3. Run: git add .")
print("4. Run: git commit -m 'Fix Railway deployment'")
print("5. Run: git push origin main")
print("6. Railway will auto-deploy!")
