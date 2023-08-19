from django.db import models
from datetime import datetime
from django.forms import model_to_dict

from django.utils.translation import gettext_lazy as _

from django.core.validators import RegexValidator

from appUsuario.models import Usuario
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.core.exceptions import ValidationError




""" Clase para pasar a mayusculas los charfield """


class Estado(models.Model):
     nombre_estado = models.CharField(max_length=45)
     

     def __str__(self):
        return self.nombre_estado
     
     class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
        

class Municipio(models.Model):
     nombre_municipio = models.CharField(max_length=45)
     id_estado=models.ForeignKey(Estado, on_delete=models.CASCADE)

     def __str__(self):
        return self.nombre_municipio
     
     class Meta:
        verbose_name = 'Municipio'
        verbose_name_plural = 'Municipios'

          
     

class Comunidad(models.Model):
     nombre_comunidad = models.CharField(max_length=45)
     id_municipio=models.ForeignKey(Municipio, on_delete=models.CASCADE)

     def __str__(self):
          return self.nombre_comunidad
    
     
     class Meta:
        verbose_name = 'Comunidad'
        verbose_name_plural = 'Comunidades'

class Colonia(models.Model):
     nombre_colonia = models.CharField(max_length=45)
     id_comunidad=models.ForeignKey(Comunidad, on_delete=models.CASCADE)

     def __str__(self):
          return self.nombre_colonia
     
     class Meta:
        verbose_name = 'Colonia'
        verbose_name_plural = 'Colonias'

class CodigoPostal(models.Model):
    codigoPostal = models.CharField(max_length=45, verbose_name='Codigo Postal')
    
    def __str__(self):
        return str(self.codigoPostal)
    
    class Meta:
        verbose_name = 'Codigo Postal'
        verbose_name_plural = 'Codigo Postales'
        ordering = ['id']

class Contribuyente(models.Model):
    rfc=models.CharField(max_length=13, 
                         unique=True, 
                         verbose_name='RFC',
                         validators=[
                             RegexValidator(r'^([A-ZÑ\x26]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])([A-Z]|[0-9]){2}([A]|[0-9]){1})?$', message='RFC es incorrecto')
                             ],
                         help_text=_("format: APMNXXXXXXHHH")
                         )
    curp=models.CharField(max_length=18, unique=True, verbose_name='CURP', 
                          validators=[
                            RegexValidator(r'^([A-Z][AEIOUX][A-Z]{2}\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[HM](?:AS|B[CS]|C[CLMSH]|D[FG]|G[TR]|HG|JC|M[CNS]|N[ETL]|OC|PL|Q[TR]|S[PLR]|T[CSL]|VZ|YN|ZS)[B-DF-HJ-NP-TV-Z]{3}[A-Z\d])(\d)$', message='El CURP es incorrecto')
        
                          ]
                         )
    email=models.CharField(max_length=45, unique=True, verbose_name='Email')

    def actualiza_contribuyente(self, new_rfc=None, new_curp=None, new_email=None):
        editorDB = BaseDatabaseSchemaEditor(connection=self._state.db)
        # Elimina la restricción UNIQUE de los campos.
        if new_rfc is not None:
            editorDB.remove_constraint(self._meta.db_table, 'rfc')

        if new_curp is not None:
            editorDB.remove_constraint(self._meta.db_table, 'curp')

        if new_email is not None:
            editorDB.remove_constraint(self._meta.db_table, 'email')

        if new_rfc is not None:
            self.rfc = new_rfc
        if new_curp is not None:
            self.curp = new_curp
        if new_email is not None:
            self.email = new_email
        self.save()

        #Valida si hay rfc, curp o email duplicados
        if new_rfc is not None:
            duplicados = Contribuyente.objects.filter(rfc=new_rfc).exclude(id=self.id)
            if duplicados.exists():
                raise ValueError(f"Ya hay un contribuyente registrado con ese RFC '{new_rfc}'")
        if new_curp is not None:
            duplicados = Contribuyente.objects.filter(curp=new_curp).exclude(id=self.id)
            if duplicados.exists():
                raise ValueError(f"Ya hay un contribuyente registrado con ese CURP '{new_curp}'")
        if new_email is not None:
            duplicados = Contribuyente.objects.filter(email=new_email).exclude(id=self.id)
            if duplicados.exists():
                raise ValueError(f"Ya hay un contribuyente registrado con ese EMAIL '{new_email}'")

        #Agrega nuevamente las restricciones de UNIQUE
        if new_rfc is not None:
            editorDB.add_constraint(self._meta.db_table, models.UniqueConstraint('rfc'))
        if new_curp is not None:
            editorDB.add_constraint(self._meta.db_table, models.UniqueConstraint('curp'))
        if new_email is not None:
            editorDB.add_constraint(self._meta.db_table, models.UniqueConstraint('email'))
        



    name=models.CharField(max_length=300, verbose_name='Nombre')
    ap=models.CharField(max_length=45, verbose_name='Apellido Paterno')
    am=models.CharField(max_length=45, verbose_name='Apellido Materno')
    calle=models.CharField(max_length=45, verbose_name='Calle')
    numeroext=models.CharField(max_length=45, 
                               verbose_name='Numero Exterior',
                               validators=[RegexValidator(r'^[0-9]+$', message='Ingresa solo números en Número exterior')],
                               )
    numeroint=models.CharField(max_length=45, 
                               verbose_name='Numero Interior',
                               validators=[RegexValidator(r'^[0-9]+$', message='Ingresa solo números en Número interior')]
                               )
    cp=models.CharField(max_length=45, verbose_name='Codigo Postal')
    estado=models.ForeignKey(Estado, default="", on_delete=models.CASCADE)
    municipio=models.ForeignKey(Municipio, default="", on_delete=models.CASCADE)
    comunidad=models.ForeignKey(Comunidad, default="", on_delete=models.CASCADE)
    colonia=models.ForeignKey(Colonia, default="", on_delete=models.CASCADE)
    
    
    
    def __str__(self):
        return self.rfc

    class Meta:
        verbose_name = 'Contribuyente'
        verbose_name_plural = 'Contribuyentes'
    
    

