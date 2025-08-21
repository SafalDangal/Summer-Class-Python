from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from store.models import Product
from .models import Cart, CartItem, Order, OrderItem
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required
def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = 1
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=quantity, cart=cart)
        cart_item.save()
    return redirect('cart')

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

def cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    except Cart.DoesNotExist:
        cart_items = []
    
    # Calculate totals
    grand_total = 0
    for cart_item in cart_items:
        grand_total += cart_item.sub_total()
    
    # Calculate tax (10% for example)
    tax = grand_total * 0.10
    total = grand_total + tax
    
    context = {
        'cart_items': cart_items,
        'grand_total': grand_total,
        'tax': tax,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


@login_required
def checkout(request):
    """Create an Order from the current cart, then show an invoice page."""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    except Cart.DoesNotExist:
        cart_items = []

    if not cart_items:
        return redirect('cart')

    # Compute totals (same logic as cart view)
    subtotal = sum(item.sub_total() for item in cart_items)
    tax = int(subtotal * 0.10)
    total = subtotal + tax

    # Create order number
    order_number = get_random_string(10).upper()
    order = Order.objects.create(
        order_number=order_number,
        subtotal=subtotal,
        tax=tax,
        total=total,
        user=request.user,
    )

    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    # Clear cart
    CartItem.objects.filter(cart=cart).delete()

    # Render invoice page
    context = {
        'order': order,
    }
    return render(request, 'cart/invoice.html', context)


def order_success(request):
    message = "Your order was placed successfully and will be delivered on time."
    return render(request, 'cart/success.html', { 'message': message })
