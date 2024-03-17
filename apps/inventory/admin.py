from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.inventory.models import Category, Discount, Inventory, Product

# Register your models here.


class ProductResources(resources.ModelResource):
    class Meta:
        model = Product


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = ProductResources


admin.site.register(Product, ProductAdmin)
admin.site.register(Inventory)
admin.site.register(Category)
admin.site.register(Discount)
