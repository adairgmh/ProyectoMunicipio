from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import widgets

from appUsuario.models import Usuario

from django.forms import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


def srt(e):
    pass


class CustomCreationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super(CustomCreationForm, self).__init__(*args, **kwargs)
        
        #las siguientes dos lineas 
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

        for fieldname in ['username','email', 'nombres','apellidos', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta: 
        model = Usuario
        fields = ('username','email', 'nombres','apellidos')

        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese el nombre del Usuario'}),
            'email' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese el email'}),
            'nombres' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese el nombre de la persona'}),
            'apellidos' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Ingrese sus apellidos de la persona'}),
            'password1' : forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}),
            'password2' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirmacion de la contraseña'}),
        }



class UserForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Usuario
        fields = ('username','email', 'nombres','apellidos','password1', 'password2')
        

        widgets = {
            'username': TextInput(
                attrs={
                    
                    'placeholder':'Ingrese el nombre del Usuario'
                }

            ),
            'email': TextInput(
                attrs={

                    'placeholder':'Ingrese el email'
                } 
            ),
            'nombres': TextInput(
                attrs={

                    'placeholder':'Ingrese el nombre de la persona'
                } 
            ),
            'apellidos': TextInput(
                attrs={

                    'placeholder':'Ingrese sus apellidos de la persona'
                } 
            ),
            'password1': PasswordInput(
                attrs={
                
                    'placeholder':'Ingrese una contraseña'
                } 
            ),
            'password2': PasswordInput(
                attrs={

                    'placeholder':'Confirmacion de la contraseña'
                } 
            ),
        

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

