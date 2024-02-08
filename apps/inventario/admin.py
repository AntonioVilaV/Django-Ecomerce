from django.contrib import admin

from apps.inventario.models import Categoria, Descuento, Inventario, Producto

from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class ProductoResources(resources.ModelResource):
    class Meta:
        model = Producto

class ProductoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = ProductoResources

admin.site.register(Producto,ProductoAdmin)
admin.site.register(Inventario)
admin.site.register(Categoria)
admin.site.register(Descuento)