#!/usr/bin/env python
"""
Complete Setup Script for Law Portal Django Project
Run this script to create all project files automatically
"""

import os
import sys

def create_file(path, content):
    """Create a file with given content"""
    # Create directory if it doesn't exist
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created: {path}")

def setup_project():
    """Create all project files"""
    
    print("🚀 Creating Law Portal Project Files...\n")
    
    # 1. Create manage.py
    create_file('manage.py', '''#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'law_portal.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)''')
    
    # 2. Create law_portal/__init__.py
    create_file('law_portal/__init__.py', '')
    
    # 3. Create law_portal/urls.py
    create_file('law_portal/urls.py', '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('laws.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)''')
    
    # 4. Create law_portal/wsgi.py
    create_file('law_portal/wsgi.py', '''import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'law_portal.settings')
application = get_wsgi_application()''')
    
    # 5. Create law_portal/asgi.py
    create_file('law_portal/asgi.py', '''import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'law_portal.settings')
application = get_asgi_application()''')
    
    # 6. Create law_portal/settings.py
    create_file('law_portal/settings.py', '''from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-key-1234567890')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'laws',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'law_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'law_portal.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'law_portal_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}''')
    
    # 7. Create laws app files
    create_file('laws/__init__.py', '')
    
    # 8. Create laws/apps.py
    create_file('laws/apps.py', '''from django.apps import AppConfig

class LawsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'laws'
    verbose_name = 'Laws Management' ''')
    
    # 9. Create simplified laws/models.py
    create_file('laws/models.py', '''from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Law(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='laws')
    summary = models.TextField()
    full_text = models.TextField()
    act_number = models.CharField(max_length=100, blank=True)
    section = models.CharField(max_length=100, blank=True)
    keywords = models.TextField(blank=True)
    jurisdiction = models.CharField(max_length=100, default="India")
    enacted_date = models.DateField(null=True, blank=True)
    last_amendment = models.DateField(null=True, blank=True)
    references = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Law"
        verbose_name_plural = "Laws"
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:340])
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_keywords_list(self):
        if self.keywords:
            return [k.strip() for k in self.keywords.split(',')]
        return []''')
    
    # 10. Create laws/admin.py
    create_file('laws/admin.py', '''from django.contrib import admin
