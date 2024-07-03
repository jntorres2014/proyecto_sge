import calendar
from itertools import count
import json
from django.db import IntegrityError
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from Clases.forms import CalificacionForm, ConsultaForm, Detalle_HorarioForm, HabilitarInstanciaForm, InasistenciasForm, Inasistencias, InstanciaForm, ReporteForm
from Core.models import Aula, Calificacion, Ciclo, Detalle_Horario, Docente, EspacioCurricular, Estudiante, Horario, InscripcionDocente, Instancia, PlanDeEstudios, Inscripcion,Division
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages
# Create your views here.
from django.shortcuts import render
from .models import Inasistencias
import plotly.graph_objs as go
from django.utils import timezone
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import ExtractYear,ExtractMonth
from django.core.serializers import serialize
from django.db.models import Avg


def crearBoletin(request,id_estudiante):
    ciclo = request.ciclo
    materias = EspacioCurricular.objects.filter(plan_id=ciclo.plan_id)
    calificaciones = Calificacion.objects.filter()
    return materias


@login_required
def inasistencias_por_anio(request):
    inasistencias_por_anio = Inasistencias.objects.annotate(year=ExtractYear('dia')).values('year').annotate(count=Count('id')).order_by('year')

    data = {
        'inasistencias_por_anio': list(inasistencias_por_anio)
    }

    return JsonResponse(data)

def inasistencias_por_mes(request, year):
    print("Entreeeee")
    inasistencias_por_mes = Inasistencias.objects.filter(dia__year=year).annotate(month=ExtractMonth('dia')).values('month').annotate(count=Count('id')).order_by('month')

    data = {
        'inasistencias_por_mes': list(inasistencias_por_mes)
    }

    return JsonResponse(data)



def reporteNotas(request):
    if request.method == 'GET':
        espacio_curricular_id = request.GET.get('espacio_curricular')
        instancia_id = request.GET.get('instancia')
        
        # Obtener las calificaciones basadas en el espacio curricular y la instancia seleccionados
        calificaciones = Calificacion.objects.filter(espacioCurricular_id=espacio_curricular_id, instancia_id=instancia_id)
        
        # Calcular el promedio de notas por ciclo lectivo
        promedios_por_ciclo = calificaciones.values('ciclo').annotate(promedio=Avg('nota'))
        
        # Preparar los datos en un formato JSON para enviar al frontend
        data = []
        for promedio in promedios_por_ciclo:
            ciclo_id = promedio['ciclo']
            promedio_valor = promedio['promedio']
            
            # Obtener el nombre o cualquier otro campo relevante del ciclo si es necesario
            ciclo_nombre = Ciclo.objects.get(id=ciclo_id).nombre
            
            # Agregar el ciclo y su promedio al diccionario
            data.append({'ciclo': ciclo_nombre, 'promedio': promedio_valor})
        
            return JsonResponse(data, safe=False, content_type='application/json')   
    espacios_curriculares = EspacioCurricular.objects.all()
    instancias = Instancia.objects.all()
    return render(request, 'Calificacion/reporteNotas.html', {'espacios_curriculares': espacios_curriculares, 'instancias': instancias})

def reportes_graficos(request):
    inasistencias_por_anio = Inasistencias.objects.annotate(year=ExtractYear('dia')).values('year').annotate(count=Count('id')).order_by('year')
    inasistencias = list(inasistencias_por_anio)
    return render(request, 'Cursada/reportesGraficos.html', {'inasistencias_por_anio': inasistencias})
@login_required
def calificacion_view(request):
    print('**********FORMULARIOOO******')
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        print('**********FORMULARIOOO******')
        print(form)
        if form.is_valid():
           form.save()
    else:
        form = CalificacionForm()

    return render(request, 'Calificacion/calificacionForm.html', {'form': form})

