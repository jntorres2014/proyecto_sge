from django.urls import re_path, path
from . import views

app_name = "Clases"
urlpatterns  = [
        path('autocomplete_estudiantes/', views.autocomplete_estudiantes, name='autocomplete_estudiantes'),
    path('reportesGraficos/', views.reportes_graficos, name='reportes_graficos'),
    path('reporteNotas/', views.reporteNotas, name='reporteNotas'),
    path('reporte/', views.reporte_view, name='reporte'),
    path('reporte/data/', views.get_reporte_data, name='reporte_data'),
    path('reporte/ciclos/', views.get_ciclos, name='reporte_ciclos'),
    path('reporte/instancias/', views.get_instancias, name='reporte_instancias'),
    re_path(r'^altaCalificacion$', views.calificacion_view),
    re_path(r'^verCalificacion$', views.calificacion_list.as_view(), name='verCalificacion'),
    re_path(r'^modificarCalificacion/(?P<id_calificacion>\d+)/$', views.calificacion_edit, name='modificarCalificacion'),
    path('inasistencias_por_anio/', views.inasistencias_por_anio, name='inasistencias_por_anio'),
    path('inasistencias_por_mes/<int:year>/', views.inasistencias_por_mes, name='inasistencias_por_mes'),
    re_path(r'^verInstancias$', views.instancias_list, name='verInstancias'),
    re_path(r'^inhabilitarInstancia/(?P<instancia_id>\d+)/$', views.inhabilitarInstancia, name='inhabilitarInstancia'),
    re_path(r'^habilitarInstancia$', views.habilitarInstancia, name='habilitarInstancia'),
    # path('Clases/habilitarInstancia/<int:instancia_id>/', views.habilitar_instancia, name='habilitar_instancia'),
    re_path(r'^altaInstancia$', views.instancia_view),
    re_path(r'^habilitarInstancia/(?P<instancia_id>\d+)/$', views.habilitarInstancia, name='habilitarInstancia'),
    re_path(r'^altaInasistencia$', views.inasistencia_view),
    re_path(r'^verInasistencia$', views.inasistencia_list.as_view(), name='verInasistencia'),
    re_path(r'^modificarInasistencia/(?P<id_inasistencia>\d+)/$', views.calificacion_edit, name='modificarInasistencia'),
     path('reporte/inasistencias/', views.reporte_inasistencias, name='reporte_inasistencias'),
    re_path(r'^altaHorario$', views.crear_horario),

    re_path(r'^nota/eliminar/$', views.eliminarNota, name='nota/eliminar'),

     #****************************** Cursada ****************************** # 
    re_path(r'^clases/menu$', views.menuCursada,name='clases/menu'),
    path('eliminarInasistencias/', views.eliminarInasistencias, name='eliminarInasistencias'),
    path('boletin/<int:estudiante_id>/<int:ciclo_id>/', views.boletinEstudiante, name='boletin'),

    re_path(r'^cargarInasistencia/(?P<idAnio>\d+)/$', views.registrarInasistencia, name= 'registrarInasistencia'),
    re_path(r'^asignar_alumno_a_aula/(?P<idAnio>\d+)/$', views.asignar_alumno_a_aula, name= 'asignar_alumno_a_aula'),
    re_path(r'^verAulas/(?P<idAnio>\d+)/(?P<idCiclo>\d+)/$', views.verAulas, name= 'verAula'),
    
    # re_path(r'^crearDivision/(?P<id>\d+)/(?P<idCiclo>\d+)/$', views.crearDivision, name='crearDivision'), 
    
    re_path(r'^crear_horario/(?P<idDivision>\d+)/$', views.crear_horario, name= 'crear_horario'),
    re_path(r'^consultar_faltas/$', views.consultar_faltas, name='consultar_faltas'),
    re_path(r'^obtener_alumnos/(?P<idEstudiante>\d+)/$', views.obtener_alumnos, name='obtener_alumnos'),
    
    re_path(r'^docente/notas/(?P<id_division>\d+)/$', views.estudiantes_aulas, name='docente/notas'),
    
    path('obtenerHorarios/', views.obtenerHorarios, name='obtenerHorarios'),
    # path('obtener_aulas/', views.obtener_aulas, name='obtener_aulas'),
    path('reporte_alumno/', views.reporte_alumno, name='reporte_alumno'),
    
    path('obtener_alumnos/', views.obtener_alumnos, name='obtener_alumnos'),
    path('actualizar_relacion/', views.actualizar_relacion, name='actualizar_relacion'),
    path('eliminar_detalle_horario/', views.eliminar_detalle_horario, name='eliminar_detalle_horario'),
    path('eliminarAlumno/', views.eliminarAlumno, name='eliminarAlumno'),
    re_path(r'^verBoletines/$', views.verBoletines, name='verBoletines'),
    path('consultar-faltas/', views.reporte_inasistencias_por_aula, name='consultar_faltas'),
]
