# Django
from django.core.management.base import BaseCommand

# Models
from apps.sale.models import OperatingStatus
from utils.sale.status_operation import STATUS_OPERATION


class Command(BaseCommand):
    help = "Create categories for products"

    def handle(self, *args, **options):
        new_status = []
        for pk, name in STATUS_OPERATION.items():
            new_status.append({"name": name, "pk": pk})
        created_status = OperatingStatus.objects.bulk_create(
            [OperatingStatus(**status) for status in new_status]
        )
        for status in created_status:
            self.stdout.write(self.style.SUCCESS('Category "%s" created' % status.name))
