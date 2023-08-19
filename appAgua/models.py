from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime
from multiselectfield import MultiSelectField
from django.db.models.signals import post_save
from django.dispatch import receiver
from appUsuario.models import Usuario


class Colonia(models.Model):
     nombre_colonia = models.CharField(max_length=45)

     def __str__(self):
          return self.nombre_colonia


class Comunidad(models.Model):
     nombre_comunidad = models.CharField(max_length=45)

     def __str__(self):
          return self.nombre_comunidad


class Concepto(models.Model):
     nombre_concepto = models.CharField(max_length=45)

     def __str__(self):
          return self.nombre_concepto


class Propietario(models.Model):
     nombre_propietario = models.CharField(max_length=45)
     apellido_paterno = models.CharField(max_length=45)
     apellido_materno = models.CharField(max_length=45)
     genero = models.CharField(max_length=15)
     calle = models.CharField(max_length=45)
     numero_celular = models.CharField(max_length=10)
     comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
     codigo_postal = models.IntegerField()
     colonia = models.ForeignKey(Colonia, on_delete=models.CASCADE)
     municipio = models.CharField(max_length=45)
     estado = models.CharField(default="Tlaxcala", max_length=45)
     email = models.CharField(max_length=45)
     
     

     def __str__(self):
          nombre = self.nombre_propietario+" "+self.apellido_paterno+" "+self.apellido_materno
          return nombre


class Tipos_servicio(models.Model):
     clave_tipo_servicio = models.CharField(max_length=45)
     tipo_uso_de_servicio = models.CharField(max_length=45)
     descripcion = models.CharField(max_length=45)

     def __str__(self):
          return self.tipo_uso_de_servicio


class Cobrador(models.Model):
     nombre = models.CharField(max_length=45)

     def __str__(self):
          return self.nombre


class Predio(models.Model):
    claveCatastral=models.CharField(max_length=31, unique=True)
    cp=models.CharField(max_length=45)
    calle=models.CharField(max_length=45)
    numeroext=models.CharField(max_length=45)
    numeroint=models.CharField(max_length=45)
    colonia=models.CharField(max_length=45)
    ciudad=models.CharField(max_length=45)
    estado=models.CharField(max_length=45)
    tipo = models.CharField(max_length=12)
    rfc = models.CharField(max_length=18)

    def __str__(self):
         return self.claveCatastral

class Servicio(models.Model):
     no_servicio = models.CharField(unique=True, max_length=10)
     no_predio = models.ForeignKey(Predio, on_delete=models.CASCADE)
     descripcion = models.CharField(max_length=200)
     costo = models.FloatField()
     id_comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
     id_colonia = models.ForeignKey(Colonia, on_delete=models.CASCADE)
     id_propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
     id_tipos_servicio = models.ForeignKey(Tipos_servicio, on_delete=models.CASCADE)

     def __str__(self):
          return str(self.no_servicio)

class Pagos_anuales(models.Model):
     no_servicio = models.IntegerField()
     anio = models.IntegerField()
     fecha = models.DateField()
     monto_mensual = models.FloatField()
     descuento = models.FloatField()
     multa = models.CharField(max_length=45)
     id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
     id_comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
     id_colonia = models.ForeignKey(Colonia, on_delete=models.CASCADE)
     id_propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)


class Pago(models.Model):
     no_servicio = models.CharField(unique=True, max_length=10)
     fecha_pago = models.DateField(default=datetime.now)
     concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE)
     costo = models.FloatField(default=0.00)
     descuento = models.FloatField(default=0.00)
     metodo_pago = models.CharField(max_length=50)
     mes_choices = (
          ('Enero', 'Enero'),
          ('Febrero', 'Febrero'),
          ('Marzo', 'Marzo'),
          ('Abril', 'Abril'),
          ('Mayo', 'Mayo'),
          ('Junio', 'Junio'),
          ('Julio', 'Julio'),
          ('Agosto', 'Agosto'),
          ('Septiembre', 'Septiembre'),
          ('Octubre', 'Octubre'),
          ('Noviembre', 'Noviembre'),
          ('Diciembre', 'Diciembre')
            )
     mes = MultiSelectField(max_length=15, choices=mes_choices)
     anio = models.IntegerField(default=0)
     multa = models.IntegerField(default=0)
     id_cobrador = models.ForeignKey(Cobrador, on_delete=models.CASCADE)
     id_comunidad = models.ForeignKey(Comunidad, on_delete=models.CASCADE)
     id_colonia = models.ForeignKey(Colonia, on_delete=models.CASCADE)
     id_propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
     id_tipos_servicio = models.ForeignKey(Tipos_servicio, on_delete=models.CASCADE)





