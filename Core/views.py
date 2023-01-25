from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from Core import forms
from .models import PlanDeEstudios, Localidad, Docente,Estudiante, EspacioCurricular
from django.views.generic import ListView,TemplateView




##################################################################

def localidad_view(request):
    if request.method == 'POST':
        form = forms.LocalidadForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/verLocalidad")
    else:
        form = forms.LocalidadForm()
    return render(request, 'Core/LocalidadForm.html', {'form': form})

class localidad_list(ListView):
    model = Localidad
    template_name = 'Core/verLocalidad.html'

def localidad_edit(request, id_localidad):
    localidad = Localidad.objects.get(id=id_localidad)
    if request.method == 'GET':
        form = forms.LocalidadForm(instance= localidad)
    else:
        form = forms.LocalidadForm(request.POST, instance= localidad)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/verLocalidad")
    return render(request, 'Core/LocalidadForm.html',{'form': form})

######################ESTUDIANTE DOCENTE##################################################

def Estudiante_view(request):
    if request.method == 'POST':
        form = forms.EstudianteForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            #estudiante = form.save(commit=False)
            #estudiante.fechaInscripcion = form.fechaInscripcion
            #estudiante.save()
            return HttpResponseRedirect("/Core/verEstudiantes")
    else:
        form = forms.EstudianteForm()

    return render(request, 'Core/Persona/EstudianteForm.html', {'form': form})


def docente_view(request):
    if request.method == 'POST':
        form = forms.DocenteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/verDocentes")
    else:
        form = forms.DocenteForm()
    return render(request, 'Core/Persona/DocenteForm.html', {'form': form})


class docente_list(ListView):
    model = Docente
    template_name = 'Core/Persona/verDocente.html'

def docente_edit(request, id_docente):
    docente = Docente.objects.get(id=id_docente)
    if request.method == 'GET':
        form = forms.DocenteForm(instance= docente)
    else:
        form = forms.DocenteForm(request.POST, instance= docente)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/verDocentes")
    return render(request, 'Core/Persona/DocenteForm.html',{'form': form})



def estudiante_edit(request, id_estudiante):
    estudiante = Estudiante.objects.get(id=id_estudiante)
    if request.method == 'GET':
        form = forms.EstudianteForm(instance= estudiante)
    else:
        form = forms.EstudianteForm(request.POST, instance= estudiante)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/Core/verEstudiantes")
    return render(request, 'Core/Persona/EstudianteForm.html',{'form':form})


class estudiante_list(ListView):
    model = Estudiante
    template_name = 'Core/Persona/verEstudiante.html'



################PLAN##################################


def plan_de_estudios_view(request):
    if request.method == 'POST':
        form = forms.PlanDeEstudiosForm(request.POST)
        if form.is_valid():
           plan= form.save()
           #plan.crear_anios_plan(plan)
           return HttpResponseRedirect("verPlan")
    else:
        form = forms.PlanDeEstudiosForm()
    return render(request, 'Core/Plan/PlanDeEstudios.html', {'form': form})

    
def plan_list(request):
    planes=PlanDeEstudios.objects.order_by('id')
    print(planes)
    return render(request, 'Core/Plan/verPlan.html', {
        'planes': planes,
    })    


def plan_edit(request, id_plan):
    plan = PlanDeEstudios.objects.get(id=id_plan)
    if request.method == 'GET':
        form = forms.PlanDeEstudiosForm(instance=plan)
    else:
        form = forms.PlanDeEstudiosForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/verPlan")
    return render(request, 'Core/Plan/PlanDeEstudios.html',{'form':form})

def Espacio_view(request, id_plan):
    if request.method == 'POST':
        form = forms.EspacioCurricularForm(request.POST, id_plan=id_plan)
        if form.is_valid():
            form.save()
    else:
        form = forms.EspacioCurricularForm(id_plan=id_plan)
    return render(request, 'Core/EspacioCurricular/EspaciosCurricularesForm.html', {
        'form': form,
        'idPlan': id_plan,})


def espacio_edit(request, id_espacio):
    espacio = EspacioCurricular.objects.get(id=id_espacio)
    if request.method == 'GET':
        form = forms.EspacioCurricularEditForm(instance= espacio)
    else:
        form = forms.EspacioCurricularEditForm(request.POST, instance= espacio)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/verEspacios")
    return render(request, 'Core/EspacioCurricular/EspaciosCurricularesForm.html',{'form':form})


class Espacio_list(ListView):
    model = EspacioCurricular
    template_name = 'Core/EspacioCurricular/verEspacios.html'

def cargar_espacios(request):
    anioPlan = request.GET.get('anio')
    espacios = EspacioCurricular.objects.filter(anio_id=anioPlan)
    print(anioPlan,espacios)
    return render(request, 'Cursada/opciones_espacios.html', {'espacios': espacios})