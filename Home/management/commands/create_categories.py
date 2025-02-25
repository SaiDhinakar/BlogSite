from django.core.management.base import BaseCommand
from Home.models import Category

class Command(BaseCommand):
    help = 'Creates initial categories'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Technology', 'description': 'Posts about technology and innovations'},
            {'name': 'Lifestyle', 'description': 'Posts about daily life and experiences'},
            {'name': 'Travel', 'description': 'Travel experiences and guides'},
            {'name': 'Food', 'description': 'Recipes and food experiences'},
        ]

        for category_data in categories:
            Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )

        self.stdout.write(self.style.SUCCESS('Successfully created categories'))