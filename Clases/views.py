from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Clases.forms import CalificacionForm, InasistenciasForm, Inasistencias, HorarioForm
from Core.models import Calificacion, Horario, inscripcionEstudianteCiclo
from django.shortcuts import render, redirect

# Create your views here.
@login_required
def calificacion_view(request):
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
           form.save()
    else:
        form = CalificacionForm()

    return render(request, 'Calificacion/calificacionForm.html', {'form': form})


# Create your views here.
@login_required
def calificacion_edit(request, id_calificacion):
    espacio = Calificacion.objects.get(id=id_calificacion)
    if request.method == 'GET':
        form = CalificacionForm(instance= espacio)
    else:
        form = CalificacionForm(request.POST, instance= espacio)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/Notas/verCalificacion")
    return render(request, 'Calificacion/calificacionForm.html',{'form':form})


class calificacion_list(ListView):
    model = Calificacion
    template_name = 'Calificacion/verCalificacion.html'
#-------------------------------------------------------------------
@login_required
def inasistencia_view(request):
    if request.method == 'POST':
        form = InasistenciasForm(request.POST)
        if form.is_valid():
           form.save()
    else:
        form = InasistenciasForm()

    return render(request, 'Inasistencia/inasistenciaForm.html', {'form': form})

# Create your views here.
@login_required
def Inasistencia_edit(request, id_inasistencia):
    inasistencia = Inasistencias.objects.get(id=id_inasistencia)
    if request.method == 'GET':
        form = InasistenciasForm(instance= inasistencia)
    else:
        form = InasistenciasForm(request.POST, instance= inasistencia)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/Notas/verInasistencias")
    return render(request, 'Inasistencia/inasistenciaForm.html',{'form':form})


class inasistencia_list(ListView):
    model = Inasistencias
    template_name = 'Inasistencia/verInasistencias.html'
    
@login_required
def crear_horario(request):
    if request.method == "POST":
        # Recupera los datos del formulario
        dia = request.POST["dia"]
        hora = request.POST["hora"]
        cantidad_modulo = int(request.POST["cantidad_modulo"])

        # Crea un nuevo horario
        horario = Horario(
            dia=dia,
            hora=hora,
            cantidad_modulo=cantidad_modulo,
            #division= division,  # Asegúrate de tener esta variable disponible
            #espacioCurricular= espacioCurricular,  # Asegúrate de tener esta variable disponible
            #docente= docente,  # Asegúrate de tener esta variable disponible
        )
        horario.save()

        # Asigna módulos adicionales si es necesario
        horario.asignar_a_modulos(cantidad_modulo)

        # Redirecciona a una página de éxito o a donde lo necesites
        return redirect("ruta_a_pagina_de_exito")
    horarios = Horario.objects.all()
    # Si no es una solicitud POST, muestra el formulario para crear horarios
    return render(request, "Division/crearHorarioDivision.html", {"horario_form": HorarioForm(), "horarios": horarios})


@login_required
def registrarInasistencia(request, idAnio):
    #ACa deberia trer los alumnos de un anio especifico de un ciclo especifico
    estudiantes = inscripcionEstudianteCiclo.objects.all()
    print(estudiantes)
    if request.method == 'POST':
        print(request.POST)
        

    return render(request, 'Cursada/cargarInasistencia.html', {'estudiantes': estudiantes})
    
    # Mostrarlos y registrar los que no estan marcados