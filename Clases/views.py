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

@login_required
def consultar_faltas(request):
    print('Methodo',request.method)
    if request.method == 'POST' :
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        estudiante_id = request.POST.get('estudiante_id')  # Nuevo campo para el estudiante
        print("HASTA ACA VAMOOOOS*****")
        if not fecha_inicio and fecha_fin:
            # Si fecha_inicio está vacía pero fecha_fin tiene valor, establece fecha_inicio igual a fecha_fin
            fecha_inicio = fecha_fin
        elif fecha_inicio and not fecha_fin:
            # Si fecha_fin está vacía pero fecha_inicio tiene valor, establece fecha_fin igual a fecha_inicio
            fecha_fin = fecha_inicio
        # Construir consulta para faltas según fecha y estudiante
        consulta_faltas = Q(dia__range=[fecha_inicio, fecha_fin])
        if estudiante_id:
            consulta_faltas &= Q(estudiante_id=estudiante_id)

        # Realizar la consulta de faltas
        inasistencias = Inasistencias.objects.filter(consulta_faltas)

        # Serializar los resultados si es necesario
        resultados = [{'nombre_alumno': falta.estudiante.Nombre, 'fecha': falta.dia} for falta in inasistencias]

        return JsonResponse({'resultados': resultados})




    return render(request, 'Cursada/reporte_inasistencia.html')
class inasistencia_list(ListView):
    model = Inasistencias
    template_name = 'Inasistencia/verInasistencias.html'


#************************Horarios************************
    
@login_required
def crear_horario(request,idDivision):
    print("*******entre aca**** ",idDivision)

    horarios = Detalle_Horario.objects.filter(horario = Horario.objects.get(division_id=idDivision))
    if request.method == "POST":
        print("******Entre al post******")
        print("requesst",request.POST)
        division = Division.objects.get(id=idDivision)
        form = Detalle_HorarioForm(request.POST, division=division)
        print("El formulario",form)
        if form.is_valid():
            print("Era valido")
            form.save()
        return redirect("/Clases/crear_horario/" + idDivision)
    print("Horarios",horarios)
    form = Detalle_HorarioForm(division = Division.objects.get(id=idDivision))
    dias = [str(tupla[0]) for tupla in Horario.CHOICES_DIA]
    modulos = [str(tupla[0]) for tupla in Horario.CHOICES_HORA]
    print(dias,modulos)
    
    return render(request, "Division/crearHorarioDivision.html", {"form": form, 
                                                                  "horarios": horarios,
                                                                  "dias": dias,
                                                                  'modulos': modulos,
                                                                  'idDivision':idDivision})


@login_required
def registrarInasistencia(request, idAnio):
    #ACa deberia trer los alumnos de un anio especifico de un ciclo especifico
    if request.method == "POST":
        print("entre al post")
        # Obtener información del formulario
        inasistencias_seleccionadas = request.POST.getlist('inasistencias_seleccionadas')
        print(inasistencias_seleccionadas)
        for estudiante_id in inasistencias_seleccionadas:
            # Verificar si la falta está marcada
            falta_key = f'falta_{estudiante_id}'
            falta = request.POST.get(falta_key, False)
            
            # Verificar si el justificado está marcado
            justificado_key = f'justificado_{estudiante_id}'
            justificado = request.POST.get(justificado_key, False)
            estudiante = Estudiante.objects.get(id=estudiante_id)
            nueva_inasistencia = Inasistencias(estudiante=estudiante, falta=falta, justificacion=justificado)
            nueva_inasistencia.save()
           #Inasistencias.create()
        

    return render(request, 'Cursada/cargarInasistencia.html', {'estudiantes': estudiante})
    
    # Mostrarlos y registrar los que no estan marcados
@login_required
def obtener_aulas(request):
    print("asignar aulas")
    # Lógica para obtener aulas desde la base de datos
    aulas = Division.objects.filter(ciclo= Ciclo.objects.get(esActual = 'True'),anio=3)  # Obtén las aulas desde tu modelo
    return render(request, 'aulas.html', {'aulas': aulas})

