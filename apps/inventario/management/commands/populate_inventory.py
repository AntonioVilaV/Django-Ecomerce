# Django
from django.core.management.base import BaseCommand

# Models
from apps.inventario.models import Inventario, Producto


class Command(BaseCommand):
    help = "Create inventory for products"

    def handle(self, *args, **options):
        for producto in Producto.objects.all():
            inventario, created = Inventario.objects.get_or_create(producto=producto)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Se creó un objeto de Inventario para {producto.nombre}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Ya existe un objeto de Inventario para {producto.nombre}"
                    )
                )
