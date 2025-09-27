from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<slug:slug>/', views.category_list, name='category_detail'),
    path('law/<slug:slug>/', views.law_detail, name='law_detail'),
    path('search/', views.search, name='search'),

    # 🚨 Temporary URL for superuser creation
    path('create-admin-temp/', views.create_admin_user, name='create_admin'),
]
