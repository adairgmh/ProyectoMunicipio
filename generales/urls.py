
from django.urls import include, path

from django.contrib.auth import views as auth_views
from generales.views import *
from generales import views

urlpatterns = [
    
    path('', PersonalLoginView.as_view(), name='Princpal'),
    
    path('contribuyente/', Contribuyente.as_view(), name='contribuyente'),
    path('contribuyente/area-consulta', Area_consulta.as_view(), name='area-consulta'),
    path('contribuyente/login/', ContribuyenteLoginView.as_view(), name='loginC'),
    path('contribuyente/logout/', views.logout_view_cont, name='logoutC'),

    path('personal/modulos/', Modulos.as_view(), name='modulos'),
    path('personal/', Personal.as_view(), name='personal'),
    path('personal/login/', PersonalLoginView.as_view(), name='loginP'),
    path('personal/logout/', views.logout_view, name='logout'),
    
]
