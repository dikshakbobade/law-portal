from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get credentials from environment or use defaults
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@lawportal.com')
        password = os.environ.get('ADMIN_PASSWORD', 'Admin@123456')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" already exists'))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created admin user "{username}"'))
            self.stdout.write(self.style.WARNING(f'Password: {password}'))
            self.stdout.write(self.style.WARNING('⚠️  Change this password after first login!'))