def boletinEstudiante(request, estudiante_id, ciclo_id):
    #Obtengo la inscripcion para poder quedarme con el año que cursa
    inscripcion = Inscripcion.objects.get(estudiante_id = estudiante_id, ciclo_id= ciclo_id)
    instancias = list(Instancia.objects.all())
    print(instancias)
    print("Anio de inscripcion",inscripcion.anio.id)
    #Obtener los espacios curruculares a ese anio de ese plan
    espacios = EspacioCurricular.objects.filter(anio_id= inscripcion.anio.id,plan = PlanDeEstudios.objects.get(id = Ciclo.objects.get(id = ciclo_id).plan.id))
    print("espacios", espacios)
    
  # Obtener todas las instancias únicas para el ciclo dado
    instancias = list(Ciclo.objects.get(pk=ciclo_id).calificacion_set.filter(estudiante_id=estudiante_id).values_list('instancia__nombre', flat=True).distinct())
    print("instancias",instancias)
    # Obtener todas las calificaciones del estudiante para el ciclo dado, agrupadas por materia
    calificaciones = Calificacion.objects.filter(estudiante_id=estudiante_id, ciclo_id=ciclo_id)
    print("Calificaciones",calificaciones)
    # Crear una lista de listas para almacenar las calificaciones

    # Calcular el promedio general del estudiante para el ciclo
    promedio_general = calificaciones.aggregate(promedio_general=Avg('nota'))['promedio_general']

    # Renderizar la plantilla con los datos del boletín y el promedio general
    # Renderizar la plantilla con los datos del boletín y el promedio general
    return render(request, 'Calificacion/boletinEstudiante.html', 
                  {'calificaciones': calificaciones,
                   'espacios': espacios,
                   'promedio':promedio_general,
                   'instancias': instancias
                   })


@login_required
def menuCursada(request):
    fecha_str = str(timezone.now())
    print(fecha_str)
    instanciaDisponible = Instancia.objects.filter(ciclo = request.ciclo,disponible = True)
    fecha_iso = fecha_str.split(" ")[0]  # Obtiene solo la parte de la fecha (AAAA-MM-DD)
    fecha_hoy = datetime.fromisoformat(fecha_iso)
    ciclo = request.ciclo
    inscriptos = Inscripcion.objects.filter(ciclo = ciclo)
    cantInscriptos = inscriptos.count()
    cantDocInsciptos = InscripcionDocente.objects.filter(ciclo = ciclo).count()
    estudiantes_sin_inscripcion = Estudiante.objects.exclude(inscripcion__ciclo=ciclo).count()
    inasistencias_hoy = Inasistencias.objects.filter(dia = fecha_hoy).count()
    if cantInscriptos == 0:
        porcentaje = 0
    else:
        porcentaje = round((inasistencias_hoy / cantInscriptos)*100 ,2)

    print("ACAAAAAAAAA INASISTENCIAS",inasistencias_hoy)
   

    return render(request, 'Cursada/menuCursada.html',{
        'ciclo ': ciclo,
        'cantInscriptos' : cantInscriptos,
        'cantDocInscriptos' : cantDocInsciptos,
        'total' : cantInscriptos + cantDocInsciptos,
        'sinInscripcion' : estudiantes_sin_inscripcion,
        'inasistencias' : inasistencias_hoy,
        'instanciaDisponible' : instanciaDisponible,
        'porcentaje': porcentaje

    })

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

def instancias_list(request):
    instancias = Instancia.objects.filter(ciclo = request.ciclo)
    return render(request, 'Calificacion/instancias.html',{'instancias':instancias})
   
    
@require_POST
@login_required
def eliminarNota(request):
    print("eliminar notaaa")
    nota_id = request.POST.get('nota_id')
    nota = get_object_or_404(Calificacion, id=nota_id)
    nota.delete()
    messages.success(request, 'La nota se eliminó correctamente.')
    return JsonResponse({'success': True})

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
    if not request.user.is_staff:
        return HttpResponseForbidden(render(request, 'Core/403.html'))
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
        resultados = [{'nombre_alumno': falta.estudiante.nombre, 'fecha': falta.dia} for falta in inasistencias]

        return JsonResponse({'resultados': resultados})

    return render(request, 'Cursada/reporte_inasistencia.html')

@login_required
def instancia_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden(render(request, 'Core/403.html'))
    print("entre a instancias")
    if request.method == 'POST':
        print(request.POST)
        form = InstanciaForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('/Clases/verInstancias')
    else:
        form = InstanciaForm()

    return render(request, 'Calificacion/instanciaForm.html', {'form': form})


