from datetime import timezone
from io import BytesIO
from django.utils import timezone
import string
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from Clases.models import Inasistencias
from Core import forms
from django.urls import reverse
from Core.resource import LocalidadResource
from .models import Aula, PlanDeEstudios, Localidad, Docente,Estudiante,EspacioCurricular, AnioPlan, Ciclo, Persona,Inscripcion, Division
from django.views.generic import ListView,TemplateView
from django.db.models import Q
from tablib import Dataset 
from django.contrib import messages
from tablib import Dataset
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Estudiante, Inscripcion
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import styles,colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


from dal import autocomplete

class MateriaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        idDiv = self.forwarded.get('horario')
        division = Division.objects.get(id = idDiv)
        anio = AnioPlan.objects.get(id = division.anio_id)
        print(anio)
        if anio:
            qs = EspacioCurricular.objects.filter(anio = anio)
        else:
            qs = EspacioCurricular.objects.all()
        print(qs)

        if self.q:
            qs = qs.filter( Q(nombre__icontains=self.q) |    
                Q(codigo__icontains=self.q) )           
        return qs



class LocalidadAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Localidad.objects.all()
        print(qs)
        if self.q:
            qs = qs.filter( Q(nombre__icontains=self.q) |    
                Q(codigoPostal__icontains=self.q) )           
        return qs
class EstudianteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        print('ENTRE A AUTOCOMPLETE******')
        ciclo_actual = Ciclo.objects.get(esActual=True)
        # Filtra los estudiantes que no están inscritos en el ciclo actual
        qs = Estudiante.objects.exclude(
            id__in=Inscripcion.objects.filter(
                ciclo=ciclo_actual
            ).values('estudiante')
            )
        #qs = Estudiante.objects.all()
        print("Entreee",qs)
        if self.q:
            qs = qs.filter( Q(Nombre__icontains=self.q) |    
                Q(apellido__icontains=self.q) |       
                Q(dni__icontains=self.q))           
        return qs
    


##################################################################
def importar(request):
    print("llegue a importar")
    result = None  # Inicializa result a None
    localidades = Localidad.objects.all()
    print(localidades)

    if request.method == 'POST':
        localidad_resource = LocalidadResource()
        dataset = Dataset()
        print(dataset)
        nuevas_localidades = request.FILES['xlsfile']
        print(nuevas_localidades)
        imported_data = dataset.load(nuevas_localidades.read())
        try:
            result = localidad_resource.import_data(dataset, dry_run=True)
            
            if not result.has_errors():
                result = localidad_resource.import_data(dataset, dry_run=False)
                messages.success(request, 'La importación se realizó correctamente.')
            else:
                messages.error(request, 'Error durante la importación. Verifica el formato del archivo.')

        except Exception as e:
            messages.error(request, f'Error durante la importación: {str(e)}')

        print(imported_data.headers)  # Imprime los nombres de columna
        print(imported_data.dict)     # Imprime los datos del archivo


    print("Result:", result)

    return render(request, 'Core/importar.html', {'result': result})
##################################################################
@login_required
def localidadView(request):
    if request.method == 'POST':
        form = forms.LocalidadForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/verLocalidad")
    else:
        form = forms.LocalidadForm()
    return render(request, 'Core/LocalidadForm.html', {'form': form})

class localidadList(ListView):
    model = Localidad
    template_name = 'Core/verLocalidad.html'
@login_required
def localidadEdit(request, id_localidad):
    localidad = Localidad.objects.get(id=id_localidad)
    if request.method == 'GET':
        form = forms.LocalidadForm(instance= localidad)
    else:
        form = forms.LocalidadForm(request.POST, instance= localidad)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/localidad/ver")
    return render(request, 'Core/LocalidadForm.html',{'form': form})

######################ESTUDIANTE DOCENTE##################################################
@login_required
def estudianteView(request):
    if request.method == 'POST':
        form = forms.EstudianteForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return HttpResponseRedirect("/Core/estudiante/ver")
    else:
        form = forms.EstudianteForm()

    return render(request, 'Core/Persona/EstudianteForm.html', {'form': form})

@login_required
def docenteView(request):
    if request.method == 'POST':
        form = forms.DocenteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/docente/ver")
    else:
        form = forms.DocenteForm()
    return render(request, 'Core/Persona/DocenteForm.html', {'form': form})


class docenteList(ListView):
    model = Docente
    template_name = 'Core/Persona/docente/ver.html'
@login_required
def docenteEdit(request, id_docente):
    docente = Docente.objects.get(id=id_docente)
    if request.method == 'GET':
        form = forms.DocenteForm(instance= docente)
    else:
        form = forms.DocenteForm(request.POST, instance= docente)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/docente/ver")
    return render(request, 'Core/Persona/DocenteForm.html',{'form': form})


