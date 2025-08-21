from django.contrib import admin
from .models import Product, Category, Variation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category_name",)}
    list_display = ("id", "category_name", "slug")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("product_name",)}
    list_display = ("id", "product_name", "price", "stock", "is_available", "is_approved", "owner", "category", "image_preview")
    readonly_fields = ("created_date", "image_preview")
    
    def image_preview(self, obj):
        return obj.image and f'<img src="{obj.image.url}" style="max-height: 100px;" />' or "No Image"
    image_preview.allow_tags = True
    image_preview.short_description = "Preview"
    list_filter = ("is_available", "is_approved", "category")
    search_fields = ("product_name", "slug")
    readonly_fields = ("created_date",)


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", "variation_category", "variation_value", "is_active")
    list_filter = ("variation_category", "is_active")
    search_fields = ("product__product_name", "variation_value")
