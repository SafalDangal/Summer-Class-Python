from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from store.models import Category, Product
from django.utils.text import slugify
import requests
import os

class Command(BaseCommand):
    help = 'Populate database with sample products and images'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Tshirt', 'slug': 'tshirt'},
            {'name': 'Electronics', 'slug': 'electronics'},
            {'name': 'Home & Living', 'slug': 'home-living'},
            {'name': 'Books', 'slug': 'books'},
            {'name': 'Accessories', 'slug': 'accessories'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'category_name': cat_data['name']}
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f"Created category: {cat_data['name']}")

        # Sample products data with image URLs
        products_data = [
            {
                'name': 'Basic White T-Shirt',
                'price': 2000,
                'stock': 50,
                'category': 'tshirt',
                'image_url': 'https://mohit-bucket.s3.us-east-1.amazonaws.com/media/photos/products/White_Tshirt.webp'
            },
            {
                'name': 'Wireless Noise Cancelling Headphones',
                'price': 15999,
                'stock': 25,
                'category': 'electronics',
                'image_url': 'https://mohit-bucket.s3.us-east-1.amazonaws.com/media/photos/products/Wireless_Noise_Cancelling_Headphones.webp'
            },
            {
                'name': 'Wooden Study Lamp',
                'price': 3450,
                'stock': 30,
                'category': 'home-living',
                'image_url': 'https://mohit-bucket.s3.us-east-1.amazonaws.com/media/photos/products/Wooden_Study_Lamp.webp'
            },
            {
                'name': 'The Psychology of Money',
                'price': 1499,
                'stock': 100,
                'category': 'books',
                'image_url': 'https://mohit-bucket.s3.us-east-1.amazonaws.com/media/photos/products/The_Psychology_of_Money.webp'
            },
            {
                'name': 'Vintage Leather Wallet',
                'price': 2899,
                'stock': 40,
                'category': 'accessories',
                'image_url': 'https://mohit-bucket.s3.us-east-1.amazonaws.com/media/photos/products/Vintage_Leather_Wallet.webp'
            },
            {
                'name': 'Smart Fitness Band',
                'price': 3299,
                'stock': 35,
                'category': 'electronics',
                'image_url': 'https://mohit-bucket.s3.us-east-1.amazonaws.com/media/photos/products/Smart_Fitness_Band.png'
            },
            {
                'name': '4K Android Smart TV – 43 Inch',
                'price': 45000,
                'stock': 10,
                'category': 'electronics',
                'image_url': 'https://mohit-bucket.s3.us-east-1.amazonaws.com/media/photos/products/4K_Android_Smart_TV__43_Inch.jpg'
            },
            {
                'name': 'Decorative Wall Clock',
                'price': 2250,
                'stock': 20,
                'category': 'home-living',
                'image_url': 'https://mohit-bucket.s3.us-east-1.amazonaws.com/media/photos/products/Decorative_Wall_Clock.jpg'
            },
        ]

        for product_data in products_data:
            # Check if product already exists
            if Product.objects.filter(slug=slugify(product_data['name'])).exists():
                self.stdout.write(f"Product {product_data['name']} already exists, skipping...")
                continue

            try:
                # Download image
                response = requests.get(product_data['image_url'], timeout=10)
                if response.status_code == 200:
                    # Create product
                    product = Product.objects.create(
                        product_name=product_data['name'],
                        slug=slugify(product_data['name']),
                        price=product_data['price'],
                        stock=product_data['stock'],
                        is_available=True,
                        category=categories[product_data['category']]
                    )

                    # Save image
                    image_name = f"{slugify(product_data['name'])}.{product_data['image_url'].split('.')[-1]}"
                    product.images.save(
                        image_name,
                        ContentFile(response.content),
                        save=True
                    )

                    self.stdout.write(
                        self.style.SUCCESS(f'Successfully created product: {product_data["name"]}')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'Failed to download image for: {product_data["name"]}')
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating product {product_data["name"]}: {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS('Database population completed!'))