@login_required
def eliminarEstudiante(request, id_estudiante):
    try:
        estudiante = Estudiante.objects.get(id=id_estudiante)
        estudiante.delete()
        messages.success(request, 'El estudiante se eliminó correctamente.')
    except Estudiante.DoesNotExist:
        messages.error(request, 'No se encontró el estudiante que intentas eliminar.')
    
    return HttpResponseRedirect("/Core/estudiante/ver")


@login_required
def eliminarInscripcion(request, id_estudiante):
    try:
        inscripcion = Inscripcion.objects.get(estudiante_id=id_estudiante)
        inscripcion.delete()
        messages.success(request, 'El estudiante se eliminó correctamente.')
    except Estudiante.DoesNotExist:
        messages.error(request, 'No se encontró el estudiante que intentas eliminar.')
    
    return HttpResponseRedirect("/Core/estudiante/inscripcion",
                                'correcto', 'Se elimino la inscripcion del alumno')

@login_required
def estudianteEdit(request, id_estudiante):
    estudiante = Estudiante.objects.get(id=id_estudiante)
    if request.method == 'GET':
        form = forms.EstudianteForm(instance= estudiante)
    else:
        form = forms.EstudianteForm(request.POST, instance= estudiante)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect("/Core/estudiante/ver")
    return render(request, 'Core/Persona/EstudianteForm.html',{'form':form})


class estudianteList(ListView):
    model = Estudiante
    template_name = 'Core/Persona/verEstudiante.html'



################PLAN##################################

@login_required
def planDeEstudiosView(request):
    if request.method == 'POST':
        form = forms.PlanDeEstudiosForm(request.POST)
        if form.is_valid():
           plan= form.save()
           plan.crear_anios_plan(plan)
           return HttpResponseRedirect("plan/ver")
    else:
        form = forms.PlanDeEstudiosForm()
    return render(request, 'Core/Plan/PlanDeEstudios.html', {'form': form})

@login_required    
def planList(request):
    planes=PlanDeEstudios.objects.all().order_by('-esActual')
    print(planes)
    return render(request, 'Core/Plan/verPlan.html', {
        'planes': planes,
    })    

@login_required    
def planDetalle(request,id_plan):

    plan=PlanDeEstudios.objects.get(id = id_plan)
    print(type(plan.cantidadAnios))
    espaciosCurriculares = EspacioCurricular.objects.filter(plan = plan).order_by('anio')
    return render(request, 'Core/Plan/verDetallePlan.html', {
        'plan': plan,
        'espaciosCurriculares' : espaciosCurriculares
    })    

@login_required
def planEdit(request, id_plan):
    plan = PlanDeEstudios.objects.get(id=id_plan)
    if request.method == 'GET':
        form = forms.PlanDeEstudiosEditForm(instance=plan)
    else:
        form = forms.PlanDeEstudiosEditForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/plan/ver")
    return render(request, 'Core/Plan/PlanDeEstudios.html',{'form':form})

def cambiarActual(request, id_plan):
    # Llama al método cambiar_actual de la clase PlanDeEstudios
    PlanDeEstudios.cambiar_actual(request, id_plan)

    # Redirige a la página deseada después de realizar el cambio
    return HttpResponseRedirect("/Core/plan/ver")
#########################################################################

@login_required
def espacioView(request,id):
    #id = 1
    print(id)
    plan = PlanDeEstudios.objects.get(id=id)
    
    espacios = EspacioCurricular.objects.filter(plan = plan)
    if request.method == 'POST':
        form = forms.EspacioCurricularForm(request.POST, id_plan=id)
        if form.is_valid():
            print("guardando datoss")
            form.save()
            espacios = EspacioCurricular.objects.filter(plan = plan)
            #return HttpResponseRedirect("/Core/EspacioCurricular/EspaciosCurricularesForm.html")
    else:
        form = forms.EspacioCurricularForm(id_plan=id)
    
    print("retornando formiulariox")
    return render(request, 'Core/EspacioCurricular/EspaciosCurricularesForm.html', {
        'form': form,
        'plan': plan,
        'espacios': espacios})


@login_required
def espacioEliminar(request, id_espacio):
    try:
        espacio = EspacioCurricular.objects.get(id=id_espacio)
        espacio.delete()
        messages.success(request, 'El espacio curricular se eliminó correctamente.')
    except Estudiante.DoesNotExist:
        messages.error(request, 'No se encontró el Ciclo que intentas eliminar.')
    
    return HttpResponseRedirect("/Core/plan/ver")

