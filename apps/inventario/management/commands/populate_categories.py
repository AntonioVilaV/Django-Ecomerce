# Django
from django.core.management.base import BaseCommand

# Models
from apps.inventario.models import Categoria
from utils.category.categories import CATEGORIES


class Command(BaseCommand):
    help = "Create categories for products"

    def handle(self, *args, **options):
        existing_categories = set(Categoria.objects.values_list("nombre", flat=True))
        new_categories = [
            category for category in CATEGORIES if category not in existing_categories
        ]
        created_categories = Categoria.objects.bulk_create(
            [Categoria(nombre=category) for category in new_categories]
        )
        for category in created_categories:
            self.stdout.write(
                self.style.SUCCESS('Category "%s" created' % category.nombre)
            )