class TipoPredio(models.Model):
    tipo=models.CharField(max_length=45, verbose_name='tipo')
    costo=models.FloatField(default=0.00)
    
    def __str__(self):
        return self.tipo

    class Meta:
        verbose_name = 'TipoPredio'
        verbose_name_plural = 'TiposPredios'
        ordering = ['id']




    
class Predio(models.Model):
    claveCatastral=models.CharField(max_length=31, unique=True, verbose_name='Clave Catastral')
    cp=models.ForeignKey(CodigoPostal, on_delete=models.CASCADE)
    calle=models.CharField(max_length=45, verbose_name='Calle')
    numeroext=models.CharField(max_length=45, verbose_name='Numero Exterior')
    numeroint=models.CharField(max_length=45, verbose_name='Numero Interior')
    colonia=models.ForeignKey(Colonia, default="", on_delete=models.CASCADE)
    comunidad=models.ForeignKey(Comunidad, default="", on_delete=models.CASCADE)
    municipio=models.CharField(default="TZOMPANTEPEC", max_length=45, verbose_name='Municipio')
    estado=models.CharField(default="TLAXCALA", max_length=45, verbose_name='Estado')
    idtipo = models.ForeignKey(TipoPredio, on_delete=models.CASCADE, verbose_name='Tipo de Predio')
    rfc = models.ForeignKey(Contribuyente, on_delete=models.CASCADE, verbose_name= 'RFC', to_field='rfc')
    
    def __str__(self):
        return str(self.claveCatastral)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Predio'
        verbose_name_plural = 'Predios'

class FormaPago(models.Model):
    formaPago = models.CharField(default="", max_length=45, verbose_name='Forma de Pago')

    def __str__(self):
        return self.formaPago

    class Meta:
        verbose_name = 'Formas de Pago'
        verbose_name_plural = 'Formas de Pago'

class Pago(models.Model):
    formaPago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)
    claveCatastral = models.ForeignKey(Predio, on_delete=models.CASCADE, verbose_name='Clave Catastral', to_field='claveCatastral')
    agnio = models.IntegerField(default=0, verbose_name='Año')
    recargo = models.FloatField(default=0.00, verbose_name='Recargo')
    descuento = models.FloatField(default=0.00, verbose_name='Descuento')
    status_inapam = models.BooleanField(default=False, verbose_name='INAPAM')
    fechaPago = models.DateField(verbose_name='Fecha de Pago')
    total = models.FloatField(default=0.00, verbose_name='Total')
    status_timbrado = models.BooleanField(default=False, verbose_name='Status del Timbrado')
    status_pagado = models.BooleanField(default=False, verbose_name='Status del Pago')
    
    def __str__(self):
        return 'CC: %s, Año: %s' % (self.claveCatastral, self.agnio)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        
        




