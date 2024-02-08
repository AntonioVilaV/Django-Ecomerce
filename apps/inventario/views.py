from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import ListView,TemplateView,CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy

from apps.inventario.models import Inventario, Producto
from mixins import validarGrupo
from apps.inventario.forms import crearProductoForm, inventarioForm, updateProductoForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.db import transaction
# Create your views here.



#Vendedor - Vistas Productos
class ListaPublicacionesVendedorActivasListView(LoginRequiredMixin,validarGrupo,ListView):
    """ Vista encargada de mostrar la lista de Publicaciones o productos publicados que estan activos. Vista para usuario tipo Vendedor """
    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    model = Producto
    template_name = "perfiles/vendedor/publicaciones/publicaciones.html"
    paginate_by=10
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eshop Django - Publicaciones Activas"
        return context
    

    def get_queryset(self):
        return Producto.objects.filter(estado=True).filter(autor=self.request.user)

class ListaPublicacionesVendedorPausadasListView(LoginRequiredMixin,validarGrupo,ListView):
    """ Vista encargada de mostrar la lista de Publicaciones o productos publicados que estan pausadas. Vista para usuario tipo Vendedor """
    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    model = Producto
    template_name = "perfiles/vendedor/publicaciones/publicaciones.html"
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eshop Django - Publicaciones Pausadas"
        return context

    def get_queryset(self):
        return Producto.objects.filter(autor=self.request.user).filter(estado=False)

class CrearPublicacionCreateView(LoginRequiredMixin,validarGrupo,CreateView):
    """ Vista encargada de crear producto o publicacion para vender en la plataforma"""
    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView") 
    template_name="perfiles/vendedor/publicaciones/crearPublicacion.html"
    model = Producto
    form_class=crearProductoForm
    second_form_class = inventarioForm
    success_url=reverse_lazy('HomePerfilTemplateView')

    def get_context_data(self, **kwargs):
        context = super(CrearPublicacionCreateView,self).get_context_data(**kwargs)
        context['title'] = "Eshop Django - Crear publicacion"

        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        return context

    def post(self,request,*args,**kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)

        if form.is_valid() and form2.is_valid():
            inventario = form2.save(commit=False)
            form.instance.autor=self.request.user
            form.instance.estado = True
            if 'foto' in self.request.FILES:
                form.instance.foto=self.request.FILES['foto']
            inventario.producto = form.save()
            inventario.save()
            
            return redirect(reverse_lazy('ListaPublicacionesVendedorActivasListView'))
        else:
            return self.render_to_response(self.get_context_data(form=form,form2=form2))

class UpdatePublicacionUpdateView(LoginRequiredMixin,validarGrupo,UpdateView):
    """ Vista encargada de actualizar o editar los datos de un Producto"""
    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    template_name="perfiles/vendedor/publicaciones/updatePublicacion.html"
    model = Producto
    second_model = Inventario
    form_class=updateProductoForm
    second_form_class = inventarioForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Producto no encontrado")

    def get_context_data(self, **kwargs):
        context = super(UpdatePublicacionUpdateView,self).get_context_data(**kwargs)
        context['title'] = "Eshop Django - Editar publicaciones"

        producto = self.model.objects.get(id=self.kwargs['pk'])
        inventario = self.second_model.objects.get(producto=producto)

        if 'form' not in context:
            context['form'] = self.form_class(instance=producto)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=inventario)
        return context

    def post(self,request,*args,**kwargs):
        
        if self.model.objects.filter(id=self.kwargs['pk']).filter(autor=self.request.user):
            producto = self.model.objects.get(id=self.kwargs['pk'])

            cantidad = self.second_model.objects.get(producto=producto)
            form = self.form_class(request.POST,instance=producto)
            form2 = self.second_form_class(request.POST,instance=cantidad)
            if form.is_valid() and form2.is_valid():
                print(form)
                if 'foto' in self.request.FILES:
                    form.instance.foto = self.request.FILES['foto']
                form.save()
                form2.save()
                
                if form.instance.estado:
                    self.success_url=reverse_lazy('ListaPublicacionesVendedorActivasListView')
                else:
                    self.success_url=reverse_lazy('ListaPublicacionesVendedorPausadasListView')

                return redirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form,form2=form2))
        else:
            raise Http404("Acción denegada")

