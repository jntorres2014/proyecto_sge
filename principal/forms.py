from django.forms import ModelForm
from .models import Task
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]
        label ={
            'username': 'Nombre de usuario',
            'first_name' : 'Nombre',
            'last_name': 'Apellido',
            'email': 'email'
        }

    



class TaskForm (ModelForm):
    class Meta:
        model = Task
        fields = [
            'title', 
            'descripcion', 
            'important',
            'user'
        ]
         