from django.contrib import admin
from appPredial.models import *
from django.contrib.auth.admin import UserAdmin



admin.site.register(Contribuyente)
admin.site.register(Predio)
admin.site.register(TipoPredio)
admin.site.register(Pago)
admin.site.register(FormaPago)
admin.site.register(CodigoPostal)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(Comunidad)
admin.site.register(Colonia)

