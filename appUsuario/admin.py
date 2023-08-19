from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from appUsuario.models import Usuario
# Register your models here.
from django.contrib import admin
from appUsuario.models import Usuario
from django.contrib.auth.admin import UserAdmin
#from usuario.forms import FormUsuario

from django.contrib.auth.admin import UserAdmin 


admin.site.register(Usuario)