###################################
###################################
@login_required
def espacioEdit(request, id_espacio):
    espacio = EspacioCurricular.objects.get(id=id_espacio)
    if request.method == 'GET':
        form = forms.EspacioCurricularEditForm(instance= espacio)
    else:
        form = forms.EspacioCurricularEditForm(request.POST, instance= espacio)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/espacio/ver")
    return render(request, 'Core/EspacioCurricular/EspaciosCurricularesForm.html',{'form':form})

@login_required
def menuPlan(request):
    return render(request, 'Core/Plan/menuPlan.html')

@login_required
def menuCiclo(request):
    hay_ciclo = Ciclo.objects.exists()
    try:
        ciclo_activo =  Ciclo.objects.get(esActual='True').fechaInicio <= timezone.now().date() >= Ciclo.objects.get(esActual='True').fechaInicio
        print("HAY CICLOOOOOOO1",ciclo_activo)
    except Ciclo.DoesNotExist:
        ciclo_activo = False
    print('ciclo',ciclo_activo)
    return render(request, 'Core/Plan/menuCiclo.html',{'cicloActivo':ciclo_activo})

@login_required
def eliminarCiclo(request, idCiclo):
    try:
        ciclo = Ciclo.objects.get(id=idCiclo)
        if not (Ciclo.objects.filter(Q(plan=ciclo.plan) & ~Q(id=idCiclo)).exists()):
            plan = PlanDeEstudios.objects.get(id = ciclo.plan.id)
            plan.implementado = 'False' 
            plan.save()
        ciclo.delete()
        messages.success(request, 'El Ciclo se eliminó correctamente.')
    except Estudiante.DoesNotExist:
        messages.error(request, 'No se encontró el Ciclo que intentas eliminar.')
    
    return HttpResponseRedirect("/Core/plan/ver")

def aniosDePlanActual(request):
    ciclo = Ciclo.objects.get(esActual=True)
    print("ciclo", ciclo)
    plan = PlanDeEstudios.objects.get(id=ciclo.plan.id)
    print("plan",plan)
    anios = AnioPlan.objects.filter(plan = plan.id)
    return render(request, 'Core/Plan/aniosActuales.html',{'anios':anios,
                                                            'ciclo':ciclo})


class espacioList(ListView):
    model = EspacioCurricular
    template_name = 'Core/EspacioCurricular/verEspacios.html'

@login_required
def cargarEspacios(request):
    anioPlan = request.GET.get('anio')
    espacios = EspacioCurricular.objects.filter(anio_id=anioPlan)
    print(anioPlan,espacios)
    return render(request, 'Cursada/opciones_espacios.html', {'espacios': espacios})

########## ESTOY ACA #################
@login_required
def anioList(request, id):
    print("llegue",id)
    ciclo = Ciclo.objects.get(esActual = 'True')
    print((ciclo))
    anioPlan = AnioPlan.objects.filter(plan = ciclo.plan)
    print(anioPlan)
    return render(request, 'Core/Plan/verAnio.html',{'anioPlan': anioPlan,
                                                     'id':ciclo.id})

@login_required
def cicloList(request, id):
    print(id)
    print("VER CICLO Estoy aca")
    anioCicloPlan= Ciclo.objects.filter(plan= id)
    print (anioCicloPlan)
    return render(request, 'Core/Plan/verCiclo.html',{'ciclo': anioCicloPlan,
                                                      'id':id})    

######ESTOY ACA####
@login_required
def cicloPlanList(request, id):
    print(id)
    plan = PlanDeEstudios.objects.get(id=id)
    print("VER CICLO estoy aca", plan.id)
    
    anioCicloPlan= Ciclo.objects.filter(plan=plan).order_by('-esActual')

    print (anioCicloPlan)
    return render(request, 'Core/Plan/verCiclo.html',{'ciclo': anioCicloPlan, 'id':id, 'plan':plan })    
@login_required
def cicloView(request):
    print('entre acaaaaa',id)
    plan = get_object_or_404(PlanDeEstudios, esActual='True')
    anios = AnioPlan.objects.filter(plan=plan.id)

    form = forms.CicloForm(request.POST) if request.method == 'POST' else forms.CicloForm()

    if request.method == 'POST' and form.is_valid():
        print("Entre aca era valido")
        ciclo = form.save()
        ciclo.crear_division_para_anio_ciclo(ciclo, anios)
        Ciclo.cambiar_actual(request, ciclo.id)
        plan.implementado = True
        plan.save()
        return redirect('/Core/ciclo/verEnPlan/'+str(plan.id))

    return render(request, 'Core/Plan/CicloForm.html', {'form': form, 'plan': plan, 'id': id})

