from django.shortcuts import render, get_object_or_404
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
    return render(request, 'search_results.html', context)