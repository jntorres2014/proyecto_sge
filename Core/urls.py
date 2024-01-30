from django.urls import path, re_path
from . import views

app_name = "Core"
urlpatterns = [
    path('estudiante-autocomplete', views.EstudianteAutocomplete.as_view(), name='estudiante-autocomplete'),
    path('localidad-autocomplete', views.LocalidadAutocomplete.as_view(), name='localidad-autocomplete'),
    
    re_path(r'^altaLocalidad$', views.localidad_view, name='altaLocalidad'),
    re_path(r'^verLocalidad$', views.localidad_list.as_view(), name='verLocalidad'),
    re_path(r'^importar/$', views.importar, name='importar'),
    re_path(r'^modificarLocalidad/(?P<id_localidad>\d+)/$', views.localidad_edit, name='modificarLocalidad'),

    re_path(r'^altaDocente$', views.docente_view, name='altaDocente'),
    re_path(r'^verDocentes$', views.docente_list.as_view(), name='verDocentes'),
    re_path(r'^modificarDocente/(?P<id_docente>\d+)/$', views.docente_edit, name='modificarDocente'),
    
    re_path(r'^altaEstudiante$', views.Estudiante_view, name='altaEstudiante'),
    re_path(r'^verEstudiantes$', views.estudiante_list.as_view(),name='verEstudiantes'),
    re_path(r'^modificarEstudiante/(?P<id_estudiante>\d+)/$', views.estudiante_edit, name='modificarEstudiante'),
    re_path(r'^eliminarEstudiante/(?P<id_estudiante>\d+)/$', views.eliminar_estudiante, name='eliminarEstudiante'),
    
    re_path(r'^altaPlan$', views.plan_de_estudios_view,name='altaPlan'),
    re_path(r'^menuPlanDeEstudio$', views.menuPlan,name='menuPlanDeEstudio'),
    re_path(r'^menuCiclo$', views.menuCiclo,name='menuCiclo'),
    
    re_path(r'^menuCursada$', views.menuCursada,name='menuCursada'),
    re_path(r'^aniosDePlanActual$', views.aniosDePlanActual,name='aniosDePlanActual'),
    
    re_path(r'^verPlan$', views.plan_list, name= 'verPlan'),
    re_path(r'^modificarPlan/(?P<id_plan>\d+)/$', views.plan_edit, name='modificarPlan'),
    re_path(r'^cambiar_actual/(?P<id_plan>\d+)/$', views.cambiar_actual, name='cambiar_actual'),

    #re_path(r'^altaAnio$', views.,name='altaAnio'),
    #re_path(r'^menuPlanDeEstudio$', views.menuPlan,name='menuPlanDeEstudio'),
    re_path(r'^verAnio/(?P<id>\d+)/$', views.anio_list, name= 'verAnio'),
    

    # re_path(r'^altaCiclo/(?P<id>\d+)/$', views.ciclo_view,name='altaCiclo'),
    
    re_path(r'^verCicloEnPlan/(?P<id>\d+)/$', views.cicloPlan_list, name='verCicloEnPlan'),
    re_path(r'^verCiclo/(?P<id>\d+)/$', views.ciclo_list, name='verCiclo'),
    re_path(r'^altaCiclo/(?P<id>\d+)/$', views.ciclo_view,name='altaCiclo'),
    
    
    re_path(r'^modificarCiclo/(?P<id_ciclo>\d+)/$', views.ciclo_edit, name='modificarCiclo'),

    re_path(r'^inscribir_Ciclo/(?P<id_ciclo>\d+)/$', views.inscripciones_alumnnos_ciclo, name='inscribir_Ciclo'),
    
    re_path(r'^alumno_division/(?P<idAnio>\d+)/(?P<idCiclo>\d+)/$', views.AsignarAlumno_Division, name='alumno_division'),    
    
    
    re_path(r'^verEspacioCurricularEnPlan/(?P<id>\d+)/$', views.Espacio_view, name='verEspacioCurricularEnPlan'),

    re_path(r'agregarEspacio/(?P<id_plan>\d+)/$', views.Espacio_view,name= 'agregarEspacio'),

    re_path(r'^altaEspacio$', views.Espacio_view,name='altaEspacio'),

    re_path(r'^verEspacios$', views.Espacio_list.as_view(), name='verEspacios'),
    re_path(r'^modificarEspacio/(?P<id_espacio>\d+)/$', views.espacio_edit, name='modificarEspacio'),
    path('ajax/cargar-espacios/', views.cargar_espacios, name='ajax_cargar_espacios'),
    
    
    re_path(r'^verDivision/(?P<id>\d+)/(?P<idCiclo>\d+)/$', views.division_list, name='verDivision'),
    re_path(r'^verDivisionInasistencia/(?P<id>\d+)/(?P<idCiclo>\d+)/$', views.verDivisionInasistencia, name='verDivisionInasistencia'),
    
    #path('altaDivision/<int:id>/', views.division_new, name='altaDivision'),
    re_path(r'^altaDivision/(?P<anio_id>\d+)/(?P<id>\d+)/$', views.division_new,name='altaDivision'),
 
    re_path(r'^inscripcion$', views.inscripciones_alumnnos_ciclo,name='inscripcion'),
    
 #   re_path(r'^altaInscripcion$', views.crearInscripcion,name='Altainscripcion'),
    
    re_path(r'^estudiantesDeAnioEnCiclo$', views.estudiantesDeAnioEnCiclo,name='estudiantesDeAnioEnCiclo'),

    #re_path(r'^verInscriptos$', views.inscriptos.as_view(), name='verInscriptos'),
    
        
    re_path(r'^asignarAlumno_Division/(?P<idAnio>\d+)(?P<idCiclo>\d+)/$', views.AsignarAlumno_Division,name='asignarAlumno_Division'),

    re_path(r'^asignar_estudiante_a_aula/(?P<id_anio>\d+)/$', views.asignar_estudiante_a_aula,name='asignar_estudiante_a_aula'),

]