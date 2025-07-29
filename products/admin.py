from django.contrib import admin
from.models import Product, Category

class catagoeryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class ProductAdmin(admin.ModelAdmin):
    exclude = ('created_at',)
    list_display = ('id', 'name', 'price', 'status', 'category', 'stock')    

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, catagoeryAdmin)


   