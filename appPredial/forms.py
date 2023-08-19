from datetime import date
from django.forms import *
from appPredial.models import *
from django.db.models import Q
from  django.core.validators import RegexValidator
from django.core.exceptions import ValidationError,ObjectDoesNotExist



class contribuyenteForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['numeroext'].required = True
        self.fields['numeroint'].required = False
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Contribuyente
        fields = ['rfc','curp','name', 'ap', 'am', 'email', 'estado', 'municipio', 'comunidad', 'colonia','cp', 'calle', 'numeroint', 'numeroext']
        labels = {
            'rfc':'RFC',
            'curp':'CURP',
            'name':'Nombre',
            'ap':'Apellido Paterno',
            'am':'Apellido Materno',
            'email':'Email',
            'estado':'Estado',
            'municipio':'Municipio',
            'comunidad':'Comunidad',
            'colonia':'Colonia',
            'cp':'Código Postal',
            'calle':'Calle',
            'numeroint':'Número Interior',
            'numeroext':'Número Exterior',
            
            
            
            }
        
        widgets = {
            'rfc': TextInput(
                attrs={
                    
                    'placeholder':'Ingrese el RFC del contribuyente'
                }

            ),
            'curp': TextInput(
                attrs={

                    'placeholder':'Ingrese el CURP del contribuyente'
                } 
            ),
            'name': TextInput(
                attrs={

                    'placeholder':'Ingrese el nombre del contribuyente'
                } 
            ),
            'ap': TextInput(
                attrs={

                    'placeholder':'Ingrese el apellido paterno del contribuyente'
                } 
            ),
            'am': TextInput(
                attrs={
                
                    'placeholder':'Ingrese el apellido materno del contribuyente'
                } 
            ),
            'email': TextInput(
                attrs={

                    'placeholder':'Ingrese el correo electronico del contribuyente'
                } 
            ),
            'cp': TextInput(
                attrs={

                    'placeholder':'Ingrese el codigo postal'
                } 
            ),
            'calle': TextInput(
                attrs={

                    'placeholder':'Ingrese el nombre de la calle'
                } 
            ),

            'numeroext': TextInput(
                attrs={

                    'placeholder':'Ingrese el numero exterior'
                } 
            ),
            'numeroint': TextInput(
                attrs={

                    'placeholder':'Ingrese el numero interior'
                } 
            ),
            'estado': Select(
                attrs={

                    'placeholder':'Ingrese el nombre del estado'
                } 
            ),
            'municipio': Select(
                attrs={
                    
                    'placeholder':'Ingrese el nombre del municipio'
                } 
            ),
            'comunidad': Select(
                attrs={

                    'placeholder':'Ingrese el nombre de la comunidad'
                } 
            ),
            'colonia': Select(
                attrs={

                    'placeholder':'Ingrese el nombre de la colonia'
                } 
            )

        }
        
    """ Funciones Clean """
    def clean_rfc(self):
        return self.cleaned_data["rfc"].upper()
    
    def clean_curp(self):
        return self.cleaned_data["curp"].upper()
    
    def clean_name(self):
        return self.cleaned_data["name"].upper()
    
    def clean_ap(self):
        return self.cleaned_data["ap"].upper()
    
    def clean_am(self):
        return self.cleaned_data["am"].upper()
    
    def clean_calle(self):
        return self.cleaned_data["calle"].upper()
    
    def clean_email(self):
        return self.cleaned_data["email"].lower()
    
    def save(self, commit=True):
        data={}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
    def validator_rfc(value):
        if value[0] != 's':
            raise ValidationError('RFC starts with s')    
        
