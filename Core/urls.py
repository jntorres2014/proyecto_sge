from django.urls import path, re_path
from . import views

app_name = "Core"
urlpatterns = [
    
    #****************************** AUTOCOMPLETE ****************************** # 
    path('estudiantes-autocomplete-aula', views.EstudianteAutocompleteAula.as_view(), name='estudiantes-autocomplete-aula'),
    path('estudiante-autocomplete', views.EstudianteAutocomplete.as_view(), name='estudiante-autocomplete'),
    path('localidad-autocomplete', views.LocalidadAutocomplete.as_view(), name='localidad-autocomplete'),
    path('espacio-autocomplete', views.MateriaAutocomplete.as_view(), name='espacio-autocomplete'),
    path('docente-autocomplete', views.DocenteAutocomplete.as_view(), name='docente-autocomplete'),
    path('docenteHora-autocomplete', views.DocenteHoraAutocomplete.as_view(), name='docenteHora-autocomplete'),
    #****************************** LOCALIDAD ****************************** # 
    re_path(r'^localidad/alta$', views.localidadView, name='localidad/alta'),
    re_path(r'^localidad/ver$', views.localidadList, name='localidad/ver'),
    re_path(r'^importar/$', views.importar, name='importar'),
    path('importarLocalidades/', views.importar_localidades, name='importarLocalidades'),
    path('importarEspacios/', views.importar_espacios, name='importarEspacios'),
    re_path(r'^localidad/modificar/(?P<id_localidad>\d+)/$', views.localidadEdit, name='localidad/modificar'),
    re_path(r'^localidad/eliminar/(?P<idLocalidad>\d+)/$', views.eliminarLocalidad, name='localidad/eliminar'),
    #****************************** DOCENTE ****************************** # 
    re_path(r'^docente/alta$', views.docenteView, name='docente/alta'),
    re_path(r'^docente/ver$', views.docenteList.as_view(), name='docente/ver'),
    re_path(r'^docente/eliminar/(?P<id_docente>\d+)/$', views.eliminarDocente, name='docente/eliminar'),
    re_path(r'^docente/modificar/(?P<id_docente>\d+)/$', views.docenteEdit, name='docente/modificar'),
    re_path(r'^docente/inscripcion$', views.inscripcionDeDocenteCiclo,name='docente/inscripcion'),
    re_path(r'^docente/menu$', views.menuDocente,name='docente/menu'),
    re_path(r'^docente/eliminarInscripcionDocente/(?P<id_docente>\d+)/(?P<id_anio>\d+)/(?P<id_ciclo>\d+)/$', views.eliminarInscripcionDocente, name='docente/eliminarInscripcionDocente'),
    
    #****************************** ESTUDIANTE ****************************** # 
    re_path(r'^estudiante/alta$', views.estudianteView, name='estudiante/alta'),
    re_path(r'^estudiante/ver$', views.estudianteList.as_view(),name='estudiante/ver'),
    re_path(r'^estudiante/modificar/(?P<id_estudiante>\d+)/$', views.estudianteEdit, name='estudiante/modificar'),
    re_path(r'^estudiante/eliminar/(?P<id_estudiante>\d+)/$', views.eliminarEstudiante, name='estudiante/eliminar'),
    re_path(r'estudiante/exportar-pdf/(?P<estudiante_id>\d+)/$', views.exportarHistorialPdf, name='exportar-pdf'),
    re_path(r'^estudiante/inscripcion$', views.inscripcionDeEstudianteCiclo,name='estudiante/inscripcion'),
    re_path(r'^estudiante/eliminarInscripcion/(?P<id_estudiante>\d+)/$', views.eliminarInscripcion, name='estudiante/eliminarInscripcion'),
    re_path(r'^verAlumnoInasistencia/(?P<idDivision>\d+)/$', views.listEstudianteAula, name='verAlumnoInasistencia'),
    re_path(r'^corregirAlumnoInasistencia/(?P<idDivision>\d+)/$', views.corregirInasistenciaAula, name='corregirAlumnoInasistencia'),        
    
    re_path(r'^estudiantesDeAnioEnCiclo$', views.estudiantesDeAnioEnCiclo,name='estudiantesDeAnioEnCiclo'),
    re_path(r'^asignarAlumno_Division/(?P<idAnio>\d+)(?P<idCiclo>\d+)/$', views.asignarEstudianteDivision,name='asignarAlumno_Division'),
    re_path(r'^asignar_estudiante_a_aula/(?P<id_anio>\d+)/$', views.asignarEstudianteAula,name='asignar_estudiante_a_aula'),

    #****************************** PLAN DE ESTUDIOS ****************************** # 
    re_path(r'^plan/alta$', views.planDeEstudiosView,name='plan/alta'),
    re_path(r'^plan/menu$', views.menuPlan,name='plan/menu'),
    re_path(r'^plan/ver$', views.planList, name= 'plan/ver'),
    re_path(r'^plan/verDetalle/(?P<id_plan>\d+)/$', views.planDetalle, name= 'plan/verDetalle'),
    re_path(r'^plan/modificar/(?P<id_plan>\d+)/$', views.planEdit, name='plan/modificar'),
    re_path(r'^cambiar_actual/(?P<id_plan>\d+)/$', views.cambiarActual, name='cambiar_actual'),

    #****************************** CICLO ****************************** # 
    re_path(r'^ciclo/menu$', views.menuCiclo,name='ciclo/menu'),
    re_path(r'^ciclo/eliminar/(?P<idCiclo>\d+)/$', views.eliminarCiclo, name='ciclo/eliminar'),
    re_path(r'^ciclo/alta/$', views.cicloView,name='ciclo/alta'),
    re_path(r'^ciclo/ver/(?P<id>\d+)/$', views.cicloList, name='ciclo/ver'),
    re_path(r'^ciclo/verEnPlan/(?P<id>\d+)/$', views.cicloPlanList, name='ciclo/verEnPlan'),
    re_path(r'^ciclo/modificar/(?P<id_ciclo>\d+)/$', views.cicloEdit, name='ciclo/modificar'),
    re_path(r'^ciclo/inscribir/(?P<id_ciclo>\d+)/$', views.inscripcionDeEstudianteCiclo, name='ciclo/inscribir'),
    
    #****************************** AÑO  ****************************** #     
    re_path(r'^anio/ver/(?P<id>\d+)/$', views.anioList, name= 'anio/ver'),
    re_path(r'^anio/verActual/$', views.anioListActual, name= 'anio/ver'),
    re_path(r'^aniosDePlanActual$', views.aniosDePlanActual,name='aniosDePlanActual'),
     
    #****************************** DIVISION  ****************************** #
    re_path(r'^alumno_division/(?P<idAnio>\d+)/(?P<idCiclo>\d+)/$', views.asignarEstudianteDivision, name='alumno_division'),    
    re_path(r'^verDivision/(?P<id>\d+)/(?P<idCiclo>\d+)/$', views.divisionList, name='verDivision'),
    re_path(r'^crearDivision/(?P<id>\d+)/(?P<idCiclo>\d+)/$', views.crearDivision, name='crearDivision'),
    re_path(r'^division/eliminar/(?P<id>\d+)/(?P<idCiclo>\d+)/$', views.eliminarDivision, name='eliminarDivision'),
    re_path(r'^verDivisionInasistencia/(?P<id>\d+)/(?P<idCiclo>\d+)/$', views.verDivisionInasistencia, name='verDivisionInasistencia'),
    

    #****************************** ESPACIOS CURRICULAR  ****************************** #    
    re_path(r'^espacio/alta$', views.espacioView,name='espacio/alta'),
    re_path(r'^espacio/verEnPlan/(?P<id>\d+)/$', views.espacioView, name='espacio/verEnPlan'),
    re_path(r'^espacio/ver$', views.espacioList.as_view(), name='espacio/ver'),
    re_path(r'^espacio/modificar/(?P<id_espacio>\d+)/$', views.espacioEdit, name='espacio/modificar'),
    re_path(r'^espacio/eliminar/(?P<id_espacio>\d+)/$', views.espacioEliminar, name='espacio/eliminar'),
        
    

]