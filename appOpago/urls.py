from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from appOpago.views import seccionOP, listOrden, createOrden, ticket, estatus, updateEstatus, pdfView

urlpatterns = [
    path('ordenesp/', seccionOP.as_view(), name='ordenesp'),
    path('listar_areas/', views.listarArea, name='listar_area'),
    path('crear_area/', views.crearArea, name='crear_area'),
    re_path(r'^editar_area/(?P<id>\d+)$', views.editarArea, name="editar_area"),
    re_path(r'^eliminar_area/(?P<id>\d+)$', views.eliminarArea, name="eliminar_area"),
    path('consulta_area/', listOrden.as_view(), name='consulta_area'),
    path('nueva_orden/', createOrden.as_view(), name='nueva_orden'),
    path('ticket/<int:pk>', ticket.as_view(), name='ticket'),
    path('listar_conceptos/', views.listarConcepto, name='listar_conceptos'),
    path('crear_concepto/', views.crearConcepto, name='crear_concepto'),
    re_path(r'^editar_concepto/(?P<id>\d+)$', views.editarConcepto, name="editar_concepto"),
    re_path(r'^eliminar_concepto/(?P<id>\d+)$', views.eliminarConcepto, name="eliminar_concepto"),
    path('reportes/', views.reportes, name='reportes'),
    path('caja/', estatus.as_view(), name='caja'),
    path('modificar/<int:pk>', updateEstatus.as_view(), name='modificar'),
    path('pdf/<int:pk>', pdfView.as_view(), name='pdf'),
]