from django.db.models import Q
@login_required
def asignar_alumno_a_aula(request, idAnio):
    print("asignar alumno", idAnio)
    ciclo = Ciclo.objects.get(esActual = 'True')
    divisiones = Division.objects.filter(anio_id=idAnio,ciclo=ciclo)
    estudiantes_inscritos = inscripcionEstudianteCiclo.objects.filter(anio=idAnio,ciclo = ciclo)
    print("estudiuantes inscriptos",estudiantes_inscritos)
    # Verificar si las aulas existen para cada división
    for division in divisiones:
        aulas_existen = Aula.objects.filter(division=division).exists()
        if not aulas_existen:
            Aula.objects.create(division=division)

    # Obtener las aulas después de verificar o crear
    aulas = Aula.objects.filter(division__in=divisiones)

    estudiantes_aula = {}  # Cambiaremos a un diccionario para asociar estudiantes con aulas
    for aula in aulas:
        estudiantes_aula[aula.id] = aula.estudiantes.all()
        print(aula.estudiantes.all())
    estudiantes_no_en_aula = []
    ids_estudiantes_aula = [estudiante.id for aula_estudiantes in estudiantes_aula.values() for estudiante in aula_estudiantes]

    print("Estudiates e aulas",ids_estudiantes_aula)
    # Obtener los IDs de los estudiantes en aulas
    print((ids_estudiantes_aula))
    for estudiante in estudiantes_inscritos:
        print("id estudiante*****",estudiante.estudiante.id,ids_estudiantes_aula)
        if estudiante.estudiante.id not in ids_estudiantes_aula:
            estudiantes_no_en_aula.append(estudiante)

    # Obtener estudiantes que no están en ninguna aula
 #   estudiantes_no_en_aula = estudiantes_inscritos.exclude(id__in=ids_estudiantes_aula)
    print("no en aula", estudiantes_no_en_aula)

    return render(request, 'Division/asignar_alumnno_aula.html', {'aulas': aulas, 
                                                                'estudiantes': estudiantes_no_en_aula,
                                                                'estudiantes_aula': estudiantes_aula,
                                                                'estudiantes_no_en_aula': estudiantes_no_en_aula})

@login_required
def obtener_alumnos(request):
    print("obtener alumno")
    # Lógica para obtener alumnos desde la base de datos
    alumnos = inscripcionEstudianteCiclo.objects.all()  # Obtén los alumnos desde tu modelo
    return render(request, 'alumnos.html', {'alumnos': alumnos})


def actualizar_relacion(request): 
    print("entre actualizar relacion")
    ciclo_actual = Ciclo.objects.get(esActual=True)
    divisiones = Division.objects.filter(ciclo=ciclo_actual)
    print(request.method)
    print('vengo por aca')

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        alumno_id = data.get('estudiante_id')
        aula_nombre = data.get('aula_nombre')
        print("recuperados", alumno_id, aula_nombre)
        estudiante = Estudiante.objects.get(Dni=alumno_id)
        print("estudiantes", estudiante)

        # Obtener el aula específica
        aula_id = int(aula_nombre)
        aula = Aula.objects.get(id=aula_id)
        print("Estudiantes de aulaa*****", aula.estudiantes.all())

        # Asignar al estudiante al aula
        aula.estudiantes.add(estudiante)
        print("Estudiantes de aulaa*****", aula.estudiantes.all())

        mensaje_exito = f'Se cargó el alumno {alumno_id} al aula {aula_nombre}'

        contenido_html = "<h1>Mi HTML</h1><p>Este es un párrafo.</p>"

        # Serializar el contenido HTML
        datos_json = {'contenido_html': contenido_html}
        return JsonResponse({'success': True, 
                             'message': mensaje_exito,
                             'datos': datos_json})
    else:
        return JsonResponse({'success': False})    
@login_required
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
    aula_id = request.POST.get('aula_id')
    estudiante_id = request.POST.get('estudiante_id')

    try:
        # Encuentra el aula por su ID
        aula = Aula.objects.get(id=aula_id)
        
        # Elimina al estudiante del aula
        aula.estudiantes.remove(estudiante_id)
        success = True
    except Aula.DoesNotExist:
        success = False
    except Estudiante.DoesNotExist:
        success = False

    return JsonResponse({'success': success})