set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# AUTO CREATE ADMIN USER
echo "Creating admin user..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
email = 'admin@lawportal.com'
password = 'Admin@123456'

if User.objects.filter(username=username).exists():
    print(f'User {username} already exists')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully!')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print('Please change this password after first login!')
EOF

echo "Build complete!"