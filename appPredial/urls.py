
from django.urls import include, path

from django.contrib.auth import views as auth_views
from appPredial import views

from appPredial.views import *

urlpatterns = [
    
    
    path('personal/predial/', Predial.as_view(), name='predial'),

    path('personal/predial/contribuyente/list', contribuyenteListView.as_view(), name='contribuyente_list'),
    path('personal/predial/contribuyente/add', contribuyenteCreateView.as_view(), name='contribuyente_add'),
    path('personal/predial/contribuyente/edit/<int:pk>', contribuyenteUpdateView.as_view(), name='contribuyente_edit'),
    path('personal/predial/contribuyente/delete/<int:pk>', contribuyenteDeleteView.as_view(), name='contribuyente_delete'),
    
    path('personal/predial/predio/list', views.predioBuscar, name='predio_list'),
    path('personal/predial/predio/add', predioCreateView.as_view(), name='predio_add'),
    path('personal/predial/predio/edit/<int:pk>', predioUpdateView.as_view(), name='predio_edit'),
    path('personal/predial/predio/delete/<int:pk>', predioDeleteView.as_view(), name='predio_delete'),
    
    path('personal/predial/pago/', PagoView.as_view(), name='pago_index'),
    path('personal/predial/pago/historial_adeudos', HistorialAdeudosListView.as_view(), name='historial_adeudos'),
    path('personal/predial/pago/historial_pagados', views.pago, name='historial_pagados'),
    path('personal/predial/pago/add/', pagoCreateView.as_view(), name='pago_add'),
    path('personal/predial/pago/pagar/<int:pk>', pagoUpdateView.as_view(), name='pagar'),
    path('personal/predial/pago/reportes/', ReportesPagoView.as_view(), name='reporte_pago'),
    path('personal/predial/pago/timbrar/', TimbrarPredial, name='timbrar_predial'),
    
    path('personal/predial/timbrado/', timbradoListView.as_view(), name='timbrado_list'),
    path('personal/predial/timbrado/timbrar/<int:pk>', Timbrar.as_view(), name='timbrar'),
    
    path('contribuyente/predial/informacion-predio/<int:id>', informacionPredio.as_view(), name='predio_info_cont'),
    path('contribuyente/predial/pagoP/add/<int:pk>', pagoUpdateViewCont.as_view(), name='pagoP_add'),
    path('contribuyente/predial/pagoP/historial', views.pagoCont, name='historialCont'),
    
    
    
    
]
#path('personal/predial/pago/', historialListView.as_view(), name='historial'),

# path('personal/predial/pago/', vbuscar.as_view(), name='pago_index'),
#
 #   