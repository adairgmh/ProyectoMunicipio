from django import forms
from .models import *
from appPredial.models import Contribuyente
from django.forms import DateInput


class FormularioPagos(forms.ModelForm):

    class Meta:
        model = Pago
        fields = ['no_servicio',
                  'fecha_pago',
                  'concepto',
                  'costo',
                  'descuento',
                  'metodo_pago',
                  'mes',
                  'anio',
                  'multa',
                  'id_cobrador',
                  'id_comunidad',
                  'id_colonia',
                  'id_propietario',
                  'id_tipos_servicio',
                  ]

        widgets = {
            'no_servicio': forms.DateInput(attrs={'type': 'number','class': 'form-control'}),
            'fecha_pago': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'concepto': forms.Select(attrs={'class': 'form-control'}),
            'costo': forms.DateInput(attrs={'type': 'number', 'class': 'form-control'}),
            'descuento': forms.NumberInput(attrs={'type': 'number', 'class': 'form-control'}),
            'metodo_pago': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),

            'anio': forms.DateInput(attrs={'type': 'number', 'class': 'form-control'}),
            'multa': forms.NumberInput(attrs={'id':'recargo',
                    'onchange': 'sumar(this.value);',

                    'class':'form-control'}),
            'id_cobrador': forms.Select(attrs={'class': 'form-control'}),
            'id_comunidad': forms.Select(attrs={'class': 'form-control'}),
            'id_colonia': forms.Select(attrs={'class': 'form-control'}),
            'id_propietario': forms.Select(attrs={'class': 'form-control'}),
            'id_tipos_servicio': forms.Select(attrs={'class': 'form-control'}),
        }


class FormularioServicios(forms.ModelForm):
    no_servicio = forms.IntegerField(widget=DateInput(attrs={'class': 'form-control', 'type': 'number'}))
    descripcion = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    costo = forms.FloatField(widget=DateInput(attrs={'class': 'form-control', 'type': 'number'}))

    class Meta:
        model = Servicio
        fields = [
            'no_servicio',
            'no_predio',
            'descripcion',
            'costo',
            'id_comunidad',
            'id_colonia',
            'id_propietario',
            'id_tipos_servicio'
        ]

        widgets = {
            'no_servicio': forms.DateInput(attrs={'type': 'number', 'class': 'form-control'}),
            'no_predio': forms.Select(attrs={'type': 'number', 'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'costo': forms.DateInput(attrs={'type': 'number', 'class': 'form-control'}),
            'id_comunidad': forms.Select(attrs={'class': 'form-control'}),
            'id_colonia': forms.Select(attrs={'class': 'form-control'}),
            'id_propietario': forms.Select(attrs={'class': 'form-control'}),
            'id_tipos_servicio': forms.Select(attrs={'class': 'form-control'})
        }


class FormularioPropietarios(forms.ModelForm):
    nombre_propietario = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    apellido_paterno = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    apellido_materno = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    genero = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    calle = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    numero_celular = forms.IntegerField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    codigo_postal = forms.IntegerField(widget=DateInput(attrs={'class': 'form-control', 'type': 'number'}))
    municipio = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    estado = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    email = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))

    class Meta:
        model = Propietario
        fields = [
            'nombre_propietario',
            'apellido_paterno',
            'apellido_materno',
            'genero',
            'calle',
            'numero_celular',
            'comunidad',
            'codigo_postal',
            'colonia',
            'municipio',
            'estado',
            'email'
        ]

        widgets = {
            'nombre_propietario': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'genero': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'calle': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'numero_celular': forms.DateInput(attrs={'type': 'number', 'class': 'form-control'}),
            'comunidad': forms.Select(attrs={'class': 'form-control'}),
            'codigo_postal': forms.DateInput(attrs={'type': 'number', 'class': 'form-control'}),
            'colonia': forms.Select(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        }


class FormularioPredios(forms.ModelForm):
    claveCatastral = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    cp = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    calle = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    numeroext = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    numeroint = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    colonia = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    ciudad = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    estado = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    tipo = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))
    rfc = forms.CharField(widget=DateInput(attrs={'class': 'form-control', 'type': 'text'}))

    class Meta:
        model = Predio
        fields = [
            'claveCatastral',
            'cp',
            'calle',
            'numeroext',
            'numeroint',
            'colonia',
            'ciudad',
            'estado',
            'tipo',
            'rfc'
        ]

        widgets = {
            'claveCatastral': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'cp': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'calle': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'numeroext': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'numeroint': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'colonia': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'type': 'text', 'class': 'form-control'}),
        }

