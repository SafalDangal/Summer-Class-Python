from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product, Category
from blogs.models import Blog
def home(request):
    products = Product.objects.all()[:8]  # Get first 8 real products from database
    blogs = Blog.objects.all()[:3]
    return render(request, 'extending/home1.html', {
        'products': products,
        'blogs': blogs
    })
