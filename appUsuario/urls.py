
from django.urls import path
from django.contrib.auth.decorators import login_required
from appUsuario.views import *

urlpatterns = [
   
    #path('registrar_usuario/',RegistrarUser.as_view(),name='registrar_usuario'),
   path('registro/',registroview, name='registro'),
   path("registro_correcto/", registroCorrecto, name="registro_correcto"),


   path('listado/', listadoUsuarios, name='verusuarios'),
   path('editar/<int:id>', editarUsuarios, name='editarusuarios'),
   path('eliminar/<int:id>', eliminarUsuarios, name='eliminarusuarios'),


#Operaciones modulo predial
   path('personal/usuario/list', usuarioListView.as_view(), name='usuario_list'),
   path('personal/usuario/add', usuarioCreateView.as_view(), name='usuario_add'),
   path('personal/usuario/edit/<int:pk>', usuarioUpdateView.as_view(), name='usuario_edit'),
   path('personal/usuario/delete/<int:pk>', usuarioDeleteView.as_view(), name='usuario_delete'),
   
   
   path('contribuyente/usuario/add-cont', usuarioCreateViewCont.as_view(), name='usuario_addcont'),
   path('contribuyente/usuario/usuario-info', usuarioInfo.as_view(), name='usuario_info'),
    
]