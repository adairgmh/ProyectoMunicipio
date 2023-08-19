from django import forms
from django.forms.models import fields_for_model
from .models import area, ordenes_pago, concepto

class AreaForm(forms.ModelForm):
    class Meta:
        model = area
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in iter (self.fields):
                self.fields[field].widget.attrs.update({'class':'form-control'})

class OPForm(forms.ModelForm):
    class Meta:
        model = ordenes_pago
        fields = [
            'folio',
            'fecha_emision',
            'nombre_solicitante',
            'descripcion',
            'area',
            'concepto',
            'monto',
            'producto',
        ]

        labels = {
            'folio' : 'Folio',
            'fecha_emision': 'Fecha de emision',
            'nombre_solicitante': 'Nombre del solicitante',
            'descripcion': 'Descripcion',
            'area': 'Area',
            'concepto': 'Concepto',
            'monto': 'Monto',
            'producto': 'producto'
        }

        widget = {
            'folio' : forms.TextInput(),
            'fecha_emision': forms.DateInput(attrs={'type':'date','class':'form-control'}),
            'nombre_solicitante': forms.TextInput(),
            'descripcion': forms.TextInput(),
            'area': forms.TextInput(),
            'concepto':forms.TextInput(),
            'monto':forms.TextInput(),
            'producto': forms.FileInput()
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in iter(self.fields):
                self.fields[field].widget.attrs.update({'class': 'forms-control'})

class conceptoForm(forms.ModelForm):
    class Meta:
        model = concepto
        fields = ['nombre', 'monto', 'area']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter (self.fields):
            self.fields[field].widget.attrs.update({'class':'form-control'})

class respuestaForm(forms.ModelForm):
    status = [
        ('True', 'Pagado'),
        ('False', 'Por pagar')
    ]
    estatus = forms.ChoiceField(choices=status,widget=forms.RadioSelect)

    class Meta:
        model = ordenes_pago
        fields = [
            'id',
            'estatus',
        ]

        labels = {
            'id':'id',
            'estatus':'estatus',
        }