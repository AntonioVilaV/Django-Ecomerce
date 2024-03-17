# Django
import os

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.perfiles.models import ContactDetails


class Command(BaseCommand):
    help = "Initialize Project"

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                user = User.objects.create_superuser(
                    "admin", "admin@admin.com", "admin"
                )
                ContactDetails.objects.create(user=user)
                seller_group = Group.objects.create(name="Seller")
                Group.objects.create(name="Buyer")
                user.groups.add(seller_group)
                self.stdout.write(self.style.SUCCESS("Usuario creado exitosamente!"))

                call_command("populate_categories")

                fixture_file = os.path.abspath(
                    os.path.join(
                        settings.BASE_DIR,
                        "..",
                        "apps",
                        "inventory",
                        "fixtures",
                        "products.json",
                    )
                )
                call_command("loaddata", fixture_file, verbosity=0)

                call_command("populate_inventory")

                call_command("populate_status_operation")

                self.stdout.write(self.style.SUCCESS("Inicialización exitosa"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
