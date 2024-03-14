# Django
from django.core.management.base import BaseCommand

# Models
from apps.inventario.models import Inventory, Product


class Command(BaseCommand):
    help = "Create inventory for products"

    def handle(self, *args, **options):
        for product in Product.objects.all():
            inventory, created = Inventory.objects.get_or_create(product=product)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Se creó un objeto de Inventory para {product.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Ya existe un objeto de Inventory para {product.name}"
                    )
                )
