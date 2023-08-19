"""ProyectoMunicipio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from appAgua.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(('generales.urls','generales'), namespace='generales')),
    path('',include(('appPredial.urls','predial'), namespace='predial')),
    path('',include(('appUsuario.urls','usuario'), namespace='usuario')),

    path('Agua/', include(('appAgua.urls','Agua'), namespace='Agua')), ## 

    #urls agua

    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logoutuser, name='logout'),
    #path('', Incio.as_view(), name='inicio'),

    path('Modulo_agua/pagos/registro/', FormularioPagoView.registro_pagos, name='registropagos'),
    path('Modulo_agua/pagos/registrado/', FormularioPagoView.procesar_pagos, name='guardarpagos'),
    path('Modulo_agua/pagos/historial/', FormularioPagoView.listar_pagos, name='verpagos'),
    path('Modulo_agua/pagos/historial/modificar/<id>/', modificar_pago, name='modificarpago'),
    path('Modulo_agua/eliminar_pago/<id>/', eliminar_pago, name='eliminarpago'),

    path('Modulo_agua/servicios/registro/', FormularioServiciosView.registro_servicios, name='registroservicios'),
    path('Modulo_agua/servicios/registrado/', FormularioServiciosView.procesar_servicio, name='guardarservicios'),
    path('Modulo_agua/servicios/historial/', FormularioServiciosView.listar_servicio, name='verservicios'),
    path('Modulo_agua/servicios/historial/modificar/<id>/', modificar_servicio, name='modificarservicio'),
    path('Modulo_agua/eliminar_servicio/<id>/', eliminar_servicio, name='eliminarservicio'),

    path('Modulo_agua/contribuyentes/registro/', FormularioContribuyentesView.registro_contribuyente, name='registrocontribuyente'),
    path('Modulo_agua/contribuyentes/registrado/', FormularioContribuyentesView.procesar_contribuyente, name='guardarcontribuyente'),
    path('Modulo_agua/contribuyentes/historial/', FormularioContribuyentesView.listar_contribuyente, name='vercontribuyentes'),
    path('Modulo_agua/contribuyentes/historial/modificar/<id>/', modificar_contribuyente, name='modificarcontribuyente'),
    path('Modulo_agua/eliminar_contribuyente/<id>/', eliminar_contribuyente, name='eliminarcontribuyente'),

    path('Modulo_agua/servicios/registro/nuevo_predio/', FormularioPrediosView.registro_predio, name='registropredios'),
    path('Modulo_agua/servicios/registro/predio_guardado/', FormularioPrediosView.procesar_predio, name='guardarpredio'),

    path('contribuyente/', webpage6, name='webpage6'),
    path('consultas/', search, name='search'),
    path('consultas1/', Buscar.as_view(), name='search1'),
    path('Modulo_agua/home/', homeadmin, name='homeadmin'),
    path('Modulo_agua/pagos/', pay, name='pay'),
    path('Modulo_agua/servicios/', service, name='service'),
    path('Modulo_agua/usuarios/', usuarios, name='usuarios'),
    path('Modulo_agua/contribuyentes/', contribuyentes, name='contribuyentes'),
    path("", include(('appUsuario.urls','usuarios'))),
    path('login/', Log.as_view(), name='login'),

    #URL de Aplicacion ordenes de pago
    path('', include('appOpago.urls')),
]
