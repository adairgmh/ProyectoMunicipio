from django.contrib import admin
from .models import area, ordenes_pago, concepto

# Register your models here.

admin.site.register(area)
admin.site.register(ordenes_pago)
admin.site.register(concepto)