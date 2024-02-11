# Django
from django.core.management.base import BaseCommand

# Models
from apps.inventario.models import Categoria
from utils.category.categories import CATEGORIES


class Command(BaseCommand):
    help = "Create categories for products"

    def handle(self, *args, **options):
        if Categoria.objects.exists():
            Categoria.objects.all().delete()
        new_categories = []
        for pk, nombre in CATEGORIES.items():
            new_categories.append({"nombre": nombre, "pk": pk})
        created_categories = Categoria.objects.bulk_create(
            [Categoria(**category) for category in new_categories]
        )
        for category in created_categories:
            self.stdout.write(
                self.style.SUCCESS('Category "%s" created' % category.nombre)
            )