def inhabilitarInstancia(request, instancia_id):
    instancia = get_object_or_404(Instancia, pk=instancia_id)
    instancia.disponible = False  # Cambiar el estado de disponible
    instancia.save()
    return redirect('/Clases/verInstancias')

@require_POST
def habilitarInstancia(request, instancia_id):
    if not request.user.is_staff:
        return HttpResponseForbidden(render(request, 'Core/403.html'))

    instancia = get_object_or_404(Instancia, pk=instancia_id)
    data = json.loads(request.body)
    fecha_fin = data.get('fecha_fin')

    # Validar si la fecha_fin es válida
    try:
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Formato de fecha incorrecto'}, status=400)

    # Validar si la fecha_fin es menor que la fecha actual
    if fecha_fin < datetime.now().date():
        return JsonResponse({'error': 'La fecha ingresada es menor a la fecha actual'}, status=400)

    # Procesar la habilitación de la instancia
    instancia.disponible = True
    instancia.fecha_inicio = datetime.now().date()
    instancia.fecha_fin = fecha_fin
    instancia.save()

    # Deshabilitar las otras instancias
    otras_instancias = Instancia.objects.exclude(id=instancia_id)
    for otra_instancia in otras_instancias:
        otra_instancia.disponible = False
        otra_instancia.save()

    return JsonResponse({'message': 'Instancia habilitada exitosamente'})

@require_POST
def habilitar_instancia(request, instancia_id):
    if not request.user.is_staff:
        return HttpResponseForbidden(render(request, 'Core/403.html'))
    instancia = get_object_or_404(Instancia, pk=instancia_id)
    fecha_fin = request.POST.get('fecha_fin')
    
    # Convertir la fecha ingresada y la fecha actual a objetos datetime.date
    fecha_fin_date = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    fecha_actual = datetime.today().date()
    
    # Verificar si la fecha ingresada es menor que la fecha actual
    if fecha_fin_date < fecha_actual:
        messages.error(request, 'La fecha ingresada es menor a la fecha actual.')
        return JsonResponse({'error': 'La fecha ingresada es menor a la fecha actual'}, status=400)
    
    instancia.disponible = True
    instancia.fecha_fin = fecha_fin_date
    instancia.save()
    messages.success(request, 'La instancia se habilitó correctamente.')
    return JsonResponse({'message': 'Instancia habilitada exitosamente'})

#*************************************************
def reporte_view(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('Acceso denegado.')
    form = ReporteForm(request.GET or None)
    context = {'form': form}
    return render(request, 'Cursada/reporte.html', context)

def get_reporte_data(request):
    plan_id = request.GET.get('plan')
    ciclo_id = request.GET.get('ciclo')
    instancia_id = request.GET.get('instancia')
    calificaciones = Calificacion.objects.all()
    print("todas las notas",calificaciones)

    if plan_id:
        calificaciones = calificaciones.filter(ciclo__plan_id=plan_id)
        print("notassssss",calificaciones)
    if ciclo_id:
        calificaciones = calificaciones.filter(ciclo_id=ciclo_id)
        print("notassssss Cilooo",calificaciones)
    if instancia_id:
        calificaciones = calificaciones.filter(instancia_id=instancia_id)

    # Agrupar calificaciones por espacio curricular
    promedio_notas = calificaciones.values('espacioCurricular__nombre').annotate(promedio=Avg('nota')).order_by('espacioCurricular__nombre')
    print("ver promedio notas", promedio_notas)
    # Preparar los datos para Chart.js
    labels = [item['espacioCurricular__nombre'] for item in promedio_notas]
    print("ver labels", labels)
    data = [item['promedio'] for item in promedio_notas]

    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Promedio de Notas',
            'data': data,
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1,
        }]
    }
    return JsonResponse(chart_data)

