
from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_admin_user(request):
    """
    Temporary view to create admin user
    DELETE THIS AFTER CREATING ADMIN!
    """
    # Security check - only allow if no admin exists
    User = get_user_model()
    
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse("Admin already exists!")
    
    # Create admin user
    user = User.objects.create_superuser(
        username='admin',
        email='admin@lawportal.com',
        password='Admin@123456'  # CHANGE THIS!
    )
    
    html = """
    <html>
    <body style="font-family: Arial; padding: 50px; background: #f0f0f0;">
        <div style="max-width: 500px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
            <h2 style="color: #28a745;">✅ Admin User Created Successfully!</h2>
            <hr>
            <p><strong>Username:</strong> admin</p>
            <p><strong>Password:</strong> Admin@123456</p>
            <hr>
            <p style="color: #dc3545;"><strong>⚠️ IMPORTANT:</strong></p>
            <ul>
                <li>Change this password immediately after login!</li>
                <li>Delete this URL from urls.py after use!</li>
                <li>Remove this view from views.py!</li>
            </ul>
            <a href="/admin/" style="display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;">Go to Admin Panel</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


# Also add this safer version that requires a secret key
def create_admin_secure(request):
    """Secure version with secret key"""
    secret = request.GET.get('secret', '')
    
    # Check secret key
    if secret != 'mysecretkey123':  # Change this!
        return HttpResponse("Unauthorized", status=403)
    
    User = get_user_model()
    
    if User.objects.filter(username='admin').exists():
        return HttpResponse("Admin already exists!")
    
    User.objects.create_superuser(
        username='admin',
        email='admin@lawportal.com',
        password='Admin@123456'
    )
    
    return HttpResponse("Admin created! Username: admin, Password: Admin@123456")