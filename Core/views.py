from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from Core import forms
from .models import PlanDeEstudios, Localidad, Docente,Estudiante,EspacioCurricular, AnioPlan, Ciclo, Persona,inscripcionEstudianteCiclo, Division
from django.views.generic import ListView,TemplateView
from django.db.models import Q

from dal import autocomplete

class EstudianteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Estudiante.objects.all()
        print(qs)
        if self.q:
            qs = qs.filter( Q(Nombre__icontains=self.q) |    # Buscar en el atributo "nombre"
                Q(Apellido__icontains=self.q) |       # Buscar en el atributo "apellido"
                Q(Dni__icontains=self.q))           # Buscar en el atributo "Dni"
        return qs


##################################################################
@login_required
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
@login_required
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
@login_required
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

@login_required
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
@login_required
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


@login_required
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

@login_required
def plan_de_estudios_view(request):
    if request.method == 'POST':
        form = forms.PlanDeEstudiosForm(request.POST)
        if form.is_valid():
           plan= form.save()
           plan.crear_anios_plan(plan)
           return HttpResponseRedirect("verPlan")
    else:
        form = forms.PlanDeEstudiosForm()
    return render(request, 'Core/Plan/PlanDeEstudios.html', {'form': form})

@login_required    
def plan_list(request):
    planes=PlanDeEstudios.objects.order_by('id')
    print(planes)
    return render(request, 'Core/Plan/verPlan.html', {
        'planes': planes,
    })    

@login_required
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

@login_required
def Espacio_view(request, id):
    print(id)
    plan = PlanDeEstudios.objects.get(id=id)
    espacios = EspacioCurricular.objects.filter(plan = id)
    if request.method == 'POST':
        form = forms.EspacioCurricularForm(request.POST, id_plan=id)
        if form.is_valid():
            print("guardando datoss")
            form.save()
            #return HttpResponseRedirect("/Core/EspacioCurricular/EspaciosCurricularesForm.html")
    else:
        form = forms.EspacioCurricularForm(id_plan=id)
        
    print("retornando formiulariox")
    return render(request, 'Core/EspacioCurricular/EspaciosCurricularesForm.html', {
        'form': form,
        'plan': plan,
        'espacios': espacios})
###################################
###################################
@login_required
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

@login_required
def menuPlan(request):
    return render(request, 'Core/Plan/menuPlan.html')

@login_required
def menuCiclo(request):
    return render(request, 'Core/Plan/menuCiclo.html')

def menuCursada(request):
    return render(request, 'Cursada/menuCursada.html')

class Espacio_list(ListView):
    model = EspacioCurricular
    template_name = 'Core/EspacioCurricular/verEspacios.html'

@login_required
def cargar_espacios(request):
    anioPlan = request.GET.get('anio')
    espacios = EspacioCurricular.objects.filter(anio_id=anioPlan)
    print(anioPlan,espacios)
    return render(request, 'Cursada/opciones_espacios.html', {'espacios': espacios})

########## ESTOY ACA #################
@login_required
def anio_list(request, id):
    
    print("llegue",id)
    plan = Ciclo.objects.filter(id = id).first()
    print((plan))
    anioPlan = AnioPlan.objects.filter(plan = plan.plan)
    print(anioPlan)
    return render(request, 'Core/Plan/verAnio.html',{'anioPlan': anioPlan,
                                                     'id':id})

@login_required
def ciclo_list(request, id):
    print(id)
    print("VER CICLO Estoy aca")
    anioCicloPlan= Ciclo.objects.filter(plan= id)
    print (anioCicloPlan)
    return render(request, 'Core/Plan/verCiclo.html',{'ciclo': anioCicloPlan,
                                                      'id':id})    

######ESTOY ACA####
@login_required
def cicloPlan_list(request, id):
    print(id)
    plan = PlanDeEstudios.objects.get(id=id)
    print("VER CICLO estoy aca", plan.id)
    
    anioCicloPlan= Ciclo.objects.filter(plan=id)

    print (anioCicloPlan)
    return render(request, 'Core/Plan/verCiclo.html',{'ciclo': anioCicloPlan, 'id':id, 'plan':plan })    

@login_required
def ciclo_view(request,id):
    plan = PlanDeEstudios.objects.get(id=id)
    print("******************")
    print(plan)
    #print(request.method)
    if request.method == 'POST':
        # form = forms.PlanDeEstudiosForm(request.POST, instance=plan)
        form = forms.CicloForm(request.POST,)
        print("entre al post")
        if form.is_valid():
            print("era valido")
            form.save()
            pagina = "/Core/verCiclo/" + id
            #print("la pagina",pagina)
        return HttpResponseRedirect("/Core/verCiclo/" + id)
    else:
        form = forms.CicloForm()
    return render(request, 'Core/Plan/CicloForm.html', {
        'form': form,
        'plan': plan,
        'id':id})
    
