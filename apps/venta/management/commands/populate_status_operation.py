# Django
from django.core.management.base import BaseCommand

# Models
from apps.venta.models import EstadoOperacion
from utils.sale.status_operation import STATUS_OPERATION


class Command(BaseCommand):
    help = "Create categories for products"

    def handle(self, *args, **options):
        new_status = []
        for pk, nombre in STATUS_OPERATION.items():
            new_status.append({"nombre": nombre, "pk": pk})
        created_status = EstadoOperacion.objects.bulk_create(
            [EstadoOperacion(**status) for status in new_status]
        )
        for status in created_status:
            self.stdout.write(
                self.style.SUCCESS('Category "%s" created' % status.nombre)
            )
