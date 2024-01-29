import json
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Clases.forms import CalificacionForm, Detalle_HorarioForm, InasistenciasForm, Inasistencias
from Core.models import Aula, Calificacion, Ciclo, Detalle_Horario, Horario, inscripcionEstudianteCiclo,Division
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
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
    print("*******entre aca**** ")
    if request.method == "POST":
        print("Entre al post")
        form = Detalle_HorarioForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/Clases/altaHorario")
    if request.method =='GET':
        data = request.GET.get('division_id')
        print("aca vamoooooos",data)
        if data is None:
            print("entr none")
            horarios = Detalle_Horario.objects.filter(horario = Horario.objects.get(id=1))
            print(horarios)
        else:
            division = Division.objects.get(id=data)
            print("division",division)
            horarios = Detalle_Horario.objects.filter(horario = Horario.objects.get(division=division)) 
            print(horarios)
            return JsonResponse({'success': True, 'message': "mensaje_exito"})
    #horarios = Detalle_Horario.objects.filter(horario = Horario.objects.get(id=1))
    #print("aca estoy",horarios[0].hora)
    print("Horarios",horarios)
    form = Detalle_HorarioForm()
    dias = [str(tupla[0]) for tupla in Horario.CHOICES_DIA]
    modulos = [str(tupla[0]) for tupla in Horario.CHOICES_HORA]
    print(dias,modulos)
    
    return render(request, "Division/crearHorarioDivision.html", {"form": form, 
                                                                  "horarios": horarios,
                                                                  "dias": dias,
                                                                  'modulos': modulos})


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
    print("asignar aulas")
    # Lógica para obtener aulas desde la base de datos
    aulas = Division.objects.filter(ciclo= Ciclo.objects.get(esActual = 'True'),anio=3)  # Obtén las aulas desde tu modelo
    return render(request, 'aulas.html', {'aulas': aulas})

def asignar_alumno_a_aula(request):
    print("asignar alumno")
    aulas = Division.objects.filter(anio_id=1)
    #estudiantes_inscritos = inscripcionEstudianteCiclo.objects.filter(ciclo= ciclo_actual)  # Define ciclo_actual según tu lógica
    estudiantes_inscritos = inscripcionEstudianteCiclo.objects.all()  # Obtén los alumnos desde tu modelo
    #print(estudiantes_inscritos[1].id)
    print(aulas)
    return render(request, 'Division/asignar_alumnno_aula.html', {'aulas': aulas, 'estudiantes': estudiantes_inscritos})

def obtener_alumnos(request):
    print("obtener alumno")
    # Lógica para obtener alumnos desde la base de datos
    alumnos = inscripcionEstudianteCiclo.objects.all()  # Obtén los alumnos desde tu modelo
    return render(request, 'alumnos.html', {'alumnos': alumnos})


def actualizar_relacion(request): 
    print("entre actualizar relacion")
    ciclo_actual = Ciclo.objects.get(esActual=True)
    divisiones = Division.objects.filter(ciclo= ciclo_actual)
    print(request.method)
    print('vengo por aca')
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        alumno_id = data.get('estudiante_id')
        aula_nombre = data.get('aula_nombre')  # Cambié aula_id a aula_nombre
        print("recuperados" , alumno_id, aula_nombre)
        
        # Lógica para asignar alumno a aula en la base de datos
        # ...
        mensaje_exito = f'Se cargó el alumno {alumno_id} al aula {aula_nombre}'

        return JsonResponse({'success': True, 'message': mensaje_exito})
    else:
        return JsonResponse({'success': False})
    

def obtenerHorarios(request):
    print("entre")
    # data = json.loads(request.body.decode('utf-8'))
    # print(data)
    # horario_id = data.get('division_id')
    # print(horario_id)
    #horario = get_object_or_404(Horario, id=horario_id)
    detalles = Detalle_Horario.objects.all()
    print(detalles)
    detalles_json = [{'dia': detalle.dia, 'hora': detalle.hora, 'espacioCurricular': detalle.espacioCurricular.nombre} for detalle in detalles]

    return JsonResponse({'detalles': detalles_json})

@require_POST
def eliminar_detalle_horario(request):
    detalle_id = request.POST.get('detalle_id')
    print("****ENTREEE", detalle_id)
    
    try:
        detalle = Detalle_Horario.objects.get(id=detalle_id)
        detalle.delete()
        success = True
    except Detalle_Horario.DoesNotExist:
        success = False

    return JsonResponse({'success': success})