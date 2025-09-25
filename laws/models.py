from django.db import models
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
        return []