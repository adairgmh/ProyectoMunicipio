from django.shortcuts import redirect, render, get_object_or_404
from appUsuario.forms import UserForm
from django.urls import reverse_lazy
from appUsuario.forms import CustomCreationForm
from django.http import JsonResponse
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView

from appUsuario.models import Usuario
from appPredial.models import *

# Create your views here.

def listadoUsuarios(request):
    usuario = Usuario.objects.all()
    contexto = {'usuarios': usuario}
    return render(request, 'registro/listarusuarios.html', contexto)


def editarUsuarios(request, id):

    usuario = get_object_or_404(Usuario, id=id)

    data = {
        'form': CustomCreationForm(instance=usuario)
    }

    if request.method == 'POST':
        formulario = CustomCreationForm(data=request.POST, instance=usuario)
        if formulario.is_valid():
            formulario.save()
            return  redirect(to='usuarios:verusuarios')
        data["form"] = formulario

    return render(request, 'registro/modificarusuarios.html', data)


def eliminarUsuarios(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    return redirect(to="usuarios:verusuarios")


def registroview(request):
    data ={
        'form':CustomCreationForm()
    }
    if request.method =='POST':
        formulario = CustomCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"El usuario ha sido registrado con éxito")
            return redirect('usuarios:registro')
        data["form"]= formulario
    return render(request, 'registro/registro.html',data)




def registroCorrecto(request):
    return render(request, 'registro/registro.html')

class usuarioListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'usuario.view_usuario'
    model = Usuario
    template_name = 'usuario_list.html'

    """ @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs) """
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Usuarios'
        context['create_url'] = reverse_lazy('predial:usuario_add')
        
        
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            data = Usuario.objects.get(pk = request.POST['id']).toJSON()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
    
    
class usuarioCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'usuario.add_usuario'
    form_class = UserForm
    model = Usuario
    template_name = 'usuario_add.html'
    success_url = reverse_lazy('usuario:usuario_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar un Nuevo Usuario'
        context['entity'] = 'Usuarios'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('usuario:usuario_list')

        return context


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data)

class usuarioUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'predial.change_usuario'
    form_class = UserForm
    model = Usuario
    template_name = 'usuario_edit.html'
    success_url = reverse_lazy('usuario:usuario_list')
    
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data) 
   
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Usuario'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('usuario:usuario_list')
        
        return context
    
class usuarioDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    
    permission_required = 'usuario.delete_usuario'
    template_name = 'usuario_delete.html'
    model = Usuario
    success_url = reverse_lazy('usuario:usuario_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de Usuario'
        context['list_url'] = reverse_lazy('usuario:usuario_list')
        return context
    

class usuarioCreateViewCont(CreateView):
    form_class = UserForm
    model = Usuario
    template_name = 'usuario_add_cont.html'
    success_url = reverse_lazy('usuario:usuario_info')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Agregar un Nuevo Usuario'
        context['entity'] = 'Usuarios'
        context['action'] = 'add'
        context['list_url'] = reverse_lazy('usuario:usuario_info')

        return context


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion' 
        except Exception as e:
                data['error'] = str(e)
        return JsonResponse(data)

class usuarioInfo(LoginRequiredMixin,generic.TemplateView):
    template_name = 'usuario_info.html'
    login_url = 'generales:loginC'

    
    def get(self, request, **kwargs):
        contribuyente = Contribuyente.objects.filter(usuario=self.request.user)
        print (contribuyente)
        x = contribuyente[0]
        print (x)
        objectlist = Predio.objects.filter(rfc=x)
        print (objectlist)
        context={
        "object_list":objectlist,

        }


        return render(request, self.template_name, context=context)
