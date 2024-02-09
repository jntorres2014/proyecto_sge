from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate

from Core.models import Ciclo, PlanDeEstudios
from .forms import TaskForm, UsuarioForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView
from django.urls import reverse_lazy

class CustomPasswordChangeView(PasswordResetView):
    template_name = 'reset_pass.html'
    success_url = reverse_lazy('reset_password_done')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'custom_reset_password.html'  # Plantilla personalizada
    email_template_name = 'custom_reset_password_email.html'  # Plantilla de correo electrónico personalizada

class PasswordResetCompleteView(PasswordResetDoneView):
    template_name = 'reset_pass_complete.html'  # Plantilla personalizada
    email_template_name = 'custom_reset_password_email.html'  # Plantilla de correo electrónico personalizada

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'reset_pass_confirm.html'  # Plantilla personalizada
    email_template_name = 'custom_reset_password_email.html'  # Plantilla de correo electrónico personalizada    
class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'reset_password_done.html'  # Plantilla personalizada
        

@login_required
def home2(request):
    hay_plan=PlanDeEstudios.objects.exists()
    hay_ciclo = Ciclo.objects.exists()
    print(hay_ciclo)
    if hay_ciclo:
        ciclo_activo = Ciclo.objects.get(esActual= 'True').fechaFin >= timezone.now().date()
        print("ciclo activo",ciclo_activo)
    else:
            ciclo_activo='False'
    return render(request, 'home.html',{'hay_plan': hay_plan,
                                        'ciclo_activo': ciclo_activo} )
@login_required
def inscripciones(request):
       return render(request, ' inscripciones.html')

@login_required
def create_task(request):
    if request.method == 'GET':      
        return render(request, 'create_task.html',{
            'form': TaskForm,
        })
    else:
        try:
            form= TaskForm(request.POST)
            tarea= form.save(commit=False)
            tarea.user= request.user
            tarea.save()
            return redirect(principal)
        except ValueError:
            return render(request, 'create_task.html',{
            'form': TaskForm,
            'error': 'Ingresar datos validos',
        })

def signup(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            print('era valido')
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.create_user(
                        username=request.POST['username'],
                        password=request.POST['password1'],
                        email=request.POST['email'],
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name']
                    )
                    user.save()
                    return redirect('registro_exitoso')  # Redireccion a una página de registro exitoso
                except:
                    return render(request, 'signup.html', {
                        'error': 'El usuario ya existe',
                        'form': form
                    })
            else:
                return render(request, 'signup.html', {
                    'error': 'Las contraseñas no coinciden',
                    'form': form
                })
        else:
            return render(request, 'signup.html', {
                #'error': form,
                'form': form
            })
    else:
        form = UsuarioForm()
    
    return render(request, 'signup.html', {'form': form})

@login_required
def principal(request):
    tareas=Task.objects.all()
    #Tareas del usuario que esta logeado
    #tareas = Task.objects.filter(user= request.user)
    return render(request, 'principal.html', {
        'tareas': tareas
    })
    
@login_required
def principal_detail(request,id):
    #task = Task.objects.get(pk= id)
    if request.method == 'GET':
        print("entre")
        task =  get_object_or_404(Task, pk= id)
        form = TaskForm(instance= task)
        return render(request, 'principal_detail.html',{
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=id)
            form = TaskForm(request.POST, instance=task)
            form.save()
            print('guarade')
            return redirect('principal') 
        except ValueError:
            return render(request, 'principal_detail.html',{
             'task': task,
             'form': form,
             'error': 'Error al actualizar',
         })
@login_required
def complete(request,id):
    task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('principal')

@login_required    
def delete(request,id):
    task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        task.delete()        
        return redirect('principal')
    


def signout(request):
    logout(request)
    return redirect('login')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,username= request.POST['username'], password=request.POST['password'])
    if user is None:
        return render(request, 'signin.html',{
            'form': AuthenticationForm,
            'error': "USUARIO O CONTRASEÑA INCORRECTA"
        })
    else:
        login(request, user)
        return redirect('home2')