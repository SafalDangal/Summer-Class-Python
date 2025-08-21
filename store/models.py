from django.db import models
from django.urls import reverse
from django.conf import settings

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class Meta:
        unique_together = ('slug', 'parent')

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products', verbose_name='Product Image')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    # Owner & Approval
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='store_products'
    )
    is_approved = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name


class Variation(models.Model):
    VARIATION_CATEGORY_CHOICES = (
        ('color', 'Color'),
        ('size', 'Size'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_category = models.CharField(max_length=50, choices=VARIATION_CATEGORY_CHOICES)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'variation_category', 'variation_value')
        ordering = ['variation_category', 'variation_value']

    def __str__(self):
        return f"{self.product.product_name} - {self.variation_category}: {self.variation_value}"
