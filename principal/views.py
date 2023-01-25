from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.


def home(request):
    return render(request, 'home.html')

def inscripciones(request):
       return render(request, 'inscripciones.html')

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
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
        print('Enviando formulario')
    else:
        print(request.POST['password1'], request.POST['password2'])
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('principal')
                #return HttpResponse('Usuario guardado correctamente')
            except:
                return render(request, 'signup.html', {
                    'error': 'El usuario ya existe',
                    'form': UserCreationForm})
        return render(request, 'signup.html', {
                    'error': 'Contraseña no coincide',
                    'form': UserCreationForm})
        #return HttpResponse('Contraseña no coincide')

        # print(request.POST)
        # print('obteniendo datos')
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
        return redirect('home')