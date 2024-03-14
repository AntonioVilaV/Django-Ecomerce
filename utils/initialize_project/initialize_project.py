import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command

from apps.perfiles.models import datosContacto


def initialize_project():
    user = User.objects.create_superuser("admin", "admin@admin.com", "admin")
    datosContacto.objects.create(user=user)

    call_command("populate_categories")

    fixture_file = os.path.join(
        settings.BASE_DIR, "apps", "inventory", "fixtures", "products.json"
    )
    call_command("loaddata", fixture_file, verbosity=0)

    call_command("populate_inventory")

    call_command("populate_status_operation")


if __name__ == "__main__":
    initialize_project()
