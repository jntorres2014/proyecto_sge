from django.forms import ModelForm

from django import forms
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

class UsuarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        # self.fields['username'].help_text = 'Por favor, ingrese la misma contraseña que antes, para verificar.'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].help_text = 'Su contraseña debe contener por lo menos 8 caracteres y al menos una letra, un número y un carácter especial'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
            
    def clean_email(self):
        email = self.cleaned_data.get('email')
        print('Verificando mauil')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está en uso. Por favor, elija otro.")
        return email
    def clean_password1(self):
        print('Verificando passwoed')
        password1 = self.cleaned_data.get('password1')

        # Verificar si la contraseña tiene al menos 8 caracteres
        if len(password1) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")

        # Verificar si la contraseña contiene letras, números y caracteres especiales
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]+$', password1):
            raise ValidationError("La contraseña debe contener letras, números y al menos un carácter especial.")

        return password1
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]
        labels ={
            'username': 'Nombre de usuario',
            'first_name' : 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
        }
        help_texts = {
            'password1': 'Su contraseña debe contener por lo menos 8 caracteres y al menos una letra, un número y un carácter especial.',
            'password2': 'Por favor, ingrese la misma contraseña que antes, para verificar.'
        }




class TaskForm (ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 
            'user',
            'descripcion', 
            'important',
        ]
        labels = {
            'title': 'Titulo', 
            'descripcion': 'Descripcion', 
            'important': 'Importante',
            'user': 'Usuario destinado'
        }