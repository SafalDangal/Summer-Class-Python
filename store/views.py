from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product, Category, Variation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm, VariationForm, RegistrationForm
import os
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

def store(request, category_slug=None, subcategory_slug=None):
    """
    Main store view that displays products with filtering and pagination
    """
    categories = Category.objects.all()
    # Ensure ordering for deterministic pagination
    products = Product.objects.filter(is_available=True, is_approved=True).order_by('-created_date')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        if subcategory_slug:
            subcategory = get_object_or_404(Category, slug=subcategory_slug, parent=category)
            products = products.filter(category=subcategory)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) |
            Q(category__category_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {
        'products': paged_products,
        'categories': categories,
        'products_count': products.count(),
    }
    
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    """
    Detailed view for a single product
    """
    product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug,
        is_available=True,
        is_approved=True,
    )
    
    context = {
        'product': product,
    }
    
    return render(request, 'store/product_detail.html', context)


def product_detail_by_id(request, pk):
    """Compatibility redirect: resolve a product by PK and redirect to the slug-based product_detail URL."""
    product = get_object_or_404(Product, pk=pk, is_available=True, is_approved=True)
    return redirect('product_detail', category_slug=product.category.slug, product_slug=product.slug)

def search(request):
    """
    Search functionality for products
    """
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_available=True, is_approved=True)
    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(category__category_name__icontains=query)
        )

    # Pagination for search results as well
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'products_count': products.count(),
        'search_query': query,
    }
    
    return render(request, 'store/store.html', context)

def categories_list(request):
    """
    List all available categories
    """
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'store/categories.html', context)

def tshirt_category(request):
    """Static T-shirt category view"""
    products = Product.objects.filter(
        category__slug='tshirt',
        is_available=True
    )
    context = {
        'products': products,
        'category_name': 'T-Shirts',
    }
    return render(request, 'store/store.html', context)

def electronics_category(request):
    """Static electronics category view"""
    products = Product.objects.filter(
        category__slug='electronics',
        is_available=True
    )
    context = {
        'products': products,
        'category_name': 'Electronics',
    }
    return render(request, 'store/store.html', context)

def home_living_category(request):
    """Static home living category view"""
    products = Product.objects.filter(
        category__slug='home-living',
        is_available=True
    )
    context = {
        'products': products,
        'category_name': 'Home & Living',
    }
    return render(request, 'store/store.html', context)

def books_category(request):
    """Static books category view"""
    products = Product.objects.filter(
        category__slug='books',
        is_available=True
    )
    context = {
        'products': products,
        'category_name': 'Books',
    }
    return render(request, 'store/store.html', context)

def accessories_category(request):
    """Static accessories category view"""
    products = Product.objects.filter(
        category__slug='accessories',
        is_available=True
    )
    context = {
        'products': products,
        'category_name': 'Accessories',
    }
    return render(request, 'store/store.html', context)


def ai_product_answer(request):
    """LLM-backed Q&A for a specific product.
    Requires env var OPENAI_API_KEY to be set. Returns JSON with 'answer'.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    question = (request.POST.get('question') or '').strip()
    product_id = (request.POST.get('product_id') or '').strip()
    if not question:
        return JsonResponse({'error': 'question is required'}, status=400)

    product = None
    if product_id:
        product = get_object_or_404(Product, id=product_id, is_available=True)

    # If OpenAI is not installed or API key is missing, return a friendly note
    api_key = os.getenv('OPENAI_API_KEY')
    if OpenAI is None or not api_key:
        fallback = (
            "AI is not configured. Set OPENAI_API_KEY and install the 'openai' package "
            "to enable AI answers."
        )
        return JsonResponse({'answer': fallback})

    client = OpenAI(api_key=api_key)
    system = (
        "You are a helpful shopping assistant. Be concise, accurate, and friendly."
    )
    if product:
        user = (
            f"Customer question: {question}\n\n"
            f"Product details:\n"
            f"- Name: {product.product_name}\n"
            f"- Category: {product.category.category_name}\n"
            f"- Price: Rs. {product.price}\n"
            f"- In Stock: {product.stock}\n"
            "If the question is unrelated, gently say so."
        )
    else:
        user = (
            f"Customer question: {question}\n"
            "No specific product provided. Answer generally for a shopping site in concise language."
        )

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.3,
        )
        answer = resp.choices[0].message.content
        return JsonResponse({'answer': answer})
    except Exception:
        return JsonResponse({'answer': 'Sorry, the AI service is unavailable right now.'}, status=502)


# ---------- Auth (Registration) ----------
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'extending/register.html', {'form': form})


# ---------- Dashboard & My Products ----------
@login_required
def my_dashboard(request):
    my_products = Product.objects.filter(owner=request.user).order_by('-created_date')
    return render(request, 'extending/dashboard.html', {'my_products': my_products})


# ---------- Product CRUD ----------
@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            # New submissions require admin approval
            product.is_approved = False
            product.save()
            messages.success(request, 'Product submitted for approval.')
            return redirect('my_products')
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def my_products(request):
    products = Product.objects.filter(owner=request.user).order_by('-created_date')
    return render(request, 'store/my_products.html', {'products': products})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            p = form.save(commit=False)
            # editing resets approval
            p.is_approved = False
            p.save()
            messages.success(request, 'Product updated and sent for re-approval.')
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {'form': form, 'title': 'Edit Product'})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted')
        return redirect('my_products')
    return render(request, 'store/product_confirm_delete.html', {'product': product})


# ---------- Variation Management ----------
@login_required
def variation_list(request, product_id):
    product = get_object_or_404(Product, pk=product_id, owner=request.user)
    variations = product.variations.all()
    return render(request, 'store/variation_list.html', {'product': product, 'variations': variations})


@login_required
def variation_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id, owner=request.user)
    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            v = form.save(commit=False)
            v.product = product
            v.save()
            messages.success(request, 'Variation added.')
            return redirect('variation_list', product_id=product.id)
    else:
        form = VariationForm()
    return render(request, 'store/variation_form.html', {'form': form, 'product': product})


@login_required
def variation_delete(request, product_id, variation_id):
    product = get_object_or_404(Product, pk=product_id, owner=request.user)
    variation = get_object_or_404(Variation, pk=variation_id, product=product)
    if request.method == 'POST':
        variation.delete()
        messages.success(request, 'Variation deleted.')
        return redirect('variation_list', product_id=product.id)
    return render(request, 'store/variation_confirm_delete.html', {'product': product, 'variation': variation})
