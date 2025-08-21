from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Category, Product

# Minimal 1x1 GIF (valid image bytes)
MINI_GIF = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\n\x00\x01\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)

CATEGORIES = [
    {"name": "Tshirt", "slug": "tshirt"},
    {"name": "Electronics", "slug": "electronics"},
    {"name": "Home & Living", "slug": "home-living"},
    {"name": "Books", "slug": "books"},
    {"name": "Accessories", "slug": "accessories"},
]

PRODUCTS = [
    {"name": "Wireless Noise Cancelling Headphones", "slug": "wireless-noise-cancelling-headphones", "price": 15999, "category": "electronics", "stock": 10},
    {"name": "Wooden Study Lamp", "slug": "wooden-study-lamp", "price": 3450, "category": "home-living", "stock": 8},
    {"name": "The Psychology of Money", "slug": "the-psychology-of-money", "price": 1499, "category": "books", "stock": 20},
    {"name": "Vintage Leather Wallet", "slug": "vintage-leather-wallet", "price": 2899, "category": "accessories", "stock": 15},
    {"name": "Smart Fitness Band", "slug": "smart-fitness-band", "price": 3299, "category": "electronics", "stock": 12},
    {"name": "Basic White T-Shirt", "slug": "basic-white-t-shirt", "price": 2000, "category": "tshirt", "stock": 25},
    {"name": "4K Android Smart TV – 43 Inch", "slug": "4k-android-smart-tv-43-inch", "price": 45000, "category": "electronics", "stock": 5},
    {"name": "Decorative Wall Clock", "slug": "decorative-wall-clock", "price": 2250, "category": "home-living", "stock": 9},
]

class Command(BaseCommand):
    help = "Seed categories and products with expected slugs so detail pages resolve"

    def handle(self, *args, **options):
        # Create categories
        slug_to_category = {}
        for c in CATEGORIES:
            cat, _ = Category.objects.get_or_create(slug=c["slug"], defaults={"category_name": c["name"]})
            slug_to_category[c["slug"]] = cat
        self.stdout.write(self.style.SUCCESS(f"Ensured {len(slug_to_category)} categories"))

        # Create products
        created_count = 0
        for p in PRODUCTS:
            cat = slug_to_category[p["category"]]
            product, created = Product.objects.get_or_create(
                slug=p["slug"],
                defaults={
                    "product_name": p["name"],
                    "price": p["price"],
                    "stock": p["stock"],
                    "is_available": True,
                    "category": cat,
                },
            )
            if created or not product.images:
                # attach tiny gif if missing
                product.images.save(f"{product.slug}.gif", ContentFile(MINI_GIF), save=False)
                product.save()
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Seed complete. New/updated products: {created_count}"))