def get_ciclos(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('Acceso denegado.')
    print("Entre a reporte ciclos")
    plan_id = request.GET.get('plan')
    ciclos = Ciclo.objects.filter(plan_id=plan_id).values('id', 'anioCalendario')
    data = {'ciclos': list(ciclos)}
    return JsonResponse(data)

def get_instancias(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('Acceso denegado.')
    ciclo_id = request.GET.get('ciclo')
    print(ciclo_id)
    instancias = Instancia.objects.filter(ciclo_id=ciclo_id).values('id', 'nombre')
    data = {'instancias': list(instancias)}
    return JsonResponse(data)
#**************************************************
# def consultar_faltas(request):
#     if request.method == 'POST' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#         form = ConsultaForm(request.POST)

#         if form.is_valid():
#             fecha_inicio = form.cleaned_data['fecha_inicio']
#             fecha_fin = form.cleaned_data['fecha_fin']
#             estudiante_id = form.cleaned_data['estudiante']

#             consulta_faltas = Q(fecha__range=[fecha_inicio, fecha_fin])
#             if estudiante_id:
#                 consulta_faltas &= Q(alumno_id=estudiante_id)

#             faltas = Inasistencias.objects.filter(consulta_faltas)

#             resultados = [{'nombre_alumno': falta.estudiante.Nombre, 'fecha': falta.dia} for falta in faltas]

#             return JsonResponse({'resultados': resultados})

#     else:
#         form = ConsultaForm()

#     return render(request, 'Cursada/reporte_inasistencia.html', {'form': form})



#     return render(request, 'Cursada/reporte_inasistencia.html')
class inasistencia_list(ListView):
    model = Inasistencias
    template_name = 'Inasistencia/verInasistencias.html'


#************************Horarios************************
    
@login_required
def crear_horario(request, idDivision):
    if not request.user.is_staff:
        return HttpResponseForbidden('Acceso denegado.')

    division = get_object_or_404(Division, id=idDivision)
    horarios = Detalle_Horario.objects.filter(horario__division_id=idDivision)

    if request.method == "POST":
        form = Detalle_HorarioForm(request.POST, division=division)
        if form.is_valid():
            form.save()
            messages.success(request, 'El horario se creó correctamente.')
            return redirect(f"/Clases/crear_horario/{idDivision}/")
        else:
            pass
            #messages.error(request, 'Error al crear el horario. Por favor, corrige los errores indicados.')
    else:
        form = Detalle_HorarioForm(division=division)

    dias = [str(tupla[0]) for tupla in Horario.CHOICES_DIA]
    modulos = [str(tupla[0]) for tupla in Horario.CHOICES_HORA]

    return render(request, "Division/crearHorarioDivision.html", {
        "form": form,
        "horarios": horarios,
        "dias": dias,
        "modulos": modulos,
        "idDivision": division,
    })
from django.shortcuts import render, redirect
@login_required
def eliminarInasistencias(request):
    if not request.user.is_staff:
        return HttpResponseForbidden('Acceso denegado.')
    if request.method == 'POST':
        inasistencias_seleccionadas = request.POST.getlist('inasistencias_seleccionadas')
        Inasistencias.objects.filter(id__in=inasistencias_seleccionadas).delete()
        return redirect('/Core/aniosDePlanActual')
    else:
        return redirect('/Core/aniosDePlanActual')
@login_required

def registrarInasistencia(request, idAnio):
    if not request.user.is_staff:
        return HttpResponseForbidden('Acceso denegado.')
    # ciclo = Ciclo.objects.get(esActual=True)
    ciclo = request.ciclo
    if request.method == "POST":
        print("aca andooooo")
        # Obtener información del formulario
        inasistencias_seleccionadas = request.POST.getlist('inasistencias_seleccionadas')
        if inasistencias_seleccionadas:
            for estudiante_id in inasistencias_seleccionadas:
                falta_key = f'falta_{estudiante_id}'
                falta = request.POST.get(falta_key, False)
                
                justificado_key = f'justificado_{estudiante_id}'
                justificado = request.POST.get(justificado_key, False)
                
                estudiante = Estudiante.objects.get(id=estudiante_id)
                nueva_inasistencia = Inasistencias(ciclo=ciclo, estudiante=estudiante, falta=falta, justificacion=justificado)
                nueva_inasistencia.save()
            
            # Después de guardar las inasistencias, redirigir a la misma página con un parámetro de éxito
            return redirect('/Core/corregirAlumnoInasistencia/'+idAnio, {'success':True,'estudiantes': estudiante})
        else:
            return render(request, 'Cursada/cargarInasistencia.html', {'error': "estudiante"})

    return render(request, 'Cursada/cargarInasistencia.html', {'estudiantes': estudiante})
    
    # Mostrarlos y registrar los que no estan marcados
@login_required
def obtener_aulas(request):
    print("asignar aulas")
    # Lógica para obtener aulas desde la base de datos
    aulas = Division.objects.filter(ciclo= Ciclo.objects.get(esActual = 'True'),anio=3)  # Obtén las aulas desde tu modelo
    return render(request, 'aulas.html', {'aulas': aulas})


@login_required 
def verAulas(request, idAnio, idCiclo):
    if not request.user.is_staff:
        return HttpResponseForbidden('Acceso denegado.')
    ciclo = Ciclo.objects.get(id= idCiclo)
    divisiones = Division.objects.filter(anio_id=idAnio,ciclo=ciclo)
    aulas = Aula.objects.filter(division__in=divisiones)
    estudiantes_inscritos = Inscripcion.objects.filter(anio=idAnio,ciclo = ciclo)
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
    return render(request, 'Division/verEstudianteAula.html', {'aulas': aulas, 
                                                                'estudiantes_aula': estudiantes_aula,
                                                                })            
    
@login_required
def asignar_alumno_a_aula(request, idAnio):
    if not request.user.is_staff:
        return HttpResponseForbidden('Acceso denegado.')
    print("asignar alumno", idAnio)
    ciclo = Ciclo.objects.get(esActual = 'True')
    ciclo=request.ciclo
    divisiones = Division.objects.filter(anio_id=idAnio,ciclo=ciclo)
    estudiantes_inscritos = Inscripcion.objects.filter(anio=idAnio,ciclo = ciclo)
    print("estudiuantes inscriptos",estudiantes_inscritos)
    aulas = Aula.objects.filter(division__in=divisiones)
    print("Estoy en aulaaass",aulas[0].estudiantes.all())
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


def estudiantes_aulas(request, id_division):
    if request.user.is_staff:
        return HttpResponseForbidden(render(request, 'Core/403.html'))

    aula = Aula.objects.get(division_id = id_division)
    horario = Horario.objects.get(division_id = id_division)
    docente = Docente.objects.get(dni = request.user.username)
    print('Docente',docente)
    espacios = Detalle_Horario.objects.filter(docente= docente, horario = horario).values('espacioCurricular').distinct()
    estudiantes = aula.estudiantes.all()
    print("Aulaaaa",aula.division.id,request.user.id)
    print(estudiantes)
    print('Espacioooos estudiantes',espacios)
    instancia = Instancia.objects.get(ciclo = request.ciclo , disponible= True)
    estudiantes_ids = request.GET.getlist(estudiantes)
    calificacion = Calificacion.objects.filter(
            docente_id=docente.id,
            instancia_id=instancia.id,
            estudiante__in=estudiantes,
            ciclo=request.ciclo,
        ).order_by('espacioCurricular')
    
    if request.method == 'GET':
        form = CalificacionForm(espacios= espacios,estudiantes= estudiantes)
    else:
        print("****FORMULARIO****")
        form = CalificacionForm(request.POST)
        if form.is_valid():
            try:
                ciclo = request.ciclo
                docente_id = Docente.objects.get(dni=request.user.username)
                calificacion_obj = form.save(commit=False)
                calificacion_obj.ciclo = ciclo
                calificacion_obj.docente = docente_id
                calificacion_obj.save()
                messages.success(request, 'Calificacion cargada correctamente.')
            except IntegrityError:
                messages.error(request, 'Ya existe una calificación para esta instancia, ciclo y estudiante.') 
                
        else:
            print("El formulariooooo",request.POST)
            messages.error(request, form.errors)

    form = CalificacionForm(espacios= espacios,estudiantes= estudiantes)        
    return render (request, 'Calificacion/verEstudiante2.html',{
        'estudiantes': estudiantes,
        'form': form,
        'espacios': espacios,
        'calificacion': calificacion
    })

    

def obtener_alumnos(request, idEstudiante):
    print("Obteniendo las inscripciones del estudiante")

    # Obtener las inscripciones del estudiante
    alumnos_inscripciones = Inscripcion.objects.filter(estudiante_id=idEstudiante)
    alumno = Estudiante.objects.get(id=alumnos_inscripciones[0].estudiante_id)
    # Diccionario para almacenar la información
    info_alumnos = {}

    for estudiante in alumnos_inscripciones:
        ciclos = Ciclo.objects.filter(id=estudiante.ciclo_id)
        for ciclo in ciclos:
            plan = PlanDeEstudios.objects.get(id=ciclo.plan_id)
            print(plan)
            # Agregar la información al diccionario
            if estudiante.estudiante_id not in info_alumnos:
                info_alumnos[estudiante.estudiante_id] = {
                    'ciclos': [],
                    'inscripciones': [],
                    'planes': []
                }
        
            info_alumnos[estudiante.estudiante_id]['ciclos'].append(ciclo)
            print('Mostrando inscripciones',estudiante.fecha)
            info_alumnos[estudiante.estudiante_id]['inscripciones'].append(estudiante)
            info_alumnos[estudiante.estudiante_id]['planes'].append(plan)
    for estudiante_id, info in info_alumnos.items():
        ciclos_serializables = []
    
    for estudiante_id, info in info_alumnos.items():
        ciclos_serializables = []
        for ciclo in info['ciclos']:
            ciclo_serializable = {
                'id': ciclo.id,
                'nombre': ciclo.anioCalendario,
                # Agregar otros campos necesarios aquí
            }
            ciclos_serializables.append(ciclo_serializable)
        info['ciclos'] = ciclos_serializables

        # Construir un diccionario serializable para cada objeto de tipo PlanDeEstudios
        planes_serializables = []
        for plan in info['planes']:
            plan_serializable = {
                'id': plan.id,
                'nombre': plan.codigo,
                # Agregar otros campos necesarios aquí
            }
            planes_serializables.append(plan_serializable)
        inscripciones_serializables = []
        for inscripcion in info['inscripciones']:
            print('en teoria tiene que estar la inscripcion',inscripcion.fecha)
            inscripcion_serializable = {
                'id': inscripcion.anio.codigo,
                'fecha': inscripcion.fecha
                # Incluye otros campos necesarios aquí
            }
            inscripciones_serializables.append(inscripcion_serializable)   
        info['inscripciones'] = inscripciones_serializables

        info['planes'] = planes_serializables
    print(info_alumnos)
    # Devolver los datos como respuesta JSON
    return JsonResponse(info_alumnos)
    print(alumno.fechaInscripcion,info_alumnos)
    return JsonResponse(info_alumnos)


def actualizar_relacion(request): 
    if not request.user.is_staff:
        return HttpResponseForbidden('Acceso denegado.')
    print("entre actualizar relacion")
    #ciclo_actual = Ciclo.objects.get(esActual=True)
    ciclo_actual = request.ciclo
    divisiones = Division.objects.filter(ciclo=ciclo_actual)
    print(request.method)
    print('vengo por aca')
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        alumno_id = data.get('estudiante_id')
        aula_nombre = data.get('aula_nombre')
        print("recuperados", alumno_id, aula_nombre)
        estudiante = Estudiante.objects.get(dni=alumno_id)
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
    detalles = Detalle_Horario.objects.all()
    print(detalles)
    detalles_json = [{'dia': detalle.dia, 'hora': detalle.hora, 'espacioCurricular': detalle.espacioCurricular.nombre} for detalle in detalles]

    return JsonResponse({'detalles': detalles_json})

@require_POST
def eliminar_detalle_horario(request):
    detalle_id = request.POST.get('detalle_id')
    try:
        detalle = Detalle_Horario.objects.get(id=detalle_id)
        detalle.delete()
        success = True
    except Detalle_Horario.DoesNotExist:
        success = False

    return JsonResponse({'success': success})

@login_required
def autocomplete_estudiantes(request):
    print("estoy aca")
    if 'term' in request.GET:
        qs = Estudiante.objects.filter(nombre__icontains=request.GET.get('term'))
        estudiantes = list(qs.values('id', 'nombre', 'apellido', 'dni'))
        return JsonResponse(estudiantes, safe=False)
    return JsonResponse([], safe=False)

@login_required
def verBoletines(request):
    if request.method == 'GET':
        inscripciones = Inscripcion.objects.filter(ciclo = request.ciclo)
        estudiantes = []
        for inscripcion in inscripciones:
            estudiantes.append(inscripcion.estudiante)
            
        estudiantes = sorted(estudiantes,key=lambda e:e.nombre)
        return render(request, 'Calificacion/verBoletines.html',
                      {'estudiantes':estudiantes})

    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        estudiante = get_object_or_404(Estudiante, id=estudiante_id)
        inscripcion = Inscripcion.objects.get(estudiante = estudiante, ciclo = request.ciclo)
        calificaciones = Calificacion.objects.filter(estudiante=estudiante,ciclo = request.ciclo)
        espacios = EspacioCurricular.objects.filter(plan = request.ciclo.plan, anio= inscripcion.anio)
        instancias = Instancia.objects.filter(ciclo = request.ciclo)
        data = {
            'espacios': [espacio.nombre for espacio in espacios],
            'instancias': [instancia.nombre for instancia in instancias],
            'calificaciones': [
                {
                    'espacio': calificacion.espacioCurricular.nombre,
                    'instancia': calificacion.instancia.nombre,
                    'nota': calificacion.nota
                }
                for calificacion in calificaciones
            ],
            'promedio': calificaciones.aggregate(Avg('nota'))['nota__avg'] if calificaciones else 'No existen notas cargadas'
        }

        return JsonResponse(data)


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


@login_required
def reporte_alumno(request):
     return render(request, 'Cursada/reporte_alumno.html')


def reporte_inasistencias(request):
    # Lógica para manejar las solicitudes del usuario y filtrar los datos
    # Puedes usar los parámetros de la URL o un formulario para recibir los filtros
    
    # Por ejemplo, supongamos que los usuarios pueden filtrar por mes y aula
    mes = request.GET.get('mes')
    aula_id = request.GET.get('aula')
    
    # Filtrar las inasistencias según los filtros seleccionados
    inasistencias = Inasistencias.objects.all()  # Obtener todas las inasistencias inicialmente
    
    if mes:
        inasistencias = inasistencias.filter(dia__month=mes)
        print(inasistencias)
    
    if aula_id:
        inasistencias = inasistencias.filter(aula_id=aula_id)
    
    # Obtener los datos necesarios para el gráfico
    # Esto dependerá de cómo estructures tus datos y de la biblioteca de gráficos que elijas

    # Generar el gráfico con Plotly
    # Aquí hay un ejemplo básico, debes adaptarlo a tus necesidades específicas
    grafico = go.Figure(data=[go.Bar(x=['Categoria1', 'Categoria2'], y=[10, 20])])

    # Convertir el gráfico a HTML para mostrarlo en el template
    grafico_html = grafico.to_html(full_html=False, default_height=500, default_width=700)

    return render(request, 'Cursada/graficoInasistencia.html', {'grafico_html': grafico_html})

def reporte_inasistencias_por_aula(request):
    aulas = Aula.objects.all()
    print(aulas)
    data = []
    for aula in aulas:
        inasistencias = Inasistencias.objects.filter(estudiante__aula=aula)
        print(inasistencias)
        data.append({
            'aula': aula.division,
            'inasistencias': inasistencias.count()
        })
    return render(request, 'Cursada/inasistencia.html', {'data': data})

def consultar_faltas(request):
    if request.method == 'POST':
        fecha_consulta = request.POST.get('fecha_consulta')
        faltas = Inasistencias.objects.filter(fecha=fecha_consulta)
        return render(request, 'faltas.html', {'faltas': faltas})
    return render(request, 'Cursada/consulta_faltas.html')



@login_required
def horarioDocente(request,idDocente):
    print("*******entre aca**** ",idDocente,request.method)
    #ciclo_actual = Ciclo.objects.get(isActual = True)
    ciclo_actual = request.ciclo
    docente = Docente.objects.get(id= idDocente)
    horarios = Horario.objects.filter(division__ciclo=ciclo_actual, docente=docente)
    print("hasta aca va,oms?")
   # El formulario no es válido, imprimir los mensajes de error
    print("Horarios",horarios)
    dias = [str(tupla[0]) for tupla in Horario.CHOICES_DIA]
    modulos = [str(tupla[0]) for tupla in Horario.CHOICES_HORA]
    print(dias,modulos)
    
    return render(request, "    html", {"horarios": horarios,
                                                                  "dias": dias,
                                                                  'modulos': modulos,})