@login_required
def ciclo_edit(request, ciclo):
    ciclo = Ciclo.objects.get(id=ciclo)
    if request.method == 'GET':
        form = forms.Ciclo(instance=ciclo)
    else:
        form = forms.CicloForm(request.POST, instance= ciclo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/Core/verCiclo")
    return render(request, 'Core/Plan/cicloForm.html',{'form': form})

################################################
@login_required
def division_list(request, id):
    print(id)
    print("VER Division")
    division= list(Division.objects.filter(anio = id))
    print("VER Division2")
    print (division)
    return render(request, 'Core/Plan/verDivision.html',{'divisiones': division,
                                                      'id':id,
                                                      'anio':division[0].anio.id})    
@login_required
def division_new(request, anio_id, id):
    anio = AnioPlan.objects.get(id=anio_id)
    ciclo = Ciclo.objects.get(id=id)
    print("Estoy en division New", request.method)
    if request.method == 'POST':
        print("etre al post")
        # Obtén los datos del formulario y crea la nueva división
        codigo = '6'
        descripcion = 'Descripción de la división'
        nueva_division = Division(ciclo=ciclo, codigo=codigo, descripcion=descripcion, anio=anio)
        nueva_division.save()
        # Redirige al usuario a la página de listado de divisiones
        return redirect('altaDivision', anio_id=anio_id,id=id)
    # Renderiza el formulario para agregar divisiones
    form = forms.DivisionForm()
    return render(request, 'Core/Plan/divisionForm.html', {
        'form': form,
        'division': nueva_division,  # Puedes incluir la nueva división si es necesario
        'id': id,
        'anio': anio,
    })


    # if request.method == 'POST':
    #     # Obtén los datos del formulario y crea la nueva división
    #     ciclo = Ciclo.objects.get(id=id)
    #     codigo = '6'
    #     descripcion = 'Descripción de la división'
    #     anio = AnioPlan.objects.get(id=anio_id)
    #     nueva_division = Division(ciclo=ciclo, codigo=codigo, descripcion=descripcion, anio=anio)
    #     nueva_division.save()
    #     # Después de crear la división, puedes redirigir al usuario nuevamente a la página de listado de divisiones
    #     return HttpResponseRedirect('/Core/verDivisiones/')    
    #     return render(request, 'Core/Plan/verDivision.html',{'divisiones': divisiones,
    #                                                   'id':id,
    #                                                   'anio':anio})
    # # Redirige a la página principal u otra página después de agregar la división
    # #return redirect('/Core/verDivision/'+id)



    # if request.method == 'POST':
    #     # form = forms.PlanDeEstudiosForm(request.POST, instance=plan)
    #     form = forms.DivisionForm(request.POST,)
    #     print("entre al post")
    #     if form.is_valid():
    #         print("era valido")
    #         form.save()
    #         pagina = "/Core/verCiclo/" + id
    #         #print("la pagina",pagina)
    #     return HttpResponseRedirect("/Core/altaDivision/" + id)
    # else:
    #     form = forms.DivisionForm()
    # return render(request, 'Core/Plan/divisionForm.html', {
    #     'form': form,
    #     'division': division,
    #     'id':id})


################################################
@login_required
def inscripciones_alumnnos_ciclo(request, id_ciclo=None):
    print("Llegue aca!!!!")
    
    inscriptos = [] if not id_ciclo else inscripcionEstudianteCiclo.objects.filter(ciclo = id_ciclo)
    if request.method == 'GET':
        form = forms.inscripcionAlumnoForm()
    else:
        print("entre al post")
        form = forms.inscripcionAlumnoForm(request.POST)
        estudiante = form.data.get('estudiante')  # Acceder a los datos sin importar si el formulario es válido
        fecha = form.data.get('fecha')
        print(fecha,estudiante)
        
        if form.is_valid():
            print("era valido")
            form.save()
            #return HttpResponseRedirect("/Core/Personas/Inscripciones.html")
    return render(request, 'Core/Persona/Inscripciones.html',{'form': form, 
                                                              #'estudiantes': estudiantes,
                                                              #'ciclos': ciclos,
                                                              #'anios': anios,
                                                              'inscriptos': inscriptos})

# class Inscripciones(forms.Form):
#     my_field = ModelSelect2(url='my_autocomplete', model=inscripcionEstudianteCiclo)

@login_required
def estudiantesDeAnioEnCiclo(request, idCiclo):
    
    estudiantesCiclo=  inscripcionEstudianteCiclo.objects.filter(ciclo = idCiclo)
    
    return render(request, 'Core/Persona/estudiantes_por_anio_ciclo.html', {'estudiantes': estudiantesCiclo})
@login_required
def AsignarAlumno_Division(request, idAnio, idCiclo):
    inscriptos = inscripcionEstudianteCiclo.objects.filter(anio = idAnio, ciclo = idCiclo)
    division = Division.objects.all()
    cantidadAlumnosInscriptos = inscriptos.count()
    print("cantidad alumnos")
    print(cantidadAlumnosInscriptos)
    if request.method == 'POST':
        form = Division(request.POST)
        if form.is_valid():
            alumno = form.save()
            #division.estudiates.add(estudiante).
            #aula.alumnos.add(alumno)
            return HttpResponseRedirect("/Notas/verInasistencias")

            #return redirect('detalle_aula', aula_id=aula_id)
    else:
        form = forms.DivisionForm()

    return render(request, 'Inasistencia/inasistenciaForm.html',{'form':form, 
                                                                 'inscriptos': inscriptos,
                                                                 'cantAlumnos': cantidadAlumnosInscriptos})