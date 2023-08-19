from django.db import models
from datetime import datetime
from time import strftime

# Create your models here.
class area(models.Model):
    nombre = models.CharField(max_length=50, null=True, blank=True)
    descripcion = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return '%s' % (self.nombre)
    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Area'

class concepto(models.Model):
    nombre = models.CharField(max_length=30)
    monto = models.CharField(max_length=10, default=0)
    area = models.ForeignKey(area,on_delete=models.CASCADE,default='1')

    def __str__(self):
        return '%s' % (self.nombre)
    
class productos(models.Model):
    producto = models.CharField(max_length=30)

    def __str__(self):
        return '%s' % (self.producto)
    
def clave():
    mes = datetime.now().month
    mes = strftime('%b')
    op = ordenes_pago.objects.count() + 1

    return f'{mes}-{op}'

class ordenes_pago(models.Model):
    id = models.AutoField(primary_key=True)
    folio = models.CharField(max_length=50, default=clave)
    fecha_emision = models.DateField(default=datetime.now)
    nombre_solicitante = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100)
    estatus = models.BooleanField(default = False)
    producto = models.FileField(upload_to='media/', null=True, blank=True)
    # concepto = models.CharField(max_length=100)
    monto = models.FloatField(default=0)
    area = models.ForeignKey(area,on_delete=models.CASCADE,default="1")
    concepto = models.ForeignKey(concepto,on_delete=models.CASCADE, default='1')

    def __str__(self):
        return '%s' % self.id
    
    def save(self, *args, **kwargs):
        if self.concepto:
            self.monto = self.concepto.monto
            super().save(*args, **kwargs)
    
    class meta:
        db_table = 'ordenes_pago'