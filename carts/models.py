from django.db import models
from django.conf import settings
from store.models import Product

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity


class Order(models.Model):
    """A simple order record created at checkout."""
    order_number = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Link to the user who placed the order (optional for guest checkouts)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    # Capture totals at time of purchase
    subtotal = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    # Optional lightweight customer fields (not strictly used now)
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.IntegerField()  # snapshot of product price at purchase time

    def line_total(self):
        return self.price * self.quantity