def cambiarActual(request, id_plan):
    # Llama al método cambiar_actual de la clase PlanDeEstudios
    PlanDeEstudios.cambiar_actual(request, id_plan)

    # Redirige a la página deseada después de realizar el cambio
    return HttpResponseRedirect("/Core/plan/ver")
    
@login_required
def cicloEdit(request, id_ciclo):
    ciclo = Ciclo.objects.get(id=id_ciclo)
    if request.method == 'GET':
        form = forms.CicloEditForm(instance=ciclo)
    else:
        form = forms.CicloEditForm(request.POST, instance= ciclo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/plan/ver")
    return render(request, 'Core/Plan/CicloForm.html',{'form': form})

################################################
@login_required
def divisionList(request, id,idCiclo):
    division= list(Division.objects.filter(anio = id,ciclo = idCiclo))
    anio = AnioPlan.objects.get(id=id)
    ciclo = Ciclo.objects.get(esActual= 'True')
    alumnos= Inscripcion.objects.filter(anio = anio,ciclo = ciclo)
    print('cantidad de alumnos',alumnos.count())
    print("VER Division")
    #division= list(Division.objects.filter(anio = id))
    print("VER Division2")
    #print(list(string.ascii_uppercase)[((len(division)))])
    print("request", request.method)
    if request.method == 'POST':
        print("etre al post")
        # Obtén los datos del formulario y crea la nueva división
        codigo = list(string.ascii_uppercase)[((len(division)))]
        descripcion = anio.codigo + ', Año Division '+ codigo
        print(descripcion)
        nueva_division = Division(ciclo=Ciclo.objects.get(esActual= 'True'), codigo=codigo, descripcion=descripcion, anio=anio)
        nueva_division.save()
        nueva_division.crear_Horario_Division()
        division= list(Division.objects.filter(anio = id,ciclo = idCiclo))
    return render(request, 'Core/Plan/verDivision.html',{'divisiones': division,
                                                      'id':idCiclo,
                                                      'anio':id,
                                                      'cant_alumnos':len(alumnos),
                                                      'cant_divisiones':len(division)})  

@login_required
def verDivisionInasistencia(request, id,idCiclo):
    print(id)
    print("VER Division")
    division= list(Division.objects.filter(anio = id,ciclo = idCiclo))
    print("VER Division2")
    print (division)
    return render(request, 'Core/Plan/verDivisionInasistencia.html',{'divisiones': division,
                                                      'id':id,
                                                      'anio':division[0].anio.id})  
################################################
@login_required
def inscripcionDeEstudianteCiclo(request, id_ciclo=1):
    id_ciclo_actual = Ciclo.objects.get(esActual=True)
    inscriptos = [] if not id_ciclo_actual else Inscripcion.objects.filter(ciclo=id_ciclo_actual)
    cant_inscriptos = inscriptos.count()

    if request.method == 'GET':
        form = forms.inscripcionAlumnoForm()
    else:
        form = forms.inscripcionAlumnoForm(request.POST)
        estudiante = form.data.get('estudiante')
        fecha = form.data.get('fecha')
        cicloid = form.data.get('ciclo')
        anio = form.data.get('anio')

        if form.is_valid():
            form.save()
            correcto = 'Alumno Inscripto correctamente'
            return render(request, 'Core/Persona/Inscripciones.html', {'form': form,
                                                                       'ciclo': id_ciclo_actual,
                                                                       'inscriptos': inscriptos,
                                                                       'cant_inscriptos': cant_inscriptos,
                                                                       'correcto': correcto
                                                                       })

    return render(request, 'Core/Persona/Inscripciones.html', {'form': form,
                                                               'inscriptos': inscriptos,
                                                               'ciclo': id_ciclo_actual})
@login_required
def estudiantesDeAnioEnCiclo(request, idCiclo):
    estudiantesCiclo=  Inscripcion.objects.filter(ciclo = idCiclo)   
    return render(request, 'Core/Persona/estudiantes_por_anio_ciclo.html', {'estudiantes': estudiantesCiclo})

def listEstudianteAula(request,idDivision):
    aula = Aula.objects.get(division_id=idDivision)
    return render(request, 'Cursada/cargarInasistencia.html',{'inscriptos': list(aula.estudiantes.all()),
                                                                 'idDivision': idDivision})

@login_required
def asignarEstudianteDivision(request, idAnio, idCiclo):
    inscriptos = Inscripcion.objects.filter(anio = idAnio, ciclo = idCiclo)
    division = Division.objects.filter(anio = idAnio, ciclo = idCiclo)
    print(division)
    cantidadAlumnosInscriptos = inscriptos.count()
    print("cantidad alumnos", inscriptos)
    print(cantidadAlumnosInscriptos)
    if request.method == 'POST':
        form = Division(request.POST)
        if form.is_valid():
            print("estoy en el Post")
            print(form)
            alumno = form.save()
            #division.estudiates.add(estudiante).
            #aula.alumnos.add(alumno)
            return HttpResponseRedirect("/Notas/verInasistencias")

            #return redirect('detalle_aula', aula_id=aula_id)
    else:
        form = forms.DivisionForm()

    return render(request, 'Cursada/cargarInasistencia.html',{'form':form, 
                                                                 'inscriptos': inscriptos,
                                                                 'cantAlumnos': cantidadAlumnosInscriptos})

def asignarEstudianteAula(request,id_anio):
    ciclo_actual = Ciclo.objects.get(esActual=True)
    # Obtener las divisiones del año y ciclo actual
    divisiones = Division.objects.filter(anio=id_anio, ciclo=ciclo_actual)

    # Obtener los estudiantes inscritos al año y ciclo actual
    estudiantes = Inscripcion.objects.filter(anio=id_anio, ciclo=ciclo_actual)
    #divisiones = Division.objects.filter(anio = id_anio,ciclo=1)
    #estudiantes = Inscripcion.objects.filter(anio = id_anio)
    print(estudiantes)
    cantidadInscriptos =estudiantes.count()
    cantidadDivisiones = divisiones.count()
    return render(request,'Cursada/Aula.html',{'inscriptos': estudiantes,
                                                                 'cantAlumnos': cantidadInscriptos,
                                                                 'cantDivisiones': cantidadDivisiones})


def exportarHistorialPdf(request, estudiante_id):
    estudiante = Estudiante.objects.get(pk=estudiante_id)
    inscripciones = Inscripcion.objects.filter(estudiante=estudiante).order_by('fecha')
    faltas = Inasistencias.objects.filter(estudiante=estudiante).order_by('dia')
    
    # Crear un buffer de bytes en memoria para el PDF
    buffer = BytesIO()

    # Crear el documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Obtener los estilos de muestra de ReportLab
    styles = getSampleStyleSheet()

    # Encabezado
    elements.append(Paragraph("Historial del Estudiante", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Estudiante: {estudiante.nombre} {estudiante.apellido}", styles['Normal']))
    elements.append(Paragraph(f"Fecha de alta: {(estudiante.fechaInscripcion).strftime('%d-%m-%Y')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Datos del historial
    data = [["Plan de Estudio", "Ciclo", 'Año', "Fecha de Inscripción"]]
    for inscripcion in inscripciones:
        data.append([
            inscripcion.ciclo.plan.anio,
            inscripcion.ciclo,
            inscripcion.anio, 
            inscripcion.fecha.strftime("%d-%m-%Y")
        ])
    
    # Crear tabla con los datos del historial
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    # Establecer ancho de las columnas
    table._argW[0] = 2.5 * inch  # Ancho de la primera columna
    table._argW[1] = 2 * inch    # Ancho de la segunda columna
    table._argW[2] = 1.5 * inch  # Ancho de la tercera columna
    
    # Establecer espacio entre filas
    table.setStyle(TableStyle([
        ('SPACEBEFORE', (0,0), (-1,-1), 12),
        ('SPACEAFTER', (0,0), (-1,-1), 12)
    ]))
    
    elements.append(table)

    # Datos de inasistencias
    inasistencias = [['Fecha', 'Justificada?']]

    for falta in faltas:
        justificada = 'SI' if falta.justificacion else 'NO'
        inasistencias.append([
            falta.dia.strftime("%d-%m-%Y"),  # Ajusta el formato según sea necesario
            justificada])

    # Crear tabla con los datos de inasistencias
    table_inasistencias = Table(inasistencias)
    table_inasistencias.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    # Establecer ancho de las columnas
    table_inasistencias._argW[0] = 2 * inch  # Ancho de la primera columna
    table_inasistencias._argW[1] = 2 * inch  # Ancho de la segunda columna
    
    # Establecer espacio entre filas
    table_inasistencias.setStyle(TableStyle([
        ('SPACEBEFORE', (0,0), (-1,-1), 12),
        ('SPACEAFTER', (0,0), (-1,-1), 12)
    ]))
    
    elements.append(Paragraph("Inasistencias:", styles['Title']))
    elements.append(table_inasistencias)

    # Construir el PDF
    doc.build(elements)
    buffer.seek(0)

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="historial_estudiante_{estudiante_id}.pdf"'
    return response