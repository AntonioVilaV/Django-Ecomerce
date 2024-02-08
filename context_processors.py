from apps.inventario.models import Categoria

def categorias_base(request):
    categorias = Categoria.objects.all()
    return {'categorias':categorias}