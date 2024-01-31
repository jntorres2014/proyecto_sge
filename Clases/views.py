import json
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Clases.forms import CalificacionForm, Detalle_HorarioForm, InasistenciasForm, Inasistencias
from Core.models import Aula, Calificacion, Ciclo, Detalle_Horario, Estudiante, Horario, inscripcionEstudianteCiclo,Division
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q
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
            horarios_list = [{'id': horario.id, 'nombre': horario.espacioCurricular.nombre} for horario in horarios]
            datos_json = {'horarios': horarios_list}

            # Devolver la respuesta como JSON
            return JsonResponse(datos_json)
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

from django.db.models import Q

def asignar_alumno_a_aula(request, idAnio):
    print("asignar alumno", idAnio)

    divisiones = Division.objects.filter(anio_id=idAnio)
    #estudiantes_inscritos = inscripcionEstudianteCiclo.objects.filter(anio=idAnio)

    # Verificar si las aulas existen para cada división
    for division in divisiones:
        aulas_existen = Aula.objects.filter(division=division).exists()
        if not aulas_existen:
            Aula.objects.create(division=division)
    print("aulas creadas")

    aulas = Aula.objects.filter(division__in=divisiones)
    # Obtener estudiantes que no están en ninguna de las aulas indicadas
    estudiantes_no_en_aula = Estudiante.objects.filter(~Q(aulas__in=aulas))
    print("estudiantes sin aulas", estudiantes_no_en_aula.Nombre)
    # Obtener estudiantes inscritos que no están en aulas
    estudiantes_inscritos_no_en_aula = estudiantes_no_en_aula.filter(
        inscripcionestudianteciclo__anio=idAnio)
    estudiantes_inscritos_no_en_aula = estudiantes_no_en_aula.filter(
    print("otros estudiantes",)
    # Obtener las aulas después de verificar o crear
    aulas = Aula.objects.filter(division__in=divisiones)
    estudiantes_aula = []

    # Obtener estudiantes que no están en ninguna aula


    return render(request, 'Division/asignar_alumnno_aula.html', {'aulas': aulas, 'estudiantes':estudiantes_inscritos_no_en_aula,
                                                                'alumnos_aula': estudiantes_aula})

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
        estudiante= Estudiante.objects.get(Dni = alumno_id)
        print("estudiantes",estudiante)
        aula = Aula.objects.get(id=int(aula_nombre))
        estudiante= Estudiante.objects.get(Dni=alumno_id)
        print("estudianteeee",estudiante)
    
        # Obtener el aula específica
        aula = Aula.objects.get(id=int(aula_nombre))
        #print("aula,aula",aula.estudiantes)
        # Asignar al estudiante al aula
        
        aula.estudiantes.add(estudiante)
        print("Estudiantes de aulaa*****",aula.estudiantes.all())
        #aula = Aula.objects.create(division_id=int(aula_nombre),estudiante=estudiante)
        #aula = Aula.objects.get(id= int(aula_nombre))
        #aula.estudiante = estudiante
        aula.save()
        mensaje_exito = f'Se cargó el alumno {alumno_id} al aula {aula_nombre}'
        contenido_html = "<h1>Mi HTML</h1><p>Este es un párrafo.</p>"

        # Serializar el contenido HTML
        datos_json = {'contenido_html': contenido_html}
        return JsonResponse({'success': True, 
                             'message': mensaje_exito,
                             'datos': datos_json})
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

@require_POST
def eliminarAlumno(request):
    detalle_id = request.POST.get('detalle_id')
    print("****ENTREEE", detalle_id)
    
    try:
        detalle = Aula.objects.get(estudiante_id=detalle_id)
        detalle.delete()
        success = True
    except Aula.DoesNotExist:
        success = False

    return JsonResponse({'success': success})