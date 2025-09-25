from django.contrib import admin
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
    date_hierarchy = 'created_at' 