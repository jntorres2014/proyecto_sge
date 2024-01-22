from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Clases.forms import CalificacionForm, InasistenciasForm, Inasistencias, HorarioForm
from Core.models import Aula, Calificacion, Ciclo, Horario, inscripcionEstudianteCiclo,Division
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

def obtener_aulas(request):
    # Lógica para obtener aulas desde la base de datos
    aulas = Division.objects.filter(ciclo= Ciclo.objects.get(esActual = 'True'))  # Obtén las aulas desde tu modelo
    return render(request, 'aulas.html', {'aulas': aulas})

def asignar_alumno_a_aula(request):
    aulas = Division.objects.filter(ciclo= Ciclo.objects.get(esActual = 'True'))
    #estudiantes_inscritos = inscripcionEstudianteCiclo.objects.filter(ciclo= ciclo_actual)  # Define ciclo_actual según tu lógica
    estudiantes_inscritos = inscripcionEstudianteCiclo.objects.all()  # Obtén los alumnos desde tu modelo
    print(estudiantes_inscritos[1].id)
    print(aulas)
    return render(request, 'Division/asignar_alumnno_aula.html', {'aulas': aulas, 'estudiantes': estudiantes_inscritos})

def obtener_alumnos(request):
    # Lógica para obtener alumnos desde la base de datos
    alumnos = inscripcionEstudianteCiclo.objects.all()  # Obtén los alumnos desde tu modelo
    return render(request, 'alumnos.html', {'alumnos': alumnos})

# def asignar_alumno_a_aula(request): 
#     ciclo_actual = Ciclo.objects.get(esActual=True)
#     divisiones = Division.objects.filter(ciclo= ciclo_actual)
#     # Filtra los estudiantes que no están inscritos en el ciclo actual
#     # alumnos_sin_aula= inscripcionEstudianteCiclo.objects.exclude(
#     #         id__in = Aula.objects.filter(
#     #             division= divisiones
#     #         ).values('estudiante')
#     #         )
#     print('vengo por aca')
#     if request.method == 'POST':
#         alumno_id = request.POST.get('alumno_id')
#         aula_id = request.POST.get('aula_id')
        
#         # Lógica para asignar alumno a aula en la base de datos
#         # ...

#         return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'success': False})