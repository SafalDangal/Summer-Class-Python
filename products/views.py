from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def products(request):
    products = Product.objects.all()
    return render(request, 'extending/products.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'extending/product_details.html', {'product': product})

def cart(request):
    return render(request, 'extending/cart.html')
