# Django
from django.core.management.base import BaseCommand

# Models
from apps.inventory.models import Category
from utils.category.categories import CATEGORIES


class Command(BaseCommand):
    help = "Create categories for products"

    def handle(self, *args, **options):
        if Category.objects.exists():
            Category.objects.all().delete()
        new_categories = []
        for pk, name in CATEGORIES.items():
            new_categories.append({"name": name, "pk": pk})
        created_categories = Category.objects.bulk_create(
            [Category(**category) for category in new_categories]
        )
        for category in created_categories:
            self.stdout.write(
                self.style.SUCCESS('Category "%s" created' % category.name)
            )