class EliminarPublicacionDeleteView(LoginRequiredMixin,validarGrupo,DeleteView):
    """ Vista encargada de eliminar producto o publicacion """
    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    model = Producto
    template_name = "perfiles/vendedor/publicaciones/eliminarPublicacion.html"
    success_url= reverse_lazy('ListaPublicacionesVendedorActivasListView')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eshop Django - Eliminar publicación"
        return context
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor==self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Producto no encontrado")
        
    def post(self,request,*args,**kwargs):
        if self.object.autor==self.request.user:
            self.object.delete()
            return redirect(reverse_lazy('ListaPublicacionesVendedorActivasListView'))
        else:
            raise Http404("Acción denegada")

class ActionPublicacionTemplateView(LoginRequiredMixin,validarGrupo,TemplateView):
    """ Vista encargada de manejar y ejecutar las acciones sobre las publicaciones; Activar o pausar publicacion """
    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    template_name="perfiles/vendedor/publicaciones/actionPublicacion.html"
    
    def dispatch(self, request, *args, **kwargs):
        try:
            producto = Producto.objects.filter(autor=self.request.user).get(id=self.kwargs['pk'])
            if self.kwargs['action'] == 'pausar' and producto.estado:
                return super().dispatch(request, *args, **kwargs)
            elif self.kwargs['action'] == 'activar' and producto.estado == False:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("Accion incorrecta")
        except Producto.DoesNotExist:
            raise Http404("Producto no existe")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action = self.kwargs['action']
        title = "Eshop Django -"
        if action[0] is 'a':
            title += "Activar publicación"
        elif action[0] is 'p':
            title += "Pausar publicación"    
        context['title'] = title
        context['action'] = action
        context['producto'] = Producto.objects.get(id=self.kwargs['pk'])
        return context
    
    def post(self,request,*args,**kwargs):
        producto = Producto.objects.filter(id=self.kwargs['pk'])
        if self.request.user == producto.get().autor:
            if self.kwargs['action'] == 'activar':
                if 'cantidad' in request.POST:
                    cantidad = request.POST['cantidad']
                    if cantidad.isdigit() and int(cantidad) > 0:
                        with transaction.atomic():
                            Inventario.objects.filter(producto=producto.get()).update(cantidad=cantidad)
                            producto.update(estado=True)
                            return redirect(reverse_lazy('ListaPublicacionesVendedorActivasListView'))
                    else:
                        return self.render_to_response(self.get_context_data(error="La cantidad debe ser un numero mayor a 0 para poder activar la publicación"))
            elif self.kwargs['action'] == 'pausar':
                producto.update(estado=False)
                return redirect(reverse_lazy('ListaPublicacionesVendedorPausadasListView'))
        

#Comprador - Vistas Productos
class ProductoDetailView(DetailView):
    """ Vista encargada de mostrar los detalles del producto al comprador y dar opciones y detalles de compra """
    model = Producto
    template_name = "perfiles/comprador/publicaciones/productoDetail.html"

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        producto = Producto.objects.get(id=self.kwargs['pk'])
        context['title'] = producto.nombre
        context['producto']= producto
        return context

class BuscarProductoListView(ListView):
    """ Vista encargada de mostrar la lista de productos resultado de la busqueda en el input superior del template. (Grilla de productos filtrados por el buscador) """
    model = Producto
    template_name = "perfiles/comprador/publicaciones/shop-grid.html"
    paginate_by = 9
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eshop Django - " + self.request.GET['search']
        context['productosRecientes'] = Producto.objects.filter(estado=True).order_by("-fecha_creada")[:4]
        return context

    def get_queryset(self):
        busqueda = self.request.GET['search']

        try:
            categoria = self.request.GET.getlist('categorias')[0]
        except IndexError:
            categoria = "Categorias"
        
        if  categoria == 'Categorias':
            return Producto.objects.filter(nombre__icontains=busqueda).filter(estado=True)
        elif categoria == "decV":
            return Producto.objects.filter(estado=True).filter(descuento__descuento__gte=0)
        else:
            return Producto.objects.filter(categoria__nombre=categoria).filter(estado=True).filter(nombre__icontains=busqueda)

            
        
        
        
