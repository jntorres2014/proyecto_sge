from django.urls import re_path, path
from . import views

app_name = "Clases"
urlpatterns  = [
    
    re_path(r'^altaCalificacion$', views.calificacion_view),
    re_path(r'^verCalificacion$', views.calificacion_list.as_view(), name='verCalificacion'),
    re_path(r'^modificarCalificacion/(?P<id_calificacion>\d+)/$', views.calificacion_edit, name='modificarCalificacion'),

    re_path(r'^altaInasistencia$', views.inasistencia_view),
    re_path(r'^verInasistencia$', views.inasistencia_list.as_view(), name='verInasistencia'),
    re_path(r'^modificarInasistencia/(?P<id_inasistencia>\d+)/$', views.calificacion_edit, name='modificarInasistencia'),
    
    re_path(r'^altaHorario$', views.crear_horario),

    re_path(r'^cargarInasistencia/(?P<idAnio>\d+)/$', views.registrarInasistencia, name= 'registrarInasistencia'),
    #path('cargar-inasistencia/<int:anio>/', views.registrarInasistencia, name='registrarInasistencia'),
    path('crear_horario/', views.crear_horario, name='crear_horario'),
]