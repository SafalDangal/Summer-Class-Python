from django.shortcuts import render
from django.http import HttpResponse
from products.models import Product as ProductsAppProduct, Category
from blogs.models import Blog
from store.models import Product as StoreProduct

def home(request):
	# This will use the base.html template with popular products
	return render(request, 'base.html')

# New: store-backed homepage (additive)
def home_store(request):
	products = StoreProduct.objects.all().order_by('-created_date')
	context = {
		'products': products
	}
	return render(request, 'home/home.html', context)