class predioForm(ModelForm):

    def __init__(self, *args, rfc=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['numeroext'].required = True
        self.fields['numeroint'].required = False
        
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
        
        if rfc is not None:
            self.initial['rfc'] = rfc

    class Meta:
        model = Predio
        fields = ['claveCatastral', 'estado', 'municipio', 'comunidad', 'colonia', 'cp', 'calle', 'numeroint', 'numeroext', 'idtipo', 'rfc' ]
        labels = {
            'claveCatastral': 'Clave Catastral',
            'cp': 'Código Postal',
            'calle': 'Calle',
            'numeroext': 'Número Exterior',
            'numeroint': 'Número Interior',
            'colonia': 'Colonia',
            'comunidad': 'Comunidad',
            'municipio': 'Municipio',
            'estado': 'Estado',
            'idtipo': 'Tipo de Predio',
            'rfc': 'RFC',


        } 

        
        
        widgets = {
            'claveCatastral': TextInput(
                attrs={
                    
                    'placeholder':'Ingrese la clave catastral'
                } 
            ),
            'cp': Select(
                
            ),
            'calle': TextInput(
                attrs={
                    
                    'placeholder':'Ingrese el nombre de la calle'
                } 
            ),
            'numeroext': TextInput(
                attrs={
                    
                    'placeholder':'Ingrese el numero exterior'
                } 
            ),
            'numeroint': TextInput(
                attrs={
                    
                    'placeholder':'Ingrese el numero interior'
                } 
            ),
            'colonia': Select(
    
            ),
            'comunidad': Select(
                
            ),
            'municipio': TextInput(
                attrs={
                    
                    'readonly': 'readonly'
                } 
            ),
            'estado': TextInput(
                attrs={
                    
                    'readonly': 'readonly'
                } 
            ),
            'idtipo': Select(
                
            ),
            'rfc': TextInput(
                attrs={
                    
                    'readonly': 'readonly'
                } 
                
            )

        }
        
    def save(self, commit=True):
        data={}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class pagoForm(ModelForm):

    def __init__(self, *args, claveCatastral=None, monto=None, fechaPago=None, agnio=None, **kwargs):
        super().__init__(*args, **kwargs)
        
            
        if claveCatastral is not None:
            self.initial['claveCatastral'] = claveCatastral
        
        if monto is not None:
            self.initial['monto'] = monto
        
        if fechaPago is not None:
            self.initial['fechaPago'] = fechaPago
        
        if agnio is not None:
            self.initial['agnio'] = agnio
            

    class Meta:
        model = Pago
        fields = '__all__'

        
        widgets = {
            'agnio': NumberInput(
                attrs={
                    
                    'placeholder':'Ingrese el año',
                    'class':'form-control'
                } 
            ),
            'recargo': NumberInput(
                attrs={
                    'id':'recargo',
                    'onchange': 'sumar(this.value);',
                    
                    'class':'form-control'
                } 
            ),
            'descuento': NumberInput(
                attrs={
                    'id':'descuento',
                    'onchange': 'restar(this.value);',
                    
                    'class':'form-control'
                } 
            ),
            'fechaPago': DateInput(
                attrs={
                    'id':'fechaPago',
                    'class':'form-control'
                } 
            ),
            'total': NumberInput(
                attrs={
                    'id':'spTotal',
                    'class':'form-control'
                } 
            ),
            'formaPago': Select(
                attrs={
                    
                    'class':'form-control'

                } 
            ),
            'claveCatastral': Select(
                attrs={
                    
                    'class':'form-control'

                }
                 
            ),
            'status_pagado': RadioSelect(
                attrs={
                    
                    
                        
                },
                choices={
                    ('True','Pagado'),
                    ('False','Pendiente')
                } 
            ),
            
            'status_inapam': CheckboxInput(
                attrs={
                    'id':'inapam',
                    'class':'form-check-input'

                }
                
            )
        }
    
    def clean_agnio(self):
        anio = self.cleaned_data.get('agnio')
        if anio > int(datetime.today().strftime('%Y')):
            raise forms.ValidationError('No se puede adelantar pagos')
            
        claveCatastral = self.cleaned_data.get('claveCatastral')
    
        Agnioexistente = Pago.objects.filter(claveCatastral=claveCatastral, agnio=anio)
        print("Primer print: ",Agnioexistente)
        
        if self.instance:
                Agnioexistente = Agnioexistente.exclude(id=self.instance.id)
        if Agnioexistente.exists():
                raise forms.ValidationError("The Year Input already here")
        return anio
           
    def save(self, commit=True):
        data={}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class contribuyentepagoForm(ModelForm):

    def __init__(self, *args, claveCatastral=None, monto=None, recargo=None, descuento=None, total=None, fecha=None, **kwargs):
        super().__init__(*args, **kwargs)
        
            
        if claveCatastral is not None:
            self.initial['claveCatastral'] = claveCatastral
        
        if monto is not None:
            self.initial['monto'] = monto
        
        if fecha is not None:
            self.initial['fechaPago'] = fecha
        
        if recargo is not None:
            self.initial['recargo'] = recargo
        
        if total is not None:
            self.initial['total'] = total
            
            
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            
            

    class Meta:
        model = Pago
        fields = '__all__'

        
        widgets = {
            'agnio': NumberInput(
                attrs={
                    
                    'placeholder':'Ingrese el año'
                } 
            ),
            'recargo': NumberInput(
                attrs={
                    
                    'placeholder':'Ingrese el nombre de la calle'
                } 
            ),
            'descuento': NumberInput(
                attrs={
                    
                    'placeholder':'Ingrese el numero exterior'
                } 
            ),
            'fechaPago': DateInput(
                attrs={
                    
                    'placeholder':'Ingrese el numero interior'
                } 
            ),
            'total': NumberInput(
                attrs={
                    
                    
                } 
            ),
            'formaPago': Select(
                attrs={
                    
                    

                } 
            ),
            'claveCatastral': Select(
                attrs={
                    
                    

                } 
            ),
            
        }
    
    def clean_agnio(self):
        anio = self.cleaned_data.get('agnio')
        try: 

            Agnioexistente = Pago.objects.get(agnio=anio)
            
            if Agnioexistente is not None:
                raise forms.ValidationError('No se puede registrar el mismo año ya pagado')
            
            
        except ObjectDoesNotExist:
            return anio
    
    
    def save(self, commit=True):
        data={}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

class ReportForm(Form):
    
        
    date_range = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    
class RespuestaForm(ModelForm):
    
    statusc = [
        ('True','Timbrado'),
        ('False','Pendiente')
    ]
    
    status_timbrado = ChoiceField(choices=statusc,widget=RadioSelect)


    class Meta:
        model = Pago
        fields = [
            'id',
            'status_timbrado',
            ]
        
        
        
    def save(self, commit=True):
        data={}
        form = super()
        try:
            if form.is_valid():
                form.save()
                print (data)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    
class pagoFormCont(ModelForm):

    def __init__(self, *args, claveCatastral=None, monto=None, fechaPago=None, agnio=None, **kwargs):
        super().__init__(*args, **kwargs)

        
        
            
        if claveCatastral is not None:
            self.initial['claveCatastral'] = claveCatastral
        
        if monto is not None:
            self.initial['monto'] = monto
        
        if fechaPago is not None:
            self.initial['fechaPago'] = fechaPago
        
        if agnio is not None:
            self.initial['agnio'] = agnio

        
     
    class Meta:
        model = Pago
        fields = '__all__'

        
        widgets = {
            'agnio': NumberInput(
                attrs={
                    'readonly':True,
                    'placeholder':'Ingrese el año',
                    'class':'form-control'
                } 
            ),
             
            'fechaPago': DateInput(
                attrs={
                    'id':'fechaPago',
                    'class':'form-control'
                } 
            ),
            'total': NumberInput(
                attrs={
                    'id':'spTotal',
                    'class':'form-control'
                } 
            ),
            'formaPago': Select(
                attrs={
                    
                    'class':'form-control'

                } 
            ),
            'claveCatastral': Select(
                attrs={
                    'readonly':'readonly',
                    'class':'form-control'

                }
                 
            ),
            'status_pagado': RadioSelect(
                attrs={
                    
                    
                        
                },
                choices={
                    ('True','Pagado'),
                    ('False','Pendiente')
                } 
            ),
            
            'status_inapam': CheckboxInput(
                attrs={
                    'id':'inapam',
                    'class':'form-check-input'

                }
                
            )
        }
    
    def clean_agnio(self):
        anio = self.cleaned_data.get('agnio')
        if anio > int(datetime.today().strftime('%Y')):
            raise forms.ValidationError('No se puede adelantar pagos')
            
        claveCatastral = self.cleaned_data.get('claveCatastral')
    
        Agnioexistente = Pago.objects.filter(claveCatastral=claveCatastral, agnio=anio)
        print("Primer print: ",Agnioexistente)
        
        if self.instance:
                Agnioexistente = Agnioexistente.exclude(id=self.instance.id)
        if Agnioexistente.exists():
                raise forms.ValidationError("The Year Input already here")
        return anio
           
    
    def save(self, commit=True):
        data={}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data