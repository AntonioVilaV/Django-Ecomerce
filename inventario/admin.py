from django.contrib import admin

from inventario.models import Categoria, Descuento, Inventario, Producto

# Register your models here.
admin.site.register(Producto)
admin.site.register(Inventario)
admin.site.register(Categoria)
admin.site.register(Descuento)