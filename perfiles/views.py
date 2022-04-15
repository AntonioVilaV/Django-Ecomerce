
from django.contrib.auth.models import Group
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic import TemplateView,UpdateView,CreateView
from django.contrib.auth.views import LoginView

from perfiles.models import datosContacto
from django.contrib.auth.models import User
from perfiles.forms import RegistroUsuarioForm, UpdateDatosContactoForm, UpdateDatosUsuarioForm

from django.contrib.auth.mixins import LoginRequiredMixin

from venta.models import RegistroVenta

from django.db.models import Q
from django.contrib.auth import authenticate, login
from inventario.models import Producto

from django.db import transaction



# Create your views here.


class HomeIndexTemplateView(TemplateView):
    """ Vista root de la plataforma, muestra las diferentes categorias y promociones """
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['man'] = Producto.objects.filter(estado=True).filter(categoria__nombre="Hombres")[:8]
        context['kids'] = Producto.objects.filter(estado=True).filter(categoria__nombre="Niños")[:8]
        context['women'] = Producto.objects.filter(estado=True).filter(categoria__nombre="Mujeres")[:8]
        
        context['title'] = "Eshop Django"
        return context


#Vendedor - Vistas

class HomePerfilTemplateView(LoginRequiredMixin,TemplateView):
    """ Vista home del perfil de usuario , encargada de mostrar el status de las operaciones de venta y compra del Vendedor"""
    template_name = 'perfiles/homeUsuario.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eshop Django - Home"

        if self.request.user.groups.get().name=='Vendedor':
            ventasActivas = RegistroVenta.objects.filter(producto__autor=self.request.user).filter(state=True).count()
            pagoPorConfirmar = RegistroVenta.objects.filter(producto__autor__pk=self.request.user.pk).filter(Q(estado_operacion__nombre='Esperando pago') | 
                                                                                                             Q(estado_operacion__nombre='Confirmando pago')).count()
            productosPorEnviar = RegistroVenta.objects.filter(producto__autor__pk=self.request.user.pk).filter(estado_operacion__nombre='Procesando Encomienda').count()
            context['resumen'] = [ventasActivas,pagoPorConfirmar,productosPorEnviar]
        elif self.request.user.groups.get().name=='Comprador':                                                                 
            compras = RegistroVenta.objects.filter(usuario=self.request.user.pk).filter(state=True).count()
            facturas = RegistroVenta.objects.filter(usuario=self.request.user.pk).filter(estado_operacion__nombre="Esperando pago").count()#Facturas P.Pagar
            envios = RegistroVenta.objects.filter(usuario=self.request.user.pk).filter(Q(estado_operacion__nombre='Procesando Encomienda') | 
                                                                                       Q(estado_operacion__nombre='Enviado')).count()
            context['resumen']=[compras,facturas,envios]
        return context

#Comprador - Vistas

class MiCuentaUpdateView(LoginRequiredMixin,UpdateView):
    """ Vista encargada de mostrar los datos de mi cuenta y da la opcion de actualizar """
    model = datosContacto
    second_model = User
    template_name='perfiles/miCuenta.html'
    form_class = UpdateDatosContactoForm
    second_form_class = UpdateDatosUsuarioForm
    success_url=reverse_lazy('HomePerfilTemplateView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eshop Django - Mi cuenta"
        usuario =  self.second_model.objects.get(id=self.kwargs['pk'])
        
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class(instance=usuario)
        return context

    def get_object(self, queryset=None):
        logeado = self.request.user
        datos = datosContacto.objects.get(usuario__id=self.kwargs['pk'])
        if datos.usuario == logeado:
            return datos
        else:
            raise Http404("Acceso denegado")
        
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().dispatch(request, *args, **kwargs)
        except datosContacto.DoesNotExist:
            raise Http404("Datos no existe")

    def post(self, request, *args, **kwargs):
        if self.object.usuario == self.request.user:
            formDatosUsuario = UpdateDatosUsuarioForm(request.POST,instance=self.request.user)
            formDatosContacto = UpdateDatosContactoForm(request.POST,instance=self.object)

            if formDatosUsuario.is_valid() and formDatosContacto.is_valid():
                formDatosUsuario.save(commit=False)
                formDatosContacto.save()
                formDatosUsuario.save()
                return self.render_to_response(self.get_context_data())
            else:
                return self.render_to_response(self.get_context_data(form=formDatosContacto,form2=formDatosUsuario))
        else:
            raise Http404("Acción dendegada")

class RegistroUsuarioCreateView(CreateView):
    """ Vista encargada de registrar un usuario en la base de datos de la plataforma"""
    model = User
    template_name = "perfiles/registrar.html"
    form_class = RegistroUsuarioForm
    success_url = reverse_lazy('HomePerfilTemplateView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registrar"
        return context
    
    
    def dispatch(self,request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('HomePerfilTemplateView'))
        else:
            return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
        response = super().form_valid(form)
        grupoID = self.request.POST['groups']
        grupo = Group.objects.get(id=grupoID)
        with transaction.atomic():
            grupo.user_set.add(self.object)
            datosContacto.objects.create(usuario=self.object)
        new_user = authenticate(username=form.cleaned_data.get('username'),password=form.cleaned_data.get('password1'))
        login(self.request,new_user)

        return response


#Session Vistas

class LoginUserLoginView(LoginView):
    """ Vista encargada de mostrar formulario de logueo"""
    template_name= "log/log.html"

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = "Login"
            return context
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('HomePerfilTemplateView')
        return super().dispatch(request, *args, **kwargs)

class DatosDeContactoTemplateView(TemplateView):
    """ Vista esta encargada de mostrar los datos de contacto de un usuario y verificar si tienes permisos para verlos """
    template_name = "perfiles/contacto/datosContacto.html"

    def dispatch(self, request, *args, **kwargs):
        
        if RegistroVenta.objects.filter(usuario=self.request.user).filter(producto__autor__id=self.kwargs['pk']).exists() or RegistroVenta.objects.filter(usuario__id=self.kwargs['pk']).filter(producto__autor=self.request.user).exists():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Objeto no encontrado")
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Eshop Django - Datos Contacto"

        context['contacto'] = datosContacto.objects.get(id=self.kwargs['pk'])
        return context 