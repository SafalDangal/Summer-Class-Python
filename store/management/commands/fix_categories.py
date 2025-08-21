from django.core.management.base import BaseCommand
from store.models import Category

class Command(BaseCommand):
    help = 'Ensure home-living and wooden-study-lamp category structure exists.'

    def handle(self, *args, **options):
        # Ensure parent category exists
        parent, created = Category.objects.get_or_create(
            slug='home-living',
            defaults={'category_name': 'Home Living'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created parent category: home-living'))
        else:
            self.stdout.write('Parent category already exists: home-living')

        # Ensure subcategory exists and is linked to parent
        subcat, sub_created = Category.objects.get_or_create(
            slug='wooden-study-lamp',
            parent=parent,
            defaults={'category_name': 'Wooden Study Lamp'}
        )
        if sub_created:
            self.stdout.write(self.style.SUCCESS('Created subcategory: wooden-study-lamp'))
        else:
            # Fix parent if needed
            if subcat.parent_id != parent.id:
                subcat.parent = parent
                subcat.save()
                self.stdout.write(self.style.SUCCESS('Fixed parent for subcategory: wooden-study-lamp'))
            else:
                self.stdout.write('Subcategory already exists and is linked: wooden-study-lamp')
