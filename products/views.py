from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def products(request):
    return render(request, 'extending/products1.html')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'extending/product_details1.html', {'product': product})
