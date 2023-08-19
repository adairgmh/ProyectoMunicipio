from cmath import log
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.contrib.auth import authenticate, login, logout
# Create your views here.

from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

''' class Principal(generic.TemplateView):
    template_name = 'personal/login.html'
    #login_url = 'generales:loginP' '''

class Contribuyente(generic.TemplateView):
    template_name = 'contribuyente/contribuyente.html'

class Area_consulta(generic.TemplateView):
    template_name = 'contribuyente/area-consulta-contribuyente.html'

class ContribuyenteLoginView(LoginView):
    template_name = 'contribuyente/login.html'

    def get_success_url(self):
        
        url = self.get_redirect_url()
        return url or '/contribuyente/usuario/usuario-info' # FIXME use reverse here instead of hardcoding the URL 

def logout_view_cont(request):
    logout(request)
    return redirect('generales:loginC')
     

class Modulos(LoginRequiredMixin, generic.TemplateView):
    template_name = 'personal/menu_modulos.html'
    login_url = 'generales:loginP'

class Personal(LoginRequiredMixin, generic.TemplateView):
    template_name = 'personal/personal.html'
    login_url = 'generales:loginP'
    
class PersonalLoginView(LoginView):
    template_name = 'personal/login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or '/personal/modulos/' # FIXME use reverse here instead of hardcoding the URL 

def logout_view(request):
    logout(request)
    return redirect('generales:loginP')
    
