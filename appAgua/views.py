from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import generic

from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import *
from .models import *
from django.contrib.auth import logout, login
from django.views.generic import ListView, TemplateView, UpdateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


#class Incio(TemplateView):
    #template_name = 'index.html'


def pay(request):
    return render(request, 'payadmin.html')


def service(request):
    return render(request, 'serviceadmin.html')


def usuarios(request):
    return render(request, 'usuarios.html')


def contribuyentes(request):
    return render(request, 'propietarios.html')


@login_required
def homeadmin(request):
    return render(request, 'homeadmin.html')


def webpage6(request):
    return render(request, 'aguapay.html')


def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            pagos = Pago.objects.filter(no_contrato__icontains=query)
            return render(request, 'aguapay.html', {'pagos': pagos})
        else:
            print("Ese nombre no esta dado de alta en el sistema")
            return render(request, 'aguapay.html', {})


class Buscar(ListView):
    model = Pago
    template_name = 'aguapay.html'

    @property
    def get_queryset(self):
        name = self.request.GET.get('name')
        if name:
            object_list = self.model.objetcs.filter(id_propietario__name__icontains=name)
        else:
            object_list = self.model.objetcs.all()
            return object_list


def logoutuser(request):
    logout(request)
    return render(request, 'personal/principal.html')


def pagar(request):
    filter = ()


class Log(LoginRequiredMixin, generic.TemplateView):
    template_name = 'registration/login.html'


class FormularioPagoView(HttpRequest):
    def registro_pagos(request):
        pago = FormularioPagos()
        return render(request, 'pagos.html', {"form": pago})


    def procesar_pagos(request):
        pago = FormularioPagos(request.POST)
        if pago.is_valid():
            pago.save()
            pago = FormularioPagos()
        return render(request, 'pagos.html', {"form": pago, "mensaje": 'OK'})

    def listar_pagos(request):
        pagos = Pago.objects.all()
        return render(request, 'listarpagos.html', {"pagos": pagos})

def modificar_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    data = {
        'form': FormularioPagos(instance = pago)
    }
    if request.method == 'POST':
        formulario = FormularioPagos(data=request.POST, instance=pago)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="verpagos")
        data["form"] = formulario
    return render(request, 'modificarpagos.html', data)

def eliminar_pago(request, id):
    pago = get_object_or_404(Pago, id=id)
    pago.delete()
    return redirect(to="verpagos")

class FormularioServiciosView(HttpRequest):
    def registro_servicios(request):
        servicio = FormularioServicios()
        return render(request, 'agregarservicio.html', {"form": servicio})

    def procesar_servicio(request):
        servicio = FormularioServicios(request.POST)
        if servicio.is_valid():
            servicio.save()
            servicio = FormularioServicios()
        return render(request, 'agregarservicio.html', {"form": servicio, "mensaje": 'OK'})

    def listar_servicio(request):
        servicios = Servicio.objects.all()
        return render(request, 'listarservicios.html', {"servicios": servicios})

def modificar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    data = {
         'form': FormularioServicios(instance=servicio)
     }
    if request.method == 'POST':
        formulario = FormularioServicios(data=request.POST, instance=servicio)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="verservicios")
        data["form"] = formulario
    return render(request, 'modificarservicio.html', data)

def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    servicio.delete()
    return redirect(to="verservicios")


class FormularioContribuyentesView(HttpRequest):
    def registro_contribuyente(request):
        propietario = FormularioPropietarios(request.POST or None)
        return render(request, 'contribuyentes.html', {"form": propietario})

    def procesar_contribuyente(request):
        propietario = FormularioPropietarios(request.POST)
        if propietario.is_valid():
            propietario.save()
            propietario = FormularioPropietarios()
        return render(request, 'contribuyentes.html', {"form": propietario, "mensaje": 'OK'})

    def listar_contribuyente(request):
        propietarios = Propietario.objects.all()
        return render(request, 'listarcontribuyentes.html', {"propietarios": propietarios})

def modificar_contribuyente(request, id):

    propietario = get_object_or_404(Propietario, id=id)

    data = {
        'form': FormularioPropietarios(instance=propietario)
    }

    if request.method == 'POST':
        formulario = FormularioPropietarios(data=request.POST, instance=propietario)
        if formulario.is_valid():
            formulario.save()
            return  redirect(to='vercontribuyentes')
        data["form"] = formulario

    return render(request, 'modificarcontribuyente.html', data)

def eliminar_contribuyente(request, id):
    propietario = get_object_or_404(Propietario, id=id)
    propietario.delete()
    return redirect(to="vercontribuyentes")

class FormularioPrediosView(HttpRequest):
    def registro_predio(request):
        predio = FormularioPredios()
        return render(request, 'predios.html', {"form": predio})

    def procesar_predio(request):
        predio = FormularioPredios(request.POST)
        if predio.is_valid():
            predio.save()
            predio = FormularioPredios()
        return render(request, 'predios.html', {"form": predio, "mensaje": 'OK'})
