from django.urls import path, re_path
from . import views

app_name = "Core"
urlpatterns = [
    path('estudiante-autocomplete', views.EstudianteAutocomplete.as_view(), name='estudiante-autocomplete'),
    path('localidad-autocomplete', views.LocalidadAutocomplete.as_view(), name='localidad-autocomplete'),
    path('espacio-autocomplete', views.MateriaAutocomplete.as_view(), name='espacio-autocomplete'),
    
    re_path(r'^altaLocalidad$', views.localidadView, name='altaLocalidad'),
    re_path(r'^verLocalidad$', views.localidadList.as_view(), name='verLocalidad'),
    re_path(r'^importar/$', views.importar, name='importar'),
    re_path(r'^modificarLocalidad/(?P<id_localidad>\d+)/$', views.localidadEdit, name='modificarLocalidad'),

    re_path(r'^altaDocente$', views.docenteView, name='altaDocente'),
    re_path(r'^verDocentes$', views.docenteList.as_view(), name='verDocentes'),
    re_path(r'^modificarDocente/(?P<id_docente>\d+)/$', views.docenteEdit, name='modificarDocente'),
    
    re_path(r'^altaEstudiante$', views.estudianteView, name='altaEstudiante'),
    re_path(r'^verEstudiantes$', views.estudianteList.as_view(),name='verEstudiantes'),
    re_path(r'^modificarEstudiante/(?P<id_estudiante>\d+)/$', views.estudianteEdit, name='modificarEstudiante'),
    re_path(r'^eliminarEstudiante/(?P<id_estudiante>\d+)/$', views.eliminarEstudiante, name='eliminarEstudiante'),
    
    re_path(r'^altaPlan$', views.planDeEstudiosView,name='altaPlan'),
    re_path(r'^menuPlanDeEstudio$', views.menuPlan,name='menuPlanDeEstudio'),
    re_path(r'^menuCiclo$', views.menuCiclo,name='menuCiclo'),

    re_path(r'^eliminarCiclo/(?P<idCiclo>\d+)/$', views.eliminarCiclo, name='eliminarCiclo'),

    re_path(r'^menuCursada$', views.menuCursada,name='menuCursada'),
    re_path(r'^aniosDePlanActual$', views.aniosDePlanActual,name='aniosDePlanActual'),
    
    re_path(r'^verPlan$', views.planList, name= 'verPlan'),
    re_path(r'^modificarPlan/(?P<id_plan>\d+)/$', views.planEdit, name='modificarPlan'),
    re_path(r'^cambiar_actual/(?P<id_plan>\d+)/$', views.cambiarActual, name='cambiar_actual'),

    re_path(r'^verAnio/(?P<id>\d+)/$', views.anioList, name= 'verAnio'),
    

    re_path(r'^altaCiclo/$', views.cicloView,name='altaCiclo'),
    
    re_path(r'^verCicloEnPlan/(?P<id>\d+)/$', views.cicloPlanList, name='verCicloEnPlan'),
    re_path(r'^verCiclo/(?P<id>\d+)/$', views.cicloList, name='verCiclo'),
    
    re_path(r'^modificarCiclo/(?P<id_ciclo>\d+)/$', views.cicloEdit, name='modificarCiclo'),

    re_path(r'^inscribir_Ciclo/(?P<id_ciclo>\d+)/$', views.inscripcionDeEstudianteCiclo, name='inscribir_Ciclo'),
    
    re_path(r'^alumno_division/(?P<idAnio>\d+)/(?P<idCiclo>\d+)/$', views.asignarEstudianteDivision, name='alumno_division'),    
    
    path('estudiante/<int:estudiante_id>/exportar-pdf/', views.exportarHistorialPdf, name='exportar_historial_pdf'),
    re_path(r'^verEspacioCurricularEnPlan/(?P<id>\d+)/$', views.espacioView, name='verEspacioCurricularEnPlan'),

    re_path(r'agregarEspacio/(?P<id_plan>\d+)/$', views.espacioView,name= 'agregarEspacio'),

    re_path(r'^altaEspacio$', views.espacioView,name='altaEspacio'),

    re_path(r'^verEspacios$', views.espacioList.as_view(), name='verEspacios'),
    re_path(r'^modificarEspacio/(?P<id_espacio>\d+)/$', views.espacioEdit, name='modificarEspacio'),
    path('ajax/cargar-espacios/', views.cargarEspacios, name='ajax_cargar_espacios'),
    
    
    re_path(r'^verDivision/(?P<id>\d+)/(?P<idCiclo>\d+)/$', views.divisionList, name='verDivision'),
    re_path(r'^verDivisionInasistencia/(?P<id>\d+)/(?P<idCiclo>\d+)/$', views.verDivisionInasistencia, name='verDivisionInasistencia'),
    re_path(r'^verAlumnoInasistencia/(?P<idDivision>\d+)/$', views.listEstudianteAula, name='verAlumnoInasistencia'),
     
    re_path(r'^inscripcion$', views.inscripcionEstudianteCiclo,name='inscripcion'),
        
    re_path(r'^estudiantesDeAnioEnCiclo$', views.estudiantesDeAnioEnCiclo,name='estudiantesDeAnioEnCiclo'),

    re_path(r'^asignarAlumno_Division/(?P<idAnio>\d+)(?P<idCiclo>\d+)/$', views.asignarEstudianteDivision,name='asignarAlumno_Division'),

    re_path(r'^asignar_estudiante_a_aula/(?P<id_anio>\d+)/$', views.asignarEstudianteAula,name='asignar_estudiante_a_aula'),

]