from .models import Category, Law

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Law)
class LawAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'act_number', 'section', 'jurisdiction']
    list_filter = ['category', 'jurisdiction', 'enacted_date']
    search_fields = ['title', 'summary', 'keywords', 'act_number']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at' ''')
    
    # 11. Create simplified laws/views.py
    create_file('laws/views.py', '''from django.shortcuts import render, get_object_or_404
from .models import Category, Law

def index(request):
    categories = Category.objects.all()
    recent_laws = Law.objects.select_related('category').order_by('-created_at')[:10]
    context = {
        'categories': categories,
        'recent_laws': recent_laws,
    }
    return render(request, 'index.html', context)

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    laws = Law.objects.filter(category=category)
    context = {
        'category': category,
        'laws': laws,
    }
    return render(request, 'category_list.html', context)

def law_detail(request, slug):
    law = get_object_or_404(Law, slug=slug)
    related_laws = Law.objects.filter(category=law.category).exclude(id=law.id)[:5]
    context = {
        'law': law,
        'related_laws': related_laws,
    }
    return render(request, 'law_detail.html', context)

def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Law.objects.filter(
            title__icontains=query
        ) | Law.objects.filter(
            summary__icontains=query
        ) | Law.objects.filter(
            keywords__icontains=query
        )
        results = results.distinct()[:50]
    
    context = {
        'query': query,
        'results': results,
        'result_count': len(results),
    }
    return render(request, 'search_results.html', context)''')
    
    # 12. Create laws/urls.py
    create_file('laws/urls.py', '''from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category_list, name='category_detail'),
    path('law/<slug:slug>/', views.law_detail, name='law_detail'),
    path('search/', views.search, name='search'),
]''')
    
    # 13. Create laws/serializers.py
    create_file('laws/serializers.py', '''from rest_framework import serializers
from .models import Category, Law

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LawSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Law
        fields = '__all__' ''')
    
    # 14. Create management command
    create_file('laws/management/__init__.py', '')
    create_file('laws/management/commands/__init__.py', '')
    
    # 15. Create load_seed command
    create_file('laws/management/commands/load_seed.py', '''from django.core.management.base import BaseCommand
from laws.models import Category, Law
from datetime import datetime

class Command(BaseCommand):
    help = 'Load sample law data'
    
    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            'Criminal', 'Civil', 'Constitutional', 'Personal/Family',
            'Corporate/Commercial', 'Labour/Employment', 'Property/Land',
            'Taxation', 'Environmental', 'Cyber/Technology'
        ]
        
        for cat_name in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={'description': f'{cat_name} laws and regulations'}
            )
            if created:
                self.stdout.write(f'Created category: {cat_name}')
        
        # Create sample laws
        criminal_cat = Category.objects.get(name='Criminal')
        Law.objects.get_or_create(
            title='Indian Penal Code - Section 302',
            defaults={
                'category': criminal_cat,
                'summary': 'Punishment for murder',
                'full_text': 'Whoever commits murder shall be punished with death, or imprisonment for life.',
                'act_number': 'IPC 1860',
                'section': '302',
                'keywords': 'murder, punishment, death penalty',
                'jurisdiction': 'India',
                'enacted_date': datetime(1860, 10, 6).date(),
            }
        )
        
        civil_cat = Category.objects.get(name='Civil')
        Law.objects.get_or_create(
            title='Contract Act - Section 10',
            defaults={
                'category': civil_cat,
                'summary': 'What agreements are contracts',
                'full_text': 'All agreements are contracts if they are made by free consent of parties.',
                'act_number': 'Contract Act 1872',
                'section': '10',
                'keywords': 'contract, agreement, consent',
                'jurisdiction': 'India',
                'enacted_date': datetime(1872, 4, 25).date(),
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))''')
    
    # 16. Create migrations folder
    create_file('laws/migrations/__init__.py', '')
    
    # 17. Create templates
    create_file('templates/base.html', '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Law Portal{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">Law Portal</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/admin/">Admin</a>
                    </li>
                </ul>
                <form class="d-flex" action="/search/" method="get">
                    <input class="form-control me-2" type="search" name="q" placeholder="Search laws...">
                    <button class="btn btn-light" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>
    
    <main class="py-4">
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>
    
    <footer class="bg-dark text-light mt-5 py-4">
        <div class="container text-center">
            <p>&copy; 2024 Law Portal. All rights reserved.</p>
        </div>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>''')
    
    create_file('templates/index.html', '''{% extends 'base.html' %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1 class="mb-4">Welcome to Law Portal</h1>
        <p class="lead">Browse laws by category or search for specific laws.</p>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <h2>Categories</h2>
        <div class="row">
            {% for category in categories %}
            <div class="col-md-4 mb-3">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">{{ category.name }}</h5>
                        <p class="card-text">{{ category.description }}</p>
                        <a href="/category/{{ category.slug }}/" class="btn btn-primary">View Laws</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <h2>Recent Laws</h2>
        <div class="list-group">
            {% for law in recent_laws %}
            <a href="/law/{{ law.slug }}/" class="list-group-item list-group-item-action">
                <h5>{{ law.title }}</h5>
                <p>{{ law.summary|truncatewords:30 }}</p>
                <small>Category: {{ law.category.name }}</small>
            </a>
            {% empty %}
            <p>No laws added yet.</p>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}''')
    
    create_file('templates/category_list.html', '''{% extends 'base.html' %}

{% block title %}{{ category.name }} - Law Portal{% endblock %}

{% block content %}
<h1>{{ category.name }} Laws</h1>
<p>{{ category.description }}</p>

<div class="list-group mt-4">
    {% for law in laws %}
    <a href="/law/{{ law.slug }}/" class="list-group-item list-group-item-action">
        <h5>{{ law.title }}</h5>
        <p>{{ law.summary|truncatewords:30 }}</p>
        <small>Act: {{ law.act_number }} | Section: {{ law.section }}</small>
    </a>
    {% empty %}
    <p>No laws in this category yet.</p>
    {% endfor %}
</div>

<a href="/" class="btn btn-secondary mt-3">Back to Home</a>
{% endblock %}''')
    
    create_file('templates/law_detail.html', '''{% extends 'base.html' %}

{% block title %}{{ law.title }} - Law Portal{% endblock %}

{% block content %}
<h1>{{ law.title }}</h1>

<div class="card mt-4">
    <div class="card-body">
        <h5>Summary</h5>
        <p>{{ law.summary }}</p>
        
        <h5>Full Text</h5>
        <p>{{ law.full_text }}</p>
        
        <h5>Details</h5>
        <ul>
            <li><strong>Act Number:</strong> {{ law.act_number }}</li>
            <li><strong>Section:</strong> {{ law.section }}</li>
            <li><strong>Category:</strong> {{ law.category.name }}</li>
            <li><strong>Jurisdiction:</strong> {{ law.jurisdiction }}</li>
            <li><strong>Keywords:</strong> {{ law.keywords }}</li>
        </ul>
    </div>
</div>

<div class="mt-4">
    <h5>Related Laws</h5>
    <div class="list-group">
        {% for related in related_laws %}
        <a href="/law/{{ related.slug }}/" class="list-group-item list-group-item-action">
            {{ related.title }}
        </a>
        {% empty %}
        <p>No related laws found.</p>
        {% endfor %}
    </div>
</div>

<a href="/category/{{ law.category.slug }}/" class="btn btn-secondary mt-3">Back to {{ law.category.name }}</a>
{% endblock %}''')
    
    create_file('templates/search_results.html', '''{% extends 'base.html' %}

{% block title %}Search Results - Law Portal{% endblock %}

{% block content %}
<h1>Search Results</h1>
{% if query %}
<p>Results for: <strong>{{ query }}</strong></p>
<p>Found {{ result_count }} result(s)</p>
{% endif %}

<div class="list-group mt-4">
    {% for law in results %}
    <a href="/law/{{ law.slug }}/" class="list-group-item list-group-item-action">
        <h5>{{ law.title }}</h5>
        <p>{{ law.summary|truncatewords:30 }}</p>
        <small>Category: {{ law.category.name }}</small>
    </a>
    {% empty %}
    <p>No results found. Try different keywords.</p>
    {% endfor %}
</div>

<a href="/" class="btn btn-secondary mt-3">Back to Home</a>
{% endblock %}''')
    
    # 18. Create static files
    create_file('static/css/styles.css', '''/* Custom styles for Law Portal */
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.navbar-brand {
    font-weight: bold;
    font-size: 1.5rem;
}

.card {
    transition: transform 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

footer {
    margin-top: auto;
}

.list-group-item {
    transition: background-color 0.3s;
}

.list-group-item:hover {
    background-color: #f8f9fa;
}''')
    
    create_file('static/js/search.js', '''// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log('Law Portal loaded');
});''')
    
    # 19. Create .env file
    create_file('.env', '''# Django Settings
SECRET_KEY=django-insecure-your-secret-key-change-this-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=law_portal_db
DB_USER=postgres
DB_PASSWORD=YOUR_PASSWORD_HERE
DB_HOST=localhost
DB_PORT=5432''')
    
    print("\n✅ All project files created successfully!")
    print("\n" + "="*50)
    print("📝 IMPORTANT NEXT STEPS:")
    print("="*50)
    print("\n1. EDIT .env FILE:")
    print("   Open .env file and change DB_PASSWORD to your PostgreSQL password")
    print("\n2. RUN THESE COMMANDS:")
    print("   python manage.py migrate")
    print("   python manage.py load_seed")
    print("   python manage.py createsuperuser")
    print("   python manage.py runserver")
    print("\n3. OPEN BROWSER:")
    print("   http://127.0.0.1:8000/")
    print("\n" + "="*50)

if __name__ == "__main__":
    setup_project()